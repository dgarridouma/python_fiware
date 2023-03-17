# This example creates a group service and a device waiting
# for data from a device using Flask and JSON. The device has to provide
# a URL for listening
import requests
import json
import os
from time import sleep

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')

YOUR_IP = 'YOUR_DEVICE_IP' # Device IP
YOUR_PORT = 'YOUR_PORT' # Device port (e.g. 3000 or 80)

# Provisioning a group service
# This example provisions an anonymous group of devices.
json_dict={
  "services": [
   {
     "apikey":      "10jggokgpepnvsb2uv4s40d59ov",
     "cbroker":     "http://orion:1026",
     "entity_type": "Thing",
     "resource":    "/iot/json" # URL where devices send data. It is required but it seems that cannot be changed
                             # https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html 
   }
 ]
}

# If we try to use again the same API key, we obtain duplicated group error.
newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+IOTAGENT_HOST+':4041/iot/services',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)

# Provisioning a device
# Note that no information about the device group is provided (this is done when sending measurement)
# This only creates the BROKER entity associated to the physical device
json_dict={
 "devices": [
   {
     "device_id":   "vehicle010",
     "entity_name": "urn:ngsi-ld:Vehicle:010",
     "entity_type": "Vehicle",
     "timezone":    "Europe/Berlin",
     "attributes": [
       { "name": "speed", "type": "Number" }, # object s removed (optional) https://iotagent-node-lib.readthedocs.io/en/2.13.0/api/index.html
       { "name": "rpm", "type": "Number" } # object r removed (optional)
     ],
     "protocol": "PDI-IoTA-UltraLight",
     "transport": "HTTP",
     "endpoint": "http://"+YOUR_IP+":"+YOUR_PORT+"/vehicle010",
     "commands": [ 
        { "name": "cmd", "type": "command" }
     ]
   }
 ]
}

newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+IOTAGENT_HOST+':4041/iot/devices',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)


# Querying data
while True:
    newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
    url = 'http://localhost:1026/v2/entities/urn:ngsi-ld:Vehicle:010?options=keyValues'
    response=requests.get(url,headers=newHeaders)
    response.encoding='utf-8'
    print(response) 
    print(response.content) 
    sleep(1)
