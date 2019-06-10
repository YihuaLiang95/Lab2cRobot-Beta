# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 18:37:38 2019

@author: zhang
"""

import time
import tensorflow as tf
import config as cfg
import os
import lenet
from lenet import Lenet
from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split

import time

def load_imagenet():
    root_ = './'
    
    data = []
    label_flag = []
    flag = 0
    
    for folder in os.listdir(root_):
        if '.' not in folder:
            for image in os.listdir('%s/%s/'%(root_, folder)):
                img = Image.open('%s/%s/%s'%(root_, folder, image)).resize((224,224))
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img_data = np.asarray(img, dtype='f')
                if len(img_data.shape) == 3:
                    data.append(img_data)
                    # data.append(img_data)
                    label_flag.append(flag)
            
            flag += 1
    # pdb.set_trace()
    # one hot
    label = np.eye(flag, dtype='f')[label_flag]
    
    return np.array(data), label
    
def main():
    # mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
    '''
    imagenet = load_imagenet()

    batch_feature, batch_label = imagenet
    np.save('batch_feature.npy', batch_feature)
    np.save('batch_label.npy', batch_label)
    '''
    print('script start')
    batch_feature = np.load('batch_feature.npy', mmap_mode = 'r').astype(np.float32)
    print('imgae load')
    batch_label = np.load('batch_label.npy', mmap_mode = 'r').astype(np.float32)
    print('data label')
    batch_x, x_test, batch_y, y_test =train_test_split(batch_feature,batch_label,test_size=0.3, random_state=0)
    
    print('Data ready')

    # sess = tf.Session()
    batch_size = cfg.BATCH_SIZE
    parameter_path = cfg.PARAMETER_FILE
    lenet = Lenet()
    max_iter = cfg.MAX_ITER
    # pdb.set_trace()
    print('Parameters loaded') 

    saver = tf.train.Saver(max_to_keep=5)
    if os.path.exists(parameter_path):
        saver.restore(parameter_path)
    else:
        lenet.global_variables_initializer()
    
    lenet.iterator_initializer(batch_x, batch_y)
    print("Dataset Initialized")

    for i in range(max_iter):
        #batch = mnist.train.next_batch(50)
        x_batch, y_batch = lenet.get_next()
         
        lenet.train_optimal(x_batch, y_batch)
        # print("Iter {}".format(i))
        
        if i % 100 == 0:
            start_time = time.clock()
            train_accuracy = lenet.get_accuracy(x_batch, y_batch)
            loss = lenet.get_loss(x_batch, y_batch)
            print("step %d, training accuracy %.3f" % (i, train_accuracy))
            print("step %d, loss %.3f" % (i, loss))
            
            test_accuracy = lenet.get_accuracy(x_test, y_test)
            print("test accuracy %.3f" % (test_accuracy))
            print('The time cost of training: %.2f'%(time.clock() - start_time))
        
        '''try:
            sess.run(lenet.train_op,feed_dict={lenet.input_images: x_batch, lenet.raw_input_label: y_batch})
        except:
            pdb.set_trace()
            pass
           ''' 

    save_path = saver.save(lenet.sess, parameter_path)
    
    fps_x_test = x_test[:-100]
    # fps_y_test = y_test[:-100]
    
    start_time = time.clock()
    digits = lenet.predict(fps_x_test)
    end_time = time.clock()
    print('Fps : %.3f'%(end_time - start_time))

if __name__ == '__main__':
    print('*' * 20)
    main()
