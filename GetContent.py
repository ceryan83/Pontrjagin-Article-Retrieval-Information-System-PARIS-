# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:22:19 2020

@author: cerya
"""
from pdf2image import convert_from_path
import pytesseract
import tempfile

# Tell pytesseract the location of the Tesseract application
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def getContentFromPDF(filepath):
    content = ''
    
    with tempfile.TemporaryDirectory() as path:
        print('Converting PDF to image...')
        images = convert_from_path(filepath, dpi = 300, 
                                   output_folder = path, 
                                   paths_only = True)
        print('Converted PDF to image. Now extracting text...')
        for image in images:
            content += pytesseract.image_to_string(image, 
                                                   lang = 'eng+equ') + '\n'
        print('Extraction complete.')
        
    return content