import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Float64

class StateSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(Float64MultiArray,'State',self.listener_callback, 10)
        self.subscription
    def listener_callback(self, msg):
        x = msg.data[0]
        y = msg.data[1]
        z = msg.data[2]
        x_vel = msg.data[3]
        y_vel = msg.data[4]
        z_vel = msg.data[5]
        self.get_logger().info(f'States recieved: :{[x, y, z, x_vel, y_vel, z_vel]}')  # CHANGE

def main(args=None):
    rclpy.init(args=args)
    subscriber = StateSubscriber()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
