#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#zelong yang, 20190330

import roslib; roslib.load_manifest('rbx1_speech')
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String,Int32
from math import copysign

import riki_patrol_nav_func

#six points:
"""
[
[0.450,  0.024, 0.000,0.000, 0.000, 0.035, 0.999],
[0.900,  0.048, 0.000,0.000, 0.000, 0.035, 0.999],
[1.350,  0.072, 0.000,0.000, 0.000, 0.035, 0.999],
[1.800, 0.096, 0.000,0.000, 0.000, 0.035, 0.999],
[2.250,  0.120, 0.000,0.000, 0.000, 0.035, 0.999],
[2.700,  0.144, 0.000,0.000, 0.000, 0.035, 0.999],
[2.700,  0.144, 0.000,0.000, 0.000, -0.563, 0.826],
[2.700,  0.144, 0.000,0.000, 0.000, 0.035, 0.999]]
"""
"""
可行版本：
[
[3.000,  0.000, 0.000,0.000, 0.000, -0.700, 0.700],
[3.000,  -0.500, 0.000,0.000, 0.000, 0.000, 1.000],
[6.000,  -0.500, 0.000,0.000, 0.000, -0.700, 0.700],
[6.000,  -2.350, 0.000,0.000, 0.000, 1.000, 0.000], #y -2.30->-2.35
[3.550,-2.350,0.000,0.000,0.000,-0.700,0.700],#3.6跟桌子太近，3.545撞椅子，3.55可以但離桌子有點近，也有可能撞桌子
[3.550, -8.700,0.000,0.000,0.000,-0.700,0.700],#-8.75離白板太近
[-0.500, -8.700,0.000,0.000,0.000,1.000,0.000]]
"""


class VoiceNav:
    def __init__(self):
        rospy.init_node('voice_nav')
        rospy.on_shutdown(self.cleanup)

        # Set a number of parameters affecting the robot's speed

        self.rate = rospy.get_param("~rate", 5)
        self.nav_command = ""
        r = rospy.Rate(self.rate)
         
        # A flag to determine whether or not voice control is paused
        self.paused = False

        # Initialize the Twist message we will publish.
        while self.nav_command == "" :
            rospy.Subscriber('fuck_the_robot', String, self.speech_callback)
            r.sleep()

        self.cmd_vel = Twist()
        self.cmd_vel_pub = rospy.Publisher('cmd_vel',Twist)

        # A mapping from keywords or phrases to commands
        rospy.loginfo("Ready to receive voice commands")
        
        # We have to keep publishing the cmd_vel message if we want the robot to keep moving.
        """
        while not rospy.is_shutdown():
            self.cmd_vel_pub.publish(self.cmd_vel)
            r.sleep()                       
        """
    def speech_callback(self, msg):

        # Get the motion command from the recognized phrase
        command = msg.data
        # Log the command to the screen
        rospy.loginfo("Command: " + str(command))
        
        if command == 'go professor':
            self.nav_command = "go professor"   
            print "here"    
            return

        elif command == 'back to lap':
            self.nav_command = 'back to lap'
            return
        else:
            return

    def get_command(self):
        return self.nav_command
    def cleanup(self):
        # When shutting down be sure to stop the robot!
        twist = Twist()
        self.cmd_vel_pub.publish(twist)
        rospy.sleep(1)
if __name__ == '__main__':
    try:
        nav_class = VoiceNav()
        print("finish")
        nav = nav_class.get_command()

        if nav == 'go professor':
            print("hello")
            riki_patrol_nav_func.PatrolNav([
#[-5.584, 0.412,0.000,   0.000, 0.000, 0.736, 0.677],# Rm 1516 Conference Rm
#[-10.162, 3.611,0.000,  0.000, 0.000, 0.985, -0.170],#Zhang Lin office
#[-10.625, 5.195,0.000,  0.000, 0.000, 0.993, -0.121],#Huang ShaoLun office
#[8.398, -0.327,0.000,   0.000,0.000,-0.714, 0.700],# Rm 1506 Conference Rm Front Door
#[14.281, 0.227,0.000,   0.000,0.000,0.741, 0.672],# Main Entrance
#[31.516, 4.700,0.000,   0.000,0.000,-0.600,0.780]#Rm 1508 Intelligent Transport Lab
[0.450,  0.024, 0.000,0.000, 0.000, 0.035, 0.999],
[0.900,  0.048, 0.000,0.000, 0.000, 0.035, 0.999]
])
        elif nav == 'back to lap':
            riki_patrol_nav_func.PatrolNav([[0.450,  0.024, 0.000,0.000, 0.000, 0.035, 0.999]])
        rospy.spin()
        riki_patrol_nav_func.rospy.spin()
    except riki_patrol_nav_func.rospy.ROSInterruptException:
        riki_patrol_nav_func.rospy.logwarn("patrol navigation exception finished.")
