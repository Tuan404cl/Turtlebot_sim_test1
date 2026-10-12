#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launch file khởi chạy SLAM Toolbox để lập bản đồ cho TurtleBot 4
Phần 2: Xây dựng bản đồ bằng SLAM Toolbox
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

ARGUMENTS = [
    DeclareLaunchArgument('launch_sim', default_value='true',
                          choices=['true', 'false'],
                          description='Tự động khởi chạy luôn Gazebo simulation'),
    DeclareLaunchArgument('world', default_value='warehouse',
                          description='Gazebo world'),
    DeclareLaunchArgument('sync', default_value='true',
                          choices=['true', 'false'],
                          description='Sử dụng Synchronous SLAM Toolbox'),
    DeclareLaunchArgument('use_sim_time', default_value='true',
                          choices=['true', 'false'],
                          description='Sử dụng simulation time'),
    DeclareLaunchArgument('rviz', default_value='true',
                          choices=['true', 'false'],
                          description='Mở RViz2 hiển thị Map và LaserScan'),
]

def generate_launch_description():
    pkg_practice = get_package_share_directory('turtlebot4_practice4')
    pkg_tb4_nav = get_package_share_directory('turtlebot4_navigation')

    sim_launch = PathJoinSubstitution([pkg_practice, 'launch', 'sim_robot.launch.py'])
    slam_params = PathJoinSubstitution([pkg_practice, 'config', 'slam_toolbox_params.yaml'])
    rviz_config = PathJoinSubstitution([pkg_practice, 'config', 'turtlebot4_mapping.rviz'])

    # 1. Khởi chạy Simulation nếu launch_sim == true
    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([sim_launch]),
        launch_arguments=[
            ('world', LaunchConfiguration('world')),
            ('rviz', 'false')
        ],
        condition=IfCondition(LaunchConfiguration('launch_sim'))
    )

    # 2. SLAM Toolbox Node
    slam_node = Node(
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            slam_params,
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static'),
            ('/scan', 'scan'),
            ('/map', 'map'),
            ('/map_metadata', 'map_metadata'),
        ]
    )

    # 3. RViz2 Visualization
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2_mapping',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(simulation)
    ld.add_action(slam_node)
    ld.add_action(rviz_node)
    return ld
