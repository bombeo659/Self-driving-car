import cv2
import numpy as np
import tensorflow as tf
from threading import Thread, Lock


class SignDetector:

	def __init__(self, cv_bridge):

		self.cv_bridge = cv_bridge

		self.image_mutex = Lock()
		self.image = None

		self.model_path = "/home/nqt/catkin_ws/src/Self-driving-car/src/Traffic.h5"
		self.sign_model = tf.keras.models.load_model(self.model_path)

	def callback_image(self, data):
		try:
			image_np = self.cv_bridge.imgmsg_to_cv2(data, "bgr8")

			image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

			self.image_mutex.acquire()
			self.image = image_np.copy()
			self.image_mutex.release()

			self.callback_processing_thread(image_np)

		except CvBridgeError as e:
			print(e)

	def detect_keypoints(self, draw_image):
		draw_image = cv2.medianBlur(draw_image, 5)
		kernel = np.ones((5, 5), np.uint8)
		opening = cv.morphologyEx(draw_image, cv.MORPH_OPEN, kernel)
		# Set our filtering parameters
		# Initialize parameter settiing using cv2.SimpleBlobDetector
		params = cv2.SimpleBlobDetector_Params()

		# Set Area filtering parameters
		params.filterByArea = True
		params.minArea = 100

        # Set Circularity filtering parameters
		params.filterByCircularity = True
		params.minCircularity = 0.9

        # Set Convexity filtering parameters
		params.filterByConvexity = True
		params.minConvexity = 0.2

        # Set inertia filtering parameters
		params.filterByInertia = True
		params.minInertiaRatio = 0.01

		# Create a detector with the parameters
		detector = cv2.SimpleBlobDetector_create(params)

		# Detect blobs
		keypoints = detector.detect(draw_image)

		return keypoints

	def callback_processing_thread(self, proc_image):
	    	# Local copy
		image = None
		#self.image_mutex.acquire()
		if self.image is not None:
			image = self.image.copy()
		#self.image_mutex.release()

		if image is None:
			return

        # ======= Process depth image =======
		keypoints = self.detect_keypoints(proc_image)

		draw = image.copy()
		blank = np.zeros((1, 1))
		draw = cv2.drawKeypoints(draw, keypoints, blank, (0, 255, 0),
                           cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

		rects = []
		crops = []

		img_rgb = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

		for keypoint in keypoints:
			x = keypoint.pt[0]
			y = keypoint.pt[1]
			center = (int(x), int(y))
			radius = int(keypoint.size / 2)

			# Bounding box:
			im_height, im_width, _ = img_rgb.shape
			pad = int(0.4*radius)
			tl_x = max(0, center[0] - radius - pad)
			tl_y = max(0, center[1] - radius - pad)
			br_x = min(im_width-1, tl_x + 2 * radius + pad)
			br_y = min(im_height-1, tl_y + 2 * radius + pad)

			rect = ((tl_x, tl_y), (br_x, br_y))

			crop = img_rgb[tl_y:br_y, tl_x:br_x]

			if crop.shape[0] > 0 and crop.shape[1] > 0:
				crop = cv.resize(crop, (32, 32))
				crop = crop.astype(np.float32) / 255.0
				crops.append(crop)
				rects.append(rect)

		if len(crops) != 0:

			preds = self.sign_model.predict(np.array(crops))
			preds = np.argmax(preds, axis=1)
			preds = preds.tolist()

			for i in range(len(preds)):
				if preds[i] == 14:
					cv2.rectangle(draw, rects[0], rects[1], (0, 0, 255), 3)
					draw = cv2.putText(draw, "Stop Sign", rects[0], cv2.FONT_HERSHEY_SIMPLEX,
                                            0.5, (0, 255, 0), 1, cv2.LINE_AA)
					print("Stop Sign")

				elif preds[i] == 33:
					cv2.rectangle(draw, rects[0], rects[1], (255, 0, 0), 3)
					draw = cv2.putText(draw, "Turn Right Sign", rects[0], cv2.FONT_HERSHEY_SIMPLEX,
                                            0.5, (0, 255, 0), 1, cv2.LINE_AA)
					print("Turn Right Sign")

				elif preds[i] == 34:
					cv2.rectangle(draw, rects[0], rects[1], (0, 0, 255), 3)
					draw = cv2.putText(draw, "Turn Left Sign", rects[0], cv2.FONT_HERSHEY_SIMPLEX,
                                            0.5, (0, 255, 0), 1, cv2.LINE_AA)
					print("Turn Left Sign")

				elif preds[i] == 35:
					cv2.rectangle(draw, rects[0], rects[1], (255, 0, 0), 3)
					draw = cv2.putText(draw, "Go Straight Sign", rects[0], cv2.FONT_HERSHEY_SIMPLEX,
                                            0.5, (0, 255, 0), 1, cv2.LINE_AA)
					print("Go Straight Sign")

			sign_debug_stream_pub.publish(bridge.cv2_to_imgmsg(draw, "bgr8"))
