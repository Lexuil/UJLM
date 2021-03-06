#Example script

import time
from Rubikbot import Rubikbot
import numpy as np

import sys


import cv2
from cv2 import *




def dcontours (mask):
    kernel = np.ones((10,10),np.uint8)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def print_color (cnts, col=(255,0,0)):
    coord=[]  
    for cnt in cnts:
        x,y,w,h = cv2.boundingRect(cnt)
        if (h >40 and w >40):
            coord.append ((x,y))
            cv2.rectangle(im,(x,y),(x+w,y+h),col,2)
    return coord

def org(lin,cub,ma,mi):
    l = len(lin)

    if(l > 0):

        for x in range(0,l):

            if (mi-20) < lin[x][0] < (mi+20):
                if l > 1:
                    cub += [lin[x][2]]
                if l == 1:
                    cub += [lin[x][2]]
                    cub += ['w']
                    cub += ['w']
                
            elif (ma-20) < lin[x][0] < (ma+20):
                if l == 3 and x == 2:
                    cub += [lin[x][2]]

                if l == 2 and len(cub)%3 == 1:
                    cub += ['w']
                    cub += [lin[x][2]]

                if l == 2 and len(cub)%3 == 2:
                    cub += [lin[x][2]]

                if l == 1:
                    cub += ['w']
                    cub += ['w']
                    cub += [lin[x][2]]
            else:
                if l == 3 and x == 1:
                    cub += [lin[x][2]]
                if l == 2 and x == 1:
                    cub += [lin[x][2]]
                    cub += ['w']
                if l == 2 and x == 0:
                    cub += ['w']
                    cub += [lin[x][2]]
                if l == 1:
                    cub += ['w']
                    cub += [lin[x][2]]
                    cub += ['w']
    else:
        cub += ['w']
        cub += ['w']
        cub += ['w']

# HSV image
#Verdes:
verde_bajos = np.array([60,60,100],np.uint8)
verde_altos = np.array([80, 255, 255],np.uint8)

#Azules:
azul_bajos = np.array([85,50,100], np.uint8)
azul_altos = np.array([115, 255, 255], np.uint8)


# rojo
rojo_bajos = np.array([1,50,90], np.uint8)
rojo_altos = np.array([18, 250, 175], np.uint8)

# Naranja
naranja_bajos = np.array([5,87,182], np.uint8)
naranja_altos = np.array([15, 255, 255], np.uint8)


# amarillo
amarillo_bajos = np.array([30,67,100], np.uint8)
amarillo_altos = np.array([50, 255, 255], np.uint8)

# blanco

blanco_bajos = np.array([1,5,130], np.uint8)
blanco_altos = np.array([2, 30, 255], np.uint8)

#blanco_bajos = np.array([40,5,130], np.uint8)
#blanco_altos = np.array([80, 30, 255], np.uint8)

def colorrec(file,file1):

    mask_green= cv2.inRange(hsv_img, verde_bajos, verde_altos) 
    mask_blue = cv2.inRange(hsv_img, azul_bajos, azul_altos)  
    mask_red = cv2.inRange(hsv_img, rojo_bajos, rojo_altos)  
    mask_orange = cv2.inRange(hsv_img, naranja_bajos, naranja_altos)  
    mask_yellow = cv2.inRange(hsv_img, amarillo_bajos, amarillo_altos)  
    mask_white = cv2.inRange(hsv_img, blanco_bajos, blanco_altos)  


    contours =dcontours(mask_white)

    ww = print_color(contours,(0,0,0))
    print "blanco",  ww

    contours =dcontours(mask_green)

    gg = print_color(contours,(0,255,0))
    print "Verdes", gg

    contours =dcontours(mask_blue)

    bb = print_color(contours,(255,0,0))
    print "azules", bb

    contours =dcontours(mask_red)

    rr = print_color(contours,(0,0,255))
    print "rojo", rr

    contours =dcontours(mask_orange)

    oo = print_color(contours,(32, 164,255))
    print "naranja", oo

    contours =dcontours(mask_yellow)

    yy = print_color(contours,(0,255,255))
    print "amarillo", yy

    for x in range(0,len(ww)):
        ww[x] = (ww[x][0],ww[x][1],'w')

    for x in range(0,len(gg)):
        gg[x] = (gg[x][0],gg[x][1],'g')

    for x in range(0,len(bb)):
        bb[x] = (bb[x][0],bb[x][1],'b')

    for x in range(0,len(rr)):
        rr[x] = (rr[x][0],rr[x][1],'r')

    for x in range(0,len(oo)):
        oo[x] = (oo[x][0],oo[x][1],'o')

    for x in range(0,len(yy)):
        yy[x] = (yy[x][0],yy[x][1],'y')

    face = []

    face += ww
    face += gg
    face += bb
    face += rr
    face += oo
    face += yy

    face.sort(key=lambda face: face[1])

    linea1 = []
    linea2 = []
    linea3 = []

    print "\nface: " , face ,"\n"

    nux = []
    nuy = []

    for x in range(0,len(face)):
        nux += [face[x][0]]

    for x in range(0,len(face)):
        nuy += [face[x][1]]

    nux.sort()
    nuy.sort()

    print nux
    print nuy,"\n"

    mmix = nux[0]
    mmax = nux[len(nux)-1]

    mmiy = nuy[0]
    mmay = nuy[len(nuy)-1]

    print mmax
    print mmix
    print mmay
    print mmiy,"\n"

    for x in range(0,len(face)):
        if ((face[0][1]-20) < face[x][1] < (face[0][1]+20) and mmiy-20 < face[x][1] < mmiy+20):
            linea1 += [face[x]]

    l1 = len(linea1)

    for x in range(l1,len(face)):
        if ((face[l1][1]-20) < face[x][1] < (face[l1][1]+20) and mmiy+20 < face[x][1] < mmay-20):
            linea2 += [face[x]]

    l2 = len(linea2) + l1

    for x in range(l2,len(face)):
        if ((face[l2][1]-20) < face[x][1] < (face[l2][1]+20) and mmay-20 < face[x][1] < mmay+20):
            linea3 += [face[x]]

    linea1.sort()
    linea2.sort()
    linea3.sort()

    print linea1
    print linea2
    print linea3,"\n"

    cube = []

    org(linea1,cube,mmax,mmix)
    org(linea2,cube,mmax,mmix)
    org(linea3,cube,mmax,mmix)

    print cube

    cv2.imshow("Show",im)
    cv2.imwrite(file1, im)
    cv2.waitKey()
    cv2.destroyAllWindows()



rubikbot = Rubikbot("/dev/ttyUSB1")
nfile = ["R1.jpg","R2.jpg","R3.jpg","R4.jpg","R5.jpg","R6.jpg"]
nfile1 = ["eR1.jpg","eR2.jpg","eR3.jpg","eR4.jpg","eR5.jpg","eR6.jpg"]

rubikbot.begin()

#calibra derecha del brazo 1 a 29
#mover U'

while(1):
    us = raw_input("...")
    us1 = us.split()

    if (us1[0] == 'mover'):
        rubikbot.movearm(us1[1])

    if (us1[0] == 'calibra'):
        rubikbot.calibratearm(int(us1[4]), us1[1], int(us1[6]))

    if (us1[0] == "home"):
        rubikbot.home()

    if (us1[0] == "init"):
        rubikbot.initial()

    if (us1[0] == "camera" and us1[1] == "all"):
        rubikbot.cam_reset()
        time.sleep(2)
        rubikbot.takepicture()
        rubikbot.getsize()
        rubikbot.savepicture(nfile)
        im = cv2.imread(nfile)
        im = cv2.bilateralFilter(im,9,75,75)
        im = cv2.fastNlMeansDenoisingColored(im,None,10,10,7,21)
        hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        colorrec(nfile)

    if (us1[0] == "reset" and us1[1] == "camera"):
        rubikbot.cam_reset()
        time.sleep(2)

    if (us1[0] == "take" and us1[1] == "picture"):
        rubikbot.takepicture()

    if (us1[0] == "get" and us1[1] == "size"):
        rubikbot.getsize()

    if (us1[0] == "save" and us1[1] == "picture"):
        rubikbot.savepicture(nfile)
        im = cv2.imread(nfile)
        im = cv2.bilateralFilter(im,9,75,75)
        im = cv2.fastNlMeansDenoisingColored(im,None,10,10,7,21)
        hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    if (us1[0] == "procesar" and us1[1] == "imagen"):
        colorrec(nfile)

    if (us1[0] == "mueve"):
        rubikbot.cara(int(us1[1]))

    if (us1[0] == "ver" and us1[1] == "cubo"):
        for x in range(0,6):
            rubikbot.cam_reset()
            time.sleep(2)
            rubikbot.takepicture()
            rubikbot.savepicture(nfile[x])
            im = cv2.imread(nfile[x])
            im = cv2.bilateralFilter(im,9,75,75)
            im = cv2.fastNlMeansDenoisingColored(im,None,10,10,7,21)
            hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
            colorrec(nfile[x],nfile1[x])
            rubikbot.cara(x+2)
        