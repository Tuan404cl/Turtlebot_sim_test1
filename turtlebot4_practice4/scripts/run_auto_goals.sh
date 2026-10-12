#!/usr/bin/env bash
# ==============================================================================
# Script tự động thực hiện 03 Navigation Goals trong Nav2
# ==============================================================================
set -e

source /opt/ros/humble/setup.bash
if [ -f "/home/tuan/turtelbot4_ws/install/setup.bash" ]; then
    source /home/tuan/turtelbot4_ws/install/setup.bash
fi

echo "======================================================="
echo "   CHẠY TỰ ĐỘNG 03 GOALS AUTONOMOUS NAVIGATION        "
echo "======================================================="
echo "Yêu cầu: Phần 4 (Nav2 Stack) đang chạy ở một terminal khác."
echo "Khởi chạy kịch bản tự động điều hướng qua 3 vùng khác nhau..."
echo "======================================================="

ros2 run turtlebot4_practice4 auto_nav_goals

