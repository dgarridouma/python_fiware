import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

# Create entity
json_dict={
    "id": "urn:ngsi-ld:Termometer:003",
    "type": "Device",
    "temperature": { "type": "Number", "value": 25.0},
    "motion": { "type": "Number", "value": 0.0},
    "location": {
        "type": "geo:json",
        "value": {
             "type": "Point",
             "coordinates": [-4.25, 36.43]
        }
    }
}

newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json','fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+ORION_HOST+':1026/v2/entities',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)


# Create entity
json_dict={
    "id": "urn:ngsi-ld:Termometer:004",
    "type": "Device",
    "temperature": { "type": "Number", "value": 15.0},
    "motion": { "type": "Number", "value": 0.0},
    "location": {
        "type": "geo:json",
        "value": {
             "type": "Point",
             "coordinates": [-3.41, 40.25]
        }
    }
}

newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json','fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+ORION_HOST+':1026/v2/entities',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)

