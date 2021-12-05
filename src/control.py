# from std_msgs.msg import Float64
# import rospy
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge, CvBridgeError
# from lane_detector import LaneDetector
# import cv2

# cv_bridge = CvBridge()

# velocity_pub = rospy.Publisher(
#     '/autoware_gazebo/velocity', Float64, queue_size=10)
# steeting_angle_pub = rospy.Publisher(
#     '/autoware_gazebo/steering_angle', Float64, queue_size=10)


# def image_callback(data):
#     global velocity_pub, steeting_angle_pub
#     try:
#         land_follower = LaneDetector()
#         frame = cv_bridge.imgmsg_to_cv2(data, "bgr8")
#         combo_image = land_follower.follow_lane(frame)
#         if land_follower.curr_steering_angle == 90:
#             data = 0
#         elif land_follower.curr_steering_angle == 89:
#             data = 0.2
#         elif land_follower.curr_steering_angle <= 88:
#             data = 0.5
#         elif land_follower.curr_steering_angle == 91:
#             data = -0.2
#         else:
#             data = -0.5
#         # data = (land_follower.curr_steering_angle - 90)*math.pi/10
#         print(data)
#         velocity_pub.publish(Float64(5))
#         steeting_angle_pub.publish(Float64(data))
#         # print("steering angle is: ", land_follower.curr_steering_angle)
#         cv2.imshow('final', combo_image)
#         cv2.waitKey(2)

#     except CvBridgeError as e:
#         print(e)


# def main():
#     global rate, velocity_pub
#     rospy.init_node('auto_control', anonymous=True)
#     rate = rospy.Rate(50)

#     img_sub = rospy.Subscriber(
#         "/image_raw", Image, image_callback, queue_size=1)

#     rospy.spin()


# if __name__ == '__main__':

# 	try:
# 		main()
# 	except KeyboardInterrupt:
# 		print("Shutting down")




from std_msgs.msg import Float64
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from lane_detector import LaneDetector
import cv2
import time

is_turning = False
time_for_turning = -1
TURNING_TIME = 1
cv_bridge = CvBridge()

velocity_pub = rospy.Publisher(
    '/autoware_gazebo/velocity', Float64, queue_size=10)
steeting_angle_pub = rospy.Publisher(
    '/autoware_gazebo/steering_angle', Float64, queue_size=10)


def image_callback(data):
    global velocity_pub, steeting_angle_pub, is_turning, time_for_turning, TURNING_TIME
    try:
        land_follower = LaneDetector()
        frame = cv_bridge.imgmsg_to_cv2(data, "bgr8")
        combo_image = land_follower.follow_lane(frame)
        if land_follower.curr_steering_angle == 90:
            data = 0
        elif land_follower.curr_steering_angle == 89:
            data = 0.2
            is_turning = True
            time_for_turning = time.time()
        elif land_follower.curr_steering_angle <= 88:
            data = 0.5
            is_turning = True
            time_for_turning = time.time()
        elif land_follower.curr_steering_angle == 91:
            data = -0.2
            is_turning = True
            time_for_turning = time.time()
        else:
            data = -0.5
            is_turning = True
            time_for_turning = time.time()
        # data = (land_follower.curr_steering_angle - 90)*math.pi/
        if is_turning:
            if time_for_turning + TURNING_TIME < time.time():
                is_turning = False
            else:
                print(data)
                velocity_pub.publish(Float64(5))
                steeting_angle_pub.publish(Float64(data))
                # print("steering angle is: ", land_follower.curr_steering_angle)
        cv2.imshow('final', combo_image)
        cv2.waitKey(2)

    except CvBridgeError as e:
        print(e)


def main():
    global rate, velocity_pub
    rospy.init_node('auto_control', anonymous=True)
    rate = rospy.Rate(5)  # 50hz

    img_sub = rospy.Subscriber(
        "/image_raw", Image, image_callback, queue_size=1)

    rospy.spin()


if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		print("Shutting down")
