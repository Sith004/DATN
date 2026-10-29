# CHƯƠNG 2. PHƯƠNG PHÁP THỰC HIỆN

**Đề tài:** Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  
**Sinh viên:** Nguyễn Trọng Thể — MSSV: 1150080117  
**GVHD:** TS. Dương Thị Thúy Nga  
*[Bản nháp Markdown — nguồn cho file Word chính thức]*

---

## Mở đầu Chương 2

Chương 2 trình bày chi tiết toàn bộ quy trình phương pháp và kỹ thuật được áp dụng trong quá trình thực hiện đề tài, từ giai đoạn kiểm duyệt và phân tích dữ liệu đến thiết kế, xây dựng và đánh giá các mô hình Machine Learning, áp dụng phương pháp giải thích mô hình SHAP và thiết kế ứng dụng Web Prototype hỗ trợ ra quyết định tín dụng. Các quyết định phương pháp được trình bày kèm luận cứ kỹ thuật và nghiệp vụ rõ ràng, nhằm đảm bảo tính tái lập và minh bạch của thực nghiệm.

---

## 2.1. Quy trình tổng thể xây dựng mô hình Machine Learning (ML Pipeline)

Quy trình nghiên cứu được thiết kế theo kiến trúc pipeline tuyến tính, tuần tự, tuân thủ nguyên tắc kiểm soát rò rỉ dữ liệu (Data Leakage Control) xuyên suốt từ đầu đến cuối. Hình 2.1 thể hiện sơ đồ tổng thể của pipeline nghiên cứu.

```
[Nguồn dữ liệu UCI Credit Card]
         ↓
[Bước 1] Data Audit & EDA (Tuần 1–3)
  - Kiểm tra tính toàn vẹn dữ liệu
  - Phân tích phân bố và tương quan
  - Phát hiện giá trị bất thường
         ↓
[Bước 2] Tiền xử lý dữ liệu (Tuần 4)
  - Loại bỏ ID và dòng trùng lặp
  - Chuẩn hóa mã danh mục
  - Phân chia Train/Test (80/20, stratify)
  - Fit RobustScaler TRÊN TRAIN ONLY
         ↓
[Bước 3] Feature Engineering (Tuần 5)
  - Tính 10 biến tài chính tổng hợp
  - Kiểm tra chất lượng 33 features
         ↓
[Bước 4] Xây dựng mô hình Baseline (Tuần 6)
  - Logistic Regression (Default & Balanced)
  - Decision Tree (Default & Balanced)
         ↓
[Bước 5] Ensemble Models (Tuần 7)
  - Random Forest (Default & Balanced)
  - XGBoost Baseline
         ↓
[Bước 6] Hyperparameter Tuning & Lựa chọn (Tuần 8)
  - RandomizedSearchCV + StratifiedKFold(5)
  - Threshold Analysis (OOF predictions)
  - Lựa chọn XGBoost Tuned (threshold=0.60)
         ↓
[Bước 7] Giải thích mô hình SHAP (Tuần 9)
  - Global Feature Importance (Beeswarm/Bar)
  - Dependence Analysis
  - Local Explanation (Waterfall)
         ↓
[Bước 8] Xây dựng ứng dụng Web Prototype (Tuần 10)
  - Streamlit DSS Prototype
  - Tích hợp pipeline dự báo
  - Kiểm thử tích hợp
```
*Hình 2.1. Sơ đồ tổng thể quy trình nghiên cứu ML Pipeline*

Nguyên tắc xuyên suốt toàn bộ pipeline: **tập Test hoàn toàn độc lập**, không tham gia vào bất kỳ bước tiền xử lý, huấn luyện, tối ưu tham số hay chọn ngưỡng nào. Mọi phép biến đổi tham số hóa (RobustScaler, Cross-Validation) đều chỉ được học từ tập Train.

---

## 2.2. Kiểm duyệt dữ liệu và Phương pháp phân tích khám phá (Data Audit & EDA)

### 2.2.1. Phương pháp kiểm duyệt chất lượng dữ liệu (Data Audit)

Kiểm duyệt dữ liệu (Data Audit) là bước bắt buộc đầu tiên trước khi xây dựng bất kỳ mô hình học máy nào, nhằm phát hiện sớm các vấn đề chất lượng dữ liệu có thể làm méo kết quả mô hình. Phương pháp kiểm duyệt được thực hiện theo bốn nội dung chính:

**a) Kiểm tra tính toàn vẹn cơ bản:**  
Kiểm tra kích thước ma trận dữ liệu, kiểu dữ liệu từng cột, số lượng ô khuyết (NULL/NaN) và tỷ lệ khuyết. Đây là bước nền tảng xác định liệu dữ liệu có cần xử lý thiếu (imputation) hay không.

**b) Kiểm tra dòng trùng lặp (Duplicate Audit):**  
Phân biệt hai cấp độ trùng lặp: (i) Trùng lặp hoàn toàn bao gồm cột định danh ID — thường là lỗi kỹ thuật ghi nhận; (ii) Trùng lặp đặc trưng — cùng thuộc tính hành vi nhưng có ID khác nhau, có thể do khách hàng mở nhiều tài khoản hoặc lỗi nhập liệu. Đối với nhóm trùng lặp đặc trưng, cần kiểm tra thêm tính nhất quán của biến mục tiêu: nếu nhãn không nhất quán (conflicting labels), cần có chiến lược xử lý riêng.

**c) Kiểm tra mã danh mục bất thường (Undocumented Categories):**  
Đối chiếu các giá trị thực tế trong từng cột phân loại với bộ giá trị được mô tả chính thức trong tài liệu nguồn (data dictionary). Các giá trị nằm ngoài phạm vi mô tả cần được phân tích bản chất (lỗi nhập liệu, giá trị đặc biệt hay danh mục chưa được tài liệu hóa) trước khi quyết định xử lý.

**d) Kiểm tra giá trị ngoại lệ và phân bố lệch (Extreme Values & Skewness):**  
Phân tích thống kê mô tả (Mean, Median, Std, Skewness, Kurtosis, Min, Max, IQR) của các biến liên tục. Đặc biệt chú ý đến hệ số lệch (Skewness) và độ nhọn (Kurtosis) — giá trị cực lớn chỉ ra phân bố lệch mạnh với ngoại lệ (outliers) ảnh hưởng đến lựa chọn phương pháp chuẩn hóa.

### 2.2.2. Phương pháp phân tích tương quan và trực quan hóa phân phối

Phân tích EDA được thực hiện theo hai cấp độ:

**a) Phân tích đơn biến (Univariate Analysis):**  
Phân phối từng biến đặc trưng được trực quan hóa bằng biểu đồ histogram và boxplot. Phân tích phân bố biến mục tiêu xác định mức độ mất cân bằng lớp, đây là thông tin then chốt cho thiết kế chiến lược huấn luyện.

**b) Phân tích đa biến và tương quan (Bivariate & Multivariate Analysis):**  
- **Ma trận tương quan Pearson** $(r_{XY})$: Đo lường mức độ tương quan tuyến tính giữa các đặc trưng đầu vào và biến mục tiêu, phát hiện các cặp đặc trưng tương quan cao (đa cộng tuyến — Multicollinearity), đặc biệt nguy hiểm với mô hình Logistic Regression.
- **Phân tích tỷ lệ vỡ nợ theo nhóm**: Tính tỷ lệ Default trong từng phân nhóm của biến phân loại (`SEX`, `EDUCATION`, `MARRIAGE`, `PAY_0`), cung cấp insight ban đầu về sức mạnh dự báo của từng biến.
- **Boxplot so sánh theo Target**: Trực quan hóa phân bố các biến liên tục giữa hai nhóm Default (y=1) và Non-Default (y=0).

---

## 2.3. Phương pháp Tiền xử lý dữ liệu và Quy tắc chống Data Leakage

### 2.3.1. Quy tắc phân chia tập Train/Test và kiểm soát rò rỉ dữ liệu (Data Leakage)

**Định nghĩa Data Leakage:**  
Rò rỉ dữ liệu xảy ra khi thông tin từ tập kiểm tra (Test set) — trực tiếp hoặc gián tiếp — tham gia vào quá trình huấn luyện, dẫn đến đánh giá quá lạc quan về hiệu năng mô hình trên dữ liệu thực tế. Data Leakage là một trong những lỗi nghiêm trọng nhất trong thực hành Machine Learning, thường khó phát hiện và gây hậu quả lớn khi triển khai thực tế.

**Quy tắc phân chia Train/Test:**  
Phân chia thực hiện **trước mọi bước tiền xử lý có tham số** (Scaling, Encoding có tham số học từ dữ liệu). Cụ thể:

$$\text{Dataset}_{\text{clean}} \xrightarrow{\text{train\_test\_split}(80\%, \text{stratify}=y, \text{seed}=42)} \{X_{\text{train}}, X_{\text{test}}, y_{\text{train}}, y_{\text{test}}\}$$

Chiến lược phân tầng (`stratify=y`) đảm bảo tỷ lệ biến mục tiêu (Default ≈ 22.13%) được bảo toàn đồng đều trong cả hai tập, điều đặc biệt quan trọng khi dữ liệu mất cân bằng.

**Nguyên tắc Fit-Only-On-Train:**  
Mọi phép biến đổi có "học" tham số thống kê từ dữ liệu (RobustScaler học Median và IQR; Encoder học tập hợp nhãn) phải thực hiện `.fit()` hoặc `.fit_transform()` duy nhất trên $X_{\text{train}}$, sau đó chỉ `.transform()` trên $X_{\text{test}}$.

**Checklist 7 tiêu chí kiểm soát Data Leakage (được xác minh thực nghiệm):**

| # | Tiêu chí | Trạng thái |
|---|---|---|
| 1 | Cột ID không được dùng làm đặc trưng | ✓ PASS |
| 2 | Train/Test Split thực hiện trước khi Fit Scaler | ✓ PASS |
| 3 | Encoder không học từ tập Test | ✓ PASS |
| 4 | RobustScaler chỉ học Median/IQR từ Train | ✓ PASS |
| 5 | SMOTE không áp dụng trên tập Test | ✓ PASS |
| 6 | Nhãn Test không tham gia vào tiền xử lý | ✓ PASS |
| 7 | Thống kê Test không được dùng cho Train | ✓ PASS |

### 2.3.2. Phương pháp xử lý giá trị ngoại lệ và giá trị bất thường

**Xử lý dòng trùng lặp đặc trưng:**  
35 dòng trùng lặp đặc trưng (khi bỏ cột ID) được xác minh 100% nhất quán về nhãn mục tiêu (không có conflicting labels), do đó loại bỏ bản ghi dư thừa, giữ lại bản ghi đại diện đầu tiên. Kích thước sau xử lý: **29.965 quan sát**.

**Xử lý mã danh mục bất thường (Categorical Anomalies):**  
Phân tích đối chiếu tài liệu UCI phát hiện các mã không được mô tả chính thức:
- `EDUCATION` có mã {0, 5, 6} → gom về mã `4 (Others)`, đưa về 4 nhóm chuẩn {1: Graduate School, 2: University, 3: High School, 4: Others}.
- `MARRIAGE` có mã {0} → gom về mã `3 (Others)`, đưa về 3 nhóm chuẩn {1: Married, 2: Single, 3: Others}.

Chiến lược gom nhóm được ưu tiên hơn loại bỏ mẫu để bảo toàn tối đa thông tin dữ liệu.

**Xử lý giá trị âm trong `BILL_AMT` và giá trị 0 trong `PAY_AMT`:**  
Giá trị âm trong `BILL_AMT1..6` phản ánh khách hàng thanh toán thừa hoặc nhận hoàn tiền/chiết khấu — là hiện tượng tài chính hoàn toàn hợp lệ, được giữ nguyên. Giá trị 0 trong `PAY_AMT1..6` có ý nghĩa nghiệp vụ rõ ràng (khách hàng không thực hiện thanh toán trong kỳ), cũng được giữ nguyên.

### 2.3.3. Phương pháp chuẩn hóa (Scaling) và mã hóa đặc trưng (Encoding)

**Lựa chọn RobustScaler:**  
Phân tích EDA phát hiện nhóm biến `PAY_AMT1..6` có skewness cực mạnh (10.6 đến 30.5) với ngoại lệ hàng trăm nghìn NTD. `RobustScaler` được lựa chọn vì:
- Sử dụng Trung vị (Median) và Khoảng tứ phân vị (IQR = Q75 − Q25) thay vì Mean và Std, **không bị méo bởi ngoại lệ cực đại**.
- Bảo toàn cấu trúc giá trị 0 (vì 0 ≤ Median trong nhiều biến, IQR ≠ 0).
- Bảo toàn ý nghĩa của giá trị âm trong `BILL_AMT`.

Công thức chuẩn hóa RobustScaler:

$$x_{\text{scaled}} = \frac{x - \text{Median}(X_{\text{train}})}{\text{IQR}(X_{\text{train}})}$$

**Phạm vi áp dụng Scaling:**  
Chỉ áp dụng cho **22 biến số học liên tục** (NUM_COLS): `LIMIT_BAL`, `AGE`, `BILL_AMT1..6`, `PAY_AMT1..6` và 10 biến tổng hợp từ Feature Engineering.  
**9 biến phân loại/thứ tự** (CAT_COLS): `SEX`, `EDUCATION`, `MARRIAGE`, `PAY_0`, `PAY_2..6` — sử dụng chiến lược Passthrough (giữ nguyên), không Encode One-Hot vì các biến `PAY_0..6` duy trì thứ tự có ý nghĩa của số tháng trậm trả.

---

## 2.4. Kỹ thuật trích rút đặc trưng (Feature Engineering)

### 2.4.1. Cơ sở đề xuất các biến chỉ số tài chính

Tập dữ liệu gốc gồm 23 biến độc lập lưu trữ thông tin lịch sử thô (raw). Tuy nhiên, mô hình có thể học hiệu quả hơn từ các chỉ số tài chính tổng hợp phản ánh **mẫu hành vi** của khách hàng qua nhiều chu kỳ, thay vì chỉ xét riêng lẻ từng tháng.

**Nguyên tắc thiết kế đặc trưng:**  
1. Mỗi biến mới phải có ý nghĩa tài chính/nghiệp vụ rõ ràng, không phải biến kỹ thuật thuần túy.
2. Công thức tính toán phải tuân thủ đúng dòng thời gian nghiệp vụ (không tạo ra Data Leakage).
3. Xử lý an toàn các trường hợp mẫu số bằng 0 hoặc âm.
4. Tính toán trên **dữ liệu thô trước khi chuẩn hóa** (không tính trên dữ liệu đã scale).

**Dòng thời gian nghiệp vụ quan trọng:**  
Trong dữ liệu, hóa đơn kỳ tháng 8 (`BILL_AMT2`) có hạn thanh toán vào tháng 9, và số tiền thực trả trong tháng 9 được ghi nhận ở `PAY_AMT1`. Do đó, tỷ lệ thanh toán đúng là `PAY_AMT1 / BILL_AMT2` (không phải `PAY_AMT1 / BILL_AMT1`).

### 2.4.2. Bảng 10 đặc trưng tổng hợp được tạo mới

| # | Tên Biến | Công thức toán học | Ý nghĩa tài chính |
|---|---|---|---|
| 1 | `UTILIZATION_RATE_SEPT` | $\dfrac{\text{BILL\_AMT1}}{\text{LIMIT\_BAL}}$ | Tỷ lệ sử dụng hạn mức tín dụng kỳ T9/2005 |
| 2 | `MEAN_BILL_AMT` | $\dfrac{1}{6}\sum_{i=1}^{6}\text{BILL\_AMT}_i$ | Quy mô dư nợ trung bình 6 tháng |
| 3 | `UTILIZATION_RATE_MEAN` | $\dfrac{\text{MEAN\_BILL\_AMT}}{\text{LIMIT\_BAL}}$ | Tỷ lệ sử dụng hạn mức trung bình 6 tháng |
| 4 | `PAY_RATIO_SEPT` | $\dfrac{\text{PAY\_AMT1}}{\text{BILL\_AMT2}}$ | Tỷ lệ thanh toán kỳ T9 trên hóa đơn T8 |
| 5 | `PAY_RATIO_MEAN` | $\dfrac{1}{5}\sum_{k=1}^{5}\dfrac{\text{PAY\_AMT}_k}{\text{BILL\_AMT}_{k+1}}$ | Trung bình tỷ lệ thanh toán 5 chu kỳ |
| 6 | `MAX_PAY_DELAY` | $\max(\text{PAY\_0}, \text{PAY\_2}, \ldots, \text{PAY\_6})$ | Số tháng trậm trả tối đa (đỉnh điểm vi phạm) |
| 7 | `COUNT_LATE_PAYMENT` | $\sum_{i}\mathbb{1}(\text{PAY}_{i} > 0)$ | Tần suất tháng bị trậm trả $\geq 1$ tháng |
| 8 | `MEAN_PAY_AMT` | $\dfrac{1}{6}\sum_{i=1}^{6}\text{PAY\_AMT}_i$ | Khả năng thanh toán trung bình hàng tháng |
| 9 | `BILL_TREND` | $\dfrac{\text{BILL\_AMT1} - \text{BILL\_AMT6}}{\text{LIMIT\_BAL}}$ | Quỹ đạo dư nợ 6 tháng tương đối với hạn mức |
| 10 | `PAY_TREND` | $\dfrac{\text{PAY\_AMT1} - \text{PAY\_AMT6}}{\text{LIMIT\_BAL}}$ | Quỹ đạo khả năng thanh toán 6 tháng |

**Xử lý biên (Edge Cases):**  
- Khi `LIMIT_BAL ≤ 0`: Gán giá trị 0.0 cho các biến chia theo `LIMIT_BAL` (thay vì NaN hoặc vô cực).
- Khi `BILL_AMT{k+1} ≤ 0` (không có nợ trong kỳ): Gán `PAY_RATIO = 1.0` (xem như đã hoàn thành 100% nghĩa vụ).

Sau khi thêm 10 biến mới vào 23 biến gốc (đã loại ID), không gian đặc trưng mở rộng từ 23 lên **33 đặc trưng** cho mỗi quan sát.

### 2.4.3. Phương pháp đánh giá thực nghiệm tính hiệu quả của các đặc trưng

Hiệu quả của Feature Engineering được đánh giá gián tiếp qua ba phương pháp:
1. **Kiểm tra chất lượng dữ liệu**: Xác minh không có giá trị NaN, vô cực và thứ tự cột nhất quán giữa Train và Test.
2. **Feature Importance từ mô hình**: So sánh thứ hạng quan trọng của biến gốc và biến tổng hợp trong kết quả mô hình (Mục 3.6).
3. **SHAP Global Explanation**: Phân tích đóng góp của từng biến vào kết quả dự báo sau khi mô hình được huấn luyện.

---

## 2.5. Các thuật toán Machine Learning đề xuất

### 2.5.1. Logistic Regression (Mô hình Cơ sở)

Hồi quy Logistic (Logistic Regression) được sử dụng làm mô hình cơ sở (Baseline Model) vì tính đơn giản, khả năng giải thích và tính ổn định thống kê. Mô hình dự báo xác suất vỡ nợ thông qua hàm sigmoid áp dụng trên tổ hợp tuyến tính các đặc trưng:

$$P(Y=1|X) = \sigma(z) = \frac{1}{1 + e^{-z}}, \quad z = \beta_0 + \sum_{j=1}^{p}\beta_j X_j$$

Trong đó $\beta_0$ là hệ số chặn và $\beta_j$ là hệ số hồi quy của đặc trưng $X_j$.

Trong bối cảnh mất cân bằng lớp, hai cấu hình được thử nghiệm: (i) Default — không điều chỉnh trọng số; (ii) Balanced — sử dụng `class_weight='balanced'` để phạt nặng lỗi bỏ sót lớp thiểu số (Default=1).

### 2.5.2. Decision Tree Classifier (Mô hình Cây Quyết định)

Cây quyết định xây dựng mô hình phân loại bằng cách chia đệ quy không gian đặc trưng theo ngưỡng tối ưu tại mỗi nút, sử dụng tiêu chí Gini Impurity:

$$\text{Gini}(p) = 1 - \sum_{k=1}^{K} p_k^2$$

Mô hình Decision Tree được thử nghiệm cả hai cấu hình Default và Balanced để phân tích ảnh hưởng của `class_weight`. Đây là mô hình có khả năng giải thích tốt nhưng dễ bị overfitting khi độ sâu lớn.

### 2.5.3. Random Forest Classifier (Mô hình Rừng Ngẫu nhiên)

Random Forest là thuật toán Ensemble theo cơ chế Bagging, xây dựng $N$ cây quyết định độc lập, mỗi cây được huấn luyện trên một tập bootstrap và chỉ xem xét $\sqrt{p}$ đặc trưng ngẫu nhiên tại mỗi nút phân chia. Kết quả cuối cùng là bầu chọn đa số (Majority Voting):

$$\hat{y} = \text{mode}\{h_1(X), h_2(X), \ldots, h_N(X)\}$$

Cơ chế này giảm phương sai (variance) so với cây đơn lẻ và tự nhiên cung cấp Feature Importance dựa trên Mean Decrease in Impurity.

### 2.5.4. XGBoost (Extreme Gradient Boosting)

XGBoost (Chen & Guestrin, 2016) là thuật toán Gradient Boosting xây dựng cây tuần tự, trong đó mỗi cây mới học từ phần dư của các cây trước. Hàm mục tiêu tối ưu hóa bao gồm hàm mất mát và thành phần chính quy hóa (Regularization):

$$\mathcal{L} = \sum_{i=1}^{n} \ell(y_i, \hat{y}_i) + \sum_{k=1}^{K} \Omega(f_k), \quad \Omega(f) = \gamma T + \frac{1}{2}\lambda \|w\|^2$$

Trong đó $T$ là số nút lá, $w$ là trọng số nút lá, $\gamma$ và $\lambda$ là hệ số chính quy hóa.

Xử lý mất cân bằng lớp trong XGBoost: tham số `scale_pos_weight` = số mẫu âm / số mẫu dương ≈ 3.52, tương đương với `class_weight='balanced'`.

---

## 2.6. Phương pháp xử lý Mất cân bằng dữ liệu (Class Imbalance)

### 2.6.1. Phân tích tác động của mất cân bằng dữ liệu

Tập dữ liệu có tỷ lệ mất cân bằng 3.52:1 (77.88% Non-Default vs 22.12% Default). Mất cân bằng dữ liệu gây ra hiện tượng **Accuracy Paradox**: một mô hình đơn giản luôn dự báo Non-Default đạt Accuracy = 77.88% mà không học được bất kỳ mẫu nào liên quan đến Default.

Hậu quả kỹ thuật: mô hình có xu hướng tối ưu chỉ số tổng thể (Accuracy) bằng cách thiên lệch về lớp đa số, dẫn đến Recall thấp đối với lớp Default — chính là nhóm khách hàng cần phát hiện trong bài toán tín dụng.

### 2.6.2. Các phương pháp xử lý được áp dụng

**Phương pháp A — Class Weighting (được áp dụng chính):**  
Điều chỉnh trọng số mất mát (`class_weight='balanced'`) để mô hình phạt nặng hơn khi bỏ sót các mẫu Default. Trọng số được tính tự động: $w_k = \frac{n_{\text{total}}}{K \cdot n_k}$.  
*Ưu điểm*: Không thay đổi phân bố dữ liệu gốc, tương thích với Cross-Validation, reproducible.

**Phương pháp B — SMOTE (không áp dụng trong thực nghiệm chính):**  
SMOTE (Synthetic Minority Over-sampling Technique) tạo mẫu giả lập cho lớp thiểu số bằng cách nội suy tuyến tính giữa các điểm dữ liệu thật. *Lưu ý quan trọng*: SMOTE chỉ được áp dụng **bên trong pipeline Cross-Validation** (trên fold train), không bao giờ trên tập test, để tránh Data Leakage thống kê (thông tin từ mẫu giả lập có thể phản ánh phân bố test). Trong thực nghiệm này, `imbalanced-learn` không được cài đặt sẵn trong môi trường dự án; do đó SMOTE không được thử nghiệm trong thực nghiệm chính (Xem Mục 3.4.1 để biết phân tích chi tiết).

**Phương pháp C — Threshold Tuning (được áp dụng):**  
Ngưỡng phân loại mặc định 0.50 không tối ưu trong bối cảnh mất cân bằng. Phân tích Threshold được thực hiện trên **out-of-fold predictions** (dự báo ngoài fold trong Cross-Validation trên tập Train — không phải tập Test) để không vi phạm nguyên tắc No-Leakage.

---

## 2.7. Phương pháp Đánh giá mô hình và Lựa chọn mô hình

### 2.7.1. Hệ thống chỉ số đánh giá đa chiều

Với bài toán phân loại nhị phân mất cân bằng, hệ thống chỉ số được thiết kế theo bốn nhóm:

**Nhóm 1 — Từ ma trận nhầm lẫn (tại ngưỡng cụ thể):**

Từ Confusion Matrix $\{TP, TN, FP, FN\}$:

| | Dự báo: Default | Dự báo: Non-Default |
|---|---|---|
| **Thực tế: Default** | TP (True Positive) | FN (False Negative) |
| **Thực tế: Non-Default** | FP (False Positive) | TN (True Negative) |

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

$$\text{Precision} = \frac{TP}{TP + FP} \quad \text{(độ chính xác khi dự báo Default)}$$

$$\text{Recall} = \frac{TP}{TP + FN} \quad \text{(tỷ lệ phát hiện Default thực tế)}$$

$$\text{F1-Score} = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

**Nhóm 2 — Đánh giá đường cong (không phụ thuộc ngưỡng):**

- **ROC-AUC**: Diện tích dưới đường cong ROC (True Positive Rate vs. False Positive Rate trên mọi ngưỡng). Giá trị $\in [0.5, 1.0]$, đo khả năng phân biệt hai lớp tổng thể.

- **PR-AUC** (Average Precision): Diện tích dưới đường cong Precision-Recall. Với dữ liệu mất cân bằng, **PR-AUC phản ánh chính xác hơn ROC-AUC** về khả năng phát hiện lớp thiểu số (Default), vì PR-AUC chú trọng vào hiệu năng trên chính lớp đó.

**Lý do ưu tiên PR-AUC:**  
Với dataset 22.12% Default, một mô hình ngẫu nhiên có PR-AUC ≈ 0.22 trong khi ROC-AUC ≈ 0.50. Do đó PR-AUC cung cấp thông tin phân biệt tốt hơn khi lớp thiểu số là trọng tâm.

### 2.7.2. Phân tích Ma trận nhầm lẫn và đánh đổi nghiệp vụ

Trong bài toán tín dụng, hai loại lỗi phân loại có chi phí nghiệp vụ không đối xứng:
- **False Negative (FN)**: Bỏ sót khách hàng thực sự vỡ nợ → Ngân hàng chấp nhận sai khoản vay rủi ro cao → **Chi phí tài chính trực tiếp**.
- **False Positive (FP)**: Cảnh báo nhầm khách hàng tốt → Từ chối hoặc hạn chế tín dụng sai → Chi phí cơ hội và ảnh hưởng khách hàng.

Do đó, **Recall của lớp Default** được coi trọng hơn Precision trong bối cảnh đề tài, song song với PR-AUC làm chỉ số tổng hợp.

### 2.7.3. Phương pháp Cross-Validation và Tối ưu siêu tham số

**Chiến lược Cross-Validation:**  
Sử dụng `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` — phân tầng đảm bảo mỗi fold có tỷ lệ Default ≈ 22.13%.

**Phương pháp tối ưu tham số — RandomizedSearchCV:**  
`GridSearchCV` với không gian tham số lớn sinh hàng nghìn tổ hợp, không thực tế về thời gian. `RandomizedSearchCV(n_iter=25, scoring='average_precision', cv=5)` khám phá không gian rộng trong thời gian hợp lý với 25 tổ hợp tham số ngẫu nhiên, đủ cho mục tiêu học thuật.

*Lưu ý*: Tối ưu tham số chỉ thực hiện trên tập Train qua Cross-Validation; tập Test không tham gia.

### 2.7.4. Tiêu chí lựa chọn mô hình

Mô hình được chọn dựa trên thứ tự ưu tiên:
1. **PR-AUC** cao nhất (tiêu chí ưu tiên với dữ liệu mất cân bằng).
2. **CV PR-AUC** ổn định (thể hiện độ tin cậy của kết quả).
3. **Recall** của lớp Default cao (giảm thiểu bỏ sót khách hàng rủi ro).
4. **F1-Score** cân bằng giữa Precision và Recall.
5. **Khả năng tích hợp SHAP** (TreeExplainer tối ưu cho tree-based models).

---

## 2.8. Phương pháp giải thích mô hình với SHAP

### 2.8.1. Phương pháp phân tích đóng góp đặc trưng cấp tổng thể (Global Explanation)

SHAP (SHapley Additive exPlanations) dựa trên lý thuyết Shapley Value từ lý thuyết trò chơi hợp tác, cung cấp giải thích **cộng tính** (additive) cho dự đoán của mô hình:

$$f(x) = \phi_0 + \sum_{i=1}^{M} \phi_i$$

Trong đó $\phi_0$ là giá trị cơ sở (dự báo trung bình khi không có thông tin đặc trưng) và $\phi_i$ là đóng góp của đặc trưng $i$ vào dự đoán cho mẫu $x$.

Giá trị Shapley chính thức:

$$\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(|N| - |S| - 1)!}{|N|!} \left[ f(S \cup \{i\}) - f(S) \right]$$

**Phương pháp TreeExplainer:**  
Đối với mô hình XGBoost (tree-based), `shap.TreeExplainer` tính toán **exact Shapley values** (không phải xấp xỉ như KernelExplainer), khai thác cấu trúc cây để tính toán hiệu quả trong $O(TLD^2)$ thay vì $O(2^M)$ (T cây, L lá, D độ sâu).

**Global Feature Importance:**  
Được tổng hợp bằng Mean |SHAP Value| trên toàn tập dữ liệu:
$$\text{Importance}(i) = \frac{1}{n}\sum_{j=1}^{n} |\phi_i^{(j)}|$$

Trực quan hóa bằng SHAP Bar Plot và SHAP Beeswarm Plot (hiển thị cả giá trị và hướng tác động).

### 2.8.2. Phương pháp phân tích đóng góp đặc trưng cấp cá thể (Local Explanation)

**Local Explanation** phân tích đóng góp của từng đặc trưng cho một dự đoán cụ thể của một khách hàng cụ thể, sử dụng Waterfall Plot để trực quan hóa từng bước tích lũy SHAP value từ giá trị cơ sở đến kết quả dự báo cuối cùng.

**Lưu ý phương pháp:**  
- SHAP values trong mô hình XGBoost ở **không gian log-odds** (raw margin), không phải không gian xác suất. Do đó, SHAP value dương không đồng nghĩa với tăng xác suất tuyến tính, mà tăng log-odds.
- Dependence Plots cho thấy **mối liên hệ trong mô hình**, không phải quan hệ nhân quả. Cách diễn đạt chính xác là "có liên hệ với rủi ro" thay vì "gây ra vỡ nợ".
- SHAP được tính trên **tập Test** (độc lập) để đảm bảo không Data Leakage.

---

## 2.9. Phân tích yêu cầu và Thiết kế kiến trúc ứng dụng Web Prototype

### 2.9.1. Yêu cầu chức năng, phi chức năng và luồng xử lý hệ thống

**Yêu cầu chức năng:**
- Nhập thông tin khách hàng qua biểu mẫu giao diện Web (23 trường đầu vào).
- Tự động thực hiện Feature Engineering và chuẩn hóa theo đúng pipeline huấn luyện.
- Dự báo xác suất vỡ nợ ước lượng bằng mô hình XGBoost Tuned chính thức.
- Hiển thị phân loại mức rủi ro thử nghiệm (Low/Medium/High Risk).
- Tính toán và hiển thị giải thích SHAP thời gian thực (Top 10 yếu tố đóng góp).

**Yêu cầu phi chức năng:**
- Nhất quán hoàn toàn với pipeline huấn luyện (Training-Serving Consistency).
- Thời gian phản hồi cho mỗi dự báo < 5 giây (bao gồm SHAP).
- Giao diện trực quan, phù hợp với mục đích Demo/Bảo vệ đồ án.
- Khả năng tái lập (reproducible) — cùng input luôn cho cùng output.

**Luồng xử lý:**  
`Nhập liệu (Web Form)` → `Validate đầu vào` → `Categorical Mapping` → `Feature Engineering` → `RobustScaler.transform()` → `XGBoost.predict_proba()` → `Threshold 0.60` → `Phân loại rủi ro` → `SHAP TreeExplainer` → `Hiển thị kết quả`

### 2.9.2. Thiết kế kiến trúc phần mềm DSS Prototype

**Kiến trúc phân tầng hai lớp:**
- **Frontend (app.py)**: Streamlit application xử lý UI, biểu mẫu nhập liệu, hiển thị kết quả và biểu đồ.
- **Backend (src/prediction.py)**: Module inference độc lập, không phụ thuộc Streamlit, chứa toàn bộ logic dự báo và SHAP.

**Nguyên lý Training-Serving Consistency:**  
Bộ đặc trưng, công thức Feature Engineering, mã hóa phân loại và bộ chuẩn hóa (`robust_scaler.pkl`) trong module Serving hoàn toàn khớp với pipeline huấn luyện từ Tuần 4–8.

---

*Phần cuối Chương 2 — Chương tiếp theo trình bày kết quả thực nghiệm cụ thể.*
