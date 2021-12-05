import cv2
import numpy as np
import tensorflow as tf
from threading import Thread, Lock
import queue
from PIL import Image as IM


class SignDetector():

    def __init__(self, image_queue):
        self.image_queue = image_queue
        self.image_mutex = Lock()
        self.model_path = "/home/nqt/catkin_ws/src/Self-driving-car/src/Traffic.h5"
        self.sign_model = tf.keras.models.load_model(self.model_path)
        self.data = None
        self.sign_detector_thread(self.image_queue)

    def sign_detector_thread(self, image_queue):
    	while True:
            image = image_queue.get()
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if image is None:
                return
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # ======= Process depth image =======
            result = 0
            draw = image.copy()
            keypoints = None
            keypoints = detect_keypoints(gray_image)

            if "KeyPoint" not in str(keypoints):
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

                    preds = self.sign_model.predict(input_data)
                    result = preds.argmax()

            if result == 14:
                print("Stop Sign")
                flag = 1
                cv2.rectangle(draw, rect[0], rect[1], (0, 0, 255), 2)
                draw = cv2.putText(draw, "Stop Sign", rect[0], cv2.FONT_HERSHEY_SIMPLEX,
                                   0.5, (0, 255, 0), 1, cv2.LINE_AA)
                if(perios_range_image < range_image):
                    perios_range_image = range_image
                    count = 0

            elif result == 33:
                flag = 2
                cv2.rectangle(draw, rect[0], rect[1], (0, 0, 255), 2)
                draw = cv2.putText(draw, "Turn Right Sign", rect[0], cv2.FONT_HERSHEY_SIMPLEX,
                                   0.5, (0, 255, 0), 1, cv2.LINE_AA)
                print("Turn Right Sign")
                if(perios_range_image < range_image):
                    perios_range_image = range_image
                    count = 0

            elif result == 34:
                flag = 3
                cv2.rectangle(draw, rect[0], rect[1], (0, 0, 255), 2)
                draw = cv2.putText(draw, "Turn Left Sign", rect[0], cv2.FONT_HERSHEY_SIMPLEX,
                                   0.5, (0, 255, 0), 1, cv2.LINE_AA)
                print("Turn Left Sign")
                if(perios_range_image < range_image):
                    perios_range_image = range_image
                    count = 0

            elif result == 35:
                flag = 4
                cv2.rectangle(draw, rect[0], rect[1], (0, 0, 255), 2)
                draw = cv2.putText(draw, "Go Straight Sign", rect[0], cv2.FONT_HERSHEY_SIMPLEX,
                                   0.5, (0, 255, 0), 1, cv2.LINE_AA)
                print("Go Straight Sign")

            else:
                print("No info")

            self.data = flag


def detect_keypoints(image):
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
    keypoints = detector.detect(image)

    return keypoints
