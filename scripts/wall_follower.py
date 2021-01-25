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
rotspeed = 45*math.pi/180 #turn 45 degrees/second

class follow_Wall(object):
    """ This node walks the robot to the wall and stops """

    def __init__(self):
        #Start rospy node
        rospy.init_node("walk_to_wall")

        #Declare node as a subscriber to the scan topic and
        # set self.process_scan as the function to be used for callback
        rospy.Subscriber("/scan", LaserScan, self.process_scan)

        #Get a publisher to the cmd_vel topic
        self.twist_pub = rospy.Publisher ("/cmd_vel", Twist, queue_size = 10)

        #Create a default twist msg (all values 0)
        lin = Vector3()
        ang = Vector3()
        self.twist = Twist(linear = lin, angular = ang)
        self.state = 0 #0 go forward to wall, 1 turn left, 2 follow wall

    def goto_wall(self,data):
        self.twist.linear.x = speed
        if data.ranges[0] > distance:
            self.twist.linear.x = speed
        else:
            #Close enough to wall, stop.
            self.twist.linear.x = 0
            self.state = 1 # time to turn left now that we found wall

    def turn_left(self,data):
        self.twist.linear.x = 0
        if(data.ranges[0] < 4*distance):
            self.twist.angular.z = rotspeed
            self.state = 1
        else:
            self.twist.linear.x = 0
            self.twist.angular.z = 0
            self.state = 2

    def follow_wall(self,data):
        # speed to move forward to find the next wall
        if data.ranges[0] > distance: # if we are far enough from the next wall
            #look on the right side of robot so we can hug the wall on the right
            range_data = np.array(data.ranges[225:315]) #90 degree sector on right
            midval = range_data[45] # distance on right hand side at midpoint
            err = (range_data[0]-range_data[-1]) #this fixes the wandering!
            err = err+2*(distance - midval) #if neg than too far, pos, then too close
            self.twist.angular.z = err/5 # this is the Kp proportional feedback term
            self.twist.linear.x = speed
            self.state = 2
        else:
            #close enough to wall, stop.
            self.twist.linear.x = 0
            self.twist.angular.z = 0
            self.state = 1 # time to turn left now that we found wall

    def process_scan(self,data):
        if self.state == 0:
            self.goto_wall(data)
        elif self.state == 1:
            self.turn_left(data)
        else:
            self.follow_wall(data)

        #publish msg to cmd_vel.
        self.twist_pub.publish(self.twist)

    def run(self):
        #keep the program alive
        rospy.spin()

if __name__ == '__main__':
    #Declare a node and run it.
    node = follow_Wall()
    node.run()


            
        
