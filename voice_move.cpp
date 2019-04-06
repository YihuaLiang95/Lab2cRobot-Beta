/***********************************************************/
/* Author: www.corvin.cn                                   */
/***********************************************************/
/* Description:该源码为接收语音解析后控制小车移动的代码，  */
/*   包括小车的前后左右移动。                              */
/*                                                         */
/***********************************************************/
/* History:                                                */
/*  20180117:init this source code.                        */
/*  20190406:lab 2c                                        */
/*                                                         */
/***********************************************************/

#include <ros/ros.h>
#include <std_msgs/Int32.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Twist.h>

#define MOVE_FORWARD_CMD 1
#define MOVE_BACK_CMD    2
#define MOVE_LEFT_CMD    3
#define MOVE_RIGHT_CMD   4
#define TURN_LEFT_CMD    5
#define TURN_RIGHT_CMD   6
#define STOP_MOVE_CMD    7

#define BACK_HOME_CMD    8
#define GO_AWAY_CMD      9

#define  GO_CONFERENCE_ROOM 10
#define  GO_PROF_ZHANG_OFFICE 11
#define  GO_PROF_HUANG_OFFICE 12
#define  GO_FRONT_DOOR     13
#define  GO_MAIN_ENTRANCE  14
#define  GO_ANOTHER_LAB    15
#define  GO_BACK_ORIGIN    16
#define  QUIT_THE_PROGRAM  17



ros::Publisher pub;
ros::Publisher nav_pub;

float speed_x = 0.5;
float speed_y = 0.5;
float turn_speed = 1.0;
int pub_flag = 0;
int nav_flag = 0;
geometry_msgs::Twist cmd_msg;
std_msgs::String nav_msg;

void subCallBack(const std_msgs::Int32::ConstPtr& msg)
{
    ROS_WARN("Get Move CMD:%d",msg->data); 

    switch(msg->data)
    {
        case MOVE_FORWARD_CMD: //move forward
            {
                nav_msg.data = "move forward";
                break;
            }

        case MOVE_BACK_CMD: //move back 
            {
                nav_msg.data = "move backward";
                break;
            }

        case MOVE_LEFT_CMD: //move left 
            {
                nav_msg.data = "move leftward";
                break;
            }

        case MOVE_RIGHT_CMD: //move right 
            {
                nav_msg.data = "move rightward";
                break;
            }

        case TURN_LEFT_CMD: //turn left 
            {
                nav_msg.data = "turn left";
                break;
            }

        case TURN_RIGHT_CMD: //turn right 
            {
                nav_msg.data = "turn right";
                break;
            }

        case STOP_MOVE_CMD: //stop move 
            {
                nav_msg.data = "stop move";
                break;
            }
			
        case GO_CONFERENCE_ROOM:
            {
                nav_msg.data = "go conference room";
                break;
            }
		case GO_PROF_ZHANG_OFFICE:
            {
                nav_msg.data = "go prof zhang office";
                break;
            }
		case GO_PROF_HUANG_OFFICE:
            {
                nav_msg.data = "go prof huang office";
                break;
            }
		case GO_FRONT_DOOR:
            {
                nav_msg.data = "go front door";
                break;
            }
		case GO_MAIN_ENTRANCE:
            {
                nav_msg.data = "go main entrance";
                break;
            }
		case GO_ANOTHER_LAB:
            {
                nav_msg.data = "go another lab";
                break;
            }
		case GO_BACK_ORIGIN:
            {
                nav_msg.data = "go back origin";
                break;
            }
		case QUIT_THE_PROGRAM:
            {
                nav_msg.data = "quit the program";
                break;
            }
        default:
            ROS_WARN("Get Unknown Move CMD:%d",msg->data); 
            break;
    }

    if((msg->data >= MOVE_FORWARD_CMD)&&(msg->data <= TURN_RIGHT_CMD))
    //if((msg->data >= MOVE_FORWARD_CMD)&&(msg->data <= BACK_TO_LAP))
    {
        nav_flag = 1;
    }
    else if( msg->data == 7 || msg->data == 8)
    {
        nav_flag = 1;
    }
	else if( msg->data >= GO_CONFERENCE_ROOM && msg->data <= QUIT_THE_PROGRAM)
    {
        nav_flag = 1;
    }
    else
    {
        ROS_WARN("set pub_flag = 0"); 
        pub_flag = 0;
    }
}


int main(int argc, char **argv)
{
    ros::init(argc, argv, "voice_move_node");
    ros::NodeHandle ndHandle;

    std::string sub_move_topic = "/voice_system/voice_cmd_vel";
    std::string pub_move_topic = "/cmd_vel";

    ros::param::get("~sub_move_topic",     sub_move_topic);
    ros::param::get("~pub_move_topic",     pub_move_topic);
    ros::param::get("~default_speed_x",    speed_x);
    ros::param::get("~default_speed_y",    speed_y);
    ros::param::get("~default_turn_speed", turn_speed);
    //ros::param::get("~nav_topic",          nav_topic);

    ros::Subscriber sub = ndHandle.subscribe(sub_move_topic, 1, subCallBack); 

    pub = ndHandle.advertise<geometry_msgs::Twist>(pub_move_topic, 1);

    nav_pub = ndHandle.advertise<std_msgs::String>("fuck_the_robot",1);

    ros::Rate loop_rate(5);
    while(ros::ok())
    {
        if(pub_flag)
        {
            pub.publish(cmd_msg);
            pub_flag=0; //only send once
        }
        else if(nav_flag)
        {
            nav_pub.publish(nav_msg);
            nav_flag = 0; //only send once
        }
        loop_rate.sleep();
        ros::spinOnce();
    }

    return 0;
}