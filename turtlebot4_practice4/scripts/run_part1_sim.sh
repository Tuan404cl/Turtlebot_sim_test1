#!/usr/bin/env bash
# ==============================================================================
# Script thực thi Phần 1: Khởi chạy TurtleBot 4 Simulation và kiểm tra topics
# ==============================================================================
set -e

# Source ROS 2 Humble và Workspace
source /opt/ros/humble/setup.bash
if [ -f "/home/tuan/turtelbot4_ws/install/setup.bash" ]; then
    source /home/tuan/turtelbot4_ws/install/setup.bash
fi

echo "======================================================="
echo "   PHẦN 1: KHỞI CHẠY TURTLEBOT 4 TRONG GAZEBO SIM     "
echo "======================================================="
echo "1. Đang khởi chạy mô phỏng thế giới warehouse..."
echo "2. Nhấn Ctrl+C để dừng mô phỏng khi hoàn tất."
echo "======================================================="

ros2 launch turtlebot4_practice4 sim_robot.launch.py world:=warehouse rviz:=true

