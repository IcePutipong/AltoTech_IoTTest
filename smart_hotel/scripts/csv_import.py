import csv, os, time, django, sys
from datetime import datetime, timezone
from crate import client


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_hotel.settings')
django.setup()

from IoT_sensor.models import SensorData

def connect_cratedb():
    try:
        connection = client.connect("http://localhost:4200", error_trace=True)
        return connection.cursor()
    except Exception as e:
        print(f"Error connecting to Cratedb: {e}")
        return None
    
def validate_data(datapoint, value):
    if datapoint == 'temperature':
        if value < 22:
            value = 22.0
        elif value > 32:
            value = 32.0
    elif datapoint == 'humidity':
        if value < 30:
            value = 30.0
        elif value > 70:
            value = 70.0
    elif datapoint == 'co2':
        if value < 400:
            value = 400.0
        elif value > 2000:
            value = 2000.0
    return value

def save_data_django(csv_datetime, device_id,datapoint, value, timestamp):
    try:
        SensorData.objects.create(datetime=csv_datetime, device_id=device_id, datapoint=datapoint, value=value, timestamp=timestamp)
    except Exception as e:
        print(f"ERROR to save the data: {e}")

def save_data_cratedb(csv_datetime, device_id, datapoint, value, timestamp, cursor):
    try:
        timestamp_str = timestamp.isoformat()

        cursor.execute("""
            INSERT INTO raw_data (datetime, device_id, datapoint, value, timestamp) 
            VALUES(?, ?, ?, ?, ?)""", [csv_datetime, device_id, datapoint, value, timestamp_str])
    except Exception as e:
        print (f"ERROR uploading data to CrateDB: {e}")

def process_csv(file_path, cursor):
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                device_id = "device-01"
                timestamp = datetime.now(timezone.utc)
                csv_datetime = row['timestamp']

                
                for datapoint in ['temperature', 'humidity', 'co2']:
                    try:
                        value = float(row[datapoint])
                        value = validate_data(datapoint, value)

                        if value is not None:
                            save_data_django(csv_datetime, device_id, datapoint, value, timestamp)
                            save_data_cratedb(csv_datetime, device_id, datapoint, value, timestamp, cursor)
                    except KeyError:
                        print(f"Datapoint {datapoint} is missing in the CSV file.")
                    except ValueError:
                        print(f"Invalid value for {datapoint}: {row[datapoint]}")
                        continue  
                
                time.sleep(5)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError as ioe:
        print(f"Error reading file: {file_path} - {ioe}")
    except Exception as e:
        print(f"Error connecting to Cratedb: {e}")

if __name__ == "__main__":
    cursor = connect_cratedb()

    if cursor: 
        current_dir = os.path.dirname(os.path.realpath(__file__))
        csv_file_path = os.path.join(current_dir, 'data', 'mock_iaq_data.csv')

        process_csv(csv_file_path, cursor)
    else:
        print("Failed to connect to Cratedb. Exit...")