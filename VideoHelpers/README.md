How to use the CameraHelper class to record videos.
===================================================

1) Import it as such:

from CameraHelper import CameraHelper

2) Create an instance either using the default constructor or parameterised constructor.

cam = CameraHelper(max_frames=50, fps=6, width = 424, height = 240)
    
3) To record a video, call the recordVideo function.

cam.recordVideo()

4) Use the getter function to view the camera properties.

cam.getProperties()
    
5) To play the recorded videos:

Play RGB stream: cam.playVideo()
Play the depth stream: cam.playVideo(filepath = "depth_video.avi")


