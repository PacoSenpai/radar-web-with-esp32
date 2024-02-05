#include <HTTPClient.h>
#include <WiFi.h>


#define SEND_DELAY 1000

const char* ssid = "Liberad_a_wifi";
const char* password = "montarto";

const char* host = "192.168.1.50";
const int httpPort = 8000;

void setup() {
  Serial.begin(9600);
  Serial.println("Connecting to wifi");

  // conectarse al wifi
  WiFi.begin(ssid, password);

  // Esperar a que establezca conexion
  Serial.println("Waiting for conection...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("Conectado!");
  Serial.println("");
  Serial.println("IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client;
  if (!client.connect(host, httpPort)) {
    Serial.print("Error conecting to website");
    return;
  }
  
  char* payload = "POST /api/enviar_cadena HTTP/1.1\r\nHost: 192.168.1.50:8000\r\nContent-Type: application/json\r\nContent-Length: 28\r\n\r\n{\"cadena\": \"Hola desde raw\"}\r\n\r\n";
  Serial.println("Sending to:");
  Serial.print(host);
  Serial.print(" -> ");
  Serial.println(payload);


  client.print(payload);


  delay(SEND_DELAY);
}
