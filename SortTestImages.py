# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 14:20:05 2019

@author: bdgecyt
"""
import os 
from shutil import copyfile

for i in os.listdir("D:\\testJPG"):
    if i.endswith("jpg"):
        if int(i[-7:-4])%10 == 9:
            src = "D:\\testJPG\\" + i
            dst = "D:\\testJPG\\forlabels\\" + i
            print(dst)
            copyfile(src, dst)
#            print(int(i[-7:-4]))
        