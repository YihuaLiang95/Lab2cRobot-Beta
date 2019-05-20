#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import record
import upload

index = 0
while(1):
    filename = "Sample"+str(index)+".wav"
    record.record(filename,if_predict=False,if_upload = True)
    #upload.upload_file(file_path = '~//catkin_ws//src//rikirobot_project//rikirobot//script//',file_name = filename,target_path='//home//robot//uploadtest//')
    
    index+=1
    
