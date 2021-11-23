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
	robot_state_publisher
	joint_state_controller
	controller_manager
	gazebo_ros_control
	transmission_interface
	effort_controllers
	velocity_controllers
	position_controllers
	cv_bridge
        image_transport
	${PKG_DEPS}
	${OpenCV_INCLUDE_DIRS}
)

find_package(OpenCV 4.2.0 REQUIRED)

catkin_package(
	CATKIN_DEPENDS
	sensor_msgs
	gazebo_msgs
	geometry_msgs
	urdf_tutorial
	controller_manager
	robot_state_publisher
	joint_state_controller
	gazebo_ros_control
	transmission_interface
	effort_controllers
	velocity_controllers
	position_controllers
)

include_directories(include
	${catkin_INCLUDE_DIRS}
	${OpenCV_INCLUDE_DIRS}
	)

add_executable(vehicle_input_subscriber src/vehicle_input_subscriber.cpp)
add_dependencies(vehicle_input_subscriber ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(vehicle_input_subscriber ${catkin_LIBRARIES})

add_executable(vehicle_info_publisher src/vehicle_info_publisher.cpp)
add_dependencies(vehicle_info_publisher ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(vehicle_info_publisher ${catkin_LIBRARIES})

install(TARGETS vehicle_input_subscriber vehicle_info_publisher
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

