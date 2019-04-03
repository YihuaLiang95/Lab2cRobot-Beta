# -*- coding: utf-8 -*-

from utils import detect_face
import numpy as np
from scipy import misc
import pdb

def face_detect(frame,pnet,rnet,onet,threshold,flags):
    factor = flags.scale_factor
    minsize = flags.minsize_face

    bounding_boxes, points = detect_face.detect_face(frame,
        minsize,pnet,rnet,onet,threshold,factor)
    # points[:,0] are places of [left eye, right eye, nose, left mouth, right mouth]

    nrof_faces = bounding_boxes.shape[0]
    if nrof_faces > 0: # find face
        det = bounding_boxes[:,0:4]
        scores = bounding_boxes[:,-1]
        # bounding_box_size = np.c_[det[:,2]-det[:,0],det[:,3]-det[:,1]]
        # bounding_box_size = bounding_box_size.astype(int)

        # first select by face_threshold
        det_arr = []
        scores_arr = []
        for i in range(nrof_faces):
            if scores[i] < flags.face_threshold: # skip
                    continue
            det_arr.append(np.squeeze(det[i]))
            scores_arr.append(scores[i])

        if flags.detect_multiple_faces: # detect multiple faces
            return det_arr,points,scores_arr
        else: # detect one face
            idx = np.argmax(scores_arr)
            return det_arr[idx],points[idx],np.max(scores_arr)

    else: # do not find face
        # print("Unable to find face.")
        return [],[],[]

def align_face(frame,det,flags):
    # read params
    margin = flags.margin
    face_size = flags.face_size
    img_size = np.asarray(frame.shape)[0:2]
    det = np.squeeze(det)
    bb = np.zeros(4,dtype=np.int32)
    bb[0] = np.maximum(det[0] - margin/2,0)
    bb[1] = np.maximum(det[1] - margin/2,0)
    bb[2] = np.minimum(det[2] + margin/2,img_size[1])
    bb[3] = np.minimum(det[3] + margin/2,img_size[0])
    cropped = frame[bb[1]:bb[3],bb[0]:bb[2] , :]
    scaled = misc.imresize(cropped,(face_size,face_size),interp="bilinear")
    return scaled