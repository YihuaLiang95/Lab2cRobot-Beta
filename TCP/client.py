# -*- coding: utf-8 -*-
import TCP_service
import numpy as np
import time
import matplotlib.pyplot as plt

HOST = "127.0.0.1"
PORT =  10086
addr = (HOST, PORT)

npy_file = 'C:/Users/zhang/Lab2cRobot-Beta/Robot_Vision/obstacle_avoiding/depth_images.npy'

img_dict = np.load(npy_file).item()
colormap = img_dict['rgb']

client = TCP_service.TCP_user(addr)

client.client_start_connection()


for i in range(10):
    n = 1 % 6
    start = time.clock()
    client.send_to(colormap[n], 'image')
    print('send')
    processed, file_type = client.receive_from()
    end = time.clock()
    print('Time Cost on processing object: %.2f s'%(end - start))

client.close_transmission()
