#include <Servo.h>

Servo myServo;  // create servo object to control a servo

int servoPin = 9;  // servo is connected to digital pin 9

void setup() {
  myServo.attach(servoPin);  // attaches the servo on pin 9 to the servo object
  
  // Read the current servo position and move to 0 degrees smoothly
  int currentPos = myServo.read();
  for (int pos = currentPos; pos >= 0; pos--) {
    myServo.write(pos);
    delay(100);
  }
}

void loop() {
  // Rotate from 0 to 90 degrees
  for (int pos = 0; pos <= 90; pos += 1) { // goes from 0 degrees to 90 degrees
    myServo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(100);                       // waits 100ms for the servo to reach the position
  }

  // Rotate from 90 to 0 degrees
  for (int pos = 90; pos >= 0; pos -= 1) { // goes from 90 degrees to 0 degrees
    myServo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(100);                       // waits 100ms for the servo to reach the position
  }
}
