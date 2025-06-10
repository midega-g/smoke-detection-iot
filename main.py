
import csv
import time
import json
from datetime import datetime, timezone
from paho.mqtt import client as mqtt_client


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



if __name__ == "__main__":
    
    MQTT_BROKER = "mosquitto"
    MQTT_PORT = 1883
    TOPIC = "smoke_detection"
    client = mqtt_client.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)

    for entry in generate_data():
        print(f"entry{entry}")
        payload = json.dumps(entry)
        print(f"payload{payload}")
        client.publish(TOPIC, payload)
        print(f"Published {payload} to topic {TOPIC}")