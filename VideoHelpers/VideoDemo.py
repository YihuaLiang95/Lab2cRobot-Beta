from CameraHelper import CameraHelper

def recordAVideo():
    cam = CameraHelper(max_frames=50, fps=6, width = 424, height = 240)
    cam.getProperties()
    cam.recordVideo()
    cam.playVideo()
    cam.playVideo(filepath = "depth_video.avi")

recordAVideo()
    
	

