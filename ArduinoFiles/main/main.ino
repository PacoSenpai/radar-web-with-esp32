#include <HTTPClient.h>
#include <WiFi.h>
#include <ESP32Servo.h>

#define SERVO_PIN 26

#define SERVO_PERIOD 100
#define REQUEST_SEND_TIME 10

#define TRIGGER_PIN 27
#define ECHO_PIN 14
#define MAX_DISTANCE 50

// Cariables for wifi connection
const char* ssid = "Prueba";
const char* password = "Pedro123";
WiFiClient client;
bool connSucc = true;

const char* host = "192.168.255.89";
const int httpPort = 8000;
long timeSendHttpReq = 0;


// Variables for Servomotor
float servoAngle = 0;
float stepAngle = 10;
bool forward = true;
Servo servo;
long timeServo = 0;

bool client1 = true;

// variables for sonar
float distanceCm = 0.0;

void moveServo(Servo &servo, float &angle, bool &forward){
  if (forward){
      servoAngle += stepAngle;
    }else{
      servoAngle -= stepAngle;
    }
    
    if (servoAngle >= 180){
      forward = !forward;
    }
    
    if (servoAngle <= 0){
      forward = !forward;
    }

    servo.write(servoAngle);
}

float measureDistance(int triggerPin, int echoPin) {
  long duration;
  digitalWrite(triggerPin, LOW);  //for generating a clean pulse
  delayMicroseconds(4);
  digitalWrite(triggerPin, HIGH);  //generate a 10 ms pulse
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  duration = pulseIn(echoPin, HIGH);  //mesure time of the pulse
  return (float)duration * 0.0171;   //convert distance to cm (342*100/1000000)/2 -> x[cm] = v[cm/ms] * t[ms] = (342*100/1000000)/2 * duration
}

void setup() {
  Serial.begin(9600);
  delay(2000);
  Serial.println("Connecting to wifi");

  servo.attach(SERVO_PIN);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

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
  do{
    connSucc = client.connect(host, httpPort);
    delay(500);
    Serial.println("connecting web");
  }
  while (!connSucc);
  
}

void loop() {

  if ((millis() - timeServo) > SERVO_PERIOD){
    moveServo(servo, servoAngle, forward);
    distanceCm = measureDistance(TRIGGER_PIN, ECHO_PIN);
    Serial.print("Anaagulo: ");
    Serial.print(servoAngle);
    Serial.print("\t\tDistance: ");
    Serial.println(distanceCm);
    timeServo = millis();
  }

  if ((millis() - timeSendHttpReq) > REQUEST_SEND_TIME){
    timeSendHttpReq = millis();
    
    if (!connSucc) 
    {
      Serial.println("Error conecting to website");
    }
    else
    { 
      char group[6];
      if (client1){
        sprintf(group, "%s","gorup1");
      }else{
        sprintf(group, "%s","gorup2");
      }
      client1 = !client1;
      
      char json[100];
      char payload[256]; 
      float angleRad = servoAngle/180 * 3.141592;
      sprintf(json, "{\"name\" : \"%s\" , \"angle\": %.2f, \"distance\": %.2f}", group, angleRad, distanceCm);
      sprintf(payload, "POST /api/send_point HTTP/1.1\r\nHost: 192.168.255.89:8000\r\nContent-Type: application/json\r\nContent-Length: %d\r\n\r\n%s\r\n\r\n", strlen(json), json);
      
      Serial.println("Sending to:");
      Serial.print(host);
      Serial.println(" -> ");
      Serial.println(payload);

      client.print(payload);
    }
    
  }
  
}
