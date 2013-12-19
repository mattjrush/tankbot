#!/usr/bin/env python

import socket
import time

import rospy
import roslib

from sensor_msgs.msg import Joy
from std_msgs.msg import String

class SendJoy:

    def __init__(self):
        # Get the ~private namespace parameters from command line or launch file.
        self.UDP_IP = rospy.get_param('~UDP_IP', '192.168.50.9')
        self.UDP_PORT = int(rospy.get_param('~UDP_PORT', '7070'))
        self.word = rospy.get_param('~command_delay', .25)
        velocityThreshold = 30

        rospy.init_node('joy_joy')
        joyPub = rospy.Publisher('joy_joy', String)
        self.lastVelocityCommand = [0,0]
        self.lastMessageTime = time.clock()

    def joystick_send(self, string_data):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        sock.sendto(string_data, (UDP_IP, UDP_Port))
        self.lastMessageTime = time.clock()
        joyPub.publish(String(string_data))

    def SpecialWord (self):
        if abs(self.lastVelocityCommand[0]) < velocityThreshold:
            self.lastVelocityCommand[0] = 0
        if abs(self.lastVelocityCommand[1]) < velocityThreshold:
            self.lastVelocityCommand[1] = 0

    def SendLastVelocityCommand(self):
        SpecialWord()
        joystick_send(str(self.lastVelocityCommand[0]) + '%' + str(self.lastVelocityCommand[1]))
        

    def IsAheadUsed(self, AheadCheck):
        if AheadCheck != 1:
            return True
        else:
            return False
        
    def IsReverseUsed(self, ReverseCheck):
        if ReverseCheck !=1:
            return True
        else:
            return False


    def CalculateAheadCommand(self, throtleCommand):
        treadsAhead = 500*(-1*throtleCommand+1)
        return [treadsAhead,treadsAhead]    

    def CalculateReverseCommand(self, throtleCommand):
        treadsReverse = -500*(-1*throtleCommand+1)
        return [treadsReverse,treadsReverse]

    def StopMotionCommand(self):
        return [0,0]


    def ReceiveAndSendToRecipient(self, joy_data):

        leftTread = float(joy_data.axes[1])
        rightTread = float(joy_data.axes[4])
        rightThrottle = float(joy_data.axes[5])
        leftThrottle = float(joy_data.axes[2])
        precisionMotionButton = int(joy_data.buttons[5])
        stopMotionButton = int(joy_data.buttons[1])
        
        if stopMotionButton != 0:
            self.lastVelocityCommand = StopMotionCommand()
        elif IsAheadUsed(rightThrottle):
            self.lastVelocityCommand = CalculateAheadCommand(rightThrottle)
        elif IsReverseUsed(leftThrottle): 
            self.lastVelocityCommand = CalculateReverseCommand(leftThrottle)
        elif precisionMotionButton == 1: 
            precisionFactor = 200
            self.lastVelocityCommand = [precisionFactor*leftTread,precisionFactor*rightTread]
        else:
            velocityFactor = 500 
            self.lastVelocityCommand = [velocityFactor*leftTread,velocityFactor*rightTread]
        
        if IsTimerExpired(timeBetweenCommands):        
            SendLastVelocityCommand()

    def IsTimerExpired(self, timeBetweenCommands):
        if time.clock() - self.lastMessageTime > timeBetweenCommands:
            return True
        else:
            return False 
    
    def update(self):
        rospy.Subscriber('/joy', Joy, self.ReceiveAndSendToRecipient)
        rospy.spin()

if __name__ == '__main__':
    
    try:
        joy = SendJoy()
        joy.update()

    except rospy.ROSInterruptException: 
        pass

    # while not rospy.is_shutdown():
    #     if IsTimerExpired(timeBetweenCommands):
    #         SendLastVelocityCommand()    