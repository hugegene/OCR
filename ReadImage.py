# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 16:21:50 2019

@author: bdgecyt
"""

try:  
    from PIL import Image
except ImportError:  
    import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_core(file):  
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(file)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

if __name__ == "__main__":
    file =  Image.open('C:\\Users\\bdgecyt\\Desktop\\aa.jpg')
    print(ocr_core(file))  
