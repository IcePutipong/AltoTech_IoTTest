# Smart Hotel IoT Sensor System
This project is an IoT-based sensor monitoring system designed to manage Indoor Air Quality (IAQ) conditions in rooms and notify technicians when the environment falls outside of guest comfort zones. The project leverages Django, CrateDB, and Line Notify to monitor sensor data and automate notifications when discomfort is detected.

# Feature
1. Data Monitoring: Continuously collects temperature, humidity, and CO2 data from IoT sensors deployed in the hotel rooms.
[csv_import File](/smart_hotel/scripts/csv_import.py)
[Mock data file](/smart_hotel/scripts/data/mock_iaq_data.csv)

2. IAQ Condition Monitoring: Periodically checks IAQ conditions over the past 5 minutes and evaluates whether they are within guest comfort ranges.
3. Automated Alerts: Sends real-time notifications via Line Notify to alert technicians when IAQ conditions are outside of comfort ranges.
[Check condition and notification](/smart_hotel/IoT_sensor/notification.py)

Youtube Link https://youtu.be/B23c-5LexCw

## Setup and Running Project
### Prerequisite:
- Python 3.x
- Docker
- Docker-Compose
- Line Notify Token

### Run Django server:
py manage.py runserver

### Run Docker containers:
./deploy.sh


