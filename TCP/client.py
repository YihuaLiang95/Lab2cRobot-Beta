# -*- coding: utf-8 -*-
import TCP_service
import numpy as np

HOST = "10.8.4.170"
PORT =  12345
addr = (HOST, PORT)

npy_file = 'C:/Users/zhang/Lab2cRobot-Beta/Robot_Vision/obstacle_avoiding/depth_images.npy'

img_dict = np.load(npy_file).item()
colormap = img_dict['colormap']

client = TCP_service.TCP_user(addr)

client.client_start_connection()

for i in range(10):
    n = 1 % 6
    
    client.send_image(colormap[n])
    processed = client.receive_image()
    
    print(processed.mean())

client.close_connection()
