# Tbsi2cRobot-Ultrasonic Sensor

1. Output: Uart TTL

2. Number of detector: 4

3. Detection Distance: 30cm~250cm

   **Note**: The distance above is the **functional distance**, which means that if you put the obstacle too far or too close to the detector, then the output value may not be reliable. If the distance is too large or small, then the output value may oscillate frequently.

4. Output format: Header + HEX value of the distance of 4 detectors(in cm)

5. Output Example:

   `CB 55 04 AA BB CC AA`

   In the example above, the `CB 55`is the header part(which should be fixed value for this sensor), while `04` means that the distance output string consists of four values behind it. `AA BB CC AA`here is **the real detected distance** by the four detectors respectively, which is measured in centimeter(cm) and shown as HEX(16进制) value. For this case, we have the distance as follows:

   Detector A: $$AA=0xaa=170cm$$

   Detector B: $$BB=0xbb=187cm$$

   Detector C: $$CC=0xcc=204cm$$

   Detector D: $$AA=0xaa=170cm$$

   | **0xcb** | **固定帧头**       |
   | -------- | ------------------ |
   | **0x55** | **命令字属性**     |
   | **0x04** | **数据个数**       |
   | **0xaa** | **数据1对应探头A** |
   | **0xbb** | **数据2对应探头B** |
   | **0xcc** | **数据3对应探头C** |
   | **0xaa** | **数据4对应探头D** |

6. How to launch the sensor node:

   (1) launch the ros system by `roscore`

   (2) launch the ultrasonic sensor by `rosrun serial_port serial_port`

7. How to integrate more subscriber/publisher node into sensor node:

   (1)the sensor node file is at `~/serial_port/`

   (2)you should change the file at `~/serial_port/src/serial_port/src/serial_port.cpp` to modify the functions. The ultrasoinc sensor node is based on the `serial`, which is a package provided by ROS to achieve serial communication.

   (3)After the file has been changed, you may need to modify `CMakeList.txt`

   (4)you should `cd` to `~/serial_port`, then `source /devel/setup.bash`

   (5)finally, `cd` to `~/serial_port`and `catkin_make`

   (6)launch the modified node by `rosrun serial_port serial_port`

8. How to see the node communication status:

   `rqt_graph`

   Currently, we only have one node after rosrun, which is /serial_port

9. The C++ code in `serial_port.cpp` file with comments:

````c++
//serial_port.cpp
#include <ros/ros.h>
#include <serial/serial.h>
#include <iostream>
 
int main(int argc, char** argv)
{
    ros::init(argc, argv, "serial_port");
    //创建句柄
    ros::NodeHandle n;
    
    //创建一个serial类，sp是名字
    serial::Serial sp;
    //创建timeout
    serial::Timeout to = serial::Timeout::simpleTimeout(100);
    //设置要打开的串口名称（我们的超声波雷达USB对应USB0）
    sp.setPort("/dev/ttyUSB0");
    //设置串口通信的波特率（我们的超声波雷达波特率）
    sp.setBaudrate(9600);
    //串口设置timeout
    sp.setTimeout(to);
 
    try
    {
        //打开串口
        sp.open();
    }
    catch(serial::IOException& e)
    {
        ROS_ERROR_STREAM("Unable to open port.");
        return -1;
    }
    
    //判断串口是否打开成功
    if(sp.isOpen())
    {
        ROS_INFO_STREAM("/dev/ttyUSB0 is opened.");
    }
    else
    {
        return -1;
    }
    
    ros::Rate loop_rate(50);  //以50Hz输出串口数据
    while(ros::ok())
    {
        //获取缓冲区内的字节数
        size_t n = sp.available();
        if(n!=0)
        {
            uint8_t buffer[128];
            //读出数据
            n = sp.read(buffer, n);
            
            for(int i=0; i<n; i++)
            {
                //16进制的方式打印到屏幕
                std::cout << std::hex << (buffer[i] & 0xff) << " ";
            }
            std::cout << std::endl;
        }
        loop_rate.sleep();
    }
    
    //关闭串口
    sp.close();
 
    return 0;
}
````

10. Product picture:

    ![img](https://img.alicdn.com/imgextra/i1/4041770501/O1CN011FZUsox0KYY3VC3_!!4041770501.jpg)

