# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 10:39:19 2019

@author: bdgecyt
"""

from pathlib import Path
import os
from os import listdir
from os.path import isfile, join
import random
import numpy as np
import pandas as pd
from shutil import copyfile
from subprocess import call
import time 
import cv2
import os


#for i in listdir("D:\\trainJPG")[:]:
##    print(i)
#    src= "D:\\trainJPG\\"+i
#    print(src)
#    tick = False
#    
#    
##    print(src[-6])
#    if(src[-6] == "_"):
##        print(src[-7])
#        if(src[-7] == "."):
#            print("aaaaaaaaaaaaa")
#            dst= src[:-7]+src[-6:]
#            print(dst)
#            tick = True
##        
#    if(src[-6] != "_"):
#        if(src[-8] == "."):
#            print("bbbbbbbbbb")
#            dst= src[:-8]+src[-7:]
#            print(dst)
#            tick = True
#        
##    if([])
##    dst = "D:\\trainJPG\\"+i[:-4]+"mp4"
##    print(dst)
#    if tick == True:
#        os.rename(src, dst)

for i in os.listdir("D:\\testJPG")[:]:
#    print(i)
    if "NVR_ch2_main_20180616100000_20180616110000" in i:
        if len(i) == 48:
            src = "D:\\testJPG\\" + i
            dst = "D:\\testJPG\\" + i[:-5] + i[-5].rjust(3,"0") +i[-4:]
            print(src)
            print(dst)
            os.rename(src, dst)
        if len(i) == 49:
            src = "D:\\testJPG\\" + i
            dst = "D:\\testJPG\\" +i[:-6] + i[-6:-4].rjust(3,"0") +i[-4:]
            print(src)
            print(dst)
            os.rename(src, dst)
    
