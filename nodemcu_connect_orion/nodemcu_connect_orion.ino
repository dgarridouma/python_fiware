#include <ESP8266WiFi.h> 

const char* ssid = "YOUR_SSID"; // Fill in with your WiFi SSID
const char* password = "YOUR_PASSWORD"; // Fill in with your WiFi password

const char* host = "192.168.1.95";  // Orion context broker IP

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

  Serial.print("connecting to ");
  Serial.println(host);
 
  // Creating client
  WiFiClient client;
  const int httpPort = 1026; // ORION port
  if (!client.connect(host, httpPort)) {
    // error connecting?
    Serial.println("Connection failed");
    return;
  }
 
  // Creating URL for connection
  String url = "/version";
 
  Serial.print("Request URL: http://");
  Serial.print(host);
  Serial.print(":");
  Serial.print(httpPort);
  Serial.println(url);
 
  // Sending request
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
         "Host: " + host + "\r\n" + 
         "Connection: close\r\n\r\n");
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 5000) {
      Serial.println(">>> Maximum time exceeded!");
      client.stop();
      return;
    }
  }

  // Reading response
  while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }
 
  Serial.println();
  Serial.println("Closing connection");

  while(1){
    delay(0); // Attending Wifi tasks... this is needed with long loops
              // to avoid error and reset              
  }
}
