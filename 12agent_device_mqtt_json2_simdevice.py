# This example simulates a device sending measurements
# and using Flask to receive commands. JSON is also used
import os
import paho.mqtt.client as mqtt
import time
from time import sleep
import json

MQTT_HOST= os.getenv('MQTT_HOST','localhost')

# The callback is called when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code "+str(reason_code))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe("/12jggokgpepnvsb2uv4s40d59ov/vehicle012/cmd") # json seems not necessary

# The callback is called when a PUBLISH message is received from the server.
def on_publish(client, userdata, mid, reason_code, properties):
    print("Published: "+str(mid))

# The callback is called when a message is received.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    res=json.loads(msg.payload.decode())
    res["cmd"]="cmd OK" # this is needed to confirm command is finished
    sleep(5) # working
    print(res)     
    client.publish("/json/12jggokgpepnvsb2uv4s40d59ov/vehicle012/cmdexe", json.dumps(res), qos=0, retain=False)

# Simulate a measurement
# docker run -it --rm --name mqtt-publisher --network varios_default efrecon/mqtt-client pub -h mosquitto -m "c|1" -t "/4jggokgpepnvsb2uv4s40d59ov/motion001/attrs"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

#client.tls_set()
client.connect(MQTT_HOST, 1883, 60)
client.loop_start()

i=0
while True:
    print(i)
    msg=dict()
    msg["speed"]=80
    msg["rpm"]=str(i)
    print(json.dumps(msg))
    client.publish("/json/12jggokgpepnvsb2uv4s40d59ov/vehicle012/attrs", json.dumps(msg), qos=0, retain=False)

    i=i+1
    time.sleep(1)
