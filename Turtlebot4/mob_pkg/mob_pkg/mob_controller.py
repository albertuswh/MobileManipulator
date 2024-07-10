#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator, TaskResult
from example_interfaces.msg import Int64
import time
from example_interfaces.srv import Trigger
from functools import partial

class mobContClass(Node): 
    def __init__(self):
        super().__init__("mobContNode") 
        self.get_logger().info("Controller Mobile Start")
        self.pub_mob = self.create_publisher(Int64, "status_tb4", 10)
        self.pub_cobot = self.create_publisher(Int64, "status_cobot", 10)
        self.sub_mob = self.create_subscription(Int64, "status_cobot", self.tuj_callback, 10)
        self.sub_mob_idmenu = self.create_subscription(Int64, "idmenu", self.tuj_menu, 10)
        self.tujuan_kembali = 0
        self.id_lokasi = Int64()

        self.get_logger().info("ambil TB4NAV")
        self.navigator = TurtleBot4Navigator()

        # Start on dock (BIKIN CODE LAMA DI-START)
        # self.navigator.info("Checking Dock Status")
        # if not self.navigator.getDockedStatus():
        #     self.navigator.info('Docking before intialising pose')
        #     self.navigator.dock()

        self.navigator.info("Setting Initial Pose")
        # Set initial pose
        initial_pose = self.navigator.getPoseStamped([-0.043, -0.0144], TurtleBot4Directions.NORTH)
        self.navigator.setInitialPose(initial_pose)

        # Wait for Nav2
        self.navigator.info("Wait Nav2 to be Active")
        self.navigator.waitUntilNav2Active()

        # self.navigator.undock() 
    
    def callback_botol_service(self, future, id):
        try:
            response = future.result()
            self.get_logger().info(str(response.success))
            self.id_lokasi.data = id
            self.pub_cobot.publish(self.id_lokasi)
        except Exception as e: 
            self.get_logger().error("Service call failed %r" %(e,))

    def tuj_menu(self,msg):
        # self.get_logger().info("masuk")
        self.idmenu = msg.data
        if self.idmenu >= 1 and self.idmenu <= 3 :
            self.navigator.info("idmenu")
            goal_pose = self.navigator.getPoseStamped([-2.75, -1.98], TurtleBot4Directions.SOUTH)
            self.navigator.startToPose(goal_pose)
            time.sleep(3)

            result = self.navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                clientBotol = self.create_client(Trigger, "cari_botol")

                while not clientBotol.wait_for_service(2.0):
                    self.get_logger().warn("Waiting for CARI BOTOL service")
                request = Trigger.Request()
                
                futureBotol = clientBotol.call_async(request)
                futureBotol.add_done_callback(partial(self.callback_botol_service, id = self.idmenu))
            else:
                self.navigator.info('Goal has an invalid return status!')
                clientBotol = self.create_client(Trigger, "cari_botol")

                while not clientBotol.wait_for_service(2.0):
                    self.get_logger().warn("Waiting for CARI BOTOL service")
                request = Trigger.Request()
                
                futureBotol = clientBotol.call_async(request)
                futureBotol.add_done_callback(partial(self.callback_botol_service, id = self.idmenu))

        elif self.idmenu == 4:
            goal_pose = self.navigator.getPoseStamped([-0.36, -0.15], TurtleBot4Directions.NORTH)
            self.navigator.startToPose(goal_pose)
        elif self.idmenu == 5:
            self.navigator.dock()
        elif self.idmenu == 6:
            self.navigator.undock() 
        elif self.idmenu == 7:
            client = self.create_client(Trigger, "say_hello")

            while not client.wait_for_service(2.0):
                self.get_logger().warn("Waiting for the hello service to become available")
            
            request = Trigger.Request()
            
            future = client.call_async(request)
            future.add_done_callback(self.callback_hello_service)


    def callback_hello_service(self, future):
        try:
            response = future.result()
            parts = response.message.split()
            # Extract the values from the parts
            x_str = parts[1]  # The part after 'x:'
            y_str = parts[3]  # The part after 'y:'
            # Convert the string values to floats
            x_value = float(x_str)
            y_value = float(y_str)
            # PERHITUNGAN KONVERSI KE SATUAN PIXEL MAP
            # offset sb y map rviz = 80cm
            # offset sb x map rviz = 10cm
            x_koord = - (y_value - 0.1)
            y_koord = -(x_value - 0.8)
            self.get_logger().info(f"{str(x_koord)} and {str(y_koord)}")
            if x_koord <= 0.0 and x_koord >= -3.5 and y_koord <= 0.0 and y_koord >= -4.5:
                goal_pose = self.navigator.getPoseStamped([x_koord, y_koord], TurtleBot4Directions.NORTH)
                self.get_logger().info("Go To TAG")
                self.navigator.startToPose(goal_pose)   
            else:
                self.get_logger().info(f"Koordinat berada di luar area kerja robot: {str(x_koord)} and {str(y_koord)}")
        except Exception as e: 
            self.get_logger().error(f"Service call failed: {e}")


    def tuj_callback(self, msg):
        self.tujuan_kembali = msg.data
        if self.tujuan_kembali == 1:
            self.get_logger().info("Ke kamar tidur")
            navigator = TurtleBot4Navigator()
            goal_pose = navigator.getPoseStamped([0.54, -3.622], TurtleBot4Directions.EAST)
            navigator.startToPose(goal_pose)
            time.sleep(0)
            self.id_lokasi.data = 10
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                navigator.info('publish ke /status_tb4')
                self.pub_mob.publish(self.id_lokasi)
            elif result == TaskResult.CANCELED:
                navigator.info('Goal was canceled!')
            elif result == TaskResult.FAILED:
                navigator.info('Goal failed!')
            else:
                navigator.info('Goal has an invalid return status!')
                self.pub_mob.publish(self.id_lokasi)
            self.tujuan_kembali = 0

        elif self.tujuan_kembali == 2:
            self.get_logger().info("Ke mejaTV")
            navigator = TurtleBot4Navigator()
            goal_pose = navigator.getPoseStamped([-2.1, -4.1], TurtleBot4Directions.EAST)
            navigator.startToPose(goal_pose)
            time.sleep(0)
            self.id_lokasi = Int64()
            self.id_lokasi.data = 10
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                navigator.info('publish ke /status_tb4')
                self.pub_mob.publish(self.id_lokasi)
            else:
                navigator.info('Goal has an invalid return status!')
                self.pub_mob.publish(self.id_lokasi)
            self.tujuan_kembali = 0

        elif self.tujuan_kembali == 3:
            self.get_logger().info("Ke meja makan")
            navigator = TurtleBot4Navigator()
            goal_pose = navigator.getPoseStamped([-1.38, -1.75], TurtleBot4Directions.NORTH)
            navigator.startToPose(goal_pose)
            time.sleep(0)
            self.id_lokasi = Int64()
            self.id_lokasi.data = 10
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                navigator.info('publish ke /status_tb4')
                self.pub_mob.publish(self.id_lokasi)
            else:
                navigator.info('Goal has an invalid return status!')
                self.pub_mob.publish(self.id_lokasi)
            self.tujuan_kembali = 0


def main(args=None):
    rclpy.init(args=args)
    node = mobContClass() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
