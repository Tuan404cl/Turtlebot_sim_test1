#!/usr/bin/env bash
# ==============================================================================
# Script điều khiển thủ công TurtleBot 4 bằng bàn phím (teleoperation)
# ==============================================================================
set -e

source /opt/ros/humble/setup.bash

echo "======================================================="
echo "   ĐIỀU KHIỂN TURTLEBOT 4 BẰNG BÀN PHÍM (TELEOP)      "
echo "======================================================="
echo "Hướng dẫn phím:"
echo "   i : Tiến tới"
echo "   , : Lùi lại"
echo "   j : Rẽ trái"
echo "   l : Rẽ phải"
echo "   k : Dừng lại"
echo "   w / x : Tăng / giảm tốc độ tuyến tính"
echo "   e / c : Tăng / giảm tốc độ góc"
echo "======================================================="

ros2 run teleop_twist_keyboard teleop_twist_keyboard
