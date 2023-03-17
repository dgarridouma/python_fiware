# This example simulates a device sending measurements
# and using Flask to receive commands
import os
import paho.mqtt.client as mqtt
import time
from time import sleep

MQTT_HOST= os.getenv('MQTT_HOST','localhost')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe("/11jggokgpepnvsb2uv4s40d59ov/vehicle011/cmd")

# The callback for when a PUBLISH message is received from the server.
def on_publish(client, userdata, mid):
    print("Published: "+str(mid))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    res=msg.payload.decode()
    print(res)
    sleep(5) # working
    res=res[:res.find("|")+1]+"cmd OK" # this is needed to confirm command is finished    
    print(res)
    client.publish("/11jggokgpepnvsb2uv4s40d59ov/vehicle011/cmdexe", res, qos=0, retain=False)



# Simulate a measurement
# docker run -it --rm --name mqtt-publisher --network varios_default efrecon/mqtt-client pub -h mosquitto -m "c|1" -t "/4jggokgpepnvsb2uv4s40d59ov/motion001/attrs"

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

#client.tls_set()
client.connect(MQTT_HOST, 1883, 60)
client.loop_start()

i=0
while True:
    print(i)
    msg="s|80#r|"+str(i)
    i=i+1

    client.publish("/11jggokgpepnvsb2uv4s40d59ov/vehicle011/attrs", msg, qos=0, retain=False)
    time.sleep(1)

