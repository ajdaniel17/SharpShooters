#include <Servo.h>

Servo servo1;

int xpos = 0;    

const int angle = 2;

int width = 640;

void setup() {
  Serial.begin(9600);
  servo1.attach(9);
  servo1.write(xpos);
}

void loop() {
  if (Serial.available() > 0) {
    int x_mid;
    if (Serial.read() == 'X') {
      x_mid = Serial.parseInt();
    }
    if (x_mid > width / 2 + 30)
      xpos += angle;
    if (x_mid < width / 2 - 30)
      xpos -= angle;

    if (xpos >= 180)
      xpos = 180;
    else if (xpos <= 0)
      xpos = 0;
      
    servo1.write(xpos);
  }
}
