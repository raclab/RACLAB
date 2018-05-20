# RFID Güvenlik Sistemi
**Hazýrlayan: Ýrem KARABUDAK**

***

Bu klasörde, RFID Güvenlik Sistemi projesinin kodlarýna, projede yararlanýlan kütüphane linklerine, ve medya içeriklerine yer verilmiþtir.

***

_**Projede Kullanýlan Malzemeler:**_

*Arduino Pro(Atmega328P / 5v 16MHz)
*Protoboard
*3.7V 860mAh Li-Ion Battery
*RF433MHz Tx modülü
*TP4056 Battery Charger(5V 1A)
*Switch
*Step-Up modülü(Output:5V)
*AMS1117 Voltage Regulator(Output:3.3V)
*Arduino Logic Level Converter(3.3V-5V)
*RFID-RC522 modülü(13.56 MHz)
*S50 1K 13.56MHz RFID Kart x2
*NTAG213 13.56MHz IC NFC Tag(MIFARE Ultralight)
*Proje Kutusu(54mmx84mmx32mm)
*220ohm Direnç x3
*RGB Led
*CP2102 USB to TTL Converter modülü

_**Projede Alýcý Devresi Ýçin Kullanýlan Malzemeler:**_

*Arduino Nano(Atmega328P / 5v 16MHz)
*Mini Breadboard x2
*RF433MHz Rx modülü
*220ohm Direnç
*Yeþil Led
*Jumper kablolar

_**Yazýlýmýn Çalýþtýrýlma Þekli:**_

*Yazýlýmýn çalýþtýrýlmasý için gerekli olan kütüphaneler aþaðýdaki linkten indirilerek(versiyonuna dikkat edilmeli) Arduino IDE'deki "libraries" klasörüne atýlýr. Daha sonra Arduino, CP2102 USB to TTL modülü yardýmýyla bilgisayara baðlanýr ve "RFIDSecuritySystem.ino" uzantýlý kod, "iþlemci", "kart" ve "port" bilgileri(Atmega328P/Arduino Pro/COM...) seçildikten sonra yüklenir. Sistemin yazýlýmýnýn yüklenmesi tamamlanmýþ olur.

_**Edinilmesi Gereken Kütüphaneler ve Linkleri:**_

*MFRC522.h - https://github.com/miguelbalboa/rfid
*RCSwitch.h(version: 2.6.2) - https://github.com/sui77/rc-switch

***

Sistemin kodu RFIDSecuritySystem.ino, alýcý kodu ise RF_Receiver.ino dosyasýndadýr.

***

_**Donanýmýn Baðlantýsý ve Çalýþma Þekli:**_

*Sistem elemanlarý protoboard üzerine yerleþtirilmiþ ve lehimlenmiþtir. Bu elemanlarýn GND pinleri birleþtirilmiþtir.
*Proje 3.7V bir Li-Ion bataryadan gücünü almaktadýr. 
*Batarya TP4056 destekli þarj ve koruma devresine baðlýdýr ve koruma devresinin çýkýþlarý da bir switch yoluyla 5V step-up modülünün giriþine baðlanmýþtýr. 5V step-up modülünün çýkýþý hem Arduino Pro (5v 16Mhz) hem 433Mhz RF Tx modülü hem de AMS1117-3.3V LDO'yu beslemektedir.LDO'nun 3.3V çýkýþý da RFID modülünün güç pinine baðlanmýþtýr. 
*RFID modülünün, Tx modülünün ve RGB ledin Arduino ile olan baðlantý þekli kodun üst kýsmýndaki açýklama bölümünde verilmiþtir.

_**Projenin Kullaným Þekli:**_

*Oluþturulan güvenlik sisteminin aktif hale gelebilmesi için switch sola çekilerek ON konumuna getirilir. Sistem çalýþtýrýldýðýnda ilk alýnan geri bildirim, ledin rengidir. Led, kullanýcýya önceki çalýþmadaki son durum verisini(kýrmýzý(off)/yeþil(on)) bildirmektedir.
*Deðiþim kartý bir kez okutulur, 500ms boyunca mavi geri bildirim ledi yanar. Daha sonra sisteme eklenmek istenen kart okutulur. Eðer sisteme ilk kez kart okutuluyorsa, 800ms; ikinci bir kart okutuluyorsa, 1600ms boyunca bildirim ledi(mavi) yanar ve kart ekleme iþlemi tamamlanýr.
*Sistem, 2 kart slotuna sahiptir. Üçüncü bir kart sisteme eklenmek istendiðinde, sistem tanýmsýz kart olarak algýlar ve kýsa aralýklarla(300ms) 3 kez bildirim ledi yanýp söner.
*Deðiþim kartý arka arkaya 2 kez okutulduðunda, sistemdeki tanýmlý kartlar silinir. Kýsa aralýklarla(100ms) 8 kez bildirim ledi yanýp söner.
*Sistemde tanýmlý olan bir kart okutulduðunda aç/kapat kontrol iþlemini yapar. Yeþil(ON) ve kýrmýzý(OFF) led ile 1sn boyunca geri bildirim alýnýr ve bu sýrada RF verici modülü ile açma ve kapatma sinyali 10ms aralýkla 2 defa gönderilir. Karþýda bir alýcý devresi olduðu taktirde bir baþka cihazýn da endüstriyel anahtarlama kontrolü ayný þekilde saðlanabilir.






