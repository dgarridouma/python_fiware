import requests
import json
import os
import paho.mqtt.client as mqtt
from time import sleep

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')
MQTT_HOST= os.getenv('MQTT_HOST','localhost')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe("/4jggokgpepnvsb2uv4s40d59ov/bell001/cmd")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    res=msg.payload.decode()
    print(res)
    res=res[:res.find("|")+1]+"ring OK" # this is needed to confirm command is finished    
    print(res)
    client.publish("/4jggokgpepnvsb2uv4s40d59ov/bell001/cmdexe", res, qos=0, retain=False)


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



# Provisioning an actuator
# The group must be provisioned before!
# (no explicit association is done when provisioning the device)
json_dict={
  "devices": [
    {
      "device_id": "bell001",
      "entity_name": "urn:ngsi-ld:Bell:001",
      "entity_type": "Bell",
      "protocol": "PDI-IoTA-UltraLight",
      "transport": "MQTT",
      #"endpoint": "http://"+YOUR_IP+":3000/bell001",
      "commands": [
        { "name": "ring", "type": "command" }
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

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.tls_set()
client.connect(MQTT_HOST, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

while True:
    # Querying data
    newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
    url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Bell:001?type=Bell&options=keyValues'
    response=requests.get(url,headers=newHeaders)
    response.encoding='utf-8'

    print(response.text)
    sleep(1)

