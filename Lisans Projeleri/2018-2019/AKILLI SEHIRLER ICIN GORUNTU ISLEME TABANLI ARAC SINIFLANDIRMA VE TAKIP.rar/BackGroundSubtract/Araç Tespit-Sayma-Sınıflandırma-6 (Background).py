
import cv2                                                      # Opencv kütüphanesi dahil edildi.
import numpy as np                                              # Numpy kütüphanesi dahil edildi.
import time                                                     # Zaman kütüphanesi dahil edildi.

offset = 14                                                     # Tolerans aralığı.
merkez_nokta = []                                               # Merkez noktalar icin bir dizi olusturuldu.
sayi = 0                                                        # Araç sayımı icin değisken belirlendi.

def merkezi_bulmak(c):                                          # Merkezi bulmak icin bir fonksiyon olusturuldu.
    M = cv2.moments(c)                                          # Ağırlık merkezini bulmamızı sağlar.
    cx = int(M['m10'] / M['m00'])                               # x koordinatı bulundu.
    cy = int(M['m01'] / M['m00'])                               # y koordinatı bulundu.
    return cx, cy                                               # x ve y koordinatları döndürüldü.

bs = cv2.bgsegm.createBackgroundSubtractorMOG()                 # Bir arka plan nesnesi oluşturuldu.

camera = cv2.VideoCapture("cars.mp4")                           # cars.mp4 videosu yakalandı.

frames_count, fps, width, height = camera.get(cv2.CAP_PROP_FRAME_COUNT), camera.get(cv2.CAP_PROP_FPS), camera.get(
    cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

width = int(width)
height = int(height)
print(frames_count, fps, width, height)                         # Video ile ilgili bazı gerekli bilgiler yazdırıldı.

while True:                                                     # Sonsuz bir döngü olusturuldu.
    t1 = time.time()                                            # İlk zaman bilgisi alındı.
    ret, frame = camera.read()                                  # Bu komut ile yakalanan görüntü okundu.
    frame_roi = frame[190:600, 100:1200]                        # Görüntünün belli bir kesiti alındı.
    # -----------------------------------------------------------------------------------------------------------------------
    gray = cv2.cvtColor(frame_roi, cv2.COLOR_RGB2GRAY)          # Görüntü gri formata çevrildi.
    blur = cv2.GaussianBlur(gray, (3, 3), 0)                    # Gauss filtresi uygulandı.
    fgmask = bs.apply(blur)                                     # Görüntünün ön plan çıkarıldı.
    th = cv2.threshold(fgmask.copy(), 220, 255, cv2.THRESH_BINARY)[1]   # Eşikleme uygulandı.   (220)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))   # Yarı capı olan yuvarlak bir çekirdek mstris olusturuldu.
                                                                    # (5x5 lik bir çekirdek olusturuldu.)

    closing = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=5)   # Küçük siyah noktaların kapatılmasında yararlıdır.

    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)     # Gürültünün çıkarılmasında faydalıdır

    erode = cv2.erode(opening, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=1)
                                                                    # Görüntü üzerinde asındırma yapıldı.

    dilated = cv2.dilate(erode, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)
                                                                    # Algıladıgımız nesne alanını arttırır.

    img, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                                                    # Tespit edilen nesnenin koordinatlari belirlendi.
                                                                    # 1. parametre uzerinde islem yapilacak parametre.
                                                                    # 2. parametre bu komut ile tespit edilen nesnenin en buyugu alinir.
                                                                # 3. parametre cv2.CHAIN_APPROX_SIMPLE veya cv2.CHAIN_APPROX_NONE kulanilir.
                                                            # cv2.CHAIN_APPROX_SIMPLE daha cok yer kaplar tum yeri bulur.
                                                    # cv2.CHAIN_APPROX_NONE sadece kose noktalari bulur. Boylece hafiza tasarrufu saglanir.

    cv2.line(frame_roi, (25, 3), (1200, 3), (0, 0, 255), 3)         # Görüntü üzerinde bir cizgi cizdirildi.
                                                                    # 1. parametre kaynak goruntu.
                                                                    # 2. parametre cizginin baslangic koordinati. (x,y)
                                                                    # 3. parametre cizginin bitis koordinati.   (x,y)
                                                                    # 4. parametre cizginin rengi.
                                                                    # 5. parametre cizginin kalinligi.

    cv2.line(frame_roi, (25, 300), (1200, 300), (0, 0, 255), 3)     # Görüntü üzerinde bir cizgi cizdirildi.

    for (i, c) in enumerate(contours):                              # Sınırlar c degiskenine, frame sayısı ise i degiskenine gönderildi.
        (x, y, w, h) = cv2.boundingRect(c)                          # Koordinatlar degiskenlere gonderildi.
        min_deger = (w >= 40) and (h >= 40)                         # Nesne icin minimum boyutlar.
        if not min_deger:                                           # Eğer tespit edilen nesnenin boyutu bu şekilde değii ise,
            continue                                                # Bir işlem atlanır.

        if (50 <= w <= 80) and (50 <= h <= 80) :                    # Eğer bu aralıkta ise,
            Arac = "Bike"                                           # Arac motorsiklettir.
            cv2.putText(frame_roi, Arac, (x-5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                                                    # Ekrana aracın türü yazdırıldı.
                                                                    # 1. parametre kaynak görüntü.
                                                                    # 2. parametre eklenecek metin kısmı.
                                                                    # 3. parametre metnin baslayacagı koordinatlar.
                                                                    # 4. parametre yazı tipi.
                                                                    # 5. parametre yazının yuksekligi.
                                                                    # 6. parametre yazının rengi. (BGR)
                                                                    # 7. parametre yazının kalınlığı.

        elif (80 < w <= 200) and (80 < h <= 200) :                  # Eğer bu aralıkta ise,
            Arac = "Car"                                            # Arac arabadır.
            cv2.putText(frame_roi, Arac, (x-5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                                                    # Ekrana aracın türü yazdırıldı.

        elif (w > 200) and (h > 200) :                              # Eğer bu aralıkta ise,
            Arac = "Truck"                                          # Araç kamyondur.
            cv2.putText(frame_roi, Arac, (x-5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                                                    # Ekrana aracın türü yazdırıldı.

        cv2.rectangle(frame_roi, (x, y), (x + w, y + h), (255, 255, 0), 2)
                                                                    # Tespit edilen nesne dikdortgen icine alindi.
                                                                    # 1. parametre islem yapılacak görüntü.
                                                                    # 2. parametre tespit edilen nesnenin sol üst koordinatları.
                                                                    # 3. parametre tespit edilen nesnenin sağ alt koordinatları.
                                                                    # 4. parametre çizilen dikdörtgenin rengi. (BGR)
                                                                    # 5. parametre çizilen dikdörtgenin kalınlığı.

        merkez = merkezi_bulmak(c)                                  # Bu komut ile nesnenin koordinatları değiskenlere atandı.
        merkez_nokta.append(merkez)                                 # Bu koordinatlar merkezi_nokta adlı diziye gönderildi.

        cv2.circle(frame_roi, (merkez), 4, (0, 0, 255), -1)         # Tespit edilen nesnenin merkezine bir daire cizdirildi.,
                                                                    # 1. parametre islem yapılacak görüntü.
                                                                    # 2. parametre cemberin merkez koordinatları.
                                                                    # 3. parametre çemberin yarıcapı.
                                                                    # 4. parametre cemberin rengi.
                                                                    # 5. parametre cemberin kalınlıgı. (-1 olursa ici dolu daire cizer.)

        for (x, y) in merkez_nokta:                                 # Tespit edilen koordinatlar degiskenlere gönderildi.

            if y < (300 + offset) and y > (300 - offset):           # Eger y koordinatı bu aralıkta tespit edilirse,
                sayi += 1                                           # Araç sayısı 1 arttırılır.
                cv2.line(frame_roi, (25, 300), (1200, 300), (0, 255, 0), 3)
                                                                    # Görüntü üzerinde bir cizgi cizdirildi.
                                                                    # 1. parametre kaynak görüntü.
                                                                    # 2. parametre cizginin başlangıç koordinatı. (x,y)
                                                                    # 3. parametre cizginin bitiş koordinatı.  (x,y)
                                                                    # 4. parametre cizginin rengi.
                                                                    # 5. parametre cizginin kalınlığı.

                merkez_nokta.remove((x, y))                         # Daha sonra bu diziden merkezi koordinatlar kaldırıldı.
                print("Arac Sayisi: " + str(sayi))                  # Arac sayısı ekrana yazdırıldı.

    cv2.putText(frame_roi, "Count :" + str(sayi), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
                                                                    # Bu komut metin yazdırmayı sağlar.
                                                                    # 1. parametre kaynak görüntü.
                                                                    # 2. parametre eklenecek metin kısmı.
                                                                    # 3. parametre metnin baslayacağı koordinatlar.
                                                                    # 4. parametre yazı tipi.
                                                                    # 5. parametre yazının yuksekliği.
                                                                    # 6. parametre yazının rengi. (BGR)
                                                                    # 7. parametre yazının kalınlığı.

    cv2.imshow("Orjinal frame", frame)                              # Orjinal görüntü ekrana getirildi.
    #cv2.imshow("gray", gray)                                        # Gri formata donüştürülen görüntü ekrana getirildi.
    #cv2.imshow("blur", blur)                                        # Gauss filtresi uygulanan görüntü ekrana getirildi.
    #cv2.imshow("fgmask", fgmask)                                    # Görüntünün önplanı ekrana getirildi.
    #cv2.imshow("Thresh", th)                                        # Eşikten geçirilen görüntü ekrana getirildi.
    #cv2.imshow("closing", closing)                                  # Closing uygulanan Görüntü ekrana getirildi.
    #cv2.imshow("opening", opening)                                  # Opening uygulanan Görüntü ekrana getirildi.
    #cv2.imshow("Erode", erode)                                      # Aşındırma uygulanan görüntü ekrana getirildi.
    #cv2.imshow("Dilate", dilated)                                   # Genişleme uygulanan görüntü ekrana getirildi.
    cv2.imshow("Frame Roi", frame_roi)                              # Görüntüde işlem yapılan kısım ekrana getirildi.

    t2 = time.time()                                                # FPS için ikinci zaman bilgisi alındı.
    FPS = (1/(t2-t1))                                               # FPS hesaplandı. (frame per second)
    print("FPS",FPS)                                                # FPS değeri yazdırıldı.

    k = cv2.waitKey(30) & 0xFF
    if k == 27:                                                     # Eğer ESC tuşuna basılırsa,
        break                                                       # Döngü sonlandırılır.

camera.release()                                                    # Kamera serbest bırakıldı.
cv2.destroyAllWindows()                                             # Bütün pencereler kapatıldı.

