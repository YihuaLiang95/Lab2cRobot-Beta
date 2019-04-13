/*
 * author: www.corvin.cn
 *
 * description: nlp node,invoke tuling server to nlp and process move cmd.
 *
 * History:
 *   20171128:init this file.
 *   20180117:增加解析语音控制小车移动和导航的命令词,可以通过中文语音来控制
 *      小车移动和自动导航到目的地。
 *   20190405:add commands of TBSI 2C
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
static string tuling_key="175418b0747f4c50b15843fe0849067e"; //default tuling key
static string move_forward_str;
static string move_forward_str1;
static string move_forward_str2;
static string move_forward_str3;
static string move_forward_str4;
static string move_forward_str5;
static string move_forward_str6;
static string move_forward_str7;
static string move_back_str;
static string move_back_str1;
static string move_back_str2;
static string move_left_str;
static string move_left_str1;
static string move_left_str2;
static string move_right_str;
static string move_right_str1;
static string move_right_str2;
static string turn_left_str;
static string turn_left_str1;
static string turn_left_str2;
static string turn_right_str;
static string turn_right_str1;
static string turn_right_str2;
static string stop_move_str;
static string back_home_str;
static string go_away_str;

static string go_conference_room_str;
static string go_prof_zhang_office_str;
static string go_prof_huang_office_str;
static string go_front_door_str;
static string go_main_entrance_str;
static string go_another_lab_str;
static string go_back_origin_str;
static string quit_the_program_str;


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

/**
 * parse tuling server response json string
 */
int parseJsonResonse(string input)
{
    Json::Value root;
    Json::Reader reader;
    cout << "tuling server response origin json str:" << input << endl;
    bool parsingSuccessful = reader.parse(input, root);

    if(!parsingSuccessful)
    {
        cout << "!!! Failed to parse the response data" <<endl;
        return 1;
    }
    const Json::Value code = root["code"];
    const Json::Value text = root["text"];
    result = text.asString();
    flag = 1;
    cout << "response code:" << code << endl;
    cout << "response text:" << result <<endl;

    return 0;
}


/**
 * send tuling server http pose requeset
 */
int HttpPostRequest(string input, string key)
{
    string buffer;

    std::string strJson = "{";
    strJson += "\"key\" : ";
    strJson += "\"";
    strJson += key;
    strJson += "\",";
    strJson += "\"info\" : ";
    strJson += "\"";
    strJson += input;
    strJson += "\"";
    strJson += "}";

    cout<< "post json string:" << strJson <<endl;
    try
    {
        CURL *pCurl = NULL;
        CURLcode res;
        curl_global_init(CURL_GLOBAL_ALL);

        // get a curl handle
        pCurl = curl_easy_init();
        if (NULL != pCurl)
        {
            //set url timeout
            curl_easy_setopt(pCurl, CURLOPT_TIMEOUT, 5);

            // First set the URL that is about to receive our POST.
            curl_easy_setopt(pCurl, CURLOPT_URL, "http://www.tuling123.com/openapi/api");

            // set curl http header
            curl_slist *plist = curl_slist_append(NULL,"Content-Type:application/json; charset=UTF-8");
            curl_easy_setopt(pCurl, CURLOPT_HTTPHEADER, plist);

            // set curl post content fileds
            curl_easy_setopt(pCurl, CURLOPT_POSTFIELDS, strJson.c_str());

            curl_easy_setopt(pCurl, CURLOPT_WRITEFUNCTION, writer);
            curl_easy_setopt(pCurl, CURLOPT_WRITEDATA, &buffer);

            // Perform the request, res will get the return code
            res = curl_easy_perform(pCurl);

            // Check for errors
            if (res != CURLE_OK)
            {
                printf("curl_easy_perform() failed:%s\n", curl_easy_strerror(res));
            }
            // always cleanup
            curl_easy_cleanup(pCurl);
        }
        curl_global_cleanup();
    }
    catch (std::exception &ex)
    {
        printf("!!! curl exception %s.\n", ex.what());
    }

    if(buffer.empty())
    {
        cout << "!!! ERROR The TuLing server response NULL" <<endl;
    }
    else
    {
        parseJsonResonse(buffer);
    }

    return 0;
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
    wstring forwardStr1   = str2wstr(move_forward_str1);
    wstring forwardStr2   = str2wstr(move_forward_str2);
    wstring forwardStr3   = str2wstr(move_forward_str3);
    wstring forwardStr4   = str2wstr(move_forward_str4);
    wstring forwardStr5   = str2wstr(move_forward_str5);
    wstring forwardStr6   = str2wstr(move_forward_str6);
    wstring forwardStr7   = str2wstr(move_forward_str7);
    wstring backStr      = str2wstr(move_back_str);
    wstring backStr1      = str2wstr(move_back_str1);
    wstring backStr2      = str2wstr(move_back_str2);
    wstring moveLeftStr  = str2wstr(move_left_str);
    wstring moveLeftStr1  = str2wstr(move_left_str1);
    wstring moveLeftStr2  = str2wstr(move_left_str2);
    wstring moveRightStr = str2wstr(move_right_str);
    wstring moveRightStr1 = str2wstr(move_right_str1);
    wstring moveRightStr2 = str2wstr(move_right_str2);
    wstring turnLeftStr  = str2wstr(turn_left_str);
    wstring turnLeftStr1  = str2wstr(turn_left_str1);
    wstring turnLeftStr2  = str2wstr(turn_left_str2);
    wstring turnRightStr = str2wstr(turn_right_str);
    wstring turnRightStr1 = str2wstr(turn_right_str1);
    wstring turnRightStr2 = str2wstr(turn_right_str2);
    wstring backHomeStr  = str2wstr(back_home_str);
    wstring goAwayStr    = str2wstr(go_away_str);
    wstring stopMoveStr  = str2wstr(stop_move_str);
	
    wstring goConferenceRoomStr = str2wstr(go_conference_room_str);
    wstring goProfZhangOfficeStr = str2wstr(go_prof_zhang_office_str);
    wstring goProfHuangOfficeStr = str2wstr(go_prof_huang_office_str);
    wstring goFrontDoorStr = str2wstr(go_front_door_str);
    wstring goMainEntranceStr = str2wstr(go_main_entrance_str);
    wstring goAnotherLabStr = str2wstr(go_another_lab_str);
    wstring goBackOriginStr = str2wstr(go_back_origin_str);
    wstring quitTheProgram = str2wstr(quit_the_program_str);

    if(convertStr.find(forwardStr) != string::npos)
    {
        ret = MOVE_FORWARD_CMD;
    }
    if(convertStr.find(forwardStr1) != string::npos)
    {
        ret = MOVE_FORWARD_CMD;
    }
    if(convertStr.find(forwardStr2) != string::npos)
    {
        ret = MOVE_FORWARD_CMD;
    }
    if(convertStr.find(forwardStr3) != string::npos)
    {
        ret = MOVE_FORWARD_CMD;
    }
    if(convertStr.find(forwardStr4) != string::npos)
    {
        ret = MOVE_FORWARD_CMD;
    }
    if(convertStr.find(forwardStr5) != string::npos)
    {
        ret = MOVE_FORWARD_CMD;
    }
    if(convertStr.find(forwardStr6) != string::npos)
    {
        ret = MOVE_FORWARD_CMD;
    }
    if(convertStr.find(forwardStr7) != string::npos)
    {
        ret = MOVE_FORWARD_CMD;
    }
    else if(convertStr.find(backStr) != string::npos) 
    {
        ret = MOVE_BACK_CMD; 
    }
    else if(convertStr.find(backStr1) != string::npos) 
    {
        ret = MOVE_BACK_CMD; 
    }
    else if(convertStr.find(backStr2) != string::npos) 
    {
        ret = MOVE_BACK_CMD; 
    }
    else if(convertStr.find(moveLeftStr) != string::npos) 
    {
        ret = MOVE_LEFT_CMD; 
    }
    else if(convertStr.find(moveLeftStr1) != string::npos) 
    {
        ret = MOVE_LEFT_CMD; 
    }
    else if(convertStr.find(moveLeftStr2) != string::npos) 
    {
        ret = MOVE_LEFT_CMD; 
    }
    else if(convertStr.find(moveRightStr) != string::npos) 
    {
        ret = MOVE_RIGHT_CMD; 
    }
    else if(convertStr.find(moveRightStr1) != string::npos) 
    {
        ret = MOVE_RIGHT_CMD; 
    }
    else if(convertStr.find(moveRightStr2) != string::npos) 
    {
        ret = MOVE_RIGHT_CMD; 
    }
    else if(convertStr.find(turnLeftStr) != string::npos) 
    {
        ret = TURN_LEFT_CMD; 
    }
    else if(convertStr.find(turnLeftStr1) != string::npos) 
    {
        ret = TURN_LEFT_CMD; 
    }
    else if(convertStr.find(turnLeftStr2) != string::npos) 
    {
        ret = TURN_LEFT_CMD; 
    }
    else if(convertStr.find(turnRightStr) != string::npos) 
    {
        ret = TURN_RIGHT_CMD; 
    }
    else if(convertStr.find(turnRightStr1) != string::npos) 
    {
        ret = TURN_RIGHT_CMD; 
    }
    else if(convertStr.find(turnRightStr2) != string::npos) 
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
    else if(convertStr.find(goConferenceRoomStr) != string::npos) 
    {
        ret = GO_CONFERENCE_ROOM; 
    }
    else if(convertStr.find(goProfZhangOfficeStr) != string::npos) 
    {
        ret = GO_PROF_ZHANG_OFFICE; 
    }
    else if(convertStr.find(goProfHuangOfficeStr) != string::npos) 
    {
        ret = GO_PROF_HUANG_OFFICE; 
    }
    else if(convertStr.find(goFrontDoorStr) != string::npos) 
    {
        ret = GO_FRONT_DOOR; 
    }
    else if(convertStr.find(goMainEntranceStr) != string::npos) 
    {
        ret = GO_MAIN_ENTRANCE; 
    }
    else if(convertStr.find(goAnotherLabStr) != string::npos) 
    {
        ret = GO_ANOTHER_LAB; 
    }
    else if(convertStr.find(goBackOriginStr) != string::npos) 
    {
        ret = GO_BACK_ORIGIN; 
    }
    else if(convertStr.find(quitTheProgram) != string::npos)
    {
        ret = QUIT_THE_PROGRAM;
    }
    return ret;
}

/**
*   when nlp node get input,will auto send http post request to tuling server
**/
void nluCallback(const std_msgs::String::ConstPtr& msg)
{
    int ret = 0;
    std::cout<<"tuling_nlu_node get input is:" << msg->data << std::endl;

    ret = parseInputString(msg->data);
    ROS_INFO("tuling_nlu_node get parseInputString return: %d", ret);
    if(ret == 0) //send tuling nlu server to process
    {
        HttpPostRequest(msg->data, tuling_key);
    }
    else if((ret >= MOVE_FORWARD_CMD)&&(ret <= STOP_MOVE_CMD))
    {
        std_msgs::Int32 move_msg;
        move_msg.data = ret;
        cmd_vel_pub.publish(move_msg);
    }
    else if((ret >= GO_CONFERENCE_ROOM)&&(ret <= QUIT_THE_PROGRAM))
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
    ros::init(argc, argv, "tuling_nlu_node");
    ros::NodeHandle ndHandle;

    string nlu_topic = "/voice_system/nlu_topic"; //default nlu topic name
    string tts_topic = "/voice_system/tts_topic"; //default tts topic name
    string cmd_topic = "/voice_system/move_topic";  //default carebot voice control move topic
    string nav_topic = "/voice_system/voice_navigation_cmd";

    ros::param::get("~nlu_topic",  nlu_topic);
    ros::param::get("~tts_topic",  tts_topic);
    ros::param::get("~tuling_key", tuling_key);

    ros::param::get("~move_forward", move_forward_str);
    ros::param::get("~move_forward1", move_forward_str1);
    ros::param::get("~move_forward2", move_forward_str2);
    ros::param::get("~move_forward3", move_forward_str3);
    ros::param::get("~move_forward4", move_forward_str4);
    ros::param::get("~move_forward5", move_forward_str5);
    ros::param::get("~move_forward6", move_forward_str6);
    ros::param::get("~move_forward7", move_forward_str7);
    ros::param::get("~move_back",  move_back_str);
    ros::param::get("~move_back1",  move_back_str1);
    ros::param::get("~move_back2",  move_back_str2);
    ros::param::get("~move_left",  move_left_str);
    ros::param::get("~move_left1",  move_left_str1);
    ros::param::get("~move_left2",  move_left_str2);
    ros::param::get("~move_right", move_right_str);
    ros::param::get("~move_right1", move_right_str1);
    ros::param::get("~move_right2", move_right_str2);
    ros::param::get("~turn_left",  turn_left_str);
    ros::param::get("~turn_left1",  turn_left_str1);
    ros::param::get("~turn_left2",  turn_left_str2);
    ros::param::get("~turn_right", turn_right_str);
    ros::param::get("~turn_right1", turn_right_str1);
    ros::param::get("~turn_right2", turn_right_str2);
    ros::param::get("~stop_move",  stop_move_str);
    
    ros::param::get("~back_home", back_home_str);    
    ros::param::get("~go_away", go_away_str);
	
    ros::param::get("~go_conference_room", go_conference_room_str);
    ros::param::get("~go_prof_zhang_office", go_prof_zhang_office_str);
    ros::param::get("~go_prof_huang_office", go_prof_huang_office_str);
    ros::param::get("~go_front_door", go_front_door_str);
    ros::param::get("~go_main_entrance", go_main_entrance_str);
    ros::param::get("~go_another_lab", go_another_lab_str);
    ros::param::get("~go_back_origin", go_back_origin_str);
    ros::param::get("~quit_the_program", quit_the_program_str);

    ros::param::get("~move_topic", cmd_topic);
    ros::param::get("~nav_topic", nav_topic);

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
