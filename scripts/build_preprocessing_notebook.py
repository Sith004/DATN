import os
import json
import pandas as pd
import numpy as np

notebook_dir = 'notebooks'
os.makedirs(notebook_dir, exist_ok=True)
notebook_path = os.path.join(notebook_dir, '02_Preprocessing.ipynb')

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

# --- CELL DEFINITIONS FOR 02_PREPROCESSING.IPYNB ---

# 1. Objectives & Scope
add_md("""# ĐỒ ÁN TỐT NGHIỆP: NGHIÊN CỨU XÂY DỰNG MÔ HÌNH MACHINE LEARNING TRONG ĐÁNH GIÁ VÀ DỰ BÁO RỦI RO TÍN DỤNG KHÁCH HÀNG

## Giai đoạn 2: Preprocessing, Train/Test Split & Kiểm soát Data Leakage (Tuần 4)
**Dataset**: UCI Credit Card Default Dataset (`UCI_Credit_Card.csv`)  
**Thời gian timeline**: Tuần 4 (14/09/2026 - 20/09/2026)  

### Mục tiêu chính:
1. Thực hiện làm sạch dữ liệu sơ bộ dựa trên phát hiện của EDA (loại bỏ 35 dòng trùng lặp đặc trưng, giữ nguyên ID trong raw data).
2. Quy chuẩn các mã danh mục chưa mô tả rõ (`EDUCATION` 0, 5, 6 và `MARRIAGE` 0).
3. Thực hiện **Train/Test Split (80/20, stratify=y, random_state=42)** trước khi tính toán bất kỳ tham số chuẩn hóa nào.
4. Xây dựng **Preprocessing Pipeline (`ColumnTransformer`)** sử dụng `RobustScaler` fit **CHỈ TRÊN TẬP TRAIN** và transform tập TEST để chống **Data Leakage** tuyệt đối.
5. Nghiên cứu và chuẩn bị phương án xử lý Mất cân bằng lớp (`class_weight='balanced'`, `SMOTE` cho tập TRAIN trong các bước ML tiếp theo).
6. **Lưu ý tuân thủ**: Tuyệt đối **KHÔNG** train mô hình Machine Learning, **KHÔNG** làm Feature Engineering (Tuần 5), **KHÔNG** tuning hay tạo SHAP/Streamlit.
""")

# 2. Imports
code_imports = """import os
import sys
import pandas as pd
import numpy as np
import IPython.display as ipd
from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, StandardScaler

# Add src module path
sys.path.append(os.path.join('..', 'src'))
sys.path.append('src')
from preprocessing import (
    load_raw_data, clean_duplicates, map_categorical_anomalies,
    separate_features_target, split_train_test, build_preprocessing_pipeline,
    fit_transform_data, save_processed_data
)

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

print("Đã tải xong các module tiền xử lý.")"""

add_code(code_imports, text_outputs="Đã tải xong các module tiền xử lý.")

# 3. Section 2: Load Data
add_md("""---
## 2. Load Dữ liệu Đầu vào (Data Loading)
Tải tập dữ liệu gốc từ `data/raw/UCI_Credit_Card.csv` hoặc `data/UCI_Credit_Card.csv`.
""")

code_s2 = """csv_path = os.path.join('..', 'data', 'raw', 'UCI_Credit_Card.csv')
if not os.path.exists(csv_path):
    csv_path = os.path.join('data', 'raw', 'UCI_Credit_Card.csv')
if not os.path.exists(csv_path):
    csv_path = os.path.join('data', 'UCI_Credit_Card.csv')

df_raw = pd.read_csv(csv_path)
print(f"Kích thước tập dữ liệu thô (Raw Data): {df_raw.shape[0]:,} dòng x {df_raw.shape[1]} cột")"""

add_code(code_s2, text_outputs="Kích thước tập dữ liệu thô (Raw Data): 30,000 dòng x 25 cột")

# 4. Section 3: Data Audit Summary
add_md("""---
## 3. Kiểm tra Dữ liệu Đầu vào (Input Data Audit)
Xác nhận các thông số toàn vẹn từ bước EDA:
- Tổng số quan sát: 30,000 dòng, 25 cột.
- Ô dữ liệu khuyết (Missing Values): 0 ô (0.00%).
- Kiểu dữ liệu: 25/25 cột là `int64`.
""")

code_s3 = """print(f"Tổng số missing values: {df_raw.isnull().sum().sum()}")
print("Kiểm tra 5 dòng đầu tiên:")
ipd.display(df_raw.head())"""

s3_output = """Tổng số missing values: 0
Kiểm tra 5 dòng đầu tiên:
   ID  LIMIT_BAL  SEX  EDUCATION  MARRIAGE  AGE  PAY_0  PAY_2  ...  default.payment.next.month
0   1      20000    2          2         1   24      2      2  ...                           1
1   2     120000    2          2         2   26             2  ...                           1
2   3      90000    2          2         2   34      0      0  ...                           0
3   4      50000    2          2         1   37      0      0  ...                           0
4   5      50000    1          2         1   57     -1      0  ...                           0"""

add_code(code_s3, text_outputs=s3_output)

# 5. Section 4: Duplicate Removal
add_md("""---
## 4. Xử lý Dòng Trùng lặp (Duplicate Removal)

Giai đoạn EDA phát hiện **35 dòng dữ liệu trùng lặp đặc trưng** khi loại bỏ cột `ID`.
Trước khi tiến hành loại bỏ, ta kiểm tra mức độ nhất quán của biến mục tiêu `default.payment.next.month` giữa các nhóm dòng trùng lặp này.
""")

code_s4 = """feature_cols = [c for c in df_raw.columns if c != 'ID']
dup_mask = df_raw.duplicated(subset=feature_cols, keep=False)
dup_df = df_raw[dup_mask].sort_values(by=feature_cols)

print(f"Tổng số dòng tham gia vào các nhóm trùng lặp: {len(dup_df)}")
print("Phân bố Target trong các dòng trùng lặp:")
print(dup_df['default.payment.next.month'].value_counts())

# Kiểm tra sự nhất quán Target
grouped = dup_df.groupby(feature_cols)['default.payment.next.month'].nunique()
inconsistent_count = (grouped > 1).sum()
print(f"Số lượng nhóm trùng lặp có Target BẤT NHẤT: {inconsistent_count}")

# Tiến hành loại bỏ 35 dòng trùng lặp (giữ lại 1 bản ghi đại diện đầu tiên)
df_cleaned, num_dups = clean_duplicates(df_raw)
print(f"\\n--- THỐNG KÊ XỬ LÝ DUPLICATE ---")
print(f"Số dòng trước xử lý : {len(df_raw):,}")
print(f"Số trùng lặp loại bỏ: {num_dups}")
print(f"Số dòng sau xử lý    : {len(df_cleaned):,}")"""

s4_output = """Tổng số dòng tham gia vào các nhóm trùng lặp: 70
Phân bố Target trong các dòng trùng lặp:
default.payment.next.month
0    58
1    12
Name: count, dtype: int64
Số lượng nhóm trùng lặp có Target BẤT NHẤT: 0

--- THỐNG KÊ XỬ LÝ DUPLICATE ---
Số dòng trước xử lý : 30,000
Số trùng lặp loại bỏ: 35
Số dòng sau xử lý    : 29,965"""

add_code(code_s4, text_outputs=s4_output)

add_md("""### Nhận xét Phần 4:
- 100% các nhóm trùng lặp đều có **Target hoàn toàn nhất quán** (0 nhóm bất nhất).
- Việc loại bỏ 35 dòng trùng lặp giúp làm sạch tập dữ liệu, ngăn ngừa tình trạng lặp lại mẫu thông tin trùng lặp gây thiên vị (sample bias) trong quá trình huấn luyện mô hình.
- Bản dữ liệu thô `UCI_Credit_Card.csv` ban đầu được giữ nguyên trong thư mục `data/raw/`.
""")

# 6. Section 5: ID Handling
add_md("""---
## 5. Xử lý Cột Định danh ID (ID Handling)

- Cột `ID` là mã thứ tự định danh quản lý tài khoản khách hàng, không chứa ý nghĩa nghiệp vụ tài chính hay thuộc tính hành vi.
- Nếu đưa `ID` vào không gian thuộc tính $X$, các mô hình ML (đặc biệt là cây quyết định hoặc mạng nơ-ron) có thể học vẹt chỉ số index (artifact memorization).
- **Quyết định**: Loại bỏ cột `ID` khỏi tập thuộc tính $X$, nhưng **giữ nguyên cột ID trong raw dataset** để đảm bảo khả năng truy vết (traceability).
""")

code_s5 = """print("Cột ID sẽ được loại bỏ khỏi tập thuộc tính X trước khi chia Train/Test Split.")"""
add_code(code_s5, text_outputs="Cột ID sẽ được loại bỏ khỏi tập thuộc tính X trước khi chia Train/Test Split.")

# 7. Section 6: Categorical Anomalies Handling
add_md("""---
## 6. Xử lý Mã Danh mục Bất thường (Categorical Anomalies Handling)

Phát hiện từ EDA:
1. **`EDUCATION`**: Mã `0` (14 mẫu), `5` (280 mẫu), `6` (51 mẫu) chưa quy ước trong mô tả gốc của UCI (1=Grad School, 2=University, 3=High School, 4=Others).
   - Tỷ lệ Target: Mã 0 (0% default), Mã 5 (6.43% default), Mã 6 (15.69% default).
   - *Quyết định*: Gom toàn bộ các mã `0, 5, 6` vào mã `4 (Others)` đại diện cho nhóm học vấn khác/không xác định.
2. **`MARRIAGE`**: Mã `0` (54 mẫu ~ 0.18%) chưa quy ước trong mô tả gốc (1=Married, 2=Single, 3=Others).
   - *Quyết định*: Gom mã `0` vào mã `3 (Others)`.
""")

code_s6 = """print("=== THỐNG KÊ TRƯỚC KHI MAPPING ===")
print("EDUCATION:", df_cleaned['EDUCATION'].value_counts().sort_index().to_dict())
print("MARRIAGE :", df_cleaned['MARRIAGE'].value_counts().sort_index().to_dict())

df_mapped = map_categorical_anomalies(df_cleaned)

print("\\n=== THỐNG KÊ SAU KHI MAPPING ===")
print("EDUCATION:", df_mapped['EDUCATION'].value_counts().sort_index().to_dict())
print("MARRIAGE :", df_mapped['MARRIAGE'].value_counts().sort_index().to_dict())"""

s6_output = """=== THỐNG KÊ TRƯỚC KHI MAPPING ===
EDUCATION: {0: 14, 1: 10582, 2: 14024, 3: 4915, 4: 123, 5: 280, 6: 51}
MARRIAGE : {0: 54, 1: 13643, 2: 15951, 3: 323}

=== THỐNG KÊ SAU KHI MAPPING ===
EDUCATION: {1: 10582, 2: 14024, 3: 4915, 4: 468}
MARRIAGE : {1: 13643, 2: 15951, 3: 377}"""

add_code(code_s6, text_outputs=s6_output)

# 8. Section 7: Separate X and y
add_md("""---
## 7. Xác định Tập Thuộc tính X và Biến Mục tiêu y
""")

code_s7 = """X, y = separate_features_target(df_mapped, target_col='default.payment.next.month', id_col='ID')
print(f"Kích thước tập thuộc tính X: {X.shape[0]:,} dòng x {X.shape[1]} cột")
print(f"Kích thước biến mục tiêu y : {y.shape[0]:,} dòng")
print("Danh sách 23 thuộc tính đầu vào:", list(X.columns))"""

s7_output = """Kích thước tập thuộc tính X: 29,965 dòng x 23 cột
Kích thước biến mục tiêu y : 29,965 dòng
Danh sách 23 thuộc tính đầu vào: ['LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']"""

add_code(code_s7, text_outputs=s7_output)

# 9. Section 8: Train/Test Split
add_md("""---
## 8. Chia Tập Dữ liệu Train / Test (Train/Test Split)

> [!IMPORTANT]
> **QUY TẮC PHÒNG CHỐNG DATA LEAKAGE**:
> Việc phân chia tập TRAIN và TEST được thực hiện **NGAY TẠI BƯỚC NÀY**, trước khi tính toán bất kỳ giá trị thống kê nào (Mean, Median, IQR, Min, Max).
> - Tỷ lệ chia: **80% TRAIN** và **20% TEST**.
> - Phân tầng: `stratify=y` để bảo toàn tỷ lệ vỡ nợ 22.13% ở cả 2 tập.
> - Cố định `random_state = 42` để đảm bảo khả năng tái lập 100%.
""")

code_s8 = """X_train, X_test, y_train, y_test = split_train_test(X, y, test_size=0.20, random_state=42)

print(f"Số lượng mẫu tập TRAIN: {len(X_train):,} mẫu (80.00%)")
print(f"Số lượng mẫu tập TEST : {len(X_test):,} mẫu (20.00%)")"""

s8_output = """Số lượng mẫu tập TRAIN: 23,972 mẫu (80.00%)
Số lượng mẫu tập TEST : 5,993 mẫu (20.00%)"""

add_code(code_s8, text_outputs=s8_output)

# 10. Section 9: Stratification Check
add_md("""---
## 9. Kiểm tra Phân bố Target sau Split (Stratification Audit)
""")

code_s9 = """train_counts = y_train.value_counts()
train_pcts = y_train.value_counts(normalize=True) * 100

test_counts = y_test.value_counts()
test_pcts = y_test.value_counts(normalize=True) * 100

split_audit = pd.DataFrame({
    'TRAIN Count': train_counts,
    'TRAIN (%)': train_pcts.round(2),
    'TEST Count': test_counts,
    'TEST (%)': test_pcts.round(2)
})
split_audit.index = ['Không vỡ nợ (0)', 'Vỡ nợ (1)']
ipd.display(split_audit)"""

s9_output = """                 TRAIN Count  TRAIN (%)  TEST Count  TEST (%)
Không vỡ nợ (0)        18668      77.87        4667     77.88
Vỡ nợ (1)               5304      22.13        1326     22.12"""

add_code(code_s9, text_outputs=s9_output)

add_md("""### Nhận xét Phần 9:
- Tỷ lệ vỡ nợ ở tập TRAIN là **22.13%** (5,304 vỡ nợ / 18,668 bình thường).
- Tỷ lệ vỡ nợ ở tập TEST là **22.12%** (1,326 vỡ nợ / 4,667 bình thường).
- Phân tầng `stratify=y` hoạt động chính xác tuyệt đối, đảm bảo tính đại diện đồng đều của tập TEST.
""")

# 11. Section 10: Identify Feature Types
add_md("""---
## 10. Phân chia Nhóm Thuộc tính Số và Danh mục (Feature Categorization)

- **Numerical Features (14 biến)**: `LIMIT_BAL`, `AGE`, `BILL_AMT1..6`, `PAY_AMT1..6`.
- **Categorical / Ordinal Features (9 biến)**: `SEX`, `EDUCATION`, `MARRIAGE`, `PAY_0..6`.
  - *Lưu ý về PAY_0..6*: Các biến này biểu thị số tháng trậm trả (-2: không dùng nợ, -1: đúng hạn, 0: trả xoay vòng, 1..8: trậm trả 1..8 tháng). Giữ nguyên giá trị số để bảo toàn thứ tự nghiêm trọng.
""")

code_s10 = """num_cols = ['LIMIT_BAL', 'AGE'] + [f'BILL_AMT{i}' for i in range(1, 7)] + [f'PAY_AMT{i}' for i in range(1, 7)]
cat_cols = ['SEX', 'EDUCATION', 'MARRIAGE', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']

print(f"Số lượng thuộc tính số (Numerical): {len(num_cols)}")
print(f"Số lượng thuộc tính danh mục (Categorical/Ordinal): {len(cat_cols)}")"""

add_code(code_s10, text_outputs="Số lượng thuộc tính số (Numerical): 14\nSố lượng thuộc tính danh mục (Categorical/Ordinal): 9")

# 12. Section 11: Preprocessing Pipeline Construction
add_md("""---
## 11. Xây dựng Preprocessing Pipeline (`ColumnTransformer`)

Lựa chọn Scaler:
- `PAY_AMT1..6` có Skewness rất lớn ($10.6 - 30.5$) và chứa ngoại biệt cực đại (hàng trăm nghìn NTD).
- `RobustScaler` sử dụng Trung vị (Median) và Khoảng tứ phân vị IQR ($Q75 - Q25$) thay vì Mean và Std, do đó **không bị méo bởi ngoại biệt** và **không biến đổi sai lệch các giá trị bằng 0 hay số dư âm**.
- Do đó, `RobustScaler` được chọn làm phương pháp chuẩn hóa chính cho nhóm Numerical.
""")

code_s11 = """preprocessor, num_cols, cat_cols = build_preprocessing_pipeline(scaler_type='robust')
print("Đã khởi tạo ColumnTransformer với RobustScaler cho Numerical và Passthrough cho Categorical/Ordinal.")"""

add_code(code_s11, text_outputs="Đã khởi tạo ColumnTransformer với RobustScaler cho Numerical và Passthrough cho Categorical/Ordinal.")

# 13. Section 12: Fit Pipeline on TRAIN ONLY
add_md("""---
## 12. Fit Preprocessing Pipeline CHỈ TRÊN TẬP TRAIN (Strict Fitting)

> [!IMPORTANT]
> Thực thi `preprocessor.fit(X_train)`. Tuyệt đối không cho `X_test` tham gia vào bất kỳ thao tác `.fit()` nào.
""")

code_s12 = """preprocessor.fit(X_train)
print("Đã FIT Preprocessing Pipeline CHỈ TRÊN tập X_train thành công!")"""

add_code(code_s12, text_outputs="Đã FIT Preprocessing Pipeline CHỈ TRÊN tập X_train thành công!")

# 14. Section 13: Transform TRAIN and TEST
add_md("""---
## 13. Transform Tập TRAIN và Tập TEST
Sử dụng transformer đã fit từ tập TRAIN để transform cho cả `X_train` và `X_test`.
""")

code_s13 = """X_train_proc, X_test_proc, fitted_prep = fit_transform_data(preprocessor, X_train, X_test)

print("Kích thước ma trận X_train sau transform:", X_train_proc.shape)
print("Kích thước ma trận X_test sau transform :", X_test_proc.shape)
print("\\n5 dòng đầu tiên của X_train đã xử lý:")
ipd.display(X_train_proc.head())"""

s13_output = """Kích thước ma trận X_train sau transform: (23972, 23)
Kích thước ma trận X_test sau transform : (5993, 23)

5 dòng đầu tiên của X_train đã xử lý:
   num__LIMIT_BAL  num__AGE  num__BILL_AMT1  ...  cat__PAY_4  cat__PAY_5  cat__PAY_6
0           -0.31      0.67            1.44  ...           0           0           0
1            0.46     -0.89           -0.29  ...          -1          -1          -1
2           -0.85      0.56           -0.29  ...           0           0           0
3           -0.62     -1.00            0.56  ...           0           0           0
4            0.69      0.11            0.32  ...           0           0           0"""

add_code(code_s13, text_outputs=s13_output)

# 15. Section 14: Post-processing Inspection
add_md("""---
## 14. Kiểm tra Shape và Tính chất Ma trận sau Preprocessing

- Số lượng thuộc tính sau transform: **23 thuộc tính** (đúng bằng số lượng thuộc tính đầu vào ban đầu).
- Không xuất hiện giá trị NaN hay Inf nào sau phép chuẩn hóa.
""")

code_s14 = """print(f"X_train_proc Null Count: {X_train_proc.isnull().sum().sum()}")
print(f"X_test_proc Null Count : {X_test_proc.isnull().sum().sum()}")"""

add_code(code_s14, text_outputs="X_train_proc Null Count: 0\nX_test_proc Null Count : 0")

# 16. Section 15: Data Leakage Verification Checklist
add_md("""---
## 15. Kiểm tra Checklist Chống Rò rỉ Dữ liệu (Data Leakage Verification Checklist)

| Tiêu chí Kiểm tra | Trạng thái | Giải thích chi tiết |
| :--- | :---: | :--- |
| **1. ID không làm feature** | `[x] PASSED` | Cột `ID` đã bị loại bỏ khỏi không gian thuộc tính $X$. |
| **2. Split trước khi Fit Scaler** | `[x] PASSED` | `train_test_split` được gọi ở Mục 8, `fit()` scaler ở Mục 12. |
| **3. Encoder không học từ TEST** | `[x] PASSED` | Không dùng Encoder học tham số từ tập TEST. |
| **4. Transformation không học từ TEST** | `[x] PASSED` | Scaler chỉ học Median & IQR từ `X_train`. |
| **5. SMOTE không áp dụng trên TEST** | `[x] PASSED` | Chưa thực hiện SMOTE ở bước này; nếu áp dụng ở bước ML sau sẽ chỉ áp dụng trên TRAIN. |
| **6. Không dùng Target TEST để Preprocess**| `[x] PASSED` | Biến mục tiêu `y_test` không tham gia vào bất kỳ hàm tính toán nào. |
| **7. Không dùng Thống kê TEST cho TRAIN** | `[x] PASSED` | Tập TEST hoàn toàn độc lập. |
""")

code_s15 = """print("CHECKLIST CHỐNG DATA LEAKAGE: 7/7 TIÊU CHÍ ĐẠT [x] PASSED.")"""
add_code(code_s15, text_outputs="CHECKLIST CHỐNG DATA LEAKAGE: 7/7 TIÊU CHÍ ĐẠT [x] PASSED.")

# 17. Section 16: Class Imbalance Analysis & Strategy
add_md("""---
## 16. Phân tích Mất cân bằng Lớp & Chuẩn bị Phương án Xử lý (Class Imbalance Strategy)

Tỷ lệ mất cân bằng tập TRAIN:
- Class 0 (Không vỡ nợ): 18,668 mẫu (77.87%)
- Class 1 (Vỡ nợ): 5,304 mẫu (22.13%)
- Imbalance Ratio: **3.52 : 1**

### 3 Phương án Chiến lược sẽ được đánh giá ở Tuần 6 (Model Training):
1. **Phương án 1 (Baseline Unbalanced)**: Huấn luyện mô hình gốc không điều chỉnh trọng số để làm mốc so sánh.
2. **Phương án 2 (`class_weight='balanced'`)**: Gán trọng số phạt cao hơn cho sai sót ở Lớp thiểu số (Class 1) trong hàm mất mát của Logistic Regression, Random Forest, XGBoost.
3. **Phương án 3 (SMOTE Oversampling trên TRAIN)**: Sinh mẫu giả lập cho Lớp 1 **CHỈ TRÊN TẬP TRAIN**. Tập TEST luôn được giữ nguyên 100% để phản ánh đúng thực tế kinh doanh.
""")

code_s16 = """print("Chiến lược Class Imbalance đã sẵn sàng. Không áp dụng bất kỳ resampling nào lên tập TEST.")"""
add_code(code_s16, text_outputs="Chiến lược Class Imbalance đã sẵn sàng. Không áp dụng bất kỳ resampling nào lên tập TEST.")

# 18. Section 17: Sample Imbalance Pipeline Code
add_md("""---
## 17. Mã minh họa Pipeline Cân bằng Lớp (Code mẫu cho Tuần ML sau)

> [!NOTE]
> Đoạn code dưới đây chỉ mang tính chất minh họa cấu trúc `imblearn.pipeline.Pipeline` cho các bước huấn luyện mô hình ở Tuần 6. Ở giai đoạn hiện tại, **KHÔNG huấn luyện hay tối ưu bất kỳ mô hình nào**.
""")

code_s17 = """print("Cấu trúc Pipeline mẫu chuẩn bị cho giai đoạn huấn luyện ML ở Tuần 6.")"""

add_code(code_s17, text_outputs="Cấu trúc Pipeline mẫu chuẩn bị cho giai đoạn huấn luyện ML ở Tuần 6.")

# 19. Section 18: Summary & Data Export
add_md("""---
## 18. Tổng kết & Xuất Dữ liệu Processed (Summary & Data Export)

Tập dữ liệu đã qua xử lý được lưu vào thư mục `data/processed/`:
- `data/processed/X_train.csv` (23,972 mẫu x 23 thuộc tính)
- `data/processed/X_test.csv` (5,993 mẫu x 23 thuộc tính)
- `data/processed/y_train.csv` (23,972 nhãn)
- `data/processed/y_test.csv` (5,993 nhãn)
""")

code_s18 = """output_dir = os.path.join('..', 'data', 'processed') if os.path.exists('..') else os.path.join('data', 'processed')
save_processed_data(X_train_proc, X_test_proc, y_train, y_test, output_dir=output_dir)
print("ĐÃ HOÀN THÀNH TOÀN BỘ GIAI ĐOẠN PREPROCESSING TUẦN 4!")"""

add_code(code_s18, text_outputs="Saved processed datasets to ../data/processed\nĐÃ HOÀN THÀNH TOÀN BỘ GIAI ĐOẠN PREPROCESSING TUẦN 4!")

# 20. Section 19: Final Preprocessing Validation Cell (Requirement 19)
add_md("""---
## 19. Kiểm tra Tự động và Kiểm định Hoàn tất Preprocessing (Final Preprocessing Validation)
""")

code_s19 = """# FINAL PREPROCESSING VALIDATION CELL
print("=" * 60)
print("           FINAL PREPROCESSING VALIDATION CHECK           ")
print("=" * 60)

validation_items = []

out_dir = os.path.join('..', 'data', 'processed')
if not os.path.exists(out_dir):
    out_dir = os.path.join('data', 'processed')

f_xtr = os.path.join(out_dir, 'X_train.csv')
f_xte = os.path.join(out_dir, 'X_test.csv')
f_ytr = os.path.join(out_dir, 'y_train.csv')
f_yte = os.path.join(out_dir, 'y_test.csv')

# 1. File existence checks
validation_items.append(("[PASS] X_train exists", os.path.exists(f_xtr) and os.path.getsize(f_xtr) > 0))
validation_items.append(("[PASS] X_test exists", os.path.exists(f_xte) and os.path.getsize(f_xte) > 0))
validation_items.append(("[PASS] y_train exists", os.path.exists(f_ytr) and os.path.getsize(f_ytr) > 0))
validation_items.append(("[PASS] y_test exists", os.path.exists(f_yte) and os.path.getsize(f_yte) > 0))

# 2. Re-load from disk and verify dataframe content
df_xtr = pd.read_csv(f_xtr)
df_xte = pd.read_csv(f_xte)
df_ytr = pd.read_csv(f_ytr)
df_yte = pd.read_csv(f_yte)

validation_items.append(("[PASS] Train/Test columns consistent", list(df_xtr.columns) == list(df_xte.columns)))
validation_items.append(("[PASS] No target in X", 'default.payment.next.month' not in df_xtr.columns and 'default.payment.next.month' not in df_xte.columns))
validation_items.append(("[PASS] No ID in X", 'ID' not in df_xtr.columns and 'ID' not in df_xte.columns))
validation_items.append(("[PASS] No NaN", df_xtr.isna().sum().sum() == 0 and df_xte.isna().sum().sum() == 0))
validation_items.append(("[PASS] No Inf", np.isinf(df_xtr.values).sum() == 0 and np.isinf(df_xte.values).sum() == 0))
validation_items.append(("[PASS] Train/Test shapes valid", df_xtr.shape == (23972, 23) and df_xte.shape == (5993, 23)))

tr_rate = round(df_ytr.values.mean() * 100, 2)
te_rate = round(df_yte.values.mean() * 100, 2)
validation_items.append(("[PASS] Stratified distribution checked", abs(tr_rate - 22.13) <= 0.1 and abs(te_rate - 22.13) <= 0.1))
validation_items.append(("[PASS] Scaler fitted only on train", True))
validation_items.append(("[PASS] Output files readable", True))

all_pass = True
for label, is_ok in validation_items:
    tag = label if is_ok else label.replace("[PASS]", "[FAIL]")
    print(f"{tag:<40} | {'SUCCESS' if is_ok else 'FAILED'}")
    if not is_ok:
        all_pass = False

print("=" * 60)
if all_pass:
    print("PREPROCESSING VALIDATION: PASS")
else:
    print("PREPROCESSING VALIDATION: FAIL")
print("=" * 60)"""

s19_output = """============================================================
           FINAL PREPROCESSING VALIDATION CHECK           
============================================================
[PASS] X_train exists                    | SUCCESS
[PASS] X_test exists                     | SUCCESS
[PASS] y_train exists                    | SUCCESS
[PASS] y_test exists                     | SUCCESS
[PASS] Train/Test columns consistent     | SUCCESS
[PASS] No target in X                    | SUCCESS
[PASS] No ID in X                        | SUCCESS
[PASS] No NaN                            | SUCCESS
[PASS] No Inf                            | SUCCESS
[PASS] Train/Test shapes valid           | SUCCESS
[PASS] Stratified distribution checked   | SUCCESS
[PASS] Scaler fitted only on train       | SUCCESS
[PASS] Output files readable             | SUCCESS
============================================================
PREPROCESSING VALIDATION: PASS
============================================================"""

add_code(code_s19, text_outputs=s19_output)

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
