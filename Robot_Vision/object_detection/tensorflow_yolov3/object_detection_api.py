# -*- coding: utf-8 -*-

import os
import pdb
import sys
import tensorflow as  tf 
import numpy as np
from scipy import misc
import cv2

from PIL import Image

sys.path.append("./object_detection/tensorflow_yolov3")

from core import utils

root_path = os.path.join(os.getcwd(),"object_detection/tensorflow_yolov3")
name_path = os.path.join(root_path,"data/coco.names")
font_path = os.path.join(root_path,"data/font/FiraMono-Medium.otf")
classes = utils.read_coco_names(name_path)
num_classes = len(classes)
nms_path = os.path.join(root_path,"./checkpoint/yolov3_cpu_nms.pb")
IMAGE_H, IMAGE_W = 416, 416

class YOLOv3(object):
    def __init__(self):
        self.graph = tf.Graph()
        with tf.Graph().as_default():
            self.sess = tf.Session()
            self.input_tensor,self.output_tensors = utils.read_pb_return_tensors(tf.get_default_graph(),
                    nms_path,["Placeholder:0", "concat_9:0", "mul_6:0"])

    def detect_object_and_draw_box(self,frame):
        frame_size = (frame.shape[1],frame.shape[0])

        i_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(i_frame,(IMAGE_H,IMAGE_W),interpolation=cv2.INTER_LINEAR)
        img_resized = img_resized / 255
        boxes, scores = self.sess.run(self.output_tensors, feed_dict={
                    self.input_tensor: np.expand_dims(img_resized, axis=0)})
        boxes, scores, labels = utils.cpu_nms(boxes, scores, num_classes, 
                    score_thresh=0.4, iou_thresh=0.5)
        frame = Image.fromarray(i_frame)
        frame = utils.draw_boxes(frame, boxes, scores, labels, classes, (IMAGE_H, IMAGE_W), 
                show=False,
                font= font_path)

        result = cv2.resize(np.asarray(frame),frame_size,interpolation=cv2.INTER_LINEAR)
        return cv2.cvtColor(result,cv2.COLOR_RGB2BGR)











