# RFID Güvenlik Sistemi
**Hazırlayan: İrem KARABUDAK**

***

Bu klasörde, RFID Güvenlik Sistemi projesinin kodlarına, projede yararlanılan kütüphane linklerine, ve medya içeriklerine yer verilmiştir.

***

_**Projede Kullanılan Malzemeler:**_

* Arduino Pro(Atmega328P / 5v 16MHz)
* Protoboard
* 3.7V 860mAh Li-Ion Battery
* RF433MHz Tx modülü
* TP4056 Battery Charger(5V 1A)
* Switch
* Step-Up modülü(Output:5V)
* AMS1117 Voltage Regulator(Output:3.3V)
* Arduino Logic Level Converter(3.3V-5V)
* RFID-RC522 modülü(13.56 MHz)
* S50 1K 13.56MHz RFID Kart x2
* NTAG213 13.56MHz IC NFC Tag(MIFARE Ultralight)
* Proje Kutusu(54mmx84mmx32mm)
* 220ohm Direnç x3
* RGB Led
* CP2102 USB to TTL Converter modülü

_**Projede Alıcı Devresi İçin Kullanılan Malzemeler:**_

* Arduino Nano(Atmega328P / 5v 16MHz)
* Mini Breadboard x2
* RF433MHz Rx modülü
* 220ohm Direnç
* Yeşil Led
* Jumper kablolar

_**Yazılımın Çalıştırılma Şekli:**_

* Yazılımın çalıştırılması için gerekli olan kütüphaneler aşağıdaki linkten indirilerek(versiyonuna dikkat edilmeli) Arduino IDE'deki "libraries" klasörüne atılır. Daha sonra Arduino, CP2102 USB to TTL modülü yardımıyla bilgisayara bağlanır ve "RFIDSecuritySystem.ino" uzantılı kod, "işlemci", "kart" ve "port" bilgileri(Atmega328P/Arduino Pro/COM...) seçildikten sonra yüklenir. Sistemin yazılımının yüklenmesi tamamlanmış olur.

_**Edinilmesi Gereken Kütüphaneler ve Linkleri:**_

* MFRC522.h - https://github.com/miguelbalboa/rfid
* RCSwitch.h(version: 2.6.2) - https://github.com/sui77/rc-switch

***

Sistemin kodu RFIDSecuritySystem.ino, alıcı kodu ise RF_Receiver.ino dosyasındadır.

***

_**Donanımın Bağlantısı ve Çalışma Şekli:**_

* Sistem elemanları protoboard üzerine yerleştirilmiş ve lehimlenmiştir. Bu elemanların GND pinleri birleştirilmiştir.
* Proje 3.7V bir Li-Ion bataryadan gücünü almaktadır. 
* Batarya TP4056 destekli şarj ve koruma devresine bağlıdır ve koruma devresinin çıkışları da bir switch yoluyla 5V step-up modülünün girişine bağlanmıştır. 5V step-up modülünün çıkışı hem Arduino Pro (5v 16Mhz) hem 433Mhz RF Tx modülü hem de AMS1117-3.3V LDO'yu beslemektedir.LDO'nun 3.3V çıkışı da RFID modülünün güç pinine bağlanmıştır. 
* RFID modülünün, Tx modülünün ve RGB ledin Arduino ile olan bağlantı şekli kodun üst kısmındaki açıklama bölümünde verilmiştir.

_**Projenin Kullanım Şekli:**_

* Oluşturulan güvenlik sisteminin aktif hale gelebilmesi için switch sola çekilerek ON konumuna getirilir. Sistem çalıştırıldığında ilk alınan geri bildirim, ledin rengidir. Led, kullanıcıya önceki çalışmadaki son durum verisini(kırmızı(off)/yeşil(on)) bildirmektedir.
* Değişim kartı bir kez okutulur, 500ms boyunca mavi geri bildirim ledi yanar. Daha sonra sisteme eklenmek istenen kart okutulur. Eğer sisteme ilk kez kart okutuluyorsa, 800ms; ikinci bir kart okutuluyorsa, 1600ms boyunca bildirim ledi(mavi) yanar ve kart ekleme işlemi tamamlanır.
* Sistem, 2 kart slotuna sahiptir. Üçüncü bir kart sisteme eklenmek istendiğinde, sistem tanımsız kart olarak algılar ve kısa aralıklarla(300ms) 3 kez bildirim ledi yanıp söner.
* Değişim kartı arka arkaya 2 kez okutulduğunda, sistemdeki tanımlı kartlar silinir. Kısa aralıklarla(100ms) 8 kez bildirim ledi yanıp söner.
* Sistemde tanımlı olan bir kart okutulduğunda aç/kapat kontrol işlemini yapar. Yeşil(ON) ve kırmızı(OFF) led ile 1sn boyunca geri bildirim alınır ve bu sırada RF verici modülü ile açma ve kapatma sinyali 10ms aralıkla 2 defa gönderilir. Karşıda bir alıcı devresi olduğu taktirde bir başka cihazın da endüstriyel anahtarlama kontrolü aynı şekilde sağlanabilir.






