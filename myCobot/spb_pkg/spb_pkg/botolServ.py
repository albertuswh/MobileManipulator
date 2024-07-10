import rclpy
from rclpy.node import Node
from example_interfaces.srv import Trigger
from spb_pkg.bottle_detection import BtlDetection
from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD 

class BotolServ(Node):
    def __init__(self):
        super().__init__('botol_service')
        self.get_logger().info("cari_botol serv started...")

        # STARTING POSE MYCOBOT
        self.mc = MyCobot("/dev/ttyAMA0", 115200)
        self.mc.power_on()       
        self.mc.send_angles([-5, (-60), 133, (-70), (-90), 0], 10)
        if(self.mc.is_moving() == 0 and self.mc.is_gripper_moving() == 0):
            self.mc.set_gripper_value(100,20)
            print(self.mc.get_gripper_value())

        self.srv = self.create_service(Trigger, 'cari_botol', self.cari_botol_callback)

    def cari_botol_callback(self, request, response):
        self.get_logger().info('Received request for bottle detection')
        detector = BtlDetection()  # Instantiate a new object detection node
        try:
            detector.detect_objects()  # Call the object detection method
            response.success = True
            response.message = "Bottle detection completed"
        except Exception as e:
            self.get_logger().error(f"An error occurred during bottle detection: {str(e)}")
            response.success = False
            response.message = f"An error occurred: {str(e)}"
        finally:
            detector.destroy_node()  # Ensure resources are cleaned up properly

        return response

def main(args=None):
    rclpy.init(args=args)
    node = BotolServ()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
