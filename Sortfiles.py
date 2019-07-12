# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:37:20 2019

@author: bdgecyt
"""

from pathlib import Path
from os import listdir
from os.path import isfile, join
import random
import numpy as np
import pandas as pd
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


#hello = "E:\\Welltech_Video"
PATH = Path("E:\\Welltech_Video")
random.seed(1)

NoDays = 12
EachDay = 18



def randomdates(num, pathname):
    num = num
    dates = np.arange(1, 31).tolist()   
    count = 0
    filenames = []
    while count < num:
        randomint = random.randint(1,31)
        if randomint in dates:
            dates.remove(randomint)
            filename = pathname + "NVR_ch1_main_201902" + str(randomint).rjust(2, '0')
            count += 1
            filenames += [filename]
    return filenames
    
#randomdates(NoDays)
#filename = "NVR_ch1_main_20190201" + "081206_20190201090000"
#print(listdir("E:\\Welltech_Video"))
filelist= []
for i in listdir(PATH):
    print(PATH/i)
    
    if len(listdir(PATH/i)) == 1:
        for j in listdir(PATH/i):
            print(PATH/i/j)
            files = randomdates(NoDays, str(PATH/i/j))
#            print(files)
            

    if len(listdir(PATH/i)) == 2:
        for j in listdir(PATH/i):
            print(PATH/i/j)
            files = randomdates(NoDays/2, str(PATH/i/j))
#            print(files)
        
    if len(listdir(PATH/i)) == 3:
        for j in listdir(PATH/i):
            print(PATH/i/j)
            files = randomdates(NoDays/3, str(PATH/i/j))
#            print(files)

    filelist += files

frame = pd.DataFrame(filelist)
print(frame)





