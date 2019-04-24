# -*- coding: utf-8 -*-

import numpy as np 
from PIL import Image
import os
import pdb
import time
import cv2


# configurations
DISTANCE_THRES = 1300
MIN_AREA = 1400
OPEN_KERNEL = (15,15)
SAVE_DIR = "./demo"

def remove_ground(colormap,depth_image):
    # TODO
    return

def mask_depth(colormap,depth_image,threshold=1000):
    """eliminate distant objects.
    """
    masked_colormap = colormap.copy()
    masked_colormap[depth_image > threshold] = 0
    return masked_colormap

def opening(colormap):
    """erode and dilate to eliminate small objects on the graph.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,OPEN_KERNEL)
    opening = cv2.morphologyEx(colormap,cv2.MORPH_OPEN,kernel)
    return opening

def binary_gray(colormap):
    ret,bi_img = cv2.threshold(colormap,127,255,cv2.THRESH_BINARY)
    bi_img = cv2.cvtColor(bi_img,cv2.COLOR_RGB2GRAY)
    return bi_img

def find_contour(colormap):
    """Find contours from a binary image.
    """
    contours, hierarchy = cv2.findContours(colormap,
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # convex hull
    hulls = []
    for i,contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area >= MIN_AREA:
            hulls.append(cv2.convexHull(contour))

    return hulls


# load data
depth_image_path = "depth_images.npy"
depth_samples = np.load(depth_image_path).item()
colormaps = depth_samples["colormap"]
depth_images = depth_samples["image"]

f_count = 0
for colormap,depth_img in zip(colormaps,depth_images):
    raw_img = cv2.cvtColor(colormap,cv2.COLOR_BGR2RGB)

    # save raw images
    raw_im = Image.fromarray(raw_img)
    raw_im.save(os.path.join(SAVE_DIR,"{}_raw.jpg".format(f_count)))

    # mask colormap with distance threshold
    img = mask_depth(raw_img,depth_img,DISTANCE_THRES)

    # opening
    img = opening(img)

    # binary
    img = binary_gray(img)

    # find contours on image
    hulls = find_contour(img)

    # save processed images
    im = Image.fromarray(img)
    im.save(os.path.join(SAVE_DIR, "{}_mask.jpg".format(f_count)))
    # im.show()

    # save drawn contours images
    cv2.drawContours(raw_img,hulls,-1,(255,0,0),3)
    hull_im = Image.fromarray(raw_img)
    hull_im.save(os.path.join(SAVE_DIR,"{}_hull.jpg".format(f_count)))

    time.sleep(1)
    im.close()
    # pdb.set_trace()
    f_count += 1






