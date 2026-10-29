# BÁO CÁO PREPROCESSING & KIỂM SOÁT DATA LEAKAGE

**Đề tài Đồ án tốt nghiệp**: "NGHIÊN CỨU XÂY DỰNG MÔ HÌNH MACHINE LEARNING TRONG ĐÁNH GIÁ VÀ DỰ BÁO RỦI RO TÍN DỤNG KHÁCH HÀNG"  
**Tập dữ liệu**: UCI Credit Card Default Dataset (`UCI_Credit_Card.csv`)  
**Giai đoạn thực hiện**: Tuần 4 (14/09/2026 – 20/09/2026)  

---

## 1. Mục tiêu

Báo cáo này trình bày toàn bộ kết quả thực hiện của **Tuần 4 (Preprocessing, Train/Test Split và Kiểm soát Data Leakage)** theo đúng đề cương timeline Đồ án tốt nghiệp.

Các mục tiêu cụ thể đạt được:
1. Thực hiện làm sạch dữ liệu sơ bộ dựa trên các phát hiện từ giai đoạn EDA (xử lý 35 dòng trùng lặp thuộc tính, bảo tồn thông tin gốc).
2. Quy chuẩn các mã danh mục chưa được mô tả rõ (`EDUCATION` 0, 5, 6 và `MARRIAGE` 0) về nhóm chuẩn.
3. Phân chia tập dữ liệu **Train/Test Split (80/20, stratify=y, random_state=42)** trước khi thực hiện bất kỳ phép chuẩn hóa hay tính toán thống kê nào.
4. Thiết lập **Preprocessing Pipeline (`ColumnTransformer`)** với `RobustScaler` fit **CHỈ TRÊN TẬP TRAIN** nhằm phòng chống rò rỉ dữ liệu (**Data Leakage**) tuyệt đối.
5. Phân tích và chuẩn bị phương án xử lý Mất cân bằng lớp (Class Imbalance Strategy) phục vụ giai đoạn huấn luyện mô hình Machine Learning ở Tuần 6.
6. Tuân thủ nguyên tắc khoanh vùng phạm vi: **KHÔNG** huấn luyện mô hình ML, **KHÔNG** làm Feature Engineering (Tuần 5), **KHÔNG** hyperparameter tuning, SHAP hay Streamlit.

---

## 2. Dữ liệu Đầu vào

- **Nguồn dữ liệu gốc**: `data/raw/UCI_Credit_Card.csv`
- **Kích thước dữ liệu thô**: $30,000 \text{ dòng} \times 25 \text{ cột}$.
- **Tình trạng ô khuyết (Missing values)**: **0 ô khuyết** ($0.00\%$).
- **Kiểu dữ liệu**: Toàn bộ $25/25$ cột là kiểu số nguyên (`int64`).
- **Biến mục tiêu**: `default.payment.next.month` (0 = Không vỡ nợ: 23,364 mẫu ~ 77.88%; 1 = Vỡ nợ: 6,636 mẫu ~ 22.12%).

---

## 3. Xử lý Cột Định danh ID

- **Bản chất nghiệp vụ**: Cột `ID` là mã số thứ tự định danh quản lý tài khoản khách hàng, không mang ý nghĩa thuộc tính hành vi hay giá trị tiên đoán rủi ro.
- **Quyết định Preprocessing**:
  - **KHÔNG xóa ID khỏi tập dữ liệu thô gốc** (`data/raw/UCI_Credit_Card.csv`) nhằm bảo đảm khả năng truy vết dữ liệu (traceability).
  - **Loại bỏ ID khỏi tập thuộc tính đầu vào $X$** trước khi chia Train/Test Split để ngăn chặn hiện tượng mô hình ML "học vẹt" chỉ số thứ tự index (artifact memorization).

---

## 4. Xử lý Dòng Trùng lặp (Duplicates)

### 4.1. Phân tích chi tiết 35 Dòng trùng lặp
Giai đoạn EDA phát hiện **35 dòng dữ liệu trùng lặp hoàn toàn các thuộc tính đặc trưng** khi loại bỏ cột `ID` (tương ứng 70 dòng tham gia vào các nhóm trùng lặp).

Trước khi tiến hành loại bỏ, chúng tôi thực hiện kiểm tra mức độ nhất quán của biến mục tiêu `default.payment.next.month` giữa các dòng trùng lặp:
- Tổng số dòng trùng lặp: 70 dòng (58 mẫu nhãn 0 và 12 mẫu nhãn 1).
- **Số lượng nhóm trùng lặp có Target BẤT NHẤT**: **0 nhóm**.
- *Đánh giá*: 100% các dòng trùng lặp đều có giá trị nhãn vỡ nợ đồng nhất tuyệt đối. Việc trùng lặp này xuất phát từ việc khách hàng mở nhiều khoản vay trùng thuộc tính hoặc lỗi ghi nhận mẫu của hệ thống.

### 4.2. Kết quả Xử lý
Loại bỏ 35 dòng trùng lặp dư thừa (giữ lại bản ghi đại diện đầu tiên):
- **Số dòng trước xử lý**: $30,000 \text{ dòng}$
- **Số dòng trùng lặp loại bỏ**: $35 \text{ dòng}$
- **Số dòng sau xử lý**: $\mathbf{29,965 \text{ dòng}}$

---

## 5. Xử lý Mã Danh mục Bất thường (Categorical Anomalies)

Không thực hiện xóa bỏ mẫu, ưu tiên bảo toàn thông tin dữ liệu bằng cách gom nhóm hợp lý:

1. **Biến `EDUCATION` (Trình độ học vấn)**:
   - Thống kê trước xử lý: Mã `1` (10,582 mẫu), Mã `2` (14,024 mẫu), Mã `3` (4,915 mẫu), Mã `4` (123 mẫu), Mã `0` (14 mẫu), Mã `5` (280 mẫu), Mã `6` (51 mẫu).
   - Các mã `0, 5, 6` chiếm tổng cộng **345 mẫu** ($1.15\%$).
   - *Quyết định*: Gom toàn bộ các mã `0, 5, 6` vào mã `4 (Others)` để đưa về 4 nhóm chuẩn theo tài liệu gốc UCI: `{1: Graduate School, 2: University, 3: High School, 4: Others}`.
2. **Biến `MARRIAGE` (Tình trạng hôn nhân)**:
   - Thống kê trước xử lý: Mã `1` (13,643 mẫu), Mã `2` (15,951 mẫu), Mã `3` (323 mẫu), Mã `0` (54 mẫu ~ 0.18%).
   - *Quyết định*: Gom mã `0` vào mã `3 (Others)` để đưa về 3 nhóm chuẩn: `{1: Married, 2: Single, 3: Others}`.
3. **Biến `PAY_0` đến `PAY_6` (Lịch sử thanh toán)**:
   - Các giá trị `-2` (không phát sinh dư nợ), `-1` (thanh toán đúng hạn), `0` (sử dụng hạn mức tín dụng xoay vòng), và `1..8` (trậm trả 1..8 tháng) **được giữ nguyên** để bảo toàn thứ tự mức độ nghiêm trọng của số tháng trậm trả.

---

## 6. Train / Test Split

Thực hiện phân chia không gian thuộc tính $X$ (23 thuộc tính) và biến mục tiêu $y$ bằng hàm `train_test_split` của Scikit-Learn:
- **Tỷ lệ phân chia**: **80% TRAIN** và **20% TEST**.
- **Phân tầng (Stratification)**: `stratify=y` nhằm đảm bảo tỷ lệ biến mục tiêu ở tập TRAIN và TEST đồng nhất với tổng thể.
- **Cố định ngẫu nhiên**: `random_state = 42`.

### Thống kê Kết quả Chia tập:

| Tập dữ liệu | Số lượng quan sát | Tỷ lệ (%) | Số lượng Không vỡ nợ (0) | Số lượng Vỡ nợ (1) | Tỷ lệ Vỡ nợ (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tập TRAIN** | 23,972 | 80.00% | 18,668 | 5,304 | **22.13%** |
| **Tập TEST** | 5,993 | 20.00% | 4,667 | 1,326 | **22.12%** |
| **Tổng cộng** | **29,965** | **100.00%** | **23,335** | **6,630** | **22.13%** |

*Đánh giá*: Phân tầng `stratify=y` hoạt động hoàn hảo, tỷ lệ vỡ nợ ở tập TRAIN và TEST cân bằng tuyệt đối ở mức **22.13%**.

---

## 7. Kiểm soát Rò rỉ Dữ liệu (Kiểm soát Data Leakage)

Chúng tôi thiết lập checklist 7 tiêu chí kiểm soát rò rỉ dữ liệu nghiêm ngặt theo chuẩn mực học máy:

| # | Tiêu chí Kiểm tra Data Leakage | Trạng thái | Giải thích chi tiết |
| :-: | :--- | :---: | :--- |
| 1 | Cột `ID` không được dùng làm feature | `[x] PASSED` | `ID` đã bị xóa khỏi tập thuộc tính $X$. |
| 2 | Train/Test Split trước khi fit Scaler | `[x] PASSED` | Split ở Mục 6, `.fit()` Scaler thực hiện ở Mục 8. |
| 3 | Encoder không học từ tập TEST | `[x] PASSED` | Không dùng Encoder phụ thuộc tham số từ tập TEST. |
| 4 | Transformation không học từ tập TEST | `[x] PASSED` | Scaler chỉ học Median và IQR từ `X_train`. |
| 5 | SMOTE không áp dụng trên tập TEST | `[x] PASSED` | SMOTE chỉ chuẩn bị áp dụng trên TRAIN ở bước ML. |
| 6 | Không dùng Target TEST để Preprocess | `[x] PASSED` | `y_test` tuyệt đối không tham gia vào tiền xử lý. |
| 7 | Không dùng Thống kê TEST cho TRAIN | `[x] PASSED` | Tập TEST hoàn toàn độc lập, chỉ dùng `.transform()`. |

---

## 8. Numerical Preprocessing (Xử lý Biến Số)

- **Danh sách 14 biến số**: `LIMIT_BAL`, `AGE`, `BILL_AMT1..6`, `PAY_AMT1..6`.
- **Xử lý số dư hóa đơn âm (`BILL_AMT < 0`)**: Giữ nguyên toàn bộ giá trị âm vì đây là hiện tượng tài chính thực tế khi khách hàng thanh toán dư nợ kỳ trước hoặc nhận hoàn tiền/chiết khấu.
- **Xử lý số tiền trả bằng 0 (`PAY_AMT = 0`)**: Giữ nguyên các giá trị 0 vì đây là chỉ báo quan trọng thể hiện khách hàng không thực hiện thanh toán trong kỳ.
- **Lựa chọn Scaler**:
  - Các biến `PAY_AMT1..6` có skewness cực mạnh ($10.6 - 30.5$) và chứa ngoại biệt cực đại.
  - Sử dụng **`RobustScaler`** (dựa trên Trung vị và Khoảng tứ phân vị IQR: $Q75 - Q25$) để chuẩn hóa. `RobustScaler` **không bị méo bởi các giá trị ngoại biệt cực đại** và **bảo toàn cấu trúc của giá trị 0 và số âm**.
  - **Quy trình fit**: `preprocessor.fit(X_train)` chỉ tính Median và IQR trên `X_train`. Sau đó thực hiện `transform(X_train)` và `transform(X_test)`.

---

## 9. Categorical Preprocessing (Xử lý Biến Danh mục)

- **Danh sách 9 biến danh mục/thứ tự**: `SEX`, `EDUCATION`, `MARRIAGE`, `PAY_0`, `PAY_2`, `PAY_3`, `PAY_4`, `PAY_5`, `PAY_6`.
- **Phương pháp Encoding**:
  - `EDUCATION` và `MARRIAGE` đã được chuẩn hóa về các mã số nguyên chuẩn `{1, 2, 3, 4}` và `{1, 2, 3}`.
  - `PAY_0..6` duy trì dạng giá trị số nguyên đại diện cho số tháng trậm trả.
  - Sử dụng chiến lược **`Passthrough`** để giữ nguyên miền giá trị định danh/thứ tự an toàn, không làm phình to chiều dữ liệu khi chưa cần thiết.

---

## 10. Class Imbalance (Xử lý Mất cân bằng Lớp)

- **Tỷ lệ mất cân bằng tập TRAIN**: 18,668 mẫu Lớp 0 (77.87%) vs 5,304 mẫu Lớp 1 (22.13%) $\rightarrow$ Imbalance Ratio $\approx \mathbf{3.52 : 1}$.
- **Đề xuất 3 phương án thử nghiệm cho Tuần 6 (Model Training)**:
  1. *Phương án 1 (Baseline Unbalanced)*: Giữ nguyên phân bố gốc để đánh giá điểm mốc.
  2. *Phương án 2 (`class_weight='balanced'`)*: Điều chỉnh trọng số mất mát trong Logistic Regression, Random Forest, XGBoost để phạt nặng lỗi bỏ sót Lớp 1.
  3. *Phương án 3 (SMOTE Oversampling trên TRAIN)*: Áp dụng SMOTE để tạo mẫu giả lập cho Lớp 1 **chỉ trên tập TRAIN** thông qua `imblearn.pipeline.Pipeline`. **Tập TEST tuyệt đối không được áp dụng SMOTE**.

---

## 11. Tập Dữ liệu sau Preprocessing

Các tập dữ liệu đã hoàn tất tiền xử lý và được lưu trữ tại `data/processed/`:

1. `data/processed/X_train.csv`: Tập thuộc tính huấn luyện ($23,972 \text{ dòng} \times 23 \text{ cột}$).
2. `data/processed/X_test.csv`: Tập thuộc tính kiểm thử ($5,993 \text{ dòng} \times 23 \text{ cột}$).
3. `data/processed/y_train.csv`: Biến mục tiêu huấn luyện ($23,972 \text{ dòng}$).
4. `data/processed/y_test.csv`: Biến mục tiêu kiểm thử ($5,993 \text{ dòng}$).

---

## 12. Bảng Tổng hợp các Quyết định Preprocessing

| Hạng mục Preprocessing | Quyết định Thực hiện | Căn cứ Kỹ thuật & Nghiệp vụ |
| :--- | :--- | :--- |
| **Xử lý Cột ID** | Loại khỏi $X$, giữ trong raw data | Ngăn mô hình học vẹt index; bảo toàn khả năng truy vết. |
| **Xử lý Duplicates** | Loại bỏ 35 dòng trùng lặp feature-level | 100% nhóm trùng có Target nhất quán; chống thiên vị mẫu. |
| **Mã EDUCATION** | Gom 0, 5, 6 về 4 (Others) | Đưa về 4 nhóm chuẩn theo tài liệu UCI; bảo toàn mẫu. |
| **Mã MARRIAGE** | Gom 0 về 3 (Others) | Đưa về 3 nhóm chuẩn theo tài liệu UCI; bảo toàn mẫu. |
| **`BILL_AMT < 0`** | Giữ nguyên giá trị âm | Dư nợ âm có ý nghĩa tài chính (thanh toán thừa/hoàn tiền). |
| **`PAY_AMT = 0`** | Giữ nguyên giá trị 0 | Giá trị 0 có ý nghĩa nghiệp vụ (không trả tiền trong kỳ). |
| **Train/Test Split** | Tách 80/20 có `stratify=y` trước Fit | Cân bằng tỷ lệ target 22.13%; chống rò rỉ dữ liệu. |
| **Chuẩn hóa Numerical** | `RobustScaler` (Fit trên TRAIN ONLY) | Tránh méo do outliers cực đại ở `PAY_AMT` ($skew > 10$). |
| **Categorical Encoding** | Ordinal / Passthrough | Bảo toàn thứ tự trậm trả theo tháng của `PAY_0..6`. |

---

## 13. Những Nội dung TUYỆT ĐỐI CHƯA THỰC HIỆN

Để tuân thủ nghiêm ngặt tiến độ Đồ án tốt nghiệp và không làm thay công việc của các tuần sau, chúng tôi xác nhận **CHƯA THỰC HIỆN** các nội dung sau:

- [ ] **Feature Engineering (Tuần 5)**: *TUYỆT ĐỐI CHƯA TẠO* các biến mới như `UTILIZATION_RATE`, `MEAN_BILL_AMT`, `MEAN_PAY_AMT`, `PAY_RATIO`, `MAX_PAY_DELAY`.
- [ ] **Huấn luyện Mô hình Machine Learning (Tuần 6)**: *TUYỆT ĐỐI CHƯA TRAIN* Logistic Regression, Decision Tree, Random Forest, XGBoost.
- [ ] **Tối ưu Siêu tham số & Lựa chọn Mô hình (Tuần 7)**: *TUYỆT ĐỐI CHƯA RUN* Hyperparameter tuning hay GridSearch.
- [ ] **Giải thích Mô hình bằng SHAP (Tuần 8)**: *TUYỆT ĐỐI CHƯA CHẠY* SHAP values.
- [ ] **Xây dựng Giao diện Streamlit (Tuần 9)**: *TUYỆT ĐỐI CHƯA VIẾT* Streamlit Web App.
