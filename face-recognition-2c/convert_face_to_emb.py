# -*- coding: utf-8 -*-

"""
use pre-trained `Inception Resnet v1` as a image feature extractor.
refer to: https://github.com/davidsandberg/facenet
"""

import os
import pdb
import time

import tensorflow as tf
import numpy as np
from scipy import misc
import cv2

import matplotlib.pyplot as plt

from utils import preprocessing

# set params
tf.app.flags.DEFINE_string("ckpt_path","ckpt/facenet/20180402-114759/model-20180402-114759.ckpt-275",
    "Path of pre-trained embedding extractor, checkpoint.")
tf.app.flags.DEFINE_string("meta_path","ckpt/facenet/20180402-114759/model-20180402-114759.meta",
    "Path of pre-trained embedding extractor, meta graph.")
tf.app.flags.DEFINE_string("load_path","./data/images",
    "Path of saved people faces")
tf.app.flags.DEFINE_string("save_path","./data/face_emb.npy",
    "Path of saved face embeddings data.")

FLAGS = tf.app.flags.FLAGS
feed_img_size = 160

def main(_):
    start_time = time.time()
    meta_path = os.path.join(os.getcwd(),FLAGS.meta_path)
    ckpt_path = os.path.join(os.getcwd(),FLAGS.ckpt_path)

    files = [os.path.join(FLAGS.load_path,p) for p in os.listdir(FLAGS.load_path)]
    names = [f.split("/")[-1] for f in files]
    emb_dict  = dict().fromkeys(names)

    with tf.Graph().as_default():
        with tf.Session() as sess:
            # load model
            saver = tf.train.import_meta_graph(meta_path)
            saver.restore(sess,ckpt_path)
            # Get input and output tensors
            images_plhd = tf.get_default_graph().get_tensor_by_name("input:0")
            emb_plhd = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            is_train_plhd = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            for i,file in enumerate(files):
                print("{}/{} img: {}".format(i+1,len(files),names[i]))
                file = os.path.join(file,os.listdir(file)[0])
                # RGB mode
                img = misc.imread(file)

                if img.shape[0] != feed_img_size or img.shape[1] != feed_img_size:
                    img = misc.imresize(img,(feed_img_size,feed_img_size),interp="bilinear")

                # preprocessing, get rid of average brightness influence.
                # ax1 = plt.subplot(211)
                # ax1.imshow(img)
                # ax2 = plt.subplot(212)
                img = preprocessing.image_processing(img)
                img = img / 255.0
                # ax2.imshow(img)
                # plt.show()

                # get embeddings
                feed_dict = {images_plhd:np.expand_dims(img,0),
                    is_train_plhd:False}
                img_emb = sess.run(emb_plhd,feed_dict)
                emb_dict[names[i]] = img_emb

    # save data
    np.save(FLAGS.save_path,emb_dict)
    print("Convert complete in {} sec.".format(int(time.time()-start_time)))

if __name__ == '__main__':
    tf.app.run()