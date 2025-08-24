#!/bin/bash
source ~/.bashrc
workspace=$(pwd)

#x7s
cd ${workspace}; cd ../..; cd ROS2/R5_ws; rm -rf build install log .catkin_workspace src/CMakeLists.txt; colcon build;
sleep 0.5

#VR
cd ${workspace}; cd ../..; cd ARX_VR_SDK/ROS2; rm -rf build install log .catkin_workspace; ./port.sh;
