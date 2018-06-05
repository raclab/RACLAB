int tamsayi = 0;
int yeni_sayi = 0 ;


void setup() {
  Serial.begin(9600);  // Seri Portu başlat
}
 
void loop() {
  if (Serial.available()) { // okumak için veri varmı.
 
    tamsayi = Serial.parseInt(); // veri dizisindeki tam sayıları oku
    

    if(yeni_sayi < tamsayi)
    {
      Serial.println(tamsayi); 
    }
    if(yeni_sayi > tamsayi)
    {
      Serial.println(yeni_sayi); 
    }

  }
  yeni_sayi = tamsayi;
  Serial.println(tamsayi); 
  Serial.println(yeni_sayi); 
  
}
 
 
