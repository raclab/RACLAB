
PLC İLE DC MOTOR KONTROLÜ Giriş çıkış isimleri

Girişler;

START(I0.0)---Sistemi başlatma butonu(NO Buton bağalanır.)
STOP(I0.1)---Sistemi durdurma butonu(NC Buton bağalanır.)
HIZ ARTTIR(I0.2)---Hız arttırma butonu(NO Buton bağalanır.)
HIZ AZALT(I0.3)---Hız azaltma butonu(NO Buton bağalanır.)
HIZ RESET(I0.4)---Hız resetleme butonu(NO Buton bağalanır.)

NETWORK 1 Klasik bir mühürleme devresi yapılmıştır

NETWORK 2 PWM oranını belirlemek için bir aşağı yukarı sayıcı tasarımı yapılmıştır. 
Clock bitleri ve pozitif kenar tetikleme kullanılmıştır. 
Clock bitlerini aktif etmek için PLC ayarlarından systen and clock memory e girim clock bitlrini enable etmek gerekir.

NETWORK 3 Sayıcıda olan sayı move bloğu yardımıyla PWM hafızasına atılır

NETWORk 4 PWM hafızasındaki sayı PWM blok yardımıyla çıkışa atılır.(PWM bloğu enable etmeyi unutmayın)
PWM çıkışın aktif olması için PLC ayarlarından PWM'i aktif etmek gerekir.(PWM'i enable edip, tim bese yi microseconds seçiniz,
pulse duration format i hunredths seçiniz, ınitial pulse duration u 50 yapınız.)

Ekteki dosya(HIZ KONTROL) tia portalda yapılmış projedir.
