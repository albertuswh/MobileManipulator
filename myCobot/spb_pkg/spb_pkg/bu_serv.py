import rclpy
from rclpy.node import Node
from example_interfaces.srv import Trigger
from od_pkg.bottle_detection import BtlDetection
import time

class BotolServ(Node):
    def __init__(self):
        super().__init__('botol_service')
        self.get_logger().info("cari_botol serv started")

        self.srv = self.create_service(Trigger, 'cari_botol', self.cari_botol_callback)
        self.detector = None

    def cari_botol_callback(self, request, response):
        self.get_logger().info('Received request for bottle detection')

        if self.detector is not None:
            self.detector.destroy_node()

        # Wait briefly before reinitializing the detector to ensure resources are released
        time.sleep(1)

        self.detector = BtlDetection()  # Instantiate the object detection node
        try:
            self.detector.detect_objects()  # Call the object detection method
            response.success = True
            response.message = "Bottle detection completed"
        except Exception as e:
            self.get_logger().error(f"An error occurred during bottle detection: {str(e)}")
            response.success = False
            response.message = f"An error occurred: {str(e)}"
        finally:
            self.detector.destroy_node()
            self.detector = None

        return response

def main(args=None):
    rclpy.init(args=args)
    node = BotolServ()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
