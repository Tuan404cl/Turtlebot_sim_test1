#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launch file khởi chạy toàn bộ ngăn xếp Autonomous Navigation (Nav2) cho TurtleBot 4
Phần 4: Navigation với Nav2
Bao gồm:
- Gazebo simulation (TurtleBot 4 trong warehouse)
- Map Server & AMCL (Localization với bản đồ đã tạo)
- Nav2 Controller, Planner, Recoveries, BT Navigator
- RViz2 với công cụ Nav2 Goal
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
    pkg_tb4_nav = get_package_share_directory('turtlebot4_navigation')

    sim_launch = PathJoinSubstitution([pkg_practice, 'launch', 'sim_robot.launch.py'])
    default_map = PathJoinSubstitution([pkg_practice, 'maps', 'map.yaml'])
    loc_params = PathJoinSubstitution([pkg_practice, 'config', 'localization_params.yaml'])
    nav2_params = PathJoinSubstitution([pkg_practice, 'config', 'nav2_params.yaml'])
    rviz_config = PathJoinSubstitution([pkg_practice, 'config', 'turtlebot4_nav2.rviz'])

    tb4_loc_launch = PathJoinSubstitution([pkg_tb4_nav, 'launch', 'localization.launch.py'])
    tb4_nav_launch = PathJoinSubstitution([pkg_tb4_nav, 'launch', 'nav2.launch.py'])

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
                              description='Mở RViz2 hiển thị Nav2 Goal, Costmaps, Path'),
    ]

    # 1. Gazebo Simulation
    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([sim_launch]),
        launch_arguments=[
            ('world', LaunchConfiguration('world')),
            ('rviz', 'false')
        ],
        condition=IfCondition(LaunchConfiguration('launch_sim'))
    )

    # 2. Localization (AMCL + Map Server)
    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([tb4_loc_launch]),
        launch_arguments=[
            ('map', LaunchConfiguration('map')),
            ('params', loc_params),
            ('use_sim_time', LaunchConfiguration('use_sim_time'))
        ]
    )

    # 3. Nav2 Navigation (Planner, Controller, Recoveries, BT Navigator)
    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([tb4_nav_launch]),
        launch_arguments=[
            ('params_file', nav2_params),
            ('use_sim_time', LaunchConfiguration('use_sim_time'))
        ]
    )

    # 4. RViz2 Navigation View
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2_nav2',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    ld = LaunchDescription(arguments)
    ld.add_action(simulation)
    ld.add_action(localization)
    ld.add_action(navigation)
    ld.add_action(rviz_node)
    return ld

