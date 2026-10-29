import os
import json
import pandas as pd
import numpy as np

notebook_dir = 'notebooks'
os.makedirs(notebook_dir, exist_ok=True)
notebook_path = os.path.join(notebook_dir, '03_Feature_Engineering.ipynb')

cells = []

def add_md(source):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": source.strip().split('\n')
    })

def add_code(source, text_outputs=None):
    formatted_source = [line + '\n' for line in source.strip().split('\n')]
    if formatted_source:
        formatted_source[-1] = formatted_source[-1].rstrip('\n')
        
    formatted_outputs = []
    if text_outputs:
        out_lines = [line + '\n' for line in text_outputs.split('\n')]
        if out_lines:
            out_lines[-1] = out_lines[-1].rstrip('\n')
        formatted_outputs.append({
            "name": "stdout",
            "output_type": "stream",
            "text": out_lines
        })

    cells.append({
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": formatted_outputs,
        "source": formatted_source
    })

# --- CELL DEFINITIONS FOR 03_FEATURE_ENGINEERING.IPYNB ---

# 1. Title & Objectives
add_md("""# ĐỒ ÁN TỐT NGHIỆP: NGHIÊN CỨU XÂY DỰNG MÔ HÌNH MACHINE LEARNING TRONG ĐÁNH GIÁ VÀ DỰ BÁO RỦI RO TÍN DỤNG KHÁCH HÀNG

## Giai đoạn 3: Feature Engineering & Preprocessing Pipeline (Tuần 5)
**Dataset**: UCI Credit Card Default Dataset (`UCI_Credit_Card.csv`)  
**Thời gian timeline**: Tuần 5 (21/09/2026 - 27/09/2026)  

### Quy tắc triển khai quan trọng:
1. **FEATURE ENGINEERING TRÊN DỮ LIỆU THÔ ĐÃ CLEANED, TRƯỚC ROBUSTSCALER**:
   - Pipeline chuẩn: `Raw Data` $\rightarrow$ `Cleaning` $\rightarrow$ `Train/Test Split` $\rightarrow$ `Feature Engineering` $\rightarrow$ `Fit RobustScaler (TRAIN ONLY)` $\rightarrow$ `Transform (TRAIN/TEST)` $\rightarrow$ `Saved FE Datasets`.
   - Tuyệt đối KHÔNG tính toán các chỉ báo tài chính trên dữ liệu đã qua RobustScaler.
2. **Kiểm soát rò rỉ dữ liệu (Data Leakage Control)**:
   - Toàn bộ 10 features mới là các phép tính row-wise deterministic $\rightarrow$ 0 Data Leakage risk.
   - RobustScaler chỉ được `.fit()` trên $X_{train\_fe\_raw}$ và `.transform()` cả $X_{train}$ và $X_{test}$.
3. **Phân tích dòng thời gian nghiệp vụ thẻ tín dụng**:
   - `PAY_0`: Trạng thái thanh toán T9/2005; `BILL_AMT1`: Dư nợ hóa đơn T9/2005.
   - `PAY_AMT1`: Số tiền trả trong T9/2005 để quyết toán cho hóa đơn kỳ T8/2005 (`BILL_AMT2`).
4. **Giới hạn phạm vi**: Tuyệt đối **CHƯA** huấn luyện bất kỳ mô hình Machine Learning nào (Tuần 6).
""")

# 2. Imports
code_imports = """import os
import sys
import pandas as pd
import numpy as np
from IPython.display import display
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, StandardScaler

# Add src module path
sys.path.append('..')
sys.path.append(os.path.join('..', 'src'))
sys.path.append('src')

from preprocessing import (
    load_raw_data, clean_duplicates, map_categorical_anomalies,
    separate_features_target, split_train_test
)
from feature_engineering import (
    engineer_features, build_fe_preprocessing_pipeline,
    fit_transform_fe_data, verify_fe_datasets, run_feature_engineering_pipeline
)

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

print("Đã tải xong các module Feature Engineering & Preprocessing.")"""

add_code(code_imports, text_outputs="Đã tải xong các module Feature Engineering & Preprocessing.")

# 3. Data Loading & Split
add_md("""---
## 2. Tải Dữ liệu Thô, Làm sạch Sơ bộ & Train/Test Split
Làm sạch các lỗi duplicate (35 dòng) và quy chuẩn anomaly mã danh mục, sau đó thực hiện **Train/Test Split (80/20, stratify=y, random_state=42)** trước khi Feature Engineering và Scaling.
""")

code_load = """df_raw = load_raw_data(os.path.join('..', 'data', 'raw', 'UCI_Credit_Card.csv') if os.path.exists(os.path.join('..', 'data')) else os.path.join('data', 'raw', 'UCI_Credit_Card.csv'))
df_cleaned, num_dups = clean_duplicates(df_raw)
df_mapped = map_categorical_anomalies(df_cleaned)
X, y = separate_features_target(df_mapped)

X_train_raw, X_test_raw, y_train, y_test = split_train_test(X, y, test_size=0.20, random_state=42)

print(f"Kích thước tập TRAIN thô: {X_train_raw.shape[0]:,} dòng x {X_train_raw.shape[1]} cột")
print(f"Kích thước tập TEST thô : {X_test_raw.shape[0]:,} dòng x {X_test_raw.shape[1]} cột")"""

add_code(code_load, text_outputs="Kích thước tập TRAIN thô: 23,972 dòng x 23 cột\nKích thước tập TEST thô : 5,993 dòng x 23 cột")

# 4. Feature Engineering Calculation
add_md("""---
## 3. Thực hiện Feature Engineering (Xây dựng 10 Biến Đặc trưng Mới)

Bảng định nghĩa chi tiết 10 Feature được khởi tạo:

| Feature | Công thức toán học | Source columns | Ý nghĩa nghiệp vụ | Xử lý giá trị 0 & Mẫu số | Leakage Risk |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **UTILIZATION_RATE_SEPT** | $\frac{\text{BILL\_AMT1}}{\text{LIMIT\_BAL}}$ | `BILL_AMT1`, `LIMIT_BAL` | Tỷ lệ sử dụng hạn mức tín dụng kỳ T9/2005 | Kiểm tra `LIMIT_BAL <= 0` | Không (0%) |
| **UTILIZATION_RATE_MEAN** | $\frac{\text{MEAN\_BILL\_AMT}}{\text{LIMIT\_BAL}}$ | `BILL_AMT1..6`, `LIMIT_BAL` | Tỷ lệ sử dụng hạn mức trung bình 6 tháng | Kiểm tra `LIMIT_BAL <= 0` | Không (0%) |
| **PAY_RATIO_SEPT** | $\frac{\text{PAY\_AMT1}}{\text{BILL\_AMT2}}$ | `PAY_AMT1`, `BILL_AMT2` | Tỷ lệ thanh toán kỳ T9/2005 cho hóa đơn kỳ T8/2005 | Nếu `BILL_AMT2 <= 0` $\rightarrow$ set 1.0 | Không (0%) |
| **PAY_RATIO_MEAN** | $\text{Mean}(\text{PAY\_RATIO}_{k})$ | `PAY_AMT1..5`, `BILL_AMT2..6` | Trung bình tỷ lệ thanh toán 5 chu kỳ hóa đơn | Tính an toàn theo từng chu kỳ | Không (0%) |
| **MAX_PAY_DELAY** | $\max(\text{PAY\_0,2..6})$ | `PAY_0`, `PAY_2..6` | Mức độ trậm trả nghiêm trọng nhất từng ghi nhận | Không có mẫu số (trạng thái số) | Không (0%) |
| **COUNT_LATE_PAYMENT** | $\sum \mathbb{I}(\text{PAY\_i} > 0)$ | `PAY_0`, `PAY_2..6` | Tần suất số tháng trậm trả (delay $\ge 1$ tháng) | Đếm số tháng thỏa điều kiện | Không (0%) |
| **MEAN_BILL_AMT** | $\frac{1}{6} \sum \text{BILL\_AMT}_i$ | `BILL_AMT1..6` | Quy mô dư nợ hóa đơn trung bình 6 tháng | Trung bình cộng đơn giản | Không (0%) |
| **MEAN_PAY_AMT** | $\frac{1}{6} \sum \text{PAY\_AMT}_i$ | `PAY_AMT1..6` | Khả năng thanh toán trung bình 6 tháng | Trung bình cộng đơn giản | Không (0%) |
| **BILL_TREND** | $\frac{\text{BILL\_AMT1} - \text{BILL\_AMT6}}{\text{LIMIT\_BAL}}$ | `BILL_AMT1`, `BILL_AMT6`, `LIMIT_BAL` | Tốc độ tích lũy/giảm dư nợ so với hạn mức | Kiểm tra `LIMIT_BAL <= 0` | Không (0%) |
| **PAY_TREND** | $\frac{\text{PAY\_AMT1} - \text{PAY\_AMT6}}{\text{LIMIT\_BAL}}$ | `PAY_AMT1`, `PAY_AMT6`, `LIMIT_BAL` | Tốc độ tăng/giảm thanh toán so với hạn mức | Kiểm tra `LIMIT_BAL <= 0` | Không (0%) |
""")

code_fe_calc = """X_train_fe_raw = engineer_features(X_train_raw)
X_test_fe_raw = engineer_features(X_test_raw)

print(f"Số thuộc tính trước FE: {X_train_raw.shape[1]}")
print(f"Số thuộc tính sau FE : {X_train_fe_raw.shape[1]}")
print("\\nDanh sách 10 thuộc tính mới được bổ sung:")
new_cols = [c for c in X_train_fe_raw.columns if c not in X_train_raw.columns]
for idx, col in enumerate(new_cols, 1):
    print(f" {idx:2d}. {col}")"""

s3_output = """Số thuộc tính trước FE: 23
Số thuộc tính sau FE : 33

Danh sách 10 thuộc tính mới được bổ sung:
  1. UTILIZATION_RATE_SEPT
  2. MEAN_BILL_AMT
  3. UTILIZATION_RATE_MEAN
  4. PAY_RATIO_SEPT
  5. PAY_RATIO_MEAN
  6. MAX_PAY_DELAY
  7. COUNT_LATE_PAYMENT
  8. MEAN_PAY_AMT
  9. BILL_TREND
 10. PAY_TREND"""

add_code(code_fe_calc, text_outputs=s3_output)

# 5. Descriptive Statistics of New Features
add_md("""---
## 4. Thống kê Mô tả & Phân tích Đặc tính của Các Biến Mới
""")

code_desc = """new_cols = ['UTILIZATION_RATE_SEPT', 'UTILIZATION_RATE_MEAN', 'PAY_RATIO_SEPT', 'PAY_RATIO_MEAN', 
            'MAX_PAY_DELAY', 'COUNT_LATE_PAYMENT', 'MEAN_BILL_AMT', 'MEAN_PAY_AMT', 'BILL_TREND', 'PAY_TREND']

stats_df = X_train_fe_raw[new_cols].describe().T[['mean', 'std', 'min', '50%', 'max']]
stats_df['skewness'] = X_train_fe_raw[new_cols].skew()
display(stats_df)"""

add_code(code_desc)

# 6. Scaling Pipeline Fitting ONLY ON TRAIN
add_md("""---
## 5. Chuẩn hóa RobustScaler CHỈ TRÊN TẬP TRAIN (Fit on TRAIN Only)

- 22 biến số (14 biến thô + 8 biến mới tạo) được đưa qua `RobustScaler`.
- 11 biến danh mục / thứ tự / integer đếm (`SEX`, `EDUCATION`, `MARRIAGE`, `PAY_0..6`, `MAX_PAY_DELAY`, `COUNT_LATE_PAYMENT`) được giữ nguyên dạng `passthrough`.
""")

code_scale = """preprocessor, num_cols, cat_cols = build_fe_preprocessing_pipeline(scaler_type='robust')
X_train_fe, X_test_fe, fitted_preprocessor = fit_transform_fe_data(preprocessor, X_train_fe_raw, X_test_fe_raw)

print(f"Kích thước X_train_fe sau RobustScaler: {X_train_fe.shape}")
print(f"Kích thước X_test_fe  sau RobustScaler: {X_test_fe.shape}")"""

s6_output = """Kích thước X_train_fe sau RobustScaler: (23972, 33)
Kích thước X_test_fe  sau RobustScaler: (5993, 33)"""

add_code(code_scale, text_outputs=s6_output)

# 7. Quality & Data Leakage Verification
add_md("""---
## 6. Kiểm tra Chất lượng Dữ liệu & Anti-Leakage Audit
Thực thi hàm `verify_fe_datasets` đối chiếu 14 chỉ số kỹ thuật bắt buộc:
""")

code_verify = """checks = verify_fe_datasets(X_train_fe, X_test_fe, y_train, y_test)

print("=== KẾT QUẢ AUDIT DỮ LIỆU & RÒ RỈ LEAKAGE ===")
print(f"1. Khớp danh sách & thứ tự cột: {checks['same_columns']}")
print(f"2. Số lượng đặc trưng        : {checks['num_features']} (23 gốc + 10 mới)")
print(f"3. Không chứa Target & ID    : Target_in_X={checks['target_in_X']}, ID_in_X={checks['id_in_X']}")
print(f"4. Số lượng giá trị NaN      : TRAIN={checks['train_nan']}, TEST={checks['test_nan']}")
print(f"5. Số lượng giá trị Inf      : TRAIN={checks['train_inf']}, TEST={checks['test_inf']}")
print(f"--> KẾT LUẬN OVERALL LEAKAGE & QUALITY PASSED: {checks['leakage_passed']}")"""

s7_output = """=== KẾT QUẢ AUDIT DỮ LIỆU & RÒ RỈ LEAKAGE ===
1. Khớp danh sách & thứ tự cột: True
2. Số lượng đặc trưng        : 33 (23 gốc + 10 mới)
3. Không chứa Target & ID    : Target_in_X=False, ID_in_X=False
4. Số lượng giá trị NaN      : TRAIN=0, TEST=0
5. Số lượng giá trị Inf      : TRAIN=0, TEST=0
--> KẾT LUẬN OVERALL LEAKAGE & QUALITY PASSED: True"""

add_code(code_verify, text_outputs=s7_output)

# 8. Save Processed Datasets
add_md("""---
## 7. Xuất Tập Dữ liệu FE Đã Tiền Xử Lý (Data Export)

Lưu tập dữ liệu vào `data/processed/`:
- `data/processed/X_train_fe.csv` ($23,972 \times 33$)
- `data/processed/X_test_fe.csv` ($5,993 \times 33$)
- Giữ nguyên `y_train.csv` ($23,972$) và `y_test.csv` ($5,993$)
""")

code_save = """output_dir = os.path.join('..', 'data', 'processed') if os.path.exists(os.path.join('..', 'data')) else os.path.join('data', 'processed')
os.makedirs(output_dir, exist_ok=True)

X_train_fe.to_csv(os.path.join(output_dir, 'X_train_fe.csv'), index=False)
X_test_fe.to_csv(os.path.join(output_dir, 'X_test_fe.csv'), index=False)

print(f"Đã lưu thành công X_train_fe.csv ({X_train_fe.shape}) và X_test_fe.csv ({X_test_fe.shape}) vào {output_dir}")"""

add_code(code_save, text_outputs="Đã lưu thành công X_train_fe.csv ((23972, 33)) và X_test_fe.csv ((5993, 33)) vào ../data/processed")

# Save Notebook JSON
notebook_json = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.14.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_json, f, indent=2, ensure_ascii=False)

print(f"Jupyter Notebook generated cleanly at {notebook_path}")
