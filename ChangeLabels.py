# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 10:06:58 2019

@author: bdgecyt
"""

import json
import os
import xml.etree.ElementTree

for i in os.listdir("D:\\trainJPG\\"):
    if i.endswith(".xml"):
        print(i)
        tree = xml.etree.ElementTree.parse("D:\\trainJPG\\"+ i)
        print("read xml file")
        root = tree.getroot()
#        for obj in root.findall("object"):
#            name =  obj.find("name").text
        for j in root.iter('name'):
#            print(j.text.lower())
            j.text = j.text.lower()
        
#        print("D:\\"+ i)
        tree.write("D:\\trainJPG\\" + i)
#            print(name)
      
  