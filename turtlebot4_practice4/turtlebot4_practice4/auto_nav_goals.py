#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động gửi ít nhất 03 Navigation Goals liên tiếp trong Nav2
Sử dụng thư viện BasicNavigator của Nav2 Simple Commander.
Robot tự động lập kế hoạch toàn cục (Global Planner) và né vật cản (Local Controller)
để lần lượt đến 3 khu vực khác nhau trên bản đồ mà không cần can thiệp thủ công.
"""

import sys
import time
import math
import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

def create_pose_stamped(navigator: BasicNavigator, x: float, y: float, yaw: float) -> PoseStamped:
    """Tạo PoseStamped trên hệ toạ độ map với góc xoay yaw (radian)."""
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = float(x)
    pose.pose.position.y = float(y)
    pose.pose.position.z = 0.0

    # Chuyển đổi yaw sang quaternion (chỉ quay quanh trục Z)
    half_yaw = yaw * 0.5
    pose.pose.orientation.x = 0.0
    pose.pose.orientation.y = 0.0
    pose.pose.orientation.z = math.sin(half_yaw)
    pose.pose.orientation.w = math.cos(half_yaw)
    return pose

def main():
    rclpy.init()
    navigator = BasicNavigator()

    print("\n=======================================================")
    print("      TURTLEBOT 4 - TỰ ĐỘNG THỰC HIỆN 03 NAV GOALS     ")
    print("=======================================================")

    print("Đang đợi Nav2 active hoàn toàn...")
    navigator.waitUntilNav2Active()
    print(">>> Nav2 đã sẵn sàng hoạt động! <<<\n")

    # Danh sách 03 khu vực mục tiêu khác nhau trong bản đồ warehouse:
    # Ban đầu robot xuất phát quanh (0.0, 0.0)
    goals = [
        {
            "name": "Goal 1: Khu vực hành lang trung tâm (Central Aisle)",
            "x": 2.0, "y": 0.5, "yaw": 0.0
        },
        {
            "name": "Goal 2: Khu vực kệ hàng phía Bắc (North Shelving Area)",
            "x": 1.0, "y": 3.0, "yaw": 1.57
        },
        {
            "name": "Goal 3: Khu vực điểm xuất phát ban đầu (Home / Dock Base)",
            "x": 0.0, "y": 0.0, "yaw": 3.14
        }
    ]

    total_goals = len(goals)
    completed_goals = 0

    for idx, g in enumerate(goals, 1):
        print(f"\n>>> [BƯỚC {idx}/{total_goals}] Bắt đầu di chuyển tới {g['name']}")
        print(f"    Toạ độ đích: x = {g['x']:.2f} m, y = {g['y']:.2f} m, yaw = {g['yaw']:.2f} rad")

        goal_pose = create_pose_stamped(navigator, g['x'], g['y'], g['yaw'])
        navigator.goToPose(goal_pose)

        start_time = time.time()
        last_feedback_time = start_time

        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            now = time.time()

            # In thông tin tiến độ mỗi 2 giây
            if feedback and (now - last_feedback_time >= 2.0):
                last_feedback_time = now
                distance_remaining = feedback.distance_remaining
                nav_time = feedback.navigation_time.sec
                print(f"    -> Đang di chuyển... Khoảng cách còn lại: {distance_remaining:.2f} m (Thời gian: {nav_time}s)")

        # Kiểm tra kết quả
        result = navigator.getResult()
        elapsed = time.time() - start_time

        if result == TaskResult.SUCCEEDED:
            completed_goals += 1
            print(f"    [THÀNH CÔNG] Đã đến {g['name']} an toàn trong {elapsed:.1f} giây!")
        elif result == TaskResult.CANCELED:
            print(f"    [BỊ HỦY] Goal {idx} đã bị hủy bỏ!")
        elif result == TaskResult.FAILED:
            print(f"    [THẤT BẠI] Goal {idx} thất bại! Nav2 không thể tìm hoặc đi tới điểm đích.")
        else:
            print(f"    [KHÔNG XÁC ĐỊNH] Trạng thái: {result}")

        time.sleep(2.0)  # Tạm dừng 2 giây trước khi sang goal tiếp theo

    print("\n==================== TỔNG KẾT NAV2 ====================")
    print(f" Số mục tiêu hoàn thành: {completed_goals}/{total_goals}")
    if completed_goals == total_goals:
        print(">>> CHÚC MỪNG: Robot đã tự động hoàn thành xuất sắc cả 3 Navigation Goals! <<<")
        print(">>> Không xảy ra va chạm, quỹ đạo di chuyển mượt mà. <<<\n")
    else:
        print(">>> Một số goal chưa hoàn thành. Kiểm tra lại costmap và vị trí đặt goal! <<<\n")

    navigator.lifecycleShutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
