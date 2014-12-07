#!/usr/bin/env python
# works for Dualshock 4
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy


tiltAng = float()
speedIdx = int()
speed = [1.0, 0.5, 0.1]

def joystickCallback(joyData):
	global tiltAng, speedIdx
	t = Twist()
	if joyData.buttons[3]:
		speedIdx = (speedIdx + 1) % 3
		rospy.loginfo("%d", speedIdx)
	t.angular.z = speed[speedIdx] * joyData.axes[0]
	t.linear.x = speed[speedIdx] * joyData.axes[1]
	tiltAng = tiltAng - 0.1 * joyData.axes[5]
	if tiltAng < -30:
		tiltAng = -30
	elif tiltAng > 30:
		tiltAng = 30
	rospy.loginfo("%f %f %f", t.linear.x, t.angular.z, tiltAng)
	velPub.publish(t)
	tiltPub.publish(Float64(tiltAng))

def service():
	global velPub, tiltPub
	velPub = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size = 1)
	tiltPub = rospy.Publisher('/tilt_angle', Float64, queue_size = 1)
	sub = rospy.Subscriber('/joy', Joy, joystickCallback, queue_size = 10)
	rospy.init_node('p3dx_joystick')
	rospy.spin()

if __name__ == '__main__':
	try:
		service()
	except rospy.ROSInterruptException: pass
		
