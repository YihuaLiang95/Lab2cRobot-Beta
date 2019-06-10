# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 18:37:39 2019

@author: zhang
"""

import tensorflow as tf
import tensorflow.contrib.slim as slim
import config as cfg

class Lenet:
    def __init__(self):
        self.sess = tf.Session()
        self.input_images = tf.placeholder(tf.float32, [None, 224, 224, 3])
        self.input_labels = tf.placeholder(tf.float32, [None, 5])
        
        self.dropout = cfg.KEEP_PROB
        
        self.iterator = None

        with tf.variable_scope("Lenet") as scope:
            self.train_digits = self.construct_net(True)
            scope.reuse_variables()
            self.pred_digits = self.construct_net(False)

        # self.prediction = tf.cast(tf.argmax(self.pred_digits, 1), dtype = tf.int32)
        self.correct_prediction = tf.equal(tf.argmax(self.pred_digits, 1), tf.argmax(self.input_labels, 1))
        self.train_accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, "float"))


        self.loss = tf.losses.softmax_cross_entropy( onehot_labels = self.input_labels, logits = self.pred_digits)
        self.lr = cfg.LEARNING_RATE
        self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)

    def get_loss(self, input_images, input_labels):
        loss = self.loss
        feed_dict = {self.input_images : input_images, self.input_labels : input_labels}
        return self.sess.run(loss, feed_dict = feed_dict)
    
    def train_optimal(self, input_images, input_labels):
        train_op = self.train_op
        feed_dict = {self.input_images : input_images, self.input_labels : input_labels}
        return self.sess.run(train_op, feed_dict = feed_dict)
    
    def get_accuracy(self, input_images, input_labels):
        get_accuracy = self.train_accuracy
        feed_dict = {self.input_images : input_images, self.input_labels : input_labels}
        return self.sess.run(get_accuracy, feed_dict = feed_dict)

    def predict(self, x_test):
        feed_dict = {self.input_images:x_test}
        pred =  self.train_digits
        return self.sess.run(pred, feed_dict = feed_dict)
    
    def iterator_initializer(self, batch_x, batch_y):
        features_placeholder = tf.placeholder(tf.float32, batch_x.shape)
        labels_placeholder = tf.placeholder(tf.float32, batch_y.shape)

        dataset = tf.data.Dataset.from_tensor_slices((features_placeholder, labels_placeholder))

        dataset = dataset.shuffle(50).batch(cfg.BATCH_SIZE).repeat()
        self.iterator = dataset.make_initializable_iterator()

        feed_dict = {features_placeholder : batch_x, labels_placeholder : batch_y}
        init = self.iterator.initializer
        self.sess.run(init, feed_dict = feed_dict)
        

    def get_next(self):
        next_element = self.iterator.get_next()
        return self.sess.run(next_element)

    def global_variables_initializer(self):

        init = tf.global_variables_initializer()
        self.sess.run(init)

    def construct_net(self,is_trained = True):
        with slim.arg_scope([slim.conv2d], padding='VALID',
                            weights_initializer=tf.truncated_normal_initializer(stddev=0.01),
                            weights_regularizer=slim.l2_regularizer(0.0005)):
            net = slim.conv2d(self.input_images,8,[3,3],1,padding='SAME',scope='conv1')
            net = slim.max_pool2d(net, [2, 2], scope='pool2')
            net = slim.conv2d(net,16,[3,3],1,scope='conv3')
            net = slim.max_pool2d(net, [2, 2], scope='pool4')
            net = slim.conv2d(net,32,[3,3],1,scope='conv5')
            
            net = slim.conv2d(net,5,[1,1],1,scope="conv6") # [None,k,k,5]
            net = tf.reduce_mean(net, [1,2], name="global_avg_pooling") # [None, 5]
            digits = tf.nn.softmax(net) # [None, 5]
            '''
            net = slim.flatten(net, scope='flat6')
            net = slim.fully_connected(net, 64, scope='fc7')
            net = slim.dropout(net, self.dropout,is_training=is_trained, scope='dropout8')
            digits = slim.fully_connected(net, 5, scope='fc9')
            '''
        return digits
