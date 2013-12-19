#!/usr/bin/env python

import socket
import sys

import roslib #roslib.load_manifest('')
import rospy

from sensor_msgs.msg import CompressedImage

#import get_ip

def receive_packet():
    #UDP_IP = "192.168.51.175" #get_ip.get_local()
    UDP_PORT = 49155
    UDP_IP = '192.168.50.37' #TEST CODE    
#   UDP_PORT = 49155 #TEST CODE

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    packet, addr = sock.recvfrom(100000) # buffer size is not 1024 bytes
    return packet


def parse_string(s):

    full_string = s
    ind = full_string.find('\xFF\xD8')
    parsed = full_string[ind:]

    return parsed

# create ros::Publisher to send Odometry messages
rospy.init_node("cam") #ros::NodeHandle n;
cam_pub = rospy.Publisher('image_raw/compressed', CompressedImage)

#crappy test
t = True
while not rospy.is_shutdown():
    #crappy test continued
    if t:
        print "Cam Running"
    t = False#    scanBroadcaster.sendTransform(

    udp_string = receive_packet()
    jpg_string = parse(udp_string)

    cam_msg = CompressedImage()
    cam_msg.header.stamp = rospy.Time.now() #should be from robot time
    cam_msg.format = "jpeg"
    cam_msg.data = jpg_string

    cam_pub.publish(cam_msg)
