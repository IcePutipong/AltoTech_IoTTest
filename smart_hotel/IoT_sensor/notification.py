import time
from audioop import avg
import requests
from datetime import timedelta
from django.utils import timezone
from IoT_sensor.models import SensorData

LINE_NOTIFY_API = "https://notify-api.line.me/api/notify"
LINE_NOTIFY_TOKEN = "1C7VDLmC6Q6xvCsaNCNr2jBTPo2TiHgONl7klcCmixN"

def check_iaq_conditions():
    now = timezone.now()
    five_minutes_ago = now - timedelta(minutes=5)

    sensor_data = SensorData.objects.filter(timestamp__gte=five_minutes_ago)

    if not sensor_data.exists():
        print("No data available for the last 5 minutes.")
        return

    avg_temp = sensor_data.filter(datapoint='temperature').aggregate(avg('value'))['value__avg']
    avg_humidity = sensor_data.filter(datapoint='humidity').aggregate(avg('value'))['value__avg']
    avg_co2 = sensor_data.filter(datapoint='co2').aggregate(avg('value'))['value__avg']

    if avg_temp < 23 or avg_temp > 26 or avg_humidity < 40 or avg_humidity > 50 or avg_co2 >= 1000:
        message = f"Discomfort detected!\nTemp: {avg_temp}°C, Humidity: {avg_humidity}%, CO2: {avg_co2} ppm"
        send_line_notify(message)

def send_line_notify(message):
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"
    }
    data = {"message": message}
    response = requests.post(LINE_NOTIFY_API, headers=headers, data=data)

    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification: {response.status_code}")

def run_periodically():
    while True:
        check_iaq_conditions()
        time.sleep(60)  

if __name__ == "__main__":
    run_periodically()  
