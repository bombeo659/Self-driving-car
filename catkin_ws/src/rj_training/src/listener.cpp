#include <ros/ros.h>
//#include <std_msgs/String.h>
#include <rj_training/StringWithHeader.h>
#include <iostream>

//void Callback(const std_msgs::StringConstPtr& msg)
void Callback (const rj_training::StringWithHeaderConstPtr& msg)
{
	std::cout << msg->data << std::endl;
}

int main(int argc, char** argv)
{
	ros::init(argc, argv, "listener");
	
	ros::NodeHandle node_handle;
	
	ros::Subscriber subscriber = node_handle.subscribe("talker_topic", 1, &Callback);
	
	ros::spin();
	
	return 0;
}
