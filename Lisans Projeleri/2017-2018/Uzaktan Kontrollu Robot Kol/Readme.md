""""""""""""""""""""""""""""""""""""""""""""""""""""Uzaktan Kontrollü Robot Kol""""""""""""""""""""""""""""""""""""""""""""""""""

Bluetooth ile robot kol kontrolü 

Arduino kodu

//

#include <Servo.h> 

#include <SoftwareSerial.h>

int bluetoothTx = 0;

int bluetoothRx = 1; //Bluetooth alıcı vericilerini tanımlar.
 
SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

Servo altservo,tutbirakservo, asagiyukariservo1, asagiyukariservo2,ilerigeriservo1, ilerigeriservo2;

void setup() {
 
 altservo.attach(5);

 ilerigeriservo1.attach(6);
 
 ilerigeriservo2.attach(7);
 
 asagiyukariservo1.attach(8);
 
 asagiyukariservo2.attach(9);

 tutbirakservo.attach(10);

 Serial.begin(9600);
 
 bluetooth.begin(9600);

}

void loop() 

{
  
  if(bluetooth.available()>= 2 )
  
  {
   
   unsigned int servopos = bluetooth.read();
    
   unsigned int servopos1 = bluetooth.read();
   
   unsigned int data = (servopos1 *256) + servopos; 
    
   Serial.println(data);

    if (data >=1000 && data <1180)                     
   
   {                                                  
      int servo1 = data;
     
     servo1 = map(servo1, 1000,1180,90,180);
     
     altservo.write(servo1);                         
      
      delay(10);
    
    }
    
    if (data >=2000 && data <2180)                     
   
   {                                                  
      
      int servo2 = data;
      
      servo2 = map(servo2, 2000,2180,50,160);
      
      tutbirakservo.write(servo2);                  
      
      delay(10);
    
    }
    
    if (data >=3000 && data<3180)
    
    {
      
      int servo3 = data;
      
      servo3 = map(servo3, 3000,3180,80,170);
      
      asagiyukariservo1.write(servo3);                         
      
      delay(10);
    
    }
    
  if (data >=4000 && data<4180)
    
    {
      
      int servo4 = data;
      
      servo4 = map(servo4, 4000,4180,80,170);
      
      asagiyukariservo2.write(servo4);                         
      
      delay(10);
   
   }
     
     if (data >=5000 && data<5180)
    
    {
      
      int servo5 = data;
      
      servo5 = map(servo5, 5000,5180,0,90);
      
      ilerigeriservo1.write(servo5);
      
      ilerigeriservo2.write(servo5);                         
      
      delay(10);
    }
   
    }
    
    }
   
    //
