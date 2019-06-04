# -*- coding: utf-8 -*-

import socket
import numpy as np
import struct
import json
import time


HOST = "127.0.0.1"
PORT =  1234
addr = (HOST, PORT)

class TCP_user():
    def __init__(self, addr):
        self.addr = addr
        self.sock = None
    
    def send_image(self, image):
        '''
        image is a image array
        '''
        print(addr)
        if 'array' not in str(type(image)):
            return
        
        
        print('Create new connection')
        try:
            # prepocess the image data
            if 'int' in str(image.dtype):
                IM = image.astype(np.uint8)
                file_type = 'np.uint8'
            else:
                IM = image.astype(np.float32)
                file_type = 'np.float32'
                
            IM_string = IM.tostring()
            
            # define the header of file
            file_info = {'file_size' : len(IM_string), 'file_shape' : image.shape, 'file_type' : file_type}
            info_byte = bytes(json.dumps(file_info),encoding='utf-8') 
            
            
            len_byte=struct.pack('i',len(info_byte)) 
            
            # send the len of file header to server
            self.sock.send(len_byte)
            # send the len of image to server (byte type)
            self.sock.send(info_byte)
            
            # send the image data to server
            self.sock.sendall(IM_string)
            print  ("sent" ,image.shape)
    
        except MemoryError:
            print('something failed sending data')
    
    def receive_image(self):
        head_len_bytes=self.sock.recv(4, socket.MSG_WAITALL)
        
        if not head_len_bytes:
            return 
        
        print('Accept new connection')
        x = struct.unpack('i',head_len_bytes)[0]
    
        head_byte = self.sock.recv(x)
        header = eval(head_byte)
    
    #    print(int(header['size']))
        
        recv_bytes = 0
        total_bytes = b''
#        start = time.clock()
        
        file_size = int(header['file_size'])
        file_shape = header['file_shape']
        file_type = eval(header['file_type'])
        
        while recv_bytes < file_size:
            if file_size - recv_bytes < 1024:
                buffer = file_size - recv_bytes
            else:
                buffer = 1024
            data = self.sock.recv(buffer, socket.MSG_WAITALL)
            total_bytes += data
            recv_bytes += buffer
        
#        end = time.clock()
    #    print(len(total_bytes))
#        print('Transmission Cost: %S'%(end - start))
        image = np.frombuffer(total_bytes, file_type).reshape(file_shape)
    #    print(a.shape)
    #    global IM
    #    IM = a[:921600].reshape(file_shape)
        return image

    def server_start_connection(self):
        #第一步：创建一个socket
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #第二步：绑定监听的地址和端口,方法bind()只接收一个tuple
        s.bind(self.addr)
        #第三步：调用listen（）方法开始监听端口，传入的参数指定等待连接的最大数量
        s.listen(2)
        #第四步：服务器程序通过一个永久循环来接收来自客户端，accept()会等待并返回一个客户端的连接
        sock,addr=s.accept()
        print ('Accepting to %s port %s' % addr)
        self.sock = sock
    
    def client_start_connection(self):
        '''
        addr = (HOST, PORT)
        '''
        # create a tcp/ip socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # connect the socket to the port where the server is listening
        print ('connecting to %s port %s' % self.addr)
        
        sock.connect(self.addr)
        print ('have connected')
        self.sock = sock

    def close_connection(self):
        print ('closing socket')
        print ("done sending")
        self.sock.close()