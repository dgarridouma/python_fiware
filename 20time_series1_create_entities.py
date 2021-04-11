import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

# Create entity
json_dict={
    "id": "urn:ngsi-ld:Termometer:001",
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
    "id": "urn:ngsi-ld:Termometer:002",
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



# Create subscription
json_dict={
  "description": "Notify QuantumLeap of all context changes",
  "subject": {
    "entities": [{"idPattern": ".*"}]
  },
"notification": {
    "http": {
      "url": "http://quantumleap:8668/v2/notify"  
    },
 "attrs": [
      "temperature","motion","location"
    ],
  "metadata": ["dateCreated", "dateModified"]  
  },
  "throttling": 1
}

newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+ORION_HOST+':1026/v2/subscriptions',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)

