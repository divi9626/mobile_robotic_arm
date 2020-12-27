#!usr/bin/env/python
import rospy
from std_msgs.msg import Float64
import math
import time

if __name__ == "__main__":
    rospy.init_node ('ik_node')

    pub_armbase = rospy.Publisher('/main_assem/armbase_controller/command', Float64, queue_size = 10)
    pub_arm1 = rospy.Publisher('/main_assem/arm1_controller/command', Float64, queue_size = 10)
    pub_arm2 = rospy.Publisher('/main_assem/arm2_controller/command', Float64, queue_size = 10)
    pub_arm3 = rospy.Publisher('/main_assem/arm3_controller/command', Float64, queue_size = 10)
    pubwheell = rospy.Publisher('/main_assem/back_l_controller/command', Float64, queue_size = 10)
    pubwheelr = rospy.Publisher('/main_assem/back_r_controller/command', Float64, queue_size = 10)

    length = 0.16
    height = 0.2
    l1 = 0.17
    l2 = 0.15
    x = -0.2
    y = 0.24 + length
    z = 0 + height 
    theta1 = math.atan2(x,y)
    
    alpha = math.atan2(z,(math.sqrt((x*x) + (y*y))))
    a = (l2*l2 - l1*l1 - (x*x + y*y))/(-2*l2*math.sqrt(x*x + y*y))
    beta = math.atan2(a, math.sqrt(1 - a*a))
    theta2 = alpha - beta
    

    m = math.sqrt(x*x - y*y) - l1*math.cos(theta2)
    n = z - l2*math.sin(theta2)
    theta3 = math.atan2(n,m) - theta2

    theta4 = -0.1

    r = rospy.Rate(10)
    time_diff = 0
    start_time = time.clock()
    while time_diff <= 10.0:
        pubwheell.publish(100)
        pubwheelr.publish(-100)
        current_time = time.clock()
        time_diff = current_time - start_time
    pubwheell.publish(0)
    pubwheelr.publish(0)
    while not rospy.is_shutdown():
        pub_armbase.publish(theta1)
        pub_arm1.publish(theta2)
        pub_arm2.publish(-theta3)
        pub_arm3.publish(theta4)
        r.sleep()
