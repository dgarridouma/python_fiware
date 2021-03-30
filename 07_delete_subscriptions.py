import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

url = 'http://'+ORION_HOST+':1026/v2/subscriptions'
response=requests.get(url)
subscriptions = json.loads(response.text)
for s in subscriptions:
  print(s["id"])
  url = 'http://'+ORION_HOST+':1026/v2/subscriptions/'+s["id"]
  response=requests.delete(url)

