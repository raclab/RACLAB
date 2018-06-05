int XmotorPin1 = 10;          
int XmotorPin2 = 11;
int XmotorPin3 = 12;
int XmotorPin4 = 13;

int YmotorPin1 = 6;          
int YmotorPin2 = 7;
int YmotorPin3 = 8;
int YmotorPin4 = 9;

int delayTime=5;
char a,b;


int gelenVeri1=0;
int gelenVeri2=0;
void setup()
{
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  Serial.begin(9600);
  
}

void loop()
{ a=0;
  b=0;
  if (Serial.available() > 0)
  {
    gelenVeri1 = Serial.read();
    a=gelenVeri1;
    Serial.print("Gelen Karakter1: ");
    Serial.println(a);

  }
if (Serial.available() > 0)
  {
    gelenVeri2 = Serial.read();
    b=gelenVeri2;
    Serial.print("Gelen Karakter2: ");
    Serial.println(b);

  }

  int x = a;
  int y = b;
  Serial.println(x);
  Serial.println(y);
  
    if(b<a)
   {
    for (int i=1 ; i<=b-48; i++) 
     {
     duz_tam_turXY();
     Serial.print("X ve Y ");
     Serial.print(i);
     Serial.println(" tur attı..");
     }
     durdur();
    for (int k=b-47 ; k<=a-48; k++) 
     {
     duz_tam_turX();
     Serial.print("X ");
     Serial.print(k);
     Serial.println(" tur attı..");
     }
     durdur();  
   }
delay(5000);


if(b>a)
   {
    for (int i=1 ; i<=a-48; i++) 
     {
     duz_tam_turXY();
     Serial.print("X ve Y ");
     Serial.print(i);
     Serial.println(" tur attı..");
      }
      durdur();
    for (int k=a-47 ; k<=b-48; k++) 
     {
     duz_tam_turY();
     Serial.print("Y ");
     Serial.print(k);
     Serial.println(" tur attı..");
     } 
     durdur();      
   }
   
delay(5000);
}







void duz_tam_turX()
  {int i;
    for(i=1;i<=5;i++)
  {
    adimlarX();
  }
  }
void duz_tam_turY()
  {int i;
    for(i=1;i<=5;i++)
  {
    adimlarY();
  }
  }

void duz_tam_turXY()
  {int i;
    for(i=1;i<=5;i++)
  {
    adimlarXY();
  }
  }

  
void adimlarX()
{
  digitalWrite(XmotorPin1, HIGH);
  digitalWrite(XmotorPin2, LOW);
  digitalWrite(XmotorPin3, LOW);
  digitalWrite(XmotorPin4, LOW);
  delay(delayTime);
  digitalWrite(XmotorPin1, LOW);
  digitalWrite(XmotorPin2, HIGH);
  digitalWrite(XmotorPin3, LOW);
  digitalWrite(XmotorPin4, LOW);
  delay(delayTime);
  digitalWrite(XmotorPin1, LOW);
  digitalWrite(XmotorPin2, LOW);
  digitalWrite(XmotorPin3, HIGH);
  digitalWrite(XmotorPin4, LOW);
  delay(delayTime);
  digitalWrite(XmotorPin1, LOW);
  digitalWrite(XmotorPin2, LOW);
  digitalWrite(XmotorPin3, LOW);
  digitalWrite(XmotorPin4, HIGH);
  delay(delayTime);
}

void adimlarY()
{
  digitalWrite(YmotorPin1, HIGH);
  digitalWrite(YmotorPin2, LOW);
  digitalWrite(YmotorPin3, LOW);
  digitalWrite(YmotorPin4, LOW);
  delay(delayTime);
  digitalWrite(YmotorPin1, LOW);
  digitalWrite(YmotorPin2, HIGH);
  digitalWrite(YmotorPin3, LOW);
  digitalWrite(YmotorPin4, LOW);
  delay(delayTime);
  digitalWrite(YmotorPin1, LOW);
  digitalWrite(YmotorPin2, LOW);
  digitalWrite(YmotorPin3, HIGH);
  digitalWrite(YmotorPin4, LOW);
  delay(delayTime);
  digitalWrite(YmotorPin1, LOW);
  digitalWrite(YmotorPin2, LOW);
  digitalWrite(YmotorPin3, LOW);
  digitalWrite(YmotorPin4, HIGH);
  delay(delayTime);
}

void adimlarXY()
{
  digitalWrite(XmotorPin1, HIGH);
  digitalWrite(YmotorPin1, HIGH);
  digitalWrite(XmotorPin2, LOW);
  digitalWrite(YmotorPin2, LOW);
  digitalWrite(XmotorPin3, LOW);
  digitalWrite(YmotorPin3, LOW);
  digitalWrite(XmotorPin4, LOW);
  digitalWrite(YmotorPin4, LOW);
  delay(delayTime);
  digitalWrite(XmotorPin1, LOW);
  digitalWrite(YmotorPin1, LOW);
  digitalWrite(XmotorPin2, HIGH);
  digitalWrite(YmotorPin2, HIGH);
  digitalWrite(XmotorPin3, LOW);
  digitalWrite(YmotorPin3, LOW);
  digitalWrite(XmotorPin4, LOW);
  digitalWrite(YmotorPin4, LOW);
  delay(delayTime);
  digitalWrite(XmotorPin1, LOW);
  digitalWrite(YmotorPin1, LOW);
  digitalWrite(XmotorPin2, LOW);
  digitalWrite(YmotorPin2, LOW);
  digitalWrite(XmotorPin3, HIGH);
  digitalWrite(YmotorPin3, HIGH);
  digitalWrite(XmotorPin4, LOW);
  digitalWrite(YmotorPin4, LOW);
  delay(delayTime);
  digitalWrite(XmotorPin1, LOW);
  digitalWrite(YmotorPin1, LOW);
  digitalWrite(XmotorPin2, LOW);
  digitalWrite(YmotorPin2, LOW);
  digitalWrite(XmotorPin3, LOW);
  digitalWrite(YmotorPin3, LOW);
  digitalWrite(XmotorPin4, HIGH);
  digitalWrite(YmotorPin4, HIGH);
  delay(delayTime);    
}



void durdur()
{
  digitalWrite(XmotorPin1, LOW);
  digitalWrite(YmotorPin1, LOW);
  digitalWrite(XmotorPin2, LOW);
  digitalWrite(YmotorPin2, LOW);
  digitalWrite(XmotorPin3, LOW);
  digitalWrite(YmotorPin3, LOW);
  digitalWrite(XmotorPin4, LOW);
  digitalWrite(YmotorPin4, LOW);
  delay(delayTime);
}







