#!/usr/bin/env python
import rospy,copy,numpy,time
import RPI.GPIO as GPIO
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.msg import LightSensorValues
from getch import getch, pause

GPIO.setmode(GPIO.BCM)
pin = 4

class WallStop():
    def __init__(self):
        self.cmd_vel = rospy.Publisher('/cmd_vel',Twist,queue_size=1)
        self.goahead_param = 500
        self.back_param = 1000
        self.sensor_values = LightSensorValues()
        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)
        self.M = 0.10
        self.M1 = 0.00
        self.e = 0.00
        self.e1 = 0.00
        self.e2 = 0.00
        self.goal = 600
        self.Kp = 0.0002
        self.Ki = 0.000025
        self.Kd = 0.00010

    def callback(self,messages):
        self.sensor_values = messages

    def callBackTest(channel):
        print ("callback")

    GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callBack=callBackTest, bouncetime=300)

    try:
        while(Trure):
            time.sleep(1)

    except KeyboardInterrpt:
        print("break")
        GPIO.cleanup()
    def run(self):
        rate = rospy.Rate(10)
        data = Twist()
        data.linear.x = 0.00

        while not rospy.is_shutdown():
            key = ord(getch())
            if key == 65:
                data.linear.x = 0.1
            elif key == 66:
                data.linear.x = -0.1
            elif key == 67:
                data.linear.y = 0.1
            elif key == 68:
                data.linear.y = -0.1
            elif key == 13:
                print ("Enter")
                break
            else: pause()
            """self.M1 = self.M
            self.e2 = self.e1
            self.e1 = self.e
            self.e = self.goal - self.sensor_values.sum_all
            
            #self.M = self.M1 + self.Kp * (self.e-self.e1)
            #self.M = self.M1 + self.Kp * (self.e-self.e1) + self.Kd * ((self.e-self.e1) - (self.e1-self.e2))
            self.M = self.M1 + self.Kp * (self.e-self.e1) + self.Ki * self.e + self.Kd * ((self.e-self.e1) - (self.e1-self.e2))            
            if self.sensor_values.sum_all < self.goahead_param:
                data.linear.x = 0.2
            elif self.sensor_values.sum_all > self.back_param:
                data.linear.x = -0.2
            else: data.linear.x = 0.0
            if self.M < 0.25 and self.M > -0.25:
                data.linear.x = self.M
            #else: data.linear.x = 0.0
            #print('move param_____________' + str(self.M))"""
            self.cmd_vel.publish(data)
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('wall_stop')
    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/motor_off')
    rospy.on_shutdown(rospy.ServiceProxy('/motor_off',Trigger).call)
    rospy.ServiceProxy('/motor_on',Trigger).call()
    WallStop().run()
