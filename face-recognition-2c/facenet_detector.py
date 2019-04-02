# -*- coding: utf-8 -*-
# Written by Zifeng
# wangzf18@mails.tsinghua.edu.cn

"face embeddings extraction for verification."
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pdb
import time

import tensorflow as tf 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import cv2

from utils import preprocessing

ckpt_path = "./ckpt/facenet/20180402-114759/model-20180402-114759.ckpt-275"
meta_path = "./ckpt/facenet/20180402-114759/model-20180402-114759.meta" 
img_size = 160

class facenet_detector(object):
    def __init__(self):
        # construct a graph for this detector
        self.graph = tf.Graph()
        self.sess = tf.Session(graph=self.graph)
        with self.graph.as_default():
            # load model
            saver = tf.train.import_meta_graph(meta_path)
            saver.restore(self.sess,ckpt_path)
            # get placeholders
            self.img_plhd = tf.get_default_graph().get_tensor_by_name("input:0")
            self.emb_plhd = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            self.is_train_plhd = tf.get_default_graph().get_tensor_by_name("phase_train:0")

    def face_verify(self,faces,name_ar,emb_ar,match_thres=0.5):
        """Do face verification.
        Argument:
            faces: array of face images, [num_of_faces,160,160,3]
            name_ar: list of loaded faces names.
            emb_ar: array of loaded faces embeddings.
        Return:
            person_name: list of predicted face names.
        """
        # faces preprocessing
        for i in range(len(faces)):
            faces[i] = preprocessing.image_processing(faces[i])
        faces = faces / 255.0

        # get embeddings
        feed_dict = {self.img_plhd:faces, self.is_train_plhd:False}
        res = self.sess.run(self.emb_plhd,feed_dict=feed_dict)
        person_name = []
        for r in res:
            r = r.reshape(1,-1)
            sim_ar = cosine_similarity(np.r_[r,emb_ar])[0,1:]
            if sim_ar.max() < match_thres:
                person_name.append("Unknown")
            else:
                # pdb.set_trace()
                idx = np.argmax(sim_ar)
                person_name.append(name_ar[idx])
        return person_name

def get_names_emb_from_dict(emb_dict):
        # get names and ar from dict
        name_ar = []
        emb_ar = []
        for k,v in emb_dict.items():
            name_ar.append(k)
            emb_ar.append(v)
        emb_ar = np.squeeze(np.array(emb_ar))
        return name_ar,emb_ar