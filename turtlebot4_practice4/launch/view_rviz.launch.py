#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launch file mở RViz2 với cấu hình phù hợp cho TurtleBot 4
- view:=mapping : Cấu hình dành cho SLAM / Mapping
- view:=nav2    : Cấu hình dành cho Nav2 Navigation & Goal
"""

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, LaunchConfigurationEquals
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    pkg_practice = get_package_share_directory('turtlebot4_practice4')

    mapping_rviz = PathJoinSubstitution([pkg_practice, 'config', 'turtlebot4_mapping.rviz'])
    nav2_rviz = PathJoinSubstitution([pkg_practice, 'config', 'turtlebot4_nav2.rviz'])

    arguments = [
        DeclareLaunchArgument('view', default_value='mapping',
                              choices=['mapping', 'nav2'],
                              description='Loại hiển thị: mapping hoặc nav2'),
        DeclareLaunchArgument('use_sim_time', default_value='true',
                              choices=['true', 'false'],
                              description='Sử dụng simulation time'),
    ]

    rviz_mapping = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2_mapping',
        output='screen',
        arguments=['-d', mapping_rviz],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        condition=LaunchConfigurationEquals('view', 'mapping')
    )

    rviz_nav2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2_nav2',
        output='screen',
        arguments=['-d', nav2_rviz],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        condition=LaunchConfigurationEquals('view', 'nav2')
    )

    ld = LaunchDescription(arguments)
    ld.add_action(rviz_mapping)
    ld.add_action(rviz_nav2)
    return ld

