Roketin icindeki arduino (verici kısım) kodları:

#include <LPS.h>
#include <TinyGPS.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <EEPROM.h>
#include <Servo.h>

TinyGPS gps;
SoftwareSerial ss(3, 2);
//gps rx ==d2
//gps tx ==d3

LPS ps;

Servo myservo;

float flat = 1000.000000;
float flon = 1000.000000;
unsigned long k,l,y=0,age;
String str1="",str2="", giden="",veri,parasut;

float gyrorakim;
float gyroref=900;
float gyrodeger;
float gyromaximum;

int max_sicaklik=0;
int a;

void setup()
{
  Serial.begin(9600);
  ss.begin(9600);
  Wire.begin();
  ps.init();
  ps.enableDefault();
  parasut="0";
  myservo.attach(5);
  myservo.write(30); 
  float pressure = ps.readPressureMillibars();
  float altitude = ps.pressureToAltitudeMeters(pressure);
  float temperature = ps.readTemperatureC();
  a=map(altitude,1000,2500,0,255);
  EEPROM.write(0, a);
  a=map(temperature,0,255,0,255);
  EEPROM.write(1, a);
}

void loop()
{
  float pressure = ps.readPressureMillibars();
  float altitude = ps.pressureToAltitudeMeters(pressure);
  float temperature = ps.readTemperatureC();
  while (ss.available())// gps veri okuma
  {
    gps.encode(ss.read());
  }
  if(millis()-y>1000)
  {
    gps.f_get_position(&flat, &flon);
    if(flat!=1000.000000 && flon!=1000.000000)
    {
      k=flat*1000000;
      str1=String(k);
      l=flon*1000000;
      str2=String(l);
      giden="";
      giden=str1 + "b" + str2;
    }
    else
    {
      giden="";
      giden="1b1c1";
    }
    y=millis();
  }
  if(gyroref>altitude)
  {
    gyrodeger=altitude;
  }
  if(altitude>gyrodeger)
  {
    gyrodeger=altitude;
  }
  if(gyrodeger>altitude)
  {
    gyromaximum=gyrodeger;
  }
  if(gyromaximum-altitude>100)
  {
    parasut="1";
    myservo.write(150);
    a=map(altitude,1000,2500,0,255);
    EEPROM.write(3, a); 
  }
  if (temperature > max_sicaklik)
  {
    max_sicaklik=temperature;
    a=map(max_sicaklik,0,255,0,255);
    EEPROM.write(4, a);
  }
  a=map(gyromaximum,1000,2500,0,255);
  EEPROM.write(2, a);
  veri="";
  veri="a"+giden+"c"+altitude+"d"+parasut+"e";
  Serial.println(veri);
  delay(50);
}

Yer kontroldeki arduino (alıcı kısım) kodları:

#include <EEPROM.h>


int a;
int okunan=0;

void setup() {
  Serial.begin(9600);

}

void loop() 
{
  okunan=EEPROM.read(0);
  a=map(okunan,0,255,1000,2500);
  Serial.println("referans ");
  Serial.println(a);
  
  okunan=EEPROM.read(1);
  a=map(okunan,0,255,0,255);
  Serial.println("referans sicaklik ");
  Serial.println(a);

  okunan=EEPROM.read(2);
  a=map(okunan,0,255,1000,2500);
  Serial.println("maximum ");
  Serial.println(a);

  okunan=EEPROM.read(3);
  a=map(okunan,0,255,1000,2500);
  Serial.println("parasut ");
  Serial.println(a);

  okunan=EEPROM.read(4);
  a=map(okunan,0,255,0,255);
  Serial.println("maximum sicaklik ");
  Serial.println(a);
  while(1)
  {
    
  }

}
