#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

## Modified by Kapil Sharma
## A simple publisher program is modified to push twist(velocity) messages
## to the turtlesim node, to simulate intoxicated movement

import rospy
#from std_msgs.msg import String
from geometry_msgs.msg import Twist
from random import randint

LOWERLIMIT2WALK = -30
UPPERLIMIT2WALK = 30
DIVIDER = 10
RATE = 10
global LEFT  
RIGHT = False

class talk2turtle():
    def __init__(self):
        #pub = rospy.Publisher('alcohol', String, queue_size=10)
        rospy.init_node('talk2turtle', anonymous=True)    
        rospy.loginfo("I am a drunk Turtle")
        rospy.on_shutdown(self.shutdown)
        rate = rospy.Rate(RATE) # 10hz
        self.cmd_vel = rospy.Publisher('/drunkturtle/turtle1/cmd_vel', Twist, queue_size=10)
        LEFT = True
        # Twist is the datatype for velocity, having angular and linear motion
        #and both have 3D components
        drunk_walk_cmd = Twist() 
        while not rospy.is_shutdown():
            if LEFT==True:
                drunk_walk_cmd.linear.x  = randint(LOWERLIMIT2WALK,UPPERLIMIT2WALK)/DIVIDER
                drunk_walk_cmd.angular.z = randint(LOWERLIMIT2WALK,UPPERLIMIT2WALK)/DIVIDER
                LEFT = False
               # RIGHT = True
            else :
                drunk_walk_cmd.linear.y  = randint(LOWERLIMIT2WALK,UPPERLIMIT2WALK)/DIVIDER
                drunk_walk_cmd.angular.z = randint(LOWERLIMIT2WALK,UPPERLIMIT2WALK)/DIVIDER
                #RIGHT = False
                LEFT  = True
            self.cmd_vel.publish(drunk_walk_cmd)
            #rospy.loginfo(drunk_walk_cmd)
            rate.sleep()
    
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop Pushing Me, I am done walking!!")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)
            

if __name__ == '__main__':
    try:
        talk2turtle()
    except:
        rospy.loginfo("I am Passing Out")  
