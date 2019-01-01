import numpy as np 		#numpy kutuphanesini ekledik
import cv2				#opencv kutuphanesini ekledik
import sys
import socket

cap = cv2.VideoCapture('video.mp4')	 		#hangi videonun alinacagi belirlendi
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()		#uygulanacak maske belirlendi
ret, frame = cap.read()					#videodan ilk frame alindi
TCP_IP = '172.20.10.6'                                  #Wi-Fi haberlesme icin IP adresi belirlendi
TCP_PORT = 5006                                         #Wi-Fi haberlesme icin PORT belirlendi
BUFFER_SIZE = 1024  			                #gonderilecek verinin uzunlugu belirlendi

while(1):

	ret, frame = cap.read()				#surekli olarak frame aliniyor
	fgmask = fgbg.apply(frame)			#maske her frame'e uygulaniyor	

	sinir1 = cv2.line(frame,(320,150),(420,150),(0,255,255),2)			#sinir belirlendi
	
	lblack1 = []			 #beyaz ve siyah renklerin yogunluklari icin diziler olusturuldu
	lwhite1 = []
	lblack2 = []
	lwhite2 = []

   	for i in xrange(320,370):						#verilen koordinatlar icin beyaz ve siyah
			if(fgmask[160,i] == 255):				#renklerin yogunluklari ilgili dizilere
				lwhite1.append([160,i])				#eklendi
			else:
				lblack1.append([160,i])
	for j in xrange(371,420):
			if(fgmask[160,j] == 255):
				lwhite2.append([160,j])
			else:
				lblack2.append([160,j])


	weight1 = float(len(lwhite1)) / len(lblack1)		#beyaz oranlari hesaplandi
	weight2 = float(len(lwhite2)) / len(lblack2)
	cv2.putText(fgmask,str(weight1)[0:3],(20,300),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA) 	#beyaz oranlari
	cv2.putText(fgmask,str(weight2)[0:3],(200,300),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)	#yazdirildi
	string_value1 = str(weight1)                            #elde edilen beyaz oranlari float'tan string'e donusturuldu
	string_value2 = str(weight2)

	if(weight1 > 0.3):
		rect1 = cv2.rectangle(fgmask,(310,160),(370,200),(255,255,255),2)			#hem maskeli goruntude hem de orijinal
		rect3 = cv2.rectangle(frame,(310,160),(370,200),(255,255,0),2)				#goruntude araclar gosterildi
     

	if(weight2 > 0.25):
		rect2 = cv2.rectangle(fgmask,(370,160),(420,200),(255,255,255),2)
		rect4 = cv2.rectangle(frame,(370,160),(420,200),(255,255,0),2)
        gonder = string_value1 + '    ' + string_value2         #gonderilecek olan veriler birlestirildi

	cv2.imshow('frame',frame)				#orijinal goruntu gosteriliyor
	cv2.imshow('mask',fgmask)				#maskeli goruntu gosteriliyor
	cv2.moveWindow('mask', 650,0)			#maskeli goruntu ekranin sagina goturuldu
        cv2.moveWindow('frame' , 0,0)
	k = cv2.waitKey(30) & 0xff                      #esc tusuna basildiginda program kapanir
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           #socket baglantisi tanimlandi
        s.connect((TCP_IP, TCP_PORT))                                   #socket baglantisi yapildi
        s.send(gonder)                                                  #veri ana merkeze gonderildi
        data = s.recv(BUFFER_SIZE)                                      #merkezden verinin gonderildigine dair onay alindi
        print data                                                      #gonderilen veri ekrana yazdirildi
        TCP_PORT = TCP_PORT + 1                                         #surekli port degisimi icin port numarasi bir arttirildi
	if k == 27:                                                     #esc tusuna basildiginda donguden cikiyor
		break

cap.release()
cv2.destroyAllWindows()

