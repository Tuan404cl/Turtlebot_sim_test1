#!/usr/bin/env bash
# ==============================================================================
# Script thực thi Phần 4: Autonomous Navigation với Nav2
# ==============================================================================
set -e

source /opt/ros/humble/setup.bash
if [ -f "/home/tuan/turtelbot4_ws/install/setup.bash" ]; then
    source /home/tuan/turtelbot4_ws/install/setup.bash
fi

MAP_FILE="/home/tuan/turtelbot4_ws/src/turtlebot4_practice4/maps/map.yaml"

echo "======================================================="
echo "   PHẦN 4: AUTONOMOUS NAVIGATION VỚI NAV2             "
echo "======================================================="
echo "Bản đồ sử dụng: $MAP_FILE"
echo "1. Đang khởi chạy Gazebo simulation + Nav2 Stack + RViz2..."
echo "2. Cách 1: Trên RViz2, nhấn công cụ 'Nav2 Goal' trên thanh công cụ và click chọn đích đến."
echo "3. Cách 2: Mở terminal khác và chạy ./run_auto_goals.sh để robot tự động đi qua 03 khu vực khác nhau."
echo "======================================================="

ros2 launch turtlebot4_practice4 sim_navigation.launch.py map:="$MAP_FILE" world:=warehouse rviz:=true
