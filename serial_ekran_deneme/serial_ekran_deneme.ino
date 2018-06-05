int yenisayi = 0;
int eskisayi = 0 ;

int motorPin1 = 8;          
int motorPin2 = 9;
int motorPin3 = 10;
int motorPin4 = 11;

int delayTime=5;

void setup() {
  Serial.begin(9600);  // Seri Portu başlat
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
}
 
void loop() {
  if (Serial.available()) 
  { // okumak için veri varmı.
 
    yenisayi = Serial.parseInt(); // veri dizisindeki tam sayıları oku
    if(yenisayi < eskisayi){
      int fark = eskisayi - yenisayi;

      for(int i = 0 ; i < fark ; i++ ){
      ters_tam_tur();
      Serial.print(i+1);
      Serial.println(" geri tur..");
      }
    }
    else if(yenisayi > eskisayi){
      int fark = yenisayi - eskisayi;

      for(int i = 0 ; i < fark ; i++ ){
      duz_tam_tur();
      Serial.print(i+1);
      Serial.println(" duz tur..");
      }
    }
    else{
      durdur();
      }
      
  Serial.print(yenisayi);
  Serial.println(" konumunda.."); 
  }
  eskisayi = yenisayi;
}

void adimlarduz()
{
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
  delay(delayTime);
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
  delay(delayTime);
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin4, LOW);
  delay(delayTime);
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, HIGH);
  delay(delayTime);
}
void adimlarters()
{
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, HIGH);
  delay(delayTime);
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin4, LOW);
  delay(delayTime);
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
  delay(delayTime);
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
  delay(delayTime);
}
void durdur()
{
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
  delay(delayTime);
}
void duz_tam_tur()
  {
    for(int i=1;i<=512;i++)
  {
    adimlarduz();
  }
  }
void ters_tam_tur()
  {
    for(int i=1;i<=512;i++)
  {
    adimlarters();
  }
  }
 
 
