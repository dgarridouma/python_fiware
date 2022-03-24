import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

print('QUERYING ALL ENTITIES')
url = 'http://'+ORION_HOST+':1026/v2/entities'
response=requests.get(url)
response.encoding='utf-8'

print(response.text)
input('press ENTER')

print('OBTAIN ENTITY DATA BY ID')
url = 'http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Store:001?type=Store'
response=requests.get(url)
response.encoding='utf-8'

print(response.text)
input('press ENTER')

print('OBTAIN ENTITY DATA BY TYPE')
# Because of the use of the options=keyValues, the response consists of JSON only without the attribute type and metadata elements.
url = 'http://'+ORION_HOST+':1026/v2/entities?type=Store&options=keyValues'
response=requests.get(url)
response.encoding='utf-8'

print(response.text)
input('press ENTER')

print('FILTER CONTEXT DATA BY COMPARING THE VALUES OF AN ATTRIBUTE')
url = 'http://'+ORION_HOST+':1026/v2/entities'

# If we have several parameters, we can use dparams
dparams={}
dparams['type']='Store'
dparams['q']="name=='Checkpoint Markt'"
dparams['options']='keyValues'

response=requests.get(url, params=dparams)
response.encoding='utf-8'

print(response.text)
input('press ENTER')


print('FILTER CONTEXT DATA BY COMPARING THE VALUES OF A SUB-ATTRIBUTE')
url = 'http://'+ORION_HOST+':1026/v2/entities'

dparams={}
dparams['type']='Store'
dparams['q']="address.addressLocality==Kreuzberg"
dparams['options']='keyValues'

response=requests.get(url, params=dparams)
response.encoding='utf-8'

print(response.text)
input('press ENTER')

print('FILTER CONTEXT DATA BY QUERYING METADATA')
url = 'http://'+ORION_HOST+':1026/v2/entities'

dparams={}
dparams['type']='Store'
dparams['mq']="address.verified==true"
dparams['options']='keyValues'

response=requests.get(url, params=dparams)
response.encoding='utf-8'

print(response.text)
input('press ENTER')

print('FILTER CONTEXT DATA BY COMPARING THE VALUES OF A GEO:JSON ATTRIBUTE')
# This example return all Stores within 1.5km the Brandenburg Gate in Berlin (52.5162N 13.3777W)
url = 'http://'+ORION_HOST+':1026/v2/entities'

dparams={}
dparams['type']='Store'
dparams['georel']="near;maxDistance:1500"
dparams['geometry']="point"
dparams['coords']="52.5162,13.3777"
dparams['options']='keyValues'

response=requests.get(url, params=dparams)
response.encoding='utf-8'

print(response.text)