Arduino üzerinden 5 servo motoru bir arayüz üzerinden kontrol etmek




#############################################################################################


C# kodu


#############################################################################################




using System.IO.Ports; // bu kütüphane seri port haberleşmesi için gerekli                                      

using System.IO;     // kütüphanenin genel ismi bu                                                  

using System.Threading; //bu kütüphane geciktirme yapmak için kullanılıyor googleye threading delay yazıp bakabilirsiniz                   



    public partial class Form1 : Form
    
    {
        SerialPort serialport; // seri porta serialport ismini verdik
        
        public Form1()
        
        {
            InitializeComponent();
            init(); // init() şeklinde bi fonksiyon oluşturduk
        }

        private void init()
        {
            serialport = new SerialPort(); // serialportu yeni seri port olarak tanıttık
            serialport.PortName = "COM5";  // burda PCnin hangi portunu kullandığımızı yazdık ben COM5 kullanıyorum
            serialport.BaudRate = 9600;  //saniye başına bit aktarım hızı arduino ile aynı olmalıdır.

            try
            {
                serialport.Open();   //seri portu açmasını sağladık

            }
            catch (Exception e)
            {
                MessageBox.Show(e.Message);  //bağlantı kopması halinde hata verecektir 

            }
            



        }



        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void trackBar1_Scroll(object sender, EventArgs e)  // track bar ekledik 5 adet
        {                                                    //ben 5 tane kullanıyorum 
            int servoPos = trackBar1.Value;                       // int cinsinden trackbarın değerini servoposa attık

            if (serialport.IsOpen)        // eğer seriport açıksa...
            {

                label1.Text = "Position: " + servoPos.ToString();  //label1 e Position:"buraya açıyı yazar"
                                                                   // string cinsinden yazdırdık

                SendServoInfo(0, servoPos);           //bu fonksiyonu alta koydum aşağıda görünce daha rahat anlarsınız

            }

        }

        private void trackBar2_Scroll(object sender, EventArgs e) //yukarıdaki işlemleri 5 kere tekrar ettik
        {                                                         //imla hatası yapmadan yazın 
            int servoPos = trackBar2.Value;

            if (serialport.IsOpen)
            {
                label2.Text = "Position: " + servoPos.ToString();
                SendServoInfo(1, servoPos);

            }

        }

        private void trackBar3_Scroll(object sender, EventArgs e)
        {
            int servoPos = trackBar3.Value;

            if (serialport.IsOpen)
            {
                label3.Text = "Position: " + servoPos.ToString();
                SendServoInfo(2, servoPos);

            }

        }

        private void trackBar4_Scroll(object sender, EventArgs e)
        {
            int servoPos = trackBar4.Value;

            if (serialport.IsOpen)
            {
                label4.Text = "Position: " + servoPos.ToString();
                SendServoInfo(3, servoPos);

            }

        }

        private void trackBar5_Scroll(object sender, EventArgs e)
        {
            int servoPos = trackBar5.Value;

            if (serialport.IsOpen)
            {
                label5.Text = "Position: " + servoPos.ToString();
                SendServoInfo(4, servoPos);
                

            }

        }






        private void button2_Click(object sender, EventArgs e) //buton2 ekledik çift tıkladık 
        {                 
           
                hareket();                               // tıkladığımızda bu fonk. çalışacak
            
        }



        private void hareket()                  //hareket fonksiyonu 
        {



            int hareket1 = 36; // servo motorlar 0-180 derece arası çalıştığı için en rahat görebileceğim açıları girdim
            int hareket2 = 72;
            int hareket3 = 108;
            int hareket4 = 144;
            int hareket5 = 180;



            trackBar1.Value = hareket1;  //hareket1 in değeri 36 ve bunu trackbara atmasını söyledim
            trackBar2.Value = hareket2;
            trackBar3.Value = hareket3;
            trackBar4.Value = hareket4;
            trackBar5.Value = hareket5;

            label1.Text = "Position: " + hareket1.ToString(); //string cinsinden labele yazacak
            label2.Text = "Position: " + hareket2.ToString();
            label3.Text = "Position: " + hareket3.ToString();
            label4.Text = "Position: " + hareket4.ToString();
            label5.Text = "Position: " + hareket5.ToString();


       

            SendServoInfo(0, hareket1);   // bunları yine yazın aşağıda detaylı açıklayacağım
            SendServoInfo(1, hareket2);  
            SendServoInfo(2, hareket3);
            SendServoInfo(3, hareket4);
            SendServoInfo(4, hareket5);
         


        }





        private void SendServoInfo(int channel, int pos)  // sendservoinfo fonk. oluşturdum 
        {
            string message = channel.ToString() + ':' + pos.ToString() + '*'; //split diye bi method var 
                     //bu method sayesinde bilgileri ayırabiliyoruz yani pozisyon bilgimiz herzaman yıldızlı gidecek
                     // hangi kanal olacağıda iki noktalı bilgi olarak gidecek
                     //yine string cinsinden
            try
            {
                serialport.Write(message);  //seri porta messageyi yaz komutu biz messageyi 1 satır yukarıda
                                            //string cinsinden verdik yani hep sayı gidiyor

            }
            catch
            {

            }

        }

        private void ResetServos()
        {
            int centrePosition = 90;
            trackBar1.Value = centrePosition;
            trackBar2.Value = centrePosition;
            trackBar3.Value = centrePosition;
            trackBar4.Value = centrePosition;
            trackBar5.Value = centrePosition;


            label1.Text = "Position: " + centrePosition.ToString();
            label2.Text = "Position: " + centrePosition.ToString();
            label3.Text = "Position: " + centrePosition.ToString();
            label4.Text = "Position: " + centrePosition.ToString();
            label5.Text = "Position: " + centrePosition.ToString();


         
                for (int channel = 0; channel < 5; channel++)
                {
                    SendServoInfo(channel, centrePosition);
                
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ResetServos();
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e) //form kapatılmadan önce yapılacak olaylar
        {
            //ben form kapatılmadan önce bütün servoları 90 dereceye çektiriyorum burası size kalmış
            ResetServos();

        }

       
    }

}


####################################################################################






####################################################################################


Arduino kodu

####################################################################################
//burda sanırım tek tek açıklamama gerek yok kod çok basit sadece split olayı biraz daha açıklayıcı oluyor orda : ve * bilgileri burda yine aynı şekilde yakalanıyor

#include <Servo.h>

int servoCount = 5;
int servoPins[] = {6, 5, 4, 3, 2};
Servo servos[5];

void setup() {
  Serial.begin(9600);
  AttachServos();

}

void loop() {
  
}

void serialEvent() {
  int channel;
  int pos;
  
  channel = Serial.readStringUntil(':').toInt();
  pos = Serial.readStringUntil('*').toInt();
  servos[channel].write(pos);
  
}

void AttachServos() {
  for(int i = 0; i < servoCount; i++) {
    servos[i].attach(servoPins[i]);
    
  }
  
}
