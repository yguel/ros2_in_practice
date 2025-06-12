from rsia_tests_interfaces.srv import SrvAtest

import rclpy
from rclpy.node import Node


class AService(Node):

    def __init__(self):
        super().__init__('srv_a')
        self.srv = self.create_service(SrvAtest, 'srv_a_test', self.srv_callback)

    def srv_callback(self, request, response):
        response.response_a = request.request_a + "_heard_and_answered"
        self.get_logger().info(f'Incoming request to service A: {request.request_a}')

        return response


def main():
    rclpy.init()

    a_service = AService()

    try:
        rclpy.spin(a_service)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, shutting down...")
    except Exception as e:
        print(f"Exception occurred: {e}")

    try:
        a_service.destroy_node()
    except Exception as e:
        print(f"Exception during shutdown: {e}")

if __name__ == '__main__':
    main()