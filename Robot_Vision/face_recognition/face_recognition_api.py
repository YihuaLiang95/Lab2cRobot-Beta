# -*- coding: utf-8 -*-
"""Provide face-recognition API to access.
"""

import os
import pdb
import sys

sys.path.append("./face_recognition")
import mtcnn_detector
import facenet_detector
from utils import detect_face

root_path = os.path.join(os.getcwd(),"face-recognition/")
emb_path = os.path.join(root_path,"data/face_emb.npy")


class faceNet(object):
    def __init__(self):
        print("Init faceNet...")
        return

    def init_model(self):
        print(model_path)
        pdb.set_trace()

        return

