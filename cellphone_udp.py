#!/usr/bin/env python
import rospy
import actionlib
import socket
import time
import tf
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Vector3
from math import sqrt,atan2,cos,sin,pi

count_flag = 0           # Sets the current count of goal
target = 4               # Number of goals
waypoint_y = [0 , 0 , 0   , 4 , 0]
waypoint_x = [2 , 6 , 9 , 11 , 0]
delta =      [0 , 0 , 0   , 80, 0]

msg = ''' USER INTERFACE
----------------------------------
			   8 : move to nxt goal
			   5 : stop
			   2 : skip next goal
		   	   0 : retry goal
'''

def patrol():
	   
	j = count_flag        
	#convert ypr to quarternion
	q = tf.transformations.quaternion_from_euler(0.0, 0.0, delta[j])

	# Get an action client
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	client.wait_for_server()

	# Define the goal
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
	goal.target_pose.pose.position.x = waypoint_x[j]
	goal.target_pose.pose.position.y = waypoint_y[j]
	goal.target_pose.pose.position.z = 0.0
	goal.target_pose.pose.orientation.x = q[0]
	goal.target_pose.pose.orientation.y = q[1]
	goal.target_pose.pose.orientation.z = q[2]
	goal.target_pose.pose.orientation.w = q[3]
	
	# Send the goal
	client.send_goal(goal)
	#client.wait_for_result()

def goal():
	
	host="192.168.43.159"
	port=2055
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host,port))
	
	global target, count_flag
	rate = rospy.Rate(10.0)

	while not rospy.is_shutdown():
		data,addr = sock.recvfrom(1024)
		val = float(data) 
		#val = input(" Enter your choice. ")
		if (val == 8.0):
			print ("recieved 8")
			if (target > 0) :
				patrol()
				count_flag = count_flag + 1
				target = target - 1
			else:
				r = input(" No more goals. Go home ? 1/0")
				count_flag = target 
				patrol()

		elif (val == 2.0):
			print ("recieved 2")
			count_flag = count_flag + 1
			patrol()
			count_flag = count_flag + 1
			target = target - 2

		elif (val == 0.0):
			print ("recieved 0")
			count_flag = count_flag - 1
			target = target + 1
			patrol()
			count_flag = count_flag + 1
			target = target - 1

		elif (val == 5.0):
			print ("recieved 5")
			break


if __name__ == '__main__':
	print(msg)    
	rospy.init_node('goal_sequence', anonymous=True)
	goal()
	rospy.spin()


































