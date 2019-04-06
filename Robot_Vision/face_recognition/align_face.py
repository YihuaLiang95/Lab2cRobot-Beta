# -*- coding: utf-8 -*-
# Written by Zifeng
# wangzf18@mails.tsinghua.edu.cn

"Align faces from raw images."
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pdb
import time

import tensorflow as tf
import numpy as np
from scipy import misc

from utils import detect_face
import mtcnn_detector

# set params
tf.app.flags.DEFINE_string("load_path","./data/raw_images",
    "Path of saved raw people faces")
tf.app.flags.DEFINE_string("save_path","./data/images",
    "Path of saved aligned faces.")

tf.app.flags.DEFINE_float("face_threshold",0.9,
    "A threshold to decide if draw box or not via output scores.")
tf.app.flags.DEFINE_integer("margin",44,
    'Margin for the crop around the bounding box (height, width) in pixels.')
tf.app.flags.DEFINE_boolean("detect_multiple_faces",True,
    "Set as `False` will only detect one face one frame.")
tf.app.flags.DEFINE_integer("minsize_face",20,
    "Minimum size of face.")
tf.app.flags.DEFINE_float("scale_factor",0.709,
    "Scale factor.")
tf.app.flags.DEFINE_integer("face_size",160,
    "Aligned face image shape.")

FLAGS = tf.app.flags.FLAGS
threshold = [0.6,0.6,0.7]

def main(_):
    if os.path.isdir(FLAGS.load_path):
        raw_images = [f for f in os.listdir(FLAGS.load_path) if f.endswith(".jpg")]
        names = [n.split(".")[0] for n in raw_images]
        # get path
        raw_images = [os.path.join(FLAGS.load_path,r) for r in raw_images]
        is_dir = True
    else:
        raw_images = [FLAGS.load_path]
        names = FLAGS.load_path.split("/")[-1]
        names = [os.path.splitext(names)[0]]

    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.1)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
        pnet,rnet,onet = detect_face.create_mtcnn(sess,"./ckpt/mtcnn")

        for i,image in enumerate(raw_images):
            img = misc.imread(image)
            # detect face
            det_arr,_,_ = mtcnn_detector.face_detect(img,
                                                                pnet,rnet,onet,threshold,FLAGS)
            if len(det_arr) == 0:
                print("Cannot find face in image: {} !".format(image))
            else:
                faces = []
                for det in det_arr:
                    faces.append(mtcnn_detector.align_face(img,det,FLAGS))
            
            # save aligned face image
            dir_of_align_face = os.path.join(FLAGS.save_path,names[i])
            for idx,face in enumerate(faces):
                if not os.path.exists(dir_of_align_face):
                    os.makedirs(dir_of_align_face)
                misc.imsave(os.path.join(dir_of_align_face,"{}_{}.jpg".format(names[i],idx)),
                        face)

            print("{}/{} {}".format(i+1,len(raw_images),names[i]))

if __name__ == '__main__':
    tf.app.run()



