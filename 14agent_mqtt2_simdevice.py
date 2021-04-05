# This examples is just to send data to example 14agent_mqtt_device_provisioning.py as alternative to NodeMCU
# The group must be created before

import requests
import json
import os
import paho.mqtt.client as mqtt
import time

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')
MQTT_HOST= os.getenv('MQTT_HOST','localhost')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe("/4jggokgpepnvsb2uv4s40d59ov/vehicle002/cmd")

# The callback for when a PUBLISH message is received from the server.
def on_publish(client, userdata, mid):
    print("Published: "+str(mid))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    res=msg.payload.decode()
    print(res)
    res=res[:res.find("|")+1]+"cmd OK" # this is needed to confirm command is finished    
    print(res)
    client.publish("/4jggokgpepnvsb2uv4s40d59ov/vehicle002/cmdexe", res, qos=0, retain=False)



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

    client.publish("/4jggokgpepnvsb2uv4s40d59ov/vehicle002/attrs", msg, qos=0, retain=False)
    time.sleep(1)

    # Querying data
    newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
    url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Vehicle:002?type=Vehicle&options=keyValues'
    response=requests.get(url,headers=newHeaders)
    response.encoding='utf-8'

    print(response.text)

