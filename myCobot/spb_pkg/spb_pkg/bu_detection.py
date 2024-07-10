import os
import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from example_interfaces.msg import Int64
from geometry_msgs.msg import Twist

class BtlDetection(Node):
    def __init__(self):
        super().__init__("btldetectNode")
        
        self.publish_ = self.create_publisher(Int64, "koord_x_obj", 10)
        self.cmd_vel_pub = self.create_publisher(Twist, "cmd_vel", 10) # Ganti topic sesuai dengan namespace robot
        
        self.thres = 0.40
        self.nms_threshold = 0.3
        self.cap = cv2.VideoCapture(0) # GANTI SESUAI ID CAMERA YG DIPAKAI
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.cap.set(10, 50)

        self.classNames = []
        classFile = os.path.join(os.path.dirname(__file__), 'coco.names')
        with open(classFile, 'rt') as f:
            self.classNames = f.read().rstrip('\n').split('\n')

        configPath = os.path.join(os.path.dirname(__file__), 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
        weightsPath = os.path.join(os.path.dirname(__file__), 'frozen_inference_graph.pb')
        self.net = cv2.dnn_DetectionModel(weightsPath, configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.sampai_botol = False

    def detect_objects(self):
        while True:
            success, img = self.cap.read()
            if not success:
                break

            frame_height, frame_width, _ = img.shape
            frame_center_x = frame_width // 2

            classIds, confs, bbox = self.net.detect(img, confThreshold=self.thres)
            bbox = list(bbox)
            confs = list(np.array(confs).reshape(1, -1)[0])
            confs = list(map(float, confs))

            indices = cv2.dnn.NMSBoxes(bbox, confs, self.thres, self.nms_threshold)

            detected = False

            for i in indices:
                if detected:
                    break

                if self.classNames[classIds[i] - 1] in ["bottle"]:
                    box = bbox[i]
                    x, y, w, h = box[0], box[1], box[2], box[3]
                    
                    self.get_logger().info("Nilai W : ")
                    self.get_logger().info(str(w))
                    
                    if w >= 1:
                        cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
                        cv2.putText(img, self.classNames[classIds[i] - 1].upper(), (x + 10, y + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                        number_x = Int64()
                        number_x.data = int(x + (w / 2))
                        self.publish_.publish(number_x)

                        bbox_center_x = x + w // 2
                        distance_threshold = 30
                        if abs(bbox_center_x - frame_center_x) < distance_threshold:
                            if w < 35:
                                self.get_logger().info('Bottle centered, moving forward')
                                twist_msg = Twist()
                                twist_msg.linear.x = 0.01  # Move forward
                                self.cmd_vel_pub.publish(twist_msg)
                                
                            elif w >= 35:
                                self.get_logger().info('Bottle centered and large enough, stopping')
                                twist_msg = Twist()
                                twist_msg.linear.x = 0.0  # Stop
                                self.cmd_vel_pub.publish(twist_msg)
                                self.sampai_botol = True
                                
                            else:
                                self.get_logger().info('Bottle centered and large enough, stopping')
                                twist_msg = Twist()
                                twist_msg.linear.x = 0.0  # Stop
                                self.cmd_vel_pub.publish(twist_msg)

                        else:
                            self.get_logger().info('Bottle detected but not centered')
                            twist_msg = Twist()
                            if bbox_center_x < frame_center_x:
                                twist_msg.angular.z = 0.005  # Rotate left
                            else:
                                twist_msg.angular.z = -0.005  # Rotate right
                            self.cmd_vel_pub.publish(twist_msg)

                        detected = True

            #cv2.imshow("Output", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif self.sampai_botol :
                break

        self.cap.release()
        cv2.destroyAllWindows()

def main(args=None):
    rclpy.init(args=args)
    node = BtlDetection()
    try:
        node.detect_objects()
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()

if __name__ == "__main__":
    main()
