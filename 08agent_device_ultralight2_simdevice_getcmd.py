# This example simulates a device sending measurements
# and using getcmd to recover commands
import requests
import os
from time import sleep

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')


rpm=2000
while True:
  # new measurement and ask for commands
  newHeaders = {'Content-type': 'text/plain'}
  response = requests.post('http://'+IOTAGENT_HOST+':7896/iot/d?k=8jggokgpepnvsb2uv4s40d59ov&i=vehicle008&getCmd=1',
                         data='s|80#r|'+str(rpm),
                         headers=newHeaders)
  print("Status code: ", response.status_code)
  print(response.text)

  if len(response.text)>0: # Command received
    cresponse=response.text[:response.text.find("|")+1]+"cmd OK"
    print('Sending response: '+cresponse)

    sleep(5)

    # Query command status (it should be DELIVERED)
    newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
    url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Vehicle:008?options=keyValues'
    response=requests.get(url,headers=newHeaders)
    response.encoding='utf-8'
    print(response) 
    print(response.content) 

    # Sending response
    newHeaders = {'Content-type': 'text/plain'}
    response = requests.post('http://'+IOTAGENT_HOST+':7896/iot/d?k=8jggokgpepnvsb2uv4s40d59ov&i=vehicle008',
                         data=cresponse,                       
                         headers=newHeaders)
    print("Status code: ", response.status_code)
    print(response.text)

    # Query command status (it should be OK)
    newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
    url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Vehicle:008?options=keyValues'
    response=requests.get(url,headers=newHeaders)
    response.encoding='utf-8'
    print(response) 
    print(response.content) 

  rpm=rpm+1
  sleep(5)

