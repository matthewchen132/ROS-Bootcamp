import rclpy
from rclpy.node import Node
import numpy as np
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from turtlesim.msg import Pose
from math import atan2, sqrt, pi
import time

class velocityPublisher(Node): # node that has a publisher to publish velocities for cmd_vel, the velocity topic
# publishes commands to the /turtle1/cmd_vel publisher through velocityPublisher
    def __init__(self):
        super().__init__('velocity_publisher') # initialize a node
        self.x_current = 0.0
        self.y_current = 0.0
        self.theta_current = 0.0

        #goal
        self.x_goal = 10*np.random.random()
        self.y_goal = 10*np.random.random()
        self.theta_goal = 2*pi*np.random.random()

        # timer
        self.loop_delay = .2
        self.timer = self.create_timer(self.loop_delay, self.timer_callback)

        # Gets current x,y, and angle.
        self.position_subscription = self.create_subscription(Pose, '/turtle1/pose',self.get_position, 10) # note: .cmd(...) will call the function, .cmd without () will pass a reference, 

        # create velocity publisher
        self.publish_velocity = self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        
    def get_position(self, msg):
        try:
            self.x_current = float(msg.x)
            self.y_current = float(msg.y)
            self.theta_current = float(msg.theta)
            vel = msg.linear_velocity
            ang_vel = msg.angular_velocity
            position = [self.x_current, self.y_current, self.theta_current]
        except AttributeError:
            self.get_logger().info("invalid states receieved.")
        # self.get_logger().info(f'X, Y, angular_velocity: {position}')

    def timer_callback(self):
        # randomly generate a a new goal 0,0 to 10,10
        x_goal = self.x_goal#*np.random.ran()
        y_goal = self.y_goal#*np.random.uniform()
        theta_goal = self.theta_goal
        # 1) subscribe to position to get current position.
        x_dist = x_goal - self.x_current 
        y_dist = y_goal - self.y_current
        theta_approach = atan2(y_dist,x_dist)
        self.get_logger().info(f'Goal (x,y, theta): {x_goal, y_goal, theta_goal}')
        distance_to_goal = sqrt(x_dist**2 + y_dist**2)

        # create a command to cmd_vel, proportional controller
        move_turtle = Twist()
        if(theta_approach-self.theta_current > 0.2):
            # First, set the linear movement to 0, and then move angle to correct trajectory
            move_turtle.linear.x = 0.0
            move_turtle.angular.z = 2*(theta_approach-self.theta_current)

        else:
            move_turtle.linear.x = 0.5*distance_to_goal 
            if distance_to_goal < 0.01:
                # if close enough, stop moving, and start rotating until we reach the goal.
                move_turtle.linear.x = 0.0
                move_turtle.angular.z = 3*theta_goal-self.theta_current
                self.get_logger().info(f"Positional goal reached!")
                self.get_logger().info(f"current distance to goal:{distance_to_goal}")
                if theta_goal-self.theta_current < 0.1:
                # if the angle becomes close enough, stop moving, angular goal is reached.
                    move_turtle.angular.z = 0.0
                    self.get_logger().info(f"angular goal reached!")
                    self.get_logger().info(f"current angle to goal (rads):{(theta_goal-self.theta_current)}")
                    # log the time it took to reach the goal
                    # _______
                    # create a new goal once we reach ten seconds
                    self.get_logger().info(f"NEW GOAL GENERATED")
                    self.x_goal = 10*np.random.random()
                    self.y_goal = 10*np.random.random()
                    self.theta_goal = 2*pi*np.random.random()


        self.get_logger().info(f'current angle {self.theta_current}')
        self.get_logger().info(f'x_error: {x_dist} y_error {y_dist}')
        self.publish_velocity.publish(move_turtle)



def main(args=None):
    rclpy.init(args=args)
    velocity_pub = velocityPublisher()
    rclpy.spin(velocity_pub)

    # prevent unnecessary resource allocation
    velocity_pub.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()