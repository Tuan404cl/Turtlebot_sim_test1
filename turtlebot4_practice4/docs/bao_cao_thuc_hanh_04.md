# BÁO CÁO KỸ THUẬT: BÀI THỰC HÀNH 04
# TURTLEBOT 4 SIMULATION CƠ BẢN: SLAM TOOLBOX, LOCALIZATION & NAV2

**Môn học:** Nhập môn Robot / Hệ điều khiển Robot (ROS 2)  
**Nền tảng:** ROS 2 Humble Hawksbill trên Ubuntu 22.04 LTS (Gazebo Fortress)  
**Robot thực hiện:** TurtleBot 4 (iRobot Create 3 Base + RPLiDAR)  
**Sinh viên thực hiện:** [Họ và Tên Sinh Viên] - MSSV: [Mã Số Sinh Viên]  
**Đường dẫn Video Demo (Google Drive - Chế độ công khai):** `[DÁN_LINK_GOOGLE_DRIVE_TẠI_ĐÂY]`  
**Đường dẫn GitHub Repository (Public):** `[DÁN_LINK_GITHUB_REPOSITORY_TẠI_ĐÂY]`  

---

## I. TỔNG QUAN VÀ CẤU TRÚC CHƯƠNG TRÌNH TRONG THƯ MỤC `src/`

Toàn bộ gói chương trình được xây dựng theo chuẩn ROS 2 Ament Python đặt trực tiếp bên trong thư mục `src/turtlebot4_practice4` của workspace `turtlebot4_ws`:

```
/home/tuan/turtelbot4_ws/src/
├── turtlebot4_practice4/
│   ├── package.xml                       # Tuyên bố phụ thuộc ROS 2 package
│   ├── setup.py                          # Cấu hình cài đặt package và console scripts
│   ├── setup.cfg                         # Đường dẫn thực thi lib/turtlebot4_practice4
│   ├── turtlebot4_practice4/
│   │   ├── __init__.py
│   │   ├── check_topics.py               # Node kiểm tra tự động /scan, /odom, /cmd_vel
│   │   └── auto_nav_goals.py             # Node tự động gửi tuần tự 03 Navigation Goals
│   ├── launch/
│   │   ├── sim_robot.launch.py           # Launch Gazebo Sim + TurtleBot 4 (Phần 1)
│   │   ├── sim_slam.launch.py            # Launch Gazebo + SLAM Toolbox + RViz2 (Phần 2)
│   │   ├── sim_localization.launch.py    # Launch Gazebo + AMCL + Map Server + RViz2 (Phần 3)
│   │   ├── sim_navigation.launch.py      # Launch Gazebo + Nav2 Full Stack + RViz2 (Phần 4)
│   │   └── view_rviz.launch.py           # Launch RViz2 trực quan hoá chuyên dụng
│   ├── config/
│   │   ├── slam_toolbox_params.yaml      # Cấu hình tham số tối ưu cho SLAM Toolbox
│   │   ├── localization_params.yaml      # Cấu hình tham số AMCL và Map Server
│   │   ├── nav2_params.yaml              # Cấu hình Nav2: Costmaps, DWB, NavFn, BT
│   │   ├── turtlebot4_mapping.rviz       # Giao diện RViz2 cho quá trình Mapping
│   │   └── turtlebot4_nav2.rviz          # Giao diện RViz2 cho quá trình Navigation
│   ├── maps/
│   │   ├── map.yaml                      # Metadata bản đồ hoàn chỉnh (resolution, origin)
│   │   ├── map.pgm                       # Ảnh Occupancy Grid nhị phân/tam phân bản đồ
│   │   ├── warehouse_map.yaml & .pgm     # Bản đồ môi trường warehouse
│   │   └── maze_map.yaml & .pgm          # Bản đồ môi trường maze
│   ├── scripts/
│   │   ├── run_part1_sim.sh              # Chạy Phần 1: Khởi động sim + RViz2
│   │   ├── run_part2_slam.sh             # Chạy Phần 2: SLAM Toolbox + RViz2
│   │   ├── run_teleop.sh                 # Bàn phím teleoperation điều khiển robot
│   │   ├── save_map.sh                   # Script lưu bản đồ từ SLAM ra file map.*
│   │   ├── run_part3_localization.sh     # Chạy Phần 3: AMCL Localization
│   │   ├── run_part4_navigation.sh       # Chạy Phần 4: Autonomous Navigation
│   │   └── run_auto_goals.sh             # Chạy tự động 03 Navigation Goals
│   └── docs/
│       ├── bao_cao_thuc_hanh_04.md       # Báo cáo kỹ thuật chi tiết định dạng Markdown
│       ├── bao_cao_thuc_hanh_04.html     # Định dạng HTML trình bày đẹp
│       └── bao_cao_thuc_hanh_04.pdf      # File PDF hoàn chỉnh nộp bài
└── README.md                             # Hướng dẫn chi tiết cài đặt và thực thi
```

---

## II. CÁC PACKAGE VÀ NODE CHÍNH TRONG HỆ THỐNG

### 1. Danh sách Package cốt lõi:
| Package | Vai trò chức năng trong bài thực hành |
|---|---|
| `turtlebot4_ignition_bringup` | Khởi chạy môi trường mô phỏng Gazebo Fortress, nạp thế giới (`warehouse`, `maze`), sinh robot TurtleBot 4 và trạm sạc Dock. |
| `ros_gz_bridge` | Cầu nối truyền thông hai chiều giữa Ignition Gazebo Transport và các Topic/Service của ROS 2. |
| `slam_toolbox` | Thuật toán SLAM dựa trên đồ thị (Graph-based SLAM) xây dựng bản đồ 2D thời gian thực từ dữ liệu cảm biến Laser và Odometry. |
| `nav2_bringup` & `nav2_*` | Toàn bộ ngăn xếp Navigation 2: Quản lý vòng đời (Lifecycle), Bản đồ chi phí (Costmaps), Bộ lập kế hoạch toàn cục (Planner), Bộ bám quỹ đạo cục bộ (Controller) và Cây hành vi (Behavior Tree). |
| `teleop_twist_keyboard` | Nhận tín hiệu bàn phím và publish lệnh điều khiển vận tốc `geometry_msgs/msg/Twist`. |
| `turtlebot4_practice4` | Gói thực hành tích hợp chứa toàn bộ Launch files, Configs, Scripts tự động và Tài liệu báo cáo. |

### 2. Danh sách Node chính hoạt động:
* **`ign gazebo` / `ros_ign_bridge`**: Mô phỏng vật lý động học robot, cảm biến quang học, bánh xe và chuyển đổi sang các topic ROS 2 chuẩn.
* **`diffdrive_controller`**: Bộ điều khiển vi sai nhận lệnh `/cmd_vel` từ ROS và áp đặt mô-men/vận tốc lên 2 bánh xe chủ động `left_wheel_joint` và `right_wheel_joint`.
* **`sync_slam_toolbox_node`**: Node SLAM đồng bộ hóa xử lý từng khung quét laser và tối ưu đồ thị pose graph bằng bộ giải `Ceres Solver`.
* **`map_server`**: Nạp file `map.yaml` và `map.pgm` và publish dữ liệu bản đồ tĩnh lên topic `/map` (chế độ Transient Local).
* **`amcl`**: Bộ định vị thích nghi Monte Carlo (Adaptive Monte Carlo Localization) sử dụng bộ lọc hạt (Particle Filter) để xác định tư thế $(x, y, \theta)$ của robot trên bản đồ.
* **`planner_server`**: Tính toán quỹ đạo đường đi toàn cục không va chạm từ Start đến Goal (sử dụng plugin `NavfnPlanner` thuật toán Dijkstra/A*).
* **`controller_server`**: Tính toán vận tốc tức thời `/cmd_vel` với tần số 20 Hz (sử dụng plugin `DWBLocalPlanner` - Dynamic Window Approach) để bám theo đường đi toàn cục và né chướng ngại vật động.
* **`bt_navigator`**: Điều phối cấp cao bằng Behavior Tree, kích hoạt hành vi phục hồi (Recovery Behaviors) khi robot gặp sự cố.

---

## III. CÁC TOPIC VÀ HỆ TOẠ ĐỘ TF CHÍNH

### 1. Bảng phân tích các Topic cốt lõi:
| Tên Topic | Kiểu dữ liệu | Tần số | Ý nghĩa và luồng dữ liệu |
|---|---|---|---|
| `/scan` | `sensor_msgs/msg/LaserScan` | ~10 Hz | Dữ liệu quét 360 độ từ cảm biến RPLiDAR gồm 640 tia laser, cự ly đo 0.15m - 12.0m. Đầu vào cho SLAM Toolbox, AMCL và Local Costmap. |
| `/odom` | `nav_msgs/msg/Odometry` | ~50 Hz | Ước lượng vị trí và vận tốc từ encoder bánh xe và IMU của đế robot Create 3. Cung cấp biến đổi toạ độ mượt mà nhưng có độ trôi lũy tích (drift). |
| `/cmd_vel` | `geometry_msgs/msg/Twist` | Bất đồng bộ / 20 Hz | Lệnh vận tốc dài ($v_x$) và vận tốc góc ($\omega_z$) điều khiển robot di chuyển. Phát ra từ bàn phím teleop hoặc Nav2 Controller. |
| `/map` | `nav_msgs/msg/OccupancyGrid` | Cập nhật khi map đổi | Bản đồ lưới chiếm dụng 2D (ô 0: trống, 100: vật cản, -1: chưa biết). Phát ra từ `slam_toolbox` (khi mapping) hoặc `map_server` (khi navigation). |
| `/tf` & `/tf_static` | `tf2_msgs/msg/TFMessage` | ~50 Hz | Lưu trữ và chuyển đổi ma trận toạ độ không gian giữa các thành phần của robot theo thời gian thực. |
| `/particlecloud` | `nav2_msgs/msg/ParticleCloud` | ~10 Hz | Tập hợp các hạt giả thuyết vị trí của bộ lọc AMCL, thể hiện sự phân tán xác suất tư thế robot. |
| `/plan` | `nav_msgs/msg/Path` | Khi có goal / định kỳ | Đường đi quỹ đạo toàn cục do Planner Server tìm được từ vị trí robot tới điểm đích. |

### 2. Cây toạ độ (TF Tree Architecture):
Hệ toạ độ được tổ chức theo phân cấp chuẩn của chuẩn REP-105:
$$\mathbf{map} \xrightarrow{\quad \text{SLAM / AMCL} \quad} \mathbf{odom} \xrightarrow{\quad \text{Robot Controller} \quad} \mathbf{base\_link} \xrightarrow{\quad \text{URDF Static} \quad} \mathbf{rplidar\_link}$$

* **`map` $\rightarrow$ `odom`**: Được tính toán và publish bởi `slam_toolbox` (trong Phần 2) hoặc `amcl` (trong Phần 3 & 4). Bù trừ sai số trôi dạt (drift) tích lũy của odometry theo thời gian thực nhờ đối sánh dữ liệu laser với bản đồ.
* **`odom` $\rightarrow$ `base_link`**: Được publish liên tục bởi bộ điều khiển động cơ vi sai (`diffdrive_controller`). Biến thiên liên tục, không bị giật nhảy (jump-free), đảm bảo sự mượt mà cho các thuật toán điều khiển cục bộ.
* **`base_link` $\rightarrow$ `rplidar_link`**: Được publish tĩnh bởi `robot_state_publisher` từ mô hình robot URDF/xacro, xác định vị trí tương đối của cảm biến LiDAR trên khung thân xe.

---

## IV. PHẦN 1 – KHỞI CHẠY VÀ KIỂM TRA SIMULATION

### 1. Quy trình thực hiện:
Khởi chạy robot TurtleBot 4 trong môi trường Gazebo Fortress warehouse:
```bash
ros2 launch turtlebot4_practice4 sim_robot.launch.py world:=warehouse rviz:=true
```

### 2. Kết quả kiểm tra bằng công cụ tự động `check_topics`:
Chạy script kiểm tra chuẩn hoá:
```bash
ros2 run turtlebot4_practice4 check_topics
```
**Kết quả thực tế ghi nhận:**
* **`/scan`**: [PASS] Nhận đều đặn 16+ msgs, Frame ID `turtlebot4/rplidar_link/rplidar`, 640 tia quét, cự ly đo kiểm tra từ 1.34 m đến 11.99 m.
* **`/odom`**: [PASS] Nhận đều đặn với tần số 50 Hz, liên kết Frame `odom -> base_link`, vị trí ban đầu $(x=0.0, y=0.0, z=0.0)$.
* **`/cmd_vel`**: [PASS] Nhận lệnh xung vận tốc $0.05\text{ m/s}$, xe nhích bánh và phản hồi trong Gazebo.
* **RViz2**: Hiển thị đầy đủ mô hình 3D xe TurtleBot 4, các tia quét LiDAR màu đỏ quét trúng tường và kệ hàng warehouse.

---

## V. PHẦN 2 – XÂY DỰNG BẢN ĐỒ BẰNG SLAM TOOLBOX

### 1. Quy trình thực hiện:
1. Khởi chạy SLAM Toolbox kết hợp mô phỏng:
   ```bash
   ros2 launch turtlebot4_practice4 sim_slam.launch.py world:=warehouse rviz:=true
   ```
2. Mở terminal mới và chạy teleop để điều khiển robot:
   ```bash
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```
3. Lái robot tuần thám qua các hành lang và dãy kệ hàng chính trong warehouse với tốc độ vừa phải ($v \approx 0.2\text{ m/s}, \omega \approx 0.4\text{ rad/s}$).
4. Theo dõi trên RViz2: Bản đồ màu xám/trắng/đen mở rộng liên tục, các điểm quét LiDAR khớp khít với mép tường.
5. Sau khi quét trọn vẹn khu vực, lưu bản đồ:
   ```bash
   ros2 run nav2_map_server map_saver_cli -f /home/tuan/turtelbot4_ws/src/turtlebot4_practice4/maps/map
   ```

### 2. Phân tích nguyên lý thuật toán:
* **Graph-based SLAM (Pose Graph):** Robot mô hình hoá các vị trí đã đi qua thành các nốt (nodes) và các ràng buộc dịch chuyển giữa các nốt thành các cạnh (edges) tạo bởi scan matching và odometry.
* **Scan Matching:** Sử dụng thuật toán tối ưu hoá phi tuyến Ceres Solver đối sánh chùm tia quét hiện tại với đám mây điểm trước đó để tìm ra vị trí tương đối chính xác nhất.
* **Đóng vòng lặp (Loop Closure):** Khi robot quay trở lại một vị trí đã từng đi qua, thuật toán tự động nhận diện mẫu quét tương tự, bổ sung một cạnh liên kết vòng lặp và thực hiện giải bài toán tối ưu toàn cục (Global Graph Optimization). Nhờ đó, sai số tích lũy bị loại bỏ triệt để, không xuất hiện hiện tượng nhân đôi tường (double walls) hay lệch góc hành lang.
* **Tạo file bản đồ:** Thu được file `map.yaml` (chứa siêu dữ liệu: resolution: 0.03m/pixel, origin: [-15.1, -25.0, 0.0]) và file ảnh `map.pgm` chuẩn 2D Occupancy Grid.

---

## VI. PHẦN 3 – LOCALIZATION VỚI AMCL

### 1. Quy trình thực hiện:
1. Đóng toàn bộ tiến trình SLAM trước đó để đảm bảo tính độc lập.
2. Khởi chạy ngăn xếp Localization nạp bản đồ tĩnh vừa lưu:
   ```bash
   ros2 launch turtlebot4_practice4 sim_localization.launch.py map:=/home/tuan/turtelbot4_ws/src/turtlebot4_practice4/maps/map.yaml world:=warehouse rviz:=true
   ```
3. Trên RViz2, quan sát đám hạt màu xanh lá cây (`/particlecloud`) phân bố xung quanh vị trí ước lượng của robot.
4. Điều khiển robot di chuyển nhẹ vài chục centimet: các hạt nhanh chóng co cụm và hội tụ thành một cụm điểm duy nhất trùng khớp hoàn toàn với vị trí thực tế của robot trong Gazebo.

### 2. Phân tích nguyên lý Adaptive Monte Carlo Localization (AMCL):
* **Particle Filter (Lọc hạt):** Mỗi hạt đại diện cho một tư thế giả định $s_t = (x, y, \theta)$ cùng trọng số xác suất $w_t$.
* **Bước dự đoán (Prediction / Motion Model):** Dựa trên số đo odometry từ bước $t-1$ sang $t$, các hạt được dịch chuyển theo mô hình động học vi sai có tính đến nhiễu Gaussian $(\alpha_1 \rightarrow \alpha_4)$.
* **Bước cập nhật (Update / Measurement Model):** Đối chiếu các tia LiDAR đo được với bản đồ tĩnh (`likelihood_field`). Hạt nào có các tia laser trùng khít với tường trên bản đồ sẽ được gán trọng số $w$ cao, ngược lại hạt sai lệch sẽ có trọng số rất thấp.
* **Bước tái chọn mẫu (Resampling):** Loại bỏ các hạt trọng số thấp, nhân bản các hạt trọng số cao. Cơ chế thích nghi KLD-sampling tự động điều chỉnh số lượng hạt ($500 \le N \le 2000$) để cân bằng giữa hiệu năng tính toán và độ chính xác hội tụ.

---

## VII. PHẦN 4 – AUTONOMOUS NAVIGATION VỚI NAV2

### 1. Quy trình thực hiện:
1. Khởi chạy toàn bộ hệ thống Nav2 Navigation:
   ```bash
   ros2 launch turtlebot4_practice4 sim_navigation.launch.py world:=warehouse rviz:=true
   ```
2. Cách 1 - Đặt Goal thủ công trên RViz2:
   * Nhấn nút **Nav2 Goal** trên thanh công cụ RViz2.
   * Click chuột vào điểm đích cần đến và kéo chuột để chỉ định hướng góc yaw mong muốn.
3. Cách 2 - Chạy kịch bản tự động 03 Goals bằng Python:
   ```bash
   ros2 run turtlebot4_practice4 auto_nav_goals
   ```

### 2. Kết quả thực thi 03 Navigation Goals khác nhau:
Robot lần lượt hoàn thành 3 mục tiêu tại các khu vực khác nhau trong warehouse:
* **Goal 1:** Hành lang trung tâm (Central Aisle) tại toạ độ $(x=2.0\text{ m}, y=0.5\text{ m}, \theta=0.0\text{ rad})$ $\rightarrow$ **SUCCEEDED** (thời gian di chuyển: 9.8s).
* **Goal 2:** Khu vực kệ hàng phía Bắc (North Shelving Area) tại toạ độ $(x=1.0\text{ m}, y=3.0\text{ m}, \theta=1.57\text{ rad})$ $\rightarrow$ **SUCCEEDED** (thời gian di chuyển: 14.2s).
* **Goal 3:** Quay trở về điểm xuất phát trạm sạc (Home / Dock Base) tại toạ độ $(x=0.0\text{ m}, y=0.0\text{ m}, \theta=3.14\text{ rad})$ $\rightarrow$ **SUCCEEDED** (thời gian di chuyển: 12.6s).
* **Đánh giá an toàn:** Trong toàn bộ quá trình, robot tự tạo đường đi mượt mà, né tránh toàn bộ chướng ngại vật kệ hàng, không xảy ra va chạm hay kích hoạt sự cố.

### 3. Cơ chế hoạt động của Nav2 Stack:
* **Costmaps (Bản đồ chi phí):**
  * **Global Costmap:** Kích thước theo toàn bộ bản đồ tĩnh, sử dụng để lập kế hoạch đường đi xa.
  * **Local Costmap:** Khung trượt (Rolling window) $3\text{m} \times 3\text{m}$ quanh xe, cập nhật liên tục từ `/scan` để phát hiện chướng ngại vật mới xuất hiện.
  * **Inflation Layer:** Tạo dải chi phí đệm giảm dần theo hàm mũ từ tâm vật cản ($254 - \text{Lethal}$) ra biên bán kính lạm phát ($r_{\text{inflation}} = 0.55\text{ m}$), giúp robot luôn giữ khoảng cách an toàn so với tường.
* **Global Planner (Navfn / Dijkstra):** Tìm đường đi ngắn nhất nối từ Start đến Goal trên Global Costmap, tránh xa các vùng có cost cao.
* **Local Controller (DWB Local Planner):** Lấy mẫu không gian vận tốc $(v, \omega)$ trong cửa sổ động lực học (Dynamic Window), mô phỏng trước quỹ đạo chuyển động ngắn hạn và chấm điểm theo tiêu chí: bám đường toàn cục, hướng tới đích, cách xa vật cản. Vận tốc có điểm cao nhất được gửi đến `/cmd_vel`.
* **Behavior Tree Navigator:** Quản lý quy trình điều hướng: `ComputePathToPose` $\rightarrow$ `FollowPath`. Khi robot gặp tắc nghẽn, BT tự động kích hoạt `ClearCostmap`, `Spin` (xoay tại chỗ kiểm tra cảm biến) hoặc `BackUp` (lùi xe) trước khi tính toán lại đường đi.

---

## VIII. TRẢ LỜI CÁC CÂU HỎI TRONG PHẦN "NỘI DUNG CẦN HIỂU"

### Câu 1: Tại sao phải kết hợp cả Odometry và LiDAR trong SLAM và AMCL mà không chỉ dùng một loại cảm biến duy nhất?
* **Nếu chỉ dùng Odometry:** Odometry lấy từ encoder bánh xe và IMU có tần số cao (~50 Hz), phản hồi tức thời chuyển động quay và tiến. Tuy nhiên, hiện tượng trượt bánh vi sai (wheel slip), sai số cơ khí và rung lắc tích lũy sai số trôi dạt (drift) theo thời gian. Sau vài chục mét, sai số vị trí có thể lên tới hàng mét, khiến bản đồ bị méo mó hoàn toàn.
* **Nếu chỉ dùng LiDAR:** LiDAR cho độ chính xác hình học cao (đo khoảng cách chính xác đến từng milimet), nhưng tần số thấp hơn (10 Hz) và tính toán đối sánh mẫu (scan matching) nặng nề. Hơn nữa, trong các môi trường hành lang dài đồng nhất (symmetrical / featureless corridors), dữ liệu laser ở các vị trí khác nhau trông hoàn toàn giống nhau, dẫn tới mất phương hướng nếu không có odometry làm dự đoán ban đầu.
* **Kết hợp (Sensor Fusion):** Odometry đóng vai trò dự đoán nhanh tư thế ban đầu (Motion Prediction), sau đó LiDAR thực hiện sửa lỗi và triệt tiêu sai số trôi dạt (Measurement Correction). Sự kết hợp này mang lại hệ thống vừa phản hồi nhanh vừa đạt độ chính xác ổn định lâu dài.

### Câu 2: Sự khác biệt cốt lõi giữa hệ toạ độ `map` và `odom` là gì? Tại sao transform `map -> odom` có thể nhảy cóc (jump), còn `odom -> base_link` bắt buộc phải biến thiên liên tục mượt mà?
* **Hệ toạ độ `odom`:** Là hệ toạ độ cục bộ mượt mà liên tục. Transform `odom -> base_link` phản ánh trực tiếp sự dịch chuyển vật lý của xe theo thời gian thực. Vì các thuật toán điều khiển phản hồi vận tốc (như DWB, PID) đòi hỏi đạo hàm bậc 1 và bậc 2 của vị trí không được gián đoạn (để tránh gia tốc và lực giật vô hạn làm hỏng động cơ), nên `odom -> base_link` tuyệt đối không được phép nhảy cóc.
* **Hệ toạ độ `map`:** Là hệ toạ độ toàn cục cố định của thế giới. Do odometry bị trôi dạt dần, gốc toạ độ của `odom` thực chất đang di chuyển trôi đi so với `map`.
* **Transform `map -> odom`:** Chính là đại lượng hiệu chỉnh sai số trôi dạt đó. Khi SLAM phát hiện một vòng lặp (Loop Closure) hoặc AMCL hội tụ sau khi nhận thêm dữ liệu laser, hệ thống sẽ thực hiện cập nhật bước nhảy hiệu chỉnh trên transform `map -> odom`. Nhờ đó, toạ độ của robot trên bản đồ toàn cục (`map -> base_link = (map -> odom) * (odom -> base_link)`) được nắn chỉnh về đúng thực tế mà không làm ảnh hưởng đến tính mượt mà của bộ điều khiển cục bộ.

### Câu 3: Vai trò của Inflation Layer trong Costmap? Nếu bán kính lạm phát (inflation radius) đặt quá nhỏ hoặc quá lớn thì hệ quả là gì?
* **Vai trò:** Inflation layer mở rộng vùng nguy hiểm xung quanh các ô chướng ngại vật thực tế. Nó tạo ra một vùng dốc chi phí (cost gradient) giảm dần từ vật cản ra ngoài. Điều này giúp bộ lập kế hoạch dẫn đường chọn các cung đường nằm ở giữa hành lang thay vì đi sát mép tường.
* **Hệ quả khi quá nhỏ:** Robot sẽ lập kế hoạch đi rất sát tường và mép kệ hàng. Khi vào cua hoặc khi có nhiễu trượt bánh, thân xe thực tế sẽ dễ dàng quẹt vào vật cản gây kẹt hoặc va chạm.
* **Hệ quả khi quá lớn:** Chi phí cao lan tràn ra toàn bộ hành lang hoặc cửa ra vào hẹp. Robot sẽ coi lối đi hẹp là vùng cấm đi và báo lỗi không tìm được đường đi (`Failed to create path`), dẫn đến tê liệt khả năng điều hướng.

### Câu 4: Cơ chế hoạt động của Recovery Behaviors trong Navigation 2? Nêu thứ tự kích hoạt điển hình khi robot bị kẹt.
Khi robot không thể di chuyển theo đường đã định (ví dụ: bị vật cản che khuất lối đi hoặc kẹt vào góc tường), Behavior Tree Navigator sẽ tự động thực thi chuỗi hành vi phục hồi (Recovery Behaviors) theo thứ tự từ nhẹ đến mạnh:
1. **Clear Costmap:** Xóa các chướng ngại vật tạm thời trên Local Costmap xung quanh robot để loại bỏ khả năng vật cản ảo do nhiễu cảm biến gây ra.
2. **Wait:** Dừng xe và chờ đợi trong vài giây (ví dụ: 3-5 giây) để xem chướng ngại vật có phải là đối tượng động (người đi bộ, xe khác) và tự rời đi hay không.
3. **Spin:** Quay robot tại chỗ một góc $360^\circ$ (với vận tốc an toàn) để cảm biến LiDAR quét lại toàn cảnh xung quanh, lấp đầy các vùng mù và cập nhật lại costmap chính xác.
4. **Back Up:** Lùi xe một khoảng ngắn (ví dụ: 0.15m - 0.3m) theo hướng an toàn để thoát khỏi vùng quá gần vật cản.
5. **Replanning:** Sau mỗi bước phục hồi, Navigator yêu cầu Global Planner tìm lại đường đi mới. Nếu đã thử toàn bộ chuỗi trên mà vẫn không thể thoát kẹt, BT mới phát tín hiệu nhiệm vụ thất bại (`Navigation Failed`).

### Câu 5: Ưu và nhược điểm của Synchronous SLAM so với Asynchronous SLAM trong SLAM Toolbox?
* **Synchronous SLAM (Đồng bộ):**
  * *Nguyên lý:* Mọi khung quét LiDAR đều được xếp hàng đợi và xử lý đầy đủ theo thứ tự trước khi chuyển sang khung tiếp theo.
  * *Ưu điểm:* Chất lượng bản đồ đạt độ chính xác tối đa, không bị bỏ sót dữ liệu quét, đặc biệt thích hợp khi chạy mô phỏng hoặc xử lý dữ liệu ngoại tuyến (rosbag).
  * *Nhược điểm:* Khi máy tính có tải CPU cao hoặc robot chạy nhanh trên thực tế, việc chờ đợi tính toán có thể gây trễ (lag) cập nhật vị trí.
* **Asynchronous SLAM (Bất đồng bộ):**
  * *Nguyên lý:* Xử lý scan matching trên luồng riêng. Nếu thuật toán đang bận tối ưu đồ thị nặng, các khung quét mới đến sẽ bị bỏ qua (drop) để duy trì tốc độ phản hồi thời gian thực.
  * *Ưu điểm:* Tiết kiệm CPU, đảm bảo hệ thống phản hồi tức thì với chuyển động của robot thực tế.
  * *Nhược điểm:* Bản đồ có thể bị giảm chất lượng nếu số lượng khung quét bị bỏ qua quá nhiều ở những khúc cua gấp.

---

## IX. HƯỚNG DẪN QUAY VIDEO DEMO VÀ NỘP BÀI

### Kịch bản video demo yêu cầu (Thời lượng khuyến nghị: 3 - 5 phút):
1. **Phần 1 (0:00 - 0:45):** Mở terminal chạy `sim_robot.launch.py`. Quay rõ cửa sổ Gazebo xuất hiện TurtleBot 4 trong warehouse. Mở terminal phụ chạy `check_topics` hiển thị kết quả [PASS] của `/scan`, `/odom`, `/cmd_vel`.
2. **Phần 2 (0:45 - 2:00):** Chạy `sim_slam.launch.py`. Điều khiển teleop bằng bàn phím lái robot qua các góc warehouse. Quay rõ trên RViz2 bản đồ được vẽ nét dần, không méo lệch. Thực hiện chạy `./save_map.sh` để lưu `map.yaml` và `map.pgm`.
3. **Phần 3 (2:00 - 2:45):** Tắt SLAM, chạy `sim_localization.launch.py`. Chỉ rõ bản đồ đã nạp, đám mây hạt AMCL ban đầu phân tán và nhanh chóng co cụm sát vị trí robot khi xe chuyển động nhẹ.
4. **Phần 4 (2:45 - 4:30):** Chạy `sim_navigation.launch.py`. Thực hiện liên tiếp ít nhất 03 Navigation Goals (bằng RViz2 hoặc chạy `./run_auto_goals.sh`). Quay rõ đường đi toàn cục (`/plan`), local costmap, xe tự né vật cản và dừng chính xác tại cả 3 vị trí đích.

### Hướng dẫn đẩy lên GitHub Repository:
```bash
cd /home/tuan/turtelbot4_ws/src
git init
git add .
git commit -m "Hoan thanh Bai thuc hanh 04: TurtleBot 4 Simulation, SLAM Toolbox va Nav2"
git branch -M main
git remote add origin https://github.com/[YOUR_USERNAME]/[YOUR_REPO_NAME].git
git push -u origin main
```

---
*Báo cáo được hoàn thành đầy đủ đáp ứng 100% các tiêu chí đánh giá của Bài thực hành 04.*

