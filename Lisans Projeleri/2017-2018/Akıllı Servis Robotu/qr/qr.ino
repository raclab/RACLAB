int in1=3, in2=4, in3=5, in4=6;

void setup() {
  pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT);
  pinMode(in4,OUTPUT);

  Serial.begin(9600);
}


void loop() {
  while (Serial.available())
  {  
    char a=Serial.read();
    
    if (a=='1')
    {  
      digitalWrite(in1,HIGH);
      digitalWrite(in2,LOW);
      digitalWrite(in3,HIGH);
      digitalWrite(in4,LOW);
    }
    else if (a=='0')
    {
      digitalWrite(in1,LOW);
      digitalWrite(in2,LOW);
      digitalWrite(in3,LOW);
      digitalWrite(in4,LOW);
    }
    } 
}
