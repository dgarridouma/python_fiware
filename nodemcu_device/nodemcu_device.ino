// Example to be used as device in 08agent_device_ultralight_nodemcu.py
#include <ESP8266WiFi.h> 
#include <ESP8266HTTPClient.h>
#include "ESP8266WebServer.h"

const char* ssid = "YOUR_SSID"; // Fill in with your WiFi SSID
const char* password = "YOUR_PASSWORD"; // Fill in with your WiFi password

int count;

ESP8266WebServer server(80);

void setup() {
  count=0;

  Serial.begin(115200);
  delay(10);

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  WiFi.mode(WIFI_STA); // WiFi Client Mode
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected"); 
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP()); // We show our IP
 
  server.on("/vehicle001", HTTP_POST,handleRootPath);    //Associate the handler function to the path
  server.begin();                    //Start the server
  Serial.println("Server listening");
}

void loop() {
  HTTPClient http;
  http.begin("http://192.168.1.95:7896/iot/d?k=5jggokgpepnvsb2uv4s40d59ov&i=vehicle001");
  http.addHeader("Content-Type", "text/plain");

  // Sensing
  char cad[16];
  sprintf(cad, "s|80#r|%d", count);
  int httpCode = http.POST(cad);
  count++;
  String payload = http.getString();
  Serial.println(httpCode);
  Serial.println(payload);
  http.end();
  delay(1000);

  // Actuating
  server.handleClient();         //Handling of incoming requests
}

void handleRootPath() {            //Handler for the rooth path
  Serial.println("Request received");
  Serial.println(server.arg("plain"));
  server.send(200, "text/plain", server.arg("plain")+" cmd OK"); 
}
