from paho.mqtt import client as mqtt_client

def on_message(client, userdata, message):
    print(f"Recived message: {str(message.payload.decode('utf-8'))}")
    

MQTT_BROKER = "mqtt.eclipseprojects.io"
TOPIC = "smoke_detector"
client = mqtt_client.Client()

client.on_message = on_message
client.connect(MQTT_BROKER)
client.subscribe(TOPIC)
client.loop_forever()
# client.loop_stop()