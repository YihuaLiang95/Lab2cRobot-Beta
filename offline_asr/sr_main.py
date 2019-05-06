from __future__ import print_function
import os
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

def speech_recognition(audio_file):
    model_path = '/home/tbsi2c/rikirobot_audio/lucky13/ros_voice_system/src/offline_asr/model'

    config = {
        'hmm': os.path.join(model_path, 'zh_cn.cd_cont_5000'),
        'lm': os.path.join(model_path, 'zh_command.lm'),
        'dict': os.path.join(model_path, 'zh_command.dic')
    }
    ps = Pocketsphinx(**config)
    ps.decode(
        audio_file=audio_file,
        buffer_size=2048,
        no_search=False,
        full_utt=False
    )

    print(ps.segments()) # => ['', '<sil>', 'go', 'forward', 'ten', 'meters', '']
    print('Detailed segments:', *ps.segments(detailed=True), sep='\n') # => [
    #     word, prob, start_frame, end_frame
    #     ('', 0, 0, 24)
    #     ('<sil>', -3778, 25, 45)
    #     ('go', -27, 46, 63)
    #     ('forward', -38, 64, 116)
    #     ('ten', -14105, 117, 152)
    #     ('meters', -2152, 153, 211)
    #     ('', 0, 212, 260)
    # ]

    print(ps.hypothesis())  # => go forward ten meters
    print(ps.probability()) # => -32079
    print(ps.score())       # => -7066
    print(ps.confidence())  # => 0.04042641466841839

    print(*ps.best(count=10), sep='\n') # => [
    #     ('go forward ten meters', -28034)
    #     ('go for word ten meters', -28570)
    #     ('go forward and majors', -28670)
    #     ('go forward and meters', -28681)
    #     ('go forward and readers', -28685)
    #     ('go forward ten readers', -28688)
    #     ('go forward ten leaders', -28695)
    #     ('go forward can meters', -28695)
    #     ('go forward and leaders', -28706)
    #     ('go for work ten meters', -28722)
    # ]
    return (ps.segments(), ps.confidence())

if __name__ == '__main__':
    audio_file = 'record/input.wav'
    speech_recognition(audio_file)
