#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#20190406 signal recive
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

import time
from math import *

global flag
flag = 1

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
        self.rate = rospy.get_param("~rate", 0.1)
        r = rospy.Rate(self.rate)

        self.nav_command = ""

        #Move and turn commands
        Location_record = [0.000,0.000,0.000,0.000,0.000,0.000,1.000]
        Location_record1 = [0.000,0.000,0.000,0.000,0.000,0.000,1.000]
        speed_forward = 1
        speed_backward = 1
        speed_leftward = 0.5
        speed_rightward = 0.5

        # Initialize the Twist message we will publish.
        while self.nav_command != "quit the program" :

            #rospy.loginfo("Waiting for voice command.")
            #Subscribe to the publisher and assign the nav_command
            rospy.Subscriber('fuck_the_robot', String, self.speech_callback,queue_size=1)
			
            #r.sleep()
			
            if self.nav_command != "" and self.nav_command !="quit the program":
                global flag
                flag = 0
                #set all navigation target pose
                self.locations = dict()
				
                cost_up = sqrt((Location_record[5]-0.000)**2+(Location_record[6]-1.000)**2) #forward direction of the map
                cost_down = sqrt((Location_record[5]-1.000)**2+(Location_record[6]-0.000)**2) #backward direction of the map
                cost_left = sqrt((Location_record[5]-0.700)**2+(Location_record[6]-0.700)**2) #leftward direction of the map
                cost_right = sqrt((Location_record[5]+0.700)**2+(Location_record[6]-0.700)**2) #rightward direction of the map
					
                if self.nav_command == "move forward":
                    rospy.loginfo("move forward")
                    if cost_up<cost_down and cost_up<cost_left and cost_up<cost_right:
                        Location_record[0] += speed_forward
                    elif cost_down<cost_up and cost_down<cost_left and cost_down<cost_right:
                        Location_record[0] -= speed_forward
                    elif cost_left<cost_up and cost_left<cost_down and cost_left<cost_right:
                        Location_record[1] += speed_forward
                    elif cost_right<cost_up and cost_right<cost_down and cost_right<cost_left:
                        Location_record[1] -= speed_forward
                    #rospy.loginfo(Location_record)
                    self.locations[0] = Pose(Point(Location_record[0],Location_record[1],Location_record[2]), Quaternion(Location_record[3],Location_record[4],Location_record[5],Location_record[6]))
                elif self.nav_command == "move backward":
                    if cost_up<cost_down and cost_up<cost_left and cost_up<cost_right:
                        Location_record[0] -= speed_backward
                    elif cost_down<cost_up and cost_down<cost_left and cost_down<cost_right:
                        Location_record[0] += speed_backward
                    elif cost_left<cost_up and cost_left<cost_down and cost_left<cost_right:
                        Location_record[1] -= speed_backward
                    elif cost_right<cost_up and cost_right<cost_down and cost_right<cost_left:
                        Location_record[1] += speed_backward
                    rospy.loginfo("move backward")
                    self.locations[0] = Pose(Point(Location_record[0],Location_record[1],Location_record[2]), Quaternion(Location_record[3],Location_record[4],Location_record[5],Location_record[6]))
                elif self.nav_command == "move leftward":
                    rospy.loginfo("move leftward")
                    if cost_up<cost_down and cost_up<cost_left and cost_up<cost_right:
                        Location_record[1] += speed_leftward
                        Location_record[5:]=[0.700,0.700]
                    elif cost_down<cost_up and cost_down<cost_left and cost_down<cost_right:
                        Location_record[1] -= speed_leftward
                        Location_record[5:]=[-0.700,0.700]
                    elif cost_left<cost_up and cost_left<cost_down and cost_left<cost_right:
                        Location_record[0] -= speed_leftward
                        Location_record[5:]=[1.000,0.000]
                    elif cost_right<cost_up and cost_right<cost_down and cost_right<cost_left:
                        Location_record[0] += speed_leftward
                        Location_record[5:]=[0.000,1.000]
                    self.locations[0] = Pose(Point(Location_record[0],Location_record[1],Location_record[2]), Quaternion(Location_record[3],Location_record[4],Location_record[5],Location_record[6]))
                elif self.nav_command == "move rightward":
                    if cost_up<cost_down and cost_up<cost_left and cost_up<cost_right:
                        Location_record[1] -= speed_rightward
                        Location_record[5:]=[-0.700,0.700]
                    elif cost_down<cost_up and cost_down<cost_left and cost_down<cost_right:
                        Location_record[1] += speed_rightward
                        Location_record[5:]=[0.700,0.700]
                    elif cost_left<cost_up and cost_left<cost_down and cost_left<cost_right:
                        Location_record[0] += speed_rightward
                        Location_record[5:]=[0.000,1.000]
                    elif cost_right<cost_up and cost_right<cost_down and cost_right<cost_left:
                        Location_record[0] -= speed_rightward
                        Location_record[5:]=[1.000,0.000]
                    rospy.loginfo("move rightward")
                    self.locations[0] = Pose(Point(Location_record[0],Location_record[1],Location_record[2]), Quaternion(Location_record[3],Location_record[4],Location_record[5],Location_record[6]))
                elif self.nav_command == "turn left":
                    if cost_up<cost_down and cost_up<cost_left and cost_up<cost_right:
                        Location_record[5:]=[0.700,0.700]
                    elif cost_down<cost_up and cost_down<cost_left and cost_down<cost_right:
                        Location_record[5:]=[-0.700,0.700]
                    elif cost_left<cost_up and cost_left<cost_down and cost_left<cost_right:
                        Location_record[5:]=[1.000,0.000]
                    elif cost_right<cost_up and cost_right<cost_down and cost_right<cost_left:
                        Location_record[5:]=[0.000,1.000]
                    rospy.loginfo("turn left")
                    self.locations[0] = Pose(Point(Location_record[0],Location_record[1],Location_record[2]), Quaternion(Location_record[3],Location_record[4],Location_record[5],Location_record[6]))
                elif self.nav_command == "turn right":
                    if cost_up<cost_down and cost_up<cost_left and cost_up<cost_right:
                        Location_record[5:]=[-0.700,0.700]
                        rospy.loginfo(Location_record)
                    elif cost_down<cost_up and cost_down<cost_left and cost_down<cost_right:
                        Location_record[5:]=[0.700,0.700]
                    elif cost_left<cost_up and cost_left<cost_down and cost_left<cost_right:
                        Location_record[5:]=[0.000,1.000]
                    elif cost_right<cost_up and cost_right<cost_down and cost_right<cost_left:
                        Location_record[5:]=[1.000,0.000]
                    rospy.loginfo("turn right")
                    self.locations[0] = Pose(Point(Location_record[0],Location_record[1],Location_record[2]), Quaternion(Location_record[3],Location_record[4],Location_record[5],Location_record[6]))
                elif self.nav_command == "stop move":
                    rospy.loginfo("stop move")
                    self.locations[0] = Pose(Point(Location_record[0],Location_record[1],Location_record[2]), Quaternion(Location_record[3],Location_record[4],Location_record[5],Location_record[6]))
                elif self.nav_command == "go conference room":
                    rospy.loginfo("go conference room")
                    Location_record = [-5.584, 0.412,0.000,0.000, 0.000, 0.736, 0.677]
                    self.locations[0] = Pose(Point(-5.584, 0.412,0.000), Quaternion(0.000, 0.000, 0.736, 0.677)) # Rm 1516 Conference Rm
                elif self.nav_command == "go prof zhang office":
                    rospy.loginfo("go prof zhang office")
                    Location_record = [-10.162, 3.611,0.000,0.000, 0.000, 0.985, -0.170]
                    self.locations[0] = Pose(Point(-10.162, 3.611,0.000), Quaternion(0.000, 0.000, 0.985, -0.170)) #Prof. Zhang Lin office
                elif self.nav_command == "go prof huang office":
                    rospy.loginfo("go prof huang office")
                    Location_record = [-10.625, 5.195,0.000,0.000, 0.000, 0.993, -0.121]
                    self.locations[0] = Pose(Point(-10.625, 5.195,0.000), Quaternion(0.000, 0.000, 0.993, -0.121))#Prof. Huang office
                elif self.nav_command == "go front door":
                    rospy.loginfo("go front door")
                    Location_record = [8.398, -0.327,0.000,0.000,0.000,-0.714, 0.700]
                    self.locations[0] = Pose(Point(8.398, -0.327,0.000), Quaternion(0.000,0.000,-0.714, 0.700))# Rm 1506 Conference Rm Front Door
                elif self.nav_command == "go main entrance":
                    rospy.loginfo("go main entrance")
                    Location_record = [14.281, 0.227,0.000,0.000,0.000,0.741, 0.672]
                    self.locations[0] = Pose(Point(14.281, 0.227,0.000), Quaternion(0.000,0.000,0.741, 0.672))# Main Entrance
                elif self.nav_command == "go another lab":
                    rospy.loginfo("go another lab")
                    Location_record = [31.516, 4.700,0.000,0.000,0.000,-0.600,0.780]
                    self.locations[0] = Pose(Point(31.516, 4.700,0.000), Quaternion(0.000,0.000,-0.600,0.780))#Rm 1508 Intelligent Transport Lab
                elif self.nav_command == "go back origin":
                    rospy.loginfo("go back origin")
                    Location_record = [0.000,0.000,0.000,0.000,0.000,0.000,1.000]
                    self.locations[0] = Pose(Point(0.000,0.000,0.000), Quaternion(0.000,0.000,0.000,1.000))
                Location_record1 = Location_record

                # Variables to keep track of success rate, running time etc.
                loop_cnt = 0
                n_goals  = 0
                n_successes  = 0
                target_num   = 0
                running_time = 0
                start_time = rospy.Time.now()
                locations_cnt = len(self.locations)
                sequeue = range(0,locations_cnt)
                rospy.loginfo(len(sequeue))
                location = 0
 
                rospy.loginfo("Starting position navigation ")
                # Begin the main loop and run through a sequence of locations

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
                        Location_record = Location_record1
                        self.nav_command = ""
                        global flag
                        flag = 1
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
                
                #rospy.sleep(self.rest_time)
            elif self.nav_command=="quit the program":
                global flag
                flag = 1
            while(flag==0):
                time.sleep(1)
            time.sleep(1)
        rospy.loginfo("program finished.")
 
    def speech_callback(self, msg):
        # Get the motion command from the recognized phrase
        command = msg.data
        # Log the command to the screen
        rospy.loginfo("Command: " + str(command))
        if command == 'move forward':
            self.nav_command = "move forward"   
            return
        elif command == 'move backward':
            self.nav_command = "move backward"   
            return
        elif command == 'move leftward':
            self.nav_command = "move leftward"   
            return
        elif command == 'move rightward':
            self.nav_command = "move rightward"   
            return
        elif command == 'turn left':
            self.nav_command = "turn left"   
            return
        elif command == 'turn right':
            self.nav_command = "turn right"   
            return
        elif command == 'stop move':
            self.nav_command = "stop move"   
            return
        elif command == 'go conference room':
            self.nav_command = "go conference room"   
            return

        elif command == 'go prof zhang office':
            self.nav_command = 'go prof zhang office'
            return

        elif command == 'go prof huang office':
            self.nav_command = 'go prof huang office'
            return

        elif command == 'go front door':
            self.nav_command = 'go front door'
            return

        elif command == 'go main entrance':
            self.nav_command = 'go main entrance'
            return

        elif command == 'go another lab':
            self.nav_command = 'go another lab'
            return

        elif command == 'go back origin':
            self.nav_command = 'go back origin'
            return
			
        elif command == 'quit the program':
            self.nav_command = 'quit the program'
            return

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
