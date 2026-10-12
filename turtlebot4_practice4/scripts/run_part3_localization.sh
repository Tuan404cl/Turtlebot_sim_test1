#!/usr/bin/env bash
# ==============================================================================
# Script thực thi Phần 3: Localization với bản đồ đã tạo
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/clean_ros.sh" > /dev/null 2>&1 || true

source /opt/ros/humble/setup.bash
if [ -f "/home/tuan/turtelbot4_ws/install/setup.bash" ]; then
    source /home/tuan/turtelbot4_ws/install/setup.bash
fi

MAP_FILE="/home/tuan/turtelbot4_ws/src/turtlebot4_practice4/maps/map.yaml"

echo "======================================================="
echo "   PHẦN 3: LOCALIZATION VỚI BẢN ĐỒ VỪA TẠO (AMCL)     "
echo "======================================================="
echo "Bản đồ sử dụng: $MAP_FILE"
echo "1. Khởi chạy Gazebo simulation + AMCL + Map Server + RViz2."
echo "2. Trên RViz2, sử dụng công cụ '2D Pose Estimate' để gán vị trí ước lượng ban đầu nếu cần."
echo "3. Lái nhẹ robot để quan sát các hạt (particle cloud) hội tụ về vị trí thực tế của robot."
echo "======================================================="

ros2 launch turtlebot4_practice4 sim_localization.launch.py map:="$MAP_FILE" world:=warehouse rviz:=true

