import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')
YOUR_IP = '192.168.1.98' # NODEMCU IP

# Provisioning an actuator

json_dict={
  "devices": [
    {
      "device_id": "bell001",
      "entity_name": "urn:ngsi-ld:Bell:001",
      "entity_type": "Bell",
      "protocol": "PDI-IoTA-UltraLight",
      "transport": "HTTP",
        "endpoint": "http://"+YOUR_IP+":80/bell001",
      "commands": [
        { "name": "ring", "type": "command" }
       ],
    }
  ]
}

newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+IOTAGENT_HOST+':4041/iot/devices',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)

