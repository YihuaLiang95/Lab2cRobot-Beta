# -*- coding: utf-8 -*-
import sys
import TCP_service
import numpy as np
from PIL import Image
import glob
import time
import pdb

import pyrealsense2 as rs

try:
    import cv2
except:
    ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
    if ros_path in sys.path:
        sys.path.remove(ros_path)
    import cv2

HOST = "10.8.4.170"
PORT =  10086
addr = (HOST, PORT)

#npy_file = 'C:/Users/zhang/Lab2cRobot-Beta/Robot_Vision/obstacle_avoiding/depth_images.npy'
#img_dict = np.load(npy_file).item()
#colormap = img_dict['colormap']

filenames = glob.glob("data/*")

client = TCP_service.TCP_user(addr)

client.client_start_connection()
cv2.namedWindow("Real-time")
start_time = time.time()

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
cv2.namedWindow("Real-time", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("Face",cv2.WINDOW_AUTOSIZE)

images_count = 0
while True:
    frames = pipeline.wait_for_frames()
    # get aligned frame
    aligned_frames = align.process(frames)
    depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
    if not depth_frame or not color_frame:
        continue
    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    cv2.imshow("Real-time", color_image)

    if images_count % 20 == 0:
        client.send_image(color_image)
        p_img = client.receive_image()

    k = cv2.waitKey(1)
    if k == ord("d"):
        client.send_image(color_image)
        p_img = client.receive_image()

    if k == ord("q"):
        print("Stop")
        break

    cv2.imshow("Face", p_img)

    images_count += 1



# for filename in filenames:
#     print(filename)
#     im = Image.open(filename)
#     img = np.array(im)
#     client.send_image(img)
#     p_img = client.receive_image()
#     # pdb.set_trace()
#     # Image.fromarray(p_img.astype(np.uint8)).show()
#     cv2.imshow("Real-time", p_img.astype(np.uint8))
#     k = cv2.waitKey(1)
#     # time.sleep(1)

duration = time.time() - start_time
print("{:.1f} sec, {} ".format(duration, len(filenames)))


# for i in range(10):
#     n = 1 % 6
    
#     client.send_image(colormap[n])
#     processed = client.receive_image()
    
#     print(processed.mean())

client.close_connection()
