import time
import math
import cv2
import numpy as np
import random


outerCircleMultiplier = 5.0/3
innerCircleMultiplier = 4.0/3
cornerList = []


def circleWaypointEnumarater(WP1,WP2,wpList):
    #Put circleWaypoints in an order. [In what order this waypoints will be processed.]
    #IMPORTANT! This function is not neccessary but in order to finish writing quickly, I avoided creating more complex algorithm.
    #This entire function gonna be deleted, and much faster version of this calculation will be moved to circleIteration function.

    enumaretedList = [WP1[1]]

    while True:
        if(len(wpList) == 0):
            break

        dist1 = 999999999999999
        counter = 0
        for wp in xrange(len(wpList)):
            dist2 = math.sqrt((math.pow((wpList[wp][0]-enumaretedList[-1][0]),2) + math.pow((wpList[wp][1]-enumaretedList[-1][1]),2)))
            if(dist2<dist1):
                dist1 = dist2
                counter = wp
        enumaretedList.append(wpList[counter])
        del wpList[counter]



    del enumaretedList[0]

    return enumaretedList



def circleIteration(WP1,WP2,circle):
    #Find the waypoints around the circle
    #Example WP list    => [x,y]
    #Example circle list=> [circleNumber, [x,y], circleRadius]


    wpCheckList = []
    wpList = []

    global outerCircleMultiplier
    global innerCircleMultiplier

    x1,y1 = WP1[1][0],WP1[1][1]
    x2,y2 = WP2[1][0],WP2[1][1]

    xc,yc = circle[1]
    rout = circle[2]*outerCircleMultiplier
    rin  = circle[2]*innerCircleMultiplier
    if(x2==x1):
        a1 = 1
        b1 = -2.0*yc
        c1 = xc*xc + yc*yc + x1*x1 - 2*x1*xc - rout*rout

        delta = b1*b1 - 4*a1*c1

    elif(y2==y1):
        a1 = 1
        b1 = -2.0*xc
        c1 = xc*xc + yc*yc + y1*y1 - 2*y1*yc - rout*rout

        delta = b1*b1 - 4*a1*c1


    else:

        a = float(y2-y1)/(x2-x1)
        b = float(x2*y1 - x1*y2)/(x2-x1) 


        a1 = a*a + 1
        b1 = 2*a*b - 2*xc-2*a*yc
        c1 = xc*xc + yc*yc + b*b - 2*b*yc - rout*rout

        delta = b1*b1 - 4*a1*c1

    if(delta>0):
        if(x2==x1):
            y11 = (-b1 - math.sqrt(delta))/(2*a1)
            y12 = (-b1 + math.sqrt(delta))/(2*a1)
            x11 = x1
            x12 = x1


        elif(y2==y1):
            x11 = (-b1 - math.sqrt(delta))/(2*a1)
            x12 = (-b1 + math.sqrt(delta))/(2*a1)
            y11 = y1
            y12 = y1



        else:
            x11 = (-b1 - math.sqrt(delta))/(2*a1)
            x12 = (-b1 + math.sqrt(delta))/(2*a1)
            y11 = a*x11 + b
            y12 = a*x12 + b


        wpList.append([x11,y11])
        wpList.append([x12,y12])
        wpCheckList.append([[x11,y11],[x12,y12]])

        while(True):
            if(len(wpCheckList) == 0):
                break

            tempList = wpCheckList.pop()

            for wp in xrange(1,len(tempList)):
                #Check if the point intercept with inner circle.
                x1,y1 = tempList[0]
                x2,y2 = tempList[wp]

                if(x2 ==x1):
                    a1 = 1
                    b1 = -2.0*yc
                    c1 = xc*xc + yc*yc + x1*x1 - 2*x1*xc - rin*rin

                    delta = b1*b1 - 4*a1*c1

                elif(y2==y1):
                    a1 = 1
                    b1 = -2.0*xc
                    c1 = xc*xc + yc*yc + y1*y1 - 2*y1*yc - rin*rin

                    delta = b1*b1 - 4*a1*c1

                else:
                    a = float(y2-y1)/(x2-x1)
                    b = float(x2*y1 - x1*y2)/(x2-x1)

                    a1 = a*a + 1
                    b1 = 2*a*b - 2*xc- 2*a*yc
                    c1 = xc*xc + yc*yc + b*b - 2*b*yc - rin*rin

                    delta = b1*b1 - 4.0*a1*c1

                
                if(delta>0):
                    x1,y1 = tempList[0]
                    x2,y2 = tempList[wp]

                    xn,yn = ((x1 + x2)/2) , ((y1 + y2)/2)

                    if(x2==x1):
                        #y = yn

                        a1 = 1
                        b1 = -2*xc
                        c1 = xc*xc + yc*yc + yn*yn -2*yn*yc - rout*rout

                        delta = b1*b1 - 4*a1*c1

                        xcout1 = (-b1 - math.sqrt(delta))/(2*a1)
                        xcout2 = (-b1 + math.sqrt(delta))/(2*a1)

                        ycout1 = yn
                        ycout2 = yn

                    elif(y2==y1):
                        #x = xn

                        a1 = 1
                        b1 = -2*yc
                        c1 = xc*xc + yc*yc + xn*xn -2*xn*xc - rout*rout

                        delta = b1*b1 - 4*a1*c1

                        ycout1 = (-b1 - math.sqrt(delta))/(2*a1)
                        ycout2 = (-b1 + math.sqrt(delta))/(2*a1)

                        xcout1 = xn
                        xcout2 = xn

                    else:

                        a = float((y2-y1)/(x2-x1))

                        b = xn/a + yn
                        a = -1/a

                        a1 = a*a + 1
                        b1 = 2*a*b - 2*xc- 2*a*yc
                        c1 = xc*xc + b*b - 2*b*yc + yc*yc - rout*rout

                        delta = b1*b1 - 4*a1*c1

                        xcout1 = (-b1 - math.sqrt(delta))/(2*a1)
                        xcout2 = (-b1 + math.sqrt(delta))/(2*a1)

                        ycout1 = a*xcout1 + b
                        ycout2 = a*xcout2 + b

                    dist1 = math.sqrt(((math.pow((xcout1-xn),2))+math.pow((ycout1-yn),2)))
                    dist2 = math.sqrt(((math.pow((xcout2-xn),2))+math.pow((ycout2-yn),2)))

                    #img = np.zeros((1024,1024,3),np.uint8)
                    #cv2.circle(img, (int(x1),int(y1)),2,(255,255,255),-1)
                    #cv2.circle(img, (int(x2),int(y2)),2,(255,255,255),-1)
                    #cv2.circle(img, (int(xc),int(yc)),int(rin), (0,255,0), 1 )
                    #cv2.circle(img, (int(xc),int(yc)),int(rout),(255,0,0), 1 )
                    #cv2.imshow('frame',img)
                    #cv2.waitKey(0)


                    if(dist1<=dist2):
                        wpCheckList.append([[xcout1,ycout1],[x1,y1],[x2,y2]])
                        wpList.append([xcout1,ycout1])
                    else:
                        wpCheckList.append([[xcout2,ycout2],[x1,y1],[x2,y2]])
                        wpList.append([xcout2,ycout2])

                else:
                    pass    
            


    wpList = circleWaypointEnumarater(WP1,WP2,wpList)

    return wpList


def collisionCheck(WP1,WP2,circles):
    #Checks if there is any collision with circles on the way.

    circleCollision = []
    updatedWP = []


    #First step is creating an area and only make calculation with circles in that area. (Makes program faster)
    circleList = limitArea(WP1,WP2,circles)


    #Now, we have to check if there is any collision with circles (well, this is the point of whole program..)
    #There may be more than one collisions, so if this is the case we should put them in order. 
    #Shorting will be done by bubble algorithm.

    #Example circles list   => [ [circleNumber,[x,y],circleRadius], ... ]
    #Example WP list        => [wpNumber,[x,y]]


    global innerCircleMultiplier
    global outerCircleMultiplier
    
    x1,y1 = WP1[1]
    x2,y2 = WP2[1]

    for circle in circleList:
        rin = circle[2] * innerCircleMultiplier
        rout = circle[2]* outerCircleMultiplier
        xc,yc = circle[1]
        if(x2==x1):
            a1 = 1
            b1 = -2*yc
            c1 = xc*xc + yc*yc + x1*x1 - 2*x1*xc - rin*rin

        elif(y2==y1):
            a1 = 1
            b1 = -2*xc
            c1 = xc*xc + yc*yc + y1*y1 -2*y1*yc - rin*rin

        else:
            a = (float(y2-y1)/(x2-x1))
            b = (float(x2*y1 - x1*y2)/(x2-x1))

            a1 = a*a + 1
            b1 = 2*a*b - 2*xc-2*a*yc
            c1 = xc*xc + yc*yc + b*b -2*b*yc -rin*rin

        delta = b1*b1 - 4*a1*c1

        if(delta>0):
            circleCollision.append(circle)

    #Sorting (Buble) Algorithm for circles that intercept. Closest one is first.

    for i in xrange(len(circleCollision)):
        for j in xrange(len(circleCollision)-i-1):
            dist0 = math.sqrt((pow((circleCollision[j][1][0]-x1),2) + pow((circleCollision[j][1][1]-y1),2)))
            dist1 = math.sqrt((pow((circleCollision[j+1][1][0]-x1),2) + pow((circleCollision[j+1][1][1]-y1),2)))

            if(dist0>dist1):
                circleCollision[j],circleCollision[j+1] = circleCollision[j+1], circleCollision[j]

    #This is where the magic begins.. 
    #Creation of waypoints around the circle

    wpList = []


    for circle in circleCollision:
        if(len(wpList) == 0):
            dist0 = math.sqrt((pow((WP1[1][0]-WP2[1][0]),2)+pow((WP1[1][1]-WP2[1][1]),2)))
            dist1 = math.sqrt((pow((WP1[1][0]-circle[1][0]),2)+pow((WP1[1][1]-circle[1][1]),2)))
            dist2 = math.sqrt((pow((WP2[1][0]-circle[1][0]),2)+pow((WP2[1][1]-circle[1][1]),2)))
            if((dist1<dist0) and (dist2<dist0)):
                wpList += circleIteration(WP1,WP2,circle)

        else:
            dist0 = math.sqrt((pow((wpList[-1][0]-WP2[1][0]),2)+pow((wpList[-1][1]-WP2[1][1]),2)))
            dist1 = math.sqrt((pow((wpList[-1][0]-circle[1][0]),2)+pow((wpList[-1][1]-circle[1][1]),2)))
            dist2 = math.sqrt((pow((WP2[1][0]-circle[1][0]),2)+pow((WP2[1][1]-circle[1][1]),2)))
            if((dist1<dist0) and (dist2<dist0)):
                wpList += circleIteration([1,wpList[-1]],WP2,circle)
            else:
                pass
    return wpList



def isPinRectangle(r,P):

    #r: A list of four points, each has a x- and a y- coordinate
    #P: A point

    #By the way, the code given in website is wrong (on purpose I believe). Just with a little touch, it will work like a charm.

    #Example of r=> [ [cornerNumber,[x,y]], ... ]
    #Example of P=> [x,y]

    #Area of rectangle  = 1/2*[(Ya-Yc)*(Xd-Xb) + (Yb-Yd)*(Xa-Xc)]
    #Area of triangle   = 1/2*[(Xa*(Yb-Yc) + Xb*(Yc-Ya) + Xc*(Ya-Yb))]



    areaRectangle = 0.5*abs(
        #                   y_A          y_C         x_D        x_B
                        (r[0][1][1]-r[2][1][1])*(r[3][1][0]-r[1][1][0])
        #                    y_B         y_D         x_A        x_C
                      + (r[1][1][1]-r[3][1][1])*(r[0][1][0]-r[2][1][0])
                    )


    ABP = 0.5*abs(
        #        x_A         y_B     y_P
             r[0][1][0]*(r[1][1][1]-P[1])
        #        x_B     y_P      y_A
            +r[1][1][0]*(P[1]-r[0][1][1])
        #     x_P      y_A        y_B
            +P[0]*(r[0][1][1]-r[1][1][1])
          )
    BCP = 0.5*abs(
        #        x_B         y_C     y_P
             r[1][1][0]*(r[2][1][1]-P[1])
        #        x_C      y_P     Y_B
            +r[2][1][0]*(P[1]-r[1][1][1])
        #     x_P      y_B        y_C
            +P[0]*(r[1][1][1]-r[2][1][1])
          )
    CDP = 0.5*abs(
        #        x_C         y_D     y_P
             r[2][1][0]*(r[3][1][1]-P[1])
        #        x_D      y_P     y_C
            +r[3][1][0]*(P[1]-r[2][1][1])
        #     x_P      y_C        y_D
            +P[0]*(r[2][1][1]-r[3][1][1])
          )
    DAP = 0.5*abs(
        #        x_D         y_A     y_P
             r[3][1][0]*(r[0][1][1]-P[1])
        #        x_A      y_P     y_D
            +r[0][1][0]*(P[1]-r[3][1][1])
        #     x_P      y_D        y_A
            +P[0]*(r[3][1][1]-r[0][1][1])
          )

    sumOfTriangles = ABP + BCP + CDP + DAP

    sumOfTriangles = float(str(sumOfTriangles)[0:(str(sumOfTriangles).find('.')+7)])
    areaRectangle  = float(str(areaRectangle)[0:(str(areaRectangle).find('.')+7)])

    return areaRectangle == sumOfTriangles


def areaCircles(cornerList,circles):
    #Finds circles in the limited area.
    #First it gets circles in the area and secondly it check if there is any intercept between lines and circle areas. 
    #Adds both of them to circleList.

    #Example circles list   => [ [circleNumber,[x,y],circleRadius], ... ]
    #Example cornerList     => [ [cornerNumber,[x,y]], ... ]
    #Extra information: cornerList is sorted already when its defined. I have no idea right now about circles list.

    #Well approach is not as simple as speaking about it but there is an awesome method that I found on internet.
    #Link: https://martin-thoma.com/how-to-check-if-a-point-is-inside-a-rectangle/
    #I must say, this is genius...  and I will copy it.
    global innerCircleMultiplier
    circleList = []


    #Are you in my love?
    for circle in circles:
        isPin = isPinRectangle(cornerList,circle[1])

        if(isPin):
            circleList.append(circle)
        #Now we will calculate if there is any interception?
        #Also we need to check if the intercepted circle already in the list? We don't want to check same circle twice..
        #I believe this is time for talking about inner and outer circles.. Inner circle is the area we don't want to take risk by entering
        #but it is not the actual circle area (it's larger than orginal circle area). Outer circle is where we put our waypoints on circle. They both
        #created for reducing interception risk with real circle. 
        #I didn't make the calculations for both inner and outer circle. Also it will be adjusted during the testes so I don't want to mess with it
        #right now. But in order to test my program I must assign a value to both inner and outer circles. 
        #Inner Circle ratio = circleRatio*(4/3), Outer Circle ratio = circleRatio*(5/3)
        #They will be defined as global variables in order to make changes quickly.
        #At this point we only need innerCircleMultiplier as imported above.

        else:

            r = circle[2]*innerCircleMultiplier 
            xc,yc = circle[1]


            for i in xrange(4):
                x1,y1 = cornerList[i][1]
                x2,y2 = cornerList[(i+1)%4][1]

                if(x2==x1):
                    a1 = 1
                    b1 = -2*yc
                    c1 = xc*xc + yc*yc + x1*x1 - 2*x1*xc - r*r 

                    delta = b1*b1 - 4.0*a1*c1

                elif(y2==y1):
                    a1 = 1
                    b1 = -2*xc
                    c1 = xc*xc + yc*yc +y1*y1 - 2*y1*yc - r*r

                    delta = b1*b1 - 4.0*a1*c1

                else:   
                    a = float((y2-y1)/(x2-x1))
                    b = float((x2*y1 - x1*y2)/(x2-x1))

                    a1 = a*a +1
                    b1 = 2*a*b - 2*xc - 2*a*yc 
                    c1 = xc*xc + b*b - 2*b*yc + yc*yc - r*r 

                    delta = b1*b1 - 4*a1*c1

                if(delta>0):
                    try:
                        if(circleList[-1][0] != circle[0]):
                            circleList.append(circle)
                    except:
                        circleList.append(circle)


    return circleList










def limitArea(WP1,WP2,circles):
    #Limits to area in order to prevent unneccessary calculations. (Only calculate circles between WPs)
    #Draw a rectangle between WPs. 
    #Draw rectangle with lines in order to see if there is any collision.
    '''                     *c5 (radius is large enough to break the line)
   1____________*c4_______________________________________________3
    |                                                            |
    |                                       *c1 (center is in)   |
    |                                                            |
    |                                                            |
    |                       *c3                                  |
  *1|   WP1 - - - - - - - - - - - - - - - - - - - - - - - - WP2  |*2
    |                                                            |
    |                                                            |
    |                       *c2                                  |
    |                                                            |
   2|____________________________________________________________|4
    '''
    #We will need four corner coordinates, which can be calculated by simple mathematical methods.
    #They will be enumarated same as the example above.
    #There will be needed to check if any of these line collide with any circle area.
    #Check 1-3 => 1-2 => 3-4 => 4-2
    #If any collide found, add them to list.
    #If center of any circle is in the rectangle, add them to list.
    #Only operate with calculated circle list. (There will be 30 circles, it will be good to prevent from calculating every 30 circles while checking
    #any collisions which will be calculate many times.)

    #Example WP list => [wpNumber,[x,y]]

    #Getting the *1 (In the example above deltaY = 0 but in reality it's gonna be rarely 0, therefore little bit more complex math required)
    global cornerList
    cornerList = []

    x1 = WP1[1][0]
    x2 = WP2[1][0]
    y1 = WP1[1][1]
    y2 = WP2[1][1]

    dist = math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))


    if(x2 == x1):

        #GETTING *1
        a1 = 1
        b1 = -2 * y1
        c1 = x1*x1 + y1*y1 + x1*x1 - 2*x1*x1 - ((0.2)*dist) * ((0.2)*dist)

        delta = b1*b1 - 4.0*a1*c1
        y11 = (-b1-math.sqrt(delta))/(2*a1)
        y12 = (-b1+math.sqrt(delta))/(2*a1)

        x11 = x1
        x12 = x1

        if(math.sqrt(math.pow((x11-x2),2) + math.pow((y11-y2),2)) > math.sqrt(math.pow((x12-x2),2) + math.pow((y12-y2),2))): 
            x1final = x11
            y1final = y11
        else:
            x1final = x12
            y1final = y12

        #GETTING *2
        a1 = 1
        b1 = -2 * y2
        c1 = x2*x2 + y2*y2 + x2*x2 - 2*x2*x2 - ((0.2)*dist) * ((0.2)*dist)

        delta = b1*b1 - 4.0*a1*c1
        y21 = (-b1-math.sqrt(delta))/(2*a1)
        y22 = (-b1+math.sqrt(delta))/(2*a1)

        x21 = x2
        x22 = x2

        if(math.sqrt(math.pow((x11-x2),2) + math.pow((y11-y2),2)) > math.sqrt(math.pow((x12-x2),2) + math.pow((y12-y2),2))): 
            x2final = x21
            y2final = y21
        else:
            x2final = x22
            y2final = y22

        #Calculation to get 1,2 via *1
        #y = y1final

        a1 = 1
        b1 = -2*x1final
        c1 = x1final*x1final + y1final*y1final + y1final*y1final - 2*y1final*y1final - ((1.0/3)*dist) * ((1.0/3)*dist)

        delta = b1*b1 - 4.0*a1*c1
        x11 = (-b1-math.sqrt(delta))/(2*a1)
        x12 = (-b1+math.sqrt(delta))/(2*a1)

        y11 = y1final
        y12 = y1final

        #Calculation to get 3,4 via *2
        #y = y2final

        a1 = 1
        b1 = -2*x2final
        c1 = x2final*x2final + y2final*y2final + y2final*y2final - 2*y2final*y2final - ((1.0/3)*dist) * ((1.0/3)*dist)

        delta = b1*b1 - 4.0*a1*c1
        x21 = (-b1-math.sqrt(delta))/(2*a1)
        x22 = (-b1+math.sqrt(delta))/(2*a1)

        y21 = y2final
        y22 = y2final


    elif(y2 == y1):

        #GETTING *1
        a1 = 1
        b1 = -2*x1
        c1 = x1*x1 + y1*y1 + y1*y1 - 2*y1*y1 - ((0.2)*dist) * ((0.2)*dist)

        delta = b1*b1 - 4.0*a1*c1
        x11 = (-b1-math.sqrt(delta))/(2*a1)
        x12 = (-b1+math.sqrt(delta))/(2*a1)

        y11 = y1
        y12 = y1

        if(math.sqrt(math.pow((x11-x2),2) + math.pow((y11-y2),2)) > math.sqrt(math.pow((x12-x2),2) + math.pow((y12-y2),2))): 
            x1final = x11
            y1final = y11
        else:
            x1final = x12
            y1final = y12

        #GETTING *2
        a1 = 1
        b1 = -2*x2
        c1 = x2*x2 + y2*y2 + y2*y2 - 2*y2*y2 - ((0.2)*dist) * ((0.2)*dist)

        delta = b1*b1 - 4.0*a1*c1
        x21 = (-b1-math.sqrt(delta))/(2*a1)
        x22 = (-b1+math.sqrt(delta))/(2*a1)

        y21 = y2
        y22 = y2

        if(math.sqrt(math.pow((x11-x2),2) + math.pow((y11-y2),2)) > math.sqrt(math.pow((x12-x2),2) + math.pow((y12-y2),2))): 
            x2final = x21
            y2final = y21
        else:
            x2final = x22
            y2final = y22


        #Calculation to get 1,2 via *1
        #x = x1final

        a1 = 1
        b1 = -2*y1final
        c1 = x1final*x1final + y1final*y1final + x1final*x1final - 2*x1final*x1final - ((1.0/3)*dist) * ((1.0/3)*dist)

        delta = b1*b1 - 4.0*a1*c1

        y11 = (-b1-math.sqrt(delta))/(2*a1)
        y12= (-b1-math.sqrt(delta))/(2*a1)

        x11 = x1final
        x12 = x1final

        #Calculation to get 3,4 via *2
        #x = x2final

        a1 = 1
        b1 = -2*y2final
        c1 = x2final*x2final + y2final*y2final + x2final*x2final - 2*x2final*x2final - ((1.0/3)*dist) * ((1.0/3)*dist)

        delta = b1*b1 - 4.0*a1*c1

        y21 = (-b1-math.sqrt(delta))/(2*a1)
        y22 = (-b1-math.sqrt(delta))/(2*a1)

        x21 = x1final
        x22 = x1final


    else:

        #GETTING *1
        a = (float(y2-y1)/(x2-x1))
        b = (float(x2*y1 - x1*y2)/(x2-x1))

        a1 = a*a +1 
        b1 = 2*a*b - 2*x1 - 2*a*y1
        c1 = x1*x1 + y1*y1 + b*b - 2*b*y1 - ((0.2)*dist) * ((0.2)*dist)


        delta1 = b1*b1 - 4*a1*c1

        x11 = (-b1-math.sqrt(delta1))/(2*a1)
        x12 = (-b1+math.sqrt(delta1))/(2*a1)

        y11 = (x11*(y2-y1) + x2*y2 - x1*y2 - x2*y2 + x2*y1)/(x2 - x1)
        y12 = (x12*(y2-y1) + x2*y2 - x1*y2 - x2*y2 + x2*y1)/(x2 - x1)

        if(math.sqrt(math.pow((x11-x2),2) + math.pow((y11-y2),2)) > math.sqrt(math.pow((x12-x2),2) + math.pow((y12-y2),2))): 
            x1final = x11
            y1final = y11
        else:
            x1final = x12
            y1final = y12

        #GETTING *2

        a1 = a*a +1 
        b1 = 2*a*b - 2*x2 - 2*a*y2
        c1 = x2*x2 + y2*y2 + b*b - 2*b*y2 - ((0.2*dist) * (0.2*dist))

        delta2 = b1*b1 - 4*a1*c1

        x21 = (-b1-math.sqrt(delta2))/(2*a1)
        x22 = (-b1+math.sqrt(delta2))/(2*a1)

        y21 = (x21*(y2-y1) + x2*y2 - x1*y2 - x2*y2 + x2*y1)/(x2 - x1)
        y22 = (x22*(y2-y1) + x2*y2 - x1*y2 - x2*y2 + x2*y1)/(x2 - x1)


        if(math.sqrt(math.pow((x21-x1),2) + math.pow((y21-y1),2)) > math.sqrt(math.pow((x22-x1),2) + math.pow((y22-y1),2))): 
            x2final = x21
            y2final = y21
        else:
            x2final = x22
            y2final = y22

        #In equation above, x1final and y1final are coordinates of *1, same as *1, x2final and y2final are coordinates of *2


        #Getting normal equations of WP line for points *1 and *2 which will be give us coordinates of 1,2,3,4

        #Calculation to get 1,2 via *1

        
        b = (x1final/a) + y1final
        bb = (x2final/a) + y2final
        a = -1.0/a
        

        a1 = a*a + 1
        b1 = 2*a*b - 2*x1final - 2*a*y1final
        c1 = x1final*x1final + y1final*y1final + b*b - 2*b*y1final - (((1.0/3)*dist) * ((1.0/3)*dist))

        delta2 = b1*b1 - 4*a1*c1

        x11 = (-b1-math.sqrt(delta2))/(2*a1)
        x12 = (-b1+math.sqrt(delta2))/(2*a1)

        y11 = a*x11 + b
        y12 = a*x12 + b


        #Calculation to get 3,4 via *2      

        a1 = a*a + 1
        b1 = 2*a*bb - 2*x2final - 2*a*y2final
        c1 = x2final*x2final + y2final*y2final + bb*bb - 2*bb*y2final - (((1.0/3)*dist) * ((1.0/3)*dist))

        delta2 = b1*b1 - 4*a1*c1

        x21 = (-b1-math.sqrt(delta2))/(2*a1)
        x22 = (-b1+math.sqrt(delta2))/(2*a1)

        y21 = a*x21 + bb
        y22 = a*x22 + bb



    #Deciding which one is 1,2,3 or 4
    # If it is upper-left it's 1, and other one is 2; same as before; if it is upper-left its 3, and other one is 4  

    #WELL THIS SHIT AINT WORK..
    #Defining new rules..
    #We need to find where WP1 located based on WP2.
    #Finding which one is on top, if y coordianates are equal, then we need to find which one is at left..
    #We need to define a variable to check all conditions.. basedLocation = [a,b]
    #a = 0, y coordinates not equal;    b, WP1 location based on WP2,   b=0 => WP1 is on the top,   b=1 => WP1 is at the bottom
    #a = 1, y coordinates are equal;    b, WP1 location based on WP2,   b=0 => WP1 is at the left,  b=1 => WP1 is at the right


    if(WP1[1][1]==WP2[1][1]):
        #a = 1 condition
        if(WP1[1][0]<WP2[1][0]):
            #b = 0 condition
            basedLocation = [1,0]
        else:
            #b = 1 condition
            basedLocation = [1,1]
    else:
        #a = 0 condition
        if(WP1[1][1]<WP2[1][1]):
            #b = 0 condition
            basedLocation = [0,0]
        else:
            #b = 1 condition
            basedLocation = [0,1]


    if[basedLocation[0]==0]:
        #a = 0 condition
        if(basedLocation[1]==0):
            #[0,0] condition
            if(x11>x12):
                cornerList.append([1,[x11,y11]])
                cornerList.append([2,[x12,y12]])
            else:
                cornerList.append([1,[x12,y12]])
                cornerList.append([2,[x11,y11]])
            if(x21>x22):
                cornerList.append([3,[x22,y22]])
                cornerList.append([4,[x21,y21]])
            else:
                cornerList.append([3,[x21,y21]])
                cornerList.append([4,[x22,y22]])
        else:
            #[0,1] condition
            if(x11<x12):
                cornerList.append([1,[x11,y11]])
                cornerList.append([2,[x12,y12]])
            else:
                cornerList.append([1,[x12,y12]])
                cornerList.append([2,[x11,y11]])
            if(x21<x22):
                cornerList.append([3,[x22,y22]])
                cornerList.append([4,[x21,y21]])
            else:
                cornerList.append([3,[x21,y21]])
                cornerList.append([4,[x22,y22]])
    else:
        #a = 1 condition
        if(basedLocation[1]==0):
            #[1,0] condition
            if(y11>y12):
                cornerList.append([1,[x11,y11]])
                cornerList.append([2,[x12,y12]])
            else:
                cornerList.append([1,[x12,y12]])
                cornerList.append([2,[x11,y11]])
            if(y21>y22):
                cornerList.append([3,[x22,y22]])
                cornerList.append([4,[x21,y21]])
            else:
                cornerList.append([3,[x21,y21]])
                cornerList.append([4,[x22,y22]])
        else:
            #[1,1] condition
            if(y11<y12):
                cornerList.append([1,[x11,y11]])
                cornerList.append([2,[x12,y12]])
            else:
                cornerList.append([1,[x12,y12]])
                cornerList.append([2,[x11,y11]])
            if(y21<y22):
                cornerList.append([3,[x22,y22]])
                cornerList.append([4,[x21,y21]])
            else:
                cornerList.append([3,[x21,y21]])
                cornerList.append([4,[x22,y22]])


    #IMPORTANT!!!
    #So I must mention that this if-else statements above actually unneccessary. But its 7 in the morning and I am tired to check which one is 1 or 2..
    #This part will be deleted and faster statement will be defined.
    #This two if statements above can be merged but yet I am still tired..


    #NOW we will send these corners to a function which will be return a list of circles in the area.

    circleList = areaCircles(cornerList,circles)

    return circleList


def wayPointChecker(wpList,circles):
    #Checks if waypoint has any obstacles on it and finds a way around them.
    #In order to do that, it passes two WP arguments to next functions.

    finalWPList = []

    for i in xrange((len(wpList)-1)):
        midWPList = collisionCheck(wpList[i],wpList[i+1],circles)

        if(len(finalWPList)==0):
            finalWPList += [wpList[i][1]] + midWPList + [wpList[i+1][1]]
            
        else:
            finalWPList += midWPList + [wpList[i+1][1]]


    return finalWPList


def randomTestParams():
    #Creates random test params for WPs and circles.

    #SUCCEED ALL PRIMER TEST PARAMS! YAAAAAAAAYYYY!!

        #TEST PARAM FOR X1 != X2 and Y1 != Y2

            #wpList = [[1,[100,100]],[2,[200,200]]]
            #circles = [[1,[155,150],30]]

        #TEST PARAM FOR Y1 = Y2

            #wpList = [[1,[50,100]],[2,[250,100]]]
            #circles = [[1,[150,105],30]]

        #TEST PARAM FOR X1 = X2

            #wpList = [[1,[200,100]],[2,[200,400]]]
            #circles = [[1,[205,250],30]]

    #SECONDARY TEST PARAMS

        #TEST PARAM FOR TWO CIRCLE BEETWEN WAYPOINTS
    
            #wpList = [[1,[100,100]],[2,[400,450]]]
            #circles = [[1,[210,195],30],[2,[300,300],20]]

        #TEST PARAMS FOR 3 WP AND TWO CIRCLES
        #PASSED IT WITH CONDITION:
        #If distance between WP1 and WP2 is shorter than WP1 and WPc's, pass the circle.
        #It wasn't neccessary to define such law, but maybe handy in the future..
        #Well apparently it turns out such kind of law definition is neccessary.. So be it :) 
            #wpList = [[1,[100,100]],[2,[400,450]],[3,[200,425]]]
            #circles = [[1,[210,195],30],[2,[300,435],15]]



    #GENERATING A RANDOM LIST OF Waypoints and Circles
    #Rules for generating a list:
    #1) WP locations cannot be same
    #2) Circles cannot be collide => Which means, we will calculate every circle with each other to prevent interrupt.
    #ARE YOU IN MY LOVE => (It's extremely simple equation..) => for given P(x,y) and C(xc,yc,radius)
    #(x-xc)^2 + (y-yc)^2 <= radius^2 provides a verification.. 
    wpList = []
    circles = []


    while(True):
        if(len(circles)==5):
            break
        x = random.randint(120,600)
        y = random.randint(120,600)
        r = random.randint(20,45)
        test = True
        for j in circles:
            if(math.sqrt(pow((x - j[1][0]),2) + pow((y - j[1][1]),2)) <= j[2]*outerCircleMultiplier*2):
                test = False
        if(test):
            circles.append([(len(circles)+1),[x,y],r])


    while(True):
        if(len(wpList) == 6):
            break
        x = random.randint(120,600)
        y = random.randint(120,600)
        test1 = True
        test2 = True
        for j in wpList:
            if((x == j[1][0]) and (y ==j[1][1])):
                test1 = False
        for i in circles:
            if(math.sqrt(pow((x - i[1][0]),2) + pow((y - i[1][1]),2)) <= i[2]*outerCircleMultiplier*1.5):
                test2 = False

        if(test1 and test2):
            wpList.append([(len(wpList)+1),[x,y]])

    print wpList
    return wpList,circles

def tester():
    img = np.zeros((720,720,3),np.uint8)

    wpList,circles = randomTestParams()
    counter= 1
    
    for i in wpList:
        cv2.circle(img,(i[1][0],i[1][1]), 5,(255,0,0),-1)
        cv2.putText(img,str(counter),(int(i[1][0])+15,int(i[1][1]-1)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),1,cv2.LINE_AA)
        counter +=1
    
    for circle in circles:
        cv2.circle(img, (circle[1][0],circle[1][1]), circle[2], (0,0,255), -1 )
        cv2.circle(img, (circle[1][0],circle[1][1]), int(circle[2]*innerCircleMultiplier), (255,0,0),1)
        cv2.circle(img, (circle[1][0],circle[1][1]), int(circle[2]*outerCircleMultiplier), (0,255,0),1)

    finalWPList =  wayPointChecker(wpList,circles)
    counter = 1
    for wp in finalWPList:
        cv2.circle(img, (int(wp[0]),int(wp[1])),2,(255,255,255),-1)
        cv2.putText(img,str(counter),(int(wp[0])-15,int(wp[1]-1)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(0,0,255),1,cv2.LINE_AA)
        counter +=1

    #for corner in xrange(len(cornerList)):
    #    cv2.circle(img, (int(cornerList[corner][1][0]),int(cornerList[corner][1][1])),2,(255,255,255),-1)
    #    cv2.line(img, (int(cornerList[corner][1][0]),int(cornerList[corner][1][1])),
    #        (int(cornerList[(corner+1)%4][1][0]),int(cornerList[(corner+1)%4][1][1])), (0,0,255),3)

    cv2.imshow('test',img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


tester()
