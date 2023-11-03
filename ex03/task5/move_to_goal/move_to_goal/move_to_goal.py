import rclpy
import sys
import math
import time
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from rclpy.node import Node

class TurtleIsMoving(Node):

     def __init__(self):
         super().__init__('move_to_goal')

         self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

         self.subscriber = self.create_subscription(Pose, '/turtle1/pose', self.update_pose, 10)
         self.pose = Pose()
         self.timer = self.create_timer(0.1, self.go_to_goal)


         self.goal_x = float(sys.argv[1])
         self.goal_y = float(sys.argv[2])
         self.goal_theta = float(sys.argv[3]) * math.pi / 180

     def update_pose(self, data):
         self.pose = data


     def go_to_goal(self):
         msg = Twist()


         lenght_of_path = math.sqrt((self.goal_x - self.pose.x) ** 2 + (self.goal_y - self.pose.y) ** 2)


         angle = math.atan2(self.goal_y - self.pose.y, self.goal_x - self.pose.x)

         linear_vel = 1.0 * lenght_of_path

         angular_vel = 4.0 * (angle - self.pose.theta)


         msg.linear.x = linear_vel
         msg.angular.z = angular_vel

         self.publisher.publish(msg)


         if lenght_of_path < 0.1 and abs(angle) > 0.1:

            msg.angular.z = self.goal_theta
            self.publisher.publish(msg)


            for count in range(9):
            	self.publisher.publish(msg)
            	time.sleep(0.1)

            msg.linear.x = 0.0  # Остановка линейного движения
            msg.angular.z = 0.0  # Остановка вращения

            self.get_logger().info("We have reached the goal.")
            self.timer.cancel()
            self.publisher.publish(msg)
            quit()

def main(args=None):
    rclpy.init(args=args)

    turtle = TurtleIsMoving()

    rclpy.spin(turtle)
    turtle.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
