#include <Servo.h>// servo kütüphanesini dahil ettik
Servo YATAY; //yatay ve dikey olarak 2 servo değişkeni tanımladık
Servo DIKEY;

int pos1 = 90; //her iki servonun başlangıç konumunu 90 dereceye ayarladık
int pos2 = 90; 
const int LDR_SOL = A0; //ldr ve pot girişleri için analog pinleri tanımladık
const int LDR_SAG = A1; 
const int LDR_YUKARI = A2; 
const int LDR_ASAGI = A3; 
const int pot_pin = A4;

int SOL = 0; //okunan değerlere göre atayacağımız değişkenleri tanımladık
int SAG = 0; 
int YUKARI = 0;
int ASAGI = 0;
int pot = 0;

void setup()
{
YATAY.attach(9); //servoların çıkışlarını ayarladık
DIKEY.attach(10); 
Serial.begin(9600);
}

void loop()
{

SOL = analogRead(LDR_SOL);//değişkenlere ldrlerden gelen bilgileri aktardık
SAG = analogRead(LDR_SAG);
YUKARI = analogRead(LDR_YUKARI);
ASAGI = analogRead(LDR_ASAGI);
pot = analogRead(pot_pin);
pot = map(pot, 0, 1023, 0, 50); //pottan okunan değeri 0-50 arasına küçülttük

Serial.print("POT = "); //bilgisayarın seri portu üzerinden ldr de okunan değerleri görmek için gerekli kısım
Serial.print(pot);
Serial.print(" LDR_SAG = ");
Serial.print(SAG);
Serial.print(" LDR_SOL = ");
Serial.print(SOL);
Serial.print(" LDR_UST = ");
Serial.print(YUKARI);
Serial.print(" LDR_ALT = ");
Serial.println(ASAGI);


 if (SOL > ( SAG + pot )) //eğer sol sağdan büyükse yatay motoru 1 azalt
 {
 if (pos1 > 0)
 pos1 -= 1;
 YATAY.write(pos1);
 }
 
 if (SAG > ( SOL + pot )) //eğer sağ soldan büyükse yatay motoru 1 artır
 {
 if ( pos1 < 180 )
 pos1++;
 YATAY.write(pos1);
 }

 if (YUKARI > ( ASAGI + pot ))//eğer yukarı asagıdandan büyükse dikey motoru 1 azalt
 {
 if ( pos2 > 0 )
 pos2 -= 1;
 DIKEY.write(pos2);
 }
 
 if (ASAGI > ( YUKARI + pot ))//eğer asagı yukarıdan büyükse yatay motoru 1 artır
 {
 if (pos2 < 180)
 pos2++;
 DIKEY.write(pos2);
 }

delay(60);//60 mikro saniye bekle
}
