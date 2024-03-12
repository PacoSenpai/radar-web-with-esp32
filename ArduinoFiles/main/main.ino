#include <WiFi.h>
#include <ESP32Servo.h>
#include "sendData.hpp"

#define SERVO_PIN 26

#define SERVO_PERIOD 100
#define REQUEST_SEND_TIME 10

#define TRIGGER_PIN 27
#define ECHO_PIN 14
#define MAX_DISTANCE 50

// Variables for wifi connection
const char* ssid = "Motorola pau";
const char* password = "montarto";

const char* host = "192.168.46.89";
const unsigned int httpPort = 8000;
long timeSendHttpReq = 0;



// Variables for Servomotor
float servoAngle = 0;
float stepAngle = 10;
bool forward = true;
Servo servo;
long timeServo = 0;

// variables for sonar
float distanceCm = 0.0;

void moveServo(Servo& servo, float& angle, bool& forward) {
  if (forward) {
    servoAngle += stepAngle;
  } else {
    servoAngle -= stepAngle;
  }

  if (servoAngle >= 180) {
    forward = !forward;
  }

  if (servoAngle <= 0) {
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
  return (float)duration * 0.0171;    //convert distance to cm (342*100/1000000)/2 -> x[cm] = v[cm/ms] * t[ms] = (342*100/1000000)/2 * duration
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
}

void loop() {

  if ((millis() - timeServo) > SERVO_PERIOD) {
    moveServo(servo, servoAngle, forward);
    distanceCm = measureDistance(TRIGGER_PIN, ECHO_PIN);
    Serial.print("Anaagulo: ");
    Serial.print(servoAngle);
    Serial.print("\t\tDistance: ");
    Serial.println(distanceCm);
    timeServo = millis();
  }

  if ((millis() - timeSendHttpReq) > REQUEST_SEND_TIME) {
    timeSendHttpReq = millis();
    float angleRad = servoAngle / 180 * 3.141592;
    bool a = wifi::sendDataToServer(host, httpPort, "group0", angleRad, distanceCm);
  }
}
