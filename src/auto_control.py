#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64

def velocity():
	pub = rospy.Publisher('velocity', Float64, queue_size=10)
	rospy.init_node('auto_control', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		data = Float64(1)
		pub.publish(data)
		rate.sleep()

if __name__ == '__main__':
	try:
		velocity()
	except rospy.ROSInterruptException:
	    rospy.logerr("ROS Interrupt Exception! Just ignore the exception!")
	except rospy.ROSTimeMovedBackwardsException:
	    rospy.logerr("ROS Time Backwards! Just ignore the exception!") 

