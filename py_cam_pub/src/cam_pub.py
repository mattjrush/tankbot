#!/usr/bin/env python

import socket
import sys
sys.path.insert(0, '../')

import roslib #roslib.load_manifest('')
import rospy

# Give ourselves the ability to run a dynamic reconfigure server.
from dynamic_reconfigure.server import Server as DynamicReconfigureServer

from sensor_msgs.msg import CompressedImage

import get_ip.py

class CamNode:
    def __init__(self):
        # Get the ~private namespace parameters from command line or launch file.
        self.UDP_IP = get_ip.get_local()
        #if self.UDP_IP != 'localhost':
        #    self.UDP_IP = int(self.UDP_IP)
        self.UDP_PORT = int(rospy.get_param('~UDP_PORT', '49154'))

        # Create a dynamic reconfigure server.
        #self.server = DynamicReconfigureServer(ConfigType, self.reconfigure)
        
        # create ros::Publisher to send Odometry messages
        cam_pub = rospy.Publisher('image_raw/compressed', CompressedImage)

        #crappy test
        t = True
        while not rospy.is_shutdown():
            #crappy test continued
            if t:
                print "Camera Running"
            t = False

            udp_string = self.receive_packet()
            jpg_string = self.parse_string(udp_string)

            cam_msg = CompressedImage()
            cam_msg.header.stamp = rospy.Time.now() #YOYOYOYO - should be from robot time
            cam_msg.format = "jpeg"
            cam_msg.data = jpg_string

            cam_pub.publish(cam_msg)

    def receive_packet(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.bind((self.UDP_IP, self.UDP_PORT))
        packet, addr = sock.recvfrom(100000) # buffer size is not 1024 bytes

        return packet

    def parse_string(self, s):
        full_string = s
        ind = full_string.find('\xFF\xD8')
        parsed = full_string[ind:]

        return parsed


if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('cam') #ros::NodeHandle n;

    try:
        cn = CamNode()
    except rospy.ROSInterruptException: 
        pass
