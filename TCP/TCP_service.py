# -*- coding: utf-8 -*-

import socket
import numpy as np
import struct
import json
import time

class TCP_user():
    def __init__(self, addr):
        self.addr = addr
        self.sock = None
        self.conn = None
        self.listen_limitation = 2
    
    def send_to(self, obj, obj_type):
	'''
	the input only support two type object
	"image" and "dict"
	image work for the raw input of network
	dict work for store the names and coordinate
	'''
        if obj_type == 'image':              
            print('Create new connection')
            
            try:
                # prepocess the image data
                if 'int' in str(obj.dtype):
                    IM = obj.astype(np.uint8)
                    image_type = 'np.uint8'
                else:
                    IM = obj.astype(np.float32)
                    image_type = 'np.float32'
                    
                IM_string = IM.tostring()
                
                # define the header of file
                file_info = {'file_size' : len(IM_string), 'image_shape' : obj.shape, 'image_type' : image_type, 'file_type' : obj_type}
                info_byte = bytes(json.dumps(file_info),encoding='utf-8') 
                
                
                len_byte=struct.pack('i',len(info_byte)) 
                
                # send the len of file header to server
                self.conn.send(len_byte)
                # send the len of image to server (byte type)
                self.conn.send(info_byte)
                
                # send the image data to server
                self.conn.sendall(IM_string)
                print  ("sent: " ,obj_type)
        
            except MemoryError:
                print('something failed sending data')
                    
        elif obj_type == 'dict':
            if 'dict' not in str(type(obj)):
                return
            
            print('Create new connection')
            
            try:

                    
                obj_json = json.dumps(obj)
                
                # define the header of file
                file_info = {'file_size' : len(obj_json), 'file_type' : obj_type}
                info_byte = bytes(json.dumps(file_info),encoding='utf-8') 
                
                
                len_byte=struct.pack('i',len(info_byte)) 
                
                # send the len of file header to server
                self.conn.send(len_byte)
                # send the len of image to server (byte type)
                self.conn.send(info_byte)
                
                # send the image data to server
                self.conn.sendall(obj_json)
                print  ("sent: " ,obj_type)
        
            except MemoryError:
                print('something failed sending data')
            
    
    def receive_from(self):
	'''
	receive object from self.conn
	header contain the information of object
	the return consist of object and the type of object
	the function will return None, None if nothing received
	'''
        head_len_bytes=self.conn.recv(4, socket.MSG_WAITALL)
        
        if not head_len_bytes:
            return None, None
        
        print('Accept new connection')
        x = struct.unpack('i',head_len_bytes)[0]
    
        head_byte = self.conn.recv(x)
        header = eval(head_byte)
    
    #    print(int(header['size']))
        
        recv_bytes = 0
        total_bytes = b''
#        start = time.clock()
        
        file_type = header['file_type']
        
        if file_type == 'dict':
            file_size = int(header['file_size'])
            
            while recv_bytes < file_size:
                if file_size - recv_bytes < 1024:
                    buffer = file_size - recv_bytes
                else:
                    buffer = 1024
                data = self.conn.recv(buffer, socket.MSG_WAITALL)
                total_bytes += data
                recv_bytes += buffer
                
                obj_dict = eval(total_bytes)
                
            return obj_dict, file_type
            
        elif file_type == 'image':
            
            file_size = int(header['file_size'])
            image_shape = header['image_shape']
            image_type = eval(header['image_type'])
            
            
            while recv_bytes < file_size:
                if file_size - recv_bytes < 1024:
                    buffer = file_size - recv_bytes
                else:
                    buffer = 1024
                data = self.conn.recv(buffer, socket.MSG_WAITALL)
                total_bytes += data
                recv_bytes += buffer
            
    #        end = time.clock()
        #    print(len(total_bytes))
    #        print('Transmission Cost: %s'%(end - start))
            image = np.frombuffer(total_bytes, image_type).reshape(image_shape)
        #    print(a.shape)
        #    global IM
        #    IM = a[:921600].reshape(file_shape)
            return image, file_type
        
        else:
            return None, None

    def server_start_connection(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(self.addr)
        sock.listen(self.listen_limitation)
        
        self.sock = sock
        
    def server_accept_message(self):
        conn,addr=self.sock.accept()
        print ('Accepting to %s port %s' % addr)
        self.conn = conn
    
    def client_start_connection(self):
        '''
        addr = (HOST, PORT)
        '''
        # create a tcp/ip socket
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # connect the socket to the port where the server is listening
        print ('connecting to %s port %s' % self.addr)
        
        conn.connect(self.addr)
        print ('have connected')
        self.conn = conn

    def close_transmission(self):
	'''
	for both client and server
	
	'''
        print('stop transmit message')
        self.conn.close()
        
    def close_connection(self):
	'''
	only work for server
	'''
        print ('closing socket')
        print ("done sending")
        self.sock.close()