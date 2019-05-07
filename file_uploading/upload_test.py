#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import upload
import time
    
#主函数
i = 0
while(i <= 17): 
    file_name = 'average_2015APEC_second_half'+str(i)+'.jpg'
    upload.upload_file('C:\\Users\\DELL\\Desktop\\',file_name)
    i += 1
    time.sleep(5)