# -*- coding: utf-8 -*-
import sys
import pyrealsense2 as rs
import numpy as np
import pdb

try:
    import cv2
except:
    ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
    if ros_path in sys.path:
        sys.path.remove(ros_path)
    import cv2


from obstacle_detection_api import ObstacleDetector

def main():
    # Initialize obstacle detector
    od = ObstacleDetector()

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

    MAX_IMAGES = 5
    idx = 0

    # Show images
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Obstacle detection", cv2.WINDOW_AUTOSIZE)

    try:
        while True:

            # Wait for a coherent pair of frames: depth and color
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

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            
            # Stack both images horizontally
            images = np.hstack((color_image, depth_colormap))

            od_image = od.detect_and_draw_contours(color_image,depth_image)

            # Show real time video
            cv2.imshow('RealSense', images)
            cv2.imshow("Obstacle detection", od_image)

            k = cv2.waitKey(1)
            if k == ord("f"):
                # Save images
                print("save one image.")
                rgb_images.append(color_image)
                depth_images.append(depth_image)
                depth_colormaps.append(depth_colormap)
                idx += 1

            if k == ord("q"):
                # break
                break

            if idx > MAX_IMAGES:
                saved_sample = {"image":depth_images,"colormap":depth_colormaps,
                    "rgb":rgb_images}
                np.save("depth_images.npy",saved_sample)
                break

    finally:

        # Stop streaming
        pipeline.stop()



if __name__ == '__main__':
    main()