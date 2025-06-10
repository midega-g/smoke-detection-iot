import csv
import time
import json
from datetime import datetime, timezone
from paho.mqtt import client as mqtt_client


MQTT_BROKER = "mqtt.eclipseprojects.io"
TOPIC = "smoke_detector"
client = mqtt_client.Client()
client.connect(MQTT_BROKER)


def generate_data():
    with open('data/smoke_detection_iot.csv', encoding='utf-8') as file:
        data = csv.DictReader(file)
        for row in data:
            # Convert numeric fields to float/int
            for key in row:
                if key != "timestamp" and row[key].replace('.', '', 1).isdigit():
                    row[key] = float(
                        row[key]) if '.' in row[key] else int(row[key])

            # Add UTC timestamp
            row["timestamp"] = int(datetime.now(timezone.utc).timestamp())
            yield row
            time.sleep(5)


for entry in generate_data():
    payload = json.dumps(entry)
    client.publish(TOPIC, payload)
    print(f"Published {payload} to topic {TOPIC}")
