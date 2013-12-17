#!/usr/bin/env python

import math
import socket

import roslib #roslib.load_manifest('odom_publisher')
import rospy
import tf

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Quaternion #msg.pose.pose.position = Point(self.x, self.y, self.z) and msg.pose.pose.orientation = Quaternion(*(kdl.Rotation.RPY(R, P, Y).GetQuaternion()))

#import get_ip

def receive_packet():
    UDP_IP = "192.168.48.72" #get_ip.get_local()
    #UDP_IP = 'localhost' #TEST CODE
    UDP_PORT = 49152

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    packet, addr = sock.recvfrom(100000) # buffer size is not 1024 bytes
    print packet

    return packet

# create ros::Publisher to send Odometry messages
rospy.init_node("odom") #ros::NodeHandle n;
odom_pub = rospy.Publisher('odom', Odometry) # node publishing Odometry to 'odom'
odom_br = tf.TransformBroadcaster() #or without the tf.

x = 0
y = 0
th = 0

#crappy test
t = True
while not rospy.is_shutdown():
#    scanBroadcaster.sendTransform(
#    scanBroadcaster.sendTransform(
#    (0, 0, 0), 
#    (0, 0, 0, 1),
#    rospy.Time.now(),
#    "base_scan",
#    "base_link"
#    )

    odom_string = receive_packet()
    data = odom_string.split("%")

    changer = int(data[0])
    dist = float(data[1])
    angle = math.radians(float(data[2]))
    
    if changer == 0:
        x += dist * math.cos(th)
        y += dist * math.sin(th)
    elif changer == 1:
        th += angle

    #since all odometry is 6DOF we'll need a quaternion created from yaw
    odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)

    stamp = rospy.Time.now()
    parent = "odom"
    child = "base_link"

    #create ROS odometry message
    odom_msg = Odometry()
    odom_msg.header.stamp = stamp
    odom_msg.header.frame_id = parent
    odom_msg.child_frame_id = child

    #set the position
    odom_msg.pose.pose.position.x = x
    odom_msg.pose.pose.position.y = y
    odom_msg.pose.pose.position.z = 0.0
    odom_msg.pose.pose.orientation.x = odom_quat[0]
    odom_msg.pose.pose.orientation.y = odom_quat[1]
    odom_msg.pose.pose.orientation.z = odom_quat[2]
    odom_msg.pose.pose.orientation.w = odom_quat[3]

    #set the velocity
    odom_msg.twist.twist.linear.x = 0
    odom_msg.twist.twist.linear.y = 0
    odom_msg.twist.twist.angular.z = 0

    #publish the Ros odometry message
    odom_pub.publish(odom_msg)

    #publish the transform over tf
    odom_br.sendTransform((x, y, 0), odom_quat, stamp, child, parent)

    #crappy test continued
    if t:
        print "Odometry Running"
        print odom_msg
    t = False
