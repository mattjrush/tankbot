#!/usr/bin/env python

#Example from: http://forums.trossenrobotics.com/printthread.php?t=4304&pp=10&page=8

import math
import socket

import roslib; ##roslib.load_manifest('pi_robot')
import rospy

from sensor_msgs.msg import LaserScan
from tf.broadcaster import TransformBroadcaster

#import get_ip

def receive_packet():
    UDP_IP = "192.168.48.72" #get_ip.get_local()
    #UDP_IP = 'localhost' #TEST CODE    
    UDP_PORT = 49151
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    packet, addr = sock.recvfrom(100000) # buffer size is not 1024 bytes

    return packet
    
def create_lidar_msg(scan, lidar_string):

    data = lidar_string.split(";")
    num_readings = 1440
    #data[0] = min angle (degrees)
    #data[1] = max angle (degrees)
    #data[2] = timestep (ms)
    #data[3] = lidar scan array
    #data[4] = min range
    #data[5] = max range	

    #print data

    scan.header.stamp = rospy.Time.now()        
    scan.header.frame_id = "base_scan"
    scan.angle_min = math.radians(float(data[0]))
    scan.angle_max = math.radians(float(data[1]))
    scan.angle_increment = math.radians(.25) #get from lidar
    scan.time_increment = float(25. / num_readings) #time in ms / measurements
    scan.scan_time = float(data[2])
    scan.range_min = float(data[4]) / 1000 #sent in mm, needs m
    scan.range_max = float(data[5]) / 1000 #sent in mm, needs m

#    string_array = data[3].strip("[").strip("]").split(",")
    array_string = data[3].translate(None, '[]')
    string_array = array_string.split(",")

    #print string_array
    # try:
    #     scan.ranges = [float(r) for r in string_array]
    #     scan.intensities = []
    # except ValueError:
    #     print "range vals failed"

    scan.ranges = [float(r) / 1000 for r in string_array] #better way?
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
rospy.init_node("base_scan") #ros::NodeHandle n;
scanPub = rospy.Publisher('base_scan', LaserScan) # node publishing LaserScan to 'base_scan'
scanBroadcaster = TransformBroadcaster()


#crappy test
t = True
while not rospy.is_shutdown():
    #crappy test continued
    if t:
        print "Lidar Running"
    t = False#    scanBroadcaster.sendTransform(
#    (0, 0, 0), 
#    (0, 0, 0, 1),
#    rospy.Time.now(),
#    "base_scan",
#    "base_link"
#    )

    scan = LaserScan()    

    lidar_string = receive_packet()
    create_lidar_msg(scan, lidar_string) 

    scanPub.publish(scan)






































