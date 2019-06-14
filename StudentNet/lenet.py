import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np

import config as cfg
import pdb

class Lenet:
    def __init__(self):
        self.sess = tf.Session()
        self.input_images = tf.placeholder(tf.float32, [None, 224, 224, 3])
        self.input_labels = tf.placeholder(tf.float32, [None, 5])
        
        self.dropout = cfg.KEEP_PROB
        
        self.iterator = None
        
        self.is_training = tf.placeholder(dtype=bool,shape=[],name="is_training")

        with tf.variable_scope("Lenet") as scope:
            # self.train_digits = self.construct_net(True)
            # scope.reuse_variables()
            # self.pred_digits = self.construct_net(False)
            self.pred_digits = self.construct_net(self.is_training)

        # self.prediction = tf.cast(tf.argmax(self.pred_digits, 1), dtype = tf.int32)
        self.correct_prediction = tf.equal(tf.argmax(self.pred_digits, 1), tf.argmax(self.input_labels, 1))
        self.train_accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, "float"))

        # loss
        self.cross_entropy_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.input_labels,logits = self.pred_digits))

        # tf.losses.softmax_cross_entropy(self.label_plhd, self.pred)
        reg_loss = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
        self.loss = tf.add_n([self.cross_entropy_loss]+reg_loss)
        
        # debug
        self.weights_0 = tf.trainable_variables()[0]

        self.lr = cfg.LEARNING_RATE
        bn_updates = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(bn_updates):
            self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss,var_list=tf.trainable_variables())

    def get_loss(self, input_images, input_labels):
        feed_dict = {self.input_images : input_images, self.input_labels : input_labels,
            self.is_training:False}
        return self.sess.run(self.loss, feed_dict = feed_dict)
    
    def train_optimal(self, input_images, input_labels):
        train_op = self.train_op
        feed_dict = {self.input_images : input_images, self.input_labels : input_labels,
            self.is_training:True}
        return self.sess.run(train_op, feed_dict = feed_dict)
    
    def get_accuracy(self, input_images, input_labels):
        accuracy = self.train_accuracy
        batch_size = 100
        nr_batch = int(np.ceil(input_images.shape[0] / batch_size))
        acc = 0
        for i in range(nr_batch):
            feed_dict = {self.input_images : input_images[i*batch_size:(i+1)*batch_size],
                self.input_labels : input_labels[i*batch_size:(i+1)*batch_size],
                    self.is_training:False}
            acc += input_images[i*batch_size:(i+1)*batch_size].shape[0] * self.sess.run(accuracy,feed_dict)
        
        return acc / input_images.shape[0]

    def predict(self, x_test):
        batch_size = 100
        nr_batch = int(np.ceil(x_test.shape[0] / batch_size))
        pred = None
        for i in range(nr_batch):
            feed_dict = {self.input_images :x_test[i*batch_size:(i+1)*batch_size],
                    self.is_training:False}
            batch_pred = self.sess.run(self.pred_digits,feed_dict)
            if pred is None:
                pred = batch_pred
            else:
                pred = np.r_[pred,batch_pred]
        return pred

    def iterator_initializer(self, batch_x, batch_y):
        features_placeholder = tf.placeholder(tf.float32, batch_x.shape)
        labels_placeholder = tf.placeholder(tf.float32, batch_y.shape)

        dataset = tf.data.Dataset.from_tensor_slices((features_placeholder, labels_placeholder))

        dataset = dataset.shuffle(50).batch(cfg.BATCH_SIZE).repeat()
        self.iterator = dataset.make_initializable_iterator()

        feed_dict = {features_placeholder : batch_x, labels_placeholder : batch_y}
        init = self.iterator.initializer
        self.sess.run(init, feed_dict = feed_dict)
        self.next_element = self.iterator.get_next()
        
    def get_next(self):
        return self.sess.run(self.next_element)

    def global_variables_initializer(self):
        init = tf.global_variables_initializer()
        self.sess.run(init)

    def construct_net(self,is_trained = True):
        batch_norm_params = {"updates_collections":tf.GraphKeys.UPDATE_OPS}
        with slim.arg_scope([slim.batch_norm],is_training=is_trained):
            with slim.arg_scope([slim.conv2d], padding='VALID',
                            weights_initializer=tf.truncated_normal_initializer(stddev=0.1),
                            weights_regularizer=slim.l2_regularizer(0.00001),
                            normalizer_fn=slim.batch_norm,
                            normalizer_params=batch_norm_params,
                            activation_fn=tf.nn.relu):
                net = slim.conv2d(self.input_images,64,[3,3],1,padding='SAME',scope='conv1')
                net = slim.max_pool2d(net, [2, 2], scope='pool2')
                net = slim.conv2d(net,128,[3,3],1,scope='conv3')
                net = slim.max_pool2d(net, [2, 2], scope='pool4')
                net = slim.conv2d(net,256,[3,3],1,scope='conv5')
            
            net = slim.conv2d(net,5,[1,1],1,scope="conv6") # [None,k,k,5]
            net = tf.reduce_mean(net, [1,2], name="global_avg_pooling") # [None, 5]
            digits = tf.nn.softmax(net) # [None, 5]
            '''
            net = slim.flatten(net, scope='flat6')
            net = slim.fully_connected(net, 64, scope='fc7')
            net = slim.dropout(net, self.dropout,is_training=is_trained, scope='dropout8')
            digits = slim.fully_connected(net, 5, scope='fc9',activation_fn=tf.nn.relu)
            '''
        return digits
