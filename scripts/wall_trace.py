#!/usr/bin/env python
import rospy, math
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.msg import LightSensorValues

class WallTrace():
    def __init__(self):
        self.cmd_vel = rospy.Publisher('/cmd_vel',Twist,queue_size=1)

        self.sensor_values = LightSensorValues()
        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)

    def callback(self,messages):
        self.sensor_values = messages

    def run(self):
        rate = rospy.Rate(20)
        d = Twist()
    
        accel = 0.02
        while not rospy.is_shutdown():
            s = self.sensor_values
            d.linear.x += accel
    
            if s.sum_forward >= 50: d.linear.x = 0.0
            elif d.linear.x <= 0.2: d.linear.x = 0.2
            elif d.linear.x >= 0.8: d.linear.x = 0.8
    
            if d.linear.x < 0.2:   d.angular.z = 0.0
            elif s.left_side < 10: d.angular.z = 0.0
            else:
                target = 50
                error = (target - s.left_side)/50.0
                d.angular.z = error * 3 * math.pi / 180.0
    
            self.cmd_vel.publish(d)
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('wall_trace')
    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/motor_off')
    rospy.on_shutdown(rospy.ServiceProxy('/motor_off',Trigger).call)
    rospy.ServiceProxy('/motor_on',Trigger).call()
    WallTrace().run()
