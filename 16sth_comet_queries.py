import requests
import json
import os

COMET_HOST = os.getenv('COMET_HOST','localhost')

print('First N Sampled Values')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'hLimit':3, 'hOffset':0}
url = 'http://'+COMET_HOST+':8666/STH/v1/contextEntities/type/Device/id/urn:ngsi-ld:Termometer:001/attributes/temperature'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
#parsed=json.loads(response.text)
#print(json.dumps(parsed,indent=4))
print(response.text)
input('press ENTER')

print('First N Sampled Values at an offset')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'hLimit':3, 'hOffset':3}
url = 'http://'+COMET_HOST+':8666/STH/v1/contextEntities/type/Device/id/urn:ngsi-ld:Termometer:001/attributes/temperature'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)
input('press ENTER')


print('Latest N Sampled Values')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'lastN':3}
url = 'http://'+COMET_HOST+':8666/STH/v1/contextEntities/type/Device/id/urn:ngsi-ld:Termometer:001/attributes/temperature'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)
input('press ENTER')


print('Sum over a time period') # mean value is not supported
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'aggrMethod': 'sum', 'aggrPeriod': 'minute'}
url = 'http://'+COMET_HOST+':8666/STH/v1/contextEntities/type/Device/id/urn:ngsi-ld:Termometer:001/attributes/motion'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)
input('press ENTER')

print('Min over a time period') # mean value is not supported
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'aggrMethod': 'min', 'aggrPeriod': 'day'}
url = 'http://'+COMET_HOST+':8666/STH/v1/contextEntities/type/Device/id/urn:ngsi-ld:Termometer:001/attributes/temperature'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)
input('press ENTER')

