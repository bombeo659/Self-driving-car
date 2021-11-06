cmake_minimum_required(VERSION 3.0.2)
project(rj_training)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

add_message_files(
	FILES
	StringWithHeader.msg
)

generate_messages(
	DEPENDENCIES
	std_msgs
)

catkin_package(
	CATKIN_DEPENDS message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(talker_node src/talker.cpp)
target_link_libraries(talker_node ${catkin_LIBRARIES})
add_dependencies(talker_node ${catkin_EXPORTED_TARGETS})

add_executable(listener_node src/listener.cpp)
target_link_libraries(listener_node ${catkin_LIBRARIES})
add_dependencies(listener_node ${catkin_EXPORTED_TARGETS})
