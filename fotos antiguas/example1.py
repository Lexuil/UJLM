#Example script

import time
from Rubikbot import Rubikbot
import numpy as np

import sys


import cv2
from cv2 import *



def dcontour2 (mask):

    kernel = np.ones((10,10),np.uint8)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def dcontours (mask):

    ret,thresh = cv2.threshold(mask,127,255,0)
    cv2.imshow("Show1" ,thresh)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    return contours


def print_color (cnts, c='n'):
    coord=[]  
    if c =='w': col=(0,0,0)
    elif c== 'b': col=(255,0,0)
    elif c== 'g': col=(0,255,0)
    elif c== 'r': col=(0,0,255)
    elif c== 'o': col=(32, 164,255)
    elif c== 'y': col=(0, 255, 255)
    else : col=(255,255,255)
    #print c
    for cnt in cnts:
        x,y,w,h = cv2.boundingRect(cnt)
        #print h, w
        if (45<h <70 and 45<w<70):
            coord.append ([x,y,c])
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

sensitivity = 95
blanco_bajos = np.array([0,0,255-sensitivity])
blanco_altos = np.array([255,sensitivity,255])

#blanco_bajos = np.array([40,5,130], np.uint8)
#blanco_altos = np.array([80, 30, 255], np.uint8)

def getKey(item):
    return item[1]

def colorrec(file,file1):

    mask_green= cv2.inRange(hsv_img, verde_bajos, verde_altos) 
    mask_blue = cv2.inRange(hsv_img, azul_bajos, azul_altos)  
    mask_red = cv2.inRange(hsv_img, rojo_bajos, rojo_altos)  
    mask_orange = cv2.inRange(hsv_img, naranja_bajos, naranja_altos)  
    mask_yellow = cv2.inRange(hsv_img, amarillo_bajos, amarillo_altos)  
    mask_white = cv2.inRange(hsv_img, blanco_bajos, blanco_altos)  


    colorsa=[]

    contours =dcontours(mask_green)
    colorsa+=(print_color(contours,'g'))

    contours =dcontours(mask_blue)
    colorsa+=(print_color(contours,'b'))

    contours =dcontours(mask_red)
    colorsa+=(print_color(contours,'r'))

    contours =dcontours(mask_orange)
    colorsa+=(print_color(contours,'o'))

    contours =dcontours(mask_yellow)
    colorsa+=(print_color(contours,'y'))

    contours =dcontours(mask_white)
    colorsa+=(print_color(contours,'w'))

    print "colours: ", colorsa


    colorsa.sort(key=getKey)





    print colorsa[:]
    l1=sorted(colorsa[0:3])
    l2=sorted(colorsa[3:6])
    l3=sorted(colorsa[6:])
    print "linea 1", l1
    print "linea2", l2
    print "linea3",l3, len(colorsa)

    result=[]
    for i in l1:
        result.append(i[2])

    for i in l2:
        result.append(i[2])

    for i in l3:
        result.append(i[2])
    print result

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
        