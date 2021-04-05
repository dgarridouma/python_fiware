import requests
import json
import os
import random

ORION_HOST = os.getenv('ORION_HOST','localhost')

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
