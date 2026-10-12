#!/usr/bin/env bash
# ==============================================================================
# Script dọn dẹp triệt để các tiến trình ROS 2 & Gazebo chạy ngầm bị kẹt
# ==============================================================================
echo "Đang dọn dẹp toàn bộ tiến trình ROS 2, Gazebo và bridges chạy ngầm..."

pids=$(ps -eo pid,cmd | grep -E "parameter_bridge|irobot_create|slam_toolbox|robot_state_publisher|joint_state_publisher|static_transform_publisher|turtlebot4_node|turtlebot4_ignition|ign gazebo|nav2_" | grep -v grep | grep -v "clean_ros" | awk '{print $1}')

if [ -n "$pids" ]; then
    kill -9 $pids 2>/dev/null || true
fi

pkill -9 -f "ign gazebo" 2>/dev/null || true
pkill -9 -f "ros2 launch" 2>/dev/null || true
ros2 daemon stop 2>/dev/null || true

sleep 1
echo "======================================================="
echo ">>> ĐÃ DỌN DẸP SẠCH TOÀN BỘ TIẾN TRÌNH THÀNH CÔNG! <<<"
echo "Bây giờ bạn có thể khởi chạy lại bình thường."
echo "======================================================="
