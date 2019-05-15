# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pdb
import matplotlib.pyplot as plt 
from matplotlib import path
from PIL import Image


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
    
def get_average_depth(contour_points, depth_image):
    """Get average depth in a convex hull from depth image
    with cv2.fillConvexPoly
    """
    mask = np.zeros_like(depth_image)
    mask = cv2.fillConvexPoly(mask, contour_points,1)
    mask_image = mask * depth_image
    
    count = mask.sum()
    depth = mask_image.sum()
    average_depth = depth / count
    
    return average_depth
    
def get_average_depth_old(contour_points, depth_image):
    '''deprecated, too slow.
    Find the average depth of the given area of depth_image
    contour_points is the points of ONE contour
    contour_ponies should be a array like array([[x1,y1],[x2,y2]],dtype=int32)
    '''
    contour_points = contour_points.reshape(-1,2)
    points = np.zeros(contour_points.shape)
    points[:,1] = contour_points[:,0]
    points[:,0] = contour_points[:,1]
    
    contour_path = path.Path(points)
    
    width, height = depth_image.shape
    coordinate = [[x,y] for x in range(width) for y in range(height)]
    in_boolen = contour_path.contains_points(coordinate)
    mask = in_boolen.reshape(width, height)
    mask_image = mask * depth_image
    
    count = mask.sum()
    depth = mask_image.sum()
    average_depth = depth / count
    
    return average_depth

    
