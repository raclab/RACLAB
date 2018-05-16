**//MUSTAFA ÜNLÜ DENGE ROBOTU KODU 161202112**

//kodlarda fazlalık icerikler bulunabilir, özellik ekleme cıkarma yaparken kalmıs olabilir.
/*
BLUETOOTH İLE KONTROL İÇİN  

DENGE HASSAS AYARI == (+),(-)

DENGE HASSAS İNCE AYARI == (a),(b)

İLERİ HIZLI == (1)

DUR == (2)

GERİ HIZLI == (3)

DUR NORMAL == (c)

İLERİ NORMAL == (d)

GERİ NORMAL == (e)

SAG DÖN == (f)

SOL DÖN == (g)

*/

#include <PID_v1.h>

#include <LMotorController.h>

#include "I2Cdev.h"

#include "MPU6050_6Axis_MotionApps20.h"

#include "Wire.h"

#define MIN_ABS_SPEED 0

#include <SoftwareSerial.h>

MPU6050 mpu;

float veri;

char state;

float veri2;

bool dmpReady = false; 

uint8_t mpuIntStatus; 

uint8_t devStatus; 

uint16_t packetSize; 

uint16_t fifoCount; 

uint8_t fifoBuffer[64]; 


Quaternion q; 

VectorFloat gravity;

float ypr[3];

double originalSetpoint = 177;  //173

double setpoint = originalSetpoint;

double movingAngleOffset = 3.3;  //0.3

double input, output;

int moveState=0;

double Kp = 35;   //40

double Kd = 0.7;  //1

double Ki = 70;   //50

PID pid(&input, &output, &setpoint, Kp, Ki, Kd, DIRECT);

double motorSpeedFactorLeft = 0.55;

double motorSpeedFactorRight = 0.45;

int ENA = 5;

int IN1 = 6;

int IN2 = 7;

int IN3 = 8;

int IN4 = 9;

int ENB = 10;

LMotorController motorController(ENA, IN1, IN2, ENB, IN3, IN4, motorSpeedFactorLeft, motorSpeedFactorRight);

volatile bool mpuInterrupt = false; 

void dmpDataReady()

{

mpuInterrupt = true;

}


void setup()

{

Serial.begin(9600);

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE

Wire.begin();

TWBR = 24;

#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE

Fastwire::setup(400, true);

#endif

while (!Serial);

mpu.initialize();

devStatus = mpu.dmpInitialize();

mpu.setXGyroOffset(128); //128

mpu.setYGyroOffset(50); //50

mpu.setZGyroOffset(-100); //-100

mpu.setZAccelOffset(1688); // 1688 

if (devStatus == 0)

{

mpu.setDMPEnabled(true);

attachInterrupt(0, dmpDataReady, RISING);

mpuIntStatus = mpu.getIntStatus();

dmpReady = true;

packetSize = mpu.dmpGetFIFOPacketSize();

pid.SetMode(AUTOMATIC);

pid.SetSampleTime(5);

pid.SetOutputLimits(-255, 255); 

}

}

void loop()

{ 

moveBackForth();

while (!mpuInterrupt && fifoCount < packetSize)

{

if(moveState==3){                                         //Sağ taraf

setpoint = originalSetpoint - 1;

pid.Compute();

motorController.turnLeft(output, 120);

delay(1);

}
else if(moveState==4){                                    //Sol taraf

setpoint = originalSetpoint + 1;

pid.Compute();

motorController.turnRight(output, 120);

delay(1);

}

else if(moveState==0||moveState==1||moveState==2){

pid.Compute();

motorController.move(output, MIN_ABS_SPEED);

delay(1);

}

}
mpuInterrupt = false;

mpuIntStatus = mpu.getIntStatus();

fifoCount = mpu.getFIFOCount();

if ((mpuIntStatus & 0x10) || fifoCount == 1024)

{

mpu.resetFIFO();

}

else if (mpuIntStatus & 0x02)

{

while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();

mpu.getFIFOBytes(fifoBuffer, packetSize);

fifoCount -= packetSize;

mpu.dmpGetQuaternion(&q, fifoBuffer);

mpu.dmpGetGravity(&gravity, &q);

mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);


float c=ypr[1];

if(Serial.available() > 0){ 

  state=Serial.read();
  
  if(state=='1'){
  
    veri2=0.04;                     //ileri
    
  }
  
  if(state=='2'){
  
    veri2=0;                     //dur
    
  }
  
  if(state=='3'){
  
    veri2=-0.04;                     //geri
    
  }
  
  if(state=='+'){
  
    veri=veri-0.01;                     //denge ayarı
    
  }
  
  if(state=='-'){
  
    veri=veri+0.01;                     //denge ayarı
    
  }
  
  if(state=='a'){
  
    veri=veri-0.005;                     //hassas denge ayarı
    
  }
  
  if(state=='b'){
 
    veri=veri+0.005;                      //hassas denge ayarı
    
  }
  
  if(state=='c'){
  
   moveState=0;                     //dur
   
  }
  
  if(state=='d'){
  
    moveState=1;                     //ileri
    
  }
  
  if(state=='e'){
  
   moveState=2;                     //geri
   
  }
  
  if(state=='f'){
  
   moveState=3;                     //sag
   
  }
  
  if(state=='g'){
  
   moveState=4;                     //sol
   
  }
  
}

float   z =((c))+ (veri) + veri2;   

input = (z-0.19) * 180/M_PI + 180;

}

}


void moveBackForth(){                                          //İleri geri hareket

if (moveState == 0)

setpoint = originalSetpoint;

else if (moveState == 1)

setpoint = originalSetpoint - movingAngleOffset;

else if (moveState == 2)

setpoint = originalSetpoint + movingAngleOffset;

} 
