import requests
import json
from flask import Flask,request
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')
YOUR_IP = '192.168.1.95' # Replace with the IP where you execute this script (e.g. ifconfig or hostname -i)

app = Flask(__name__)

@app.route("/subscription/temperature-change",methods=['POST'])
def changes():
    print('Change received: ')
    print(request.data)
    return "Received"


# Create entity
json_dict={
    "id": "urn:ngsi-ld:Termometer:001",
    "type": "Device",
    "temperature": { "type": "Number", "value": 25.0},
    "humidity": { "type": "Number", "value": 80.0},
}

newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}
response = requests.post('http://'+ORION_HOST+':1026/v2/entities',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)

# Create subscription
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
      "url": "http://"+YOUR_IP+":3000/subscription/temperature-change"
    },
    "attrs": [ "temperature" ] # Only temperature attribute is notified
  }
}

newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}
response = requests.post('http://'+ORION_HOST+':1026/v2/subscriptions',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)