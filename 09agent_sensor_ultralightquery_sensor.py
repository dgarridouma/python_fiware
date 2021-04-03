# Example just to check measurements when using (mostly) a NodeMCU
import requests
import json
from flask import Flask,request
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')

# Querying data
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Motion:001?type=Motion'
response=requests.get(url,headers=newHeaders)
response.encoding='utf-8'

print(response.text)

