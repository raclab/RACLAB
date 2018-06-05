#include<Servo.h>
Servo servomotor;
void setup() {
  // put your setup code here, to run once:
servomotor.attach(8);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  

 
      servomotor.write(0);


   // servomotor.write(0);
}
