#!/usr/bin/env python

import rospy
import roslib
import socket
from sensor_msgs.msg import Joy
from std_msgs.msg import String
import time

rospy.init_node('joy_joy')
pub = rospy.Publisher('joy_joy', String)
lastVelocityCommand = [0,0]
lastMessageTime = time.clock()

def joystick_send(stringdata):
    global lastMessageTime

    UDP_IP = "192.168.50.9"
    UDP_Port = 7070
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.sendto(stringdata, (UDP_IP, UDP_Port))
    lastMessageTime = time.clock()    
    pub.publish(String(stringdata))

def IsVelocityCommandBelowThreshold ():
    global lastVelocityCommand
    velocityThreshold = 30
    if abs(lastVelocityCommand[0]) < velocityThreshold:
        lastVelocityCommand[0] = 0
    if abs(lastVelocityCommand[1]) < velocityThreshold:
        lastVelocityCommand[1] = 0

def SendLastVelocityCommand():
    global lastVelocityCommand
    IsVelocityCommandBelowThreshold()
    joystick_send(str(lastVelocityCommand[0]) + '%' + str(lastVelocityCommand[1]))

def create_equal(throttle_command, forward): #YOYOYOYO BETTER NAME!!!
    treadsAhead = 500*(-1*throttle_command+1)
    if forward:
        return [treadsAhead, treadsAhead]
    else:
        return [-treadsAhead, -treadsAhead]

def StopMotionCommand():
    return [0,0]

def ReceiveAndSendToRecipient(joy_data):
    global lastVelocityCommand
    global timeBetweenCommands

    left_tread = float(joy_data.axes[1])
    right_tread = float(joy_data.axes[4])
    right_throttle = float(joy_data.axes[5])
    left_throttle = float(joy_data.axes[2])
    precisionMotionButton = int(joy_data.buttons[5])
    stopMotionButton = int(joy_data.buttons[1])
    
    if stopMotionButton != 0:
        lastVelocityCommand = StopMotionCommand()
    elif right_throttle == 1:
        lastVelocityCommand = create_equal(right_throttle, True)
    elif left_throttle == 1: 
        lastVelocityCommand = create_equal(left_throttle, False)
    elif precisionMotionButton == 1: 
        precisionFactor = 200
        lastVelocityCommand = [precisionFactor*left_tread,precisionFactor*right_tread]
    else:
        velocityFactor = 500 
        lastVelocityCommand = [velocityFactor*left_tread,velocityFactor*right_tread]
    
    if IsTimerExpired(timeBetweenCommands):        
        SendLastVelocityCommand()

def IsTimerExpired(timeBetweenCommands):
    if time.clock() - lastMessageTime > timeBetweenCommands:
        return True
    else:
        return False 
    
rospy.Subscriber('/joy', Joy, ReceiveAndSendToRecipient)

while not rospy.is_shutdown():
    timeBetweenCommands = 0.3
    if IsTimerExpired(timeBetweenCommands):
        SendLastVelocityCommand()    

