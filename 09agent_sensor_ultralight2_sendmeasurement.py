import requests
import json
import os
from time import sleep

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')


# Simulate a measurement (PORT 7896)
# Be careful! If we use a non-existing id, the request also returns a 200 code because an entity is created with that id
# and entity name Thing:id-used
newHeaders = {'Content-type': 'text/plain'}

count=1
while True:
  response = requests.post('http://'+IOTAGENT_HOST+':7896/iot/d?k=4jggokgpepnvsb2uv4s40d59ov&i=motion001',
                         data='c|'+str(count),
                         headers=newHeaders)
  print("Status code: ", response.status_code)
  print(response.text)
  count+=1
  sleep(5)


