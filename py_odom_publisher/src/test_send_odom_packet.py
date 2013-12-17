import socket
import time

import rospy

def send_packet(string_data):

    UDP_IP = "localhost"
    UDP_Port = 49152
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.sendto(string_data, (UDP_IP, UDP_Port))   

def generate_message(bob):

    if bob:
        odom_string = "0%10%90"
    else:
        odom_string = "1%10%90"
    
    return odom_string

bob = True
while not rospy.is_shutdown():

    pack = generate_message(bob)
    send_packet(pack)
    bob = not bob #poor bob is confused

    time.sleep(1)






