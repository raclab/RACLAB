#include <SPI.h> //SPI haberleşme için kütüphaneyi dahil ettik
#include <nRF24L01.h> //haberleşme modülünün kütüphanesini dahil ettik
#include <RF24.h>

#define CE_PIN   9  
#define CSN_PIN  10
const uint64_t pipe = 0xE8E8F0F0E1LL;
RF24 radio(CE_PIN, CSN_PIN); //haberleşme modülünün pinlerini tanımladık
int data[2];

int metal;
int led = 4;

const int Motor1_Ileri = A0;//Sağ Motor hareketi için pinleri tanımladık
const int Motor1_Geri = A1;
const int Motor1_PWM = 3;

const int Motor2_Ileri = A3;//Sol Motor hareketi için pinleri tanımladık
const int Motor2_Geri = A2;
const int Motor2_PWM = 6; 
void setup()   
{
  pinMode(metal,INPUT); //kullandığımız tüm pinleri giriş-çıkış şekilde arduinoya tanıttık
  pinMode(Motor1_Ileri,OUTPUT);
  pinMode(Motor1_Geri,OUTPUT);
  pinMode(Motor1_PWM,OUTPUT);
  pinMode(Motor2_Ileri,OUTPUT);
  pinMode(Motor2_Geri,OUTPUT);
  pinMode(Motor2_PWM,OUTPUT);
  Serial.begin(9600);//haberleşmeyi başlattık
  radio.begin();
  radio.openReadingPipe(1,pipe);
  radio.startListening();; 
}


void loop()  {

  int  metal =digitalRead(2);//2. pinden okunan değere göre işlem seçimini sağladık
  if ( metal == HIGH){  //bir değer okunduysa bütün motorları kapatıp orada durmasını sağladık
  digitalWrite(led, HIGH);
  
  digitalWrite(Motor1_Ileri,LOW);
  digitalWrite(Motor1_Geri,LOW);
  analogWrite(Motor1_PWM,0);
  digitalWrite(Motor2_Ileri,LOW);
  digitalWrite(Motor2_Geri,LOW);
  analogWrite(Motor2_PWM,0);
    
    radio.stopListening();;
    
  }
  
  if ( radio.available() ) //metal okunmadığında devam edilecek
  {
    int y = data[1]; //vericiden gelen dataları dizilere aktardık
    int x = data[0];
    radio.read( data, sizeof(data) ); //okunan her bir değere aralığına göre hız değişkeni tanımladık
    if(y >= 400 && y <= 600) {
     digitalWrite(Motor1_Ileri,LOW);
    digitalWrite(Motor1_Geri,LOW);
    analogWrite(Motor1_PWM,0);
    digitalWrite(Motor2_Ileri,LOW);
    digitalWrite(Motor2_Geri,LOW);
    analogWrite(Motor2_PWM,0);
    }
     if(y >= 535 && y <= 650) {
     digitalWrite(Motor1_Ileri,LOW);
    digitalWrite(Motor1_Geri,HIGH);
    analogWrite(Motor1_PWM,100);
    digitalWrite(Motor2_Ileri,LOW);
    digitalWrite(Motor2_Geri,HIGH);
    analogWrite(Motor2_PWM,100);}
    
    if(y > 650 && y <= 800) {
     digitalWrite(Motor1_Ileri,LOW);
    digitalWrite(Motor1_Geri,HIGH);
    analogWrite(Motor1_PWM,140);
    digitalWrite(Motor2_Ileri,LOW);
    digitalWrite(Motor2_Geri,HIGH);
    analogWrite(Motor2_PWM,140);
    }
    if(y > 800 && y <= 950) {
     digitalWrite(Motor1_Ileri,LOW);
    digitalWrite(Motor1_Geri,HIGH);
    analogWrite(Motor1_PWM,180);
    digitalWrite(Motor2_Ileri,LOW);
    digitalWrite(Motor2_Geri,HIGH);
    analogWrite(Motor2_PWM,180);
    }
    if(y > 950 && y <= 1023) {
     digitalWrite(Motor1_Ileri,LOW);
    digitalWrite(Motor1_Geri,HIGH);
    analogWrite(Motor1_PWM,255);
    digitalWrite(Motor2_Ileri,LOW);
    digitalWrite(Motor2_Geri,HIGH);
    analogWrite(Motor2_PWM,255);}
 
    if(y >= 0 && y <= 7) {
     digitalWrite(Motor1_Ileri,HIGH);
    digitalWrite(Motor1_Geri,LOW);
    analogWrite(Motor1_PWM,255);
    digitalWrite(Motor2_Ileri,HIGH);
    digitalWrite(Motor2_Geri,LOW);
    analogWrite(Motor2_PWM,255);
    }
    if(y > 7 && y <= 200) {
     digitalWrite(Motor1_Ileri,HIGH);
    digitalWrite(Motor1_Geri,LOW);
    analogWrite(Motor1_PWM,180);
    digitalWrite(Motor2_Ileri,HIGH);
    digitalWrite(Motor2_Geri,LOW);
    analogWrite(Motor2_PWM,180);
    }
    if(y > 200 && y <= 350) {
     digitalWrite(Motor1_Ileri,HIGH);
    digitalWrite(Motor1_Geri,LOW);
    analogWrite(Motor1_PWM,140);
    digitalWrite(Motor2_Ileri,HIGH);
    digitalWrite(Motor2_Geri,LOW);
    analogWrite(Motor2_PWM,140);
    }
    if(y >350 && y <= 517) {
     digitalWrite(Motor1_Ileri,HIGH);
    digitalWrite(Motor1_Geri,LOW);
    analogWrite(Motor1_PWM,100);
    digitalWrite(Motor2_Ileri,HIGH);
    digitalWrite(Motor2_Geri,LOW);
    analogWrite(Motor2_PWM,100);
    }
    if(x >= 400 && x <= 513 ) {
     digitalWrite(Motor1_Ileri,HIGH);
    digitalWrite(Motor1_Geri,LOW);
    analogWrite(Motor1_PWM,100);
    digitalWrite(Motor2_Ileri,LOW);
    digitalWrite(Motor2_Geri,HIGH);
    analogWrite(Motor2_PWM,100);
    }
    if(x >= 300 && x < 400  ) {
     digitalWrite(Motor1_Ileri,HIGH);
    digitalWrite(Motor1_Geri,LOW);
    analogWrite(Motor1_PWM,165);
    digitalWrite(Motor2_Ileri,LOW);
    digitalWrite(Motor2_Geri,HIGH);
    analogWrite(Motor2_PWM,165);
    }
    if(x >= 100 && x < 300 ) {
     digitalWrite(Motor1_Ileri,HIGH);
    digitalWrite(Motor1_Geri,LOW);
    analogWrite(Motor1_PWM,205);
    digitalWrite(Motor2_Ileri,LOW);
    digitalWrite(Motor2_Geri,HIGH);
    analogWrite(Motor2_PWM,205);
    }
    if(x >= 0 && x < 100) {
     digitalWrite(Motor1_Ileri,HIGH);
    digitalWrite(Motor1_Geri,LOW);
    analogWrite(Motor1_PWM,255);
    digitalWrite(Motor2_Ileri,LOW);
    digitalWrite(Motor2_Geri,HIGH);
    analogWrite(Motor2_PWM,255);
    }
    if(x >= 532 && x <= 700) {
     digitalWrite(Motor1_Ileri,LOW);
    digitalWrite(Motor1_Geri,HIGH);
    analogWrite(Motor1_PWM,100);
    digitalWrite(Motor2_Ileri,HIGH);
    digitalWrite(Motor2_Geri,LOW);
    analogWrite(Motor2_PWM,100);
    }
    if(x > 700 && x <= 820) {
     digitalWrite(Motor1_Ileri,LOW);
    digitalWrite(Motor1_Geri,HIGH);
    analogWrite(Motor1_PWM,165);
    digitalWrite(Motor2_Ileri,HIGH);
    digitalWrite(Motor2_Geri,LOW);
    analogWrite(Motor2_PWM,165);
    }
    if(x >= 820 && x <= 920) {
     digitalWrite(Motor1_Ileri,LOW);
    digitalWrite(Motor1_Geri,HIGH);
    analogWrite(Motor1_PWM,205);
    digitalWrite(Motor2_Ileri,HIGH);
    digitalWrite(Motor2_Geri,LOW);
    analogWrite(Motor2_PWM,205);
    }
    if(x >= 920 && x <= 1023) {
     digitalWrite(Motor1_Ileri,LOW);
    digitalWrite(Motor1_Geri,HIGH);
    analogWrite(Motor1_PWM,255);
    digitalWrite(Motor2_Ileri,HIGH);
    digitalWrite(Motor2_Geri,LOW);
    analogWrite(Motor2_PWM,255);
    }
 
    Serial.print(" x=");
    Serial.print(x);
    Serial.print(" y=");
    Serial.println(y);
    
    
  }
      
  
  
  
}
