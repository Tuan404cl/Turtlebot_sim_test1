#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launch file khởi chạy mô phỏng TurtleBot 4 trong Gazebo (Ignition)
Phần 1: TurtleBot 4 Simulation
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

ARGUMENTS = [
    DeclareLaunchArgument('world', default_value='warehouse',
                          description='Gazebo world: warehouse, depot, or maze'),
    DeclareLaunchArgument('model', default_value='standard',
                          choices=['standard', 'lite'],
                          description='Mô hình TurtleBot 4 (standard hoặc lite)'),
    DeclareLaunchArgument('rviz', default_value='false',
                          choices=['true', 'false'],
                          description='Mở RViz2 trực tiếp cùng simulator'),
    DeclareLaunchArgument('x', default_value='0.0', description='Toạ độ X khởi đầu'),
    DeclareLaunchArgument('y', default_value='0.0', description='Toạ độ Y khởi đầu'),
    DeclareLaunchArgument('z', default_value='0.0', description='Toạ độ Z khởi đầu'),
    DeclareLaunchArgument('yaw', default_value='0.0', description='Góc Yaw khởi đầu (rad)'),
]

def generate_launch_description():
    pkg_tb4_ign = get_package_share_directory('turtlebot4_ignition_bringup')
    pkg_practice = get_package_share_directory('turtlebot4_practice4')

    tb4_ign_launch = PathJoinSubstitution([
        pkg_tb4_ign, 'launch', 'turtlebot4_ignition.launch.py'
    ])

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([tb4_ign_launch]),
        launch_arguments=[
            ('world', LaunchConfiguration('world')),
            ('model', LaunchConfiguration('model')),
            ('x', LaunchConfiguration('x')),
            ('y', LaunchConfiguration('y')),
            ('z', LaunchConfiguration('z')),
            ('yaw', LaunchConfiguration('yaw')),
            ('rviz', LaunchConfiguration('rviz'))
        ]
    )

    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(simulation)
    return ld
