# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:35:33 2019

@author: bdgecyt
"""

import sys
import argparse
from opencvui import openimage
from ReadImage import ocr_core
import matplotlib.pyplot as plt
import os

import cv2
print(cv2.__version__)

def extractImages(pathIn, pathOut, sec, videoname):
    count = sec
    num = 0
    vidcap = cv2.VideoCapture(pathIn)
    success, image = vidcap.read()
    success = True
    while success:
      vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 
      success,image = vidcap.read()
      
#      im= image[SKcrop[1]:SKcrop[3],SKcrop[0]:SKcrop[2],:]
#      a = ocr_core(im)
#      plt.imshow(im)
#      plt.show()
#      print(a)
      
      print ('Read a new frame: ', success)
      cv2.imwrite( pathOut + "\\" + videoname + "_frame%d.jpg" % num, image)     # save frame as JPEG file
      count = count + sec
      num += 1
      print(count)


if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--pathIn", help="path to video", default = "C:\\Users\\bdgecyt\\Desktop\\videos\\welltech_main_20181214_090000_100000_test_video.mp4")
    a.add_argument("--pathOut", help="path to images", default = "C:\\Users\\bdgecyt\\Desktop\\videos\\extractedimages")
    args = a.parse_args()
    print(args)
    
    head, tail = os.path.split(args.pathIn)
    print(tail[:-4])
    
    vidcap = cv2.VideoCapture(args.pathIn)
    success,image = vidcap.read()
#    SKcrop = openimage(imagename = None, image = image)
    extractImages(args.pathIn, args.pathOut, 1/7, tail[:-4])

    
    
    

