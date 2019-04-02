#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#zelong yang, 20190330
import riki_patrol_nav_func

if __name__ == '__main__':
    try:
        riki_patrol_nav_func.PatrolNav([
[0.450,  0.024, 0.000,0.000, 0.000, 0.035, 0.999],
[0.900,  0.048, 0.000,0.000, 0.000, 0.035, 0.999],
[1.350,  0.072, 0.000,0.000, 0.000, 0.035, 0.999],
[1.800, 0.096, 0.000,0.000, 0.000, 0.035, 0.999],
[2.250,  0.120, 0.000,0.000, 0.000, 0.035, 0.999],
[2.700,  0.144, 0.000,0.000, 0.000, 0.035, 0.999],
[2.700,  0.144, 0.000,0.000, 0.000, -0.563, 0.826],
[2.700,  0.144, 0.000,0.000, 0.000, 0.035, 0.999]])
        riki_patrol_nav_func.rospy.spin()
    except riki_patrol_nav_func.rospy.ROSInterruptException:
        riki_patrol_nav_func.rospy.logwarn("patrol navigation exception finished.")
