import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')

# Sending command
json_dict={
  "cmd": {
      "type" : "command",
      "value" : ""
  }
}

newHeaders = {'Content-Type': 'application/json','fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Vehicle:001/attrs'
response=requests.patch(url,data=json.dumps(json_dict),headers=newHeaders)
response.encoding='utf-8'
print(response) 
print(response.content) 

