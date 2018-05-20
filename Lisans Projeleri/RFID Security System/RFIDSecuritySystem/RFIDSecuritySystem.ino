/*RC522 bağlantıları aşağıdaki gibidir.
 * -----------------------------------------------------------------------------------------
 *             MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
 *             Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
 * Signal      Pin          Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------
 * RST/Reset   RST          9             5         D9         RESET/ICSP-5     RST
 * SPI SS      SDA(SS)      10            53        D10        10               10
 * SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
 * SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
 * SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
 */


#include <SPI.h>                      //SPI kütüphanesi tanımlandı.
#include <MFRC522.h>                  //RFID kütüphanesi tanımlandı.
#include <EEPROM.h>                   //EEPROM kütüphanesi tanımlandı.
#include <RCSwitch.h>                 //RF kütüphanesi tanımlandı.

#define SS_PIN 10                     //RFID'nin SDA pini, 10. pin olarak tanımlandı.
#define RST_PIN 9                     //RFID'nin RST pini, 9. pin olarak tanımlandı.
#define Mavi 5                        //Mavi led, 5. pin olarak tanımlandı.
#define Yes 6                         //Yeşil led, 6. pin olarak tanımlandı.
#define Kir 7                         //Kırmızı led, 7. pin olarak tanımlandı.
#define RF433 8                       //RF, 8.pin olarak tanımlandı.
#define OpenCode 32                   //Açma sinyalinin kodu 32 olarak tanımlandı.(Programın daha hızlı çalışabilmesi ve sinyal iletim menzilinin artırılabilmesi için 2 haneli kod kullanıldı.)
#define CloseCode 78                  //Kapatma sinyalinin kodu 78 olarak tanımlandı.(Programın daha hızlı çalışabilmesi ve sinyal iletim menzilinin artırılabilmesi için 2 haneli kod kullanıldı.)

MFRC522 rfid(SS_PIN, RST_PIN);        //RFID'ye ayarlanan pinler RFID kütüphanesine tanıtıldı.
MFRC522::MIFARE_Key key;              //Key değişkeni RFID kütüphanesine tanıtıldı.

RCSwitch RFVerici = RCSwitch();       //RFVerici, RCSwitch.h kütüphanesine tanıtıldı.       

byte nuidPICC[4];                     //Yeni UID'yi tutacak dizi
byte uid[4];                          //1. slottaki kartın UID'sini tutacak dizi
byte uid2[4];                         //2. slottaki kartın UID'sini tutacak dizi
int edit=0;                           //Ayar değişkeni tanımlanıp sıfırlandı.
int onoff=EEPROM.read(10);;           //onoff değişkeni tanımlanıp EEPROM.read(10)'daki veri atandı. (Elektrik Kesintisi Koruması)
  
void setup() {
  pinMode(Mavi, OUTPUT);              //Gerekli pinler çıkış yapıldı.
  pinMode(Kir, OUTPUT);               
  pinMode(Yes, OUTPUT);
  RFVerici.enableTransmit(RF433);     //8. pin, verici pini olarak kütüphaneye eklendi.
  delay(100);                         //Mikroişlemcinin değişiklikleri daha doğru yapabilmesi için 100ms gecikme süresi eklendi.
  //Serial.begin(9600);                 //Seri port başlatıldı.
  SPI.begin();                        //Arduino'nun RFID ile haberleşebilmesi için SPI başlatıldı.
  rfid.PCD_Init();                    //MFRC522'nin başlatma fonksiyonu çalıştırıldı.
  for (byte i = 0; i < 6; i++) {      //Projede kullanılacak kartların şifresi olmadığı için şifre dizisine sıfırlar eklendi.
    key.keyByte[i] = 0xFF;        
  }
  updateuid();                        //updateuid() fonksiyonu çağırılıp slotlardaki UID'ler programa alındı.
  if(onoff==1){                       //Elektrik kesintisi koruması ile önceki çalışmadaki ayar programa alındı.
    digitalWrite(Kir,HIGH);
    digitalWrite(Yes,LOW);
    RFVerici.send(CloseCode, 24);     //433Mhz frekansında kapatma sinyali gönderildi.
    delay(10);
    RFVerici.send(CloseCode, 24);
  }
  else{
    digitalWrite(Kir,LOW);
    digitalWrite(Yes,HIGH);
    RFVerici.send(OpenCode, 24);      //433Mhz frekansında açma sinyali gönderildi.
    delay(10);
    RFVerici.send(OpenCode, 24);
        
  }
  //Serial.println(F("KOD BASLADI"));   //Seri porta "KOD BASLADI" yazdırıldı.
}

void loop() {
  if ( ! rfid.PICC_IsNewCardPresent())//Yeni kart olup olmadığı kontrol edildi.
    return;
  if ( ! rfid.PICC_ReadCardSerial())  //Kartın okunabilirliği kontrol edildi.
    return;
    
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak); //Kart tipi okundu.

  // Kartın klasik MIFARE veya ultralight tip olup olmadığı kontrol edilip, geçersizse seri porta "Lütfen Geçerli Bir Kart Giriniz." yazdırıldı.
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&  
    piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
    piccType != MFRC522::PICC_TYPE_MIFARE_4K &&
    piccType != MFRC522::PICC_TYPE_MIFARE_UL) {
    //Serial.println(F("Lütfen Geçerli Bir Kart Giriniz."));
    return;
  }
    if ((rfid.uid.uidByte[0] == uid[0] &&         //1. veya 2. slotta uidsi bulunan bir kart okutulmuşsa;
    rfid.uid.uidByte[1] == uid[1] && 
    rfid.uid.uidByte[2] == uid[2] && 
    rfid.uid.uidByte[3] == uid[3]) || 
    (rfid.uid.uidByte[0] == uid2[0] && 
    rfid.uid.uidByte[1] == uid2[1] && 
    rfid.uid.uidByte[2] == uid2[2] && 
    rfid.uid.uidByte[3] == uid2[3])) {
      if(edit==1){                                //Önceden değişim kartı basıldıysa basılan kart slottan silindi.
        if (rfid.uid.uidByte[0] == uid[0]){
          for (int bg=0;bg<=3;bg++){
            EEPROM.write(bg,0);
          }
        }
        else if (rfid.uid.uidByte[0] == uid2[0]){
          for (int bg=0;bg<=3;bg++){
            EEPROM.write(bg+4,0);
          }
        }
        updateuid();                              //UID belleği güncellendi.
        edit=0;                                   //Ekleme/Çıkarma tamamlandı.
        return;                                   //Loopun başına dönüldü.
      }
      if(onoff==1) {                              //Kapatma ve açma sinyali loopu
        digitalWrite(Kir,LOW);
        digitalWrite(Yes,HIGH);
        RFVerici.send(OpenCode, 24);              //433Mhz frekansında açma sinyali gönderildi.
        delay(10);
        RFVerici.send(OpenCode, 24);
        onoff=0;
        EEPROM.write(10,onoff);
      }  
      else {
        digitalWrite(Kir,HIGH);
        digitalWrite(Yes,LOW);
        RFVerici.send(CloseCode, 24);             //433Mhz frekansında kapatma sinyali gönderildi.
        delay(10);
        RFVerici.send(CloseCode, 24);
        onoff=1;
        EEPROM.write(10,onoff);
      }
      delay(600);                                 //Kartın çekilmesi için 1sn boyunca beklendi.
    }
    else if (rfid.uid.uidByte[0] == 0xF4 &&       //Değişim kartı okutulmuşsa;
    rfid.uid.uidByte[1] == 0x54 && 
    rfid.uid.uidByte[2] == 0xDB && 
    rfid.uid.uidByte[3] == 0XD9 ) {
      if(edit==1){                                //Daha önceden okutulup 2. kez okutulduysa 2 slottaki UID'ler silinir.
        for (int bg=0;bg<=7;bg++){
            EEPROM.write(bg,0);
            digitalWrite(Mavi,HIGH);
            delay(100);
            digitalWrite(Mavi,LOW);
            delay(100);
        }
        updateuid();                              //UID belleği güncellendi.
        edit=0;                                   //Ekleme/Çıkarma tamamlandı.
        //Serial.println(F("Bellek Sıfırlandı."));
        delay(500);                               //Kartın çekilmesi için beklendi.
        return;                                   //Loop başına dönüldü.
      }
      //Serial.println(F("Değişim kartı basıldı."));
      edit=1;                                     //Kart değişimi aktifleştirildi.
      digitalWrite(Mavi,HIGH);                    //Bildirim ledi yanıp söndü.
      delay(500);
      digitalWrite(Mavi,LOW);
      delay(1000);
    }
    else{                                         //Değişim kartı veya 2 slotta UID'si bulunan kartlardan biri basılmamışsa;
      if(edit==1){                                //Değişim işlemi aktifse basılan kart slotlardan boş olana eklenir.
        Serial.println(F("Kart Ekleme/Çıkarma"));
        if(uid[0]==0 && uid[1]==0){               //1. Slot boşsa yeni kartın UID'sini buraya yaz.
          for (int bg=0;bg<=3;bg++){
            EEPROM.write(bg,rfid.uid.uidByte[bg]);
          }
          digitalWrite(Mavi,HIGH);
          delay(800);
          digitalWrite(Mavi,LOW);
          delay(500);
        }
        else if(uid2[0]==0 && uid2[1]==0){        //2. Slot boşsa yeni kartın UID'sini buraya yaz.
          for (int bg=0;bg<=3;bg++){
            EEPROM.write(bg+4,rfid.uid.uidByte[bg]);
          }
          digitalWrite(Mavi,HIGH);
          delay(1600);
          digitalWrite(Mavi,LOW);
          delay(500);
        }
        else if(uid[0]!=0  && uid2[0]!=0){        //Slotlar doluysa bildirim ledini 6 kez kısa yakıp söndür.
          //Serial.println(F("Slotlar dolu."));
          for (int bg=0;bg<=6;bg++){
            digitalWrite(Mavi,HIGH);
            delay(100);
            digitalWrite(Mavi,LOW);
            delay(300);
          }
        }
        updateuid();                              //UID belleği güncellendi.
        edit=0;                                   //Ekleme/Çıkarma tamamlandı.
      }
      else{                                       //Değişim işlemi aktif değilse kart tanımsız kart olarak gösterilir.
        //Serial.println(F("Tanımsız Kart"));
        for (int bg=0;bg<=2;bg++){
            digitalWrite(Mavi,HIGH);
            delay(300);
            digitalWrite(Mavi,LOW);
            delay(100);
        }
      }
    }
}

void updateuid(){                                 //Eepromdaki yeni değerlere göre 1. ve 2. slottaki kartların uidleri UID dizilerine eklendi.
  for (int gg=0;gg<=3;gg++){
  uid[gg]=EEPROM.read(gg);
  uid2[gg]=EEPROM.read(gg+4);
  }
}

