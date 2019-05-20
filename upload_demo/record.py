import pyaudio
import wave
import numpy as np
from scipy import fftpack
import voiceprint
import pyttsx3
import upload

def record(file_name = "Sample.wav",if_predict = True, if_upload = False):
    RESPEAKER_RATE = 16000
    RESPEAKER_CHANNELS = 1 # change base on firmwares, default_firmware.bin as 1 or i6_firmware.bin as 6
    RESPEAKER_WIDTH = 2
    # run getDeviceInfo.py to get index
    RESPEAKER_INDEX = 8  # refer to input device id
    CHUNK = 1024
    RECORD_SECONDS = 3
    #move to function parameters
    time = RECORD_SECONDS
    threshold = 7000
    WAVE_OUTPUT_FILENAME = file_name
    #parameters done
    p = pyaudio.PyAudio()

    stream = p.open(
                rate=RESPEAKER_RATE,
                format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                input=True,
                input_device_index=RESPEAKER_INDEX,)

    print("* recording")

    frames = [] 
    if RECORD_SECONDS > 0: 
        for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        RECORD_SECONDS = 0
    if RECORD_SECONDS == 0:
        stopflag = 0
        stopflag2 = 0
        while True:
            data = stream.read(CHUNK)
            rt_data = np.frombuffer(data,np.dtype('<i2'))
            fft_temp_data = fftpack.fft(rt_data,rt_data.size,overwrite_x = True)
            fft_data = np.abs(fft_temp_data)[0:fft_temp_data.size//2+1]
        
            if sum(fft_data) // len(fft_data) > threshold:
                stopflag += 1
            else:
                stopflag2 += 1
            oneSecond=int(RESPEAKER_RATE/CHUNK)
            if stopflag2 + stopflag > oneSecond:
                if stopflag2 > oneSecond // 3*2:
                    break
                else:
                    stopflag2 = 0
                    stopflag = 0
            frames.append(data)
    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    if if_predict:
        predict = voiceprint.voiceprint(file_name)
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty("rate",120)
        volume = engine.getProperty('volume')
        engine.setProperty("volume",volume+5)
        engine.say("You are " + predict +'.')
        engine.runAndWait()
        
    if if_upload:
        upload.upload_file(file_path = './/',file_name = file_name,target_path='//home//robot//uploadtest//')
    
    return
