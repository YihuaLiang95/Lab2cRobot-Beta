/*
 *
 * description: offline nlp node
 
*/

#include <ros/ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Int32.h>
#include <sstream>
#include <jsoncpp/json/json.h>
#include <curl/curl.h>
#include <string>
#include <exception>
#include <codecvt>


using namespace std;


static int flag = 0;
static string result;
static string move_forward_str;
static string move_back_str;
static string move_left_str;
static string move_right_str;
static string turn_left_str;
static string turn_right_str;
static string back_home_str;
static string go_away_str;
static string stop_move_str;


#define MOVE_FORWARD_CMD 1
#define MOVE_BACK_CMD    2
#define MOVE_LEFT_CMD    3
#define MOVE_RIGHT_CMD   4
#define TURN_LEFT_CMD    5
#define TURN_RIGHT_CMD   6
#define STOP_MOVE_CMD    7

#define BACK_HOME_CMD    8
#define GO_AWAY_CMD      9


ros::Publisher cmd_vel_pub;
ros::Publisher nav_move_pub;


int writer(char *data, size_t size, size_t nmemb, string *writerData)
{
     if (writerData == NULL)
     {
         return -1;
     }
     int len = size*nmemb;
     writerData->append(data, len);

     return len;
}

wstring str2wstr(const std::string& str)
{
    using convert_typeX = std::codecvt_utf8<wchar_t>;
    wstring_convert<convert_typeX, wchar_t> converterX;

    return converterX.from_bytes(str);
}

int parseInputString(string input)
{
    int ret = 0;
    wstring convertStr = str2wstr(input); 

    wstring forwardStr   = str2wstr(move_forward_str);
    wstring backStr      = str2wstr(move_back_str);
    wstring moveLeftStr  = str2wstr(move_left_str);
    wstring moveRightStr = str2wstr(move_right_str);
    wstring turnLeftStr  = str2wstr(turn_left_str);
    wstring turnRightStr = str2wstr(turn_right_str);
    wstring backHomeStr  = str2wstr(back_home_str);
    wstring goAwayStr    = str2wstr(go_away_str);
    wstring stopMoveStr  = str2wstr(stop_move_str);
/*
    if (strcmp(convertStr, forwardStr) == 0)
    {
        ret = MOVE_FORWARD_CMD;
    }

    if(strcmp(convertStr, forwardStr) == 0)
    {
        ret = MOVE_FORWARD_CMD;
    }
    else if(strcmp(convertStr, backStr) == 0)
    {
        ret = MOVE_BACK_CMD; 
    }
    else if(strcmp(convertStr, moveLeftStr) == 0)
    {
        ret = MOVE_LEFT_CMD; 
    }
    else if(strcmp(convertStr, moveRightStr) == 0)
    {
        ret = MOVE_RIGHT_CMD; 
    }
    else if(strcmp(convertStr, turnLeftStr) == 0)
    {
        ret = TURN_LEFT_CMD; 
    }
    else if(strcmp(convertStr, turnRightStr) == 0)
    {
        ret = TURN_RIGHT_CMD; 
    }
    else if(strcmp(convertStr, backHomeStr) == 0) 
    {
        ret = BACK_HOME_CMD; 
    }
    else if(strcmp(convertStr, goAwayStr) == 0)
    {
        ret = GO_AWAY_CMD; 
    }
    else if(strcmp(convertStr, stopMoveStr) == 0)
    {
        ret = STOP_MOVE_CMD; 
    }
*/
    if(convertStr.find(forwardStr) != string::npos)
    {
        ret = MOVE_FORWARD_CMD;
    }
    else if(convertStr.find(backStr) != string::npos) 
    {
        ret = MOVE_BACK_CMD; 
    }
    else if(convertStr.find(moveLeftStr) != string::npos) 
    {
        ret = MOVE_LEFT_CMD; 
    }
    else if(convertStr.find(moveRightStr) != string::npos) 
    {
        ret = MOVE_RIGHT_CMD; 
    }
    else if(convertStr.find(turnLeftStr) != string::npos) 
    {
        ret = TURN_LEFT_CMD; 
    }
    else if(convertStr.find(turnRightStr) != string::npos) 
    {
        ret = TURN_RIGHT_CMD; 
    }
    else if(convertStr.find(backHomeStr) != string::npos) 
    {
        ret = BACK_HOME_CMD; 
    }
    else if(convertStr.find(goAwayStr) != string::npos) 
    {
        ret = GO_AWAY_CMD; 
    }
    else if(convertStr.find(stopMoveStr) != string::npos) 
    {
        ret = STOP_MOVE_CMD; 
    }
    return ret;
}

/**
*   when nlp node get input, match the input with pre-defined word
**/
void nluCallback(const std_msgs::String::ConstPtr& msg)
{
    int ret = 0;
    std::cout<<"offline_nlu_node get input is:" << msg->data << std::endl;

    ret = parseInputString(msg->data);
    ROS_INFO("offline_nlu_node get parseInputString return: %d", ret);
    if(ret == 0) //Do not match any commands
    {
        ROS_INFO("Do not match any commands");
    }
    else if((ret >= MOVE_FORWARD_CMD)&&(ret <= STOP_MOVE_CMD))
    {
        std_msgs::Int32 move_msg;
        move_msg.data = ret;
        cmd_vel_pub.publish(move_msg);
    }
    else //send nav msg
    {
        std_msgs::Int32 nav_msg;
        nav_msg.data = ret;
        nav_move_pub.publish(nav_msg);
    }
}

/**
 * main function
 */
int main(int argc, char **argv)
{
    ros::init(argc, argv, "offline_nlp_node");
    ros::NodeHandle ndHandle;

    string nlu_topic = "/voice_system/nlu_topic"; //default nlu topic name
    string tts_topic = "/voice_system/tts_topic"; //default tts topic name
    string cmd_topic = "/voice_system/move_topic";  //default carebot voice control move topic
    string nav_topic = "/voice_system/voice_navigation_cmd";
/*
    ros::param::get("~nlu_topic",  nlu_topic);
    ros::param::get("~tts_topic",  tts_topic);

    ros::param::get("~move_forward", move_forward_str);
    ros::param::get("~move_back",  move_back_str);
    ros::param::get("~move_left",  move_left_str);
    ros::param::get("~move_right", move_right_str);
    ros::param::get("~turn_left",  turn_left_str);
    ros::param::get("~turn_right", turn_right_str);
    ros::param::get("~stop_move",  stop_move_str);
    
    ros::param::get("~back_home", back_home_str);    
    ros::param::get("~go_away", go_away_str);

    ros::param::get("~move_topic", cmd_topic);
    ros::param::get("~nav_topic", nav_topic);
*/
    ros::Subscriber sub_nlu = ndHandle.subscribe(nlu_topic, 3, nluCallback);
    ros::Publisher tts_pub  = ndHandle.advertise<std_msgs::String>(tts_topic, 1);
    cmd_vel_pub  = ndHandle.advertise<std_msgs::Int32>(cmd_topic, 1);
    nav_move_pub = ndHandle.advertise<std_msgs::Int32>(nav_topic, 1);

    ros::Rate loop_rate(10);
    while(ros::ok())
    {
        if(flag)
        {
           std_msgs::String msg;
           msg.data = result;
           tts_pub.publish(msg);
           flag = 0;
        }
        ros::spinOnce();
        loop_rate.sleep();
    }

    return 0;
}


