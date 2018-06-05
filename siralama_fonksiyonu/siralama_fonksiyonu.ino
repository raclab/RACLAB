/*       c de sıralama fonksiyonu

#include <stdio.h> 
#include <conio.h> 
void main(){ 

int i,j,num; 
int numbers[10]={5,8,6,7,2,19,12,35,95,1}; 

for(i=0;i<10;i++) 
{ 
for(j=i+1;j<10;j++) 
{ 

if(numbers>numbers[j]){ 
num=numbers; 
numbers=numbers[j]; 
numbers[j]=num;} 
} 

} 
for(i=0;i<10;i++) 
printf("%d ",numbers); 
getch(); 
} 


*/

int sayi1 = 0 ;
int sayi2 = 0 ;
int dizi[3] = {0 , 0 , HIGH};
int dizi1[3] = {0 , 0 , LOW};

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  sayi1 = 0;
  sayi2 = 0;
  if (Serial.available()) 
  {
    int sayi1 = Serial.parseInt();
    int sayi2 = Serial.parseFloat();
    
    fonksiyon1(sayi1,sayi2);
    for(int i=0 ; i<3 ; i++)
    {
      dizi1[i] = dizi[i];
    }
    for(int i = 0 ; i<3 ; i++)
    {
      Serial.println(dizi1[i]);
    }
  }
}

void fonksiyon1(int a , int b)
{
  if(a>b)
  {
    dizi[0] = a;
    dizi[1] = b;
    return dizi[3];
  }
  else
  {
    dizi[0] = b;
    dizi[1] = a; 
    return dizi[3];
  }
}

