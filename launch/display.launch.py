#!/usr/bin/env python3
import os, xacro

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Path to your URDF file
    xacro_file = os.path.join(
        get_package_share_directory('pedestals_description'),
        'urdf',
        'kuka_pedestal.xacro'
    )
    
    rviz_config_file = os.path.join(
        get_package_share_directory('pedestals_description'),
        'rviz',
        'config.rviz'
    )
    
    robot_description_content = xacro.process_file(xacro_file).toxml()
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        # Launch with the provided RViz config if available
        arguments=['-d', rviz_config_file] if os.path.exists(rviz_config_file) else []
    )
    
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}]
    )
    
    return LaunchDescription([
        rviz_node,
        robot_state_publisher_node
    ])