import requests
import json
import os
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from time import sleep

# Import settings from settings.py
token=""
USER = ""
PASSWORD = ""
SERVICE = ""
SERVICE_PATH = ""
ORION_HOST =""

try:
   from settings import *
except ImportError:
   pass

warnings.simplefilter('ignore',InsecureRequestWarning)

def get_token():
  global token

  url = 'https://'+ORION_HOST+':6001/v3/auth/tokens'
  headers = {'fiware-service': SERVICE, 'fiware-servicepath': SERVICE_PATH, 'Content-type': 'application/json'}

  payload={
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "domain": {
                        "name": SERVICE
                    },
                    "name": USER,
                    "password": PASSWORD
                }
            }
        },
        "scope": {
            "project": {
                "domain": {
                   "name": SERVICE
                },
                "name": SERVICE_PATH
            }
        }
    }
}

  response=requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
  response.encoding='utf-8'
  print(response.headers["X-Subject-Token"])
  token=response.headers["X-Subject-Token"]


get_token()
url = 'https://'+ORION_HOST+':2026/v2/entities?id=waspmote:ISTHP02B'
headers = {'fiware-service': SERVICE, 'fiware-servicepath': SERVICE_PATH, 'X-Auth-Token': token}


while True:
  try:
    response=requests.get(url, headers=headers, verify=False)
    response.encoding='utf-8'
    #print(response.text)
    dict=json.loads(response.text)
    print(dict[0]["TC"]["value"])
    sleep(60)
  except:
    get_token()
