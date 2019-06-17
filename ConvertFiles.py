# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 16:23:24 2019

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



#im = plt.imread(path+"\\image_label20190523-093653.jpg")
#print(im.shape)
#im= im[25:70,25:500,:]
#plt.imshow(im)
#plt.show()
#a = ocr_core(im)
#print(a)

SKcrop= {"a": [25,70,35,500], "b":[]}

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def getTimeCat(time):
    # --> Morning = 0400-1000
    mornStart = datetime.time(8, 0, 1)
    mornEnd = datetime.time(12, 0, 0)

    # --> Midday = 1000-1600
    midStart = datetime.time(12, 0, 1)
    midEnd = datetime.time(3, 0, 0)

    # --> Evening = 1600-2200
    eveStart = datetime.time(3, 0, 1)
    eveEnd = datetime.time(7, 0, 0)

    if time_in_range(mornStart, mornEnd, time):
      timecat = "morning" #morning
    elif time_in_range(midStart, midEnd, time):
      timecat = "afternoon" #midday
    elif time_in_range(eveStart, eveEnd, time):
      timecat = "evening" #evening
      
    return timecat

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="C:\\Users\\bdgecyt\\Desktop\\SengKang_Part_1", help="folder path")
    parser.add_argument("--sitename", type=str, default="SK", help="name of site")

    opt = parser.parse_args()
    path = opt.folder
    print(path)
    directories = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    print(directories)
    site = opt.sitename
    print(site)


    WorkersList = []
    for i in directories[:1]:
        for file in os.listdir(path+"\\"+i):
            if file.endswith(".jpg"):
                im = plt.imread(path +"\\"+ i +"\\" + file)
        #        print(im.shape)
                im= im[SKcrop[i][0]:SKcrop[i][1],SKcrop[i][2]:SKcrop[i][3],:]
                plt.imshow(im)
                plt.show()
                a = ocr_core(im)
                print(a)
                name = site + i + re.sub('[:/ ]', '', a)
                print(name)
                try:
                    tree = ET.parse(path+"\\"+ i +"\\"+file[:-4]+".xml")
                    root = tree.getroot()
                    boxes = root.findall('object')
                    print(len(boxes))
                    dt = parser.parse(a)
                    month = dt.month
                    year = dt.year
        #        print(dt)
        #        print(dt.time())
                    timecat =  getTimeCat(dt.time())
                    print(timecat)
                    print([name, year, month, timecat, len(boxes)])
                    WorkersList +=[[name,year, month, timecat, len(boxes)]]
                except:
                    print("file has no label")
            
    print(WorkersList)
    pd.DataFrame(WorkersList)


        