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
rosrun self-driving-car auto_control.py
```


#### Training and testing traffic signs

![stop](https://github.com/bombeo659/Self-driving-car/blob/main/image/iamge2.png)

![turn](hhttps://github.com/bombeo659/Self-driving-car/blob/main/image/iamge1.png)

![graph](hhttps://github.com/bombeo659/Self-driving-car/blob/main/image/rosgraph.png)
