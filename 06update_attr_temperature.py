import requests
import json
import os
import random

ORION_HOST = os.getenv('ORION_HOST','localhost')

json_dict={
#    "id": "urn:ngsi-ld:Termometer:001",
#    "type": "Device",
    "temperature": { "type": "Number", "value": random.randint(25,30)},
}
  
newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}
response = requests.put('http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Termometer:001/attrs', data=json.dumps(json_dict), headers=newHeaders)

# success code - 204
print(response) 
  
print(response.content) 
