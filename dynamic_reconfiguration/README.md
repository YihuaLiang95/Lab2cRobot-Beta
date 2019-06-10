# Simple Tutorial to dynamic_reconfigure

This tutorial is for the basic utilization of ROS package dynamic_reconfigure. Basically a server has been added to riki_patrol_nav.py as well as set_location_nav_patrol.py which is for the client.



![gif](https://github.com/YihuaLiang95/Lab2cRobot-Beta/blob/weitao/dynamic_reconfiguration/IMG/gif.gif)

## 1. Download, and install dynamic reconfiguration in your ros platform

The package is available on [dynamic_reconfigure](http://wiki.ros.org/dynamic_reconfigure) which links to the Github, where you can clone to your catkin_workspace/src and install it by catkin_make.



## 2. Add "dynamic reconfiguration" feature to your node(optional)

More details can be referred at [Tutorials for dynamic_reconfigure](http://wiki.ros.org/dynamic_reconfigure/Tutorials). Here only basic concepts and ideas are provided.  **If no other parameters outside /move_base are concerned, this step could be skipped.** 

1.  Dynamic reconfigure are implemented by **Service in ROS**.

2. **Some modification to the original package  are needed (for server part), which usually includes C++ code. Better to know some basic C++.**

3. Some packages may have been **implemented dynamic reconfigure** in the original code. Check CMakeList.txt and package.xml to confirm. Like the following codes from costmap2D:

   ![CMakeList](https://github.com/YihuaLiang95/Lab2cRobot-Beta/blob/weitao/dynamic_reconfiguration/IMG/1.png)

4. Server implementation requires a node through rospy, while client doesn't.

5. A better configuration is to use two separate .cpp or .py for server and client, respectively.



# 3. Modify parameters needed in the riki_patrol_nav.py

Two separate sets of parameters for Prof. Huang's office and Main entrance has been added to the riki_patrol_nav.py. Change or add more parameters if needed. 

![main entrance](https://github.com/YihuaLiang95/Lab2cRobot-Beta/blob/weitao/dynamic_reconfiguration/IMG/2.png)



![prof huang office](https://github.com/YihuaLiang95/Lab2cRobot-Beta/blob/weitao/dynamic_reconfiguration/IMG/3.png)



Parameters that could be set dynamically can be checked through 

```
rosrun dynamic_reconfigure dynparam list
```

or GUI  where you can also **manually set parameters after all the nodes are initilized**

```
rosrun rqt_reconfigure rqt_reconfigure
```



# 4. Run set_location_nav_patrol.py and send goal in the terminal

Read the original command in  riki_patrol_nav.py, and type the command you want in the terminal, and stop the client by typing **stop**. Then the client will be killed automatically. **Upper and lower cases are ignored since all the input in this terminal will be converted into lower cases by the python script.** 



**BE AWARE AND REMEMBER TO MODIFY CODE IN riki_patrol_nav.py IF NECESSARY ** when adding new commands.



Currently available command are as follows:

- quit the program
- move forward
- move backward
- move leftward
- move rightward
- turn left
- turn right
- stop move
- move around
- multimodal recognition (Features of multimodal recognition done by Yihua )
- go conference room
- go prof zhang office
- go prof huang office
- go front door
- go main entrance
- go another lab
- go back origin



use following command to run riki_patrol_nav.py:

```
rosrun rikirobot riki_patrol_nav.py
```



# Extra: Brief steps to fine-tune parameters in navigation package

1. Modify or add code snippets related to parameters used in navigation in riki_patrol_nav.py.

2. Launch all the nodes needed. Following command includes all the nodes relevant to voice navigation.

   ```
   roslaunch rikirobot voice_nav_bwsensors_filtered_bringup.launch2
   ```

3. Run the client for dynamic reconfigure.

   ```
   rosrun rikirobot riki_patrol_nav.py
   ```

3. Type in the command you need in terminal.