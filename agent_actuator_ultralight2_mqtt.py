import requests
import json
import os
import paho.mqtt.client as mqtt

ORION_HOST = os.getenv('ORION_HOST','localhost')
IOTAGENT_HOST = os.getenv('IOTAGENT_HOST','localhost')
MQTT_HOST= os.getenv('MQTT_HOST','localhost')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe("/4jggokgpepnvsb2uv4s40d59ov/bell001/cmd")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    res=msg.payload.decode()+" ring OK" # this is needed to confirm command is finished    
    print(res)
    client.publish("/4jggokgpepnvsb2uv4s40d59ov/bell001/cmdexe", res, qos=0, retain=False)

# Provisioning an actuator

json_dict={
  "devices": [
    {
      "device_id": "bell001",
      "entity_name": "urn:ngsi-ld:Bell:001",
      "entity_type": "Bell",
      "protocol": "PDI-IoTA-UltraLight",
      "transport": "MQTT",
      #"endpoint": "http://"+YOUR_IP+":3000/bell001",
      "commands": [
        { "name": "ring", "type": "command" }
       ],
    }
  ]
}

newHeaders = {'Content-type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
response = requests.post('http://'+IOTAGENT_HOST+':4041/iot/devices',
                         data=json.dumps(json_dict),
                         headers=newHeaders)
print("Status code: ", response.status_code)
print(response.text)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.tls_set()
client.connect(MQTT_HOST, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
