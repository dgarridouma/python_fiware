import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')
PERSEO_HOST = os.getenv('PERSEO_HOST','localhost')

# Create entity
json_dict={
    "id": "urn:ngsi-ld:Termometer:004",
    "type": "Device",
    "temperature": { "type": "Number", "value": 25.0},
    "motion": { "type": "Number", "value": 0.0},
    "abnormal": { "type": "Boolean", "value": False},
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
    "id": "urn:ngsi-ld:Termometer:005",
    "type": "Device",
    "temperature": { "type": "Number", "value": 15.0},
    "motion": { "type": "Number", "value": 0.0},
    "abnormal": { "type": "Boolean", "value": False},
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


# Create rule
json_dict={
    "name": "temp_rule_update",
    "text": "select *,\"temp_rule_update\" as ruleName from pattern [every ev=iotEvent(cast(cast(temperature?,String),float)>25.0 and type=\"Device\")]",
    "action": {
        "type": "update",
        "parameters": {
            "attributes": [
                {
                    "name": "abnormal",
                    "value": True,
                    "type": "Boolean"
                }
            ]
        }
    }
}

newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json','fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+PERSEO_HOST+':9090/rules/',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)


# Create subscription for perseo-fe
json_dict={
  "description": "Notify me of all temperature changes",
  "subject": {
    "entities": [{"idPattern": ".*", "type": "Device"}],
    "condition": {
      "attrs": [ "temperature" ] # Fired when temperature changes. If empty, every change on every attribute is notified
    }
  },
   "notification": {
    "http": {
        # If we use orion in a container, we cannot use 'localhost' because localhost it is used by the container
        # We have to replace with our own IP (e.g. ipconfig)
      "url": "http://"+"perseo-fe"+":9090/notices"
    }
  }
}

newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json','fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+ORION_HOST+':1026/v2/subscriptions',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)

newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json','fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.get('http://'+"localhost"+':9090/rules',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)
