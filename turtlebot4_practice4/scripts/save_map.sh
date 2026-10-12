#!/usr/bin/env bash
# ==============================================================================
# Script lưu bản đồ từ SLAM Toolbox thành map.yaml và map.pgm
# ==============================================================================
set -e

source /opt/ros/humble/setup.bash

# Thư mục lưu map
MAP_DIR="/home/tuan/turtelbot4_ws/src/turtlebot4_practice4/maps"
mkdir -p "$MAP_DIR"

MAP_NAME="${1:-map}"
OUTPUT_PATH="$MAP_DIR/$MAP_NAME"

echo "======================================================="
echo "   LƯU BẢN ĐỒ SLAM TOOLBOX RA FILE                    "
echo "======================================================="
echo "Đang lưu bản đồ tới: $OUTPUT_PATH.yaml và $OUTPUT_PATH.pgm ..."

ros2 run nav2_map_server map_saver_cli -f "$OUTPUT_PATH" --ros-args -p save_map_timeout:=10.0

if [ -f "$OUTPUT_PATH.yaml" ] && [ -f "$OUTPUT_PATH.pgm" ]; then
    echo "======================================================="
    echo " [THÀNH CÔNG] Bản đồ đã được lưu thành công:"
    echo "  - Metadata: $OUTPUT_PATH.yaml"
    echo "  - Image:    $OUTPUT_PATH.pgm"
    echo "======================================================="
else
    echo " [LỖI] Không thể lưu bản đồ. Vui lòng kiểm tra topic /map đang active!"
    exit 1
fi

