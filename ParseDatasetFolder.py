# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 11:03:17 2019

@author: bdgecyt
"""

from pathlib import Path
from os import listdir
from os.path import isfile, join
import random
import numpy as np
import pandas as pd
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]




def parsefilename(i):
    if i[7] == "_":
        channel = i[4:7] 
        month = i[13:19]
        day= i[19:21]
        time = i[21:27]
        
    if i[7] != "_":
        channel = i[4:8] 
        month = i[14:20]
        day= i[20:22]
        time = i[22:28]
        
    return channel, month, day, time

#hello = "E:\\Welltech_Video"
PATH = Path("C:\\Users\\bdgecyt\\Desktop\\train")
random.seed(1)

NoDays = 12
EachDay = 18


listinfo =[]
for i in listdir(PATH):
    ch, mn, dy, ti = parsefilename(i)
    listinfo += [[mn, dy, ch, ti]]
    
frame = pd.DataFrame(listinfo, columns=["month", "day", "channel", "time"])
#frame["month"] =  pd.to_datetime(frame["date"])
#frame.index = frame["date"]
#frame = frame.drop(["date"], axis =1)
print(frame)

#frame.groupby(by=[frame.index.month, frame.index.year])
#
#frame.groupby(pd.Grouper(freq='M'))

frame.resample('M').count()

a = frame.groupby(["month", "channel"])['day'].count()
a.index
a["required"] = 4
a.index[3]