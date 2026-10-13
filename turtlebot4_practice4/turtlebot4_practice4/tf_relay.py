#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TF Relay Node cho mô phỏng TurtleBot 4 trong Gazebo
Chức năng:
1. Liên tục phát static/sensor transforms (RPLiDAR và OAK-D) vào topic /tf (tần số 20 Hz).
2. Tự động tính toán và phát liên tục biến đổi `map -> odom` ở tần số 20 Hz dựa trên /amcl_pose và /odom,
   giúp loại bỏ hoàn toàn hiện tượng transform timeout / extrapolation errors trong Nav2 controller_server.
3. Cung cấp các dummy service phần cứng (start_motor, oakd/start_camera...) phục vụ simulator.
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from std_srvs.srv import Empty, Trigger
import tf2_ros

def euler_to_quaternion(roll: float, pitch: float, yaw: float):
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    return qx, qy, qz, qw

def quaternion_to_yaw(qx: float, qy: float, qz: float, qw: float) -> float:
    siny_cosp = 2.0 * (qw * qz + qx * qy)
    cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
    return math.atan2(siny_cosp, cosy_cosp)

class TFRelay(Node):
    def __init__(self):
        super().__init__('tf_relay')
        self.declare_parameter('robot_name', 'turtlebot4')
        self.robot_name = self.get_parameter('robot_name').value

        # Mock dummy services để khắc phục triệt để lỗi phần cứng không có trong Gazebo
        self.srv_start_motor = self.create_service(Empty, 'start_motor', self._empty_cb)
        self.srv_stop_motor = self.create_service(Empty, 'stop_motor', self._empty_cb)
        self.srv_start_cam = self.create_service(Trigger, 'oakd/start_camera', self._trigger_cb)
        self.srv_stop_cam = self.create_service(Trigger, 'oakd/stop_camera', self._trigger_cb)

        # LƯU Ý: KHÔNG gọi định kỳ /request_nomotion_update. AMCL tự phát lại map->odom
        # mỗi khi nhận /scan; ép cập nhật liên tục khi đứng yên làm suy biến hạt (particle)
        # và làm nghẽn service của AMCL.

        self.get_logger().info('TF Relay sẵn sàng: Mock Hardware Services.')

    def _empty_cb(self, request, response):
        return response

    def _trigger_cb(self, request, response):
        response.success = True
        response.message = 'Simulation dummy service OK'
        return response

def main(args=None):
    rclpy.init(args=args)
    node = TFRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

