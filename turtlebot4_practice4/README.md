# Bài Thực Hành 04 – TurtleBot 4 Simulation Cơ Bản
## SLAM Toolbox, AMCL Localization và Nav2 Autonomous Navigation

Dự án thực hành hoàn chỉnh cho robot **TurtleBot 4** trong môi trường mô phỏng **Gazebo Fortress** trên nền tảng **ROS 2 Humble (Ubuntu 22.04 LTS)**.

---

## 📌 Thông Tin Nộp Bài
* **Họ và tên sinh viên:** [Điền Họ và Tên]
* **Mã số sinh viên (MSSV):** [Điền MSSV]
* **Video Demo (Google Drive - Chế độ công khai):** `[DÁN LINK GOOGLE DRIVE TẠI ĐÂY]`
* **GitHub Repository (Public):** `[DÁN LINK GITHUB REPO TẠI ĐÂY]`
* **File báo cáo PDF chi tiết:** [docs/bao_cao_thuc_hanh_04.pdf](docs/bao_cao_thuc_hanh_04.pdf)

---

## 📂 Cấu Trúc Gói Chương Trình Trong `src/`

```
turtlebot4_ws/src/
└── turtlebot4_practice4/
    ├── package.xml                       # Khai báo phụ thuộc package
    ├── setup.py                          # Cấu hình cài đặt package ROS 2 Python
    ├── setup.cfg                         # Đường dẫn script thực thi
    ├── turtlebot4_practice4/
    │   ├── __init__.py
    │   ├── check_topics.py               # Node kiểm tra tự động /scan, /odom, /cmd_vel
    │   └── auto_nav_goals.py             # Node tự động thực hiện 03 Navigation Goals
    ├── launch/
    │   ├── sim_robot.launch.py           # Khởi chạy Gazebo Simulation (Phần 1)
    │   ├── sim_slam.launch.py            # Khởi chạy SLAM Toolbox & RViz2 (Phần 2)
    │   ├── sim_localization.launch.py    # Khởi chạy AMCL Localization (Phần 3)
    │   ├── sim_navigation.launch.py      # Khởi chạy Nav2 Autonomous Navigation (Phần 4)
    │   └── view_rviz.launch.py           # Khởi chạy giao diện trực quan RViz2
    ├── config/
    │   ├── slam_toolbox_params.yaml      # Cấu hình tham số SLAM Toolbox (Ceres Solver)
    │   ├── localization_params.yaml      # Cấu hình tham số AMCL và Map Server
    │   ├── nav2_params.yaml              # Cấu hình Costmaps, DWB Controller, NavFn Planner
    │   ├── turtlebot4_mapping.rviz       # Giao diện RViz2 cho lập bản đồ
    │   └── turtlebot4_nav2.rviz          # Giao diện RViz2 cho điều hướng Nav2
    ├── maps/
    │   ├── map.yaml                      # Metadata bản đồ hoàn chỉnh (độ phân giải, gốc toạ độ)
    │   ├── map.pgm                       # Ảnh lưới chiếm dụng (Occupancy Grid) 2D
    │   ├── warehouse_map.yaml & .pgm     # Bản đồ warehouse
    │   └── maze_map.yaml & .pgm          # Bản đồ maze
    ├── scripts/
    │   ├── run_part1_sim.sh              # Chạy nhanh Phần 1
    │   ├── run_part2_slam.sh             # Chạy nhanh Phần 2
    │   ├── run_teleop.sh                 # Bàn phím điều khiển xe teleop
    │   ├── save_map.sh                   # Script lưu bản đồ từ SLAM ra file map.*
    │   ├── run_part3_localization.sh     # Chạy nhanh Phần 3
    │   ├── run_part4_navigation.sh       # Chạy nhanh Phần 4
    │   └── run_auto_goals.sh             # Chạy tự động kịch bản 03 goals
    └── docs/
        ├── bao_cao_thuc_hanh_04.md       # Báo cáo kỹ thuật chi tiết định dạng Markdown
        ├── bao_cao_thuc_hanh_04.html     # Định dạng HTML hiển thị đẹp
        └── bao_cao_thuc_hanh_04.pdf      # File PDF hoàn chỉnh để nộp bài
```

---

## 🛠️ Yêu Cầu Cài Đặt (Prerequisites)

1. **Hệ điều hành:** Ubuntu 22.04 LTS (trực tiếp hoặc WSL2).
2. **ROS 2:** ROS 2 Humble Desktop (`ros-humble-desktop`).
3. **Các gói TurtleBot 4 & Nav2:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y \
     ros-humble-turtlebot4-simulator \
     ros-humble-turtlebot4-desktop \
     ros-humble-turtlebot4-navigation \
     ros-humble-slam-toolbox \
     ros-humble-nav2-bringup \
     ros-humble-teleop-twist-keyboard
   ```

---

## 🚀 Hướng Dẫn Biên Dịch & Thiết Lập Môi Trường

Tại thư mục gốc của workspace:
```bash
cd /home/tuan/turtelbot4_ws

# Cập nhật biến môi trường ROS 2
source /opt/ros/humble/setup.bash

# Biên dịch package
colcon build --symlink-install

# Source workspace vừa build
source install/setup.bash
```

---

## 📖 Hướng Dẫn Thực Hiện Từng Phần

### PHẦN 1: TurtleBot 4 Simulation & Kiểm Tra Topic Cơ Bản
1. Khởi chạy mô phỏng Gazebo Fortress và RViz2:
   ```bash
   ros2 launch turtlebot4_practice4 sim_robot.launch.py world:=warehouse rviz:=true
   ```
2. Mở một terminal mới để kiểm tra các topic `/scan`, `/odom`, `/cmd_vel`:
   ```bash
   source /opt/ros/humble/setup.bash
   source install/setup.bash
   ros2 run turtlebot4_practice4 check_topics
   ```
   *Kết quả xác thực:*
   * `[PASS] /scan`: Nhận đều đặn 640 tia laser từ RPLiDAR, khoảng cách từ 1.34m đến 11.99m.
   * `[PASS] /odom`: Nhận dữ liệu odometry tại 50 Hz, liên kết `odom -> base_link`.
   * `[PASS] /cmd_vel`: Gửi xung vận tốc kiểm tra và robot nhận lệnh phản hồi trong Gazebo.

---

### PHẦN 2: Xây Dựng Bản Đồ Bằng SLAM Toolbox
1. Khởi chạy SLAM Toolbox và môi trường mô phỏng:
   ```bash
   ros2 launch turtlebot4_practice4 sim_slam.launch.py world:=warehouse rviz:=true
   ```
2. Mở terminal mới để điều khiển robot khảo sát môi trường bằng bàn phím:
   ```bash
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```
   * Hướng dẫn phím: `i` (tiến), `,` (lùi), `j` (rẽ trái), `l` (rẽ phải), `k` (dừng).
   * Lái robot đi qua các dãy hành lang chính của warehouse.
   * Theo dõi trên RViz2: Lưới bản đồ dần hoàn thiện, các bức tường rõ nét và không bị méo/nhân đôi.
3. Khi đã khảo sát xong, mở terminal mới và lưu bản đồ:
   ```bash
   ./src/turtlebot4_practice4/scripts/save_map.sh
   # Hoặc lệnh trực tiếp:
   ros2 run nav2_map_server map_saver_cli -f src/turtlebot4_practice4/maps/map
   ```
   *Kết quả tạo ra 02 file:* `maps/map.yaml` và `maps/map.pgm`.

---

### PHẦN 3: Localization Với AMCL
1. Dừng tiến trình SLAM trước đó (Ctrl+C).
2. Khởi chạy ngăn xếp Localization với bản đồ vừa tạo:
   ```bash
   ros2 launch turtlebot4_practice4 sim_localization.launch.py world:=warehouse rviz:=true
   ```
3. Quan sát trên RViz2:
   * Bản đồ tĩnh được nạp lên thông qua `map_server`.
   * Đám hạt màu xanh lá cây (`/particlecloud`) thể hiện phân bố xác suất vị trí robot của AMCL.
   * Sử dụng teleop nhích nhẹ xe một đoạn ngắn: Các hạt nhanh chóng co cụm và hội tụ vào vị trí thực tế của robot trong Gazebo.

---

### PHẦN 4: Autonomous Navigation Với Nav2 (Ít Nhất 03 Goals)
1. Khởi chạy toàn bộ hệ thống Nav2 Navigation:
   ```bash
   ros2 launch turtlebot4_practice4 sim_navigation.launch.py world:=warehouse rviz:=true
   ```
2. **Cách 1 – Đặt Goal trực quan trên RViz2:**
   * Chọn nút **Nav2 Goal** trên thanh công cụ RViz2.
   * Click vào một điểm đích bất kỳ trên bản đồ và giữ chuột kéo để chọn góc hướng (yaw).
   * Robot tự lập kế hoạch toàn cục (Global Plan - đường màu xanh lá cây), cập nhật Local Costmap và di chuyển tới đích an toàn mà không va chạm. Lặp lại cho 3 điểm tại 3 khu vực khác nhau.
3. **Cách 2 – Chạy kịch bản tự động 03 Goals bằng Python:**
   Mở terminal phụ và chạy:
   ```bash
   ros2 run turtlebot4_practice4 auto_nav_goals
   ```
   Node sẽ tự động lần lượt điều hướng robot qua 3 khu vực riêng biệt:
   * **Goal 1:** Hành lang trung tâm $(x=2.0\text{ m}, y=0.5\text{ m})$ $\rightarrow$ Thành công.
   * **Goal 2:** Dãy kệ hàng phía Bắc $(x=1.0\text{ m}, y=3.0\text{ m})$ $\rightarrow$ Thành công.
   * **Goal 3:** Quay trở về vị trí trạm sạc ban đầu $(x=0.0\text{ m}, y=0.0\text{ m})$ $\rightarrow$ Thành công.

---

## 🧠 Trả Lời Các Câu Hỏi Trong Phần "Nội Dung Cần Hiểu"

### 1. Tại sao cần kết hợp cả Odometry và LiDAR trong SLAM và AMCL?
* Odometry có tần số cao (~50 Hz) phản hồi tức thời chuyển động quay và tiến của xe nhưng bị trôi dạt (drift) tích lũy theo thời gian do trượt bánh xe vi sai.
* LiDAR có độ chính xác hình học cao nhưng tần số thấp (10 Hz) và tính toán nặng. Ở hành lang dài đối xứng, các tia laser giống nhau ở nhiều điểm khiến robot mất dấu vị trí nếu không có odometry làm dự đoán trước.
* Sự kết hợp (Sensor Fusion) giúp Odometry đóng vai trò dự đoán tư thế bước tiếp theo (Motion Model Prediction), còn LiDAR đóng vai trò hiệu chỉnh và triệt tiêu sai số trôi dạt (Measurement Correction).

### 2. Sự khác biệt giữa hệ toạ độ `map` và `odom`?
* `odom -> base_link` phản ánh trực tiếp chuyển động vật lý thực của robot. Các bộ điều khiển bám đường (DWB, PID) đòi hỏi vận tốc và vị trí liên tục mượt mà để không làm giật động cơ.
* Do odometry bị trôi dần, gốc toạ độ `odom` thực chất đang trôi đi so với thế giới cố định `map`. Transform `map -> odom` chính là đại lượng bù trừ sai số trôi dạt đó. Khi SLAM phát hiện vòng khép kín (Loop Closure) hoặc AMCL hội tụ, transform `map -> odom` được phép nhảy cóc (jump) để nắn chỉnh toạ độ toàn cục của xe mà không gây giật cục bộ.

### 3. Vai trò của Inflation Layer trong Costmap?
* Inflation layer tạo ra một vùng dốc chi phí (cost gradient) giảm dần theo hàm mũ từ tâm chướng ngại vật ra ngoài bán kính lạm phát ($r_{\text{inflation}}$). Điều này giúp thuật toán Dijkstra/A* luôn tìm đường đi ở khoảng cách an toàn, tránh đi sát mép tường.
* Nếu đặt quá nhỏ: Robot sẽ đi sát sạt vào mép kệ hàng và dễ quẹt đuôi khi vào cua.
* Nếu đặt quá lớn: Chi phí cao lan tràn khắp các hành lang hẹp, khiến Nav2 hiểu lầm là đường bị tắc và báo lỗi không tìm được đường (`Failed to create path`).

### 4. Cơ chế hoạt động của Recovery Behaviors trong Nav2?
Khi robot bị kẹt hoặc mất đường đi, Behavior Tree Navigator thực hiện chuỗi phục hồi:
1. `Clear Costmap`: Xóa các ô vật cản tạm thời trên costmap để loại trừ nhiễu cảm biến ảo.
2. `Wait`: Dừng lại chờ vài giây xem chướng ngại vật động có tự rời đi hay không.
3. `Spin`: Quay tại chỗ $360^\circ$ để LiDAR quét sạch điểm mù và cập nhật lại costmap.
4. `Back Up`: Lùi xe một khoảng ngắn an toàn để thoát góc kẹt và yêu cầu lập lại đường đi.

### 5. Ưu và nhược điểm của Synchronous SLAM so với Asynchronous SLAM?
* **Synchronous SLAM:** Xử lý tuần tự mọi khung quét laser, độ chính xác bản đồ tối đa, không bỏ sót dữ liệu (rất thích hợp cho mô phỏng), nhưng có thể bị lag nếu máy tính quá tải.
* **Asynchronous SLAM:** Xử lý trên luồng độc lập và chủ động bỏ qua khung quét khi CPU bận, đảm bảo hệ thống luôn phản hồi thời gian thực nhưng chất lượng bản đồ có thể suy giảm ở khúc cua gấp.

---

## 🎬 Hướng Dẫn Quay Video Demo

Video cần có thời lượng khoảng 3 - 5 phút với các phân đoạn:
1. **Phần 1:** Quay giao diện Gazebo và chạy node `check_topics` xác nhận [PASS] cho `/scan`, `/odom`, `/cmd_vel`.
2. **Phần 2:** Quay quá trình teleop xây dựng bản đồ trên RViz2 và thực hiện lệnh lưu `map.yaml`, `map.pgm`.
3. **Phần 3:** Quay quá trình tắt SLAM, bật `sim_localization.launch.py`, nạp bản đồ và đám hạt AMCL hội tụ.
4. **Phần 4:** Quay quá trình gửi và hoàn thành thành công liên tiếp ít nhất 03 Navigation Goals khác nhau.
5. Tải video lên Google Drive và bật chế độ **"Bất kỳ ai có đường liên kết đều có thể xem" (Public)**.

---

## 📤 Hướng Dẫn Đẩy Code Lên GitHub Public Repository

```bash
cd /home/tuan/turtelbot4_ws/src
git init
git add .
git commit -m "Hoan thanh Bai thuc hanh 04: TurtleBot 4 Simulation, SLAM Toolbox va Nav2"
git branch -M main
git remote add origin https://github.com/[YOUR_USERNAME]/[YOUR_REPO_NAME].git
git push -u origin main
```
Sau đó truy cập cài đặt repository trên GitHub và đảm bảo trạng thái hiển thị là **Public**.

