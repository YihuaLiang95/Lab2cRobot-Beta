#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
import get_audio
import sr_main

class offlineAsr(object):
    def __init__(self):
        rospy.init_node('offline_asr_node', anonymous=False)

        self.asrFlag = False
        self.ASRCMD = 1
        self.text_result = ""

        self.asr_topic = "/voice_system/asr_topic"
        self.nlu_topic = "/voice_system/nlu_topic"

        self.asr_topic = rospy.get_param("~asr_topic")
        self.nlu_topic = rospy.get_param("~nlu_topic")

        # Create subscriber and publisher
        rospy.Subscriber(self.asr_topic, Int32, self.topiccallback, queue_size = 1)
        self.pub = rospy.Publisher(self.nlu_topic, String, queue_size=3)
        print('Initialization')
        self.rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            if self.asrFlag:
                print('ASR ')
                self.msg = String()
                self.msg.data = self.text_result
                rospy.loginfo(self.msg.data)
                self.pub.publish(self.msg)
                self.asrFlag = False
            self.rate.sleep()

    def asrProcess(self, filepath = '/home/tbsi2c/record/offline_input.wav'):
        #record an audio to the target path
        get_audio.record(filepath)
        #use the model to recognize the text
        print ("start recognize")
        result = sr_main.speech_recognition(filepath)
        self.asrFlag = True
        #judge whether it is confidence enough
        if result[1] > 0.2:
            return ("".join(result[0][1:]))
            #return the result without control labels
        else:
            return ("LowConfidence")

    def topiccallback(self, msg):
        rospy.loginfo("Now in Offline ASR Callback function...")
        #If the message is to ASR
        if (msg.data == self.ASRCMD):
            self.text_result = self.asrProcess()


    
if __name__ == '__main__':
    try:
        offlineAsr()
        #rospy.spin()
    except rospy.ROSInterruptException:
        rospy.logwarn("Offline ASR exception")
