#include <WiFiClient.h>
#include "sendData.hpp"
static WiFiClient client;
namespace wifi 
{
bool sendDataToServer(const char* host, const unsigned int httpPort, const char* group, const float angleRad, const float distanceCm) {
  bool connSucc = client.connect(host, httpPort);
  if (connSucc) {
    char json[100];
    char payload[256];
    sprintf(json, "{\"name\" : \"%s\" , \"angle\": %.2f, \"distance\": %.2f}", group, angleRad, distanceCm);
    sprintf(payload, "POST /api/send_point HTTP/1.1\r\nHost: %s:%d\r\nContent-Type: application/json\r\nContent-Length: %d\r\n\r\n%s\r\n\r\n", host, httpPort, strlen(json), json);

    Serial.println("Sending to:");
    Serial.print(host);
    Serial.println(" -> ");
    Serial.println(payload);
    client.print(payload);
    return true;
  } 
  Serial.println("Error connecting to server");
  Serial.println("Check host ip and port");

  return false;
}
}


