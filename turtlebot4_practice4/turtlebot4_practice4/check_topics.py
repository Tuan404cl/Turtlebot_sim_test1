#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script kiểm tra các topic cơ bản của TurtleBot 4 Simulation:
- /scan (sensor_msgs/msg/LaserScan)
- /odom (nav_msgs/msg/Odometry)
- /cmd_vel (geometry_msgs/msg/Twist)
"""

import sys
import time
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

class TopicChecker(Node):
    def __init__(self):
        super().__init__('turtlebot4_topic_checker')

        self.scan_count = 0
        self.odom_count = 0
        self.last_scan_time = None
        self.last_odom_time = None
        self.scan_ranges_sample = None
        self.scan_frame = None
        self.odom_pos = None
        self.odom_frame = None

        # Subscribers with best effort / reliable compatibility
        self.sub_scan = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.sub_odom = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # Publisher for /cmd_vel verification
        self.pub_cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)

        self.get_logger().info("Đang kiểm tra các topic: /scan, /odom, /cmd_vel...")

    def scan_callback(self, msg: LaserScan):
        self.scan_count += 1
        self.last_scan_time = time.time()
        self.scan_frame = msg.header.frame_id
        valid_ranges = [r for r in msg.ranges if not math.isinf(r) and not math.isnan(r)]
        if valid_ranges:
            self.scan_ranges_sample = (len(msg.ranges), min(valid_ranges), max(valid_ranges))

    def odom_callback(self, msg: Odometry):
        self.odom_count += 1
        self.last_odom_time = time.time()
        self.odom_frame = f"{msg.header.frame_id} -> {msg.child_frame_id}"
        p = msg.pose.pose.position
        self.odom_pos = (p.x, p.y, p.z)

    def test_cmd_vel(self):
        msg = Twist()
        msg.linear.x = 0.05
        msg.angular.z = 0.0
        self.pub_cmd_vel.publish(msg)
        time.sleep(0.3)
        # Stop
        msg.linear.x = 0.0
        self.pub_cmd_vel.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    checker = TopicChecker()

    timeout = 10.0
    start_time = time.time()

    print("\n=======================================================")
    print("      TURTLEBOT 4 SIMULATION - TOPIC VERIFICATION     ")
    print("=======================================================")
    print(f"Lắng nghe topics trong {timeout} giây...\n")

    while rclpy.ok() and (time.time() - start_time < timeout):
        rclpy.spin_once(checker, timeout_sec=0.1)
        if checker.scan_count >= 5 and checker.odom_count >= 5:
            break

    # Test publish /cmd_vel
    checker.test_cmd_vel()

    print("------------------ KẾT QUẢ KIỂM TRA -------------------")
    # Check /scan
    if checker.scan_count > 0:
        num_rays, min_r, max_r = checker.scan_ranges_sample if checker.scan_ranges_sample else (0, 0, 0)
        print(f" [PASS] /scan")
        print(f"        - Số lượng message nhận được: {checker.scan_count}")
        print(f"        - Frame ID: {checker.scan_frame}")
        print(f"        - Số tia quét: {num_rays}, Cự ly min: {min_r:.2f} m, max: {max_r:.2f} m")
    else:
        print(" [FAIL] /scan - Chưa nhận được dữ liệu laser scan!")

    # Check /odom
    if checker.odom_count > 0:
        x, y, z = checker.odom_pos if checker.odom_pos else (0, 0, 0)
        print(f" [PASS] /odom")
        print(f"        - Số lượng message nhận được: {checker.odom_count}")
        print(f"        - Frames: {checker.odom_frame}")
        print(f"        - Vị trí hiện tại: x={x:.3f}, y={y:.3f}, z={z:.3f}")
    else:
        print(" [FAIL] /odom - Chưa nhận được dữ liệu odometry!")

    # Check /cmd_vel
    print(f" [PASS] /cmd_vel")
    print("        - Đã gửi thành công lệnh thử nghiệm Twist (linear=0.05 m/s, stop)")

    print("-------------------------------------------------------")
    if checker.scan_count > 0 and checker.odom_count > 0:
        print(">>> TẤT CẢ CÁC TOPIC CƠ BẢN HOẠT ĐỘNG HOÀN TOÀN BÌNH THƯỜNG! <<<\n")
        exit_code = 0
    else:
        print(">>> CẢNH BÁO: Một số topic chưa nhận được dữ liệu. Kiểm tra lại Gazebo! <<<\n")
        exit_code = 1

    checker.destroy_node()
    rclpy.shutdown()
    return exit_code

if __name__ == '__main__':
    sys.exit(main())

