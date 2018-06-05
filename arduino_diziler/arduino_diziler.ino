char harfler[16] = {'M','U','H','E','N','D','I','S','B','E','Y','I','N','L','E','R'}; // bknz char olarak tanımlanan yani harf içeren ifadeler tek tırnak arasına alınarak yazılır

int sayilar[4] = {1,3,5,7};

void setup(){

Serial.begin(9600);

}

void loop(){

for(char i = 0;i < 16; i++)

{

Serial.println(harfler[i]);

}

for(int i = 0;i < 4; i++)

{

Serial.println(sayilar[i]);

}

while(1); // Sonsuz döngü, program kilitlendi.

}
