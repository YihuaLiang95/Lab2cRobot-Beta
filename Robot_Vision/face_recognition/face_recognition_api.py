# -*- coding: utf-8 -*-
"""Provide face-recognition API to access.
"""
# -*- coding: utf-8 -*-

import os
import pdb
import sys
import tensorflow as tf 
import numpy as np 
from scipy import misc
import cv2

sys.path.append("./face_recognition")
import mtcnn_detector
import facenet_detector
from utils import detect_face

from cfg.face_config import config

root_path = os.path.join(os.getcwd(),"face_recognition/")
mtcnn_path = os.path.join(root_path,"ckpt/mtcnn")
emb_path = os.path.join(root_path,"data/face_emb.npy")
emb_dict = np.load(emb_path).item()
facenet_ckpt_path = os.path.join(root_path,"ckpt/facenet/20180402-114759/model-20180402-114759.ckpt-275")
facenet_meta_path = os.path.join(root_path,"ckpt/facenet/20180402-114759/model-20180402-114759.meta")

class faceNet(object):
    def __init__(self):
        # GPU options
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5,allow_growth=True)
        sess_config = tf.ConfigProto(gpu_options=gpu_options)

        with tf.Graph().as_default():
            self.sess = tf.Session(config=sess_config)
            # load mtcnn detector
            self.pnet,self.rnet,self.onet = \
                    detect_face.create_mtcnn(self.sess,mtcnn_path)
            # load face verification model
            self.verify_cls = facenet_detector.facenet_detector(meta_path = facenet_meta_path,
                    ckpt_path = facenet_ckpt_path)
            self.name_ar,self.emb_ar = facenet_detector.get_names_emb_from_dict(emb_dict)

    def detect_face(self,frame):
        # detect face
        det_arr,pts_arr,scores_arr = mtcnn_detector.face_detect(frame,self.pnet,self.rnet,self.onet,
                            [0.6,0.7,0.7],config)
        return det_arr

    def verify_face(self,frame,det_arr):
        if len(det_arr) > 0:
            faces = []
            # face verification
            for i,det in enumerate(det_arr):
                face = mtcnn_detector.align_face(frame,det,config)
                face = misc.imresize(face,(160,160),interp="bilinear")
                faces.append(face)
            faces = np.array(faces)
            person_name = self.verify_cls.face_verify(faces,
                        self.name_ar,self.emb_ar,config.match_threshold)
        else:
            person_name = []

        return person_name

    def verify_face_and_draw_box(self,frame,det_arr):
        o_frame = frame.copy()
        person_name = self.verify_face(frame,det_arr)
        if len(det_arr) > 0:
            for i,det in enumerate(det_arr):
                self.draw_box_with_name(o_frame,det,person_name=person_name[i])
        return o_frame,person_name

    def detect_face_and_draw_box(self,frame):
        o_frame = frame.copy()
        det_arr = self.detect_face(frame)
        if len(det_arr) > 0:
            for i,det in enumerate(det_arr):
                self.draw_box(o_frame,det)
        return o_frame,det_arr

    def detect_face_name_and_draw_box(self,frame):
        o_frame = frame.copy()
        det_arr = self.detect_face(frame)
        person_name = self.verify_face(frame,det_arr)
        if len(det_arr) > 0:
            for i,det in enumerate(det_arr):
                self.draw_box_with_name(o_frame,det,person_name=person_name[i])
        return o_frame,person_name


    def draw_box_with_name(self,frame,box,person_name="Unknown"):
        box = box.astype(int)
        cv2.putText(frame,person_name,(box[0],box[3]),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
        cv2.rectangle(frame,(box[0],box[1]),(box[2],box[3]),(0,97,255),2)      

    def draw_box(self,frame,box):
        box = box.astype(int)
        cv2.putText(frame,"face",(box[0],box[3]),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
        cv2.rectangle(frame,(box[0],box[1]),(box[2],box[3]),(0,97,255),2)      

