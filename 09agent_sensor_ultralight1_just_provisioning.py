# Provisioning a group and sensor (can be also combined with a NodeMCU)
import requests
import json
import os
from time import sleep

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
     "device_id":   "motion001",
     "entity_name": "urn:ngsi-ld:Motion:001",
     "entity_type": "Motion",
     "timezone":    "Europe/Berlin",
     "attributes": [
       { "object_id": "c", "name": "count", "type": "Integer" }
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

# Querying data
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Motion:001'
while True:
  response=requests.get(url,headers=newHeaders)
  response.encoding='utf-8'
  print(response.text)
  sleep(5)
