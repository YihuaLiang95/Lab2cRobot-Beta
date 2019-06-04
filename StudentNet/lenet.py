import tensorflow as tf
import tensorflow.contrib.slim as slim
import config as cfg

class Lenet:
    def __init__(self):
        self.input_images = tf.placeholder(tf.float32, [None, 224, 224, 3])
        self.raw_input_label = tf.placeholder(tf.float32, [None, 3])
        self.input_labels = tf.cast(self.raw_input_label,tf.int32)
        self.dropout = cfg.KEEP_PROB

        with tf.variable_scope("Lenet") as scope:
            self.train_digits = self.construct_net(True)
            scope.reuse_variables()
            self.pred_digits = self.construct_net(False)

        # self.prediction = tf.cast(tf.argmax(self.pred_digits, 1), dtype = tf.int32)
        self.correct_prediction = tf.equal(tf.argmax(self.pred_digits, 1), tf.argmax(self.input_labels, 1))
        self.train_accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, "float"))


        self.loss = tf.losses.softmax_cross_entropy( self.input_labels, self.train_digits)
        self.lr = cfg.LEARNING_RATE
        self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)



    def construct_net(self,is_trained = True):
        with slim.arg_scope([slim.conv2d], padding='VALID',
                            weights_initializer=tf.truncated_normal_initializer(stddev=0.01),
                            weights_regularizer=slim.l2_regularizer(0.0005)):
            net = slim.conv2d(self.input_images,6,[3,3],1,padding='SAME',scope='conv1')
            net = slim.max_pool2d(net, [2, 2], scope='pool2')
            net = slim.conv2d(net,16,[3,3],1,scope='conv3')
            net = slim.max_pool2d(net, [2, 2], scope='pool4')
            net = slim.conv2d(net,32,[3,3],1,scope='conv5')
            net = slim.flatten(net, scope='flat6')
            net = slim.fully_connected(net, 84, scope='fc7')
            net = slim.dropout(net, self.dropout,is_training=is_trained, scope='dropout8')
            digits = slim.fully_connected(net, 3, scope='fc9')
        return digits