"""""""""""""""""""""""""""""""""""""""""""""""""""Uzaktan Kontrollü Robot"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Bluetooth ile kontrol edilen robot projesi.

Arduino Kodu

#############################################################################################

  const int motorA1  = 5;  
 
  const int motorA2  = 6;  
  
  const int motorB1  = 10; 
  
  const int motorB2  = 9;  
  
  const int LED1 = 2;
  
  const int LED2 = 3;
  
  const int LED3 = 4;
  
  const int LED4 = 12;

  
  int i=0; 
  
  int j=0; 
  
  int state; 
  
  int vSpeed=255;

void setup() 

{
    
    pinMode(motorA1, OUTPUT);
    
    pinMode(motorA2, OUTPUT);
    
    pinMode(motorB1, OUTPUT);
    
    pinMode(motorB2, OUTPUT);
    
    pinMode(LED1, OUTPUT);
    
    pinMode(LED2, OUTPUT);
    
    pinMode(LED3, OUTPUT);
    
    pinMode(LED4, OUTPUT);   
    
    Serial.begin(9600);

}
 
void loop() 

{

 if(digitalRead(state)==LOW) 
 
 { 
       
       state='S'; 
      
      digitalWrite(LED1, LOW);
      
      digitalWrite(LED2, LOW);
      
      digitalWrite(LED3, LOW);
      
      digitalWrite(LED4, LOW);
      
 }
 
    if(Serial.available() > 0)
   
   {     
      
      state = Serial.read();   
    
    }
  
    if (state == '0')
    
    {
      
      vSpeed=0;
      
      digitalWrite(LED1, LOW);
      
      digitalWrite(LED2, LOW);
      
      digitalWrite(LED3, LOW);
      
      digitalWrite(LED4, LOW);
      
      }
    
    else if (state == '1')
    
    {
      
      vSpeed=100;
      
      digitalWrite(LED1, HIGH);
      
      digitalWrite(LED2, LOW);
      
      digitalWrite(LED3, LOW);
      
      digitalWrite(LED4, LOW);
      
      }
    
    else if (state == '2')
    
    {
      
      vSpeed=180;
      
      digitalWrite(LED1, HIGH);
      
      digitalWrite(LED2, HIGH);
      
      digitalWrite(LED3, LOW);
      
      digitalWrite(LED4, LOW);
      
      }
    
    else if (state == '3')
    
    {
      
      vSpeed=200;
      
      digitalWrite(LED1, HIGH);
      
      digitalWrite(LED2, HIGH);
      
      digitalWrite(LED3, HIGH);
      
      digitalWrite(LED4, LOW);
      
      }
    
    else if (state == '4')
    
    {
      
      vSpeed=255;
      
      digitalWrite(LED1, HIGH);
      
      digitalWrite(LED2, HIGH);
      
      digitalWrite(LED3, HIGH);
      
      digitalWrite(LED4, HIGH);
      
      }
     
  /***********************İleri****************************/

    if (state == 'F') 
   
   {
      
      analogWrite(motorA1, vSpeed); 
      
      analogWrite(motorA2, 0);
      
      analogWrite(motorB1, vSpeed);
      
      analogWrite(motorB2, 0); 
    }
    
  /**********************İleri Sol************************/
  
    else if (state == 'G') 
    
    {
    analogWrite(motorA1,vSpeed ); 
    
    analogWrite(motorA2, 0);  
      
    analogWrite(motorB1, 100);   
      
    analogWrite(motorB2, 0); 
    
    }
    
  /**********************İleri Sağ************************/
  
    else if (state == 'I') 
    
    {
        
        analogWrite(motorA1, 100); 
        
        analogWrite(motorA2, 0); 
        
        analogWrite(motorB1, vSpeed);     
        
        analogWrite(motorB2, 0); 
    
    }
    
  /***********************Geri****************************/
  
    else if (state == 'B') 
    
    {
      
      analogWrite(motorA1, 0);   
      
      analogWrite(motorA2, vSpeed); 
      
      analogWrite(motorB1, 0);   
      
      analogWrite(motorB2, vSpeed); 
    
    }
    
  /**********************Geri Sol************************/
  
    else if (state == 'H') 
    
    {
      
      analogWrite(motorA1, 0);   
      
      analogWrite(motorA2, 100); 
      
      analogWrite(motorB1, 0);
          
      analogWrite(motorB2, vSpeed); 
    
    }
    
  /**********************Geri Sağ************************/
  
    else if (state == 'J') 
    
    {
      
      analogWrite(motorA1, 0);  
      
      analogWrite(motorA2, vSpeed); 
      
      analogWrite(motorB1, 0);   
      
      analogWrite(motorB2, 100); 
    
    }
    
  /***************************Sol*****************************/
  
    else if (state == 'L') 
    
    {
      
      analogWrite(motorA1, vSpeed);   
      
      analogWrite(motorA2, 150); 
      
      analogWrite(motorB1, 0); 
      
      analogWrite(motorB2, 0); 
    
    }
    
  /***************************Sağ*****************************/
  
    else if (state == 'R') 
    
    {
      
      analogWrite(motorA1, 0);   
      
      analogWrite(motorA2, 0); 
      
      analogWrite(motorB1, vSpeed);   
      
      analogWrite(motorB2, 150);     
    
    }
    
    /************************Stop*****************************/
    
    else if (state == 'S')
    
    {
        
        analogWrite(motorA1, 0);  
        
        analogWrite(motorA2, 0); 
        
        analogWrite(motorB1, 0);  
        
        analogWrite(motorB2, 0);
    
    }  

}
