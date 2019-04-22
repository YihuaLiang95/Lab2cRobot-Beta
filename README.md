# Zelong Yang's work
List the work done and to be done week by week.
   # 1. Week 3 and 4</br>
   Doing the contacting work with Jinzheng Company and Siemens company. After consulting, we decided not to do the internet of things module temporarily. Then I joined the motion group.
   # 2. Week 5</br>
   Wrote a function to directly control the motion of the robot using command streams (like 'forward', 'forward', ...) instead of the keyboard control.
   Wrote a module to desgnate the destination point to the robot and it will find its way there automaticly.
   Found the format of the position points, designed a way from room 1505 to the conference room. Record the vedio
   # 3. Week 6</br>
   Colabrate with Yihua Liang, built the connection interface between the voice module and the motion module so that the robot can go to the designated destination using voice command. The target position and the map is provided by Weijia Feng and the voice control port is provided by Lu Liu. 
   # 4. Week 7</br>
   Calibrated the linear velocity and the angular velocity precisely using rular and protractor. After calibration the angular error decreased from 10° to 4° and the linear error decreased about 5%.
   Added more synonym voice command so that the voice control function would be more roubustic to error voice recognition.
   # 5. Week 8 and 9</br>
   Arranged the codes in the github.
   
   Colabrated with Yihua Liang: built the voiceprint module, which recognizes the voice and tell the name of the speaker.
   The voiceprint module includes three parts: voice recording, voice recognizing and speech synthesis.
   
   Implemented the voiceprint module into the voice module, so we can turn on the voiceprint module using voice command.
