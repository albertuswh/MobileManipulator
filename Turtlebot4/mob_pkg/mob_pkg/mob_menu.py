#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import tkinter as tk
from example_interfaces.msg import Int64
import paho.mqtt.client as mqtt

class mob_menuClass(Node):
    def __init__(self):
        super().__init__("mob_menuNode")
        self.get_logger().info("MENU TA Node is Starting...")
        self.pub_menu_ta = self.create_publisher(Int64, "idmenu", 10)
        self.id_lokasi=Int64()

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Choose Location:")  # Set the title of the window
        self.root.geometry("300x350")  # Set the size of the window

        # Define a function to be called when the button is clicked
        def on_button_kasur():
            self.get_logger().info("Menunju Kamar Tidur")
            self.id_lokasi.data = 1
            self.pub_menu_ta.publish(self.id_lokasi)

        def on_button_mejaTV():
            self.get_logger().info("Menuju ruang tengah")
            self.id_lokasi.data = 2
            self.pub_menu_ta.publish(self.id_lokasi)

        def on_button_mejaMakan():
            self.get_logger().info("Menuju meja makan")
            self.id_lokasi.data = 3
            self.pub_menu_ta.publish(self.id_lokasi)

        def on_button_home():
            self.get_logger().info("Menuju Dekat Dock")
            self.id_lokasi.data = 4
            self.pub_menu_ta.publish(self.id_lokasi)

        def on_button_dock():
            self.get_logger().info("Dock")
            self.id_lokasi.data = 5
            self.pub_menu_ta.publish(self.id_lokasi)

        def on_button_undock():
            self.get_logger().info("Undock")
            self.id_lokasi.data = 6
            self.pub_menu_ta.publish(self.id_lokasi)

        def on_button_detect():
            self.get_logger().info("Detect Location")
            try:
                # Define the MQTT broker details (local network)
                broker = "192.168.14.41"  # Replace with the IP address of your broker
                port = 1883  # Default MQTT port for non-secure connection
                topic = "spb"
                # Define the message to be published
                message = "hello"
                # Create an MQTT client instance
                client = mqtt.Client()
                # Connect to the MQTT broker
                client.connect(broker, port, 60)
                # Publish the message to the specified topic
                client.publish(topic, message)
                # Disconnect from the broker
                client.disconnect()

                self.id_lokasi.data = 7
                self.pub_menu_ta.publish(self.id_lokasi)
            except:
                self.get_logger().info("Tidak terhubung dengan MQTT")
                
        
        # Create buttons that call the above functions when clicked
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

        button_undock = tk.Button(self.root, text="Detect Lokasi", command=on_button_detect)
        button_undock.pack(pady=10)

        # Schedule the ROS2 spin function to be called periodically
        self.root.after(100, self.ros_spin)

    def ros_spin(self):
        rclpy.spin_once(self, timeout_sec=0.1)
        # Call this method again after 100 milliseconds
        self.root.after(100, self.ros_spin)

def main(args=None):
    rclpy.init(args=args)
    node = mob_menuClass()
    # Start the Tkinter event loop
    node.root.mainloop()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
