from CameraHelper import CameraHelper

def recordAVideo():
    cam = CameraHelper()
    cam.recordVideo()
    cam.playVideo()
    cam.playVideo(filepath = "depth_video.avi")

recordAVideo()
    
	

