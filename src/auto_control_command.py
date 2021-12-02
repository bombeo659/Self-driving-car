import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64

velocity_pub = rospy.Publisher('/autoware_gazebo/velocity', Float64, queue_size=10)
steeting_angle_pub = rospy.Publisher('/autoware_gazebo/steering_angle', Float64, queue_size=10)

def callback(data):
   print("Received command: ", data.data)
   if data.data == "STOP":
      velocity_pub.publish(Float64(0))
      steeting_angle_pub.publish(Float64(0))

   elif data.data == "TURN_RIGHT":
      start = rospy.get_time()
      duration = rospy.Duration(3)
      while((rospy.get_time() - start) < duration.to_sec()):
         pass

      start = rospy.get_time()
      duration = rospy.Duration(3)
      while((rospy.get_time() - start) < duration.to_sec()):
         velocity_pub.publish(Float64(4))
         steeting_angle_pub.publish(Float64(-2))

      start = rospy.get_time()
      duration = rospy.Duration(2.5)
      while((rospy.get_time() - start) < duration.to_sec()):
         velocity_pub.publish(Float64(4))
         steeting_angle_pub.publish(Float64(0))

      start = rospy.get_time()
      duration = rospy.Duration(4.5)
      while((rospy.get_time() - start) < duration.to_sec()):
         velocity_pub.publish(Float64(4))
         steeting_angle_pub.publish(Float64(-2))

      velocity_pub.publish(Float64(3))
      steeting_angle_pub.publish(Float64(0))

   elif data.data == "TURN_LEFT":
      start = rospy.get_time()
      duration = rospy.Duration(2)
      while((rospy.get_time() - start) < duration.to_sec()):
         pass

      start = rospy.get_time()
      duration = rospy.Duration(3)
      while((rospy.get_time() - start) < duration.to_sec()):
         velocity_pub.publish(Float64(4))
         steeting_angle_pub.publish(Float64(2))

      start = rospy.get_time()
      duration = rospy.Duration(2.5)
      while((rospy.get_time() - start) < duration.to_sec()):
         velocity_pub.publish(Float64(4))
         steeting_angle_pub.publish(Float64(0))

      start = rospy.get_time()
      duration = rospy.Duration(4.5)
      while((rospy.get_time() - start) < duration.to_sec()):
         velocity_pub.publish(Float64(4))
         steeting_angle_pub.publish(Float64(2))

      velocity_pub.publish(Float64(3))
      steeting_angle_pub.publish(Float64(0))

   elif data.data == "GO_STRAIGHT":
      velocity_pub.publish(Float64(2))
      steeting_angle_pub.publish(Float64(0))

   elif data.data == "START":
      velocity_pub.publish(Float64(3))
      steeting_angle_pub.publish(Float64(0))
   else:
      pass

def main():
   rospy.init_node('auto_control_command', anonymous=True)
   rospy.Subscriber("/command_control", String, callback)

   rospy.spin()

if __name__ == '__main__':
   main()