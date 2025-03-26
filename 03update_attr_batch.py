import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

json_dict= {
  "actionType": "update",
  "entities": [
    {
        "type": "Store",
        "id": "urn:ngsi-ld:Store:001",
        "category": {"type":"Text", "value": "categoryUpdatedBatch"},
        "stars": {"type": "Number", "value": 7}
    },    
    {
        "type": "Store",
        "id": "urn:ngsi-ld:Store:002",
        "name": {"type":"Text", "value": "name updated"},
        # "specialOfferBatch": {"value": True} # new attributes cannot be added
    }
  ]
}
  
newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}
response = requests.post('http://'+ORION_HOST+':1026/v2/op/update', data=json.dumps(json_dict), headers=newHeaders)

# success code - 204
print(response) 
  
print(response.content) 
