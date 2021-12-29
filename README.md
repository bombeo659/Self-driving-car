# Logic Design Project

## Dependencies

* Ubuntu 20.04
* ROS Noetic
* OpenCV 4.2.0
* Python 3

## How to build

To build the package, follow the next steps:

```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone https://github.com/bombeo659/self-driving-car.git
copy all items from scripts to /usr/share/gazebo-11/media/materials/scripts
cd ..
catkin_make
```

## How to run

To run the package, follow the next steps:

```
cd ~/catkin_ws
source devel/setup.bash
roslaunch self-driving-car world_test.launch
rosrun self-driving-car control.py
```


## Training and testing traffic signs

![turn](https://github.com/bombeo659/Self-driving-car/blob/main/image/lane_heading.png)

![stop](https://github.com/bombeo659/Self-driving-car/blob/main/image/sign1.png)

![graph](https://github.com/bombeo659/Self-driving-car/blob/main/image/image.png)
