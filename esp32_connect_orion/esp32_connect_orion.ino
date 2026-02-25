#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* host = "YOUR_CB_IP";
const int httpPort = 1026;

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
  HTTPClient http;
  String url = "http://" + String(host) + ":" + httpPort + "/version";

  Serial.print("GET ");
  Serial.println(url);

  http.begin(url);
  int httpCode = http.GET();

  if (httpCode > 0) {
    Serial.println("Response code: " + String(httpCode));
    Serial.println(http.getString());
  } else {
    Serial.println("Request failed: " + http.errorToString(httpCode));
  }

  http.end();
  delay(1000);
}