#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launch file khởi chạy Localization (AMCL + Map Server) cho TurtleBot 4
Phần 3: Localization với bản đồ đã tạo
"""

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    pkg_practice = get_package_share_directory('turtlebot4_practice4')
    pkg_nav2_bringup = get_package_share_directory('nav2_bringup')

    sim_launch = PathJoinSubstitution([pkg_practice, 'launch', 'sim_robot.launch.py'])
    default_map = PathJoinSubstitution([pkg_practice, 'maps', 'map.yaml'])
    loc_params = PathJoinSubstitution([pkg_practice, 'config', 'localization_params.yaml'])
    rviz_config = PathJoinSubstitution([pkg_practice, 'config', 'turtlebot4_mapping.rviz'])
    nav2_loc_launch = PathJoinSubstitution([pkg_nav2_bringup, 'launch', 'localization_launch.py'])

    arguments = [
        DeclareLaunchArgument('launch_sim', default_value='true',
                              choices=['true', 'false'],
                              description='Khởi chạy kèm Gazebo simulation'),
        DeclareLaunchArgument('world', default_value='warehouse',
                              description='Gazebo world'),
        DeclareLaunchArgument('use_sim_time', default_value='true',
                              choices=['true', 'false'],
                              description='Sử dụng simulation time'),
        DeclareLaunchArgument('map', default_value=default_map,
                              description='Đường dẫn file map.yaml'),
        DeclareLaunchArgument('rviz', default_value='true',
                              choices=['true', 'false'],
                              description='Mở RViz2 hiển thị AMCL particle cloud và robot pose'),
    ]

    # 1. Simulation (GroupAction scoped=True để tránh rviz argument ghi đè ra ngoài)
    simulation = GroupAction(
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([sim_launch]),
                launch_arguments=[
                    ('world', LaunchConfiguration('world')),
                    ('rviz', 'false')
                ]
            )
        ],
        scoped=True,
        condition=IfCondition(LaunchConfiguration('launch_sim'))
    )

    # 2. Nav2 Localization (AMCL + Map Server)
    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([nav2_loc_launch]),
        launch_arguments=[
            ('map', LaunchConfiguration('map')),
            ('use_sim_time', LaunchConfiguration('use_sim_time')),
            ('params_file', loc_params),
            ('autostart', 'true')
        ]
    )

    # 3. RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2_localization',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    ld = LaunchDescription(arguments)
    ld.add_action(simulation)
    ld.add_action(localization)
    ld.add_action(rviz_node)
    return ld

