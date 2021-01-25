#!/usr/bin/env python3
#TOPICS
#cmd_vel : publish to, used for setting robot velocity
#scan : subscribing, where the wall is
import rospy
import numpy as np
import math

#msg needed for /scan
from sensor_msgs.msg import LaserScan

#msgs needed for /cmd_vel
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

#how close i will get to the wall
distance = 0.5 # stay 1/2 meters away from the wall
speed = 0.25
rotspeed = math.pi #turn 180  degrees/second

class follow_person(object):
    """ This node walks the robot to an object and stops """

    def __init__(self):
        #Start rospy node
        rospy.init_node("walk_to_person")

        #Declare node as a subscriber to the scan topic and
        # set self.process_scan as the function to be used for callback
        rospy.Subscriber("/scan", LaserScan, self.process_scan)

        #Get a publisher to the cmd_vel topic
        self.twist_pub = rospy.Publisher ("/cmd_vel", Twist, queue_size = 10)

        #Create a default twist msg (all values 0)
        lin = Vector3()
        ang = Vector3()
        self.twist = Twist(linear = lin, angular = ang)

    def follow_person(self,data):
        range_data = np.array(data.ranges) #convert to numpy array
        minval = min(range_data) # closest point in space
        mindir = np.argmin(range_data) # find direction to person
        if mindir < 180:
            self.twist.angular.z = rotspeed*(mindir - 0) /180
        else:
            self.twist.angular.z = rotspeed*(mindir-360)/180
        #speed to move forward to find the next person

        if data.ranges[0] > distance: # if we are far enough from the person
            self.twist.linear.x = speed
        else:
            #Close enough to person, stop.
            self.twist.linear.x = 0
            
    def process_scan(self,data):
        self.follow_person(data)
        #publish msg to cmd_vel.
        self.twist_pub.publish(self.twist)

    def run(self):
        #keep the program alive
        rospy.spin()

if __name__ == '__main__':
    #Declare a node and run it.
    node = follow_person()
    node.run()


            
        
