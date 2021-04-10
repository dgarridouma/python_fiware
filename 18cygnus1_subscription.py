import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

# Create entity
json_dict={
    "id": "urn:ngsi-ld:Termometer:001",
    "type": "Device",
    "temperature": { "type": "Number", "value": 25.0},
    "motion": { "type": "Number", "value": 0.0}
}

newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json','fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+ORION_HOST+':1026/v2/entities',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)

# Create subscription
json_dict={
  "description": "Notify Cygnus of all context changes",
  "subject": {
    "entities": [{"idPattern": ".*"}]
  },
"notification": {
    "http": {
      "url": "http://cygnus:5051/notify"
    }
  },
#  "throttling": 5
}

newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+ORION_HOST+':1026/v2/subscriptions',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)
# Use next example to insert data and then:
# docker run -it --network docker_default --entrypoint /bin/bash mongo
# A shell opens:
# mongo --host mongo-db
# show dbs
# use sth_openiot
# show collections
# db["sth_/_urn:ngsi-ld:Termometer:001_Device"].find().limit(10);
