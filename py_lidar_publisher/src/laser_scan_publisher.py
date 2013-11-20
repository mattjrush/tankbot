
#Example from: http://forums.trossenrobotics.com/printthread.php?t=4304&pp=10&page=8

import roslib; roslib.load_manifest('pi_robot')
import rospy
from sensor_msgs.msg import LaserScan
from tf.broadcaster import TransformBroadcaster

def receive_packet():
    UDP_IP = "192.168.49.197"
    UDP_PORT = 12345
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(100000) # buffer size is not 1024 bytes

def parse_data(data):
    #stuff


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
#float32[] intensities    # intensity data [device-specific units]

# create ros::Publisher to send LaserScan messages
rospy.init_node("base_scan") #ros::NodeHandle n;
scanPub = rospy.Publisher('base_scan', LaserScan) # node publishing LaserScan to 'base_scan'
scanBroadcaster = TransformBroadcaster()


scan_rate = 1 #THIS NEEDS TO BE SET
rate = rospy.Rate(scan_rate)

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
    scan.angle_min = -scan.angle_increment*(num_readings/2);
    scan.angle_max = scan.angle_increment*(num_readings/2);
    scan.angle_increment = 0.00436
    scan.time_increment = (1 / laser_frequency) / (num_readings)
    scan.scan_time = scan_rate
    scan.range_min = 0.0
    scan.range_max = 100.0
    scan.ranges = ranges    
    scanPub.publish(scan)

    rate.sleep()




















