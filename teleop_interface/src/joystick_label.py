import socket
import Tkinter
import rospy
import roslib
from sensor_msgs.msg import Joy
from std_msgs.msg import String

currentState = "rotation"

rotationStored = 0
translationStored = 0

def LabelCreate():
    global joystickMotion
    Tkinter.Label(root, textvariable=joystickMotion).pack()
    

def ReceiveAndSendToRecipient(joy_data):
    global joystickMotion
    global currentState
    global rotationStored
    global translationStored
    rotationJoystick = round(float(joy_data.axes[3]),1)
    translationJoystick = round(float(joy_data.axes[1]),1)
    joystickButtonClicked = int(joy_data.buttons[0]) != 0
    
    if joystickButtonClicked: 
        if currentState == "rotation":
            rotationStored = rotationJoystick            
            currentState = "translation"
        else:
            translationStored = translationJoystick            
            currentState ="rotation"
            IPSendPack(str(rotationStored)+"%"+str(translationJoystick))
 
    rotationDisplay = rotationStored
    translationDisplay = translationStored
    
    if currentState == "rotation":
        rotationDisplay = rotationJoystick
    else:
        translationDisplay = translationJoystick
            
    displayText = "Current State:"+currentState+"\n"
    displayText += "rotation:" + str(rotationDisplay)+"\n"
    displayText += "translation:" + str(translationDisplay)
 
    joystickMotion.set(displayText)
    
def IPSendPack(stringdata):
    UDP_IP = "192.168.50.9"
    UDP_Port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.sendto(stringdata, (UDP_IP, UDP_Port))
    

rospy.init_node('joy_joy')
pub = rospy.Publisher('joy_joy', String)
rospy.Subscriber('/joy', Joy, ReceiveAndSendToRecipient)


root = Tkinter.Tk()
joystickMotion = Tkinter.StringVar()
LabelCreate()
Tkinter.mainloop()



