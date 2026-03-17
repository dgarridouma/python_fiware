# Send command to devices of #10 examples
import requests
import json
import os
import random

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')

# Sending command
json_dict={
  "type" : "command",
  "value" : random.randint(20,30)
}

newHeaders = {'Content-Type': 'application/json','fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Vehicle:010/attrs/cmd?type=Vehicle' # type=Vehicle seems necessary
                                                                                              # to transmit "value"
response=requests.put(url,data=json.dumps(json_dict),headers=newHeaders)
response.encoding='utf-8'
print(response) 
print(response.content) 
