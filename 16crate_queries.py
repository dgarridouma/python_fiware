import requests
import json
import os

QUANTUMLEAP_HOST = os.getenv('QUANTUMLEAP_HOST','localhost')

print('First N Sampled Values')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'offset':3, 'limit':3}
url = 'http://'+QUANTUMLEAP_HOST+':8668/v2/entities/urn:ngsi-ld:Termometer:001/attrs/temperature'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)


print('Last N Sampled Values')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'lastN':3}
url = 'http://'+QUANTUMLEAP_HOST+':8668/v2/entities/urn:ngsi-ld:Termometer:001/attrs/temperature'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)

print('Sum over time period (last N)')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'aggrMethod': 'count','aggrPeriod': 'minute', 'lastN': 3}
url = 'http://'+QUANTUMLEAP_HOST+':8668/v2/entities/urn:ngsi-ld:Termometer:001/attrs/motion'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)

print('Min over time period')
newHeaders = {'fiware-service': 'openiot', 'fiware-servicepath': '/'}
payload =  { 'aggrMethod': 'min','aggrPeriod': 'minute'}
url = 'http://'+QUANTUMLEAP_HOST+':8668/v2/entities/urn:ngsi-ld:Termometer:001/attrs/motion'
response=requests.get(url,headers=newHeaders,params=payload)
response.encoding='utf-8'
print(response.text)
