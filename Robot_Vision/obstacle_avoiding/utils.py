# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pdb

def mask_depth(colormap,depth_image,threshold=1000):
    """eliminate distant objects.
    """
    masked_colormap = colormap.copy()
    masked_colormap[depth_image > threshold] = 0
    return masked_colormap

def opening(colormap,open_kernel):
    """erode and dilate to eliminate small objects on the graph.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,open_kernel)
    opening = cv2.morphologyEx(colormap,cv2.MORPH_OPEN,kernel)
    return opening

def binary(colormap):
    ret,bi_img = cv2.threshold(colormap,1,255,cv2.THRESH_BINARY)
    return bi_img

def find_contour(colormap,min_area):
    """Find contours from a binary image.
    """
    contours, hierarchy = cv2.findContours(colormap,
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # convex hull
    hulls = []
    for i,contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area >= min_area:
            hulls.append(cv2.convexHull(contour))

    return hulls

def crop_depth(depth_image,crop_ground=0.25):
    """Crop the lower crop_ground part of the input image.
    """
    m,n = depth_image.shape[0],depth_image.shape[1]
    depth_image[int((1 - crop_ground)*m):,:] = 50000
    return depth_image