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
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000


#hello = "E:\\Welltech_Video"
PATH = Path("E:\\Welltech_Video")
random.seed(1)

NoDays = 12
EachDay = 18

#def checkstats(path):
#    filenames = listdir(path)
#    pd.DataFrame(filenames)
#  
#    for i in filenames:
#         if len(listdir(PATH/i)) == 1:
#            print("into 1")
#            for j in listdir(PATH/i):
#                filelist += files
#                files = randomdates(NoDays, i, j, "E:\\Welltech_Video\\train")
#                print(files)
#                filelist += files
#    
#        if len(listdir(PATH/i)) == 2:
#            print("is 2 cameras folder")
#            for j in listdir(PATH/i):
#                files = randomdates(NoDays/2, i, j, "E:\\Welltech_Video\\train")
#                print(files)
#                filelist += files
#    
#        if len(listdir(PATH/i)) == 3:
#            print("into 3")
#            for j in listdir(PATH/i):
#                files = randomdates(NoDays/3,i,j, "E:\\Welltech_Video\\train")
#                print(files)
#                filelist += files
#
#
#def readfolder(path):
#    filenames = listdir(path)
#    for i in filenames:
#         if i[7] == "_":
#             if i[4:7] == pathnamej.lower() and i[-8:-2] == pathnamei:
#                 similarfiles += [i]

def randomdates(num, pathnamei, pathnamej, checkdir):
    count = 0
    filenames = []
    similarfiles = []
    newfiles = []
#    print(pathnamei)
#    print(pathnamej)
    
    if checkdir:
        filenames += [i[:21] if i[7] == "_" else i[:22] for i in listdir(checkdir)]
        for i in filenames:
#            print(i)
            if i[7] == "_":
                if i[4:7] == pathnamej.lower() and i[-8:-2] == pathnamei:
                    similarfiles += [i]
            
            if i[7] != "_":
                if i[4:8] == pathnamej.lower() and i[-8:-2] == pathnamei:
                    similarfiles += [i]
                    
    count = len(similarfiles)
    print("count of similar files:")
    print(count)
    print(similarfiles)
    
    while count < num:
        randomint = random.randint(1,31)
        filename = "NVR_"+ pathnamej.lower() +"_main_" + pathnamei[-6:] + str(randomint).rjust(2, '0')
#        print("generated")
#        print(filename)
        if filename not in filenames:
            count += 1
            filenames += [filename]
            similarfiles += [filename]
            newfiles += [filename]
            
    return similarfiles
    

#filelist= []
#for i in listdir(PATH):
#    print(PATH/i)
#    if len(listdir(PATH/i)) == 1:
#        print("into 1")
#        for j in listdir(PATH/i):
#            filelist += files
##                files = randomdates(NoDays, i, j, "E:\\Welltech_Video\\train")
#            print(files)
#            filelist += files
#
#    if len(listdir(PATH/i)) == 2:
#        print("is 2 cameras folder")
#        for j in listdir(PATH/i):
##                files = randomdates(NoDays/2, i, j, "E:\\Welltech_Video\\train")
#            print(files)
#            filelist += files
#
#    if len(listdir(PATH/i)) == 3:
#        print("into 3")
#        for j in listdir(PATH/i):
##                files = randomdates(NoDays/3,i,j, "E:\\Welltech_Video\\train")
#            print(files)
#            filelist += files
#
#frame = pd.DataFrame(filelist)
#frame.to_csv("list.csv")
#print(frame)
    

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




filenames = listdir("E:\\Welltech_Video")
frame = pd.DataFrame(filenames, columns = ["months"])
frame["Cameras"] = [listdir(PATH/i)for i in listdir(PATH)]
#Frame["days"] = [["e"]*int(j) for j in (NoDays/len(i) for i in Frame["Cameras"])]
frame["week"] = [[1,2,3,4] for i in range(len(frame))]
frame["timeofday"] = [["morning", "afternoon", "evening"] for i in range(len(frame))]


#Frame.noCameras.apply(pd.Series).stack().reset_index(level=1, drop=True).to_frame('hello')
expand = split_data_frame_list(frame, "Cameras")
expand = split_data_frame_list(expand, "week")
expand = split_data_frame_list(expand, "timeofday")

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(frame)
    print(expand)

#expand.groupby(["months", "Cameras"])['days'].count()   


PATH2 = Path("C:\\Users\\bdgecyt\\Desktop\\train")
listinfo =[]
for i in listdir(PATH2):
    mn, ch, dy, ti = parsefilename(i)
    listinfo += [[mn, dy, ch, ti, i]]

folderframe = pd.DataFrame(listinfo, columns=["month", "day", "channel", "time", "filename"])
folderframe["day"] = folderframe["day"].astype(int)
folderframe["time"] = folderframe["time"].astype(int)
print(folderframe)

def binweek(df, col):
    bins = [0, 8, 16, 24, 32]
    labels = [1,2,3,4]
    df["week"] = pd.cut(df[col], bins=bins, labels=labels)
    return df

def bintime(df, col):
    bins = [70000, 120000, 160000, 190000]
    labels = ["morning", "afternoon", "evening"]
    df["timeofday"] = pd.cut(df[col], bins=bins, labels=labels)
    return df
    
folderframe = binweek(folderframe, "day")
folderframe = bintime(folderframe, "time")
print(folderframe.head())


print(expand.head())

final = pd.merge(expand, folderframe, how='left', left_on=['months', 'Cameras', 'week', 'timeofday'], right_on = ['month', 'channel', 'week', 'timeofday'])


print(final)





















