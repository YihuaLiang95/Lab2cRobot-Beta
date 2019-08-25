# Simple Tutorial to Laser_filter

This tutorial is for the basic utilization of ROS package laser_filter.

## 1. Download, and install laser_filter in your ros platform

## 2.Write a .launch for the desired filter
Basically, according to [the wiki of laser filters](http://wiki.ros.org/laser_filters), you could modify a template .yaml which stores parameters to meet your own need as follows:


my_laser_config.yaml:

```
scan_filter_chain:
- name: unique_name1
  type: LaserFilterClass1
  params:
    param1: a
    param2: b
- name: unique_name2
  type: LaserFilterClass2
  params:
    param1: a
    param2: b
```



## 3. Modify related nodes 

To suceesfully substitute laser data with filtered  laser data, you also need to remap the topic arguments (detalis have been illustrated [Remapping Arguments](http://wiki.ros.org/Remapping%20Arguments) and [remap](http://wiki.ros.org/roslaunch/XML/remap)) Here we adpot the second way, i.e, add a new line in the head of launch file to replace the orginal /scan topic with /scan_filtered topic. An example is as follows, a new line has been add on the second line.

```
<launch>
  <node pkg="move_base" type="move_base" respawn="false" name="move_base" output="screen">
    <remap from="scan" to="scan_filtered" />
    <rosparam file="$(find rikirobot)/param/navigation/$(env RIKIBASE)/costmap_common_params.yaml" command="load" ns="global_costmap" />
    <rosparam file="$(find rikirobot)/param/navigation/$(env RIKIBASE)/costmap_common_params.yaml" command="load" ns="local_costmap" />
    <rosparam file="$(find rikirobot)/param/navigation/local_costmap_params.yaml" command="load" />
    <rosparam file="$(find rikirobot)/param/navigation/global_costmap_params.yaml" command="load" />
    <rosparam file="$(find rikirobot)/param/navigation/$(env RIKIBASE)/base_local_planner_params.yaml" command="load" />
    <rosparam file="$(find rikirobot)/param/navigation/move_base_params.yaml" command="load" />
  </node>
</launch>
               
```

## 4. Some further tips

1. You could also combine such a filter into your origial launcah file, so that no additional step to turn on the filter is needed.
2. In order to determine which node subscribe to /scan topic, you could use command line rosnode as well as rostopic to check the relationship between your insterested node and /scan topic.