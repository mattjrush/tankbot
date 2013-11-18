
#Example from: http://forums.trossenrobotics.com/printthread.php?t=4304&pp=10&page=8

import roslib; roslib.load_manifest('pi_robot')
import rospy
from sensor_msgs.msg import LaserScan
from tf.broadcaster import TransformBroadcaster

rospy.init_node("base_scan")
scanPub = rospy.Publisher('base_scan', LaserScan)
scanBroadcaster = TransformBroadcaster()

scan_rate = 1
rate = rospy.Rate(scan_rate)

rospy.loginfo("Started base scan at " + str(scan_rate) + " Hz")

while not rospy.is_shutdown():
#    scanBroadcaster.sendTransform(
#    (0, 0, 0), 
#    (0, 0, 0, 1),
#    rospy.Time.now(),
#    "base_scan",
#    "base_link"
#    )
    
    ranges = list()
    
    for i in range(30):
        ranges.append(5)
    
    scan = LaserScan()
    scan.header.stamp = rospy.Time.now()        
    scan.header.frame_id = "base_link"
    scan.angle_min = -1.57
    scan.angle_max = 1.57
    scan.angle_increment = 0.108275862
    scan.scan_time = scan_rate
    scan.range_min = 0.5
    scan.range_max = 6.0
    scan.ranges = ranges    
    scanPub.publish(scan)

    rate.sleep()
