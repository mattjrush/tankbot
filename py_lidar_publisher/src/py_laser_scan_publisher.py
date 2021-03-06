#!/usr/bin/env python

#Example from: http://forums.trossenrobotics.com/printthread.php?t=4304&pp=10&page=8

import math
import socket

import roslib; ##roslib.load_manifest('pi_robot')
import rospy

from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
    
def create_lidar_msg(L):
    
    raw_lidar = L.data
    stripped_lidar = raw_lidar.translate(None, '[]').translate(None, '"').translate(None, '\'')
    array_lidar = stripped_lidar.split(",")

    num_readings = 1440
    scan = LaserScan() 
    scan.header.stamp = rospy.Time.now()        
    scan.header.frame_id = "base_scan"
    scan.angle_min = math.radians(float(array_lidar[0]))
    scan.angle_max = math.radians(float(array_lidar[1]))
    scan.angle_increment = math.radians(.25) #get from lidar
    scan.time_increment = float(25. / num_readings) #time in ms / measurements
    scan.scan_time = float(array_lidar[2])
    scan.range_min = float(array_lidar[4]) / 1000 #sent in mm, needs m
    scan.range_max = float(array_lidar[5]) / 1000 #sent in mm, needs m
#    string_array = array_lidar[3].strip("[").strip("]").split(",")
    array_string = array_lidar[3].translate(None, '[]')
    string_array = array_string.split(",")
    scan.ranges = [float(r) / 1000 for r in string_array] #better way?

    scanPub.publish(scan)
#
# Laser scans angles are measured counter clockwise, with 0 facing forward
# (along the x-axis) of the device frame
#

#Header header
#float32 angle_min        # start angle of the scan [rad]
#float32 angle_max        # end angle of the scan [rad]
#float32 angle_increment  # angular distance between measurements [rad]
#float32 time_increment   # time between measurements [seconds]
#float32 scan_time        # time between scans [seconds]
#float32 range_min        # minimum range value [m]
#float32 range_max        # maximum range value [m]
#float32[] ranges         # range ` [m] (Note: values < range_min or > range_max should be discarded)
#float32[] intensities    # intensity data [device-specific units] array empty if no data

# create ros::Publisher to send LaserScan messages
#scanBroadcaster = TransformBroadcaster()

#def string_to_laser():
rospy.init_node('base_scan')
scanPub = rospy.Publisher('base_scan', LaserScan) # node publishing LaserScan to 'base_scan'
rospy.Subscriber("lidar_vals", String, create_lidar_msg)
rospy.spin()

# if __name__ == '__main__':
#     string_to_laser()






























