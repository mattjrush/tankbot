#!/usr/bin/env python

#Example from: http://forums.trossenrobotics.com/printthread.php?t=4304&pp=10&page=8

import socket

import roslib; ##roslib.load_manifest('pi_robot')
import rospy

from std_msgs.msg import String

#import get_ip

def receive_packet():
    #UDP_IP = "192.168.48.72" #get_ip.get_local()
    UDP_IP = 'localhost' #TEST CODE    
    UDP_PORT = 49151
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    packet, addr = sock.recvfrom(100000) # buffer size is not 1024 bytes

    return packet

def separate(rstring, choice):

    package = rstring.split(";")
    if choice == "encoders":
        return package[:2]
    elif choice == "lidar":
        return package[2:]

# create ros::Publisher to send LaserScan messages
rospy.init_node("seperator") #ros::NodeHandle n;
scanPub = rospy.Publisher('lidar_vals', String) # node publishing LaserScan to 'base_scan'
#scanBroadcaster = TransformBroadcaster()
wheelPub = rospy.Publisher('encoder_vals', String)

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

    #wheels = String()
    #scan = String()    

    robot_string = receive_packet()
    wheels = str(separate(robot_string, "encoders"))
    scan = str(separate(robot_string, "lidar"))

    # wheelPub.publish(wheels)
    # scanPub.publish(scan)
    wheelPub.publish(wheels)
    scanPub.publish(scan)

    #crappy test continued
    if t:
        print "Lidar Running"
        # print scan
        # print wheels
    t = False




































