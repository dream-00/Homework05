#!/usr/bin/env python

"""

    RoboCup@Home Education | oc@robocupathomeedu.org
    navi.py - enable turtlebot to navigate to predefined waypoint location

"""

import rospy, os, sys
from std_msgs.msg import String
from std_msgs.msg import Int32
from sound_play.libsoundplay import SoundClient
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler

original = 0
start = 1

class NavToPoint:
    def __init__(self, script_path):

        rospy.on_shutdown(self.cleanup)

        self.soundhandle = SoundClient()
        rospy.sleep(1)
        self.soundhandle.stopAll()

        self.soundhandle.say('Hello, I am Robort. What can I do for you?')
        rospy.loginfo("Hello, I am Robort. What can I do for you?")
        rospy.sleep(10)
        rospy.Subscriber('/lm_data', String, self.talkback)   

	# Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        rospy.loginfo("Waiting for move_base action server...")

        # Wait for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(120))
        rospy.loginfo("Connected to move base server")

        # A variable to hold the initial pose of the robot to be set by the user in RViz
        initial_pose = PoseWithCovarianceStamped()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)



        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
        	rospy.sleep(1)
            
        rospy.loginfo("Ready to go")
	rospy.sleep(1)
        #self.soundhandle.say('start')
        #rospy.loginfo("start")
        #rospy.sleep(10)

        self.locations = dict()   
             
        # the first point
        A_x = -0.6895
        A_y = 0.6998
        A_theta = 1.000
        
        quaternion = quaternion_from_euler(0.0, 0.0, A_theta)
        self.locations['A'] = Pose(Point(A_x, A_y, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

       #the second point
        B_x = 0.3371
        B_y = -2.0511
        B_theta = 2.000
       
        quaternion = quaternion_from_euler(0.0, 0.0, B_theta)
        self.locations['B'] = Pose(Point(B_x, B_y, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

       #the third point
        C_x =-0.9122
        C_y =-1.4539
        C_theta = 0.500
        
        quaternion = quaternion_from_euler(0.0, 0.0, C_theta)
        self.locations['C'] = Pose(Point(C_x, C_y, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

    def talkback(self, msg):

        #if original==1:
        # Print the recognized words on the screen
            rospy.loginfo(msg.data)
	    self.goal = MoveBaseGoal()
            rospy.loginfo("Starting navigation test")
           
	    self.goal.target_pose.header.frame_id = 'map'
	    self.goal.target_pose.header.stamp = rospy.Time.now()

	    if msg.data.find('PLEASE MOVE TO THE FIRST POINT')>-1:
        	    #rospy.sleep(1)
		    self.soundhandle.say('Going to the first point.')
                    rospy.loginfo('Going to the first point.')

	            self.goal.target_pose.pose = self.locations['A']
  	            self.move_base.send_goal(self.goal)
	            waiting = self.move_base.wait_for_result(rospy.Duration(300))
	            if waiting == 1:
	                rospy.loginfo("Reached point the first point.")
                        self.soundhandle.say('Reached point the first point.')
	                rospy.sleep(2)
		        #rospy.sleep(10) 

	    elif msg.data.find('PLEASE MOVE TO THE SECOND POINT')>-1:
        	    #rospy.sleep(1)
		    self.soundhandle.say('Going to the second point.')
		    rospy.loginfo('Going to the second point.')

	            self.goal.target_pose.pose = self.locations['B']
  	            self.move_base.send_goal(self.goal)
	            waiting = self.move_base.wait_for_result(rospy.Duration(300))
	            if waiting == 1:
	                rospy.loginfo("Reached point the second point.")
                        self.soundhandle.say('Reached point the second point.')
	                rospy.sleep(2)
		        #rospy.sleep(10) 

	    elif msg.data.find('PLEASE MOVE TO THE THIRD POINT')>-1:
        	    #rospy.sleep(1)
		    self.soundhandle.say('Going to the third point.')
                    rospy.loginfo('Going to the third point.')

	            self.goal.target_pose.pose = self.locations['C']
  	            self.move_base.send_goal(self.goal)
	            waiting = self.move_base.wait_for_result(rospy.Duration(300))
	            if waiting == 1:
	                rospy.loginfo("Reached point the third point.")
                        self.soundhandle.say('Reached point the third point.')
	                rospy.sleep(2)
		        #rospy.sleep(10) 
                    
	    else:
                    rospy.sleep(3)
		    self.soundhandle.say('where do you want me go?')
                    rospy.loginfo('where do you want me go?')                    
        



    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose
	#if original == 0:
	self.origin = self.initial_pose.pose.pose
	global original
		#original = 1

    def cleanup(self):
        self.soundhandle.stopAll()
        rospy.loginfo("Shutting down navigation	....")
	self.move_base.cancel_goal()


if __name__=="__main__":
    rospy.init_node('navi_point')
    try:
        NavToPoint(sys.path[0])
        rospy.spin()
    except:
        pass

