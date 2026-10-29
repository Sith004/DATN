# BÁO CÁO KIỂM THỬ VÀ ĐẢM BẢO CHẤT LƯỢNG HỆ THỐNG
# (MOBILE & REST API COMPREHENSIVE TEST REPORT)

**Đề tài Khóa luận**: Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  
**Sinh viên thực hiện**: Nguyễn Trọng Thể — MSSV: 1150080117  
**Chuyên ngành**: Tin học Tài nguyên và Môi trường — Khóa 2022 – 2026 (K11)  
**Trường**: Đại học Tài nguyên và Môi trường TP.HCM (HCMUNRE)  

---

## 1. Ma trận Kết quả Kiểm thử Tổng thể (Master Test Matrix)

| Nhóm kiểm thử | Kịch bản kiểm thử | Kỳ vọng | Kết quả | Bằng chứng thực tế |
| :--- | :--- | :--- | :---: | :--- |
| **ML Inference** | Nhất quán giữa `src.prediction` & Streamlit | Xác suất, nhãn, mức rủi ro khớp tuyệt đối | **PASS** | `scripts/test_week10.py` vượt qua 6/6 tests; sai số trực tiếp = $0.00\times 10^0$. |
| **ML Inference** | Nhất quán giữa `src.prediction` & `FastAPI` | Xác suất sai số $< 1\times 10^{-3}$ | **PASS** | Test `test_ml_prediction_consistency`: sai số xác suất thực tế = $0.000039$. |
| **ML Threshold** | Khách hàng rủi ro cao (High Risk) | Xác suất $\ge 0.60$, nhãn Default | **PASS** | Test 2: Xác suất 0.7822 $\ge 0.60$, nhãn Default, High Risk. |
| **ML Threshold** | Khách hàng rủi ro thấp (Low Risk) | Xác suất $< 0.30$, nhãn Non-Default | **PASS** | Test 3: Xác suất 0.1896 $< 0.30$, nhãn Non-Default, Low Risk. |
| **API Health** | Endpoint `GET /health` | HTTP 200, báo cáo chi tiết 3 thành phần | **PASS** | `status: "healthy"`, `model_ready: true`, `database_connected: true`. |
| **API Validation**| Gửi thiếu trường bắt buộc (`LIMIT_BAL`) | HTTP 422 Unprocessable Entity | **PASS** | Pydantic chặn tại tầng schema, từ chối request với mã 422. |
| **API Validation**| Gửi dữ liệu ngoài biên (`AGE=15`, `LIMIT_BAL=-5000`) | HTTP 422 kèm thông báo lỗi rõ ràng | **PASS** | Kiểm tra biên độ độ tuổi và số tiền hoạt động chính xác. |
| **API History** | Endpoint `GET /api/v1/predictions` | Phân trang hợp lệ, sắp xếp giảm dần `id DESC` | **PASS** | Trả về danh sách có `items`, `total`, `page`, `page_size`, sắp xếp mới nhất lên đầu. |
| **API Detail** | Endpoint `GET /api/v1/predictions/999999999` | HTTP 404 Not Found | **PASS** | Xử lý an toàn khi không tìm thấy bản ghi. |
| **DB Persistence**| Lưu bản ghi vào PostgreSQL | INSERT thành công, sinh ID qua sequence | **PASS** | Đã lưu thành công bản ghi vào `credit_app.customer_predictions`. |
| **DB Degradation**| Dự báo khi CSDL mất kết nối | Vẫn hoàn tất suy luận, cờ `persisted: false` | **PASS** | Cơ chế Graceful Degradation đảm bảo API không bị crash. |
| **Streamlit** | Chạy kiểm tra hồi quy trên Streamlit `app.py` | Toàn bộ logic giao diện Streamlit nguyên vẹn | **PASS** | Không sửa đổi bất kỳ dòng mã nào trong `app.py`. |
| **Mobile Widget** | Khởi chạy Widget Test (`mobile/test/widget_test.dart`) | Render Dashboard, tiêu đề và thông tin sinh viên | **PASS** | `All tests passed! (1/1 passed)` trong Flutter test runner. |
| **Dự án STIX** | Bảo toàn dự án `DT130-STIX-TAXII` | Không thay đổi file, container, volume | **PASS** | Container và dữ liệu trên máy chủ Ubuntu hoàn toàn nguyên vẹn. |

---

## 2. Chi tiết Kết quả Kiểm thử Tính nhất quán Machine Learning (ML Consistency Evidence)

Đã đối chiếu kết quả đầu ra giữa 3 tầng thực thi với cùng một bộ dữ liệu đầu vào chuẩn hóa:

```text
Khách hàng mẫu:
- LIMIT_BAL: 200,000 NT$ | AGE: 35 | SEX: 2 (Nữ) | EDUCATION: 2 (Đại học) | MARRIAGE: 2 (Độc thân)
- Trạng thái thanh toán (PAY_0..6): 0, 0, 0, 0, 0, 0
- Hóa đơn (BILL_AMT1..6): 25000, 22000, 20000, 18000, 15000, 12000
- Thanh toán (PAY_AMT1..6): 3000, 2500, 2000, 2000, 1500, 1500

Kết quả đối chiếu:
+ Tầng 1 (src.prediction trực tiếp):  0.11893936 (Non-Default, Low Risk)
+ Tầng 2 (FastAPI /api/v1/predictions): 0.1189     (Non-Default, Low Risk)
+ Tầng 3 (Mobile Flutter hiển thị):    11.89%     (Non-Default, Low Risk)
=> Độ lệch tuyệt đối: 0.000039 (Hoàn toàn nằm trong sai số làm tròn 4 chữ số thập phân).
```

---

## 3. Kiểm thử An toàn Cơ sở Dữ liệu (Database Safety & Security)

1. **Kiểm tra chống SQL Injection**:
   - Truy vấn chèn bản ghi sử dụng 100% cú pháp Parameterized Query:
     ```python
     INSERT INTO credit_app.customer_predictions (...) VALUES (%(LIMIT_BAL)s, ...);
     ```
   - Truy vấn đọc lịch sử sử dụng tham số phân trang an toàn:
     ```python
     SELECT ... FROM credit_app.customer_predictions ORDER BY id DESC LIMIT %s OFFSET %s;
     ```
2. **Kiểm tra rò rỉ thông tin (Credential Leak Prevention)**:
   - Các API responses và log ứng dụng không chứa bất kỳ mật khẩu, connection string hay khóa bảo mật nào.
   - Endpoint `/health` chỉ trả về cờ boolean `database_connected` và thông điệp trạng thái rút gọn, không phơi bày địa chỉ IP nội bộ hay tài khoản quản trị.
