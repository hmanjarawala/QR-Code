# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 10:29:21 2020

@author: Himanshu.Manjarawala
"""

import tempfile
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
import cv2 as cv

def scan_image(imagefilename):
    image = cv.imread(imagefilename)
    
    qrcodes = []
    decoded = decode(image)
    for d in decoded:
        qrcodes.append(d.data.decode("utf-8"))
    return (len(qrcodes)>0), qrcodes

def scan_pdf(pdffilename):
    poppler_path = r"C:\Users\himanshu.manjarawala\OneDrive - EY\Documents\TTT\poppler-20.12.1\bin"
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(pdffilename, dpi=800, output_folder=path, poppler_path=poppler_path)
        qrcodes = []
        for image in images_from_path:
            decoded = decode(image)
            for d in decoded:
                qrcodes.append(d.data.decode("utf-8"))
    return (len(qrcodes)>0), qrcodes