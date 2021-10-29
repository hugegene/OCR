# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 13:36:26 2019

@author: SaRRU
"""

import os
from os import listdir
from os.path import isfile, join

path = "E:\\Welltech_Video_mp4\\201909\\CH9\\"

for i in listdir(path):
    name = i.split("_")
#    print(name)
    rename = "NVR_ch9_main_" + name[1]
    print(rename)
    os.rename(path+i, path+rename)
    