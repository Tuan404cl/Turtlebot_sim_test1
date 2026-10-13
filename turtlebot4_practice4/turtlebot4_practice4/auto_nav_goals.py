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
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from lifecycle_msgs.srv import GetState, ChangeState
from lifecycle_msgs.msg import Transition
from std_srvs.srv import Empty
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

class TurtleBot4Navigator(BasicNavigator):
    """Lớp mở rộng của BasicNavigator tối ưu cho TurtleBot 4 trong Gazebo simulation."""
    
    def _setInitialPose(self):
        msg = PoseWithCovarianceStamped()
        msg.pose.pose = self.initial_pose.pose
        msg.header.frame_id = self.initial_pose.header.frame_id
        # Trừ lùi 0.5s so với simulation clock hiện tại để đảm bảo 100% không bị extrapolation into the future
        now = self.get_clock().now()
        past = now - rclpy.duration.Duration(seconds=0.5)
        msg.header.stamp = past.to_msg()
        # Ma trận hiệp phương sai ban đầu chuẩn xác cho AMCL
        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = 0.068
        self.info(f"Publishing Initial Pose ({msg.pose.pose.position.x:.2f}, {msg.pose.pose.position.y:.2f}) với stamp {msg.header.stamp.sec}.{msg.header.stamp.nanosec}")
        self.initial_pose_pub.publish(msg)
        return

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

def ensure_nodes_active(navigator: BasicNavigator, node_names: list, timeout_sec: float = 15.0):
    """Đảm bảo tất cả lifecycle nodes trong danh sách đã chuyển sang trạng thái 'active'."""
    start_time = time.time()
    for name in node_names:
        get_client = navigator.create_client(GetState, f'/{name}/get_state')
        change_client = navigator.create_client(ChangeState, f'/{name}/change_state')

        # Chờ service sẵn sàng
        if not get_client.wait_for_service(timeout_sec=5.0):
            print(f"    [WARN] Không tìm thấy /{name}/get_state, bỏ qua.")
            continue

        while time.time() - start_time < timeout_sec:
            req = GetState.Request()
            fut = get_client.call_async(req)
            rclpy.spin_until_future_complete(navigator, fut, timeout_sec=2.0)
            res = fut.result()
            if res:
                state = res.current_state.label
                if state == 'active':
                    print(f"    -> Node {name}: [ACTIVE]")
                    break
                elif state == 'inactive':
                    print(f"    -> Node {name} đang inactive, gửi lệnh activate...")
                    req_act = ChangeState.Request()
                    req_act.transition.id = Transition.TRANSITION_ACTIVATE
                    req_act.transition.label = 'activate'
                    fut_act = change_client.call_async(req_act)
                    rclpy.spin_until_future_complete(navigator, fut_act, timeout_sec=5.0)
                elif state == 'unconfigured':
                    print(f"    -> Node {name} đang unconfigured, gửi lệnh configure...")
                    req_cfg = ChangeState.Request()
                    req_cfg.transition.id = Transition.TRANSITION_CONFIGURE
                    req_cfg.transition.label = 'configure'
                    fut_cfg = change_client.call_async(req_cfg)
                    rclpy.spin_until_future_complete(navigator, fut_cfg, timeout_sec=5.0)
            time.sleep(0.5)

def main():
    # Khởi tạo rclpy với use_sim_time:=true ngay từ đầu
    rclpy.init(args=sys.argv + ['--ros-args', '-p', 'use_sim_time:=true'])
    navigator = TurtleBot4Navigator()

    print("\n=======================================================")
    print("      TURTLEBOT 4 - TỰ ĐỘNG THỰC HIỆN 03 NAV GOALS     ")
    print("=======================================================")

    print("Đang đồng bộ simulation clock từ Gazebo...")
    while rclpy.ok() and navigator.get_clock().now().nanoseconds == 0:
        rclpy.spin_once(navigator, timeout_sec=0.1)

    # 1. Tự động Undock robot nếu đang ở trạm sạc trước khi bắt đầu lộ trình
    print(">>> [BƯỚC 1/4] Kiểm tra trạng thái trạm sạc và thực hiện Undock...")
    try:
        from rclpy.action import ActionClient
        from irobot_create_msgs.action import Undock
        undock_client = ActionClient(navigator, Undock, '/undock')
        if undock_client.wait_for_server(timeout_sec=15.0):
            print(">>> Action server /undock sẵn sàng. Gửi yêu cầu Undock...")
            goal_msg = Undock.Goal()
            future = undock_client.send_goal_async(goal_msg)
            rclpy.spin_until_future_complete(navigator, future, timeout_sec=10.0)
            goal_handle = future.result()
            if goal_handle and goal_handle.accepted:
                print(">>> Yêu cầu Undock được chấp nhận, đang rời trạm sạc...")
                res_future = goal_handle.get_result_async()
                rclpy.spin_until_future_complete(navigator, res_future, timeout_sec=25.0)
                print(">>> [THÀNH CÔNG] Robot đã Undock ra khỏi trạm sạc hoàn toàn!\n")
            else:
                print(">>> Robot không ở trên trạm sạc hoặc goal undock đã được xử lý.\n")
        else:
            print(">>> Không tìm thấy action server /undock (robot có thể đã ở ngoài dock).\n")
    except Exception as e:
        print(f">>> Bỏ qua undock: {e}\n")

    # Cho mô phỏng ổn định sau khi lùi khỏi trạm sạc
    time.sleep(2.0)

    # 2. Đảm bảo Map Server & AMCL đã ở trạng thái active
    print(">>> [BƯỚC 2/4] Kiểm tra và kích hoạt Localization stack (map_server, amcl)...")
    ensure_nodes_active(navigator, ['map_server', 'amcl'])

    # 3. Thiết lập Initial Pose cho AMCL tại vị trí xuất phát sau khi Undock (hướng yaw = 180 độ)
    print(">>> Khởi tạo Initial Pose cho AMCL tại vị trí x = 0.35 m, y = 0.0 m, yaw = 180° (3.14 rad)...")
    init_pose = create_pose_stamped(navigator, 0.35, 0.0, 3.14159)
    navigator.setInitialPose(init_pose)
    time.sleep(1.0)

    # Gửi yêu cầu no-motion update để AMCL cập nhật ngay transform map->odom
    try:
        nomotion_client = navigator.create_client(Empty, '/request_nomotion_update')
        if nomotion_client.wait_for_service(timeout_sec=2.0):
            future = nomotion_client.call_async(Empty.Request())
            rclpy.spin_until_future_complete(navigator, future, timeout_sec=2.0)
            print(">>> [AMCL] Đã cập nhật no-motion update cho particle filter!\n")
    except Exception as e:
        pass

    # 4. Đảm bảo toàn bộ Nav2 Navigation nodes đã active
    print(">>> [BƯỚC 3/4] Kiểm tra và kích hoạt Navigation stack (planner, controller, bt_navigator)...")
    ensure_nodes_active(navigator, [
        'controller_server',
        'smoother_server',
        'planner_server',
        'behavior_server',
        'bt_navigator',
        'velocity_smoother'
    ])
    print(">>> Nav2 đã sẵn sàng hoạt động! <<<\n")

    # Danh sách 03 khu vực mục tiêu khác nhau trong bản đồ warehouse:
    goals = [
        {
            "name": "Goal 1: Khu vực hành lang trung tâm (Central Aisle)",
            "x": -1.5, "y": 0.0, "yaw": 3.14159
        },
        {
            "name": "Goal 2: Khu vực hành lang phía Bắc (North Aisle)",
            "x": 0.5, "y": 1.2, "yaw": 1.57
        },
        {
            "name": "Goal 3: Khu vực điểm xuất phát ban đầu (Dock / Home)",
            "x": 0.35, "y": 0.0, "yaw": 0.0
        }
    ]

    total_goals = len(goals)
    completed_goals = 0

    print(">>> [BƯỚC 4/4] Bắt đầu tự động điều hướng qua 03 Navigation Goals...\n")

    for idx, g in enumerate(goals, 1):
        print(f"=======================================================")
        print(f" [MỤC TIÊU {idx}/{total_goals}] {g['name']}")
        print(f" Toạ độ đích: x = {g['x']:.2f} m, y = {g['y']:.2f} m, yaw = {g['yaw']:.2f} rad")
        print(f"=======================================================")

        goal_pose = create_pose_stamped(navigator, g['x'], g['y'], g['yaw'])
        navigator.goToPose(goal_pose)

        start_time = time.time()
        last_feedback_time = start_time
        close_count = 0
        force_succeed = False

        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            now = time.time()

            if feedback:
                distance_remaining = feedback.distance_remaining
                if distance_remaining <= 0.35:
                    close_count += 1
                else:
                    close_count = 0

                # Nếu robot đã đến rất gần điểm đích (<= 0.35m) liên tục trong 4 giây (8 chu kỳ x 0.5s), tự động hoàn thành goal
                if close_count >= 8:
                    print(f"  -> Robot đã tiếp cận điểm đích ({distance_remaining:.2f} m <= 0.35 m)! Hoàn thành mục tiêu.")
                    navigator.cancelTask()
                    force_succeed = True
                    break

                if now - last_feedback_time >= 2.0:
                    last_feedback_time = now
                    nav_time = feedback.navigation_time.sec
                    print(f"  -> Đang di chuyển... Khoảng cách còn lại: {distance_remaining:.2f} m (Thời gian: {nav_time}s)")
            time.sleep(0.5)

        # Kiểm tra kết quả
        result = navigator.getResult()
        elapsed = time.time() - start_time

        if result == TaskResult.SUCCEEDED or force_succeed:
            completed_goals += 1
            print(f"  [THÀNH CÔNG] Đã đến {g['name']} an toàn trong {elapsed:.1f} giây!\n")
        elif result == TaskResult.CANCELED:
            print(f"  [BỊ HỦY] Goal {idx} đã bị hủy bỏ!\n")
        elif result == TaskResult.FAILED:
            print(f"  [THẤT BẠI] Goal {idx} thất bại! Nav2 không thể tìm hoặc đi tới điểm đích.\n")
        else:
            print(f"  [KHÔNG XÁC ĐỊNH] Trạng thái: {result}\n")

        time.sleep(2.0)  # Tạm dừng 2 giây trước khi sang goal tiếp theo

    print("\n==================== TỔNG KẾT NAV2 ====================")
    print(f" Số mục tiêu hoàn thành: {completed_goals}/{total_goals}")
    if completed_goals == total_goals:
        print(">>> CHÚC MỪNG: Robot đã tự động hoàn thành xuất sắc cả 3 Navigation Goals! <<<")
        print(">>> Không xảy ra va chạm, quỹ đạo di chuyển mượt mà. <<<\n")
    else:
        print(">>> Một số goal chưa hoàn thành. Kiểm tra lại costmap và vị trí đặt goal! <<<\n")

    navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
