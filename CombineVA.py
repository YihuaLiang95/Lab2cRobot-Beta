import sys
import cv2
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
RESPEAKER_CHANNELS = 1 # change base on firmwares, default_firmware.bin as 1 or i6_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 1  # refer to input device id
CHUNK = 1024

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
def CatchFrames(videoname = "VideoRecord.avi",camera_to_use = 0,TimeLength=7.0,RandFrames=False,ShowWindow = False):

    cap = cv2.VideoCapture(0)
    codec = cv2.VideoWriter_fourcc(*"MJPG")
    fps = 25.0
    image_size = (640,480)
    output = cv2.VideoWriter(videoname,codec,fps,image_size)
    
    if ShowWindow :
        windowName = "Live"
        cv2.namedWindow(windowName,cv2.WINDOW_NORMAL)
    else:
        pass
    
    if not(((len(sys.argv)==2) and (cap.open(str(sys.argv[1]))) or (cap.open(camera_to_use)))):
        print("Error: no camera can be used or no video sources")
        return -1

    if RandFrames == True:
        OutCounter = random.randint(1,50)
        
    start = time.time()
    end = time.time()
    Count = 0
    while(cap.isOpened()):
        if end-start >= TimeLength:
            break
            
        _,frame = cap.read()
        #pdb.set_trace()
        start_t = cv2.getTickCount()
        output.write(frame)
        
        Count += 1
        if RandFrames == True:
            if Count == OutCounter:
                Outframe = frame.deepcopy()
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
    if RandFrames == True:
        return videoname,Outframe
    else:
        return videoname,frame
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
    record(WAVE_OUTPUT_FILENAME=filename,RECORD_SECONDS=Time)
    sig = psudo_realtime_wav(filename)

    videoname,frame = CatchFrames(TimeLength=Time)
    """
    r_thread = RecordThread(psudo_realtime_wav,(filename,5.0,22050))
    v_thread = RecordThread(CatchFrames,("VideoRecord.avi",0,5.0))

    r_thread.start()
    v_thread.start()

    r_thread.join()
    v_thread.join()

    sig = r_thread.get_result()
    videoname,frame = v_thread.get_result()

    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    return sig,frame,videoname
def recordVA_p(filename='output.wav',videoname = "VideoRecord.avi",Time = 2.0):
    pool = multiprocessing.Pool(processes = 3)
    result = []
    result.append(pool.apply_async(CatchFrames,(videoname,0,Time)))
    result.append(pool.apply_async(psudo_realtime_wav,(filename,Time)))
    pool.close()
    pool.join()
    sig = result[1].get()
    videoname,frame = result[0].get()

    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    return sig,frame,videoname
if __name__ == "__main__":
    print("start")
    s = time.time()
    sig,frame,videoname = recordVA_p(filename = 'ouput.wav',Time=5.0)
    plt.imshow(frame)
    e = time.time()
    print("done,%.3f" % (e-s))