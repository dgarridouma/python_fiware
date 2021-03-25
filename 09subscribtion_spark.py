import requests
import json
import os

ORION_HOST = os.getenv('ORION_HOST','localhost')

# Create entity
json_dict={
    "id": "urn:ngsi-ld:Termometer:001",
    "type": "Device",
    "temperature": { "type": "Number", "value": 25.0},
    "motion": { "type": "Number", "value": 0.0}
}

newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json','fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+ORION_HOST+':1026/v2/entities',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)

# Create subscription
json_dict={
  "description": "Notify Spark of all context changes",
  "subject": {
    "entities": [{"idPattern": ".*"}]
  },
  "notification": {
    "http": {
      "url": "http://spark-worker-1:9001"
    }
  }
}

newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+ORION_HOST+':1026/v2/subscriptions',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)

# (As root user if needed):
# docker exec -it spark-worker-1 bin/bash
# /spark/bin/spark-submit --class  org.fiware.cosmos.tutorial.MinTemp --master spark://spark-master:7077 --deploy-mode client /home/cosmos-examples/target/cosmos-examples-1.2.2.jar --conf "spark.driver.extraJavaOptions=-Dlog4jspark.root.logger=WARN,console"
