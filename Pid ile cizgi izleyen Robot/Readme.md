
#include <QTRSensors.h> // QTR Sensörü tanımlandı.

#define CW  0 // Motorların hangi durumda ne tarafa hareket
#define CCW 1 // edeceği belirlendi.

#define MOTOR_A 0 
#define MOTOR_B 1 

const byte PWMA = 3;  // 1. motor hız pini
const byte PWMB = 11; // 2. motor hız pini
const byte DIRA = 12; // 1. motor yön pini
const byte DIRB = 13; // 2. motor yön pini

#define Kp 0.0009 // Oransal Kazanç 0.0009 --> süper
#define Ki 0      // İntegral Kazancı
#define Kd 0     // Türev Kazancı

#define M1_minumum_hiz 55   // M1 Motorunun minimum hızı belirlendi.
#define M2_minumum_hiz 55   // M2 Motorunun minimum hızı belirlendi.
#define M1_maksimum_hiz 65  // M1 Motorunun maksimum hızı belirlendi.
#define M2_maksimum_hiz 65  // M2 Motorunun maksimum hızı belirlendi.

#define NUM_SENSORS             6  // 6 Sensör kullanılacak.
#define NUM_SAMPLES_PER_SENSOR  4  // Ölçümler içinden 4 değer alındı.
#define EMITTER_PIN             QTR_NO_EMITTER_PIN  // Emiter pin kullanılmadı.

// Pinler sırası ile A0 A1 A2 A3 A4 A5 pinlerine bağlı olduğu tanımlandı.
QTRSensorsAnalog qtra((unsigned char[]) {0, 1, 2, 3, 4, 5}, 
  NUM_SENSORS, NUM_SAMPLES_PER_SENSOR, EMITTER_PIN);
  
unsigned int sensorValues[NUM_SENSORS];

unsigned int error = 0;     // Hata değerini tutan değişken.
unsigned int lastError = 0; // İlk hatadan sonra ölçülen hata.
int motorSpeed = 0;         // Hataya göre motor hızının ayarlanmasında kullanılır. 
int leftMotorSpeed = 0;     // Sol motor hızı.
int rightMotorSpeed = 0;    // Sağ motor hızı.

unsigned int integral=0;    

 void setup() 
 {
  
   setupArdumoto(); // Ardumoto (Motor sürücü) ayarları.

   QTR8A_kalibrasyon (); //Sensör kalibrasyonu yapılıyor.

 }

 void loop()
{
 
 unsigned int sensors[6];
 int position = qtra.readLine(sensors); // Konum bilgisi pozisyon değerine gönderildi.
 error = 2500 - position ;              // Hataya göre aracın çizginin sağında mı yoksa solunda mı olduğu belirlendi.
 integral = integral + error;
  
 motorSpeed = Kp*error + Kd*(error - lastError) + Ki*integral;
 lastError = error;
 
 leftMotorSpeed = M1_minumum_hiz + motorSpeed;  // Hataya göre sol motor hızı ayarlandı.
 rightMotorSpeed = M2_minumum_hiz - motorSpeed; // Hataya göre sağ motor hızı ayarlandı.
  
 set_motors(leftMotorSpeed, rightMotorSpeed); //Motor hızları.

}
 
void set_motors(int motor1speed, int motor2speed)
{
  
if (motor1speed > M1_maksimum_hiz ) motor1speed = M1_maksimum_hiz; //MAKSİMUM MOTOR 1 HIZ LİMİTİ
if (motor2speed > M2_maksimum_hiz ) motor2speed = M2_maksimum_hiz; // MAKSİMUM MOTOR 2 HIZ LİMİTİ
if (motor1speed < 0) motor1speed = 0; // MİNIMUM MOTOR 1 HIZ LİMİTİ
if (motor2speed < 0) motor2speed = 0; // MİNİMUM MOTOR 2 HIZ LİMİTİ
 
 driveArdumoto(MOTOR_A, CW, motor1speed ); //1.MOTOR HIZI
 driveArdumoto(MOTOR_B, CW, motor2speed ); // 2.MOTOR HIZI

}

void driveArdumoto(byte motor, byte yon, byte hiz)
{
  if (motor == MOTOR_A)
  {
    digitalWrite(DIRA, yon); // Motor 1 yön
    analogWrite(PWMA, hiz);  // Motor 1 hız
  }
  else if (motor == MOTOR_B)
  {
    digitalWrite(DIRB, yon); // Motor 2 yön
    analogWrite(PWMB, hiz);  // Motor 2 hız
  }  
}

void stopArdumoto(byte motor) // Motorları durdurur.
{
  driveArdumoto(motor, 0, 0);
}

void setupArdumoto()
{
  
  pinMode(PWMA, OUTPUT); // pin giriş çıkışları belirlendi.
  pinMode(PWMB, OUTPUT);
  pinMode(DIRA, OUTPUT);
  pinMode(DIRB, OUTPUT);

  digitalWrite(PWMA, LOW); // Başlangıçta motor hızları sıfırlandı.
  digitalWrite(PWMB, LOW);
  digitalWrite(DIRA, LOW);
  digitalWrite(DIRB, LOW);
  
}
 void QTR8A_kalibrasyon ()  //QTR-8A sensörünün kalibrasyon ayarları.
 {

  delay(500);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);   // Kalibrasyon modunda olduğumuzu göstermek için Arduino'nun LED'ini açtık.
  
  for (int i = 0; i < 400; i++)  // Kalibrasyon yaklaşık 10 saniye sürüyor.
  {
    
    qtra.calibrate();       // Kişi başına kalibrasyon, ortalama 2.5 msn'dir.  
  
  }
  digitalWrite(13, LOW);     // Kalibrasyona devam ettiğimizi göstermek için led söndürüldü. 

  Serial.begin(9600);
  
  for (int i = 0; i < NUM_SENSORS; i++)
  {
    
    Serial.print(qtra.calibratedMinimumOn[i]); // Ölçülen minimum değerler yazdırıldı.
    Serial.print(' ');
  
  }
  Serial.println();
  
  for (int i = 0; i < NUM_SENSORS; i++)
  {
    
    Serial.print(qtra.calibratedMaximumOn[i]); // Ölçülen maksimum değerler yazdırıldı.
    Serial.print(' ');
  
  }
  
  Serial.println();
  Serial.println();
  delay(1000);
  
 }
