# This examples is justo to check the status of commands sent when used in a NodeMCU
import requests
import json
import os

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
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://localhost:1026/v2/entities/urn:ngsi-ld:Bell:001?type=Bell&options=keyValues'
response=requests.get(url,headers=newHeaders)
response.encoding='utf-8'
print(response) 
print(response.content) 
