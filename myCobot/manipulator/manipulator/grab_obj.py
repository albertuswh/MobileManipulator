import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from pymycobot.mycobot import MyCobot

from pymycobot import PI_PORT, PI_BAUD 

import time


class ControllerCobot(Node):
    def __init__(self):
        super().__init__('kontrol_mycobot')
        
        self.sub_state_obj = self.create_subscription(Int64, "status_tb4", self.state_callback, 10)
        self.pub_state_obj = self.create_publisher(Int64, "status_cobot", 10)

        self.mc = MyCobot("/dev/ttyAMA0", 115200)
        #self.mc.power_on()
        
        self.get_logger().info("Grab Object started")
                    
        # 0 = TB4 belum sampai, 1 = TB4 sampai stasiun minum, 2 = TB4 sampai ke user
        self.state_robot = 0        

    def state_callback(self, msg):
        self.state_robot = msg.data
        #TB4 sudah tiba di lokasi
        if self.state_robot >= 1 and self.state_robot <= 5:
            joints_angle = self.mc.get_angles()
            angle_base = joints_angle[0]
            if angle_base <= -5 and angle_base >= -45: # MAX JOINT 1 AGAR ROBOT TIDAK JATUH
                self.mc.send_angles([angle_base, 76, 0, -84.5, -90, 0], 10) #UPDATE ANGLE SESUAI DENGAN MEJA
                time.sleep(10)
                self.mc.set_gripper_value(15, 10)
                time.sleep(5)
                self.mc.send_angles([0, (-60), 133, (-70), (-90), 0], 10)
                time.sleep(3)
            else:
                self.mc.send_angles([-6, 76, 0, -84.5, -90, 0], 10) #UPDATE ANGLE SESUAI DENGAN MEJA
                time.sleep(10)
                self.mc.set_gripper_value(15, 10)
                time.sleep(5)
                self.mc.send_angles([0, (-60), 133, (-70), (-90), 0], 10)
                time.sleep(3)
                
            id_lokasi = Int64()
            id_lokasi.data = self.state_robot
            self.pub_state_obj.publish(id_lokasi)
                    
        elif self.state_robot == 10:
        #TB4 sudah kembali dan kasih kode 10 lalu reset state dari robot
            time.sleep(5)
            self.mc.set_gripper_value(100, 10)
            self.state_robot = 0


def main(args=None):
    rclpy.init(args=args)
    node = ControllerCobot()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

