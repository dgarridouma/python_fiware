# Provisioning a group and sensor (can be also combined with a NodeMCU)
import requests
import json
from flask import Flask,request
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')

# Provisioning a group service
# This example provisions an anonymous group of devices.
json_dict={
  "services": [
   {
     "apikey":      "4jggokgpepnvsb2uv4s40d59ov",
     "cbroker":     "http://orion:1026",
     "entity_type": "Thing",
     "resource":    "/iot/d" # URL where devices send data. It is required but it seems that cannot be changed
                             # https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html 
   }
 ]
}

# If we try to use again the same API key, we obtain duplicated group error.
newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+IOTAGENT_HOST+':4041/iot/services',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)

# Provisioning a sensor
# Note that no information about the device group is provided (this is done when sending measurement)
# This only creates the BROKER entity associated to the physical device
json_dict={
 "devices": [
   {
     "device_id":   "room001",
     "entity_name": "urn:ngsi-ld:Room:001",
     "entity_type": "Motion",
     "timezone":    "Europe/Berlin",
     "attributes": [
       { "object_id": "h", "name": "temperature", "type": "Integer", "entity_name": "dev:temp1","entity_type": "Device" },
       { "object_id": "t", "name": "humidity", "type": "Integer", "entity_name": "dev:hum1","entity_type": "Device"},
     ],
   }
 ]
 # commands can be also included
}

newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+IOTAGENT_HOST+':4041/iot/devices',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)

# Simulate a measurement (PORT 7896)
# Be careful! If we use a non-existing id, the request also returns a 200 code because an entity is created with that id
# and entity name Thing:id-used
newHeaders = {'Content-type': 'text/plain'}
response = requests.post('http://'+IOTAGENT_HOST+':7896/iot/d?k=4jggokgpepnvsb2uv4s40d59ov&i=room001',
                         data='h|80#t|25',
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)

# Querying data
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://'+ORION_HOST+':1026/v2/entities/dev:temp1'
response=requests.get(url,headers=newHeaders)
response.encoding='utf-8'

print(response.text)


# Querying data
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://'+ORION_HOST+':1026/v2/entities/dev:hum1'
response=requests.get(url,headers=newHeaders)
response.encoding='utf-8'

print(response.text)

