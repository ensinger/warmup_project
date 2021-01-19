#!/usr/bin/env python3

import rospy

#msgs for /cmd_vel
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from math import radians

# How many meters on the side of a square?
distance = 1

class drawSquare(object):
    """ This node draws a square with the robot """
    def __init__(self):
        #start rospy node
        rospy.init_node("draw_Square")

        #on control-c shutdown
        rospy.on_shutdown(self.shutdown)

        # get a publisher to the cmd_vel topic
        self.twist_pub= rospy.Publisher("/cmd_vel", Twist, queue_size = 10)
        #use 10 Hz update rate
        r = rospy.Rate(10)

        #Create a default twist msg to move forward
        moveForward = Twist()
        moveForward.linear.x = 0.25 #.25 meters per second
        #Create another twist msg to turn at 90 degrees / second
        turnLeft = Twist()
        turnLeft.angular.z = radians(90)

        turnCounter = 0
        while not rospy.is_shutdown(): #do forever until shutdown
            #40 updates at 10/sec = 4 seconds
            #4 secs at 0.25 m/sec = 1 meter
            for i in range (0,40):
                self.twist_pub.publish(moveForward)
                r.sleep()
            self.twist_pub.publish(Twist())

            #now turn left for 10 updates at 10 updates/sec = 1 second
            #1 second at 90 degrees/sec = 90 degrees
            for i in range (0,10):
                self.twist_pub.publish(turnLeft)
                r.sleep()
            self.twist_pub.publish(Twist())

            rospy.loginfo("Turn: " + str(turnCounter))
            turnCounter = turnCounter + 1

    def run(self):
        #keep the program alive
        rospy.spin()

    def shutdown(self):
        rospy.loginfo("Stop the draw square node")
        self.twist_pub.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    #Declare a node and run it
    node = drawSquare()
    node.run()
