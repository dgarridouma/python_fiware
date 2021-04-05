// Example to be used with 14agent_mqtt1_device_provisioning.py and 14agent_mqtt3_send_command_ultralight.py
/* MQTT-FIWARE Example created from...*/
/***************************************************
  Adafruit MQTT Library ESP8266 Example

  Must use ESP8266 Arduino from:
    https://github.com/esp8266/Arduino

  Works great with Adafruit's Huzzah ESP board & Feather
  ----> https://www.adafruit.com/product/2471
  ----> https://www.adafruit.com/products/2821

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  Written by Tony DiCola for Adafruit Industries.
  MIT license, all text above must be included in any redistribution
 ****************************************************/
#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

/************************* WiFi Access Point *********************************/

#define WLAN_SSID       "YOUR SSID HERE"
#define WLAN_PASS       "YOUR PASSWORD HERE"


/************************* Adafruit.io Setup *********************************/

#define AIO_SERVER      "YOUR MQTT IP HERE"        
#define AIO_SERVERPORT  1883                   // use 8883 for SSL

/************ Global State (you don't need to change this!) ******************/

// Create an ESP8266 WiFiClient class to connect to the MQTT server.
WiFiClient client;
// or... use WiFiClientSecure for SSL
//WiFiClientSecure client;

// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, "", "");

/****************************** Feeds ***************************************/

// Setup feeds for publishing.
Adafruit_MQTT_Publish measurement = Adafruit_MQTT_Publish(&mqtt, "/4jggokgpepnvsb2uv4s40d59ov/vehicle002/attrs");

Adafruit_MQTT_Publish cmdexe = Adafruit_MQTT_Publish(&mqtt, "/4jggokgpepnvsb2uv4s40d59ov/vehicle002/cmdexe");

// Setup a feed called 'cmd' for subscribing to commands.
Adafruit_MQTT_Subscribe cmd = Adafruit_MQTT_Subscribe(&mqtt, "/4jggokgpepnvsb2uv4s40d59ov/vehicle002/cmd");

/*************************** Sketch Code ************************************/

// Bug workaround for Arduino 1.6.6, it seems to need a function declaration
// for some reason (only affects ESP8266, likely an arduino-builder bug).
void MQTT_connect();

void setup() {
  Serial.begin(115200);
  delay(10);

  // Connect to WiFi access point.
  Serial.println(); Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);

  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("WiFi connected");
  Serial.println("IP address: "); Serial.println(WiFi.localIP());

  // Setup MQTT subscription for cmd feed.
  mqtt.subscribe(&cmd);
}

int x=0;

void loop() {
  // Ensure the connection to the MQTT server is alive (this will make the first
  // connection and automatically reconnect when disconnected).  See the MQTT_connect
  // function definition further below.
  MQTT_connect();

  // this is our 'wait for incoming subscription packets' busy subloop
  // try to spend your time here

  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(5000))) {
    if (subscription == &cmd) {
      Serial.println("Request received");
      Serial.println((char *)cmd.lastread);
      String res=(char *)cmd.lastread;
      res=res.substring(0,res.indexOf("|")+1)+"cmd OK";
      Serial.println(res);
      char cad[16];
      res.toCharArray(cad,16);
      cmdexe.publish(cad); // Error control is missing
    }
  }

  // Now we can publish stuff!
  Serial.print(F("\nSending measurement "));
  Serial.print(x);
  Serial.print("...");
  x++;
  char cad[16];
  sprintf(cad, "s|80#r|%d", x);
  if (! measurement.publish(cad)) {
    Serial.println(F("Failed"));
  } else {
    Serial.println(F("OK!"));
  }

  // ping the server to keep the mqtt connection alive
  // NOT required if you are publishing once every KEEPALIVE seconds
  /*
  if(! mqtt.ping()) {
    mqtt.disconnect();
  }
  */
}

// Function to connect and reconnect as necessary to the MQTT server.
// Should be called in the loop function and it will take care if connecting.
void MQTT_connect() {
  int8_t ret;

  // Stop if already connected.
  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected
       Serial.println(mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       mqtt.disconnect();
       delay(5000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         // basically die and wait for WDT to reset me
         while (1);
       }
  }
  Serial.println("MQTT Connected!");
}
