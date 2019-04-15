# -*- coding: utf-8 -*-

import sys
sys.path.append("../Robot_Speech")

import speech_api


def main():
    speech_api.say_hello("Zifeng","hello.wav")
    return

if __name__ == '__main__':
    main()


