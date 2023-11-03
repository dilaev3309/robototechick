import rclpy
import sys
from rclpy.node import Node
from c_pack.srv import FullNameSumService

class ClientName(Node):

    def __init__(self):
        super().__init__('client_name')
        self.client = self.create_client(FullNameSumService, 'summ_full_name')

        # Ожидание доступности сервиса. 
        # Если сервис не становится доступным в течение 1 секунды, 
        # выводится соответ. сообщение
        while not self.client.wait_for_service(timeout_sec=1.0):
        	self.get_logger().info('Service is unavailable')
         
        # Объект запроса для сервиса, 
        # который будет использоваться для отправки запроса сервису
        self.request = FullNameSumService.Request()

    # Принимаем аргументы last_name, name и first_name, 
    # устанавливаем их в объекте запроса, а затем вызываем сервис асинхронно
    def give_request(self, last_name, name, first_name):
        self.request.last_name = last_name
        self.request.name = name
        self.request.first_name = first_name
        
        res = self.client.call_async(self.request)
        # Ожидаем завершения асинхронного вызова сервиса
        rclpy.spin_until_future_complete(self, res)
        
        return res.result()

def main():
    rclpy.init()
    client_name = ClientName()

    # Отправляем запрос к сервису, передав аргументы командной строки
    res = client_name.give_request(sys.argv[1], sys.argv[2], sys.argv[3])

    # Если получен результат, выводим полное имя
    if res: client_name.get_logger().info('Full name: %s' % res.full_name)
        
    client_name.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
