#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import tkinter as tk 
import time
from example_interfaces.msg import Int64
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator , TaskResult


class location_class(Node): 
    def __init__(self):
        super().__init__("locMenuNode") 
        self.get_logger().info("UI Menu Lab IoT Node Starting...")
        self.pub_menu_loc = self.create_publisher(Int64, "status_tb4", 10)
        self.sub_menu_loc = self.create_subscription(Int64, "status_cobot", self.tuj_callback, 10)
        self.tujuan_kembali = 0

        navigator = TurtleBot4Navigator()
        navigator.info("Initialising Pose and wait Nav2 to be active ")

        # Start on dock
        if not navigator.getDockedStatus():
            navigator.info('Docking before intialising pose')
            navigator.dock()

        # Set initial pose
        initial_pose = navigator.getPoseStamped([-0.02, -0.136], TurtleBot4Directions.NORTH)
        navigator.setInitialPose(initial_pose)

        # Wait for Nav2
        navigator.waitUntilNav2Active()

        # Undock
        navigator.undock()

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Choose Location:")  # Set the title of the window
        self.root.geometry("300x350")  # Set the size of the window

        # Define a function to be called when the button is clicked
        def on_button_kasur():
            self.get_logger().info("Menunju Kamar Tidur")
            goal_pose = navigator.getPoseStamped([-2.93, -1.73], TurtleBot4Directions.SOUTH)
            navigator.startToPose(goal_pose)
            time.sleep(10)
            id_lokasi = Int64()
            id_lokasi.data = 1
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                navigator.info('publish ke /status_tb4')
                self.pub_menu_loc.publish(id_lokasi)
            elif result == TaskResult.CANCELED:
                navigator.info('Goal was canceled!')
            elif result == TaskResult.FAILED:
                navigator.info('Goal failed!')
            else:
                navigator.info('Goal has an invalid return status!')
                self.pub_menu_loc.publish(id_lokasi)
        
            

        def on_button_mejaTV():
            self.get_logger().info("Menuju ruang tengah")
            goal_pose = navigator.getPoseStamped([-2.93, -1.73], TurtleBot4Directions.SOUTH)
            navigator.startToPose(goal_pose)
            time.sleep(10)
            id_lokasi = Int64()
            id_lokasi.data = 2
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                navigator.info('publish ke /status_tb4')
                self.pub_menu_loc.publish(id_lokasi)
            elif result == TaskResult.CANCELED:
                navigator.info('Goal was canceled!')
            elif result == TaskResult.FAILED:
                navigator.info('Goal failed!')
            else:
                navigator.info('Goal has an invalid return status!')
                self.pub_menu_loc.publish(id_lokasi)
        


        def on_button_mejaMakan():
            self.get_logger().info("Menuju meja makan")
            goal_pose = navigator.getPoseStamped([-2.93, -1.73], TurtleBot4Directions.SOUTH)
            navigator.startToPose(goal_pose)
            time.sleep(10)
            id_lokasi = Int64()
            id_lokasi.data = 3
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                navigator.info('publish ke /status_tb4')
                self.pub_menu_loc.publish(id_lokasi)
            elif result == TaskResult.CANCELED:
                navigator.info('Goal was canceled!')
            elif result == TaskResult.FAILED:
                navigator.info('Goal failed!')
            else:
                navigator.info('Goal has an invalid return status!')
                self.pub_menu_loc.publish(id_lokasi)
        
        def on_button_home():
            self.get_logger().info("Menuju Dekat Dock")
            goal_pose = navigator.getPoseStamped([-0.36, -0.15], TurtleBot4Directions.NORTH)
            navigator.startToPose(goal_pose)

        def on_button_dock():
            navigator.dock()

        def on_button_undock():    
            navigator.undock()

        # Create a button that calls the above function when clicked
        button_kasur = tk.Button(self.root, text="Kasur", command=on_button_kasur)
        button_kasur.pack(pady=10)

        button_mejaKomp = tk.Button(self.root, text="Sofa", command=on_button_mejaTV)
        button_mejaKomp.pack(pady=10)

        button_mejaBuku = tk.Button(self.root, text="Meja Makan", command=on_button_mejaMakan)
        button_mejaBuku.pack(pady=10)

        button_home = tk.Button(self.root, text="Home", command=on_button_home)
        button_home.pack(pady=10)

        button_dock = tk.Button(self.root, text="Dock", command=on_button_dock)
        button_dock.pack(pady=10)

        button_undock = tk.Button(self.root, text="Undock", command=on_button_undock)
        button_undock.pack(pady=10)

        # Schedule the ROS2 spin function to be called periodically
        self.root.after(1, self.ros_spin)
    
    def tuj_callback(self, msg):
        self.tujuan_kembali = msg.data
        if self.tujuan_kembali == 1:
            self.get_logger().info("Ke kamar tidur")
            navigator = TurtleBot4Navigator()
            goal_pose = navigator.getPoseStamped([0.54, -3.622], TurtleBot4Directions.EAST)
            navigator.startToPose(goal_pose)
            time.sleep(5)
            # self.check_posisi_user()
            id_lokasi = Int64()
            id_lokasi.data = 10
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                navigator.info('publish ke /status_tb4')
                self.pub_menu_loc.publish(id_lokasi)
            elif result == TaskResult.CANCELED:
                navigator.info('Goal was canceled!')
            elif result == TaskResult.FAILED:
                navigator.info('Goal failed!')
            else:
                navigator.info('Goal has an invalid return status!')
                self.pub_menu_loc.publish(id_lokasi)
            self.tujuan_kembali = 0

        elif self.tujuan_kembali == 2:
            self.get_logger().info("Ke mejaTV")
            navigator = TurtleBot4Navigator()
            goal_pose = navigator.getPoseStamped([-2.6, -3.7], TurtleBot4Directions.EAST)
            navigator.startToPose(goal_pose)
            time.sleep(5)
            id_lokasi = Int64()
            id_lokasi.data = 10
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                navigator.info('publish ke /status_tb4')
                self.pub_menu_loc.publish(id_lokasi)
            elif result == TaskResult.CANCELED:
                navigator.info('Goal was canceled!')
            elif result == TaskResult.FAILED:
                navigator.info('Goal failed!')
            else:
                navigator.info('Goal has an invalid return status!')
                self.pub_menu_loc.publish(id_lokasi)
            self.tujuan_kembali = 0

        elif self.tujuan_kembali == 3:
            self.get_logger().info("Ke meja makan")
            navigator = TurtleBot4Navigator()
            goal_pose = navigator.getPoseStamped([-1.38, -1.75], TurtleBot4Directions.NORTH)
            navigator.startToPose(goal_pose)
            time.sleep(5)
            id_lokasi = Int64()
            id_lokasi.data = 10
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                navigator.info('publish ke /status_tb4')
                self.pub_menu_loc.publish(id_lokasi)
            elif result == TaskResult.CANCELED:
                navigator.info('Goal was canceled!')
            elif result == TaskResult.FAILED:
                navigator.info('Goal failed!')
            else:
                navigator.info('Goal has an invalid return status!')
                self.pub_menu_loc.publish(id_lokasi)
            self.tujuan_kembali = 0

    def ros_spin(self):
        rclpy.spin_once(self, timeout_sec=0.1)
        # Call this method again after 100 milliseconds
        self.root.after(1, self.ros_spin)


def main(args=None):
    rclpy.init(args=args)
    node = location_class() 
    # Start the Tkinter event loop
    node.root.mainloop()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
