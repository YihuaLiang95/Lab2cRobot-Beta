# -*- coding: utf-8 -*-
import cv2
import numpy as np

def image_processing(img):
    # contrast limiting adaptive histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    for i in range(3):
        img[:,:,i] = clahe.apply(img[:,:,i])
    return img
