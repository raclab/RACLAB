#include<Servo.h>

int eski_x = 0;
int eski_y = 0;
int fark_x = 0;
int fark_y = 0;
int fark_xy = 0;

int dizi[6] = {0,0,0,0,0,0};
int dizi1[6] ={0,0,0,0,0,0}; 

const int stepPinx1 = 2;
const int stepPinx2 = 4;
const int stepPiny = 3;
 
const int dirPinx1 = 5; 
const int dirPinx2 = 7; 
const int dirPiny = 6;

const int Enable = 8;

int buton_pinxu = 9;
int buton_pinxd = 10;
int buton_pinyu = 11;
int buton_pinyd = 12;
int buton_degerxu = 0;
int buton_degerxd = 0;
int buton_degeryu = 0;
int buton_degeryd = 0;

Servo servomotor;

void setup() {
  pinMode(stepPinx1,OUTPUT); 
  pinMode(stepPinx2,OUTPUT);
  pinMode(stepPiny,OUTPUT);
   
  pinMode(dirPinx1,OUTPUT); 
  pinMode(dirPinx2,OUTPUT);
  pinMode(dirPiny,OUTPUT);

  pinMode(Enable,OUTPUT);

  pinMode(buton_pinxu, INPUT);
  pinMode(buton_pinxd, INPUT);
  pinMode(buton_pinyu, INPUT);
  pinMode(buton_pinyd, INPUT);

  servomotor.attach(13);

  Serial.begin(9600);
}

void loop() {
  digitalWrite(Enable,LOW); 
  buton_degerxu = digitalRead(buton_pinxu);
  buton_degerxd = digitalRead(buton_pinxd);
  buton_degeryu = digitalRead(buton_pinyu);
  buton_degeryd = digitalRead(buton_pinyd);

  if (buton_degerxu == HIGH)
  {
    x_control(1 , HIGH);
  }
  
  if (buton_degerxd == HIGH)
  {
    x_control(1 , LOW);
  }
  if (buton_degeryu == HIGH)
  {
    y_control(1 , HIGH);
  }

  if (buton_degeryd == HIGH)
  {
    y_control(1 , LOW);
  }
  
  if (Serial.available()) 
  {
    int yeni_x = Serial.parseInt();
    int yeni_y = Serial.parseFloat();


    sirala(yeni_x , eski_x , yeni_y , eski_y);

    for(int i=0 ; i<6 ; i++)
    {
      dizi1[i] = dizi[i];
    }
    
    fark_x = dizi1[0] - dizi1[1];
    fark_y = dizi1[3] - dizi1[4];

    sirala(fark_x , fark_y , 0 , 0);
    fark_xy = dizi[0] - dizi[1];
    
    if(dizi[2] == HIGH)
    {
      xy_control(fark_y , dizi1[2] , dizi1[5]);
      x_control(fark_xy , dizi1[2]); 
    }
    else
    {
      xy_control(fark_x , dizi1[2] , dizi1[5]);
      y_control(fark_xy , dizi1[5]); 
    }
    
    eski_x = yeni_x;
    eski_y = yeni_y;
    Serial.print(yeni_x);
    Serial.print(","); 
    Serial.print(yeni_y); 
    Serial.println(" konumunda.."); 

    for(int i=0 ; i<91 ; i++)
    {
      servomotor.write(i);
      delay(15);
    }
    
    y_control( 1 , HIGH );
    y_control( 1 , LOW  );
    
    for(int i=0 ; i<91 ; i++)
    {
      servomotor.write(90 - i);
      delay(15);
    }    
  }
}


int xy_control(int a , int b , int c)
{
  digitalWrite(dirPinx1,b); 
  digitalWrite(dirPinx2,b); 
  digitalWrite(dirPiny,c); 
  for(int x = 0; x < 200*a; x++) 
  {
    digitalWrite(stepPinx1,HIGH); 
    digitalWrite(stepPinx2,HIGH);
    digitalWrite(stepPiny,HIGH);
    delayMicroseconds(500); 
    digitalWrite(stepPinx1,LOW);
    digitalWrite(stepPinx2,LOW);
    digitalWrite(stepPiny,LOW);
    delayMicroseconds(500); 
  } 
}

int x_control(int a , int b)
{
  digitalWrite(dirPinx1,b); 
  digitalWrite(dirPinx2,b);
  for(int x = 0; x <  1200*a; x++) 
  {
    digitalWrite(stepPinx1,HIGH); 
    digitalWrite(stepPinx2,HIGH); 
    delayMicroseconds(500); 
    digitalWrite(stepPinx1,LOW);
    digitalWrite(stepPinx2,LOW);  
    delayMicroseconds(500); 
  }
}

int y_control(int a , int b)
{
  digitalWrite(dirPiny,b); 
  for(int x = 0; x < 1200*a; x++) 
  {
    digitalWrite(stepPiny,HIGH); 
    delayMicroseconds(500); 
    digitalWrite(stepPiny,LOW); 
    delayMicroseconds(500); 
  }
}

void sirala(int a , int b , int c , int d)
{
  if(a>b)
  {
    dizi[0] = a;
    dizi[1] = b;
    dizi[2] = HIGH;
    
  }
  else
  {
    dizi[0] = b;
    dizi[1] = a;
    dizi[2] = LOW;
  }
  if(c>d)
  {
    dizi[3] = c;
    dizi[4] = d;
    dizi[5] = HIGH;
  }
  else
  {
    dizi[3] = d;
    dizi[4] = c; 
    dizi[5] = LOW;
  }
  return dizi[6];
}




/*    if(yeni_x > eski_x && yeni_y > eski_y)
    {
      fark_x = yeni_x - eski_x ;
      fark_y = yeni_y - eski_y ;

      if(fark_x > fark_y)
      {
        fark_xy = fark_x - fark_y ;
        xy_control(fark_y , HIGH , HIGH);
        x_control(fark_xy , HIGH)
      }
      else
      {
        fark_xy = fark_y - fark_x ;
        xy_control(fark_x , HIGH , HIGH);
        y_control(fark_xy , HIGH)
      } 
    }
    
    else if(yeni_x < eski_x && yeni_y > eski_y)
    {
      fark_x = eski_x - yeni_x ;
      fark_y = yeni_y - eski_y ;

      if(fark_x > fark_y)
      {
        fark_xy = fark_x - fark_y ;
        xy_control(fark_x , LOW , HIGH);
        x_control(fark_xy , LOW)
      } 
      else
      {
        fark_xy = fark_y - fark_x ;
        xy_control(fark_x , LOW , HIGH);
        y_control(fark_xy , HIGH)
      }   
    }
    
    else if(yeni_x > eski_x && yeni_y < eski_y)
    {
      fark_x = yeni_x - eski_x ;
      fark_y = eski_y - yeni_y ;

      if(fark_x > fark_y)
      {
        fark_xy = fark_x - fark_y ;
        xy_control(fark_y , HIGH , LOW);
        x_control(fark_xy , HIGH)
      }
      else
      {
        fark_xy = fark_y - fark_x ;
        xy_control(fark_x , HIGH , LOW);
        y_control(fark_xy , LOW)
      } 
    }
    
    else if(yeni_x < eski_x && yeni_y < eski_y)
    {
      fark_x = eski_x  - yeni_x ;
      fark_y = eski_y  - yeni_y ;

      if(fark_x > fark_y)
      {
        fark_xy = fark_x - fark_y ;
        xy_control(fark_y , LOW , LOW);
        x_control(fark_xy , LOW)
      }
      else
      {
        fark_xy = fark_y - fark_x ;
        xy_control(fark_x , LOW , LOW);
        y_control(fark_xy , LOW)
      }
    }

    else
    {
      durdur();
    } */
