import rclpy, sys
from rclpy.node import Node
from geometry_msgs.msg import Twist


class SquarePublisher(Node):

    def __init__(self):
        super().__init__('publisher')
        self.publisher = self.create_publisher(Twist, '/robot/cmd_vel', 10)
        timer_period = 2.0  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.move_state = 0

    def timer_callback(self):
        twist = Twist()
        # линейная и угловая скорости
        if self.move_state == 0:
            twist.linear.x = 1.0  # движение вперед
            twist.angular.z = 0.0
            self.move_state += 1
        elif self.move_state == 1:
            twist.linear.x = 0.0  # остановка
            twist.angular.z = 1.0
            self.move_state += 1
        elif self.move_state == 2:
            twist.linear.x = 1.0  # поворот
            twist.angular.z = 0.0
            self.move_state += 1
        elif self.move_state == 3:
            twist.linear.x = 0.0  # остановка
            twist.angular.z = 1.0
            self.move_state += 1
        else:
            twist.linear.x = 1.0  # движение вперед
            twist.angular.z = 0.0
            self.move_state = 0

        self.publisher.publish(twist)


def main(args=None):
    rclpy.init(args=args)

    square_movement = SquarePublisher()

    rclpy.spin(square_movement)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
