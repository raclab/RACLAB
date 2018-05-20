#include <RCSwitch.h>                         //RF kütüphanesi tanımlandı.

#define OpenCode 32                           //Açma sinyalinin kodu 32 olarak tanımlandı.
#define CloseCode 78                          //Kapatma sinyalinin kodu 78 olarak tanımlandı.
RCSwitch RFAlici = RCSwitch();                //RFVerici, RCSwitch.h kütüphanesine tanıtıldı.

void setup() {
  RFAlici.enableReceive(0);                   //Receiver on interrupt 0 => that is pin #2
  pinMode(3, OUTPUT);                         //Yeşil led            
  //pinMode(4, OUTPUT);                       //Kırmızı led
}

void loop() {
  if (RFAlici.available()) {                      
    long veri = RFAlici.getReceivedValue();
    if (veri != 0) {                          //10 ms aralıklarla gelen sinyal var mı kontrol edilir. Açma sinyali gelmişse yeşil led yakılır, kapatma sinyali gelmişse kırmızı led yakılır.
      if(veri==OpenCode){
        //digitalWrite(4,LOW);
        //digitalWrite(3,HIGH);
        digitalWrite(3,HIGH);
      }
      else if(veri==CloseCode){
        //digitalWrite(4,HIGH);
        //digitalWrite(3,LOW);
        digitalWrite(3,LOW);
      }
    }
  }          
  delay(10);                
}


