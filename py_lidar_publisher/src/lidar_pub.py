#!/usr/bin/env python

#Example from: http://forums.trossenrobotics.com/printthread.php?t=4304&pp=10&page=8

import math

import roslib; ##roslib.load_manifest('pi_robot')
import rospy

from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from std_msgs.msg import Header

#import get_ip

class LidarNode:

    def __init__(self):
        # Get the ~private namespace parameters from command line or launch file.
        self.parent = rospy.get_param('~parent', 'base_scan')
        self.child = rospy.get_param('~child', 'base_link')

        # Initialize the node and name it.
        rospy.init_node("base_scan") #ros::NodeHandle n;
        # create ros::Publisher to send LaserScan messages
        self.scanPub = rospy.Publisher('base_scan', LaserScan) 

        self.num_readings = rospy.get_param('~num_readings', 1000)

    def create_header(self):
        head = Header()
        head.stamp = rospy.Time.now() #YOYOYOYOshould be from robot
        head.frame_id = self.parent

        return head

    # Laser scans angles are measured counter clockwise, with 0 facing forward
    # (along the x-axis) of the device frame

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
    def create_lidar_msg(self, L):
 
        raw_lidar = L.data
        stripped_lidar = raw_lidar.translate(None, '[]').translate(None, '"').translate(None, '\'')
        array_lidar = stripped_lidar.split(",")
        
        lidar_msg = LaserScan()
        lidar_msg.header = self.create_header() #self?
        lidar_msg.angle_min = math.radians(float(array_lidar[2]))
        lidar_msg.angle_max = math.radians(float(array_lidar[3]))
        lidar_msg.angle_increment = math.radians(0.25) #MAKE PARAM
        lidar_msg.time_increment = 0.025/(270*4) #time in ms / measurements YOYOYOYO CHECK THIS
        lidar_msg.scan_time = float(array_lidar[4]) / 1000 #time in ms
        lidar_msg.range_min = float(array_lidar[6]) / 1000 #sent in mm, should be meters
        lidar_msg.range_max = float(array_lidar[7]) / 1000 #sent in mm, should be meters


        array_string = array_lidar[5].translate(None, '[]')
        string_array = array_string.split(",")
        lidar_msg.ranges = [float(r) / 1000 for r in string_array] #better way?

        self.scanPub.publish(lidar_msg)

    def update(self):
        
        rospy.Subscriber("lidar_vals", String, self.create_lidar_msg)
        rospy.spin()

if __name__ == '__main__':

    try:
        ln = LidarNode()
        ln.update()
    except rospy.ROSInterruptException: 
        pass




































