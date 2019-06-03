How to use the CameraHelper class to record videos.
===================================================

1) Import it as such:
=====================
If CameraHelper.py is in the working directory:
-----------------------------------------------
from CameraHelper import CameraHelper

If CameraHelper.py is in another directory:
-------------------------------------------
from X.CameraHelper import CameraHelper

2) Create an instance either using the default constructor or parameterised constructor：
========================================================================================

cam = CameraHelper(max_frames=50, fps=6, width = 424, height = 240)
    
3) To record a video, call the recordVideo function. The video gets stored under the names "RGB_video.avi" and "depth_video.avi" respectively, in the current working directory.:
====================================================

cam.recordVideo()

4) Use the getter function to view the camera properties:
=========================================================

cam.getProperties()
    
5) To play the recorded videos:
===============================

Play RGB stream: cam.playVideo()
Play the depth stream: cam.playVideo(filepath = "depth_video.avi")



