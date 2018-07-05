#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import win_unicode_console
win_unicode_console.enable()

import glob, os
from sklearn.preprocessing import LabelEncoder
import imutils
from imutils import paths
from scipy import io
import numpy as np
import imutils
import cv2
import sys
import time
import datetime

saveLocation = "pics"
folderChar = "\\"
monitor_winSize = (1024, 768)
cam_resolution = (1024, 768)
rotated = True
angle = 90

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_resolution[0])
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_resolution[1])

picCount = 0
classCount = 0
summaryCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
classObject = "a"
msg = ""

def putText(image, text, x, y, color=(255,255,255), thickness=1, size=1.2):
    if x is not None and y is not None:
        cv2.putText( image, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)
    return image


	
while(camera.isOpened()):
    if not os.path.exists(saveLocation + folderChar + classObject):
        os.makedirs(saveLocation + folderChar + classObject)
	
    (grabbed, img) = camera.read()   

    r = monitor_winSize[1] / img.shape[1]
    dim = (monitor_winSize[0], int(img.shape[0] * r))
    img2 = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    putText(img2, "class:" + classObject + "(" + str(summaryCount[ord(classObject)-96]) + ")" , 10, 40, color=(0,0,255), thickness=2, size=1.5)
    putText(img2, msg, 10, 75, color=(0,255,0), thickness=2, size=1)
    cv2.imshow("Frame", img2)
    key = cv2.waitKey(1)
	
    if(key>=1 and key<=26):
        classCount = 0
        classObject = chr(key+96)
        		
    elif(key==113):  #q to exit
        break
		
    elif(key==32):  #SPACE key
        classCount += 1
        picCount += 1
        summaryCount[ord(classObject)-96] += 1
		
        filename = classObject + "_" + str(summaryCount[ord(classObject)-96]) + "_" + str(int(time.time())) + ".jpg"
        if(rotated == True):
            img = imutils.rotate_bound(img, angle)
			
        cv2.imwrite(saveLocation + folderChar + classObject + folderChar + filename, img)
        msg = "#" + str(summaryCount[ord(classObject)-96]) + " saved to " + filename
