# BÁO CÁO KIỂM TOÁN VÀ ĐÁNH GIÁ BAN ĐẦU HỆ THỐNG
# (INITIAL REPOSITORY & ENVIRONMENT AUDIT REPORT)

**Đề tài Khóa luận**: Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  
**Sinh viên thực hiện**: Nguyễn Trọng Thể — MSSV: 1150080117  
**Chuyên ngành**: Tin học Tài nguyên và Môi trường — Khóa 2022 – 2026 (K11)  
**Trường**: Đại học Tài nguyên và Môi trường TP.HCM (HCMUNRE)  
**Thời điểm kiểm toán**: 2026-10-29  
**Mục tiêu**: Khảo sát hiện trạng toàn diện hệ thống Machine Learning, cơ sở dữ liệu PostgreSQL, môi trường phát triển và toolchain di động trước khi triển khai ứng dụng Android Flutter và backend FastAPI.

---

## 1. Xác thực Thực tế Hệ thống Machine Learning Hiện hữu (Confirmed ML Facts)

| Hạng mục | Hiện trạng thực tế đã xác minh | Ghi chú kỹ thuật |
| :--- | :--- | :--- |
| **Vị trí Artifact mô hình** | `models/final_candidate_model.pkl` (1,028,618 bytes) | Mô hình XGBoost Tuned chính thức được lựa chọn tại Tuần 8. |
| **Fitted Transformer** | `models/robust_scaler.pkl` (1,399 bytes) | `RobustScaler` được fit độc quyền trên tập `X_train_fe` (22 đặc trưng số). |
| **Metadata mô hình** | `reports/week8_model_selection_meta.json` | Xác nhận threshold: 0.60; ROC-AUC: 0.7769; PR-AUC: 0.562; F1-score: 0.5409; 33 đặc trưng. |
| **Module suy luận hiện hữu** | `src/prediction.py` (319 dòng mã) | **ĐÃ HOÀN TOÀN ĐỘC LẬP VỚI STREAMLIT**. Không import Streamlit, có thể tái sử dụng trực tiếp bởi FastAPI. |
| **Hàm suy luận chính** | `predict_single_customer(raw_inputs: dict, model, scaler)` | Trả về: `probability` (float), `prediction_label` ("Default"/"Non-Default"), `risk_level` ("High Risk"/"Medium Risk"/"Low Risk"), `feature_vector`, `feature_vector_raw`. |
| **Số lượng biến đầu vào thô** | **23 thuộc tính bắt buộc** | `LIMIT_BAL`, `AGE`, `SEX`, `EDUCATION`, `MARRIAGE`, `PAY_0`, `PAY_2`..`6`, `BILL_AMT1`..`6`, `PAY_AMT1`..`6`. |
| **Quy tắc tiền xử lý danh mục** | `EDUCATION`: `{0, 5, 6} → 4` (Khác)<br>`MARRIAGE`: `{0} → 3` (Khác) | Khớp 100% với logic tiền xử lý tại `src/preprocessing.py`. |
| **10 đặc trưng kỹ thuật (FE)** | 1. `UTILIZATION_RATE_SEPT`<br>2. `MEAN_BILL_AMT`<br>3. `UTILIZATION_RATE_MEAN`<br>4. `PAY_RATIO_SEPT`<br>5. `PAY_RATIO_MEAN`<br>6. `MAX_PAY_DELAY`<br>7. `COUNT_LATE_PAYMENT`<br>8. `MEAN_PAY_AMT`<br>9. `BILL_TREND`<br>10. `PAY_TREND` | Tính toán tự động bởi `src/prediction.py::engineer_features_single()`, công thức khớp tuyệt đối với Tuần 5. |
| **Thứ tự 33 đặc trưng** | Khớp 100% với `FEATURE_ORDER` và file `data/processed/X_train_fe.csv`. | 22 cột số được chuẩn hóa qua `RobustScaler`; 11 cột phân loại/rời rạc được giữ nguyên (passthrough). |
| **Ngưỡng & Phân loại rủi ro** | Ngưỡng quyết định chính thức: **0.60**<br>- Xác suất $\ge 0.60$: **Default** (High Risk)<br>- $0.30 \le \text{Xác suất} < 0.60$: **Non-Default** (Medium Risk)<br>- Xác suất $< 0.30$: **Non-Default** (Low Risk) | Logic kinh doanh đã kiểm định, không được thay đổi trên Mobile. |
| **Explainable AI (XAI)** | SHAP `TreeExplainer` hỗ trợ giải thích cục bộ qua hàm `compute_shap_single()` và `get_top_shap_contributors()`. | Trả về đóng góp SHAP theo log-odds margin. |

---

## 2. Xác thực Kết nối và Cấu trúc PostgreSQL (Confirmed DB Facts)

| Tiêu chí | Cấu hình & Hiện trạng thực tế | Bằng chứng kiểm tra |
| :--- | :--- | :--- |
| **Trạng thái kết nối** | **ĐÃ KẾT NỐI THÀNH CÔNG** qua SSH Tunnel | Hàm `src.database.check_db_status()` trả về `(True, 'Đã kết nối an toàn qua SSH Tunnel (Port 15432)')`. |
| **Cấu hình kết nối (.env)** | `DB_HOST=127.0.0.1`, `DB_PORT=15432`<br>`DB_NAME=credit_risk_db`, `DB_USER=app_streamlit` | Cấu hình qua biến môi trường, bảo mật thông tin đăng nhập. |
| **Topology mạng DB** | Windows Port `15432` $\rightarrow$ SSH Tunnel $\rightarrow$ Ubuntu `192.168.100.34:5433` $\rightarrow$ Docker `credit-risk-postgres-db:5432` | Đang chạy bình thường trên máy chủ Ubuntu. |
| **Schema cơ sở dữ liệu** | `credit_app` | Schema hiện hữu chứa dữ liệu của đồ án. |
| **Bảng `credit_app.model_metadata`** | Chứa 1 bản ghi: `model_id='xgboost_tuned_v1'`, `threshold=0.60`, `roc_auc=0.7769`, `f1_score=0.5409`. | Đã kiểm tra qua truy vấn SQL thực tế. |
| **Bảng `credit_app.customer_predictions`** | Khóa chính: `id` (`bigint` sinh bởi sequence `credit_app.customer_predictions_id_seq`).<br>Thời gian: `created_at` (`timestamptz`, default `CURRENT_TIMESTAMP`).<br>Các cột: 23 thuộc tính đầu vào (`numeric`, `integer`), `default_probability`, `prediction_label`, `risk_level`, `model_version`, `threshold`, `engineered_features` (`jsonb`). | Hiện đã có dữ liệu dự báo từ ứng dụng Streamlit (các bản ghi ID #2, #3, #4...). |
| **Độ an toàn truy vấn** | **100% Parameterized Queries** | Sử dụng cú pháp tham số `%(key)s` của `psycopg2`, ngăn ngừa triệt để lỗ hổng SQL Injection. |
| **Cơ chế Graceful Degradation** | Khi mất kết nối DB, hàm lưu trả về `(False, None, error_msg)` mà không làm sập ứng dụng. | Tiến trình suy luận ML vẫn hoạt động độc lập và trả về kết quả cho người dùng. |

---

## 3. Khảo sát Môi trường và Toolchain Phát triển (Environment & Tooling)

| Công cụ / Nền tảng | Phiên bản / Đường dẫn thực tế | Trạng thái sẵn sàng |
| :--- | :--- | :---: |
| **Python** | Python 3.14.4 tại `F:\DATN\project\.venv\Scripts\python.exe` | **SẴN SÀNG** |
| **Thư viện Web & API** | `uvicorn 0.54.0`, `starlette 1.7.0` đã có trong `.venv`.<br>Chưa có: `fastapi`, `pydantic`. | **CẦN CÀI BỔ SUNG** (`fastapi`, `pydantic` vào `.venv`) |
| **Flutter SDK** | Flutter 3.47.2 (Channel stable) tại `C:\src\flutter` | **SẴN SÀNG** |
| **Dart SDK** | Dart 3.13.2 | **SẴN SÀNG** |
| **Android SDK** | Android SDK 36.0.0 (Platform 37.0, Build-tools 36.0.0) tại `F:\App\Android\SDK` | **SẴN SÀNG** |
| **Java JDK** | OpenJDK 25.0.2 tại `F:\App\Android\Android Studio\jbr` | **SẴN SÀNG** |
| **Android Licenses** | Tất cả 8/8 giấy phép SDK đã được chấp thuận (`All SDK package licenses accepted`). | **SẴN SÀNG** (`flutter doctor` báo `No issues found!`) |
| **Android Debug Bridge** | `F:\App\Android\SDK\platform-tools\adb.exe` (Version 1.0.41) | **SẴN SÀNG** |
| **Thiết bị Android vật lý** | Chưa cắm thiết bị qua cổng USB Debugging. | Sẽ kết nối ở Phase 6 qua Wi-Fi chung hoặc cáp USB. |
| **Mạng kết nối di động** | Card mạng Wi-Fi Windows Host có IP: `192.168.100.11`.<br>Cùng dải mạng nội bộ với Ubuntu Host `192.168.100.34`. | Điện thoại kết nối chung mạng Wi-Fi sẽ truy cập FastAPI qua `http://192.168.100.11:8000`. |

---

## 4. Các Giả định Cần Làm rõ và Điểm Cần Lưu ý (Assumptions & Risks)

1. **Bảo tồn ứng dụng Streamlit**:
   Ứng dụng `app.py` và `src/` hiện đang hoạt động ổn định. Tuyệt đối không chỉnh sửa `app.py` hay cấu trúc mô hình. FastAPI sẽ được triển khai như một dịch vụ backend độc lập chạy song song.
2. **Cài đặt thư viện Python**:
   Chỉ cài đặt `fastapi` và `pydantic` vào môi trường ảo `F:\DATN\project\.venv`, không cài đặt toàn cục (global).
3. **Cơ chế kết nối của Điện thoại Android vật lý**:
   Điện thoại thật không thể dùng `127.0.0.1` hay `localhost`. Cần cho phép FastAPI bind vào `0.0.0.0:8000` trên Windows Host và cấu hình cấu trúc Base URL trên Flutter có thể cấu hình linh hoạt (`http://192.168.100.11:8000` hoặc chỉnh sửa trên màn hình Cài đặt).
4. **Bảo mật mạng PostgreSQL**:
   FastAPI chạy trên Windows Host sẽ kết nối tới PostgreSQL thông qua SSH Tunnel `127.0.0.1:15432`. Điện thoại di động chỉ giao tiếp với FastAPI qua HTTP REST API, tuyệt đối không mở trực tiếp cổng PostgreSQL ra mạng ngoài.
5. **Dự án STIX-TAXII**:
   Nằm độc lập trên hệ thống Ubuntu, không có bất kỳ thao tác nào can thiệp tới container hay dữ liệu của dự án này.

---

## 5. Kết quả Kiểm thử Cơ sở Hiện tại (Baseline Tests)

| Kiểm thử | Kết quả | Bằng chứng chi tiết |
| :--- | :---: | :--- |
| **Kiểm tra tính toàn vẹn 6/6 tests ([scripts/test_week10.py](file:///f:/DATN/project/scripts/test_week10.py))** | **PASS** | Test 1 (Bình thường): Xác suất 0.1189, Nhãn Non-Default, Low Risk.<br>Test 2 (Rủi ro cao): Xác suất 0.7822, Nhãn Default, High Risk.<br>Test 3 (Rủi ro thấp): Xác suất 0.1896, Nhãn Non-Default, Low Risk.<br>Test 4 (33 đặc trưng): Khớp 100% với `X_train_fe.csv`.<br>Test 5 (Độ nhất quán trực tiếp): Sai số $0.00\times 10^0$.<br>Test 6 (SHAP explanation): Tính toán SHAP TreeExplainer thành công. |
| **Kiểm tra kết nối PostgreSQL ([src/database.py](file:///f:/DATN/project/src/database.py))** | **PASS** | `check_db_status()` trả về True, truy vấn 3 bản ghi dự báo gần nhất thành công. |
| **Kiểm tra công cụ di động (`flutter doctor`)** | **PASS** | Flutter 3.47.2, Android toolchain 36.0.0, OpenJDK 25.0.2 đều đạt chuẩn 100%. |

---

## 6. Kiến trúc Đề xuất và Kế hoạch Thực hiện Từng giai đoạn

### 6.1. Cấu trúc Thư mục và File Đề xuất:

```text
F:\DATN\project\
├── api/                           # [MỚI] FastAPI REST Backend
│   ├── __init__.py
│   ├── main.py                    # Khởi tạo FastAPI, CORS, Exception Handlers
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py              # GET /health
│   │   └── predictions.py         # POST /api/v1/predictions, GET /api/v1/predictions, GET /api/v1/predictions/{id}
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── prediction.py          # Pydantic schemas: CustomerInputSchema, PredictionResponseSchema, HistorySchema
│   └── services/
│       ├── __init__.py
│       └── prediction_service.py  # Service gọi src/prediction.py và src/database.py
├── mobile/                        # [MỚI] Ứng dụng Flutter Android Mobile App
│   ├── pubspec.yaml
│   ├── lib/
│   │   ├── main.dart
│   │   ├── config/api_config.dart
│   │   ├── models/                # CustomerInput, PredictionResult, PredictionHistory
│   │   ├── services/api_service.dart
│   │   └── screens/
│   │       ├── home_dashboard_screen.dart
│   │       ├── customer_input_form_screen.dart
│   │       ├── prediction_result_screen.dart
│   │       ├── prediction_history_screen.dart
│   │       └── settings_screen.dart
├── tests/                         # [MỚI] Bộ kiểm thử API & ML Consistency
│   ├── test_api_health.py
│   ├── test_api_prediction.py
│   └── test_ml_consistency.py
├── src/                           # [GIỮ NGUYÊN] Các module hiện hữu
├── models/                        # [GIỮ NGUYÊN] Các file model và scaler hiện hữu
├── app.py                         # [GIỮ NGUYÊN] Ứng dụng Streamlit hiện hữu
```

### 6.2. Kế hoạch triển khai chi tiết:

1. **Giai đoạn 2 & 3 (FastAPI REST Backend)**:
   - Cài đặt `fastapi` và `pydantic` vào `.venv`.
   - Tạo thư mục `api/` và triển khai các schemas, endpoints `/health`, `/api/v1/predictions` (POST dự báo & lưu DB, GET xem lịch sử, GET chi tiết).
   - Đảm bảo cơ chế Graceful Degradation: Nếu CSDL gặp sự cố, vẫn trả về kết quả dự báo thành công và cờ `persisted: false`.
2. **Giai đoạn 4 (Kiểm thử API & Tính nhất quán ML)**:
   - Viết và chạy automated tests trong `tests/` để so sánh trực tiếp kết quả giữa `src/prediction.py`, Streamlit logic và FastAPI endpoint trên cùng một bộ dữ liệu thử nghiệm.
3. **Giai đoạn 5 (Flutter Android App)**:
   - Khởi tạo dự án Flutter trong thư mục `mobile/`.
   - Xây dựng 5 màn hình chuẩn Material 3: Dashboard, Form nhập liệu 23 trường có validation chặt chẽ, Màn hình kết quả trực quan (Gauge chart, nhãn cảnh báo), Màn hình lịch sử dự báo (kèm pull-to-refresh), Màn hình cài đặt IP máy chủ.
4. **Giai đoạn 6 & 8 (Build APK & Hướng dẫn kết nối thiết bị thật)**:
   - Cấu hình quyền `INTERNET` và network security config cho Android (hỗ trợ HTTP cleartext cục bộ trong môi trường dev).
   - Biên dịch debug APK: `mobile/build/app/outputs/flutter-apk/app-debug.apk`.
   - Hướng dẫn cấu hình kết nối mạng Wi-Fi và thử nghiệm trên điện thoại thật.
5. **Giai đoạn 7 & 9 (Kiểm thử hồi quy & Hoàn thiện tài liệu)**:
   - Chạy toàn bộ bài kiểm tra hồi quy xác nhận Streamlit, ML model và PostgreSQL vẫn nguyên vẹn 100%.
   - Tạo các tài liệu kiến trúc, kiểm thử và hướng dẫn demo trong `reports/`.
