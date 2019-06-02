import sys
import numpy as np
import matplotlib.pyplot as plt
import pyrealsense2 as rs

class CameraHelper:
    def __init__(self, max_frames = 10, fps = 30, width = 640, height = 480):
        self.max_frames = max_frames
        self.frames_per_sec = fps
        self.width = width
        self.height = height
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.codec = cv2.VideoWriter_fourcc(*"MJPG")
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, self.frames_per_sec)
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, self.frames_per_sec)

    def saveVideo(rgbStream = True, depthStream = True):
        if (not rgbStream) and (not depthStream):
            return None
        outputColor, outputDepth = None, None
        if rgbStream:
            outputColor = cv2.VideoWriter('RGB_video.avi',codec,FPS,(self.width, self.height))
        if depthStream:
            outputDepth = cv2.VideoWriter('depth_video.avi',codec,FPS,(self.width, self.height))
        self.pipeline.start(config)
        idx = 0
        try:
            while True:
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                depth_frame = frames.get_depth_frame()
                if not depth_frame or not color_frame:
                    continue
                if (idx > self.max_frames):
                    break
                if rgbStream:
                    color_image = np.asanyarray(color_frame.get_data())
                    outputColor.write(color_image)
                if depthStream:
                    depth_image = np.asanyarray(depth_frame.get_data())
                    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,alpha=0.03),cv2.COLORMAP_JET)
                    outputDepth.write(depth_colormap)
                #images = np.hstack((color_image,depth_colormap))
                #cv2.imshow('realsense',images)
                #key = cv2.waitKey(1)
                idx+=1
            outputColor.release()
            outputDepth.release()
        finally:
            self.pipeline.stop()
        print("Saved %d frames." % (idk-1))

    def readVideo(filepath = 'RGB_video.avi'):
        cap = cv2.VideoCapture(filepath)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imshow('Display',rgb)
            if (not ret) or (cv2.waitKey(10) & 0xFF == ord('q')):
                break
        cap.release()
        cv2.destroyAllWindows()
    
