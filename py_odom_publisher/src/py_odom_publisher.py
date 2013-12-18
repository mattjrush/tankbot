#!/usr/bin/env python

#Example from: http://forums.trossenrobotics.com/printthread.php?t=4304&pp=10&page=8

import math
import socket

import roslib; ##roslib.load_manifest('pi_robot')
import rospy

from std_msgs.msg import Int16
from std_msgs.msg import String
from tf.broadcaster import TransformBroadcaster
    
def string_to_raw_odom(lidar_string):
    
    l_val = Int16()
    r_val = Int16()
    
    package = rstring.split(";")
    l_val.data = int(package[0])
    r_val.data = int(package[1])

    lPub.Publish(l_val)
    rPub.Publish(r_val)
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
#float32[] ranges         # range data [m] (Note: values < range_min or > range_max should be discarded)
#float32[] intensities    # intensity data [device-specific units] array empty if no data

# create ros::Publisher to send LaserScan messages
#scanBroadcaster = TransformBroadcaster()

def string_to_raw_odom():
    rospy.init_node('raw_odom')
    rospy.Subscriber("encoder_vals", String, string_to_raw_odom)
    lPub = rospy.Publisher('lwheel', Int16) # node publishing LaserScan to 'base_scan'
    rPub = rospy.Publisher('rwheel', Int16) # node publishing LaserScan to 'base_scan'

    print "Running Lidar"
    rospy.spin()

if __name__ == '__main__':
    string_to_raw_odom()





