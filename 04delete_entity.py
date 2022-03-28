import requests
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Store:001'
response=requests.delete(url)
print(response)
