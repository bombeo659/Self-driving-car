import numpy as np
import cv2
from sklearn import linear_model
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import roslib

bridge = CvBridge()

#Compute slope of the line when points are given
def compute_slope(x1,y1,x2,y2):
    a = 0
    if x2!=x1:
        a = (y2-y1)/(x2-x1)
    return a

def extract_lane(road_lines):
    left_lane = []
    right_lane = []
    left_slope = []
    right_slope = []

    if road_lines is not None:
        for x in range(0, len(road_lines)):
            for x1,y1,x2,y2 in road_lines[x]:
                slope = compute_slope(x1,y1,x2,y2)
                # print(slope)
                if (slope < 0):
                    left_lane.append(road_lines[x])
                    left_slope.append(slope)
                else:
                    if (slope > 0):
                        right_lane.append(road_lines[x])
                        right_slope.append(slope)
                
    return left_lane, right_lane , left_slope, right_slope
    


def print_lanes(left_lane, right_lane, left_slope, right_slope):
    #print("Left lane")
    for x in range(0, len(left_lane)):
        print(left_lane[x], left_slope[x])
    #print("Right lane")
    for x in range(0, len(right_lane)):
        print(right_lane[x], right_slope[x])

def split_append(left_lane, right_lane):
    left_lane_sa = []
    right_lane_sa = []
    
    for x in range(0, len(left_lane)):
        for x1,y1,x2,y2 in left_lane[x]:
            left_lane_sa.append([x1, y1])
            left_lane_sa.append([x2, y2])

    for y in range(0, len(right_lane)):
        for x1,y1,x2,y2 in right_lane[y]:
            right_lane_sa.append([x1,y1])
            right_lane_sa.append([x2,y2])
            
    left_lane_sa = np.array(left_lane_sa)
    right_lane_sa = np.array(right_lane_sa)
    left_lane_sa,right_lane_sa = sort(left_lane_sa,right_lane_sa)
    return left_lane_sa,right_lane_sa

#This fucntion prints the lanes after the frame is split and merged
def print_lanes_sa(left_lane_sa, right_lane_sa):
    #print("Left lane")
    for x in range(0, len(left_lane_sa)):
        print(left_lane_sa[x])
    #print("Right lane")
    for x in range(0, len(right_lane_sa)):
        print(right_lane_sa[x])          

def sort(left_lane_sa,right_lane_sa):
    left_lane_sa = left_lane_sa[np.argsort(left_lane_sa[:, 0])]
    right_lane_sa = right_lane_sa[np.argsort(right_lane_sa[:, 0])]

    return left_lane_sa, right_lane_sa


def draw_lanes(left_lane_sa, right_lane_sa,frame):
    left_lane_x = []
    left_lane_y = []
    right_lane_x = []
    right_lane_y = []

    for x1,y1 in left_lane_sa:
        left_lane_x.append([x1])
        left_lane_y.append([y1])

    for x1,y1 in right_lane_sa:
        right_lane_x.append([x1])
        right_lane_y.append([y1])

    left_ransac_x = np.array(left_lane_x)
    left_ransac_y = np.array(left_lane_y)

    right_ransac_x = np.array(right_lane_x)
    right_ransac_y = np.array(right_lane_y)

        
    left_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
    #print(left_ransac_x,left_ransac_y,len(left_ransac_x),len(left_ransac_y), left_ransac_x.shape )
    left_ransac.fit(left_ransac_x, left_ransac_y)
    slope_left = left_ransac.estimator_.coef_
    intercept_left = left_ransac.estimator_.intercept_

    right_ransac = linear_model.RANSACRegressor()
    right_ransac.fit(right_ransac_x, right_ransac_y)
    slope_right = right_ransac.estimator_.coef_
    intercept_right = right_ransac.estimator_.intercept_

    ysize = frame.shape[0]
    xsize = frame.shape[1]
    y_limit_low = int(0.95*ysize)
    y_limit_high = int(0.65*ysize)

    #Coordinates for point 1(Bottom Left)
    y_1 = ysize
    x_1 = int((y_1-intercept_left)/slope_left)

    #Coordinates for point 2(Bottom Left)
    y_2 = y_limit_high
    x_2 = int((y_2-intercept_left)/slope_left)

    #Coordinates for point 3(Bottom Left)
    y_3 = y_limit_high
    x_3 = int((y_3-intercept_right)/slope_right)
    
    #Coordinates for point 4(Bottom Right)
    y_4 = ysize
    x_4 = int((y_4-intercept_right)/slope_right)

    cv2.line(frame,(x_1,y_1),(x_2,y_2),(0,255,255),3)
    cv2.line(frame,(x_3,y_3),(x_4,y_4),(0,255,255),3)
    pts = np.array([[x_1, y_1], [x_2, y_2], [x_3, y_3], [x_4, y_4]])
    mask_color = (255,255,0)
    frame_copy = frame.copy()
    cv2.fillPoly(frame_copy, np.int32([pts]), mask_color)
    opacity = 0.4
    cv2.addWeighted(frame_copy,opacity,frame,1-opacity,0,frame)


def imgCallback(data):
    frame = bridge.imgmsg_to_cv2(data, "bgr8")
#frame = cv2.imread('image_17.png')

    # Color space conversion
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2. cvtColor(frame, cv2.COLOR_BGR2HLS)
    ysize = img_gray.shape[0]
    xsize = img_gray.shape[1]

    #Detecting white colors
    mask_white = cv2.inRange(img_gray, 200, 255)

    mask_onimage = cv2.bitwise_and(img_gray, mask_white)

    #Smoothing for removing noise
    gray_blur = cv2.GaussianBlur(mask_onimage, (5,5), 0)

    #Region of Interest Extraction
    mask_roi = np.zeros(img_gray.shape, dtype=np.uint8) 
    left_bottom = [0, ysize]
    right_bottom = [xsize-0, ysize]
    apex_left = [((xsize/2)-50), ((ysize/2)+50)]
    apex_right = [((xsize/2)+50), ((ysize/2)+50)]
    mask_color = 255
    roi_corners = np.array([[left_bottom, apex_left, apex_right, right_bottom]], dtype=np.int32)
    cv2.fillPoly(mask_roi, roi_corners, mask_color)
    image_roi = cv2.bitwise_and(gray_blur, mask_roi)

    #Thresholding before edge
    ret, img_postthresh = cv2.threshold(image_roi, 50, 255, cv2.THRESH_BINARY)

    #Use canny edge detection
    edge_low = 50
    edge_high = 200
    img_edge = cv2.Canny(img_postthresh, edge_low, edge_high)

    #Hough Line Draw
    minLength = 20
    maxGap = 10
    road_lines = cv2.HoughLinesP(img_postthresh, 1, np.pi/180, 20, minLength, maxGap)
    left_lane, right_lane, left_slope, right_slope = extract_lane(road_lines)
    left_lane_sa, right_lane_sa = split_append(left_lane, right_lane)
    
    draw_lanes(left_lane_sa, right_lane_sa,frame)
    cv2.imshow('Image',frame)
    cv2.imshow('Post Threshold',img_postthresh)
    cv2.waitKey(1)



# def imgCallback(data):
	
# 	cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
	
# 	process(cv_image)
	
def main():
	print("Hey Universe!")
	rospy.init_node('my_planner_node')
	img_sub = rospy.Subscriber("/image_raw", Image, imgCallback)
	rospy.spin()

if __name__ == "__main__":
	main()