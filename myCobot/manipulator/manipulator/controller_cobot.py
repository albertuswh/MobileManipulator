import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from pymycobot.mycobot import MyCobot

from pymycobot import PI_PORT, PI_BAUD 


class ControllerCobot(Node):
    def __init__(self):
        super().__init__('kontrol_mycobot')
        self.subscription = self.create_subscription(Int64, 'koord_x_obj',self.coord_callback,10)

        self.mc = MyCobot("/dev/ttyAMA0", 115200)
        self.mc.power_on()
        
        self.get_logger().info("starting robot controller")
        
        #Steadt STATE (TAMBAHKAN COORD SESUAI DENGAN TINGGI MEJA)        
        self.mc.send_angles([0, (-60), 133, (-70), (-90), 0], 10)
        
        if(self.mc.is_moving() == 0 and self.mc.is_gripper_moving() == 0):
            self.mc.set_gripper_value(100,20)
            print(self.mc.get_gripper_value())

    def coord_callback(self, msg):
        x_coord = msg.data
#width Cam = 630. x tengah = 315 dengan +- 30 pixel toleransi 
        if x_coord == -1:
            # Move joint 1 left and right untuk cari botol
            self.get_logger().info('Moving joint 1 left and right')
        elif x_coord < 285:
            # Increase angle on joint 1
            current_angles = self.mc.get_angles()
            #print(current_angles)
            current_angles[0] += 2  # Increment by 5 (adjust as needed)
            print(current_angles[0])
            if(self.mc.is_moving() == 0 and self.mc.is_gripper_moving() == 0):
                self.mc.send_angle(1, current_angles[0] , 10)
            #self.get_logger().info('Increasing angle on joint 1')
            
        elif x_coord > 345:
            # Decrease angle on joint 1
            current_angles = self.mc.get_angles()
            current_angles[0] -= 2  # Decrement by 5 (adjust as needed)
            if(self.mc.is_moving() == 0 and self.mc.is_gripper_moving() == 0):
                self.mc.send_angle(1, current_angles[0] , 10)
            #self.get_logger().info('Decreasing angle on joint 1')
        elif x_coord > 285 and x_coord < 345:
            #kalo botol ditengah, maka majukan koord X untuk mengambil botol
            pass
        else:
            # Stop moving joint 1
            pass


def main(args=None):
    rclpy.init(args=args)
    node = ControllerCobot()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
