# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 12:31:31 2019

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
from Sortfiles import setupdesired, readexisting, randomdates, checkforvalidfiles, checkotherfolder

random.seed(time.time())
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000

def split_test_video(video, secs, extractfps, start_frame, i):
    
    vidcap2 = cv2.VideoCapture(video)
#    total_frame = vidcap2.get(cv2.CAP_PROP_FRAME_COUNT)
#    print(total_frame)
#    fps = vidcap2.get(cv2.CAP_PROP_FPS)
#    print(fps)
#    least_startframe = int(total_frame - fps*secs)
#    start_frame = random.randint(0, least_startframe)
#    end_frame = start_frame+ int(fps*secs)
    incre= 1/extractfps
    print(incre)
    
    vidcap2.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    success, image = vidcap2.read()
    starttime = vidcap2.get(cv2.CAP_PROP_POS_MSEC)
    currenttime = vidcap2.get(cv2.CAP_PROP_POS_MSEC)
    duration = int(str(secs)+"000")
    print(duration)
    index = 0
    while success:
        print(currenttime - starttime)
        if currenttime - starttime > duration:
            break
        vidcap2.set(cv2.CAP_PROP_POS_MSEC, currenttime)    # added this line 
        success,image = vidcap2.read()
        filename = str("D:\\testJPG\\") + i[:-4] + "_" + str(index).rjust(3, "0") +".jpg"
        print(filename)
        cv2.imwrite(filename, image)      # save frame as JPEG file
        currenttime += incre*1000 
        index += 1


if __name__=="__main__":
      
    desired = setupdesired()
    desired["images"] = "have"
    desiredsummary = pd.DataFrame(desired.groupby(["month"])["images"].count())
#    print(desiredsummary)
    
    existing = readexisting(folderpath= "D:\\testJPG")
    existing["shortname"]= [i[:-6] if i[-6]== "_" else i[:-7] if i[-7] == "_" else i[:-8] for i in existing["filename"]]
#    print(existing)

    existingsummary = pd.DataFrame(existing.groupby(["month"])["filename"].count())
    print(existingsummary)
 
    finalsummary = pd.merge(desiredsummary, existingsummary, how='left', left_on=['month'], right_on = ['month'])
    print(finalsummary)
    
    testfolder = readexisting(folderpath= "D:\\testMP4")
    testfolder["shortname"]= [i[:-4] for i in testfolder["filename"]]
#    print(testfolder.head())
    
#    MP4folder = readexisting(folderpath= "D:\\testMP4")
#    MP4folder["shortname"] = [i[:-4] for i in MP4folder["filename"]]
#    print(MP4folder)
#    
#    missingfromMP4 = pd.merge(MP4folder, existing, how='left', left_on=['shortname'], right_on = ['shortname'])
#    print(missingfromMP4.head())
#    
#    missing = missingfromMP4.loc[pd.isna(missingfromMP4["timeofday_y"]).values, :]["filename_x"].unique()
#    print(missing[0])
    
    
    missingsummary =  pd.merge(testfolder, existing, how='left', left_on=['shortname'], right_on = ['shortname'])
#    print(missingsummary.head())
    missingindex = missingsummary.loc[pd.isna(missingsummary["timeofday_y"]).values, :]["filename_x"].unique()
    print(missingindex)

    for i in missingindex[:]:
#        converted = False
#        for j in os.listdir("D:\\testmp4"):
##            print(j)
#            if i[:-4] in j:
#                print("matched")
#                converted  = True
#        print("   Converted: " + str(converted))
#        source = "D:\\test\\" + i
        destination = "D:\\testMP4\\" + i
        
#        if converted == False:
#            print("   converting " + source)
#            start_time = time.time()
#            call(['ffmpeg', '-y', '-i', source, "-vcodec", "libx264", "-crf", "24", destination])
#            end_time = time.time()
#            print("   finishing converting, time taken:")
#            print(end_time - start_time)
        print("D:\\testMP4\\" +i)
        cap = cv2.VideoCapture(destination)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        def onChange(trackbarValue):
            cap.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)
            err,img = cap.read()
        #    height , width , layers =  img.shape
        #    new_h= int(height/4)
        #    new_w= int(width/4)
        #    resize = cv2.resize(img, (new_w, new_h)) 
            cv2.imshow("mywindow", img)
            pass
        
        cv2.namedWindow('mywindow', cv2.WINDOW_NORMAL)
        cv2.createTrackbar( 'start', 'mywindow', 0, length, onChange )
        #cv2.createTrackbar( 'end'  , 'mywindow', 100, length, onChange )
        
        onChange(0)
        k= cv2.waitKey()
        if k == 27:
            start = cv2.getTrackbarPos('start','mywindow')
            cv2.destroyAllWindows()
        print(start)
        
        split_test_video(destination, 60, 7, start, i)

        
#        mon = i
#        print(mon)
#        cam = desired["channel"][desired['month'] == mon].unique()
#        cam = cam[random.randint(0, len(cam)-1)]
#        wek = desired["week"][desired['month'] == mon].unique()
#        wek = wek[random.randint(0, len(wek)-1)]
#        tim = desired["timeofday"][desired['month'] == mon].unique()
#        tim = tim[random.randint(0, len(tim)-1)]
#
#        
#        count = 0
#        tries = 0
#        ok = False
#        while count < 1:
#            if tries == 6000:
#                print("tried too many times")
#                break  
#
#            generatedname = randomdates(mon, cam, wek, tim)
#            valid = checkforvalidfiles(generatedname[:-2], 100000000)
#            if valid:
#                ok = checkotherfolder("D:\\trainJPG", valid)
#            tries +=1
#            if ok == True:
#                try:
#                    print("   " + str(valid) + " is valid and copied")
##                    source= "E:\\Welltech_Video" + "\\" + mon +"\\" + cam + "\\" + str(valid)
##                    destination = "D:\\test\\" + str(valid)
##                    copyfile(source, destination)
##                    print("   completed copying files")
##                     
##                    print("   converting dav file" )
##                    source2 = destination
##                    destination2 = "D:\\trainMP4\\" +  valid[:-3] +"mp4"
##                    start_time = time.time()
##                    call(['ffmpeg', '-y', '-i', source2, "-vcodec", "libx264", "-crf", "24", destination2])
##                    end_time = time.time()
##                    print("   finishing converting, time taken:")
##                    print(end_time - start_time)
#                    count += 1
#
#                except Exception as e: 
#                    print(e)
##                    print("   deleteting copied files")
##                    if os.path.exists(destination):
##                        os.remove(destination)
##                    if os.path.exists(destination2):
##                        os.remove(destination2)
#
#
#            MP4folder = readexisting(folderpath= "D:\\testMP4")  
#            missingfile = MP4folder["filename"][(MP4folder["month"] == mon) & (MP4folder["channel"] == cam) & (MP4folder["week"] == wek) & (MP4folder["timeofday"] == tim)]             
#            
#
#        if len(missingfile) > 0:
#            print("   number of matched MP4 is "  + str(len(missingfile)))
#            video = str("D:\\trainMP4\\" + missingfile.values[0])
#            print("   splitting" + video)
#            split_video(video, 12, missingfile.values[0])

#    existingsummary = pd.DataFrame(existing.groupby(["month", "channel", "week", "timeofday"])["filename"].count())
#    print(existingsummary)
#  
#    finalsummary = pd.merge(desiredsummary, existingsummary, how='left', left_on=['month', 'channel', 'week', 'timeofday'], right_on = ['month', 'channel', 'week', 'timeofday'])
#    print(finalsummary)