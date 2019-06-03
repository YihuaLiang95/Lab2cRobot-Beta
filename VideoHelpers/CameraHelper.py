import sys
import numpy as np
import matplotlib.pyplot as plt
import pyrealsense2 as rs
try:
    import cv2
except:
    ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
    if ros_path in sys.path:
        sys.path.remove(ros_path)
    import cv2

'''
To alter the defaukt properties such as fps, width and height, please run 
'rs-enumerate-devices' on the terminal to get a list of possible values.
'''
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

    def recordVideo(self, rgbStream = True, depthStream = True):
        if (not rgbStream) and (not depthStream):
            return None
        print("Initialising camera pipeline and video writers..")
        outputColor, outputDepth = None, None
        if rgbStream:
            outputColor = cv2.VideoWriter('RGB_video.avi',self.codec,self.frames_per_sec,(self.width, self.height))
        if depthStream:
            outputDepth = cv2.VideoWriter('depth_video.avi',self.codec,self.frames_per_sec,(self.width, self.height)) 
        self.pipeline.start(self.config)
        print("Starting camera stream..")
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
                idx+=1
            outputColor.release()
            outputDepth.release()
        finally:
            self.pipeline.stop()
            print("Done with streaming and saving camera stream.")
        print("Saved %d frames." % (idx-1))

    def getProperties(self):
        print("Maximum #frames to record: %d\nFrames per second: %d\nWidth: %f\nHeight:%f\n" %(self.max_frames, self.frames_per_sec, self.width, self.height))

    def playVideo(self, filepath = 'RGB_video.avi'):
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
    
