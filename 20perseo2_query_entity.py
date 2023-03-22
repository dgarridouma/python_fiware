# This example creates a group service and a device waiting
# for data from a device using getcmd
import requests
import json
import os
from time import sleep

ORION_HOST = os.getenv('ORION_HOST','localhost')

while True:
  # Querying data
  newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
  url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Termometer:005?options=keyValues'
  response=requests.get(url,headers=newHeaders)
  response.encoding='utf-8'

  print(response.text)
  sleep(1)
