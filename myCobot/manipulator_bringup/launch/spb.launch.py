from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    
    
    detect_bottle = Node(
        package="spb_pkg",
        executable="btlServ",
    )
    
    grab_object = Node(
        package="manipulator",
        executable="grab_bottle",
    )
    
    ld.add_action(detect_bottle)
    ld.add_action(grab_object)
    
    return ld

