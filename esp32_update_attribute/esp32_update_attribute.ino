#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* host = "YOUR_CB_IP";
const int httpPort = 1026;
const char* url = "/v2/entities/urn:ngsi-ld:Store:001/attrs";

void setup() {
  Serial.begin(115200);
  delay(10);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected - IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi lost, reconnecting...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("Reconnected");
  }

  JsonDocument doc;
  doc["category"]["type"]      = "Text";
  doc["category"]["value"]     = "categoryUpdated";
  doc["stars"]["type"]         = "Number";
  doc["stars"]["value"] = (esp_random() % 6) + 1;
  doc["specialOffer"]["value"] = true;

  String jsonPayload;
  serializeJson(doc, jsonPayload);
  Serial.print("JSON: ");
  Serial.println(jsonPayload);

  HTTPClient http;
  String fullUrl = "http://" + String(host) + ":" + httpPort + url;
  http.begin(fullUrl);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Accept", "application/json");

  int httpCode = http.POST(jsonPayload);

  if (httpCode > 0) {
    Serial.println("Response code: " + String(httpCode));
  } else {
    Serial.println("Request failed: " + http.errorToString(httpCode));
  }

  http.end();
  delay(3000);
}