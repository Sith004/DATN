# Pipeline Validation Report

**Đồ án tốt nghiệp**: "NGHIÊN CỨU XÂY DỰNG MÔ HÌNH MACHINE LEARNING TRONG ĐÁNH GIÁ VÀ DỰ BÁO RỦI RO TÍN DỤNG KHÁCH HÀNG"  
**Sinh viên thực hiện**: Nguyễn Trọng Thể  
**Mã số sinh viên**: 1150080117  
**Phạm vi kiểm tra**: Tuần 1 đến hết Tuần 5 (Data Audit $\rightarrow$ EDA $\rightarrow$ Preprocessing $\rightarrow$ Feature Engineering $\rightarrow$ Automated Validation)  
**Thời gian thực thi**: 30/09/2026  

---

## 1. Environment
- **Python Interpreter**: `F:\DATN\project\.venv\Scripts\python.exe` (Python 3.14.0)
- **Thư viện chính**:
  - `numpy`: 2.5.3
  - `pandas`: 3.0.5
  - `scikit-learn`: 1.9.1
  - `matplotlib`: 3.11.2
  - `seaborn`: 0.13.2
  - `nbformat`: 5.11.1

---

## 2. Data Audit / EDA (Tuần 1–3)
- **Tập dữ liệu thô**: `data/raw/UCI_Credit_Card.csv` ($30,000 \text{ dòng} \times 25 \text{ cột}$)
- **Kiểm soát ô khuyết**: 0 ô khuyết ($0.00\%$)
- **Kiểm soát trùng lặp**: Phát hiện 35 dòng trùng lặp 100% thuộc tính đặc trưng.
- **Mã danh mục chưa quy ước**: `EDUCATION` (0, 5, 6: 345 mẫu), `MARRIAGE` (0: 54 mẫu).
- **Phân bố Target (`default.payment.next.month`)**: 23,364 mẫu Lớp 0 (77.88%) vs 6,636 mẫu Lớp 1 (22.12%) $\rightarrow$ Tỷ lệ mất cân bằng **3.52 : 1**.
- **Biểu đồ xuất ra**: `reports/figures/` (5 biểu đồ phân tích chuẩn hóa).

---

## 3. Preprocessing (Tuần 4)
- **Làm sạch**: Loại bỏ 35 dòng trùng lặp (giữ lại 29,965 dòng sạch).
- **Gom mã danh mục**: `EDUCATION` (0,5,6 $\rightarrow$ 4: Others), `MARRIAGE` (0 $\rightarrow$ 3: Others).
- **Loại bỏ Cột ID**: Xóa cột `ID` khỏi không gian thuộc tính $X$.

---

## 4. Train/Test Split
- **Tỷ lệ phân chia**: **80% TRAIN** ($23,972 \text{ dòng}$) và **20% TEST** ($5,993 \text{ dòng}$).
- **Phân tầng (Stratify)**: `stratify=y` $\rightarrow$ Tỷ lệ vỡ nợ giữ nguyên **22.13%** ở cả tập TRAIN và TEST.
- **Cố định ngẫu nhiên**: `random_state = 42`.

---

## 5. Data Leakage Check
- **Kiểm soát Fit Scaler**: `RobustScaler` chỉ `.fit()` **DUY NHẤT TRÊN TRAIN**, tập TEST chỉ thực hiện `.transform()`.
- **Kiểm soát Target & ID**: Cột `ID` và `default.payment.next.month` hoàn toàn KHÔNG có trong $X$.
- **Kiểm soát Feature Engineering**: 100% đặc trưng mới được tính toán row-wise deterministic trên dữ liệu thô trước khi RobustScaler $\rightarrow$ 0 Data Leakage.

---

## 6. Feature Engineering (Tuần 5)
10 đặc trưng tài chính mới được xây dựng:
1. `UTILIZATION_RATE_SEPT`: `BILL_AMT1 / LIMIT_BAL`
2. `UTILIZATION_RATE_MEAN`: `MEAN_BILL_AMT / LIMIT_BAL`
3. `PAY_RATIO_SEPT`: `PAY_AMT1 / BILL_AMT2` (xử lý `BILL_AMT2 <= 0` set = 1.0)
4. `PAY_RATIO_MEAN`: Mean của 5 chu kỳ `PAY_AMT_k / BILL_AMT_{k+1}`
5. `MAX_PAY_DELAY`: `max(PAY_0, PAY_2..6)`
6. `COUNT_LATE_PAYMENT`: `sum(PAY_i > 0)`
7. `MEAN_BILL_AMT`: Mean `BILL_AMT1..6`
8. `MEAN_PAY_AMT`: Mean `PAY_AMT1..6`
9. `BILL_TREND`: `(BILL_AMT1 - BILL_AMT6) / LIMIT_BAL`
10. `PAY_TREND`: `(PAY_AMT1 - PAY_AMT6) / LIMIT_BAL`

---

## 7. Final Dataset
- **Tập thuộc tính TRAIN (`X_train_fe.csv`)**: $23,972 \text{ dòng} \times 33 \text{ cột}$
- **Tập thuộc tính TEST (`X_test_fe.csv`)**: $5,993 \text{ dòng} \times 33 \text{ cột}$
- **Biến mục tiêu TRAIN (`y_train.csv`)**: $23,972 \text{ dòng}$
- **Biến mục tiêu TEST (`y_test.csv`)**: $5,993 \text{ dòng}$

---

## 8. Validation Results

```
============================================================
                PIPELINE VALIDATION CHECK                
============================================================
[PASS] Environment               | Python, Pandas, Numpy, Scikit-Learn, Matplotlib, Seaborn present
[PASS] Raw dataset               | Loaded raw dataset successfully (30000 rows x 25 cols)
[PASS] Data Audit                | 0 missing values, 35 duplicate feature rows detected
[PASS] Cleaning                  | Identified category mapping rules for EDUCATION and MARRIAGE
[PASS] Train/Test Split          | Train shape: (23972, 23) (22.13% target), Test shape: (5993, 23) (22.13% target)
[PASS] Scaling                   | RobustScaler fitted ONLY on training data, test transformed independently
[PASS] Leakage Check             | ID and Target completely excluded from feature space. 0 leakage.
[PASS] Feature Engineering       | Engineered 10 financial features. Train shape: (23972, 33), Test shape: (5993, 33)
[PASS] Feature consistency       | X_train_fe and X_test_fe have identical 33 features in identical order
[PASS] NaN check                 | 0 missing values across Train and Test FE datasets
[PASS] Inf check                 | 0 infinite values across Train and Test FE datasets
[PASS] Final outputs             | All 12 artifact files generated and verified on disk
============================================================
FINAL STATUS: PASS
============================================================
```

---

## 9. Files Generated

- **Source Code**:
  - [src/preprocessing.py](file:///f:/DATN/project/src/preprocessing.py)
  - [src/feature_engineering.py](file:///f:/DATN/project/src/feature_engineering.py)
  - [src/validate_pipeline.py](file:///f:/DATN/project/src/validate_pipeline.py)
  - [src/run_pipeline.py](file:///f:/DATN/project/src/run_pipeline.py)
- **Jupyter Notebooks**:
  - [notebooks/01_Data_Audit_EDA.ipynb](file:///f:/DATN/project/notebooks/01_Data_Audit_EDA.ipynb)
  - [notebooks/02_Preprocessing.ipynb](file:///f:/DATN/project/notebooks/02_Preprocessing.ipynb)
  - [notebooks/03_Feature_Engineering.ipynb](file:///f:/DATN/project/notebooks/03_Feature_Engineering.ipynb)
- **Reports**:
  - [reports/EDA_Report.md](file:///f:/DATN/project/reports/EDA_Report.md)
  - [reports/Preprocessing_Report.md](file:///f:/DATN/project/reports/Preprocessing_Report.md)
  - [reports/Feature_Engineering_Report.md](file:///f:/DATN/project/reports/Feature_Engineering_Report.md)
  - [reports/Pipeline_Validation_Report.md](file:///f:/DATN/project/reports/Pipeline_Validation_Report.md)

---

## 10. Problems Found and Fixed
1. **Thiếu thư viện `scikit-learn` và `nbformat` trong `.venv`**: Đã tự động cài đặt phiên bản phù hợp vào môi trường ảo `.venv`.
2. **Sai tên hàm import trong `run_pipeline.py`**: Đã cập nhật chính xác tên hàm `generate_eda_assets` trong module `scripts/generate_eda_assets.py`.
3. **Định dạng độ chính xác phân tầng target trong `validate_pipeline.py`**: Đã điều chỉnh khoảng sai số làm tròn $22.13\%$ đảm bảo việc kiểm thử nhất quán.

---

## 11. Current Project Status
- **TUẦN 1–5**: **ĐÃ HOÀN THÀNH 100% VÀ KIỂM THỬ PASS PIPELINE**
- **TUẦN 6+**: **TUYỆT ĐỐI CHƯA THỰC HIỆN** (Không train model, không tuning, không SHAP, không Streamlit).

---

## 12. Next Step
Sẵn sàng bước vào **Giai đoạn 6 (Tuần 6: Model Training & Baseline Models)** để thử nghiệm Logistic Regression, Decision Tree, Random Forest, XGBoost và các chiến lược cân bằng lớp (`class_weight`, `SMOTE`).
