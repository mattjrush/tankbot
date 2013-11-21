import socket
import time

import rospy

def send_packet(string_data):

    UDP_IP = "localhost"
    UDP_Port = 49152
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.sendto(string_data, (UDP_IP, UDP_Port))   

def generate_message(r):

    num_readings = 1440
    rate = r

    angle_min = "-60"
    angle_max = "60"
    scan_time = str(rate)
    range_min = "0"
    range_max = str(num_readings)

    ranges = str([i for i in range(num_readings)])

    l = [angle_min, angle_max, scan_time, ranges, range_min, range_max]
    lidar_string = ';'.join(l)
    
    return lidar_string

scan_time = 1
#rospy.init_node('my_node_name')
#r = rospy.Rate(scan_time)
while not rospy.is_shutdown():

    pack = generate_message(scan_time)
    send_packet(pack)

#    r.sleep()
    time.sleep(1)










