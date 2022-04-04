import requests
import json
import os

QUANTUMLEAP_HOST = os.getenv('QUANTUMLEAP_HOST','localhost')

print('First N Sampled Values')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'offset':3, 'limit':3}
url = 'http://'+QUANTUMLEAP_HOST+':8668/v2/entities/urn:ngsi-ld:Termometer:003/attrs/temperature'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)


print('Last N Sampled Values')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'lastN':3}
url = 'http://'+QUANTUMLEAP_HOST+':8668/v2/entities/urn:ngsi-ld:Termometer:003/attrs/temperature'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)

print('Sum over time period (last N)')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'aggrMethod': 'count','aggrPeriod': 'minute', 'lastN': 3}
url = 'http://'+QUANTUMLEAP_HOST+':8668/v2/entities/urn:ngsi-ld:Termometer:003/attrs/motion'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)

print('Min over time period')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'aggrMethod': 'min','aggrPeriod': 'minute', 'limit':10} # limit 10
url = 'http://'+QUANTUMLEAP_HOST+':8668/v2/entities/urn:ngsi-ld:Termometer:003/attrs/temperature'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)

print('Latest N Sampled Values near a point')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://'+QUANTUMLEAP_HOST+':8668/v2/types/Device/attrs/temperature?lastN=4&georel=near;maxDistance:5000&geometry=point&coords=40.25,-3.41'
response=requests.get(url,headers=newHeaders)
response.encoding='utf-8'
print(response.text)

print('Latest N Sampled Values in an area')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
url = 'http://'+QUANTUMLEAP_HOST+':8668/v2/types/Device/attrs/temperature?lastN=4&&georel=coveredBy&geometry=polygon&coords=41,-5;35,-5;35,0;41,0;41,-5'
response=requests.get(url,headers=newHeaders)
response.encoding='utf-8'
print(response.text)