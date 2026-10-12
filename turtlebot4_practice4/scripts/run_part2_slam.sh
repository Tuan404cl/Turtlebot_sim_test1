#!/usr/bin/env bash
# ==============================================================================
# Script thực thi Phần 2: Xây dựng bản đồ bằng SLAM Toolbox
# ==============================================================================
set -e

source /opt/ros/humble/setup.bash
if [ -f "/home/tuan/turtelbot4_ws/install/setup.bash" ]; then
    source /home/tuan/turtelbot4_ws/install/setup.bash
fi

echo "======================================================="
echo "   PHẦN 2: XÂY DỰNG BẢN ĐỒ VỚI SLAM TOOLBOX & RVIZ2   "
echo "======================================================="
echo "Đang khởi chạy Gazebo simulation + SLAM Toolbox + RViz2..."
echo "Mẹo: Mở một terminal khác và chạy ./run_teleop.sh để lái robot khảo sát môi trường!"
echo "Khi hoàn thành bản đồ, mở một terminal khác và chạy ./save_map.sh để lưu map.yaml và map.pgm."
echo "======================================================="

ros2 launch turtlebot4_practice4 sim_slam.launch.py world:=warehouse rviz:=true
