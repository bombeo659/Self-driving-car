import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


bridge = CvBridge()

def imgCallback(data):
	cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
	# width 800, height 

	gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
	
	cntr = 1
	cntr += 1
	savingName = str(cntr) + ".jpg"
	
	cv2.imwrite(savingName, cv_image)

	cv2.imshow("Raw Image", gray_image)
	
	cv2.waitKey(3)

def main():
	print("Hey Universe!")
	rospy.init_node('my_planner_node')
	img_sub = rospy.Subscriber("/image_raw", Image, imgCallback)
	rospy.spin()

if __name__ == "__main__":
	main()
