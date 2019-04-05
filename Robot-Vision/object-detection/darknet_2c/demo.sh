export CUDA_VISIBLE_DEVICES= 1
# ./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg
./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights test_multiface.mp4


