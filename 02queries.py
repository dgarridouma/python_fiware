import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

print('Querying all entities')
url = 'http://'+ORION_HOST+':1026/v2/entities'
response=requests.get(url)
response.encoding='utf-8'

print(response.text)

print('OBTAIN ENTITY DATA BY ID')
url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Store:001?type=Store'
response=requests.get(url)
response.encoding='utf-8'

print(response.text)

print('OBTAIN ENTITY DATA BY TYPE')
# Because of the use of the options=keyValues, the response consists of JSON only without the attribute type and metadata elements.
url = 'http://'+ORION_HOST+':1026/v2/entities?type=Store&options=keyValues'
response=requests.get(url)
response.encoding='utf-8'

print(response.text)

print('FILTER CONTEXT DATA BY COMPARING THE VALUES OF AN ATTRIBUTE')
# it can be URL encoded and held within single quote characters ' = %27
url = 'http://'+ORION_HOST+':1026/v2/entities?type=Store&q=name==%27Checkpoint%20Markt%27&options=keyValues'
response=requests.get(url)
response.encoding='utf-8'

print(response.text)

print('FILTER CONTEXT DATA BY COMPARING THE VALUES OF A SUB-ATTRIBUTE')
url = 'http://'+ORION_HOST+':1026/v2/entities?type=Store&q=address.addressLocality==Kreuzberg&options=keyValues'
response=requests.get(url)
response.encoding='utf-8'

print(response.text)

print('FILTER CONTEXT DATA BY QUERYING METADATA')
url = 'http://'+ORION_HOST+':1026/v2/entities?type=Store&mq=address.verified==true&options=keyValues'
response=requests.get(url)
response.encoding='utf-8'

print(response.text)

print('FILTER CONTEXT DATA BY COMPARING THE VALUES OF A GEO:JSON ATTRIBUTE')
# This example return all Stores within 1.5km the Brandenburg Gate in Berlin (52.5162N 13.3777W)
url = 'http://'+ORION_HOST+':1026/v2/entities?type=Store&georel=near;maxDistance:1500&geometry=point&coords=52.5162,13.3777&options=keyValues'
response=requests.get(url)
response.encoding='utf-8'

print(response.text)