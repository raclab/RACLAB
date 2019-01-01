#include <SPI.h> //SPI haberleşmesi için kütüphaneyi dahil ettik    
#include <nRF24L01.h>//haberleşme modülünün kütüphanelerini dahil ettik
#include <RF24.h>


#define CE_PIN   9  //haberleşme modülünün pinlerini arduinoya tanıttık
#define CSN_PIN 10
#define x_axis A0 // x ve y ekseni için anolog pin tanımladık
#define y_axis A1 



const uint64_t pipe = 0xE8E8F0F0E1LL; 
RF24 radio(CE_PIN, CSN_PIN); 
int data[2];  

void setup() 
{
  Serial.begin(9600); //haberleşmeyi başlattık
  radio.begin();
  radio.openWritingPipe(pipe);
}

void loop()   
{

  data[0] = analogRead(x_axis); //potansiyometreden okunan değerleri bir diziye aktardık
  data[1] = analogRead(y_axis);
  radio.write( data, sizeof(data) ); //bu dizileri kablosuz aktardık
 
 Serial.print(" x="); //arduino programının seri port ekranından potansiyometreden okunan değeri okumak için gerekli kısım
  Serial.print(analogRead(x_axis));
   Serial.print(" y= ");
  Serial.println(analogRead(A1));

}

