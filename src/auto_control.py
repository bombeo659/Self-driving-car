import rospy
import cv2
import numpy as np
import tensorflow as tf
from std_msgs.msg import Float64
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import threading
from threading import Thread, Lock
from PIL import Image as IM

cv_bridge = CvBridge()
image_global = None
image_global_mutex = Lock()
rate = 0
range_image = 0
perios_range_image = 0
count = 0
flag = 0 #0: no info 1: stop 2: left 3: right

model_path = "/home/nqt/catkin_ws/src/Self-driving-car/src/Traffic.h5"
sign_model = tf.keras.models.load_model(model_path)

sign_debug_stream_pub = rospy.Publisher("/sign_detection", Image, queue_size=1)
command_pub = rospy.Publisher("/command_control", String, queue_size=10)

command = ""

def image_debug_callback(data):
	image_debug = cv_bridge.imgmsg_to_cv2(data, "bgr8")
	cv2.imshow("Image Debug", image_debug)
	cv2.waitKey(1)

def image_callback(data):
	global image_global
	try:
		image_global = cv_bridge.imgmsg_to_cv2(data, "bgr8")
		# image_global = cv2.resize(image_global, (400, 200))

		image_np = image_global.copy()
		image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

		thread = threading.Thread(target=callback_processing_thread, args=(image_np,))
		thread.start()

		thread.join()
		# callback_processing_thread(image_np)

	except CvBridgeError as e:
		print(e)

def detect_keypoints(draw_image):	
	# Set our filtering parameters
	# Initialize parameter settiing using cv2.SimpleBlobDetector
	params = cv2.SimpleBlobDetector_Params()
	 
	# Set Area filtering parameters 
	params.filterByArea = True
	params.minArea = 100

    # Set Circularity filtering parameters 
	params.filterByCircularity = True 
	params.minCircularity = 0.87

    # Set Convexity filtering parameters 
	params.filterByConvexity = True
	params.minConvexity = 0.02
        
    # Set inertia filtering parameters 
	params.filterByInertia = True
	params.minInertiaRatio = 0.01
	 
	# Create a detector with the parameters
	detector = cv2.SimpleBlobDetector_create(params)
		 
	# Detect blobs
	keypoints = detector.detect(draw_image)

	return keypoints

def callback_processing_thread(proc_image):
	global image_global, image_global_mutex, sign_model, count, flag, range_image, perios_range_image
	image = None
	# image_global_mutex.acquire()
	if image_global is not None:
		image = image_global.copy()
	# image_global_mutex.release()

	if image is None:
		return
	# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ======= Process depth image =======
	result = 0
	draw = image.copy()
	keypoints = None
	keypoints = detect_keypoints(proc_image)

	if "KeyPoint"  not in str(keypoints):
		pass
	else:
		blank = np.zeros((1, 1))  
		draw = cv2.drawKeypoints(draw, keypoints, blank, (0, 0, 255), 
	                           cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

		rects = []
		crops = []
		
		for keypoint in keypoints:
			x = keypoint.pt[0]
			y = keypoint.pt[1]
			center = (int(x), int(y))
			radius = int(keypoint.size / 2) 
			
			# Bounding box:
			im_height, im_width, _ = draw.shape
			pad = int(0.4*radius)
			tl_x = max(0, center[0] - radius - pad)
			tl_y = max(0, center[1] - radius - pad)
			br_x = min(im_width-1, tl_x + 2 * radius + pad)
			br_y = min(im_height-1, tl_y + 2 * radius + pad)

			rect = ((tl_x, tl_y), (br_x, br_y))
			crop = image[tl_y:br_y, tl_x:br_x]
			range_image = abs(tl_x - tl_y)

			image_fromarray = IM.fromarray(crop, 'RGB')
			resize_image = image_fromarray.resize((30, 30))
			expand_input = np.expand_dims(resize_image, axis=0)
			input_data = np.array(expand_input)
			input_data = input_data/255
			
			preds = sign_model.predict(input_data)
			result = preds.argmax()

	if result == 14:
		print("Stop Sign")
		flag = 1
		cv2.rectangle(draw, rect[0], rect[1], (0, 0, 255), 2)
		draw = cv2.putText(draw, "Stop Sign", rect[0], cv2.FONT_HERSHEY_SIMPLEX ,  
            0.5, (0,255,0), 1, cv2.LINE_AA) 
		if(perios_range_image < range_image):
			perios_range_image = range_image
			count = 0
    
	elif result == 33:
		flag = 2
		cv2.rectangle(draw, rect[0], rect[1], (0, 0, 255), 2)
		draw = cv2.putText(draw, "Turn Right Sign", rect[0], cv2.FONT_HERSHEY_SIMPLEX ,  
            0.5, (0,255,0), 1, cv2.LINE_AA) 
		print("Turn Right Sign")
		if(perios_range_image < range_image):
			perios_range_image = range_image
			count = 0

	elif result == 34:
		flag = 3
		cv2.rectangle(draw, rect[0], rect[1], (0, 0, 255), 2)
		draw = cv2.putText(draw, "Turn Left Sign", rect[0], cv2.FONT_HERSHEY_SIMPLEX ,  
            0.5, (0,255,0), 1, cv2.LINE_AA) 
		print("Turn Left Sign")
		if(perios_range_image < range_image):
			perios_range_image = range_image
			count = 0
    
	elif result == 35:
		flag = 4
		cv2.rectangle(draw, rect[0], rect[1], (0, 0, 255), 2)
		draw = cv2.putText(draw, "Go Straight Sign", rect[0], cv2.FONT_HERSHEY_SIMPLEX ,  
            0.5, (0,255,0), 1, cv2.LINE_AA) 
		print("Go Straight Sign")

	else:
		print("No info")
		if (perios_range_image == range_image):
				count += 1
		
		if count == 10:
			count = 0
			range_image = 0
			perios_range_image = 0
			if flag == 1:
				command_pub.publish("STOP")
			elif flag == 2:
				command_pub.publish("TURN_RIGHT")
			elif flag == 3:
				command_pub.publish("TURN_LEFT")

			flag = 0	
		else:
			pass
	# print(count)	
	sign_debug_stream_pub.publish(cv_bridge.cv2_to_imgmsg(draw, "bgr8"))

def main():
	global rate
	rospy.init_node('auto_control', anonymous=True)
	rate = rospy.Rate(50)

	img_sub = rospy.Subscriber("/image_raw", Image, image_callback, queue_size=1)
	img_debug_sub = rospy.Subscriber("/sign_detection", Image, image_debug_callback, queue_size=1)

	command_pub.publish("START")
	rospy.spin()

if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		print("Shutting down")
