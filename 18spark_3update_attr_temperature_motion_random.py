import requests
import json
import os
import random
from time import sleep

ORION_HOST = os.getenv('ORION_HOST','localhost')

while True:
  json_dict={
  #    "id": "urn:ngsi-ld:Termometer:003",
  #    "type": "Device",
      "temperature": { "type": "Number", "value": random.randint(0,30)},
      "motion": { "type": "Number", "value": random.randint(0,1)}
  }
  
  newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
  response = requests.put('http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Termometer:003/attrs', data=json.dumps(json_dict), headers=newHeaders)
  # Update is shown in the Spark job log
  # success code - 204
  print(response) 
  
  print(response.content) 
  print(json_dict['temperature'],json_dict['motion'])
  sleep(1)
