# -*- coding: utf-8 -*-
"""Provide obstacle detection API to access.
"""

import os
import pdb
import numpy as np 

import cv2
from PIL import Image

from cfg.config import config
from utils import mask_depth,opening,binary,find_contour,crop_depth

class ObstacleDetector(object):
    def __init__(self):
        return

    def detect_contour(self,colormap,depth_image):
        """Given colormap (RGB) images and depth image, get contours.
        
        Args:
            colormap: input RGB colormap.
            depth_image: a depth image containing depth information.
        Returns:
            hulls: a list of hull containing objects.
        """

        # mask depth image with cropping
        depth_image = crop_depth(depth_image,config.crop_ground)

        # mask colormap with distance threshold
        img = mask_depth(colormap,depth_image,config.distance_thres)

        # opening
        img = opening(img,config.open_kernel)

        # binary and gray
        img = binary(img)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

        hulls = find_contour(img,config.min_area)
        
        return hulls

    def draw_contour(self,colormap,hulls):
        cv2.drawContours(colormap,hulls,-1,(255,0,0),3)

    def detect_and_draw_contours(self,colormap,depth_image):
        hulls = self.detect_contour(colormap,depth_image)
        self.draw_contour(colormap,hulls)
        return colormap

def main():
    od = ObstacleDetector()
    depth_samples = np.load("depth_images.npy").item()
    colormaps = depth_samples["colormap"]
    depth_images = depth_samples["image"]

    # get a sample
    colormap = colormaps[5]
    depth_image = depth_images[5]

    colormap = cv2.cvtColor(colormap,cv2.COLOR_BGR2RGB)
    image = od.detect_and_draw_contours(colormap,depth_image)
    im = Image.fromarray(image)
    im.save("demo/5_hull_crop.jpg")
    im.show()
    
    # pdb.set_trace()

if __name__ == '__main__':
    main()

