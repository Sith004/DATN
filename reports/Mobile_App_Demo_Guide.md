# HƯỚNG DẪN TRIỂN KHAI VÀ THỰC HÀNH DEMO ỨNG DỤNG DI ĐỘNG
# (MOBILE APP & BACKEND DEMONSTRATION GUIDE)

**Đề tài Khóa luận**: Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  
**Sinh viên thực hiện**: Nguyễn Trọng Thể — MSSV: 1150080117  
**Chuyên ngành**: Tin học Tài nguyên và Môi trường — Khóa 2022 – 2026 (K11)  
**Trường**: Đại học Tài nguyên và Môi trường TP.HCM (HCMUNRE)  

---

## 1. Chuẩn bị Môi trường và Thiết bị Trước Buổi Demo

1. **Máy tính Windows**:
   - Địa chỉ IP Wi-Fi đã xác thực: `192.168.100.11`.
   - Đảm bảo môi trường ảo Python `.venv` đã sẵn sàng.
2. **Máy chủ Ubuntu (Chứa PostgreSQL)**:
   - Địa chỉ IP: `192.168.100.34`.
   - Docker container `credit-risk-postgres-db` đang chạy trên cổng nội bộ `5433`.
3. **Điện thoại Android Thật**:
   - Đã kết nối vào **cùng một mạng Wi-Fi** với máy tính (dải IP `192.168.100.x`).
   - Đã bật tùy chọn "Cài đặt từ nguồn không xác định" (đối với file APK debug).

---

## 2. Quy trình Khởi chạy Từng bước (Step-by-Step Execution)

### Bước 1: Khởi động Đường hầm SSH kết nối PostgreSQL

Nếu chưa mở đường hầm SSH kết nối CSDL từ Windows sang Ubuntu, mở PowerShell và chạy:
```powershell
# Chạy script tự động đã cấu hình sẵn trong dự án:
cd F:\DATN\project
.\Chay_Do_An.bat

# Hoặc mở riêng đường hầm SSH ngầm nếu chỉ demo Mobile App:
ssh -N -L 15432:127.0.0.1:5433 the@192.168.100.34
```
*Kiểm tra cổng 15432*: `Test-NetConnection 127.0.0.1 -Port 15432` phải trả về `TcpTestSucceeded : True`.

---

### Bước 2: Khởi động FastAPI REST Backend

Mở một cửa sổ PowerShell mới tại thư mục dự án và khởi chạy máy chủ backend:
```powershell
cd F:\DATN\project
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
> [!NOTE]
> Tham số `--host 0.0.0.0` là bắt buộc để máy chủ lắng nghe yêu cầu từ các thiết bị khác trong mạng LAN Wi-Fi (như điện thoại Android).

---

### Bước 3: Xác minh Trạng thái Sức khỏe Hệ thống (`/health`)

Mở trình duyệt trên máy tính hoặc điện thoại và truy cập:
👉 `http://192.168.100.11:8000/health`

Kết quả trả về chuẩn JSON:
```json
{
  "status": "healthy",
  "api_version": "1.0.0",
  "model_ready": true,
  "model_name": "XGBoost Tuned (Final Candidate)",
  "threshold": 0.60,
  "database_connected": true,
  "database_status_message": "Đã kết nối an toàn qua SSH Tunnel (Port 15432)"
}
```

---

### Bước 4: Cài đặt Ứng dụng Android (APK) lên Điện thoại

File APK debug đã được biên dịch sẵn tại:
📁 `F:\DATN\project\mobile\build\app\outputs\flutter-apk\app-debug.apk`

**Cách 1: Cài đặt trực tiếp qua ADB (Nếu cắm cáp USB có bật USB Debugging)**
```powershell
& "F:\App\Android\SDK\platform-tools\adb.exe" install -r F:\DATN\project\mobile\build\app\outputs\flutter-apk\app-debug.apk
```

**Cách 2: Cài đặt thủ công không cần cáp**
- Chép file `app-debug.apk` sang điện thoại (qua Zalo, Google Drive, hoặc chia sẻ tệp nội bộ).
- Trên điện thoại, nhấn vào file APK để tiến hành cài đặt.
- Tên ứng dụng hiển thị trên màn hình: **Credit Risk ML - Nguyễn Trọng Thể**.

---

### Bước 5: Cấu hình và Kiểm tra Kết nối trên Điện thoại

1. Mở ứng dụng **Credit Risk ML** trên điện thoại.
2. Tại màn hình chính (Dashboard), nhấn vào biểu tượng **Bánh răng Cài đặt** ở góc phải trên.
3. Kiểm tra trường **FastAPI Base URL**:
   - Giá trị mặc định là: `http://192.168.100.11:8000`.
   - Có thể chọn nhanh qua chip "Wi-Fi LAN (192.168.100.11:8000)".
4. Nhấn nút **Kiểm tra kết nối (Ping /health)**:
   - Hệ thống sẽ đo độ trễ (latency ping ~ 15-40ms) và hiển thị thông báo xanh: *Kết nối thành công! Mô hình XGBoost Tuned sẵn sàng, CSDL PostgreSQL đã kết nối*.
5. Nhấn **LƯU VÀ QUAY LẠI**.

---

### Bước 6: Thực hiện Dự báo Rủi ro Thử nghiệm

1. Tại Dashboard, nhấn **Dự báo Rủi ro Khách hàng**.
2. Thử nghiệm với các kịch bản mẫu qua thanh **Quick Presets**:
   * **Kịch bản 1: Khách hàng Bình thường (Normal Customer)**
     - Nhấn chip `Bình thường (Low Risk)`.
     - Nhấn `TIẾN HÀNH DỰ BÁO RỦI RO`.
     - Kết quả hiển thị: Xác suất ~ **11.89%**, Nhãn **✅ NON-DEFAULT**, Mức độ: **Low Risk**.
     - Thông báo cơ sở dữ liệu: `PostgreSQL: Đã lưu bản ghi #ID an toàn`.
   * **Kịch bản 2: Khách hàng Rủi ro cao (High Risk Customer)**
     - Quay lại và nhấn chip `Rủi ro cao (High Risk)`.
     - Nhấn `TIẾN HÀNH DỰ BÁO RỦI RO`.
     - Kết quả hiển thị: Xác suất ~ **78.22%**, Nhãn **⚠️ DEFAULT**, Mức độ: **High Risk** (màu đỏ nổi bật).
     - Xem bảng phân tích giải thích SHAP: Các biến `PAY_0`, `UTILIZATION_RATE` đẩy mức độ rủi ro lên.

---

### Bước 7: Kiểm tra Lịch sử Lưu trữ trên PostgreSQL

1. Nhấn nút **Xem Lịch sử** hoặc quay lại Dashboard chọn **Lịch sử Dự báo (PostgreSQL)**.
2. Danh sách hiển thị toàn bộ các lượt dự báo gần nhất sắp xếp từ mới đến cũ.
3. Kéo màn hình xuống để thực hiện **Pull-to-refresh** cập nhật dữ liệu trực tiếp từ PostgreSQL.
4. Xác nhận bản ghi vừa tạo hiển thị chính xác mã ID, thời gian thực hiện, xác suất, nhãn và hạn mức.

---

### Bước 8: Kiểm thử Cơ chế Chống sập (Graceful Degradation)

1. Tạm thời tắt đường hầm SSH hoặc ngắt kết nối mạng.
2. Thực hiện một lượt dự báo mới trên ứng dụng:
   - Quá trình suy luận Machine Learning của XGBoost **vẫn hoàn tất thành công**.
   - Ứng dụng hiển thị thông báo vàng: *Cơ sở dữ liệu: Mất kết nối CSDL - Quá trình dự báo Machine Learning vẫn hoàn tất*.
   - Ứng dụng **tuyệt đối không bị văng (crash)**, chứng minh tính ổn định cao trong môi trường thực tế.

---

### Bước 9: Đóng Dịch vụ Sau Buổi Demo

Khi kết thúc buổi bảo vệ/demo:
```powershell
# 1. Tắt tiến trình FastAPI: Nhấn Ctrl + C tại cửa sổ PowerShell đang chạy Uvicorn.
# 2. Đóng đường hầm SSH:
taskkill /F /IM ssh.exe
```
