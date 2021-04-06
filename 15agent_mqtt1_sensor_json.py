import requests
import json
import os
import paho.mqtt.client as mqtt
import time
import json

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')
MQTT_HOST= os.getenv('MQTT_HOST','localhost')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_publish(client, userdata, mid):
    print("Published: "+str(mid))


# Provisioning a group service
# When using MQTT it seems that only a group (the first) is automatically used for sending commands!

json_dict={
  "services": [
   {
     "apikey":      "4jggokgpepnvsb2uv4s40d59ov",
     "cbroker":     "http://orion:1026",
     "entity_type": "Thing",
     "resource":    "" # not needed for MQTT "/iot/d"
   }
 ]
}

newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+IOTAGENT_HOST+':4041/iot/services',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)


# Provisioning a sensor

json_dict={
 "devices": [
   {
     "device_id":   "motion001",
     "entity_name": "urn:ngsi-ld:Motion:001",
     "entity_type": "Motion",
     "protocol": "IoTA-JSON",
     "transport":   "MQTT",                 # This is not specified when using http
     "timezone":    "Europe/Berlin",
     "attributes": [
       { "object_id": "c", "name": "count", "type": "Integer" }
     ],
   }
 ]
}

newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+IOTAGENT_HOST+':4041/iot/devices',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)

# Simulate a measurement
# docker run -it --rm --name mqtt-publisher --network varios_default efrecon/mqtt-client pub -h mosquitto -m "c|1" -t "/4jggokgpepnvsb2uv4s40d59ov/motion001/attrs"

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
#client.tls_set()
client.connect(MQTT_HOST, 1883, 60)
client.loop_start()

for i in range(3):
    print(i)
    msg=dict()
    msg["c"]=str(i)
    print(json.dumps(msg))
    client.publish("/json/4jggokgpepnvsb2uv4s40d59ov/motion001/attrs", json.dumps(msg), qos=0, retain=False)
    time.sleep(1)

client.disconnect()

# Querying data
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Motion:001?type=Motion'
response=requests.get(url,headers=newHeaders)
response.encoding='utf-8'

print(response.text)

