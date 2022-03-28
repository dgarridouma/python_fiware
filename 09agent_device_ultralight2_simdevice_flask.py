# This example simulates a device sending measurements
# and using Flask to receive commands
import requests
from flask import Flask,request
import os
from time import sleep
from threading import Thread

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')

app = Flask(__name__)

@app.route("/vehicle009",methods=['POST'])
def changes():
    print('Command received: ')
    res=request.data.decode()
    print(res)
    sleep(5)
    res=res[:res.find("|")+1]+"vehicle OK" # this is needed to confirm command is finished
    print(res)
    return res

def send_measurement():
    rpm=2000
    while True:
        # new measurement
        newHeaders = {'Content-type': 'text/plain'}
        response = requests.post('http://'+IOTAGENT_HOST+':7896/iot/d?k=9jggokgpepnvsb2uv4s40d59ov&i=vehicle009',
                         data='s|80#r|'+str(rpm),
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
