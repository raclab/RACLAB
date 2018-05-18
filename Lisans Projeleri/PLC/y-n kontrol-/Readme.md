PLC İLE DC MOTOR KONTROLÜ
Giriş çıkış isimleri
 
   Girişler;
1.	START(I0.0)---Sistemi başlatma butonu
2.	STOP(I0.1)---Sistemi durdurma butonu
3.	SÜREKLİ(I0.2)---Sürekli çalıştırma butonu
4.	KESİKLİ(I0.3)---Kesikli çalıştırma butonu
5.	STOP(1)(I0.4)¬¬---Çalışan motoru durdurma butonu
6.	İLERİ(I0.5)---İleri yönde çalıştırma butonu
7.	GERİ(I0.6)---Geri yönde çalıştırma butonu
    Çıkışlar;
1.	M_İLERİ(Q0.0)---Motoru ileri yönde sürmek için röleyi tetikler
2.	M_GERİ(Q0.1)---Motoru geri yönde sürmek için röleyi tetikler
3.	START(1)(Q0.2)---Motorun çalışmaya hazır durumda olduğunu anlamak için röleyi anahtarlar(Röleye lamba bağlanır)
4.	STOP(2)(Q0.3)---Motorun çalışmaya hazır durumda olmadığını anlamak için röleyi anahtarlar(Röleye lamba bağlanır)
5.	SAĞA DÖNÜŞ(Q0.4)---Motorun sağa döndüğünü anlamak için röleyi anahtarlar(Röleye lamba bağlanır)
6.	SOLA DÖNÜŞ(Q0.5)---Motorun sola döndüğünü anlamak için röleyi anahtarlar(Röleye lamba bağlanır)
7.	SÜREKLİ ÇALIŞIYOR(Q0.6)---Motorun sürekli çalıştığını  anlamak için röleyi anahtarlar(Röleye lamba bağlanır)
8.	KESİKLİ ÇALIŞIYOR(Q0.7)---Motorun kesikli çalıştığını  anlamak için röleyi anahtarlar(Röleye lamba bağlanır)

NETWORK 1
Sistemin başlaması için start butonuna basılması gerekmektedir. Start butonuna basıldığında mühürleme kontağı yardımıyla stop butonuna basılana kadar sistem çalışmaya devam eder.

NETWORK 2
Kesikli ve sürekli çalışmayı kontrol etmek için hangi şekilde çalıştırılmak isteniyorsa o butona basılmalıdır. Sürekli çalışma butonuna bir sefer basıldığında mühürleme kontağı yardımıyla kesikli çalışma butonuna basılana kadar sistem sürekli çalışır.

NETWORK 3 
Motor sağa doğru dönerken sola dön komutu almaz. Stop(1) butonuna basılınca çalışmayı durdurur.

NETWORK 4
Motor sola doğru dönerken sağa dön komutu almaz. Stop(1) butonuna basınca çalışmayı durdurur.

NETWORK 5
Motorun hangi durumda olduğunu anlamak için yapılmıştır. Çıkışlara röle bağlanır.(PLC’ye zarar vermemek için)

Ekteki dosya(KESİKLİ SÜREKLİ ÇALIŞMA DC) tia portalda yapılmış projedir.
