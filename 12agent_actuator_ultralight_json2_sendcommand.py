# This example can be used to send commands to both desktop and NodeMCU actuators
import requests
import json
import os
import random

ORION_HOST = os.getenv('ORION_HOST','localhost')

# We can directly send a command to the IoT Agent:
#curl -iX POST   http://localhost:4041/v2/op/update   -H 'Content-Type: application/json'   -H 'fiware-service: openiot'   -H 'fiware-servicepath: /'   -d '{
#    "actionType": "update",
#    "entities": [
#        {
#            "type": "Bell",
#            "id": "urn:ngsi-ld:Bell:001",
#            "ring" : {
#                "type": "command",
#                "value": ""
#            }
#        }
#    ]
#}'

# Query command status
#newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
#url = 'http://localhost:1026/v2/entities/urn:ngsi-ld:Bell:001?type=Bell&options=keyValues'
#response=requests.get(url,headers=newHeaders)
#response.encoding='utf-8'
#print(response) 
#print(response.content) 


json_dict={
  "type" : "command",
  "value" : str(random.randint(20,30))
}

newHeaders = {'Content-Type': 'application/json','fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Bell:001/attrs/ring?type=Bell'
response=requests.put(url,data=json.dumps(json_dict),headers=newHeaders)
response.encoding='utf-8'
print(response) 
print(response.content) 
