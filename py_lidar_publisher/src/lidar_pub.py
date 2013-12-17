#!/usr/bin/env python

#Example from: http://forums.trossenrobotics.com/printthread.php?t=4304&pp=10&page=8

import math
import socket
import sys
#sys.path.insert(0, '../')

import roslib; ##roslib.load_manifest('pi_robot')
import rospy

from tf.broadcaster import TransformBroadcaster
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Header

#import get_ip

class LidarNode:

    def __init__(self):
        # Get the ~private namespace parameters from command line or launch file.
        self.UDP_IP = "192.168.48.72" #get_ip.get_local()
        self.UDP_PORT = int(rospy.get_param('~UDP_PORT', '49151'))
        self.parent = rospy.get_param('~parent', 'base_scan')
        self.child = rospy.get_param('~child', 'base_link')

        self.num_readings = rospy.get_param('~num_readings', 0)

        # create ros::Publisher to send LaserScan messages
        scanPub = rospy.Publisher('base_scan', LaserScan) # node publishing LaserScan to 'base_scan'
        scanBroadcaster = TransformBroadcaster()

        #crappy test
        t = True
        while not rospy.is_shutdown():
        #    scanBroadcaster.sendTransform(
        #    (0, 0, 0), 
        #    (0, 0, 0, 1),
        #    rospy.Time.now(),
        #    "base_scan",
        #    "base_link"
        #    )

            lidar_string = self.receive_packet()
            scan = self.create_lidar_msg(lidar_string) 

            self.scanPub.publish(scan)

            #crappy test continued
            if t:
                print "Lidar Running"
                print scan 
            t = False

    def receive_packet(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.bind((self.UDP_IP, self.UDP_PORT))
        packet, addr = sock.recvfrom(100000) # buffer size is not 1024 bytes

        return packet

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
    def create_lidar_msg(lidar_string):
        lidar_msg = LaserScan()    
        data = lidar_string.split(";")
        #num_readings = 1440 --------------------------------
        #data[0] = min angle (degrees)
        #data[1] = max angle (degrees)
        #data[2] = timestep (ms)
        #data[3] = lidar scan array
        #data[4] = min range
        #data[5] = max range	

        #print data

        lidar_msg.header = create_header() #self?
        lidar_msg.angle_min = math.radians(float(data[0]))
        lidar_msg.angle_max = math.radians(float(data[1]))
        lidar_msg.angle_increment = math.radians(.25) #get from lidar
        lidar_msg.time_increment = float(25. / self.num_readings) #time in ms / measurements YOYOYOYO CHECK THIS
        lidar_msg.scan_time = float(data[2])
        lidar_msg.range_min = float(data[4]) / 1000 #sent in mm, should be meters
        lidar_msg.range_max = float(data[5]) / 1000 #sent in mm, should be meters


        array_string = data[3].translate(None, '[]')
        string_array = array_string.split(",")
        lidar_msg.ranges = [float(r) / 1000 for r in string_array] #better way?
    #    string_array = data[3].strip("[").strip("]").split(",")
        # string_array = data[3].split(",")
        # try:
        #     lidar_msg.ranges = [float(r) for r in string_array]
        #     lidar_msg.intensities = []
        # except ValueError:
        #     print "range vals failed"

        return lidar_msg

    def create_header(self):
        head = Header()
        head.stamp = rospy.Time.now() #YOYOYOYOshould be from robot
        head.frame_id = self.parent

        return head

if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node("base_scan") #ros::NodeHandle n;

    try:
        ln = LidarNode()
    except rospy.ROSInterruptException: 
        pass




































