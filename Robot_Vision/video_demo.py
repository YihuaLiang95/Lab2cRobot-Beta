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

from cfg.face_config import config as face_config
from cfg.object_config import config as object_config
# Packages
from face_recognition.face_recognition_api import faceNet
from object_detection.tensorflow_yolov3.object_detection_api import YOLOv3

# Define FLAGS
tf.app.flags.DEFINE_string("video_path","http://10.13.0.235:8080/video",
    "Path of input video stream.")

tf.app.flags.DEFINE_boolean("detect_face",False,
    "Set as `True` will detect face in the video.")

tf.app.flags.DEFINE_boolean("detect_object",False,
    "Set as `True` will detect objects in the video.")

FLAGS = tf.app.flags.FLAGS

# DEMO on remote IP camera
RESOLUTION = (600,480)
REMOTE_CAM_IP = "http://10.13.0.235:8080/video"

if FLAGS.video_path == "0":
    video_capture = cv2.VideoCapture(int(FLAGS.video_path))
elif FLAGS.video_path != REMOTE_CAM_IP:
    video_capture = cv2.VideoCapture(FLAGS.video_path)
else: # remote IP camera
    video_capture = cv2.VideoCapture(REMOTE_CAM_IP)


def main(_):
    # init modules
    if FLAGS.detect_face:
        facenet = faceNet()

    if FLAGS.detect_object:
        yolo = YOLOv3()

    # init
    f_count = 1
    f_rate = 0
    det_arr = []
    cv2.namedWindow("Real-time",cv2.WINDOW_AUTOSIZE)
    # read frames from the cam
    start_time = time.time()
    while True:
        ret,frame = video_capture.read()
        frame = cv2.resize(frame,RESOLUTION,interpolation=cv2.INTER_LINEAR)

        # detect objects
        if FLAGS.detect_object:
            if f_count % object_config.object_detect_interval == 0:
                frame = yolo.detect_object_and_draw_box(frame)

        # detect face
        if FLAGS.detect_face:
            if f_count % face_config.face_detect_interval == 0:
                person_name = facenet.detect_face_name_and_draw_box(frame)
                print("Hello, {} !".format(person_name))
            else:
                facenet.detect_face_and_draw_box(frame)
        
        # put Text
        fps_info = "FPS: {}".format(f_rate)
        cv2.putText(frame, text=fps_info, org=(50, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=(255, 0, 0), thickness=2)

        # check current FPS
        if f_count % 5 == 0:
            end_time = time.time()
            f_rate = int(5/(end_time-start_time))
            start_time = time.time()

        # if f_count % face_config.face_detect_interval == 0:
        #     cv2.imwrite("object_detect.jpg",frame)

        print("FPS:",int(f_rate))
        f_count += 1
        cv2.imshow("Real-time",frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    return

if __name__ == '__main__':
    tf.app.run()