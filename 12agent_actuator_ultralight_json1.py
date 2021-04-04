import requests
import json
from flask import Flask,request
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')
YOUR_IP = '192.168.1.95'

app = Flask(__name__)

@app.route("/bell001",methods=['POST'])
def changes():
    print('Command received: ')
    print(request.data.decode())
    dres=json.loads(request.data.decode())
    dres["ring"]=" ring OK"
    res=json.dumps(dres) 
    print(res)
    return res



# Provisioning an actuator

json_dict={
  "devices": [
    {
      "device_id": "bell001",
      "entity_name": "urn:ngsi-ld:Bell:001",
      "entity_type": "Bell",
      "protocol": "PDI-IoTA-UltraLight",
      "transport": "HTTP",
      "endpoint": "http://"+YOUR_IP+":3000/bell001",
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
