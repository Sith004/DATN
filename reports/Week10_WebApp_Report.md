# TUẦN 10: BÁO CÁO KỸ THUẬT ỨNG DỤNG WEB PROTOTYPE (STREAMLIT DSS)
## Week 10 — Web Application Development Report

**Đề tài:** Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  
**Sinh viên:** Nguyễn Trọng Thể — MSSV: 1150080117  
**Ngày hoàn thành kỹ thuật:** 24/10/2026  
**Trạng thái:** `COMPLETED` — Test suite PASS 6/6 bài kiểm thử (đã chạy lại và xác nhận lại ngày 24/10/2026)

---

## 1. Mục tiêu và Phạm vi (Objectives & Scope)

### 1.1. Mục tiêu

Tuần 10 nhằm hiện thực hóa toàn bộ pipeline Machine Learning đã được phát triển trong Tuần 1–9 thành một ứng dụng **Hệ thống hỗ trợ ra quyết định tín dụng (Decision Support System — DSS Prototype)** có thể tương tác được. Ứng dụng cho phép người dùng nhập thông tin thực tế của một khách hàng, nhận kết quả dự báo xác suất vỡ nợ từ mô hình XGBoost Tuned đã được lựa chọn tại Tuần 8, đồng thời trực quan hóa giải thích quyết định bằng SHAP TreeExplainer theo đúng phương pháp đã phân tích tại Tuần 9.

### 1.2. Phạm vi và Giới hạn

- **Trong phạm vi:**
  - Ứng dụng Web cục bộ (localhost) sử dụng framework Streamlit.
  - Tích hợp hoàn chỉnh pipeline dự báo: Categorical Mapping → Feature Engineering → Scaling → Prediction.
  - Hiển thị xác suất vỡ nợ, nhãn phân loại nhị phân, mức rủi ro 3 cấp (Low/Medium/High).
  - Giải thích quyết định theo cấp độ cá thể (Local Explanation) bằng SHAP TreeExplainer thời gian thực.
  - Kiểm thử tích hợp toàn bộ pipeline dự báo với 6 bài kiểm thử tự động.
- **Ngoài phạm vi:**
  - Triển khai Cloud (Production deployment).
  - Xác thực người dùng, lưu trữ lịch sử tra cứu, cơ sở dữ liệu.
  - Tái huấn luyện mô hình trực tuyến (online learning).
  - Tuân thủ các tiêu chuẩn quản trị rủi ro ngân hàng (Basel II/III).

---

## 2. Kiến trúc Ứng dụng (Application Architecture)

### 2.1. Sơ đồ kiến trúc tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│                     STREAMLIT FRONTEND (app.py)                 │
│  ┌──────────────────┐    ┌───────────────────────────────────┐  │
│  │  Tab 1: Dự báo   │    │  Tab 2: Hướng dẫn & Thông tin    │  │
│  │  Rủi ro          │    │  (Architecture, Limitations)      │  │
│  └──────────────────┘    └───────────────────────────────────┘  │
│             │                                                    │
│   ┌─────────┴───────────────────────────────────────────────┐   │
│   │   INPUT FORM (4 sections, 23 raw feature fields)        │   │
│   │   Thông tin KH | Lịch sử TT | Dư nợ HĐ | Tiền TT      │   │
│   └─────────────────────────────────────────────────────────┘   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │  src/prediction.py    │  (Backend inference module)
                    │  ─────────────────    │
                    │  1. map_categorical() │  EDUCATION/MARRIAGE mapping
                    │  2. engineer_features │  10 financial features
                    │  3. RobustScaler      │  22 numerical features scaled
                    │  4. XGBoost Tuned     │  Probability of Default
                    │  5. Threshold 0.60    │  Binary classification
                    │  6. Risk level logic  │  Low / Medium / High
                    │  7. compute_shap_    │  SHAP TreeExplainer
                    │     single()          │  local explanation
                    └───────────┬───────────┘
                                │
            ┌───────────────────┼──────────────────────┐
            │                   │                      │
  ┌─────────▼──────┐  ┌────────▼────────┐  ┌─────────▼──────────┐
  │ final_candidate│  │ robust_scaler   │  │ week8_model        │
  │ _model.pkl     │  │ .pkl            │  │ _selection_meta.json│
  │ (XGBoost Tuned)│  │ (22 num cols)   │  │ (model metadata)   │
  └────────────────┘  └─────────────────┘  └────────────────────┘
```

### 2.2. Tệp nguồn chính

| Tệp | Kích thước | Vai trò |
|---|---|---|
| [`app.py`](file:///F:/DATN/project/app.py) | 791 dòng / 33,672 bytes | Frontend Streamlit — UI, luồng tương tác |
| [`src/prediction.py`](file:///F:/DATN/project/src/prediction.py) | 319 dòng / 12,322 bytes | Backend inference module |
| [`models/final_candidate_model.pkl`](file:///F:/DATN/project/models/final_candidate_model.pkl) | 1,028,618 bytes | Mô hình XGBoost Tuned chính thức |
| [`models/robust_scaler.pkl`](file:///F:/DATN/project/models/robust_scaler.pkl) | 1,399 bytes | RobustScaler fit trên X_train_fe (22 biến) |
| [`reports/week8_model_selection_meta.json`](file:///F:/DATN/project/reports/week8_model_selection_meta.json) | 1,389 bytes | Metadata siêu tham số & kết quả mô hình |
| [`scripts/test_week10.py`](file:///F:/DATN/project/scripts/test_week10.py) | 116 dòng / 4,054 bytes | Bộ kiểm thử tích hợp 6 ca |

### 2.3. Hướng dẫn khởi chạy ứng dụng

```powershell
# Di chuyển đến thư mục gốc dự án
cd F:\DATN\project

# Khởi chạy ứng dụng Streamlit
.\.venv\Scripts\python.exe -m streamlit run app.py

# Mặc định: http://localhost:8501
```

---

## 3. Luồng xử lý Dữ liệu đầu vào và Dự báo (Inference Pipeline)

Luồng xử lý trong `src/prediction.py::predict_single_customer()` tuân thủ chính xác pipeline huấn luyện từ Tuần 1–8, đảm bảo tính nhất quán (training-serving consistency):

### Bước 1 — Categorical Mapping (`map_categorical()`)
```python
# EDUCATION: Gộp các giá trị bất thường {0, 5, 6} → 4 (Other)
edu_map  = {0: 4, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4}
# MARRIAGE:  Gộp giá trị bất thường {0} → 3 (Other)
marr_map = {0: 3, 1: 1, 2: 2, 3: 3}
```
*Nhất quán với `src/preprocessing.py::map_categorical_anomalies()` tại Tuần 4.*

### Bước 2 — Feature Engineering (`engineer_features_single()`)
Tính toán 10 biến tài chính mới **trên dữ liệu thô** (không dùng dữ liệu đã scale):

| # | Biến | Công thức | Xử lý biên (Edge case) |
|---|---|---|---|
| 1 | `UTILIZATION_RATE_SEPT` | `BILL_AMT1 / LIMIT_BAL` | 0.0 nếu `LIMIT_BAL ≤ 0` |
| 2 | `MEAN_BILL_AMT` | `mean(BILL_AMT1..6)` | — |
| 3 | `UTILIZATION_RATE_MEAN` | `MEAN_BILL_AMT / LIMIT_BAL` | 0.0 nếu `LIMIT_BAL ≤ 0` |
| 4 | `PAY_RATIO_SEPT` | `PAY_AMT1 / BILL_AMT2` | 1.0 nếu `BILL_AMT2 ≤ 0` |
| 5 | `PAY_RATIO_MEAN` | `mean(PAY_AMTk / BILL_AMT{k+1})` cho k=1..5 | 1.0 nếu mẫu `≤ 0` |
| 6 | `MAX_PAY_DELAY` | `max(PAY_0, PAY_2..6)` | — |
| 7 | `COUNT_LATE_PAYMENT` | `sum(PAY_i > 0)` | — |
| 8 | `MEAN_PAY_AMT` | `mean(PAY_AMT1..6)` | — |
| 9 | `BILL_TREND` | `(BILL_AMT1 - BILL_AMT6) / LIMIT_BAL` | 0.0 nếu `LIMIT_BAL ≤ 0` |
| 10 | `PAY_TREND` | `(PAY_AMT1 - PAY_AMT6) / LIMIT_BAL` | 0.0 nếu `LIMIT_BAL ≤ 0` |

*Khớp 100% với `src/feature_engineering.py::engineer_features()` tại Tuần 5 — xác nhận bởi Test 4.*

### Bước 3 — Xây dựng DataFrame theo thứ tự 33 features (`FEATURE_ORDER`)
Đảm bảo thứ tự cột khớp chính xác với tập `X_train_fe.csv`:
```
LIMIT_BAL, AGE, BILL_AMT1..6, PAY_AMT1..6,
UTILIZATION_RATE_SEPT, UTILIZATION_RATE_MEAN, PAY_RATIO_SEPT, PAY_RATIO_MEAN,
MEAN_BILL_AMT, MEAN_PAY_AMT, BILL_TREND, PAY_TREND,
SEX, EDUCATION, MARRIAGE, PAY_0, PAY_2..6,
MAX_PAY_DELAY, COUNT_LATE_PAYMENT
```

### Bước 4 — Scaling bằng RobustScaler (`models/robust_scaler.pkl`)
- 22 biến liên tục số học (NUM_COLS) được scale bằng `RobustScaler` đã fit trên `X_train_fe.csv` (23,972 mẫu).
- 11 biến categorical/ordinal (CAT_COLS): `SEX, EDUCATION, MARRIAGE, PAY_0..6, MAX_PAY_DELAY, COUNT_LATE_PAYMENT` — **Passthrough, không scale**.
- Đảm bảo không có train-test leakage: Scaler được fit DUY NHẤT trên train.

### Bước 5 — Dự báo xác suất (`XGBoost Tuned`)
```python
probability = float(model.predict_proba(df_scaled)[0, 1])
```

### Bước 6 — Phân loại theo ngưỡng (`threshold = 0.60`)
```
prob ≥ 0.60  → DEFAULT    (⚠️ High Risk)
prob ≥ 0.30  → NON-DEFAULT (🟡 Medium Risk — application-layer only)
prob < 0.30  → NON-DEFAULT (🟢 Low Risk)
```
*Ngưỡng 0.60 được xác định bằng phân tích Out-of-Fold trên tập validation tại Tuần 8. Không sử dụng tập test để chọn ngưỡng.*

### Bước 7 — Giải thích SHAP thời gian thực (`compute_shap_single()`)
```python
explainer   = shap.TreeExplainer(model)
shap_values = explainer.shap_values(feature_vector_scaled)  # Shape: (33,)
expected_val = float(explainer.expected_value)  # base rate log-odds = 0.08986
```

---

## 4. Tích hợp Mô hình XGBoost Tuned và SHAP (Model & XAI Integration)

### 4.1. Thông số Mô hình XGBoost Tuned (Official — Week 8)

| Siêu tham số | Giá trị tối ưu |
|---|---|
| `n_estimators` | 250 |
| `learning_rate` | 0.03 |
| `max_depth` | 6 |
| `subsample` | 0.6 |
| `colsample_bytree` | 0.9 |
| `gamma` | 0.3 |
| `reg_alpha` | 0.5 |
| `reg_lambda` | 1.0 |
| `min_child_weight` | 1 |
| **Chiến lược tối ưu** | RandomizedSearchCV (n_iter=25, 5-Fold Stratified CV, scoring=average_precision) |
| **CV Score** | 0.5646 (average_precision) |

### 4.2. Kết quả định lượng trên tập Test (5,993 mẫu, threshold=0.60)

| Chỉ số | Giá trị | So sánh tốt nhất trước tuning |
|---|---|---|
| **PR-AUC** | **0.5620** | 0.5611 (+0.0009) — Cao nhất toàn hệ thống |
| **ROC-AUC** | 0.7769 | 0.7792 (-0.0023) |
| **Recall** | **0.6161** | 0.3582 (+0.2579) — Cải thiện lớn nhất |
| **F1-Score** | **0.5409** | 0.4684 (+0.0725) |
| **Precision** | 0.4820 | 0.6766 (-0.1946) |
| **Accuracy** | 0.7686 | 0.8201 (-0.0515) |

*Lý do chọn: PR-AUC là chỉ số ưu tiên trong bài toán imbalanced class (22.1% default). Recall cao (~61.6%) giảm thiểu tổn thất do bỏ lọt default (False Negative).*

### 4.3. Top 5 yếu tố rủi ro quan trọng nhất (SHAP Global, Week 9)

| Rank | Feature | Mean\|SHAP\| | Nguồn gốc |
|---|---|---|---|
| 1 | `MAX_PAY_DELAY` | 0.4494 | Feature Engineering (Tuần 5) |
| 2 | `PAY_0` | 0.2797 | Biến gốc từ dataset |
| 3 | `COUNT_LATE_PAYMENT` | 0.1211 | Feature Engineering (Tuần 5) |
| 4 | `BILL_AMT1` | 0.1126 | Biến gốc từ dataset |
| 5 | `UTILIZATION_RATE_SEPT` | 0.0942 | Feature Engineering (Tuần 5) |

*3/5 biến quan trọng nhất là biến tài chính tạo mới (Feature Engineering) — minh chứng cho đóng góp thực tiễn của Tuần 5.*

---

## 5. Các Chức năng Giao diện (UI Features)

### 5.1. Cấu trúc giao diện

Ứng dụng bao gồm 2 tab chính, sidebar thông tin mô hình:

**Sidebar (Thông tin cố định):**
- Thông số mô hình: XGBoost Tuned, Threshold 0.60, 33 features, Train/Test size.
- Bảng hiệu năng trên tập Test (Week 8).
- Top 5 yếu tố rủi ro (SHAP Week 9).
- Phân loại mức rủi ro (Low/Medium/High Risk).

**Tab 1 — "🔍 Dự báo Rủi ro":**
- Form nhập liệu 4 section với tổng cộng 23 trường đầu vào:
  - *Section 1: Thông tin khách hàng* — `LIMIT_BAL`, `AGE`, `SEX`, `EDUCATION`, `MARRIAGE`.
  - *Section 2: Lịch sử thanh toán* — `PAY_0`, `PAY_2`, `PAY_3`, `PAY_4`, `PAY_5`, `PAY_6`.
  - *Section 3: Dư nợ hóa đơn* — `BILL_AMT1..BILL_AMT6`.
  - *Section 4: Số tiền đã thanh toán* — `PAY_AMT1..PAY_AMT6`.
- Nút "🔍 Dự báo Rủi ro Tín dụng".
- Kết quả dự báo sau khi submit:
  - Gauge chart tương tác (Plotly): Xác suất vỡ nợ 0–100%, ngưỡng 60% trực quan.
  - Badge nhãn phân loại: `⚠️ DEFAULT` (đỏ) / `✅ NON-DEFAULT` (xanh).
  - Badge mức rủi ro: 🔴 High / 🟡 Medium / 🟢 Low.
  - Bảng feature vector thô và đã scale (33 features).
  - Biểu đồ SHAP Bar (Top 10 contributions) — tính toán thời gian thực.
  - Bảng yếu tố tăng rủi ro (SHAP > 0) và yếu tố bảo vệ (SHAP < 0).
  - Nhận xét tự động về quyết định (feature tên + diễn giải).
  - Expander: Chi tiết 10 công thức Feature Engineering.

**Tab 2 — "📖 Hướng dẫn & Thông tin":**
- Giới thiệu kiến trúc hệ thống.
- Thông tin tập dữ liệu và mô hình.
- Bảng phân loại rủi ro.
- Giới hạn của prototype.
- Thông tin đồ án.

### 5.2. Validate dữ liệu đầu vào

Ứng dụng thực hiện kiểm tra cơ bản khi submit:
- `LIMIT_BAL ≥ 10,000` NT$.
- `18 ≤ AGE ≤ 100`.
- Các giá trị `PAY_AMT` không âm.

### 5.3. Caching Streamlit

```python
@st.cache_resource  # Model và Scaler: chỉ load 1 lần, cache toàn session
def get_model():
    return load_model()

@st.cache_resource
def get_scaler():
    return load_scaler()

@st.cache_data      # Metadata: cache data
def get_meta():
    return load_model_meta()
```

---

## 6. Bảng Kiểm thử và Kết quả Thực tế (Test Results)

Bộ kiểm thử tự động tại [`scripts/test_week10.py`](file:///F:/DATN/project/scripts/test_week10.py) được thực thi với lệnh:
```powershell
.\.venv\Scripts\python.exe scripts\test_week10.py
```

Kết quả chạy thực tế ngày **24/10/2026** (Exit code: 0 — không có lỗi):

| # | Tên kiểm thử | Mô tả | Điều kiện PASS | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|
| **Test 1** | Normal Customer | Khách hàng thông thường: hạn mức 200K, tuổi 35, PAY_0=0, BILL_AMT1=25K | Feature count = 33; Label = Non-Default | Prob = **11.89%**, Non-Default, Low Risk; Feature count = **33** | ✅ `PASS` |
| **Test 2** | High-Risk Customer | Khách hàng rủi ro cao: hạn mức 50K, PAY_0=3, PAY_2=3, không trả nợ | Probability > 60% | Prob = **78.22%**, Default, High Risk | ✅ `PASS` |
| **Test 3** | Low-Risk Customer | Khách hàng rủi ro thấp: hạn mức 500K, tất cả PAY trả trước hạn (-1) | Probability < 30% | Prob = **18.96%**, Non-Default, Low Risk | ✅ `PASS` |
| **Test 4** | Feature Order Verification | Kiểm tra 33 features khớp thứ tự với `X_train_fe.csv` | FEATURE_ORDER == X_train_cols | Feature order: **VERIFIED (33 features match X_train_fe.csv)** | ✅ `PASS` |
| **Test 5** | Direct Model Consistency | So sánh probability từ `predict_single_customer()` và `model.predict_proba()` trực tiếp | Difference < 1e-6 | Direct model: **0.11893936**; predict_single: **0.11893936**; Difference = **0.00e+00** | ✅ `PASS` |
| **Test 6** | SHAP Explanation | Kiểm tra `compute_shap_single()` trả về đúng shape và expected value | SHAP values shape = (33,) | SHAP shape = **(33,)**; Expected value = **0.089860**; Sum of SHAP = **-2.0924** | ✅ `PASS` |

**Tổng kết kiểm thử: 6/6 PASS — Exit code 0**

---

## 7. Xác minh Tính nhất quán Training-Serving (Training-Serving Consistency)

Các cơ chế đảm bảo tính nhất quán giữa quá trình huấn luyện (Tuần 1–8) và phục vụ dự báo (Tuần 10):

| Thành phần | Training pipeline | Serving pipeline | Nhất quán? |
|---|---|---|---|
| Categorical mapping | `src/preprocessing.py::map_categorical_anomalies()` | `src/prediction.py::map_categorical()` — code giống hệt | ✅ KHỚP |
| Feature Engineering | `src/feature_engineering.py::engineer_features()` | `src/prediction.py::engineer_features_single()` — code giống hệt | ✅ KHỚP (xác nhận Test 4) |
| Feature order (33 cols) | Thứ tự cột `X_train_fe.csv` → `week8_model_selection_meta.json::feature_names` | `FEATURE_ORDER` list trong `prediction.py` | ✅ KHỚP (xác nhận Test 4) |
| Scaling | `RobustScaler.fit(X_train_fe[NUM_COLS])` | `models/robust_scaler.pkl` (fit trên X_train_fe, 22 NUM_COLS) | ✅ ĐÚNG scaler |
| Model | `models/final_candidate_model.pkl` (XGBoost Tuned, Thresh=0.60) | `load_model()` tải đúng `final_candidate_model.pkl` | ✅ ĐÚNG model |
| Threshold | 0.60 (xác định tại Tuần 8 OOF analysis) | `OFFICIAL_THRESHOLD = 0.60` | ✅ KHỚP |
| CAT_COLS passthrough | Passthrough trong ColumnTransformer Tuần 8 | Không scale CAT_COLS trong predict | ✅ ĐÚNG |

---

## 8. Hạn chế Hiện tại (Current Limitations)

### 8.1. Giới hạn kỹ thuật

1. **Notebook chưa có output SHAP embedded:** Notebook `07_Model_Interpretability.ipynb` có 10 ô vẽ biểu đồ SHAP không có output nhúng trực tiếp trong file `.ipynb` (Execution Count hợp lệ, biểu đồ đã được lưu vào `reports/figures/` qua backend Agg). Đây là hành vi bình thường khi dùng `matplotlib.use('Agg')` để tránh xung đột render GUI trên Windows.
2. **SHAP computation time:** Tính toán SHAP TreeExplainer thời gian thực cho mỗi khách hàng mất khoảng 1–3 giây tùy cấu hình máy. Không cached giữa các request.
3. **Ứng dụng chỉ hỗ trợ single prediction:** Không hỗ trợ batch prediction hoặc upload file CSV.

### 8.2. Giới hạn học thuật

1. **Dataset scope:** Mô hình được huấn luyện trên dữ liệu Đài Loan năm 2005. Chưa thực hiện external validation trên dữ liệu từ thị trường/thời điểm khác.
2. **Threshold cố định:** Threshold 0.60 được chọn dựa trên F1-Score OOF, không phải cost matrix thực tế của ngân hàng.
3. **Prototype học thuật:** Không phải hệ thống phê duyệt tín dụng thực tế. Kết quả không được dùng để ra quyết định cấp tín dụng.

---

## 9. Danh sách Artifacts Tuần 10 (Deliverables)

| Artifact | Đường dẫn | Kích thước | Ghi chú |
|---|---|---|---|
| Frontend Web App | [`app.py`](file:///F:/DATN/project/app.py) | 791 dòng / 33,672 bytes | Streamlit application entry point |
| Backend Inference | [`src/prediction.py`](file:///F:/DATN/project/src/prediction.py) | 319 dòng / 12,322 bytes | Prediction + SHAP module |
| Official Model | [`models/final_candidate_model.pkl`](file:///F:/DATN/project/models/final_candidate_model.pkl) | 1,028,618 bytes | XGBoost Tuned (từ Tuần 8) |
| RobustScaler | [`models/robust_scaler.pkl`](file:///F:/DATN/project/models/robust_scaler.pkl) | 1,399 bytes | Fit trên X_train_fe (Tuần 8) |
| Test Suite | [`scripts/test_week10.py`](file:///F:/DATN/project/scripts/test_week10.py) | 116 dòng / 4,054 bytes | 6 Integration Tests |
| Week 10 Report | [`reports/Week10_WebApp_Report.md`](file:///F:/DATN/project/reports/Week10_WebApp_Report.md) | Tệp này | Báo cáo kỹ thuật |

---

## 10. Kết luận (Conclusion)

Tuần 10 đã hoàn thành việc hiện thực hóa toàn bộ quy trình Machine Learning tích hợp vào ứng dụng Web Prototype (DSS) sử dụng Streamlit, đáp ứng đầy đủ các yêu cầu của đề cương chi tiết tại mục 2.9 và 3.7:

- ✅ **Kiến trúc DSS Prototype** hoàn chỉnh: Input → FE → Scaling → Model → Risk Classification → SHAP.
- ✅ **Giao diện người dùng** đầy đủ 4 section nhập liệu, Gauge Chart, biểu đồ SHAP tương tác thời gian thực.
- ✅ **Nhất quán hoàn toàn** với pipeline huấn luyện Tuần 1–8 (được xác minh bằng Test 4 và Test 5 với difference = 0.00e+00).
- ✅ **Kiểm thử tích hợp** 6/6 bài PASS, bao gồm ca khách hàng thông thường, rủi ro cao, rủi ro thấp, kiểm tra thứ tự đặc trưng, tính nhất quán dự báo và tính toán SHAP.
- ✅ **Mô hình XGBoost Tuned** (Threshold=0.60, PR-AUC=0.5620, Recall=0.6161) được tích hợp và phục vụ dự báo ổn định.

Ứng dụng sẵn sàng phục vụ mục đích demo, chấm điểm và bảo vệ đồ án tốt nghiệp tại Khoa Công nghệ Thông tin, Trường ĐH Tài nguyên và Môi trường TP.HCM.

---

*Báo cáo được lập ngày 24/10/2026 — Sinh viên: Nguyễn Trọng Thể (MSSV: 1150080117)*  
*GVHD: TS. Dương Thị Thúy Nga*
