#!/usr/bin/env bash
python ~/catkin_ws/src/py_lidar_publisher/test_send_packet.py &
python ~/catkin_ws/src/py_odom_publisher/test_send_odom_packet.py &
