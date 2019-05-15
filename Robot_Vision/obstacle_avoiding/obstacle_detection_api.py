# -*- coding: utf-8 -*-
"""Provide obstacle detection API to access.
"""

import os
import pdb
import numpy as np
import sys

try:
    import cv2
except:
    ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
    if ros_path in sys.path:
        sys.path.remove(ros_path)
    import cv2
    # sys.path.append(ros_path)

from PIL import Image

from cfg.config import config
from utils import mask_depth,opening,binary,find_contour,crop_depth,get_average_depth

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
        
        # compute average depth
        depth_list = self.compute_depth(hulls, depth_image)
        #pdb.set_trace()
        self.draw_depth_txt(colormap,hulls,depth_list)
        return colormap
        
    def draw_depth_txt(self,frame,hulls,depth_list):
        for i,hull in enumerate(hulls):
            tx,ty = hull[0].flatten()
            avg_depth = str(round(0.001 * depth_list[i] ,2)) + "m"
            cv2.putText(frame, avg_depth, (tx,ty), cv2.FONT_HERSHEY_SIMPLEX,
                1,(255,255,0),2)
    
    def compute_depth(self, hulls,depth_image):
        depth_list = []
        for contour_points in hulls:
            avg_depth = get_average_depth(contour_points, depth_image)
            depth_list.append(avg_depth)
        return depth_list

def main():
    od = ObstacleDetector()
    depth_samples = np.load("depth_images.npy").item()
    colormaps = depth_samples["colormap"]
    depth_images = depth_samples["image"]
    rgb_images = depth_samples["rgb"]

    # get a sample
    colormap = colormaps[5]
    colormap = cv2.cvtColor(colormap,cv2.COLOR_BGR2RGB)
    depth_image = depth_images[5]
    rgb_image = rgb_images[5]

    od.computer_depth(rgb_image,depth_image)
    
    mix = np.concatenate((colormap,rgb_image),axis=1)
    image = od.detect_and_draw_contours(rgb_image,depth_image)
    im = Image.fromarray(image)
    im.save("5_hull_crop.jpg")
    im.show()   


    # colormap_gray = cv2.cvtColor(colormap,cv2.COLOR_RGB2GRAY)
    # gray = cv2.cvtColor(rgb_image,cv2.COLOR_RGB2GRAY)
    # rgb_depth = np.concatenate((colormap,rgb_image),axis=1)
    # im = Image.fromarray(rgb_depth)
    # im.save("demo/compare_rgb_depth.jpg")
    # im.show()

    # mix = cv2.addWeighted(gray,0.5,colormap_gray,0.5,0)
    # im = Image.fromarray(mix)
    # im.save("demo/mix_rgb_depth.jpg")
    # im.show()

    # image = od.detect_and_draw_contours(colormap,depth_image)
    # im = Image.fromarray(image)
    # im.save("demo/5_hull_crop.jpg")
    # im.show()
    
    # pdb.set_trace()

if __name__ == '__main__':
    main()
