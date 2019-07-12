# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 12:42:59 2019

@author: bdgecyt
"""

import cv2
import numpy as np
 
cropping = False
x_start, y_start, x_end, y_end = 0, 0, 0, 0
 
def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping
 
    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        if x_start != 0 and y_end != 0:
            x_start, y_start, x_end, y_end = 0, 0, 0, 0
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
 
    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
 
    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False  # cropping is finished
     
#        refPoint = [(x_start, y_start), (x_end, y_end)]
#
#        if len(refPoint) == 2: #when two points were found
#            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
#            cv2.imshow("Cropped", roi)

def openimage(imagename = "C:\\Users\\bdgecyt\\Desktop\\SengKang_Part_1\\a\\image_label20190523-093653.jpg", image = None):
    if image is not None:
        oriImage = image.copy()
        imagename = "image"
    else:
        print(imagename)
        image = cv2.imread(imagename)
        oriImage = image.copy()
        
    cv2.namedWindow(imagename)
    cv2.setMouseCallback(imagename, mouse_crop)
    
    while True:
     
        i = image.copy()
     
        if x_start == 0 and y_end == 0:
            cv2.imshow(imagename, image)
     
        else:
            cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
            cv2.imshow(imagename, i)
    
        k = cv2.waitKey(1)
        if k == 27:
            print(x_start, y_start, x_end, y_end)
            break    
    
    cv2.destroyAllWindows()
    return x_start, y_start, x_end, y_end
    
    
if __name__ == "__main__":
    cropped_coor = openimage()
    print(cropped_coor)
