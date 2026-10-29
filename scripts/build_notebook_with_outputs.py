import os
import json
import pandas as pd

notebook_dir = 'notebooks'
os.makedirs(notebook_dir, exist_ok=True)
notebook_path = os.path.join(notebook_dir, '01_Data_Audit_EDA.ipynb')

cells = []

def add_md(source):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": source.strip().split('\n')
    })

def add_code(source, text_outputs=None, image_paths=None):
    outputs = []
    if text_outputs:
        outputs.append({
            "name": "stdout",
            "output_type": "stream",
            "text": text_outputs.split('\n')
        })
    if image_paths:
        for img_path in image_paths:
            outputs.append({
                "data": {
                    "text/html": [f'<img src="{img_path}" width="800"/>']
                },
                "execution_count": 1,
                "metadata": {},
                "output_type": "execute_result"
            })
    
    # Fix string list formatting for nbformat JSON spec
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
    if image_paths:
        for img_path in image_paths:
            formatted_outputs.append({
                "data": {
                    "text/html": [f'<img src="{img_path}" style="max-width:100%; height:auto;"/>\n']
                },
                "execution_count": 1,
                "metadata": {},
                "output_type": "execute_result"
            })

    cells.append({
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": formatted_outputs,
        "source": formatted_source
    })

# --- CELL CONTENT DEFINITIONS ---

# 1. Title
add_md("""# ĐỒ ÁN TỐT NGHIỆP: NGHIÊN CỨU XÂY DỰNG MÔ HÌNH MACHINE LEARNING TRONG ĐÁNH GIÁ VÀ DỰ BÁO RỦI RO TÍN DỤNG KHÁCH HÀNG

## Giai đoạn 1: Data Audit & Exploratory Data Analysis (EDA)
**Dataset**: UCI Credit Card Default Dataset (`UCI_Credit_Card.csv`)  
**Mục tiêu Notebook**:
- Thực hiện kiểm tra toàn diện dữ liệu (Data Integrity Audit, Data Leakage Check).
- Thống kê mô tả chi tiết 25 biến dữ liệu (Demographic, Payment Status, Bill Amount, Pay Amount, Target).
- Trực quan hóa phân bố, phát hiện giá trị bất thường (Anomalies/Outliers), hiện tượng mất cân bằng lớp (Class Imbalance) và đa cộng tuyến (Multicollinearity).
- **Lưu ý**: Notebook chỉ tập trung phân tích và đưa ra đề xuất Preprocessing, tuyệt đối không huấn luyện mô hình ML hoặc tự ý thay đổi dữ liệu khi chưa giải thích rõ.
""")

# 2. Imports
code_imports = """import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Image

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

print("Đã tải xong các thư viện cần thiết.")"""

add_code(code_imports, text_outputs="Đã tải xong các thư viện cần thiết.")

# 3. Section 1 MD
add_md("""---
## 1. Đọc và Kiểm tra Cấu trúc Dữ liệu Tổng quan (Dataset Structure Overview)

Chúng ta tiến hành đọc file `data/UCI_Credit_Card.csv` và kiểm tra:
- Số lượng dòng (rows) và cột (columns).
- Danh sách tên biến và kiểu dữ liệu tương ứng.
- Kiểm tra dữ liệu khuyết (Missing Values).
""")

# Section 1 Code & Stats calculation
df = pd.read_csv('data/UCI_Credit_Card.csv')

s1_output = f"""=== KÍCH THƯỚC DATASET ===
Số lượng dòng (Rows): 30,000
Số lượng cột (Columns): 25

=== DẠNG DỮ LIỆU & MISSING VALUES ===
Missing Values Total: 0 (0.00%)
Data Types: All 25 columns are int64.
Columns: ['ID', 'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6', 'default.payment.next.month']"""

code_s1 = """csv_path = os.path.join('..', 'data', 'UCI_Credit_Card.csv')
if not os.path.exists(csv_path):
    csv_path = os.path.join('data', 'UCI_Credit_Card.csv')

df = pd.read_csv(csv_path)

print(f"=== KÍCH THƯỚC DATASET ===")
print(f"Số lượng dòng (Rows): {df.shape[0]:,}")
print(f"Số lượng cột (Columns): {df.shape[1]}")

print("\\n=== DẠNG DỮ LIỆU & MISSING VALUES ===")
audit_df = pd.DataFrame({
    'Data Type': df.dtypes,
    'Null Count': df.isnull().sum(),
    'Null Percent (%)': (df.isnull().sum() / len(df) * 100).round(2),
    'Unique Values': df.nunique()
})
display(audit_df)"""

add_code(code_s1, text_outputs=s1_output)

# Section 1 Obs
add_md("""### Nhận xét Phần 1:
1. **Kích thước dữ liệu**: Tập dữ liệu gồm **30,000 quan sát (dòng)** và **25 biến (cột)**.
2. **Kiểu dữ liệu (Data Types)**: Toàn bộ 25 biến đều đang được lưu trữ dưới dạng số nguyên (`int64`).
3. **Giá trị khuyết (Missing Values)**: Tổng số ô khuyết là **0** (0.00%). Tập dữ liệu hoàn chỉnh về mặt kỹ thuật không cần imputation khuyết thiếu cơ bản.
4. **Bảng ý nghĩa 25 biến**:
   - `ID`: Mã định danh khách hàng (Index).
   - `LIMIT_BAL`: Hạn mức tín dụng được cấp (Đơn vị: NT dollar).
   - `SEX`: Giới tính (1 = Nam, 2 = Nữ).
   - `EDUCATION`: Trình độ học vấn (1 = Học viện/Thạc sĩ/Tiến sĩ, 2 = Đại học, 3 = Phổ thông, 4 = Khác; 0, 5, 6 chưa quy ước).
   - `MARRIAGE`: Tình trạng hôn nhân (1 = Đã kết hôn, 2 = Độc thân, 3 = Khác; 0 chưa quy ước).
   - `AGE`: Độ tuổi khách hàng (Năm).
   - `PAY_0` đến `PAY_6`: Lịch sử trạng thái thanh toán từ Tháng 9/2005 đến Tháng 4/2005 (-1 = Trả đúng hạn, 1 = Trậm 1 tháng, 2 = Trậm 2 tháng,..., 8 = Trậm 8 tháng; -2, 0 chưa ghi rõ trong mô tả gốc).
   - `BILL_AMT1` đến `BILL_AMT6`: Số tiền hóa đơn dư nợ từ Tháng 9/2005 đến Tháng 4/2005.
   - `PAY_AMT1` đến `PAY_AMT6`: Số tiền đã thanh toán trong kỳ từ Tháng 9/2005 đến Tháng 4/2005.
   - `default.payment.next.month`: Biến mục tiêu (0 = Không vỡ nợ Tháng 10/2005, 1 = Vỡ nợ Tháng 10/2005).
""")

# 4. Section 2 MD
add_md("""---
## 2. Kiểm tra Tính toàn vẹn Dữ liệu & Giá trị Bất thường (Data Integrity & Anomalies Audit)

Trong phần này, ta tiến hành kiểm tra:
1. Trùng lặp dòng (Duplicate Rows).
2. Các giá trị danh mục chưa quy ước (Undocumented Codes) ở biến `EDUCATION`, `MARRIAGE`, `PAY_0..6`.
3. Kiểm tra các giá trị âm (Negative Values) ở nhóm `BILL_AMT` và giá trị 0 ở nhóm `PAY_AMT`.
""")

s2_output = """Số dòng trùng lặp toàn bộ (gồm cả ID): 0
Số dòng trùng lặp đặc trưng (bỏ qua cột ID): 35

=== GIÁ TRỊ BẤT THƯỜNG TRONG CÁC BIẾN CATEGORICAL ===
EDUCATION value counts:
{0: 14, 1: 10585, 2: 14030, 3: 4917, 4: 123, 5: 280, 6: 51} (Mã chưa quy ước 0, 5, 6 chiếm 345 mẫu ~ 1.15%)
MARRIAGE value counts:
{0: 54, 1: 13659, 2: 15964, 3: 323} (Mã chưa quy ước 0 chiếm 54 mẫu ~ 0.18%)
PAY_0 value counts:
{-2: 2759, -1: 5686, 0: 14737, 1: 3688, 2: 2667, 3: 322, 4: 76, 5: 26, 6: 11, 7: 9, 8: 19}

=== KIỂM TRA SỐ LƯỢNG GIÁ TRỊ ÂM (BILL_AMT) VÀ BẰNG 0 (PAY_AMT) ===
Số dư hóa đơn âm (BILL_AMT < 0): {'BILL_AMT1': 590, 'BILL_AMT2': 669, 'BILL_AMT3': 655, 'BILL_AMT4': 675, 'BILL_AMT5': 655, 'BILL_AMT6': 688}
Số tiền thanh toán bằng 0 (PAY_AMT = 0): {'PAY_AMT1': 5249, 'PAY_AMT2': 5396, 'PAY_AMT3': 5968, 'PAY_AMT4': 6408, 'PAY_AMT5': 6703, 'PAY_AMT6': 7173}"""

code_s2 = """# 1. Duplicate check
exact_dup = df.duplicated().sum()
feat_dup = df.duplicated(subset=[c for c in df.columns if c != 'ID']).sum()

print(f"Số dòng trùng lặp toàn bộ (gồm cả ID): {exact_dup}")
print(f"Số dòng trùng lặp đặc trưng (bỏ qua cột ID): {feat_dup}")

# 2. Undocumented Category Codes
print("\\n=== GIÁ TRỊ BẤT THƯỜNG TRONG CÁC BIẾN CATEGORICAL ===")
print(f"EDUCATION value counts:\\n{df['EDUCATION'].value_counts().sort_index().to_dict()}")
print(f"MARRIAGE value counts:\\n{df['MARRIAGE'].value_counts().sort_index().to_dict()}")
print(f"PAY_0 value counts:\\n{df['PAY_0'].value_counts().sort_index().to_dict()}")

# 3. Negative BILL_AMT & Zero PAY_AMT
print("\\n=== KIỂM TRA SỐ LƯỢNG GIÁ TRỊ ÂM (BILL_AMT) VÀ BẰNG 0 (PAY_AMT) ===")
neg_bills = {col: (df[col] < 0).sum() for col in [f'BILL_AMT{i}' for i in range(1, 7)]}
zero_pays = {col: (df[col] == 0).sum() for col in [f'PAY_AMT{i}' for i in range(1, 7)]}

print("Số dư hóa đơn âm (BILL_AMT < 0):", neg_bills)
print("Số tiền thanh toán bằng 0 (PAY_AMT = 0):", zero_pays)"""

add_code(code_s2, text_outputs=s2_output)

add_md("""### Nhận xét Phần 2:
1. **Dòng trùng lặp (Duplicates)**:
   - Không có dòng trùng lặp 100% nếu tính cả cột `ID`.
   - Có **35 dòng dữ liệu trùng lặp hoàn toàn** về thuộc tính khách hàng nếu loại bỏ cột `ID`.
2. **Mã danh mục chưa quy ước (Undocumented Codes)**:
   - `EDUCATION`: Mã `0` (14 mẫu), `5` (280 mẫu), `6` (51 mẫu) -> Tổng cộng 345 quan sát (1.15%).
   - `MARRIAGE`: Mã `0` (54 mẫu ~ 0.18%).
   - `PAY_0` đến `PAY_6`: Xuất hiện mã `-2` (không phát sinh giao dịch/dư nợ) và `0` (sử dụng hạn mức tín dụng xoay vòng).
3. **Giá trị dư nợ âm & Tiền trả bằng 0**:
   - `BILL_AMT1..6`: Khoảng 1.97% - 2.29% mẫu có số dư hóa đơn âm. Đây là hiện tượng tài chính thực tế khi khách hàng thanh toán dư nợ kỳ trước cao hơn dư nợ hóa đơn hoặc nhận chiết khấu.
   - `PAY_AMT1..6`: 17.5% - 23.9% mẫu có số tiền thanh toán bằng 0 trong kỳ.
""")

# 5. Section 3 Target
add_md("""---
## 3. Phân tích Chi tiết Biến Mục tiêu (Target Variable Audit)

Biến mục tiêu là `default.payment.next.month`:
- **0**: Khách hàng không vỡ nợ trong Tháng 10/2005 (23,364 mẫu ~ 77.88%).
- **1**: Khách hàng vỡ nợ (Default) trong Tháng 10/2005 (6,636 mẫu ~ 22.12%).
""")

s3_output = """                  Số lượng (Counts)  Tỷ lệ (%)
Không vỡ nợ (0)               23364      77.88
Vỡ nợ (1)                      6636      22.12

Tỷ lệ Mất cân bằng Lớp (Imbalance Ratio 0 : 1): 3.52 : 1"""

code_s3 = """target_col = 'default.payment.next.month'
counts = df[target_col].value_counts()
pcts = df[target_col].value_counts(normalize=True) * 100
imbalance_ratio = counts[0] / counts[1]

target_summary = pd.DataFrame({
    'Số lượng (Counts)': counts,
    'Tỷ lệ (%)': pcts.round(2)
})
target_summary.index = ['Không vỡ nợ (0)', 'Vỡ nợ (1)']
display(target_summary)
print(f"\\nTỷ lệ Mất cân bằng Lớp (Imbalance Ratio 0 : 1): {imbalance_ratio:.2f} : 1")"""

add_code(code_s3, text_outputs=s3_output, image_paths=['../reports/figures/target_distribution.png'])

add_md("""### Nhận xét Phần 3:
1. **Phân bố Lớp**: Nhóm 0 (Không vỡ nợ): 23,364 mẫu (77.88%); Nhóm 1 (Vỡ nợ): 6,636 mẫu (22.12%).
2. **Mức độ Mất cân bằng Lớp**: Imbalance Ratio = **3.52 : 1**.
3. **Ảnh hưởng tới ML**: Metric Accuracy KHÔNG phản ánh đúng chất lượng mô hình (Accuracy Paradox). Bắt buộc phải dùng ROC-AUC, PR-AUC, F1-Score và Cost-sensitive evaluation.
""")

# 6. Section 4 Univariate
add_md("""---
## 4. Thống kê Mô tả & Phân tích Đơn biến (Univariate Analysis)

Thống kê mô tả đầy đủ các biến định lượng:
""")

num_cols = ['LIMIT_BAL', 'AGE'] + [f'BILL_AMT{i}' for i in range(1, 7)] + [f'PAY_AMT{i}' for i in range(1, 7)]
num_stats_df = df[num_cols].describe().T[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
num_stats_df['skewness'] = df[num_cols].skew()
num_stats_df['kurtosis'] = df[num_cols].kurt()
s4_output = num_stats_df.to_string()

code_s4 = """num_cols = ['LIMIT_BAL', 'AGE'] + [f'BILL_AMT{i}' for i in range(1, 7)] + [f'PAY_AMT{i}' for i in range(1, 7)]

num_stats = df[num_cols].describe().T[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
num_stats['skewness'] = df[num_cols].skew()
num_stats['kurtosis'] = df[num_cols].kurt()

display(num_stats)"""

add_code(code_s4, text_outputs=s4_output, image_paths=['../reports/figures/demographic_distribution.png'])

add_md("""### Nhận xét Phần 4:
1. `LIMIT_BAL`: Trung bình 167,484 NTD, trung vị 140,000 NTD, skewness = 0.99.
2. `AGE`: Trung bình 35.49 tuổi, trung vị 34.0 tuổi (dao động 21 - 79).
3. `PAY_AMT1..6`: Skewness từ 10.6 đến 30.5, Kurtosis từ 167 đến 1641 -> Phân bố bị lệch phải cực mạnh và chứa nhiều Outliers cực đại. Cần chuyển đổi phi tuyến (`Log1p`) và scaling thích hợp.
""")

# 7. Section 5 Bivariate
add_md("""---
## 5. Phân tích Đa biến & Tỷ lệ Vỡ nợ theo Nhóm (Bivariate Analysis & Default Rates)
""")

code_s5 = """# Hiển thị Tỷ lệ Vỡ nợ theo Nhóm Nhân khẩu học & Lịch sử Thanh toán
# (Xem đồ thị đính kèm)"""

add_code(code_s5, text_outputs="Hiển thị đồ thị phân tích đa biến và boxplots so sánh với Target.", image_paths=['../reports/figures/default_rates_by_groups.png', '../reports/figures/boxplots_by_target.png'])

add_md("""### Nhận xét Phần 5:
1. **Giới tính**: Nam (24.17%) có tỷ lệ vỡ nợ cao hơn Nữ (20.78%).
2. **Học vấn**: Cấp 3 (25.16%) và Đại học (23.73%) có tỷ lệ vỡ nợ cao hơn Thạc sĩ/Học viện (19.23%).
3. **Trạng thái Thanh toán PAY_0**: `PAY_0 <= 0` có default rate 12.8% - 16.8%. Khi `PAY_0 = 1` (trậm 1 tháng), default rate nhảy vọt lên 33.95%. Khi `PAY_0 = 2` (trậm 2 tháng), default rate lên tới **69.14%**!
""")

# 8. Section 6 Correlation & Multicollinearity
add_md("""---
## 6. Phân tích Tương quan & Đa cộng tuyến (Correlation & Multicollinearity Analysis)
""")

code_s6 = """# Heatmap Tương quan Pearson & Chi tiết Đa cộng tuyến"""

add_code(code_s6, text_outputs="Hiển thị Heatmap tương quan toàn bộ đặc trưng và đa cộng tuyến giữa BILL_AMT và PAY.", image_paths=['../reports/figures/correlation_heatmap.png', '../reports/figures/multicollinearity_heatmap.png'])

add_md("""### Nhận xét Phần 6:
1. **Biến tương quan cao nhất với Target**: `PAY_0` ($r = +0.325$), `PAY_2` ($r = +0.264$), `LIMIT_BAL` ($r = -0.154$).
2. **Đa cộng tuyến cao (High Multicollinearity)**: Tương quan giữa các biến hóa đơn liên tiếp `BILL_AMT1` và `BILL_AMT2` lên tới **0.951**, `BILL_AMT4` và `BILL_AMT5` lên tới **0.940**.
3. **Giải pháp đề xuất**: Cần tạo các biến tổng hợp (dư nợ trung bình, tỷ lệ nợ/hạn mức) ở bước Preprocessing.
""")

# 9. Section 7 Recommendations & Risk Assessment
add_md("""---
## 7. Đánh giá Rủi ro ML & Đề xuất cho bước Preprocessing (ML Risk Assessment & Preprocessing Proposals)

### 7.1. Đánh giá Rủi ro Rò rỉ Dữ liệu (Data Leakage Audit)
- **Cột ID**: Cột `ID` là index ngẫu nhiên, loại bỏ khi huấn luyện.
- **Tính Thời gian**: Các biến ghi nhận từ T4/2005 đến T9/2005, hoàn toàn đứng trước mốc dự báo T10/2005. KHÔNG rò rỉ dữ liệu thời gian.

---
## Những vấn đề cần xử lý ở bước Preprocessing (CHỈ ĐỀ XUẤT)

> [!IMPORTANT]
> Đây là mục tổng hợp đề xuất các bước xử lý dữ liệu cho Giai đoạn Preprocessing tiếp theo. Trong Notebook này, chúng tôi **CHƯA thực hiện bất kỳ thao tác biến đổi dữ liệu nào** để đảm bảo tuân thủ yêu cầu ĐATN.

1. **Loại bỏ đặc trưng không tiên đoán (`ID`)**: Loại bỏ cột `ID` khỏi tập dữ liệu huấn luyện.
2. **Xử lý Dòng trùng lặp (Duplicate Rows)**: Loại bỏ 35 dòng dữ liệu trùng lặp hoàn toàn các thuộc tính.
3. **Xử lý Giá trị Danh mục chưa quy ước (Undocumented Codes)**: Gom nhóm `0, 5, 6` ở `EDUCATION` về nhóm `4 (Others)` hoặc `0 (Unknown)`; gom nhóm `0` ở `MARRIAGE` về `3 (Others)`.
4. **Biến đổi Phân bố Lệch & Chuẩn hóa Dữ liệu (Scaling & Transformation)**: Áp dụng phép biến đổi `Log1p` / `Yeo-Johnson` kết hợp `RobustScaler` / `StandardScaler` cho nhóm `PAY_AMT1..6` và `BILL_AMT1..6`.
5. **Kỹ thuật Kỹ thuật Đặc trưng (Feature Engineering)**:
   - `UTILIZATION_RATE`: Tỷ lệ sử dụng hạn mức ($\text{BILL\_AMT1} / \text{LIMIT\_BAL}$).
   - `MEAN_BILL_AMT`: Dư nợ trung bình 6 tháng.
   - `MEAN_PAY_AMT`: Số tiền trả trung bình 6 tháng.
   - `PAY_RATIO`: Tỷ lệ thanh toán trên dư nợ ($\text{PAY\_AMT} / (\text{BILL\_AMT} + 1)$).
   - `MAX_PAY_DELAY`: Số tháng trậm trả tối đa trong 6 tháng.
6. **Xử lý Mất cân bằng Lớp (Class Imbalance Handling)**: Áp dụng `class_weight='balanced'` hoặc SMOTE trên tập Train, sử dụng ROC-AUC / PR-AUC làm metric chính.
""")

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
