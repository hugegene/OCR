# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 09:40:05 2019

@author: bdgecyt
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from ReadImage import ocr_core
import xml.etree.ElementTree as ET
from dateutil import parser
import datetime
import pandas as pd
import re
from opencvui import openimage
import argparse
from opencvui import openimage
import cv2
from pathlib import Path
from os import listdir
from Sortfiles import parsefilename
from Sortfiles import  readexisting
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000

PATH = Path("D:")

def split_video(video, TOTAL_IMAGE, i):
    vidcap2 = cv2.VideoCapture(video)
    total_frame = int(vidcap2.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frame)
    fps = int(vidcap2.get(cv2.CAP_PROP_FPS))
    print(fps)
    ms = 5000
    for index in range(0, TOTAL_IMAGE):
#        vidcap2 = cv2.VideoCapture(video)
        
        if index == 0:
          frame_no = fps * 2 - 1 # The frame in 2nd second
        else:
          frame_no = int((total_frame / TOTAL_IMAGE) * index)
          
        print(frame_no)
        vidcap2.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        success, image = vidcap2.read()
        filename = str(PATH/"trainJPG") +"\\" + i[:-3] + "_" + str(index) +".jpg"
        print(filename)
        cv2.imwrite(filename, image) 
        
if __name__=="__main__":
    desired = setupdesired()
    
JPGfolder= readexisting(folderpath= "D:\\trainJPG")
#print(JPGfolder)
JPGsummary = JPGfolder.groupby(["month", "channel", "week", "timeofday"])["filename"].count()
print(pd.DataFrame(JPGsummary).columns)
#
MP4folder = readexisting(folderpath= "D:\\trainMP4")
#print(MP4folder)
MP4summary = MP4folder.groupby(["month", "channel", "week", "timeofday"])["filename"].count()
#print(pd.DataFrame(MP4summary))
#
#final = pd.merge(MP4folder, JPGfolder, how='left', left_on=['month', 'channel', 'week', 'timeofday'], right_on = ['month', 'channel', 'week', 'timeofday'])
#print(final)
#
finalsummary = pd.merge(pd.DataFrame(MP4summary), pd.DataFrame(JPGsummary), how='left', left_on=['month', 'channel', 'week', 'timeofday'], right_on = ['month', 'channel', 'week', 'timeofday'])
print(finalsummary)
##
##print(final.groupby(["month", "channel", "week", "timeofday"])["filename_y"].count())
#
#missingindex = finalsummary.loc[pd.isna(finalsummary["filename_y"]), :].index
#print(missingindex)
#
#for i in missingindex[:]:
#    missingfile = MP4folder["filename"][(MP4folder["month"] == i[0]) & (MP4folder["channel"] == i[1]) & (MP4folder["week"] == i[2]) & (MP4folder["timeofday"] == i[3])]
#    print(missingfile.values[0])
#    video = str(PATH/"trainMP4"/missingfile.values[0])
#    print(video)
#    split_video(video, 12, missingfile.values[0])
