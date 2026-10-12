#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launch file mở RViz2 với cấu hình phù hợp cho TurtleBot 4
- view:=sim     : Cấu hình cho Phần 1 (Simulation cơ bản, Fixed Frame: odom)
- view:=mapping : Cấu hình cho Phần 2 (SLAM Toolbox, Fixed Frame: map)
- view:=nav2    : Cấu hình cho Phần 3 & 4 (Localization & Nav2, Fixed Frame: map)
"""

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import LaunchConfigurationEquals
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    pkg_practice = get_package_share_directory('turtlebot4_practice4')

    sim_rviz = PathJoinSubstitution([pkg_practice, 'config', 'turtlebot4_sim.rviz'])
    mapping_rviz = PathJoinSubstitution([pkg_practice, 'config', 'turtlebot4_mapping.rviz'])
    nav2_rviz = PathJoinSubstitution([pkg_practice, 'config', 'turtlebot4_nav2.rviz'])

    arguments = [
        DeclareLaunchArgument('view', default_value='sim',
                              choices=['sim', 'mapping', 'nav2'],
                              description='Loại hiển thị: sim (odom), mapping (map), hoặc nav2 (map)'),
        DeclareLaunchArgument('use_sim_time', default_value='true',
                              choices=['true', 'false'],
                              description='Sử dụng simulation time'),
    ]

    rviz_sim = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2_sim',
        output='screen',
        arguments=['-d', sim_rviz],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        condition=LaunchConfigurationEquals('view', 'sim')
    )

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
    ld.add_action(rviz_sim)
    ld.add_action(rviz_mapping)
    ld.add_action(rviz_nav2)
    return ld
