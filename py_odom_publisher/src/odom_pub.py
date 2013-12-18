#!/usr/bin/env python

import roslib #roslib.load_manifest('odom_publisher')
import rospy

from std_msgs.msg import Int16
from std_msgs.msg import String

class OdomNode:

    def __init__(self):
        # Get the ~private namespace parameters from command line or launch file.
        self.parent = rospy.get_param('~parent', 'odom')
        self.child = rospy.get_param('~child', 'base_link')

        # Initialize the node and name it.
        rospy.init_node('raw_odom')
        self.lPub = rospy.Publisher('lwheel', Int16) # node publishing LaserScan to 'base_scan'
        self.rPub = rospy.Publisher('rwheel', Int16) # node publishing LaserScan to 'base_scan'

    def string_to_raw_odom(self, O):
        
        raw_odom = O.data
        stripped_odom = raw_odom.translate(None, '[]').translate(None, '"').translate(None, '\'')
        array_odom = stripped_odom.split(",")
        #print package[0]

        l_val = Int16()
        r_val = Int16()

        #print package
        l_val.data = int(array_odom[0])
        r_val.data = int(array_odom[1])

        self.lPub.publish(l_val)
        self.rPub.publish(r_val)
            
    def update(self):
        rospy.Subscriber("encoder_vals", String, self.string_to_raw_odom)
        rospy.spin()

if __name__ == '__main__':

    try:
        on = OdomNode()
        on.update()
    except rospy.ROSInterruptException: 
        pass
