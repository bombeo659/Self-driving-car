cmake_minimum_required(VERSION 3.0.2)
project(self-driving-car)

add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
	roscpp
	rospy
	std_msgs
	sensor_msgs
	gazebo_msgs
	geometry_msgs
	urdf_tutorial
	joint_state_controller
	controller_manager
	gazebo_ros_control
	cv_bridge
	${OpenCV_INCLUDE_DIRS}
)

find_package(OpenCV 4.2.0 REQUIRED)

catkin_package(CATKIN_DEPENDS
	sensor_msgs
	gazebo_msgs
	geometry_msgs
	urdf_tutorial
	controller_manager
	robot_state_publisher
	joint_state_controller
	gazebo_ros_control
)

include_directories(include
	${catkin_INCLUDE_DIRS}
	${OpenCV_INCLUDE_DIRS}
)

add_executable(vehicle_input_subscriber src/vehicle_input_subscriber.cpp)
add_dependencies(vehicle_input_subscriber ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(vehicle_input_subscriber ${catkin_LIBRARIES})

install(TARGETS vehicle_input_subscriber
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

catkin_install_python(PROGRAMS src/control.py src/auto_control.py src/auto_control_command.py
 	DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)