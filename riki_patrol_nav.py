#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#20190404 signal recive
import rospy
import random
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

import roslib; roslib.load_manifest('rbx1_speech')
from geometry_msgs.msg import Twist
from std_msgs.msg import String,Int32
from math import copysign

class PatrolNav(object):
    def __init__(self,sequeue_para = []): #exam:Pose(Point(1.192,  0.053, 0.000), Quaternion(0.000, 0.000, 0.005, 1.000))
        rospy.init_node('riki_patrol_nav_node', anonymous=False)
        rospy.on_shutdown(self.shutdown)

        # From launch file get parameters
        self.rest_time     = rospy.get_param("~rest_time", 0)
        self.keep_patrol   = rospy.get_param("~keep_patrol",   False)
        self.keep_patrol = False
        self.random_patrol = rospy.get_param("~random_patrol", False)
		self.random_patrol = False
        self.patrol_type   = rospy.get_param("~patrol_type", 0)
		self.patrol_type   = 0
        self.patrol_loop   = rospy.get_param("~patrol_loop", 1)
        self.patrol_time   = rospy.get_param("~patrol_time", 5)	

        # Goal state return values
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED', 'SUCCEEDED', 'ABORTED',
                       'REJECTED', 'PREEMPTING', 'RECALLING', 'RECALLED', 'LOST']		

        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.move_base.wait_for_server(rospy.Duration(5)) #30->5
        rospy.loginfo("Connected to move base server")

        #Frequency to get the voice command. Unit: Herts
        self.rate = rospy.get_param("~rate", 0.5)
        r = rospy.Rate(self.rate)

        self.nav_command = ""
		Nav_command = self.nav_cammand

        # Initialize the Twist message we will publish.
        while self.nav_command != "quit the program" :
            rospy.loginfo("Waiting for voice command.")
			#Subscribe to the publisher and assign the nav_command
            rospy.Subscriber('fuck_the_robot', String, self.speech_callback,queue_size=1)
			#The command changed in the midway
			if Nav_command!= self.command:
			    rospy.signal_shutdown('Quit')
				continue
			#record the command
			Nav_command = self.nav_cammand
			
            r.sleep()
			
            if self.nav_cammand != "" and self.nav_command !="quit the program":
                #set all navigation target pose
                self.locations = dict()
                if self.nav_command == "go conference room":
                    rospy.loginfo("go conference room")
                    self.locations[0] = Pose(Point(-5.584, 0.412,0.000), Quaternion(0.000, 0.000, 0.736, 0.677)) # Rm 1516 Conference Rm
                elif self.nav_command == "go prof zhang office":
                    rospy.loginfo("go prof zhang office")
                    self.locations[0] = Pose(Point(-10.162, 3.611,0.000), Quaternion(0.000, 0.000, 0.985, -0.170)) #Prof. Zhang Lin office
                elif self.nav_command == "go prof huang office":
                    rospy.loginfo("go prof huang office")
                    self.locations[0] = Pose(Point(-10.625, 5.195,0.000), Quaternion(0.000, 0.000, 0.993, -0.121))#Prof. Huang office
				elif self.nav_command == "go front door":
                    rospy.loginfo("go front door")
                    self.locations[0] = Pose(Point(8.398, -0.327,0.000), Quaternion(0.000,0.000,-0.714, 0.700))# Rm 1506 Conference Rm Front Door
				elif self.nav_command == "go main entrance":
                    rospy.loginfo("go main entrance")
                    self.locations[0] = Pose(Point(14.281, 0.227,0.000), Quaternion(0.000,0.000,0.741, 0.672))# Main Entrance
				elif self.nav_command == "go another lab":
                    rospy.loginfo("go another lab")
                    self.locations[0] = Pose(Point(31.516, 4.700,0.000), Quaternion(0.000,0.000,-0.600,0.780))#Rm 1508 Intelligent Transport Lab
				elif self.nav_command == "go back origin":
				    rospy.loginfo("go back origin")
					self.locations[0] = Pose(Point(0.000,0.000,0.000), Quaternion(0.000,0.000,0.000,1.000))

                # Variables to keep track of success rate, running time etc.
                loop_cnt = 0
                n_goals  = 0
                n_successes  = 0
                target_num   = 0
                running_time = 0
                location   = 0
                start_time = rospy.Time.now()
                locations_cnt = len(self.locations)
                sequeue = range(0,locations_cnt)
 
                rospy.loginfo("Starting position navigation ")
                # Begin the main loop and run through a sequence of locations
                while not rospy.is_shutdown():
                    #judge if set keep_patrol is true
                    if self.keep_patrol == False:
                        if self.patrol_type == 0: #use patrol_loop
                            if target_num == locations_cnt:
                                if loop_cnt < self.patrol_loop-1:
                                    target_num = 0
                                    loop_cnt = loop_cnt+ 1
                                    rospy.logwarn("Left patrol loop cnt: %d", self.patrol_loop-loop_cnt)
                                elif loop_cnt == self.patrol_loop-1:
                                    rospy.logwarn("Now patrol loop over, exit...")
                                    #rospy.signal_shutdown('Quit')
                                    break
                    elif self.keep_patrol != False:
                        rospy.loginfo("keep patrol")
                        if self.random_patrol == False:
                            rospy.loginfo("random patrol false")
                            if target_num == locations_cnt:
                                target_num = 0
                        elif self.random_patrol == True:
                            target_num = random.randint(0, locations_cnt-1)
 
                # Get the next location in the current sequence
                location = sequeue[target_num]
                rospy.loginfo("Going to: " + str(location))
                self.send_goal(location)
 
                # Increment the counters
                target_num += 1
                n_goals    += 1
 
                # Allow 5 minutes to get there
                finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))
                # Check for success or failure
                if not finished_within_time:
                    self.move_base.cancel_goal()
                    rospy.logerr("ERROR:Timed out achieving goal")
                else:
                    state = self.move_base.get_state()
                    if state == GoalStatus.SUCCEEDED:
                        n_successes += 1
                        rospy.loginfo("Goal succeeded!")
                    else:
                        rospy.logerr("Goal failed with error code:"+str(goal_states[state]))
 
                # How long have we been running?
                running_time = rospy.Time.now() - start_time
                running_time = running_time.secs/60.0
 
                # Print a summary success/failure and time elapsed
                rospy.loginfo("Success so far: " + str(n_successes) + "/" +
                              str(n_goals) + " = " +
                              str(100 * n_successes/n_goals) + "%")
                rospy.loginfo("Running time: " + str(self.trunc(running_time, 1)) + " min")
                rospy.sleep(self.rest_time)
 
                if self.keep_patrol == False and self.patrol_type == 1: #use patrol_time
                    if running_time >= self.patrol_time:
                        rospy.logwarn("Now reach patrol_time, back to original position...")
                        self.send_goal(0)
                        rospy.signal_shutdown('Quit')
 
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
			
        elif command == 'quit the program'
		    self.nav_command = 'quit the program'
        else:
            return

    def send_goal(self, locate):
        # Set up the next goal location
        self.goal = MoveBaseGoal()
        self.goal.target_pose.pose = self.locations[locate]
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.header.stamp = rospy.Time.now()
        self.move_base.send_goal(self.goal) #send goal to move_base

    def trunc(self, f, n):
        # Truncates/pads a float f to n decimal places without rounding
        slen = len('%.*f' % (n, f))
        return float(str(f)[:slen])

    def shutdown(self):
        rospy.logwarn("Stopping the patrol...")

if __name__ == '__main__':
    try:
        PatrolNav()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.logwarn("patrol navigation exception finished.")
