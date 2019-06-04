import time
import tensorflow.examples.tutorials.mnist.input_data as input_data
import tensorflow as tf
import config as cfg
import os
import lenet
from lenet import Lenet
from PIL import Image
import numpy as np
import random
from sklearn.model_selection import train_test_split

import pdb

def load_imagenet():
    root_ = 'D:/下载/imagenet'
    
    data = []
    label_flag = []
    flag = 0
    
    for folder in os.listdir(root_):
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
    '''imagenet = load_imagenet()
    
    batch_feature, batch_label = imagenet
    np.save('batch_feature.npy', batch_feature)
    np.save('batch_label.npy', batch_label)
    '''
    batch_feature = np.load('E:/Python3/knowledge_distillation/datasets/batch_feature.npy')
    batch_label = np.load('E:/Python3/knowledge_distillation/datasets/batch_label.npy')
    
    batch_x, x_test, batch_y, y_test =train_test_split(batch_feature,batch_label,test_size=0.3, random_state=0)
    
    sess = tf.Session()
    batch_size = cfg.BATCH_SIZE
    parameter_path = cfg.PARAMETER_FILE
    lenet = Lenet()
    max_iter = cfg.MAX_ITER
    
    

    saver = tf.train.Saver()
    if os.path.exists(parameter_path):
        saver.restore(parameter_path)
    else:
        sess.run(tf.global_variables_initializer())
    
    # 创建placeholder
    # batch_x = tf.cast(batch_x, dtype=tf.float32)
    # print(batch_x.dtype)
    features_placeholder = tf.placeholder(tf.float32, batch_x.shape)
    labels_placeholder = tf.placeholder(tf.float32, batch_y.shape)
    
    # 创建dataset
    dataset = tf.data.Dataset.from_tensor_slices((features_placeholder, labels_placeholder))
    
    # 批量读取,打散数据,repeat()
    dataset = dataset.shuffle(50).batch(batch_size).repeat() 
    iterator = dataset.make_initializable_iterator()
    
    sess.run(iterator.initializer, feed_dict={features_placeholder: batch_x,labels_placeholder: batch_y})
    next_element = iterator.get_next()

    for i in range(max_iter):
        #batch = mnist.train.next_batch(50)
        x_batch, y_batch = sess.run(next_element)
        if i % 10 == 0:
            train_accuracy = sess.run(lenet.train_accuracy,feed_dict={
                lenet.input_images: x_batch,lenet.raw_input_label: y_batch
            })
            loss = sess.run(lenet.loss,feed_dict={
                lenet.input_images: x_batch,lenet.raw_input_label: y_batch
            })
            print("step %d, training accuracy %.3f" % (i, train_accuracy))
            print("step %d, loss %.3f" % (i, loss))
            
            test_accuracy = sess.run(lenet.train_accuracy,feed_dict={
                lenet.input_images: x_test, lenet.raw_input_label: y_test
            })
            print("test accuracy %.3f" % (test_accuracy))
        sess.run(lenet.train_op,feed_dict={lenet.input_images: x_batch, lenet.raw_input_label: y_batch})
        '''try:
            sess.run(lenet.train_op,feed_dict={lenet.input_images: x_batch, lenet.raw_input_label: y_batch})
        except:
            pdb.set_trace()
            pass
           ''' 

    save_path = saver.save(sess, parameter_path)
    start_time = time.clock()
    test_accuracy = sess.run(lenet.train_accuracy,feed_dict={
                lenet.input_images: x_test, lenet.raw_input_label: y_test
            })
    end_time = time.clock()
    print("test accuracy %.3f" % (test_accuracy))
    print('Fps : %.3f'%(end_time - start_time))

if __name__ == '__main__':
    main()
