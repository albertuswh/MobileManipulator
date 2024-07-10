import os
import rclpy
from rclpy.node import Node

import cv2
import numpy as np
from pymycobot.mycobot import MyCobot

from pymycobot import PI_PORT, PI_BAUD 

from example_interfaces.msg import String
from example_interfaces.msg import Int64

class btlDetection(Node):
    def __init__(self):
        super().__init__("btldetectNode")
        
        self.publish_ =  self.create_publisher(Int64, "koord_x_obj", 10)
        #self.pub_w = self.create_publisher(Int64, "width_obj", 10)
        #self.pub_w_once = True
        
        
        # Set the threshold and NMS threshold
        thres = 0.40
        nms_threshold = 0.3

        # Capture video from the webcam
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 630)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)
        cap.set(10, 50)

        # Load class names from the coco.names file
        classNames = []
#        classFile = "coco.names"
        classFile = os.path.join(os.path.dirname(__file__), 'coco.names')

        with open(classFile, 'rt') as f:
            classNames = f.read().rstrip('\n').split('\n')

        # Load the model configuration and weights
        configPath = os.path.join(os.path.dirname(__file__), 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
        weightsPath = os.path.join(os.path.dirname(__file__), 'frozen_inference_graph.pb')

        net = cv2.dnn_DetectionModel(weightsPath, configPath)
        net.setInputSize(320, 320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)


        while True:
            success, img = cap.read()
            if not success:
                break

            # Get the dimensions of the frame
            frame_height, frame_width, _ = img.shape

            # Calculate the center of the frame
            frame_center_x = frame_width // 2
            frame_center_y = frame_height // 2

            classIds, confs, bbox = net.detect(img, confThreshold=thres)
            bbox = list(bbox)
            confs = list(np.array(confs).reshape(1, -1)[0])
            confs = list(map(float, confs))

            indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_threshold)

            detected = False  # Flag to indicate if an object has been detected

            for i in indices:
                if detected:
                    break  # Exit the loop if an object has already been detected

                if classNames[classIds[i] - 1] == "bottle" or classNames[classIds[i] - 1] == "cup":
                    box = bbox[i]
                    x, y, w, h = box[0], box[1], box[2], box[3]
                    
#filter untuk botol yang dekat, jadi jika width terlalu kecil, tidak akan terbaca
                    if w >= 60:
                        cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
                        cv2.putText(img, classNames[classIds[i] - 1].upper(), (x + 10, y + 30),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                        number_x = Int64()
                        number_x.data = int(x + (w/2))

                        self.publish_.publish(number_x)

                        # Calculate the center of the bounding box
                        bbox_center_x = x + w // 2
                        bbox_center_y = y + h // 2

                        # Check if the bounding box is near the center of the frame
                        distance_threshold = 30  # Distance threshold in pixels
                        #if abs(bbox_center_x - frame_center_x) < distance_threshold and abs(bbox_center_y - frame_center_y) < distance_threshold:
                        if abs(bbox_center_x - frame_center_x) < distance_threshold:
                            #self.get_logger().info('Botol di tengah')
                            print("nilai W = ", w)
                        else:
                            print("Botol belum di tengah")

                        detected = True  # Set the flag to true indicating an object has been detected
                        
                        #if w >= 200:
                        #    mc.set_gripper_value(20, 20)
                        #    print("Ambil Botol")
                        #else:
                        #    mc.set_gripper_value(100,20)

            cv2.imshow("Output", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        
        
def main(args=None):
    rclpy.init(args=args)
    node = btlDetection()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()    
