int tamSayi = 0;
float ondalikliSayi = 0;
void setup() {
  Serial.begin(9600);  // Seri Portu başlat
}

void loop() {
  if (Serial.available()) { // okumak için veri varmı.

    tamSayi = Serial.parseInt(); // veri dizisindeki tam sayıları oku
    Serial.println(tamSayi);
    tamSayi = tamSayi - 5;
    Serial.println(tamSayi);

    ondalikliSayi = Serial.parseFloat(); // veri dizisindeki ondalikli sayıları oku
    Serial.println(ondalikliSayi);
    int a = ondalikliSayi;
    Serial.println(a);
    int b = a - 3;
    Serial.println(b);
    
    

  }
}
