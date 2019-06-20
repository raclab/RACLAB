import cv2
import numpy as np
import http.client
import urllib
import time
import os,sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



offset = 14

merkez_nokta = []
sayi = 0
sayi1 = 0
sayi2 = 0
sayi3 = 0
key = 'OG8IK5UPMG36XOSY'




veri = open("veri.txt", "w")


def veri_gonder(sayi,sayi1,sayi2,sayi3):
    
    while True:
        params = urllib.parse.urlencode({'field1':sayi1,'field2':sayi2,'field3':sayi3,'field4':sayi,'key':key})
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        veri.write(str(sayi))
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            
        except:
            print ("connection failed"),sys.exc_info()
            
        
        data = response.read()
        conn.close()
        break
    
    

def merkezi_bulmak(c):
    M = cv2.moments(c)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    return cx, cy
    # cv2.bgsegm.createBackgroundSubtractorMOG()
    # cv2.createBackgroundSubtractorKNN(dist2Threshold =400.0, detectShadows = True)

bs = cv2.bgsegm.createBackgroundSubtractorMOG()

camera = cv2.VideoCapture("cars.mp4")

frames_count, fps, width, height = camera.get(cv2.CAP_PROP_FRAME_COUNT), camera.get(cv2.CAP_PROP_FPS), camera.get(
    cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

width = int(width)
height = int(height)
print(frames_count, fps, width, height)

m = 0
frame_counter = 0
mn=0

while (True):
    
    ret, frame = camera.read()
    frame_roi = frame[190:600, 100:1200]
    frame_counter += 1
    #cv2.imshow("frame_roi", frame_roi)
    # -----------------------------------------------------------------------------------------------------------------------
    gray = cv2.cvtColor(frame_roi, cv2.COLOR_RGB2GRAY)
    #cv2.imshow("gray", gray)

    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    #cv2.imshow("blur", blur)

    fgmask = bs.apply(blur)
    #cv2.imshow("fgmask", fgmask)

    th = cv2.threshold(fgmask.copy(), 220, 255, cv2.THRESH_BINARY)[1]
    #cv2.imshow("Thresh", th)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    closing = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=5)
    #cv2.imshow("closing", closing)

    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    #cv2.imshow("opening", opening)

    erode = cv2.erode(opening, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=1)

    dilated = cv2.dilate(erode, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)

    x,contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame_roi, (25, 3), (1200, 3), (0, 0, 255), 3)

    cv2.line(frame_roi, (25, 300), (1200, 300), (0, 0, 255), 3)

    for (i, c) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(c)
        min_deger = (w >= 40) and (h >= 40)
        if not min_deger:
            continue

        if (50 <= w <= 80) and (50 <= h <= 80) :
            Arac = "Motosiklet"
            cv2.putText(frame_roi, Arac, (x-5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        elif (80 < w <= 200) and (80 < h <= 200) :
            Arac = "Araba"
            cv2.putText(frame_roi, Arac, (x-5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        elif (w > 200) and (h > 200) :
            Arac = "Kamyon"
            cv2.putText(frame_roi, Arac, (x-5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.rectangle(frame_roi, (x, y), (x + w, y + h), (255, 255, 0), 2)

        merkez = merkezi_bulmak(c)
        merkez_nokta.append(merkez)

        cv2.circle(frame_roi, (merkez), 4, (0, 0, 255), -1)

        for (x, y) in merkez_nokta:

            if y < (300 + offset) and y > (300 - offset):
                sayi += 1
                cv2.line(frame_roi, (25, 300), (1200, 300), (0, 255, 0), 3)

                merkez_nokta.remove((x, y))
                print("Arac Sayisi: " + str(sayi))

    cv2.putText(frame_roi, "Sayi: " + str(sayi), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    
    
    
    cv2.imshow("Orjinal frame", frame)
    #cv2.imshow("fgmask", fgmask)
    #cv2.imshow("Erode", erode)
    #cv2.imshow("Dilate", dilated)
    # cv2.imshow("Diff", frame & cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR))
    #cv2.imshow("Frame Roi", frame_roi)

    sayi2=sayi+2
    sayi3=sayi-5
    sayi1=sayi+5
    
    m = m+1
    mn= mn+1
    if mn==350:
        sayi2=sayi-8
        sayi3=sayi-6
        sayi4=sayi+9
        mn=0
    if m == 300:
        veri_gonder(sayi,sayi1,sayi2,sayi3)
        sayi=0
        sayi1=0
        sayi2=0
        sayi3=0
        
        m=0
        
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
    
    if frame_counter == camera.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0 #Or whatever as long as it is the same as next line
        #camera.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
        camera = cv2.VideoCapture("cars.mp4")

    

camera.release()
    
#camera = cv2.VideoCapture("cars.mp4")
#veri_gonder(sayi)
#time.sleep(3)
cv2.destroyAllWindows()
