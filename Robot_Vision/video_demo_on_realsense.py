# -*- coding: utf-8 -*-
"""Receive frames from remote robot camera, process and return.
"""
import time
import sys
sys.path.append("/home/tbsi2c/Program/zifeng/Lab2cRobot-Beta")
sys.path.append("/home/tbsi2c/Program/zifeng/Lab2cRobot-Beta/Robot_Speech")
from Robot_Speech import speech_api

try:
    import cv2
except:
    ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
    if ros_path in sys.path:
        sys.path.remove(ros_path)
    import cv2
    # sys.path.append(ros_path)

import tensorflow as tf 
import numpy as np 
import pdb
import os
import pyrealsense2 as rs

from cfg.face_config import config as face_config
from cfg.object_config import config as object_config
# Packages
from face_recognition.face_recognition_api import faceNet
from object_detection.tensorflow_yolov3.object_detection_api import YOLOv3

# Define FLAGS
tf.app.flags.DEFINE_string("video_path","0",
    "Path of input video stream.")

tf.app.flags.DEFINE_boolean("detect_face",False,
    "Set as `True` will detect face in the video.")

tf.app.flags.DEFINE_boolean("detect_object",False,
    "Set as `True` will detect objects in the video.")

FLAGS = tf.app.flags.FLAGS

# DEMO on remote IP camera
RESOLUTION = (600,480)
REMOTE_CAM_IP = "http://10.13.0.235:8080/video"

#if FLAGS.video_path in ["0","1","2","3"]:
#    video_capture = cv2.VideoCapture(int(FLAGS.video_path))
#elif FLAGS.video_path != REMOTE_CAM_IP:
#    video_capture = cv2.VideoCapture(FLAGS.video_path)
#else: # remote IP camera
#    video_capture = cv2.VideoCapture(REMOTE_CAM_IP)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# Start streaming
pipeline.start(config)

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
        frames = pipeline.wait_for_frames()
        frame = frames.get_color_frame()
        if not frame:
            continue
        frame = np.asanyarray(frame.get_data())    
        #ret,frame = video_capture.read()
        frame = cv2.resize(frame,RESOLUTION,interpolation=cv2.INTER_LINEAR)
        raw_frame = frame.copy()

        # detect objects
        if FLAGS.detect_object:
            if f_count % object_config.object_detect_interval == 0:
                frame = yolo.detect_object_and_draw_box(frame)

        # detect face
        if FLAGS.detect_face:
            if f_count % face_config.face_detect_interval == 0:
                frame,person_name = facenet.detect_face_name_and_draw_box(frame)
                if len(person_name) > 0:
                    print("Hello, {} !".format(",".join(person_name)))
                    speech_api.say_hello(person_name,"hello.wav")
                else:
                    print("No person found!")
            else:
                frame,det_arr = facenet.detect_face_and_draw_box(frame)
               
        
        # put Text
        fps_info = "FPS: {}".format(f_rate)
        cv2.putText(frame, text=fps_info, org=(50, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=(255, 0, 0), thickness=2)

        # check current FPS
        if f_count % 5 == 0:
            end_time = time.time()
            f_rate = int(5/(end_time-start_time))
            start_time = time.time()

        key = cv2.waitKey(1)
        if key == ord("f"):
            # detect face
            try:
                frame,person_name = facenet.detect_face_name_and_draw_box(raw_frame)
            except:
                raise ImportError("The face recognition module is not initialized.")
            cv2.namedWindow("Face_Recognition")
            cv2.imshow("Face_Recognition",frame)
            cv2.imwrite("face.jpg",frame)
            # say hello
            if len(person_name) > 0:
                speech_api.say_hello(person_name,"hello.wav")


        if key == ord("o"):
            # detect objects
            try:
                frame = yolo.detect_object_and_draw_box(raw_frame)
            except:
                raise ImportError("The object detection module is not initialized.")
            cv2.namedWindow("Object_Detection")
            cv2.imshow("Object_Detection",frame)
            cv2.imwrite("object.jpg",frame)

        if  key == ord("q"):
            break

        print("FPS:",int(f_rate))
        f_count += 1
        cv2.imshow("Real-time",frame)

    video_capture.release()
    cv2.destroyAllWindows()

    return

if __name__ == '__main__':
    tf.app.run()
