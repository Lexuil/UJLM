#Example script

import time
from JPEGCamera import JPEGCamera
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
        if (h >100 and w >100):
            coord.append ((x,y))
            cv2.rectangle(im,(x,y),(x+w,y+h),col,2)
    return coord





camera = JPEGCamera("/dev/ttyUSB1")
nfile = "T1.jpg"
nfile1 = "extractedT1.jpg"
camera.begin()
camera.reset()
time.sleep(3)
camera.takepicture()
camera.getsize()

#image=camera.get_image()
camera.savePicture(nfile)
#camera.show(nfile)

im = cv2.imread(nfile)
im = cv2.bilateralFilter(im,9,75,75)
im = cv2.fastNlMeansDenoisingColored(im,None,10,10,7,21)
hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)   # HSV image
#Verdes:
verde_bajos = np.array([60,60,100],np.uint8)
verde_altos = np.array([80, 255, 255],np.uint8)

#Azules:
azul_bajos = np.array([85,70,95], np.uint8)
azul_altos = np.array([115, 255, 255], np.uint8)


# rojo
rojo_bajos = np.array([1,60,90], np.uint8)
rojo_altos = np.array([18, 250, 175], np.uint8)

# Naranja
naranja_bajos = np.array([5,100,182], np.uint8)
naranja_altos = np.array([15, 255, 255], np.uint8)


# amarillo
amarillo_bajos = np.array([30,67,100], np.uint8)
amarillo_altos = np.array([50, 255, 255], np.uint8)

# blanco

blanco_bajos = np.array([1,5,130], np.uint8)
blanco_altos = np.array([2, 30, 255], np.uint8)

#blanco_bajos = np.array([40,5,130], np.uint8)
#blanco_altos = np.array([80, 30, 255], np.uint8)



mask_green= cv2.inRange(hsv_img, verde_bajos, verde_altos) 
mask_blue = cv2.inRange(hsv_img, azul_bajos, azul_altos)  
mask_red = cv2.inRange(hsv_img, rojo_bajos, rojo_altos)  
mask_orange = cv2.inRange(hsv_img, naranja_bajos, naranja_altos)  
mask_yellow = cv2.inRange(hsv_img, amarillo_bajos, amarillo_altos)  
mask_white = cv2.inRange(hsv_img, blanco_bajos, blanco_altos)  


contours =dcontours(mask_white)
print "blanco",  print_color(contours,(0,0,0))

contours =dcontours(mask_green)
print "Verdes", print_color(contours,(0,255,0))

contours =dcontours(mask_blue)
print "azules",  print_color(contours,(255,0,0))

contours =dcontours(mask_red)
print "rojo",  print_color(contours,(0,0,255))

contours =dcontours(mask_orange)
print "naranja",  print_color(contours,(32, 164,255))

contours =dcontours(mask_yellow)
print "amarillo",  print_color(contours,(0,255,255))




cv2.imshow("Show",im)
cv2.imwrite(nfile1, im)
cv2.waitKey()
cv2.destroyAllWindows()