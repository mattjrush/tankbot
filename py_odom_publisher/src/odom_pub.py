#!/usr/bin/env python

import math
import socket
import sys
# sys.path.insert(0, '../')

import roslib #roslib.load_manifest('odom_publisher')
import rospy
import tf

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Quaternion #msg.pose.pose.position = Point(self.x, self.y, self.z) and msg.pose.pose.orientation = Quaternion(*(kdl.Rotation.RPY(R, P, Y).GetQuaternion()))
from std_msgs.msg import Header

#import get_ip

class OdomNode:

    def __init__(self):
        # Get the ~private namespace parameters from command line or launch file.
        self.UDP_IP = "192.168.48.72" #get_ip.get_local()
        self.UDP_PORT = int(rospy.get_param('~UDP_PORT', '49152'))
        self.parent = rospy.get_param('~parent', 'odom')
        self.child = rospy.get_param('~child', 'base_link')

        self.x = 0
        self.y = 0
        self.th = 0
        self.odom_quat = tf.transformations.quaternion_from_euler(0, 0, 0)

        odom_pub = rospy.Publisher('odom', Odometry) # node publishing Odometry to 'odom'
        odom_br = tf.TransformBroadcaster() #or without the tf.

        #crappy test
        t = True
        while not rospy.is_shutdown():

            odom_string = self.receive_packet()
            data = odom_string.split("%")
            self.update_vals(data)

            #create and populate ROS Odometry message
            odom = self.create_odom_msg()

            #publish the Ros odometry message
            self.odom_pub.publish(odom)

            #publish the transform over tf
            self.odom_br.sendTransform((x, y, 0), odom_quat, stamp, child, parent)

            #crappy test continued
            if t:
                print "Odometry Running"
                print odom
            t = False

    def receive_packet(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.bind((self.UDP_IP, self.UDP_PORT))
        packet, addr = sock.recvfrom(100000) # buffer size is not 1024 bytes
        print packet

        return packet

    def create_odom_msg(self):
        #create ROS odometry message
        odom_msg = Odometry()
        odom_msg.header = create_header()
        odom_msg.child_frame_id = self.child

        #set the position
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0
        odom_msg.pose.pose.orientation.x = odom_quat[0]
        odom_msg.pose.pose.orientation.y = odom_quat[1]
        odom_msg.pose.pose.orientation.z = odom_quat[2]
        odom_msg.pose.pose.orientation.w = odom_quat[3]

        #set the velocity YOYOYOYOYOYOYOYOYOYOYO
        odom_msg.twist.twist.linear.x = 0
        odom_msg.twist.twist.linear.y = 0
        odom_msg.twist.twist.angular.z = 0
        
        return odom_msg

    def create_header(self):
        head = Header()
        head.stamp = rospy.Time.now() #YOYOYOYOshould be from robot
        head.frame_id = self.parent

        return head

    def update_vals(self, data):
        changer = int(data[0]) #better name
        dist = float(data[1])
        angle = math.radians(float(data[2]))
        
        if changer == 0:
            self.x += dist * math.cos(th)
            self.y += dist * math.sin(th)
        elif changer == 1:
            self.th += angle

        #since all odometry is 6DOF we'll need a quaternion created from yaw
        odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)

if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node("odom") #ros::NodeHandle n;

    try:
        on = OdomNode()
    except rospy.ROSInterruptException: 
        pass
