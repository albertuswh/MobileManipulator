from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    
    
    detect_bottle = Node(
        package="manipulator",
        executable="bottle_detection",
    )
    
    controller_cobot_x = Node(
        package="manipulator",
        executable="controller_cobot",
    )
    
    grab_object = Node(
        package="manipulator",
        executable="grab_bottle",
    )
    
    ld.add_action(detect_bottle)
    ld.add_action(controller_cobot_x)
    ld.add_action(grab_object)
    
    return ld

