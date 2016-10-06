#!/usr/bin/env python  

# This code is a modification of the ros tf-listener tutorial
import roslib
roslib.load_manifest('turtle_social_navigation')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv
from random import randint

#coeffcients of Proportional controller
Kv = 1.75
KTHETA = 4
CONST = -0.7

if __name__ == '__main__':
    rospy.init_node('tf_turtle')

    listener = tf.TransformListener()
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawner(4, 2, 0, 'turtle2')

    #Spawning turtles to create a wall and obstacles
    for i in range(2,6):
        spawner(i, 8 , 0, 'turtle'+str(i*20) )
    for i in range(7,11):
        spawner(i, 4 , 0, 'turtle'+str(i*20) )
    
    spawner(2, 10 , 0, 'turtle3' )
    spawner(3, 6, 0, 'turtle4' )
    spawner(6, 2, 0, 'turtle10' )
    spawner(1, 3, 0,'turtle13' )
    spawner(10, 7, 0,'turtle14' )
    spawner(10, 2, 0,'turtle15' )
    
    turtle_vel_2 = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)
    
    #Movement of obstacles
#    turtle_vel_3 = rospy.Publisher('turtle3/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)
#    turtle_vel_4 = rospy.Publisher('turtle4/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            #transforming information in robot FOR to pedestrian FOR for following Leader action 
            (trans,rot) = listener.lookupTransform('/turtle2', '/turtle1', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
#   This is just a Proportional controller which evaluates the linear velocity based on the distance between the leader
#   and the follower, both objects have their own local frames
        angular = KTHETA * math.atan2(trans[1], trans[0])
        linear = Kv * math.sqrt(trans[0] ** 2 + trans[1] ** 2) + CONST
        cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        turtle_vel_2.publish(cmd)
        
#        cmd.linear.x  = randint(LOWERLIMIT2WALK,UPPERLIMIT2WALK)/DIVIDER
#        cmd.angular.z = randint(LOWERLIMIT2WALK,UPPERLIMIT2WALK)/DIVIDER
#        turtle_vel_3.publish(cmd)
        
#        cmd.linear.x  = randint(LOWERLIMIT2WALK,UPPERLIMIT2WALK)/DIVIDER
#        cmd.angular.z = randint(LOWERLIMIT2WALK,UPPERLIMIT2WALK)/DIVIDER
#        turtle_vel_4.publish(cmd)

        rate.sleep()
