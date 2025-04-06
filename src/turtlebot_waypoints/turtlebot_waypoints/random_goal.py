import rclpy
from rclpy.node import Node
import numpy as np
from math import pi, atan2, cos, sin, sqrt
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


class path_planner(Node):
    def __init__(self):
        super().__init__("Turtlebot")
        self.x= 0.0
        self.y= 0.0
        # generate a random goal
        self.goal_x = 10*np.random.random()
        self.goal_y = 10*np.random.random()
        self.theta = normalize_angle(2*pi*np.random.random())

        # get position -> subscribe to the /odom topic
        self.sub_odom = self.create_subscription(Odometry,"/odom", self.get_odom, 10)

        # create the initial trajectory:

        # create a publisher to /cmd_vel
        self.cmd_vel = self.create_publisher(Twist, "/cmd_vel",10)

        # create our looping function
        timestep = 0.01
        self.timer = self.create_timer(timestep, self.loop)

    def generate_goal(self):
        self.goal_x = 10*np.random.random()
        self.goal_y = 10*np.random.random()
        self.goal_theta = 2*pi*np.random.random()
        self.trajectory 

    
    def generate_path_to_goal(self):
        '''Creates a path of 100 "waypoints" from initial position to final goal.
           Does this by finding trajectory from x_i,y_i to goal position, then generating
           a 2D array of x,y of points from this x_i, y_i to the goal'''
        C1 = 0.0
        x_dist = self.goal_x - self.x
        y_dist = self.goal_y - self.y

        traj = atan2(y_dist, x_dist) # trajectory
        path = [] # first, initialize an empty  list
        
        # datapoint ex:
        while C1 <= 1:
            x = self.x + C1*cos(traj)*x_dist
            y = self.y + C1*sin(traj)*y_dist
            path.append([x, y])
            C1 += 0.01
        return np.array(path)

    def convert_quaternion(self,x,y,z,w):
        ''' converts quaternions into cartesian angles'''
        # TODO
        angles = 0.0
        return angles

    def get_odom(self, odometry_msg):
        ''' Updates the current x y position of the robot
            and prints a rounded value of the x y position.'''
        self.x = odometry_msg.pose.pose.position.x
        self.y = odometry_msg.pose.pose.position.y

        # orientation (quaternion)
        self.theta = self.convert_quaternion(odometry_msg.pose.pose.orientation.x, 
                                odometry_msg.pose.pose.orientation.y, 
                                odometry_msg.pose.pose.orientation.z,
                                odometry_msg.pose.pose.orientation.w)
        self.get_logger().info(f" Retrieved (X,Y, theta): {round(self.x, 3), round(self.y,3), round(self.theta)},") # implement theta later

    def loop(self):
        '''Pure Pursuit Controller'''
        # first, find lookahead distance & planned path
        lookahead_dist = 0.5# tunable lookahead distance
        goal_path = self.generate_path_to_goal()
        for i in range(len(goal_path)):
            # loop through goal paths and current positions, 
            # finding the lowest point which is > than lookahead distance
            x_path = goal_path[i,0]   
            y_path = goal_path[i,1]
            dist_path = sqrt( (x_path-self.x)**2 + (y_path - self.x)**2)

            if dist_path >= lookahead_dist:
                # finds the first point in path larger than lookahead dist
                self.pursuit_x = goal_path[i,0]
                self.pursuit_y = goal_path[i,1]
                self.get_logger().info(f"Pursuing the point: {round(self.pursuit_x, 3), round(self.pursuit_y,3)}" )
                break

        # pseudocode
        # 1: control the robot to the lookahead point by creating a msg to cmd/vel
        msg = Twist()
        # find goal trajectory:
        self.theta_approach = normalize_angle(atan2(self.pursuit_y-self.xy, self.pursuit_x-self.x))
        # Define angular errors:
        theta_error = self.theta_approach - self.theta
        msg.angular.z = 1.0*theta_error # P control for now
        
        msg.linear.x = 1.0

        self.cmd_vel.publish(msg=msg)
        self.get_logger().info('Loop is running')
def normalize_angle(angle):
        '''Normalizes angle between -pi to pi'''
        return (angle + pi) % (2*pi) - pi
def main():
    rclpy.init()
    chaser = path_planner()
    rclpy.spin(chaser)
    rclpy.shutdown()
    