import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64

velocity_pub = rospy.Publisher('/autoware_gazebo/velocity', Float64, queue_size=10)
steeting_angle_pub = rospy.Publisher('/autoware_gazebo/steering_angle', Float64, queue_size=10)
def callback(data):
   rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def listener():

   rospy.init_node('listener', anonymous=True)
   rospy.Subscriber("/command_control", String, callback)

   rospy.spin()

if __name__ == '__main__':
   listener()