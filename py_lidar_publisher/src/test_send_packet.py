import socket
import time

import rospy

def send_packet(string_data):

    UDP_IP = "localhost"
    UDP_Port = 49151
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.sendto(string_data, (UDP_IP, UDP_Port))   

def generate_message(r):

    rate = r

    angle_min = "-60"
    angle_max = "60"
    scan_time = str(rate)
    range_min = "0"
    range_max = str(35000)

    ranges = [10000. for r in range(120*4)]
    ranges_s = str(ranges)

    # for i in range(num_readings):
    #     ranges.append(i)
    #     if i > 15:
    #         i = 0
    # ranges_s = str(ranges)

    l = [angle_min, angle_max, scan_time, ranges_s, range_min, range_max]
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










