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
     "apikey":      "5jggokgpepnvsb2uv4s40d59ov",
     "cbroker":     "http://orion:1026",
     "entity_type": "Thing2",
     "resource":    "/iot/d" # URL where devices send data. It is required but it seems that cannot be changed
                             # https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html 
   }
 ]
}

# If we try to use again the same API key, we obtain duplicated group error. We have to change the key
# Somehow, API keys are used to identify groups
newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+IOTAGENT_HOST+':4041/iot/services',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)

# Provisioning a device (sensor+commands)
# Note that no information about the device group is provided (this is done when sending measurement)
# This only creates the BROKER entity associated to the physical device
json_dict={
 "devices": [
   {
     "device_id":   "vehicle001",
     "entity_name": "urn:ngsi-ld:Vehicle:001",
     "entity_type": "Vehicle",
     "timezone":    "Europe/Berlin",
     "attributes": [
       { "object_id": "s", "name": "speed", "type": "Number" },
       { "object_id": "r", "name": "rpm", "type": "Number" }
     ],
     #"protocol": "PDI-IoTA-UltraLight",
     #"transport": "HTTP",
     #"endpoint": "http://"+YOUR_IP+":80/vehicle001", If we can "act" as server
     "commands": [ 
        { "name": "cmd", "type": "command" }
     ]
   }
 ]
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
response = requests.post('http://'+IOTAGENT_HOST+':7896/iot/d?k=5jggokgpepnvsb2uv4s40d59ov&i=vehicle001',
                         data='s|80#r|2000',
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)

# Querying data
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Vehicle:001'
response=requests.get(url,headers=newHeaders)
response.encoding='utf-8'

print(response.text)

rpm=2000
while True:
  # Checking pending commands (polling from the device) or checking when sending measurement
  print('Checking command')

  #newHeaders = {'Content-type': 'text/plain'}
  #response = requests.get('http://'+IOTAGENT_HOST+':7896/iot/d?k=5jggokgpepnvsb2uv4s40d59ov&i=vehicle001&getCmd=1',
  #                       headers=newHeaders)
  #print("Status code: ", response.status_code)
  #print(response.text)

  newHeaders = {'Content-type': 'text/plain'}
  response = requests.post('http://'+IOTAGENT_HOST+':7896/iot/d?k=5jggokgpepnvsb2uv4s40d59ov&i=vehicle001&getCmd=1',
                         data='s|80#r|'+str(rpm),
                         headers=newHeaders)
  print("Status code: ", response.status_code)
  print(response.text)

  if len(response.text)>0: # Command received
    cresponse=response.text[:response.text.find("|")+1]+"cmd OK"
    print('Sending response: '+cresponse)

    # Query command status (it should be PENDING)
    newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
    url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Vehicle:001?options=keyValues'
    response=requests.get(url,headers=newHeaders)
    response.encoding='utf-8'
    print(response) 
    print(response.content) 

    # Sending response
    newHeaders = {'Content-type': 'text/plain'}
    response = requests.post('http://'+IOTAGENT_HOST+':7896/iot/d?k=5jggokgpepnvsb2uv4s40d59ov&i=vehicle001',
                         data=cresponse,                       
                         headers=newHeaders)
    print("Status code: ", response.status_code)
    print(response.text)

    # Query command status (it should be OK)
    newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
    url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Vehicle:001?options=keyValues'
    response=requests.get(url,headers=newHeaders)
    response.encoding='utf-8'
    print(response) 
    print(response.content) 

  rpm=rpm+1
  sleep(5)

