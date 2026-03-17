# This example simulates a device sending measurements
# and using Flask to receive commands
import requests
import json
from flask import Flask,request
import os
from time import sleep
from threading import Thread

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')

app = Flask(__name__)

@app.route("/vehicle010",methods=['POST'])
def changes():
    print('Command received: ')
    print(request.data.decode())
    sleep(3) # Working (Higher times produce a 404 error when sending commands)
             # The error is shown in the process that request the command
             # This doesn't happen with Ultralight agent!
    dres=json.loads(request.data.decode())
    dres["cmd"]=" cmd OK"
    res=json.dumps(dres) 
    print(res)
    return res

def send_measurement():
    rpm=2000
    while True:
        # Simulate a measurement (PORT 7896)
        # Be careful! If we use a non-existing id, the request also returns a 200 code because an entity is created with that id
        # and entity name Thing:id-used
        newHeaders = {'Content-type': 'application/json'}
        response = requests.post('http://'+IOTAGENT_HOST+':7896/iot/json?k=10jggokgpepnvsb2uv4s40d59ov&i=vehicle010',
                         data='{"speed": 80,"rpm": '+str(rpm)+'}',
                         headers=newHeaders)
        print("Status code: ", response.status_code)
        print(response.text)

        rpm=rpm+1
        sleep(5)

if __name__ == "__main__":
    process = Thread(target=send_measurement)
    process.daemon=True
    process.start()
    app.run(host='0.0.0.0', port=3000)
