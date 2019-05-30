import sys
import math
import pyaudio
import wave
from scipy.io import wavfile
import numpy as np
import time
import random
import threading
import matplotlib.pyplot as plt
import multiprocessing
import pyrealsense2 as rs

"""
It is not recommended to change the parameters.
BUT remember change respeaker index when move to different device 
"""
RESPEAKER_CHANNELS = 1 # change base on firmwares, default_firmware.bin as 1 or i6_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 8  # refer to input device id
CHUNK = 1024

try:
    import cv2
except:
    ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
    if ros_path in sys.path:
        sys.path.remove(ros_path)
    import cv2
def record(WAVE_OUTPUT_FILENAME = "output.wav", RECORD_SECONDS = 2,RESPEAKER_RATE = 22050):
    p = pyaudio.PyAudio()

    stream = p.open(
                rate=RESPEAKER_RATE,
                format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                input=True,
                input_device_index=RESPEAKER_INDEX,)

    #print("* recording")

    frames = []

    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    #print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
    print(stream)


    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return
def psudo_realtime_wav(filename = 'output.wav',Time = 2, Frequency=22050):
    record(WAVE_OUTPUT_FILENAME=filename,RECORD_SECONDS=Time,RESPEAKER_RATE=Frequency)
    DEFAULT_LENGTH = 44100
    _,sig = wavfile.read(filename)
    sig_size = sig.size
    if sig_size < DEFAULT_LENGTH:
        sig = np.append(sig,np.zeros(DEFAULT_LENGTH-sig_size))
    elif sig_size > DEFAULT_LENGTH:
        sig = sig[0:DEFAULT_LENGTH-1]
    return sig
def CatchFrames(videoname = "VideoRecord.avi",camera_to_use = 0,TimeLength=2.0,ShowWindow = False):

    cap = cv2.VideoCapture(0)
    codec = cv2.VideoWriter_fourcc(*"MJPG")
    fps = 25.0
    image_size = (640,480)
    output = cv2.VideoWriter(videoname,codec,fps,image_size)
    #default fps 30， size 640，480
    if ShowWindow :
        windowName = "Live"
        cv2.namedWindow(windowName,cv2.WINDOW_NORMAL)
    else:
        pass
    
    if not(((len(sys.argv)==2) and (cap.open(str(sys.argv[1]))) or (cap.open(camera_to_use)))):
        print("Error: no camera can be used or no video sources")
        return -1
        
    start = time.time()
    end = time.time()
    frames = []
    Count = 0
    while(cap.isOpened()):
        if end-start >= TimeLength:
            break
            
        _,frame = cap.read()
        #pdb.set_trace()
        start_t = cv2.getTickCount()
        output.write(frame)
        frames.append(frame)
        Count += 1
        if ShowWindow :
            cv2.imshow(windowName,frame)
        stop_t = ((cv2.getTickCount() - start_t)/cv2.getTickFrequency())#remove writing time
        key = cv2.waitKey(max(2, 40 - int(math.ceil(stop_t)))) & 0xFF
        if key == (ord =='q'):
            break
        end = time.time() - stop_t
    cap.release()
    output.release()
    cv2.destroyAllWindows()

    return frames
def CatchFrames_RS(MAX_IMAGES=5,Width=640,Height=480,FPS = 30,SHOW=True):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth,Width,Height,rs.format.z16,FPS)
    config.enable_stream(rs.stream.color,Width,Height,rs.format.bgr8,FPS)
    

    profile = pipeline.start(config)
    
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    clip_distance_in_meter = 1.
    clip_distance = clip_distance_in_meter/depth_scale

    align_to = rs.stream.color
    align = rs.align(align_to)

    rgb_images = []
    depth_colormaps= []
    depth_images = []

    MAX_IMAGES = 5
    idx = 0
    start = time.time()
    end = time.time()
    cv2.namedWindow('realsense',cv2.WINDOW_AUTOSIZE)
    try:
        while True:
            frames = pipeline.wait_for_frames()

            aligned_frames = align.process(frames) 
            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()

            if not depth_frame or not color_frame:
                continue
            
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())

            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,alpha=0.03),cv2.COLORMAP_JET)
            images = np.hstack((color_image,depth_colormap))

           
            cv2.imshow('realsense',images)
            key = cv2.waitKey(1)
            if key == (ord=='q'):
                break
            color_image = cv2.cvtColor(color_image,cv2.COLOR_BGR2RGB)
            rgb_images.append(color_image)
            depth_images.append(depth_image)
            depth_colormaps.append(depth_colormap)
            end = time.time()
            #if end - start >= TimeLength:
            if idx > MAX_IMAGES:            
                saved_sample = {"image":depth_images,"colormap":depth_colormaps,"rgb":rgb_images}
                np.save("depth_images.npy",saved_sample)
                break
            idx+=1
            print(idx)
    finally:
        pipeline.stop()
    return rgb_images

class RecordThread(threading.Thread):
    def __init__(self,func,args,name=""):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.result = self.func(*self.args)
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
            
def recordVA_t(filename='output.wav',Time=2):

    """

    """
    r_thread = RecordThread(psudo_realtime_wav,(filename,5.0,22050))
    v_thread = RecordThread(CatchFrames,("VideoRecord.avi",0,5.0))

    r_thread.start()
    v_thread.start()

    r_thread.join()
    v_thread.join()

    sig = r_thread.get_result()
    frames = v_thread.get_result()
    return sig,frames
def recordVA_p(filename='output.wav',Time = 2.0,MAX_IMAGES=5,HIDTH=128,WIDTH=128,FPS=30,Show=False):
    """
    This function will use multiprocess to catch frames while recording voice
    Attention: the process is not well synchrounized.
    filename: name of audio output
    Time: length of audio
    MAX_IMAGES: the number of frames that will be catched. Don't set value larger than 14
    HIDTH: hidth of frames
    WIDTH: width of frames
    FPS: Fps of input stream
    Show: whether show the results on screen
    """
    pool = multiprocessing.Pool(processes = 3)
    result = []
    result.append(pool.apply_async(psudo_realtime_wav,(filename,Time)))
    result.append(pool.apply_async(CatchFrames_RS,(MAX_IMAGES,HIDTH,WIDTH,FPS,Show)))
    pool.close()
    pool.join()
    sig = result[0].get()
    frames = result[1].get()
    return sig,frames
def Copy_Record(TimeLength=5):
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    profile = pipeline.start(config)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    # print("Depth scale is", depth_scale)
    clip_distance_in_meter = 1.
    clip_distance = clip_distance_in_meter / depth_scale  # around 1:1000

    # Align rgb image and depth image
    align_to = rs.stream.color
    align = rs.align(align_to)

    rgb_images = []
    depth_colormaps = []
    depth_images = []
    MAX_IMAGES = 15
    idx = 0
    #start = time.time()
    try:
        while True:

            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            # depth_frame = frames.get_depth_frame()
            # color_frame = frames.get_color_frame()
            
            # get aligned frame
            aligned_frames = align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            
            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            
            # Stack both images horizontally
            images = np.hstack((color_image, depth_colormap))

            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)
            k = cv2.waitKey(1)
            if k == ord("f"):
                break    # Save images
            rgb_images.append(color_image)
            depth_images.append(depth_image)
            depth_colormaps.append(depth_colormap)
            idx += 1
            if idx > MAX_IMAGES:
                saved_sample = {"image":depth_images,"colormap":depth_colormaps,
                    "rgb":rgb_images}
                np.save("depth_images.npy",saved_sample)
                break

    finally:

        # Stop streaming
        pipeline.stop()
if __name__ == "__main__":
    print("start")
    s = time.time()
    sig,frames = recordVA_p()
    e = time.time()
    print("done,%.3f" % (e-s))
