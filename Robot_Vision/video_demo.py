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

# Define FLAGS
tf.app.flags.DEFINE_string("video_path","http://10.13.0.235:8080/video",
    "Path of input video stream.")

tf.app.flags.DEFINE_boolean("detect_face",True,
    "Set as `True` will detect face in the video.")

tf.app.flags.DEFINE_boolean("detect_object",False,
    "Set as `True` will detect objects in the video.")

FLAGS = tf.app.flags.FLAGS

# DEMO on remote IP camera
RESOLUTION = (800,480)
REMOTE_CAM_IP = "http://10.13.0.235:8080/video"
video_capture = cv2.VideoCapture(REMOTE_CAM_IP)


def main(_):
    # init face recognition module
    facenet = faceNet()

    # init
    f_count = 1
    f_rate = 0
    det_arr = []
    # read frames from the cam
    while True:
        start_time = time.time()
        ret,frame = video_capture.read()
        frame = cv2.resize(frame,RESOLUTION,interpolation=cv2.INTER_CUBIC)

        # process each frame
        if FLAGS.detect_face:
            facenet.detect_face_and_draw_box(frame)

        cv2.imshow("Remote Cam",frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # check current FPS
        end_time = time.time()
        f_rate = int(1/(end_time-start_time))
        print("FPS:",int(f_rate))


    video_capture.release()
    cv2.destroyAllWindows()

    return

if __name__ == '__main__':
    tf.app.run()