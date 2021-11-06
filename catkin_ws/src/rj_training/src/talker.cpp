#include <ros/ros.h>
//#include <std_msgs/String.h>
#include <rj_training/StringWithHeader.h>


int main(int argc, char** argv)
{
	//setup
	ros::init(argc, argv, "talker");
	
	ros::NodeHandle node_handle;
	
	ros::NodeHandle private_node_handle("~");
	//ros::Publisher publisher = node_handle.advertise<std_msgs::String>("talker_topic", 1);
	ros::Publisher publisher = node_handle.advertise<rj_training::StringWithHeader>("talker_topic", 1);
	
	std::string greeting = private_node_handle.param<std::string>("greeting", "hello");
	//publish and loop
	ros::Rate rate(10); //Hz
	while(ros::ok())
	{
		//std_msgs::String msg;
		rj_training::StringWithHeader msg;
		msg.data = greeting;
		publisher.publish(msg);
		ros::spinOnce(); // update
		rate.sleep();
	}
	return 0;
}
