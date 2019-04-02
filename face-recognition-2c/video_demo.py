# -*- coding: utf-8 -*-
# Written by Zifeng
# wangzf18@mails.tsinghua.edu.cn

"real-time face detection and verification"
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pdb
import time

import tensorflow as tf
import cv2
import numpy as np
from scipy import misc

from utils import detect_face
import mtcnn_detector
import facenet_detector

tf.app.flags.DEFINE_string("video_path","0",
    "Video path, if set 0, capture video from camera.")
tf.app.flags.DEFINE_string("emb_path","./data/face_emb.npy",
    "Saved faces embeddings path.")

tf.app.flags.DEFINE_string("video_resolution","800*600",
    "Resolution of the video frame, format as `xxx*xxx`")
tf.app.flags.DEFINE_integer("face_size",200,
    "Aligned face image shape.")
tf.app.flags.DEFINE_float("face_threshold",0.9,
    "A threshold to decide if draw box or not via output scores.")
tf.app.flags.DEFINE_float("match_threshold",0.5,
    "A threshold to decide if one exists in stored face embeddings.")

tf.app.flags.DEFINE_boolean("with_gpu",False,
    "Set as `True` will make use of GPU for detection.")
tf.app.flags.DEFINE_boolean("detect_multiple_faces",True,
    "Set as `False` will only detect one face one frame.")

tf.app.flags.DEFINE_float("gpu_memory_fraction",0.5,
    "Upper bound on the amount of GPU memory that will be used by the process.")
tf.app.flags.DEFINE_integer("frame_interval",2,
    "Doing detection per number of frames")
tf.app.flags.DEFINE_integer("minsize_face",20,
    "Minimum size of face.")
tf.app.flags.DEFINE_float("scale_factor",0.709,
    "Scale factor.")
tf.app.flags.DEFINE_integer("margin",44,
'Margin for the crop around the bounding box (height, width) in pixels.')

FLAGS = tf.app.flags.FLAGS

def main(_):
    
    # force use of CPU
    if FLAGS.with_gpu == False:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""

    threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
    emb_path = FLAGS.emb_path
    try:
        emb_dict = np.load(emb_path).item()
    except:
        print("Cannot load embeddings data from {} !".format(emb_path))
        
    # load face verification model
    facenet_ = facenet_detector.facenet_detector()
    name_ar,emb_ar = facenet_detector.get_names_emb_from_dict(emb_dict)

    if FLAGS.video_path in ["0","1"]:
        video_path = int(FLAGS.video_path)
        print("Capture video from camera {}.".format(video_path))
    else:
        video_path = FLAGS.video_path

    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=
                            FLAGS.gpu_memory_fraction)
        sess = tf.Session(config=tf.ConfigProto(
                            gpu_options=gpu_options, 
                            log_device_placement=False,
                            allow_soft_placement=True),)
        with sess.as_default():
            pnet,rnet,onet = detect_face.create_mtcnn(sess,"./ckpt/mtcnn")

        video_capture = cv2.VideoCapture(video_path)
        f_count = 0
        f_rate = 0
        det_arr = []
        start_time = time.time()
        while True:
            # capture frame by frame
            ret,frame = video_capture.read()
            # scaled frame
            f_width,f_height = [int(a) for a in FLAGS.video_resolution.split("*")]
            try:
                o_frame = cv2.resize(frame,(f_width,f_height),interpolation=cv2.INTER_CUBIC)
            except:
                break

            i_frame = cv2.cvtColor(o_frame,cv2.COLOR_BGR2RGB)

            if f_count % FLAGS.frame_interval == 0:
                # check current FPS                
                end_time = time.time()
                if (end_time-start_time) > 1:
                    f_rate = int(f_count/(end_time-start_time))
                    start_time = time.time()
                    f_count = 0
            
                # detect face
                det_arr,pts_arr,scores_arr = mtcnn_detector.face_detect(i_frame,
                                                                pnet,rnet,onet,threshold,FLAGS)

                if len(det_arr) > 0:
                    faces = []
                    for i,det in enumerate(det_arr):
                        # get aligned faces as input
                        face = mtcnn_detector.align_face(i_frame,det,FLAGS)
                        # resize, as input for pretrained Inception-ResNet-V1
                        face = misc.imresize(face,(160,160),interp="bilinear")
                        faces.append(face)
                    # face verification
                    faces = np.array(faces)
                    person_name = facenet_.face_verify(faces,name_ar,emb_ar,FLAGS.match_threshold)
            
            # draw boxes
            if len(det_arr) > 0:
                for i,det in enumerate(det_arr):
                    draw_box(o_frame,det,person_name=person_name[i])
            
            # other put Texts
            print("number of faces: {} scores: {}".format(len(det_arr),scores_arr)) 
            cv2.putText(o_frame,"num of faces:"+str(len(det_arr)),(10,60),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),thickness=2,lineType=2)
            cv2.putText(o_frame,str(f_rate)+"fps",(10,30),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),thickness=2,lineType=2)

            f_count += 1
            cv2.imshow("Real-time Output",o_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()


def draw_box(frame,box,person_name="Unknown"):
    box = box.astype(int)
    cv2.putText(frame,person_name,(box[0],box[3]),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
    cv2.rectangle(frame,(box[0],box[1]),(box[2],box[3]),(0,97,255),2)

if __name__ == '__main__':
    tf.app.run()













