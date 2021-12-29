from std_msgs.msg import Float64
from std_msgs.msg import String
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import math
import tensorflow as tf
from threading import Thread, Lock
import queue
from PIL import Image as IM


image_global = None
image_global_mutex = Lock()
rate = 0
range_image = 0
count = 0
flag = 0  # 0: no info 1: stop 2: left 3: right
command_sign = 0

model_path = "/home/nqt/catkin_ws/src/Self-driving-car/src/Traffic.h5"
sign_model = tf.keras.models.load_model(model_path)
command_pub = rospy.Publisher("/command_control", String, queue_size=1)


def callback_processing_thread(proc_image):
    global image_global, image_global_mutex, sign_model, count, flag, range_image
    image = None
    # image_global_mutex.acquire()
    if image_global is not None:
        image = image_global.copy()
        # image_global_mutex.release()

    if image is None:
        return
    # ======= Process depth image =======
    result = 0
    draw = image.copy()
    # cv2.imshow("daw", draw)
    # cv2.waitKey(0)
    keypoints = None
    keypoints = detect_keypoints(proc_image)

    input_data_list = []
    rects = []
    range_images = []

    if "KeyPoint" not in str(keypoints):
        pass
    else:
        blank = np.zeros((1, 1))
        draw = cv2.drawKeypoints(draw, keypoints, blank, (0, 0, 255),
                                 cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

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

            input_data_list.append(input_data)
            rects.append(rect)
            range_images.append(range_image)

    if len(range_images) != 0 and max(range_images) > 165 and len(input_data_list) != 0:

        preds = sign_model.predict(input_data_list)
        preds = np.argmax(preds, axis=1)
        preds = preds.tolist()

        for i in range(len(preds)):
            if preds[i] == 14:
                flag = 1
                cv2.rectangle(draw, rects[i][0], rects[i][1], (0, 0, 255), 2)
                draw = cv2.putText(draw, "Stop Sign", rects[i][0], cv2.FONT_HERSHEY_SIMPLEX,
                                   0.5, (0, 255, 0), 1, cv2.LINE_AA)

            elif preds[i] == 33:
                flag = 2
                cv2.rectangle(draw, rects[i][0], rects[i][1], (0, 0, 255), 2)
                draw = cv2.putText(draw, "Turn Right Sign", rects[i][0], cv2.FONT_HERSHEY_SIMPLEX,
                                   0.5, (0, 255, 0), 1, cv2.LINE_AA)

            elif preds[i] == 34:
                flag = 3
                cv2.rectangle(draw, rects[i][0], rects[i][1], (0, 0, 255), 2)
                draw = cv2.putText(draw, "Turn Left Sign", rects[i][0], cv2.FONT_HERSHEY_SIMPLEX,
                                   0.5, (0, 255, 0), 1, cv2.LINE_AA)

            elif preds[i] == 35:
                flag = 4
                cv2.rectangle(draw, rects[i][0], rects[i][1], (0, 0, 255), 2)
                draw = cv2.putText(draw, "Go Straight Sign", rects[i][0], cv2.FONT_HERSHEY_SIMPLEX,
                                   0.5, (0, 255, 0), 1, cv2.LINE_AA)
            else:
                pass

    if flag == 1:
        command_pub.publish("STOP")
    elif flag == 2:
        command_pub.publish("TURN_RIGHT")
    elif flag == 3:
        command_pub.publish("TURN_LEFT")
    elif flag == 4:
        command_pub.publish("GO_STRAIGHT")
    else:
        pass
    flag = 0
    input_data_list.clear()
    rects.clear()
    range_images.clear()

    cv2.imshow("Sign Detector", draw)
    cv2.waitKey(2)


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


_SHOW_IMAGE = False


class LaneDetector():
    def __init__(self):
        self.curr_steering_angle = 90
        self.line = 0

    def follow_lane(self, frame):
        # Main entry point of the lane follower
        show_image("orig", frame)

        lane_lines, frame = detect_lane(frame)
        self.line = len(lane_lines)
        final_frame = self.steer(frame, lane_lines)

        return final_frame

    def steer(self, frame, lane_lines):
        if len(lane_lines) == 0:
            return frame
        self.curr_steering_angle = compute_steering_angle(frame, lane_lines)

        curr_heading_image = display_heading_line(
            frame, self.curr_steering_angle)
        show_image("heading", curr_heading_image)

        return curr_heading_image


def detect_lane(frame):
    edges = detect_edges(frame)
    show_image('edges', edges)

    cropped_edges = region_of_interest(edges)
    show_image('edges cropped', cropped_edges)

    line_segments = detect_line_segments(cropped_edges)
    line_segment_image = display_lines(frame, line_segments)
    show_image("line segments", line_segment_image)

    lane_lines = average_slope_intercept(frame, line_segments)
    lane_lines_image = display_lines(frame, lane_lines)
    show_image("lane lines", lane_lines_image)

    return lane_lines, lane_lines_image


def detect_edges(frame):
    # Color space conversion
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecting white colors
    mask_white = cv2.inRange(img_gray, 200, 255)

    # mask = cv2.bitwise_and(img_gray, mask_white)

    # detect edges
    edges = cv2.Canny(mask_white, 200, 400)

    return edges


def region_of_interest(canny):
    ysize = canny.shape[0]
    xsize = canny.shape[1]
    # Smoothing for removing noise
    gray_blur = cv2.GaussianBlur(canny, (5, 5), 0)

    # Region of Interest Extraction
    mask_roi = np.zeros_like(gray_blur)
    left_bottom = [0, ysize]
    right_bottom = [xsize, ysize]
    apex_left = [(0), (3*ysize/4)]
    apex_right = [(xsize), (3*ysize/4)]
    mask_color = 255
    roi_corners = np.array(
        [[left_bottom, apex_left, apex_right, right_bottom]], dtype=np.int32)
    cv2.fillPoly(mask_roi, roi_corners, mask_color)
    masked_image = cv2.bitwise_and(gray_blur, mask_roi)

    return masked_image


def detect_line_segments(cropped_edges):
    # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
    rho = 1  # precision in pixel, i.e. 1 pixel
    angle = np.pi / 180  # degree in radian, i.e. 1 degree
    min_threshold = 10  # minimal of votes
    line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, np.array([]), minLineLength=10,
                                    maxLineGap=4)

    return line_segments


def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    if line_segments is None:
        return lane_lines

    height, width, _ = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1/3
    # left lane line segment should be on left 2/3 of the screen
    left_region_boundary = width * (1 - boundary)
    # right lane line segment should be on left 1/3 of the screen
    right_region_boundary = width * boundary

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))

    return lane_lines


def compute_steering_angle(frame, lane_lines):
    """ Find the steering angle based on lane line coordinate
        We assume that camera is calibrated to point to dead center
    """
    if len(lane_lines) == 0:
        return -90

    height, width, _ = frame.shape
    if len(lane_lines) == 1:
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
    else:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        # 0.0 means car pointing to center, -0.03: car is centered to left, +0.03 means car pointing to right
        camera_mid_offset_percent = 0.02
        mid = int(width / 2 * (1 + camera_mid_offset_percent))
        x_offset = (left_x2 + right_x2) / 2 - mid

    # find the steering angle, which is angle between navigation direction to end of center line
    y_offset = int(3*height / 4)

    # angle (in radian) to center vertical line
    angle_to_mid_radian = math.atan(x_offset / y_offset)
    # angle (in degrees) to center vertical line
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi*0.6)
    # this is the steering angle needed by picar front wheel
    steering_angle = angle_to_mid_deg + 90

    return steering_angle


def display_lines(frame, lines, line_color=(0, 255, 0), line_width=5, line_hight=4):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2),
                         line_color, line_width, line_hight)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image


def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=5, line_hight=4):
    heading_image = np.zeros_like(frame)
    height, width, _ = frame.shape

    steering_angle_radian = steering_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - 2*height/3/math.tan(steering_angle_radian))
    y2 = int(3*height/4)

    cv2.line(heading_image, (x1, y1), (x2, y2),
             line_color, line_width, line_hight)
    heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)

    return heading_image


def length_of_line_segment(line):
    x1, y1, x2, y2 = line
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def show_image(title, frame, show=_SHOW_IMAGE):
    if show:
        cv2.imshow(title, frame)
        # cv2.waitKey(0)


def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 3 / 4)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]


cv_bridge = CvBridge()

velocity_pub = rospy.Publisher(
    '/autoware_gazebo/velocity', Float64, queue_size=5)
steeting_angle_pub = rospy.Publisher(
    '/autoware_gazebo/steering_angle', Float64, queue_size=5)

steeting_angle = []
angle_rad = 0
speed = 0


def lane_callback(data):
    global velocity_pub, steeting_angle_pub, angle_rad, command_sign, speed
    try:
        land_follower = LaneDetector()
        frame = cv_bridge.imgmsg_to_cv2(data, "bgr8")
        combo_image = land_follower.follow_lane(frame)
        if command_sign == 0:
            steeting_angle.append(land_follower.curr_steering_angle)
            if(land_follower.line == 2):
                speed = 10
            elif(land_follower.line == 1):
                speed = 5
            elif(land_follower.line == 0):
                speed = 0
            else:
                pass
        elif command_sign == 1:
            speed = 0
        else:
            pass

        if(len(steeting_angle) == 10):
            data = np.average(steeting_angle, axis=None)
            angle_rad = round(((90 - data)/180 * math.pi * 1.2), 3)
            if(land_follower.line == 1):
                angle_rad = round(angle_rad + 0.5*angle_rad, 3)
            steeting_angle.clear()

            velocity_pub.publish(Float64(speed))
            steeting_angle_pub.publish(Float64(angle_rad))
            print("Info: ", speed, angle_rad)

        cv2.imshow('Lane Detector', combo_image)
        cv2.waitKey(2)

    except CvBridgeError as e:
        print(e)


def sign_callback(data):
    global image_global
    try:
        image_global = cv_bridge.imgmsg_to_cv2(data, "bgr8")
        image_np = image_global.copy()
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

        callback_processing_thread(image_np)

    except CvBridgeError as e:
        print(e)


def command_sign_callback(data):
    global command_sign, velocity_pub, steeting_angle_pub

    print(data.data)
    if data.data == "STOP":
        command_sign = 1
        velocity_pub.publish(Float64(0))
        steeting_angle_pub.publish(Float64(0))

    elif data.data == "TURN_RIGHT":
        command_sign = 2
        velocity_pub.publish(Float64(13))
        start = rospy.get_time()
        duration = rospy.Duration(0.175)
        while((rospy.get_time() - start) < duration.to_sec()):
            steeting_angle_pub.publish(Float64(-0.55))
        velocity_pub.publish(Float64(0))
        command_sign = 0

    elif data.data == "TURN_LEFT":
        command_sign = 3
        velocity_pub.publish(Float64(13))
        start = rospy.get_time()
        duration = rospy.Duration(0.175)
        while((rospy.get_time() - start) < duration.to_sec()):
            steeting_angle_pub.publish(Float64(0.55))
        velocity_pub.publish(Float64(0))
        command_sign = 0

    elif data.data == "GO_STRAIGH":
        command_sign = 4
        velocity_pub.publish(Float64(10))
    else:
        command_sign = 0


def main():
    global rate, velocity_pub
    rospy.init_node('control', anonymous=True)
    rate = rospy.Rate(50)

    lane_sub = rospy.Subscriber(
        "/image_raw", Image, lane_callback, queue_size=1)
    sign_sub = rospy.Subscriber(
        "/image_raw", Image, sign_callback, queue_size=1)
    rospy.Subscriber("/command_control", String, command_sign_callback)
    rospy.spin()


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
