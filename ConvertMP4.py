# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 11:03:17 2019

@author: bdgecyt
"""

from pathlib import Path
from os import listdir
from os.path import isfile
from Sortfiles import parsefilename
import time 
from subprocess import call

PATH = Path("D:\\train")  
#source = str(PATH/"NVR_ch9_main_20190401192124_20190401200000.dav")
#destination = str("D:\\" + "only.mp4")
#print(source)
#print(destination)

#end_time = time.time()
#print("time taken:")
#print(start_time - end_time)

for i in listdir(PATH):
    mn, ch, dy, ti = parsefilename(i)
    if int(mn) > 201812:
        source = str(PATH/i)
        destination = "D:\\trainMP4\\" +  i[:-3] +".mp4"
        if isfile(destination) == False:
            try:
                print("converting " + source)
                start_time = time.time()
                call(['ffmpeg', '-y', '-i', source, "-vcodec", "libx264", "-crf", "24", destination])
                end_time = time()
                print("finishing converting, time taken:")
                print(start_time - end_time)
            except:
                print("cant convert files")

    

#try:
##    print(str(valid) + " is copied")
##    source= "E:\\Welltech_Video" + "\\" + mon +"\\" + cam + "\\" + str(valid)
##    destination = "D:\\train\\" + str(valid)
##    copyfile(source, destination)
##    destination = "D:\\train\\" + str(valid)[:-3]+"mp4"
##    print(destination)
#    call(['ffmpeg', '-y', '-i', source, "-vcodec", "libx264", "-crf", "24", destination])
#    end_time = time()
#    print("Finish Converting, time taken:")
#    print(start_time - end_time)
#    
#except:
#    print("cant convert files")