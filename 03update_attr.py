import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

json_dict={
    "category": {"type":"Text", "value": "categoryUpdated"},
    "stars": {"type": "Number", "value": 6},
    "specialOffer": {"value": True}  # new attribute
}
  
newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}
response = requests.post('http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Store:001/attrs', data=json.dumps(json_dict), headers=newHeaders)
# if we use requests.put (instead requests.post), attributes are replaced by the used at the request

# success code - 204
print(response) 
  
print(response.content) 
