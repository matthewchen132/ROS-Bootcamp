import rclpy
from rclpy.node import Node
import numpy as np
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from turtlesim.msg import Pose
from math import atan2, sqrt, pi
import math
import time
from turtlesim.srv import Spawn

# 1 DEGREE ERROR + .04 POSITION ERROR IS USUALLY GUARANTEED IN 8 SECONDS



class velocityPublisher(Node): # node that has a publisher to publish velocities for cmd_vel, the velocity topic
# publishes commands to the /turtle1/cmd_vel publisher through velocityPublisher
    def __init__(self):
        super().__init__("velocity_publisher") # initialize a node
        self.x_current = 0.0
        self.y_current = 0.0
        self.theta_current = 0.0
        self.integral_error_approach = 0.0
        self.position_reached = False
        self.angle_reached = False

        #goal
        self.x_goal = 10*np.random.random()
        self.y_goal = 10*np.random.random()
        self.theta_goal = 2*pi*np.random.random()
        self.get_logger().info(f"Goal (x,y, theta): {self.x_goal, self.y_goal, math.degrees(self.theta_goal)}")

        # timer
        self.loop_delay = .01
        self.timer = self.create_timer(self.loop_delay, self.timer_callback)
        
        # creates a new goal / status update every 10 seconds
        self.generate_goal = self.create_timer(8, self.generate_new_goal)

        #loop timer
        self.new_goal_time = None

        # Gets current x,y, and angle.
        self.position_subscription = self.create_subscription(Pose, "/turtle1/pose",self.get_position, 10) # note: .cmd(...) will call the function, .cmd without () will pass a reference, 

        # create velocity publisher
        self.publish_velocity = self.create_publisher(Twist,"/turtle1/cmd_vel",10)

        

    def get_position(self, msg):
        try:
            self.x_current = float(msg.x)
            self.y_current = float(msg.y)
            self.theta_current = float(msg.theta)

        except AttributeError:
            self.get_logger().info("invalid states receieved.")

    def generate_new_goal(self):
        # notify whether criterion was met:
        if self.position_reached:
            self.get_logger().info(f"Positional goal reached!")
        if self.angle_reached: 
            self.get_logger().info(f"Angular goal reached!")
        #print errors
        self.get_logger().info(f"Distance error:{sqrt((self.x_goal-self.x_current)**2+(self.y_goal-self.y_current)**2)}")
        self.get_logger().info(f"Angular error (degrees):{math.degrees(abs(self.theta_goal-self.theta_current))}")
        self.get_logger().info("\n\n")
        # resets the signals
        self.position_reached = False
        self.angle_reached = False
        self.x_goal =  10*np.random.random()
        self.y_goal =  10*np.random.random()
        self.theta_goal =  2*pi*np.random.random()
        self.get_logger().info(f"New Goal Generated(x,y, theta): {self.x_goal, self.y_goal, math.degrees(self.theta_goal)}")


    def timer_callback(self):
        # randomly generate a a new goal 0,0 to 10,10
        x_goal = self.x_goal#*np.random.ran()
        y_goal = self.y_goal#*np.random.uniform()
        theta_goal = self.theta_goal
        # 1) subscribe to position to get current position.
        x_dist = x_goal - self.x_current 
        y_dist = y_goal - self.y_current
        theta_approach = atan2(y_dist,x_dist)
        distance_to_goal = sqrt(x_dist**2 + y_dist**2)
        # create a command to cmd_vel, proportional controller
        move_turtle = Twist()
    
        # start commanding linear and angular velocity
        # PD control for approach angle
        error_approach =normalize_angle(theta_approach)-normalize_angle(self.theta_current)
        move_turtle.angular.z = 3*(error_approach) + 0.04*error_approach/self.loop_delay # PD control prevents overshoot
        move_turtle.linear.x = 2.0*distance_to_goal 
        if distance_to_goal < 0.04:
            # if close enough, stop moving, and start rotating until we reach the goal.
            move_turtle.linear.x = 0.0
            move_turtle.angular.z = 8*(normalize_angle(self.theta_goal)-normalize_angle(self.theta_current))
            self.position_reached = True


            if math.degrees(abs(self.theta_goal-self.theta_current)) < 1 or  (360 - math.degrees(abs(self.theta_goal-self.theta_current)) < 1):
            # if the angle becomes close enough, stop moving, angular goal is reached.
                self.angle_reached = True
                move_turtle.angular.z = 0.0

        # self.get_logger().info(f"current angle to goal (degrees):{math.degrees(normalize_angle(self.theta_goal-self.theta_current))}")
        self.publish_velocity.publish(move_turtle)

def normalize_angle(angle_rads):
        if angle_rads > pi:
            angle_rads -= 2*pi
        elif angle_rads < -pi:
            angle_rads += 2*pi
        return angle_rads

def main(args=None):
    rclpy.init(args=args)
    velocity_pub = velocityPublisher()
    rclpy.spin(velocity_pub)

    # prevent unnecessary resource allocation
    velocity_pub.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()