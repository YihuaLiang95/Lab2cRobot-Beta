# -*- coding: utf-8 -*-
import TCP_service
import time 

HOST = "127.0.0.1"
PORT =  10086
addr = (HOST, PORT)

def image_process(image):
    if 'array' not in str(type(image)):
        return
    
    processed = image[:,:,0]
    
    return processed
    
server = TCP_service.TCP_user(addr)
 
server.server_start_connection()
    
flag = 1
while 1:
    if flag == 1:
        server.server_accept_message()
        
    
    start = time.clock()
    obj, file_type = server.receive_from()
    if file_type:        
        flag = 0
    else:
        server.close_transmission()
        flag = 1
    end = time.clock()
    print('Time Cost on recvicing object: %.2f s'%(end - start))
    
    if file_type == 'dict':
        server.send_to(obj, file_type)
    elif file_type == 'image':
        processed = image_process(obj)
        server.send_to(processed, file_type)


server.close_connection()