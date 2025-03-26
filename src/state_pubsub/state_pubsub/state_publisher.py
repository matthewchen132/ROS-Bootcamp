import rclpy
from rclpy.node import Node
import numpy as np
from std_msgs.msg import Float64, Float64MultiArray

class StatePublisher(Node):

    def __init__(self):
        super().__init__('state_publisher')
        self.states = self.create_publisher(Float64MultiArray, 'State',10)
        timer_period = .5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Float64MultiArray()
        x = round(np.random.random(),3) # reduces Floats to 3 digits for simplicity
        y = round(np.random.random(),3)
        z = round(np.random.random(),3)
        u = round(np.random.random(),3)
        v = round(np.random.random(),3)
        w = round(np.random.random(),3)
        msg.data = [x, y, z, u, v, w]
        self.states.publish(msg)
        self.get_logger().info(f"{msg.data}")

# Main function which initilizes StatePublisher, and publishes 6 states every half second
def main(args=None):
    rclpy.init(args=args)
    state_publisher = StatePublisher()
    rclpy.spin(state_publisher)
    state_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
