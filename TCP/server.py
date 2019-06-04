# -*- coding: utf-8 -*-
import TCP_service

HOST = "10.8.4.170"
PORT =  10086
addr = (HOST, PORT)

def image_process(image):
    if 'array' not in str(type(image)):
        return
    
    processed = image / 255
    
    return processed
    
server = TCP_service.TCP_user(addr)

server.server_start_connection()
    
while 1:
#	#创建一个新线程来处理TCP链接
#    threading.Thread(target=tcplink,args=(sock,addr)).start()
    image = server.receive_image()
    print(type(image))
    
    processed = image_process(image)
    print('Processed')
    server.send_image(processed)

server.close_connection()