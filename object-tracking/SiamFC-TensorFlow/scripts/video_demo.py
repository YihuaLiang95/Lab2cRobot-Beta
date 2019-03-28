# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import pdb
import os
import sys
import time

import tensorflow as tf 
import numpy as np 
import cv2
from glob import glob

CURRENT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR,".."))

from inference import inference_wrapper
from inference.tracker import Tracker,TargetState
from utils.infer_utils import Rectangle,convert_bbox_format
from utils.misc_utils import auto_select_gpu, mkdir_p, sort_nicely, load_cfgs,get_center


CHECKPOINT = "Logs/SiamFC/track_model_checkpoints/SiamFC-3s-color-pretrained"

tf.app.flags.DEFINE_string("video_path","assets/TestFace",
    "The input video path.")
tf.app.flags.DEFINE_string("video_resolution","800*600",
    "Resolution of the video frame, format as `xxx*xxx`")

FLAGS = tf.app.flags.FLAGS

def main(_):
    # load model
    model_config,_,track_config = load_cfgs(CHECKPOINT)
    track_config["log_level"] = 0
    track_config["is_video"] = True

    g = tf.Graph()
    with g.as_default():
        model = inference_wrapper.InferenceWrapper()
        restore_fn = model.build_graph_from_config(model_config,track_config,CHECKPOINT)
    g.finalize()

    if not os.path.isdir(track_config['log_dir']):
        tf.logging.info('Creating inference directory: %s', track_config['log_dir'])
        mkdir_p(track_config['log_dir'])

    gpu_options = tf.GPUOptions(allow_growth=True)
    sess_config = tf.ConfigProto(gpu_options=gpu_options)
    with tf.Session(graph=g,config=sess_config) as sess:
        restore_fn(sess)
        tracker = Tracker(model,model_config=model_config,track_config=track_config)

        video_name = os.path.basename(FLAGS.video_path)
        video_log_dir = os.path.join(track_config["log_dir"],video_name)
        mkdir_p(video_log_dir)

        first_line = open(FLAGS.video_path + '/groundtruth_rect.txt').readline()
        bb = [int(v) for v in first_line.strip().split(',')]
        # Rectangle: [x,y,width,height]
        init_bb = Rectangle(bb[0] - 1, bb[1] - 1, bb[2], bb[3])  # 0-index in python

        # read from video
        video_path = glob(os.path.join(FLAGS.video_path,"*.mp4"))[0]
        video_capture = cv2.VideoCapture(video_path)

        trajectory = []
        f_count = 0
        f_rate = 0
        start_time = time.time()
        while True:
            # capture frame by frame
            _,frame = video_capture.read()
            f_width,f_height = [int(a) for a in FLAGS.video_resolution.split("*")]
            try:
                o_frame = cv2.resize(frame,(f_width,f_height),interpolation=cv2.INTER_CUBIC)
            except:
                break
            i_frame = cv2.cvtColor(o_frame,cv2.COLOR_BGR2RGB)

            # cv2.imwrite("test.jpg",o_frame)
            # pdb.set_trace()

            if f_count == 0: # initialize the tracker
                first_box = convert_bbox_format(init_bb,"center-based")
                bbox_feed = [first_box.y,first_box.x,first_box.height,first_box.width]
                input_feed = [i_frame,bbox_feed]
                frame2crop_scale = tracker.siamese_model.initialize(sess,input_feed)
                # Storing target state
                original_target_height = first_box.height
                original_target_width = first_box.width
                search_center = np.array([get_center(tracker.x_image_size),
                                          get_center(tracker.x_image_size)])
                current_target_state = TargetState(bbox=first_box,
                                                   search_pos=search_center,
                                                   scale_idx=int(get_center(tracker.num_scales)))
                # setup initialized params
                current_param = {"original_target_width":original_target_width,
                                                "original_target_height":original_target_height,
                                                "search_center":search_center,
                                                "current_target_state":current_target_state}

            bbox,current_param = tracker.track_frame(sess,i_frame,
                                                                                                current_param,
                                                                                                video_log_dir)
            # add overlays
            end_time = time.time()
            f_rate = int(1/(end_time-start_time))
            start_time = time.time()
            draw_box(o_frame,bbox)
            cv2.putText(o_frame,str(f_rate)+"fps",(10,30),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),thickness=2,lineType=2)

            trajectory.append(bbox)
            f_count += 1

            cv2.imshow("Real-time Ouput",o_frame)
            # if f_count > 30:
            #     cv2.imwrite("test.jpg",o_frame)
            #     pdb.set_trace()
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        # save track results
        # pdb.set_trace()
        with open(os.path.join(video_log_dir,"track_rect.txt"),"w") as f:
            for region in trajectory:
                rect_str = "{},{},{},{}\n".format(region.x+1,region.y+1,
                        region.width,region.height)
                f.write(rect_str)

def draw_box(frame,box):
        # box = box.astype(int)
        print(box)
        x1,y1 = int(box.x - box.width/2),int(box.y - box.height/2)
        x2,y2 = int(box.x+box.width/2), int(box.y + box.height/2)
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,977,255),2)
        cv2.putText(frame,"object",(x1,y1),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,(0,255,0),2)

if __name__ == '__main__':
    tf.app.run()







