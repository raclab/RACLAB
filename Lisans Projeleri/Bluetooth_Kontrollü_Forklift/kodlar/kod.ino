
#include <SoftwareSerial.h>

SoftwareSerial baglanti(10,11);
int led=7;
char c;
int stby1 = 2;
int stby2 = 13;
int i = 0;
int j = 0;
int k = 0;

int pwmPina = 5;
int pwmPinb = 9;
int pwmPinc = 6;

int mot1_ileri=8;
int mot1_geri=12;

int mot2_ileri=3;
int mot2_geri=4;


int mot_yukari=1;
int mot_asagi=0;



void ileri()
{
   
  digitalWrite(mot1_ileri,HIGH);
  digitalWrite(mot1_geri, LOW);
  digitalWrite(mot2_ileri, HIGH);
  digitalWrite(mot2_geri, LOW);
 }
void geri()
{
   
  digitalWrite(mot1_ileri,LOW);
  digitalWrite(mot1_geri, HIGH);
  digitalWrite(mot2_ileri, LOW);
  digitalWrite(mot2_geri, HIGH);
}
void sag()
{
   
  digitalWrite(mot1_ileri,LOW);
  digitalWrite(mot1_geri, HIGH);
  digitalWrite(mot2_ileri, HIGH);
  digitalWrite(mot2_geri, LOW);
}

void sol()
{
   
  digitalWrite(mot1_ileri,HIGH);
  digitalWrite(mot1_geri, LOW);
  digitalWrite(mot2_ileri, LOW);
  digitalWrite(mot2_geri, HIGH);
}

void yukari_kaldir()
{
   
  digitalWrite(mot_yukari, HIGH);
  digitalWrite(mot_asagi,LOW);
  
  
}
void asagi_indir()
{
   
  digitalWrite(mot_yukari,LOW);
  digitalWrite(mot_asagi,HIGH);

}
void dur()
{ 
  
  digitalWrite(mot1_ileri,LOW);
  digitalWrite(mot1_geri, LOW);
  
  digitalWrite(mot2_ileri, LOW);
  digitalWrite(mot2_geri, LOW);
  
  digitalWrite(mot_yukari, LOW);
  digitalWrite(mot_asagi,LOW);
}



void setup() {
  baglanti.begin(9600);
  
  pinMode(pwmPina,OUTPUT);
  pinMode(pwmPinb,OUTPUT);
  pinMode(pwmPinc,OUTPUT);
  
  digitalWrite(stby1,HIGH);
  digitalWrite(stby2,HIGH);

  
  pinMode(mot1_ileri,OUTPUT);
  pinMode(mot1_geri,OUTPUT);
  pinMode(mot2_ileri,OUTPUT);
  pinMode(mot2_geri,OUTPUT);
  pinMode(mot_yukari,OUTPUT);
  pinMode(mot_asagi,OUTPUT);

}

void loop() {
if(baglanti.available()){
  c=baglanti.read(); //gelen veri okundu
  if (c=='W')
  {
    ileri();
   
  }
  else if(c=='A')
  {
    sol();
    
  }
  else if(c=='S')
  {
    geri();
  }
  else if(c=='D')
  {
    sag();
  }
  else if (c=='R')
  {
    yukari_kaldir();
  }
  else if (c=='F')
  {
    asagi_indir();
  }
  else if (c=='H')
  {
    dur();
  }
  for(i=0;i<100;i = i+1)

      {  
           // pwmi motor sürücüsüne gönderiyoruz
             analogWrite(pwmPina,i);             
      }
      for(j=0;j<100;j = j+1)

      {  
           // pwmi motor sürücüsüne gönderiyoruz
             analogWrite(pwmPinb,j);             
      }
      for(k=0;k<100;k = k+1)

      {  
           // pwmi motor sürücüsüne gönderiyoruz
             analogWrite(pwmPinc,k);             
      }
  
 }
 
}

