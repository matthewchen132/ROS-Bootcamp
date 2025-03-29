import rclpy
from rclpy.node import Node
import numpy as np
import math
from turtlesim.srv import Spawn, Kill
import turtlesim
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class spawnTurtle(Node):
    def __init__(self):
        super().__init__("cleaner_turtle")
    # clear screen of turtles:
    # ros2 service call /kill turtlesim/srv/Kill "{name: 'turtle1'}"
        # self.clear_screen = self.create_client(Kill, "\")
        self.clear = self.create_client(Kill, "/kill")
        self.clear_screen()

    # Node will access the turtlesim service "Spawn" to create a turtle
        # First, create a client to access communication to the service
        self.spawn = self.create_client(Spawn, "/spawn")
        # next, send commands to spawn a turtle using "Spawn.Request"
        self.spawn_turtle(5.0, 5.0, 0.0, "Cleaner")

    # Position turtle
        self.x = 6.0
        self.y = 6.0
        self.theta = 90.0
        self.vx = 0.0
        self.vy = 0.0
        self.radius_cleaned = math.sqrt((self.x-5.0)**2 + (self.y-5.0)**2)
        self.velocity_scale = 1.0
        
        # Topic subscriptions:
        self.position = self.create_subscription(Pose, "/Cleaner/pose", self.get_position,10)
        self.publish_velocity = self.create_publisher(Twist,"/Cleaner/cmd_vel", 10)

        # Create the timers (looping commands)
        self.create_timer(.1, self.clean) # initiates spiral motion

    def spawn_turtle(self,x,y,theta,name):
        # With a client created, we can now send requests to the Spawn service
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = name
        request_result = self.spawn.call_async(request)
        rclpy.spin_until_future_complete(self, request_result)
    def clear_screen(self):
        request = Kill.Request()
        request.name = "turtle1"
        request_result = self.clear.call_async(request)
        rclpy.spin_until_future_complete(self, request_result)     
    def get_position(self,msg):
        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta
        self.get_logger().info(f" (R, theta (degrees)){round(self.radius_cleaned,3), round(normalize_angle_degrees(self.theta), 3)}")
    def clean(self):
        self.radius_cleaned = math.sqrt((self.x-5.0)**2 + (self.y-5.0)**2)

        msg = Twist()
        msg.linear.x = 6.0*self.velocity_scale
        msg.angular.z = 5*math.pi
        self.velocity_scale += .15


        # v_theta = 10
        # msg.linear.x, msg.angular.y = self.radial_conversion(v_theta,self.theta)
        # msg.angular.z = v_theta/self.radius_cleaned
        
        if(abs(self.radius_cleaned -5.0) < 0.03):# at a radius of 5, stop.
            msg.linear.x = 0.0
            msg.linear.y = 0.0
            msg.angular.z = 0.0


        # store previous coords:
            # previous_theta = self.theta
            # if(self.theta > )

        self.publish_velocity.publish(msg)

    def radial_conversion(self,v_theta, theta):
        # Polar coords Vr conversion -> x and y space
        self.vx = -v_theta*math.cos(self.theta)
        self.vy = v_theta*math.sin(self.theta)
        return self.vx, self.vy
    
def normalize_angle_degrees(angle):
    #normalizes an angle (in rads)
    return math.degrees(((angle+ math.pi) % (2*math.pi) -math.pi))



    
def main(args=None):
    rclpy.init(args=args)
    turtle = spawnTurtle()
    rclpy.spin(turtle)
    turtle.destroy_node
    rclpy.shutdown()

if __name__ == "__main__":
    main()