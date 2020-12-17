# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 17:55:00 2020

@author: Himanshu.Manjarawala
"""

import qrcode


def generate_qrcode(qrcodestring, qrcodeimage):
    try:
        
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=10,
                           border=4)
        qr.add_data(qrcodestring)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qrcodeimage)
        return qrcodeimage
    except Exception as e:
        print(e)