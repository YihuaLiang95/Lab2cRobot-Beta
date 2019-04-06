# -*- coding: utf-8 -*-
"""Receive frames from remote robot camera, process and return.
"""
import time

import cv2
import tensorflow as tf 
import numpy as np 
import pdb
import sys
import os

# Packages
from face_recognition.face_recognition_api import faceNet

RESOLUTION = (800,600)
REMOTE_CAM_IP = "http://10.13.0.235:8080/video"

video_capture = cv2.VideoCapture(REMOTE_CAM_IP)

def main():
    # init
    f_count = 1
    f_rate = 0
    det_arr = []
    start_time = time.time()




    # read frames from the cam
    while True:
        ret,frame = video_capture.read()
        frame = cv2.resize(frame,RESOLUTION,interpolation=cv2.INTER_CUBIC)

        # process each frame


        cv2.imshow("Remote Cam",frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # check current FPS
        end_time = time.time()
        f_rate = int(1/(end_time-start_time))


    video_capture.release()
    cv2.destroyAllWindows()

    return

if __name__ == '__main__':
    main()