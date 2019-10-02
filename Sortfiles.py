# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:37:20 2019

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

#random.seed(time.time())
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000


def randomdates(month, ch, week, timeofday):
    
    if week == 1:
        day = random.randint(1,7)
    else:
        day = random.randint((week-1)*8,week*8-1)

    if timeofday == "morning":
        time = random.randint(7,12)
    elif timeofday == "afternoon":
        time = random.randint(12,16)
    elif timeofday == "evening":
        time = random.randint(16,18)
        
    minutes = random.randint(1,60)
    seconds = random.randint(1,60)
  
    filename = "NVR_"+ ch.lower() +"_main_" + month + str(day).rjust(2, '0') + str(time).rjust(2, '0') + str(minutes).rjust(2, '0') + str(seconds).rjust(2, '0')
#    print(filename)
    return filename

  
def checkforvalidfiles(filename, filesize):
    validfile = None
    PATH = Path("E:\\Welltech_Video_mp4")  
    month, channel, day, time = parsefilename(filename)
#    print(listdir(PATH/month/channel))
    for i in listdir(PATH/month/channel):
        if filename in i:
            if os.stat(PATH/month/channel/i).st_size > filesize:
                validfile =  i
#                print("valid file")
    return validfile
    
    
def parsefilename(i):
    if i[7] == "_":
        channel = i[4:7].upper()
        month = i[13:19]
        day= i[19:21]
        time = i[21:27]
    
    if i[7] != "_":
        channel = i[4:8].upper() 
        month = i[14:20]
        day= i[20:22]
        time = i[22:28]
    
    return  month, channel, day, time
    
    
def split_data_frame_list(df, 
                       target_column,
                      output_type=float):
    ''' 
    Accepts a column with multiple types and splits list variables to several rows.

    df: dataframe to split
    target_column: the column containing the values to split
    output_type: type of all outputs
    returns: a dataframe with each entry for the target column separated, with each element moved into a new row. 
    The values in the other columns are duplicated across the newly divided rows.
    '''
    row_accumulator = []
    def split_list_to_rows(row):
        split_row = row[target_column]
        if isinstance(split_row, list):
          for s in split_row:
              new_row = row.to_dict()
              new_row[target_column] = s
              row_accumulator.append(new_row)
          if split_row == []:
              new_row = row.to_dict()
              new_row[target_column] = None
              row_accumulator.append(new_row)
        else:
          new_row = row.to_dict()
          new_row[target_column] = split_row
          row_accumulator.append(new_row)
    df.apply(split_list_to_rows, axis=1)
    new_df = pd.DataFrame(row_accumulator)
    return new_df


def setupdesired():
    PATH = Path("E:\\Welltech_Video_mp4")  
    filenames = listdir(PATH)
    frame = pd.DataFrame(filenames, columns = ["month"])
    frame["channel"] = [listdir(PATH/i) for i in listdir(PATH)]
    #Frame["days"] = [["e"]*int(j) for j in (NoDays/len(i) for i in Frame["Cameras"])]
    frame["week"] = [[1,2,3,4] for i in range(len(frame))]
    frame["timeofday"] = [["morning", "afternoon", "evening"] for i in range(len(frame))]
    
    
    #Frame.noCameras.apply(pd.Series).stack().reset_index(level=1, drop=True).to_frame('hello')
    expand = split_data_frame_list(frame, "channel")
    expand = split_data_frame_list(expand, "week")
    expand = split_data_frame_list(expand, "timeofday")
    
    expand = expand[expand["channel"]!="CH15"]
    
#    print(frame)
#    print(expand)
#    print(len(expand))
    return expand

def checkotherfolder(baseon, toclean):
    existing = readexisting(folderpath= baseon)
    existing["filename"]= [i[:-11] for i in existing["filename"]]
    for i in existing['filename']:
        if i in toclean:
            return False
    return True

def readexisting(folderpath= None, csv = None):
    listinfo =[]
    if folderpath:
        PATH2 = Path(folderpath)
        for i in listdir(PATH2):
            if i.endswith((".jpg", ".mp4", ".dav")):
                mn, ch, dy, ti = parsefilename(i)
                listinfo += [[mn, dy, ch, ti, i]]
    if csv:
        data = pd.read_csv(csv)
        for i in data.values:
            mn, ch, dy, ti = parsefilename(i[0])
            listinfo += [[mn, dy, ch, ti, i[0]]]

    folderframe = pd.DataFrame(listinfo, columns=["month", "day", "channel", "time", "filename"])
#    print(folderframe[:10])

    folderframe["day"] = folderframe["day"].astype(int)
    folderframe["time"] = folderframe["time"].astype(int)
#    print(folderframe)
    
    def binweek(df, col):
        bins = [0, 7, 15, 23, 31]
        labels = [1,2,3,4]
        df["week"] = pd.cut(df[col], bins=bins, labels=labels, right = True)
        return df
    
    def bintime(df, col):
        bins = [70000, 120000, 160000, 200000]
        labels = ["morning", "afternoon", "evening"]
        df["timeofday"] = pd.cut(df[col], bins=bins, labels=labels)
        return df
        
    folderframe = binweek(folderframe, "day")
    folderframe = bintime(folderframe, "time")
#    print(folderframe.head())
    return folderframe

def split_video(video, TOTAL_IMAGE, i):
    vidcap2 = cv2.VideoCapture(video)
    total_frame = int(vidcap2.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frame)
    fps = int(vidcap2.get(cv2.CAP_PROP_FPS))
#    print(fps)
    for index in range(0, TOTAL_IMAGE):
#        vidcap2 = cv2.VideoCapture(video)
        
        if index == 0:
          frame_no = fps * 2 - 1 # The frame in 2nd second
        else:
          frame_no = int((total_frame / TOTAL_IMAGE) * index)
          
#        print(frame_no)
        vidcap2.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        success, image = vidcap2.read()
        filename = str("D:\\trainJPG\\") + i[:-4] + "_" + str(index) +".jpg"
        print(filename)
        cv2.imwrite(filename, image) 
        
def checktrainagainsttest():

    trainfolder = readexisting(folderpath= "D:\\trainJPG")
    trainfolder["shortname"]= [i[:-6] if i[-6]== "_" else i[:-7] for i in trainfolder["filename"]]
#    print(trainfolder.head())
    trainfolder.groupby(["shortname"])["week"].count()
    
    testfolder = readexisting(folderpath= "D:\\testJPG")
    testfolder["filename"]= [i[:-6] if i[-6]== "_" else i[:-7] if i[-7] == "_" else i[:-8] for i in testfolder["filename"]]
#    print(testfolder[:20])
#    testfolder.groupby(["filename"])["week"].count()
    
    merge = trainfolder.merge(testfolder, how='inner', left_on=["shortname"], right_on=["filename"])
#    print(merge)
    
    for i in merge["filename_x"].unique():
        path = "D:\\trainJPG\\" + i
        print("removing " + path + " because its in test set")
#        print(path[:-4] + ".xml")
        os.remove(path)
        if(os.path.isfile(path[:-4] + ".xml")):
            print("removing " + path[:-4] + ".xml" + " because its in test set")
            os.remove(path[:-4] + ".xml")


def cleanfolder(baseon, toclean):
    existing = readexisting(folderpath= baseon)
#    print([len(i) for i in existing["filename"]])
    existing["filename"]= [i[:-11] for i in existing["filename"]]
    tocleanfolder = readexisting(folderpath= toclean)
#    print(tocleanfolder["filename"])

    for i in tocleanfolder["filename"]:
        delete = True
        for j in existing['filename']:
            if j in i:
#                print("Jpgs found, file should be kept")
                delete = False
        if delete == True:
            print("deleting " + toclean + i + " because there are no jpegs to this video files extracted")
            os.remove(toclean+i)

def checkforlonelyXML(cleanpath):
    for file in os.listdir(cleanpath):
        if file.endswith(".xml"):
#            print(cleanpath + file[:-4] + ".jpg")
            if os.path.isfile(cleanpath + file[:-4] + ".jpg") == False:
                print("deleting lone xml:" + cleanpath + file)
                os.remove(cleanpath + file)

if __name__=="__main__":

    checkforlonelyXML("D:\\trainJPG\\")
    checktrainagainsttest()
    cleanfolder("D:\\trainJPG", "D:\\trainMP4\\")
    cleanfolder("D:\\trainJPG", "D:\\train\\")

    #Set up CSV according to folders
#    desired = setupdesired()
#    desired["images"] = "have"
#    desired.to_csv("desiredworkers.csv", index= False)
#    desired.dtypes
    
    #Use exisiting CSV 
    desired = pd.read_csv("desiredworkers.csv")
    desired['month'] = desired['month'].astype(str)
#    print(desired)
    
    desiredsummary = pd.DataFrame(desired.groupby(["month", "channel", "week", "timeofday"])["images"].count())
#    print(desiredsummary)
    
    existing = readexisting(folderpath= "D:\\trainJPG")
#    print(existing.head())

    existingsummary = pd.DataFrame(existing.groupby(["month", "channel", "week", "timeofday"])["filename"].count())
#    print(existingsummary)
      
    finalsummary = pd.merge(desiredsummary, existingsummary, how='left', left_on=['month', 'channel', 'week', 'timeofday'], right_on = ['month', 'channel', 'week', 'timeofday'])
    print(finalsummary)
    finalsummary.to_csv("workersdatasetsummary.csv")
    
    continueanot = input("continue files update (y/n): ")
    if continueanot == "y":
        
        print("continue on..")
    #    
        missingindex = finalsummary.loc[pd.isna(finalsummary["filename"]), :].index
        print(len(missingindex))
        
        for i in missingindex[135:]:
            
            print("working on" + str(i))
            MP4folder = readexisting(folderpath= "D:\\trainMP4")
            missingfile = MP4folder["filename"][(MP4folder["month"] == i[0]) & (MP4folder["channel"] == i[1]) & (MP4folder["week"] == i[2]) & (MP4folder["timeofday"] == i[3])]
            
            if len(missingfile) == 0:
                print("   Number of matched MP4 files is 0, grabbing from source files")
                count = 0
                tries = 0
                
                mon = i[0]
                cam = i[1]
                wek = i[2]
                tim = i[3]
                
                while count < 1:
                    if tries == 8000:
                        print("tried too many times")
                        break  
                    generatedname = randomdates(mon, cam, wek, tim)
#                    print(generatedname[:-4])
                    valid = checkforvalidfiles(generatedname[:-4], 300000000)
    #                print(valid)
                    tries += 1
                    if valid:
                        ok = checkotherfolder("D:\\testJPG", valid)
                        if ok == True:
                            if valid.endswith(".mp4"):
                                print(valid + "is mp4")
                                try:
                                    source= "E:\\Welltech_Video_mp4" + "\\" + mon +"\\" + cam + "\\" + str(valid)
                                    destination = "D:\\trainMP4\\" + str(valid)
                                    copyfile(source, destination)
                                    count += 1
                                except:
                                    print("copied mp4 from F drive fails")
                                    
                            elif valid.endswith(".dav"):
                                print(valid + "is dav")
                                try:
                                    print("   " + str(valid) + " is valid and copied")
                                    source= "E:\\Welltech_Video_mp4" + "\\" + mon +"\\" + cam + "\\" + str(valid)
                                    destination = "D:\\train\\" + str(valid)
                                    copyfile(source, destination)
                                    print("   completed copying files")
                                    
                                    print("   converting dav file" )
                                    source2 = destination
                                    destination2 = "D:\\trainMP4\\" +  valid[:-3] +"mp4"
                                    start_time = time.time()
                                    call(['ffmpeg', '-y', '-i', source2, "-vcodec", "libx264", "-crf", "24", destination2])
                                    end_time = time.time()
                                    print("   finishing converting, time taken:")
                                    print(end_time - start_time)
                                
                                    count += 1
                                    
                                except Exception as e: 
                                    print(e)
                                    print("   deleting copied files")
                                    if os.path.exists(destination):
                                        os.remove(destination)
                                    if os.path.exists(destination2):
                                        os.remove(destination2)
                            
                            MP4folder = readexisting(folderpath= "D:\\trainMP4")  
                            missingfile = MP4folder["filename"][(MP4folder["month"] == i[0]) & (MP4folder["channel"] == i[1]) & (MP4folder["week"] == i[2]) & (MP4folder["timeofday"] == i[3])]             
           
            if len(missingfile) > 0:
                print("   number of matched MP4 is "  + str(len(missingfile)))
                video = str("D:\\trainMP4\\" + missingfile.values[0])
                print("   splitting" + video)
                split_video(video, 12, missingfile.values[0])
