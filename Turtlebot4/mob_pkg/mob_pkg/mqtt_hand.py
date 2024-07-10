import paho.mqtt.client as mqtt
import rclpy
from rclpy.node import Node
from example_interfaces.srv import Trigger

class helloMqttServ(Node):
    def __init__(self):
        super().__init__('mqttServ')
        self.get_logger().info("hello serv started")
        self.srv = self.create_service(Trigger, 'say_hello', self.say_hello_callback)
        # Define the MQTT broker details (local network)
        self.broker = "192.168.14.41"  # Replace with the IP address of your broker
        self.port = 1883  # Default MQTT port for non-secure connection
        self.topic = "koordinattag"

        # Flag to indicate when to stop the loop
        self.message_received = False

        # Variable to store the received message
        self.received_message = ""

        # Create an MQTT client instance
        self.client = mqtt.Client() 

    # Define the callback function for when a message is received
    def on_message(self, client, userdata, message):
        self.get_logger().info(f"Message received: {message.payload.decode()} on topic {message.topic}")
        self.received_message = message.payload.decode()
        self.message_received = True
        client.disconnect()  # Disconnect the client

    def say_hello_callback(self, request, response):
        self.get_logger().info('Received request for hello')
        self.message_received = False  # Reset the flag for each service call
        self.received_message = ""  # Reset the message storage

        # Assign the on_message callback function
        self.client.on_message = self.on_message

        # Connect to the MQTT broker
        self.client.connect(self.broker, self.port, 60)

        # Subscribe to the specified topic
        self.client.subscribe(self.topic)

        # Start the MQTT client loop and stop after one message is received
        while not self.message_received:
            self.client.loop()
        # self.get_logger().info("Client loop stopped after receiving one message.")

        response.success = True
        response.message = self.received_message
        self.get_logger().info(f"Sending response: {response.message}")
        return response

def main(args=None):
    rclpy.init(args=args)
    node = helloMqttServ()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
