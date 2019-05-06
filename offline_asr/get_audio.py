# -*- coding:utf-8 -*-
import pyaudio
import wave
input_filename = "input.wav"               
input_filepath = "record/"              # path name has to be changed
in_path = "/home/tbsi2c/record/offline_input.wav"

def record(filepath):
    CHUNK = 256
    FORMAT = pyaudio.paInt16
    CHANNELS = 1                # 声道数
    RATE = 16000                # 采样率
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = filepath
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("*"*10, "Start recording: Input audio in 5 seconds")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("*"*10, "End recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == '__main__':
    record(in_path)
