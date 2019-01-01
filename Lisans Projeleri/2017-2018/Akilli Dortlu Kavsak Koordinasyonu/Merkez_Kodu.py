import socket           #Wi-Fi haberlesme icin socket kutuphanesi eklendi
import sys

TCP_IP = '172.20.10.6'  #baglanti yapilacak IP adresi belirlendi
TCP_PORT = 5007         #baglanti yapilacak PORT belirlendi
BUFFER_SIZE = 1024      #gonderilecek verinin uzunlugu belirlendi

while True:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #baglanti tanimlandi
	s.bind((TCP_IP, TCP_PORT))              #baglanti yapildi
	s.listen(1)                             #baglanti araniyor
	conn, addr = s.accept()                 #baglanti onaylandi
	print 'Connection address:', addr       #baglanti bilgileri ekrana yazdirildi

	data = conn.recv(BUFFER_SIZE)           #gelen veri okundu
	if data != "":                          #veri bos olmadigi surece
		print "received data:", data    #veriyi ekrana yazdirdi

		if data == "0.0    0.0":        #gelen veriye gore yol durumu belirlendi
			print "YOL MUSAIT"
		else:
			print "YOLDA ARAC VAR"

	conn.send(data)                         #vericiye verinin alindigina dair onay gonderdi
	TCP_PORT = TCP_PORT + 1                 #port sayisi surekli kullanilacagindan bir arttirildi
	print "************************************************"
#s.close()

