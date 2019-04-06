# -*- coding: utf-8 -*-
import tensorflow as tf
import os
import shutil
import pdb
from tensorflow.python.framework import graph_util


# --------------------------------------------------------
def test_pb_save_and_load():
	pb_file_path = "model/pb_model"
	# build graph
	with tf.Session() as sess:
		x = tf.placeholder(tf.int32,name="x")
		y = tf.placeholder(tf.int32,name="y")
		b = tf.Variable(1,name="b")
		xy = tf.multiply(x,y)
		op = tf.add(xy,b,name="output")
		sess.run(tf.global_variables_initializer())
		feed_dict = {x:10,y:3}
		print(sess.run(op,feed_dict))
		# save pb model
		print("save model.")
		save_pb_model(sess,pb_file_path)

	# load pb model
	print("load model.")
	sess = tf.Session(graph=tf.Graph())
	sess = read_pb_model(sess,pb_file_path)
	sess.close()

def save_pb_model(sess,pb_file_path):
	# constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph_def, ["output"])
	# with tf.gfile.FastGFile(os.path.join(pb_file_path,"model.pb"),mode="wb") as f:
	# 	f.write(constant_graph.SerializeToString())
	if os.path.exists(pb_file_path):
		shutil.rmtree(pb_file_path)

	builder = tf.saved_model.builder.SavedModelBuilder(os.path.join(pb_file_path,"pb_model"))
	builder.add_meta_graph_and_variables(sess,tags=["test_model"])
	builder.save()

def read_pb_model(sess,pb_file_path):
	tf.saved_model.loader.load(sess,
		tags=["test_model"], # this tag must be same as graph of saved model.
		export_dir = os.path.join(pb_file_path,"pb_model")
		)
	# sess.run(tf.global_variables_initializer())

	x = sess.graph.get_tensor_by_name("x:0")
	y = sess.graph.get_tensor_by_name("y:0")
	op = sess.graph.get_tensor_by_name("output:0")
	ret  = sess.run(op,feed_dict={x:5,y:10})
	print(ret)
	return sess

# --------------------------------------------------------
def test_signature_save_and_load():
	"use tf.saved_model.signature_def_utils.build_signature_def to save model."
	"ref to: https://blog.csdn.net/thriving_fcl/article/details/75213361"

	sign_file_path = "model/sign_model"
	# build graph
	with tf.Session() as sess:
		x = tf.placeholder(tf.int32,name="x")
		b = tf.Variable(1,name="b")
		y = tf.add(x,b,name="output")
		sess.run(tf.global_variables_initializer())
		feed_dict = {x:10}
		print(sess.run(y,feed_dict))

		# save model
		save_sign_model(sess,sign_file_path,x,y)

	# load model
	sess = tf.Session()
	inputs,outputs = load_sign_model(sess,sign_file_path)
	res = sess.run(outputs,feed_dict={inputs:12345})
	print("result:",res)


def save_sign_model(sess,save_model_dir,inputs,outputs):
	x = inputs
	y = outputs
	if os.path.exists(save_model_dir):
		shutil.rmtree(save_model_dir)

	builder = tf.saved_model.builder.SavedModelBuilder(save_model_dir)
	# x is input tensor, keep_prob is prob of dropout
	inputs = {"input_x":tf.saved_model.utils.build_tensor_info(x)}
	# inputs = {"input_x":tf.saved_model.utils.build_tensor_info(x),
	# 	"keep_prob":tf.saved_model.utils.build_tensor_info(keep_prob)}

	# y is output tensor
	outputs = {"output": tf.saved_model.utils.build_tensor_info(y)}

	signature = tf.saved_model.signature_def_utils.build_signature_def(
		inputs = inputs,
		outputs = outputs,
		method_name="test_signature_save_and_load",
		)

	builder.add_meta_graph_and_variables(sess,
		tags=["test_signature_model"],
		signature_def_map = {"test_signature":signature},
		)

	builder.save()

def load_sign_model(sess,save_model_dir):
	input_key = "input_x"
	output_key="output"
	signature_key = "test_signature"
	meta_graph_def = tf.saved_model.loader.load(sess,
		tags=["test_signature_model"],
		export_dir=save_model_dir,
		)
	# obtain SignatureDef object from meta_graph_def
	signature = meta_graph_def.signature_def

	x_tensor_name = signature[signature_key].inputs[input_key].name
	y_tensor_name = signature[signature_key].outputs[output_key].name

	# obtain tensor and inference
	x = sess.graph.get_tensor_by_name(x_tensor_name)
	y = sess.graph.get_tensor_by_name(y_tensor_name)

	return x,y

def main():
	test_pb_save_and_load()
	test_signature_save_and_load()


if __name__ == '__main__':
	main()