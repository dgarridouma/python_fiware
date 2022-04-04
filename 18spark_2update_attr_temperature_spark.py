# This example is just to control how many measurements are sent (Logger example) with a constant value (MinTemp example)
# For instance, if you launch this example 3 times, Logger should show 3 and the minimum temperature is always the constant value (MinTemp)
import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

json_dict={
#    "id": "urn:ngsi-ld:Termometer:003",
#    "type": "Device",
    "temperature": { "type": "Number", "value": 29.0} # A constant value just to test everything is Ok.
}
  
newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.put('http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Termometer:003/attrs', data=json.dumps(json_dict), headers=newHeaders)
# Update is shown in the Spark job log
# success code - 204
print(response) 
  
print(response.content) 
