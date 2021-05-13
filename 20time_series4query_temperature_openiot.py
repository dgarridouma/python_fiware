import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

url = 'http://'+ORION_HOST+':1026/v2/entities'
payload = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response=requests.get(url, headers=payload)
response.encoding='utf-8'

print(response.text)

#url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Temperature:003?type=Device'
#response=requests.get(url)
#response.encoding='utf-8'

#print(response.text)
