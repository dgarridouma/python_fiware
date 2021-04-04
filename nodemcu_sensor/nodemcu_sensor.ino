// Example to be used as sensor in 09agent_sensor_ultralight1.py
#include <ESP8266WiFi.h> 
#include <ESP8266HTTPClient.h>

const char* ssid = "YOUR_SSID"; // Fill in with your WiFi SSID
const char* password = "YOUR_PASSWORD"; // Fill in with your WiFi password

void setup() {
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
}


void loop() {
  HTTPClient http;
  http.begin("http://192.168.1.95:7896/iot/d?k=4jggokgpepnvsb2uv4s40d59ov&i=motion001");  // replace with your Orion IP and API key
  http.addHeader("Content-Type", "text/plain");
  int httpCode = http.POST("c|2");
  String payload = http.getString();
  Serial.println(httpCode);
  Serial.println(payload);
  http.end();
  delay(1000);
}
