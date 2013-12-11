#!/usr/bin/env python

import roslib 
#roslib.load_manifest('')
import rospy

import tf

class TfNode:
    """docstring for TfNode"""
    def __init__(self, arg):
        self.parent = rospy.get_param('~parent', 'base_link')
        self.child = rospy.get_param('~child', 'base_scan')
        self.x = int(rospy.get_param('~offset_x', 0))
        self.y = int(rospy.get_param('~offset_y', 0))
        self.z = int(rospy.get_param('~offset_z', 0))

        tf_pub = tf.TransformBroadcaster()
		
        r = rospy.Rate(100)
        while not rospy.shutdown():
            tf.sendTransform((self.x, self.y, self.z),
                tf.transformations.quaternion_from_euler(0, 0, 0, 1),
                rospy.Time.now(), self.parent, self.child)
            r.sleep()

if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('tf_publisher') #ros::NodeHandle n;

    try:
        tfn = TfNode()
    except rospy.ROSInterruptException: 
        pass