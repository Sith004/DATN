# CHƯƠNG 3. CÀI ĐẶT THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ

**Đề tài:** Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  
**Sinh viên:** Nguyễn Trọng Thể — MSSV: 1150080117  
**GVHD:** TS. Dương Thị Thúy Nga  
*[Bản nháp Markdown — nguồn cho file Word chính thức]*

---

## Mở đầu Chương 3

Chương 3 trình bày toàn bộ kết quả thực nghiệm theo từng giai đoạn của quy trình nghiên cứu được mô tả trong Chương 2. Mỗi kết quả được cung cấp kèm nguồn gốc kiểm chứng (tên file báo cáo/CSV/notebook tương ứng) và phân tích ý nghĩa. Các bảng số liệu lấy trực tiếp từ kết quả chạy thực nghiệm đã lưu; mọi số liệu chưa được xác minh đều được ghi nhận rõ ràng bằng `[CẦN XÁC MINH]`.

---

## 3.1. Môi trường phát triển và Thư viện cài đặt

### 3.1.1. Phần cứng và Hệ điều hành

| Thành phần | Thông tin |
|---|---|
| Hệ điều hành | Windows 11 (x64) |
| Python | 3.x (môi trường ảo `.venv`) |
| Công cụ lập trình | Jupyter Notebook, VS Code, PowerShell |

### 3.1.2. Thư viện chính và phiên bản

| Thư viện | Vai trò |
|---|---|
| `pandas` | Xử lý dữ liệu dạng bảng (DataFrame) |
| `numpy` | Tính toán số học và ma trận |
| `scikit-learn` | Mô hình ML, Pipeline, Metrics, Preprocessing |
| `xgboost` | XGBoost Classifier |
| `shap (0.52.0)` | SHAP TreeExplainer, Global & Local Explanation |
| `matplotlib`, `seaborn` | Trực quan hóa dữ liệu và kết quả |
| `streamlit` | Web Prototype Framework |
| `joblib`, `pickle` | Lưu/tải model artifacts |
| `plotly` | Biểu đồ tương tác (Gauge chart) trong ứng dụng |

### 3.1.3. Cấu trúc mã nguồn và dữ liệu

| Thư mục/File | Nội dung |
|---|---|
| `data/raw/UCI_Credit_Card.csv` | Dữ liệu thô gốc (30.000 bản ghi) |
| `data/processed/X_train_fe.csv` | Tập Train sau Feature Engineering (23.972 × 33) |
| `data/processed/X_test_fe.csv` | Tập Test sau Feature Engineering (5.993 × 33) |
| `data/processed/y_train.csv` | Nhãn Train (23.972 quan sát) |
| `data/processed/y_test.csv` | Nhãn Test (5.993 quan sát) |
| `models/final_candidate_model.pkl` | Mô hình XGBoost Tuned chính thức |
| `models/robust_scaler.pkl` | RobustScaler fit trên Train |
| `src/` | Module Python cốt lõi |
| `notebooks/` | Jupyter Notebooks với output đầy đủ |
| `reports/` | Báo cáo kỹ thuật từng giai đoạn |

---

## 3.2. Kết quả kiểm duyệt dữ liệu EDA và Cài đặt Tiền xử lý

### 3.2.1. Kết quả thực nghiệm kiểm duyệt chất lượng dữ liệu (Data Audit)

*Nguồn: `reports/EDA_Report.md`, Notebook `01_Data_Audit_EDA.ipynb`*

**Kết quả tổng quan:**

| Chỉ số kiểm tra | Kết quả |
|---|---|
| Kích thước dữ liệu gốc | 30.000 quan sát × 25 cột |
| Số ô khuyết (Missing values) | 0 (0,00%) |
| Kiểu dữ liệu | 25/25 cột là `int64` |
| Trùng lặp 100% (kể cả ID) | 0 dòng |
| Trùng lặp đặc trưng (bỏ qua ID) | **35 dòng** |
| Mã EDUCATION bất thường {0, 5, 6} | 345 mẫu (1,15%) |
| Mã MARRIAGE bất thường {0} | 54 mẫu (0,18%) |

**Phân bố biến mục tiêu:**

Bảng 3.1. Phân bố biến mục tiêu `default.payment.next.month` (trước xử lý)

| Giá trị | Ý nghĩa | Số lượng | Tỷ lệ (%) |
|---|---|---|---|
| **0** | Không vỡ nợ (Non-Default) | 23.364 | 77,88% |
| **1** | Vỡ nợ (Default) | 6.636 | 22,12% |
| **Tổng** | | **30.000** | **100,00%** |

*[Chèn Hình 3.1: Biểu đồ phân bố biến mục tiêu — nguồn: `reports/figures/target_distribution.png`]*

**Nhận xét:** Tỷ lệ mất cân bằng lớp (Imbalance Ratio) = 3,52:1. Một mô hình ngây thơ luôn dự báo Non-Default sẽ đạt Accuracy = 77,88% mà không học được bất kỳ mẫu vỡ nợ nào — đây là lý do ưu tiên PR-AUC và Recall thay vì Accuracy làm chỉ số chính.

**Thống kê mô tả các biến số học (Bảng 3.2):**

| Biến | Mean | Std | Min | Median | Max | Skewness |
|---|---|---|---|---|---|---|
| `LIMIT_BAL` | 167.484 | 129.748 | 10.000 | 140.000 | 1.000.000 | 0,99 |
| `AGE` | 35,49 | 9,22 | 21 | 34 | 79 | 0,73 |
| `BILL_AMT1` | 51.223 | 73.636 | -165.580 | 22.382 | 964.511 | 2,66 |
| `PAY_AMT1` | 5.664 | 16.563 | 0 | 2.100 | 873.552 | **14,67** |
| `PAY_AMT2` | 5.921 | 23.041 | 0 | 2.009 | 1.684.259 | **30,45** |

*Ghi chú: Đơn vị tiền tệ là NTD (Đài loan New Dollar). Skewness > 10 ở nhóm `PAY_AMT` là lý do chọn RobustScaler.*

*[Chèn Hình 3.2: Biểu đồ phân bố nhân khẩu học — nguồn: `reports/figures/demographic_distribution.png`]*

**Các phát hiện tương quan chính (Hình 3.3):**
- `PAY_0`: $r = +0,325$ — biến tương quan mạnh nhất với Default.
- `LIMIT_BAL`: $r = -0,154$ — hạn mức cao liên quan với rủi ro thấp hơn.
- Nhóm `BILL_AMT1..6`: $r(\text{BILL\_AMT1}, \text{BILL\_AMT2}) = 0,951$ — đa cộng tuyến nghiêm trọng.

*[Chèn Hình 3.3: Ma trận tương quan Pearson — nguồn: `reports/figures/correlation_heatmap.png`]*

### 3.2.2. Kết quả thực nghiệm làm sạch dữ liệu và chuẩn hóa

*Nguồn: `reports/Preprocessing_Report.md`, Notebook `02_Preprocessing.ipynb`*

**Kết quả xử lý làm sạch dữ liệu:**

| Bước xử lý | Quyết định | Kết quả |
|---|---|---|
| Loại bỏ cột ID | Loại khỏi tập X | ID không có giá trị tiên đoán |
| Kiểm tra nhóm trùng lặp đặc trưng | 35 nhóm, 70 dòng | 100% nhóm nhất quán nhãn |
| Loại bỏ 35 dòng trùng lặp dư thừa | Giữ bản đại diện đầu tiên | 29.965 quan sát |
| Gom EDUCATION {0,5,6} → 4 | 345 mẫu → nhóm Others | Đưa về 4 nhóm chuẩn |
| Gom MARRIAGE {0} → 3 | 54 mẫu → nhóm Others | Đưa về 3 nhóm chuẩn |

**Kết quả phân chia Train/Test:**

Bảng 3.3. Kết quả phân chia tập Train/Test (Stratified 80/20, random_state=42)

| Tập dữ liệu | Số quan sát | Tỷ lệ (%) | Non-Default | Default | Tỷ lệ Default |
|---|---|---|---|---|---|
| **TRAIN** | **23.972** | 80,00% | 18.668 | 5.304 | **22,13%** |
| **TEST** | **5.993** | 20,00% | 4.667 | 1.326 | **22,12%** |
| **Tổng** | **29.965** | 100,00% | 23.335 | 6.630 | **22,13%** |

*Nhận xét: Phân tầng hoạt động hoàn hảo — tỷ lệ Default nhất quán 22,13% ở cả hai tập.*

**Kết quả kiểm tra Data Leakage — 7/7 tiêu chí: ✓ PASS**  
*(Xem Bảng chi tiết tại Mục 2.3.1)*

### 3.2.3. Kết quả thực nghiệm Feature Engineering

*Nguồn: `reports/Feature_Engineering_Report.md`, Notebook `03_Feature_Engineering.ipynb`*

**Kết quả kiểm tra chất lượng dữ liệu sau Feature Engineering:**

Bảng 3.4. Kết quả kiểm định chất lượng ma trận đặc trưng sau Feature Engineering

| Chỉ số kiểm tra | X_train_fe | X_test_fe | Trạng thái |
|---|---|---|---|
| Số dòng | 23.972 | 5.993 | ✓ PASS |
| Số cột (features) | **33** | **33** | ✓ PASS |
| Ô khuyết (NaN) | 0 | 0 | ✓ PASS |
| Giá trị vô cực (Inf) | 0 | 0 | ✓ PASS |
| Biến mục tiêu có trong X | Không | Không | ✓ PASS |
| Cột ID có trong X | Không | Không | ✓ PASS |
| Data Leakage (Scaler fit Train only) | PASS | Transform only | ✓ PASS |

**Thống kê các biến tổng hợp mới trên tập Train (Bảng 3.5):**

| Biến mới | Mean | Median | Min | Max | Skewness |
|---|---|---|---|---|---|
| `UTILIZATION_RATE_SEPT` | 0,4243 | 0,3134 | -0,6156 | 6,4553 | 1,02 |
| `UTILIZATION_RATE_MEAN` | 0,3746 | 0,2851 | -0,2723 | 5,3644 | 1,15 |
| `PAY_RATIO_SEPT` | 0,8841 | 1,0000 | 0,0000 | 1,0000 | -1,45 |
| `PAY_RATIO_MEAN` | 0,8624 | 0,9854 | 0,0000 | 1,0000 | -1,68 |
| `MAX_PAY_DELAY` | 0,6832 | 0,0000 | -2,0000 | 8,0000 | 1,62 |
| `COUNT_LATE_PAYMENT` | 0,8041 | 0,0000 | 0,0000 | 6,0000 | 1,95 |
| `MEAN_BILL_AMT` | 44.982 | 21.114 | -56.043 | 893.021 | 2,75 |
| `MEAN_PAY_AMT` | 5.275 | 2.399 | 0 | 321.200 | 6,84 |
| `BILL_TREND` | 0,0784 | 0,0021 | -3,2104 | 4,8512 | 1,48 |
| `PAY_TREND` | 0,0028 | 0,0000 | -3,5100 | 4,1200 | 0,85 |

---

## 3.3. Thực nghiệm Xây dựng mô hình cơ sở (Baseline) và So sánh mô hình

### 3.3.1. Kết quả huấn luyện mô hình cơ sở — Logistic Regression

*Nguồn: `reports/Model_Baseline_Report.md`, `reports/model_baseline_results.csv`, Notebook `04_Model_Baseline.ipynb`*

Bảng 3.6. Kết quả mô hình Logistic Regression trên tập Test (5.993 mẫu)

| Cấu hình | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| LR Default | 0,8106 | 0,6610 | 0,2956 | 0,4085 | 0,7492 | 0,5162 |
| LR Balanced | 0,7469 | 0,4466 | 0,6018 | 0,5127 | 0,7514 | 0,5123 |

**Ma trận nhầm lẫn — LR Default:**

| | Dự báo: Non-Default | Dự báo: Default |
|---|---|---|
| **Thực tế: Non-Default** | TN = 4.466 | FP = 201 |
| **Thực tế: Default** | FN = 934 | TP = 392 |

**Ma trận nhầm lẫn — LR Balanced:**

| | Dự báo: Non-Default | Dự báo: Default |
|---|---|---|
| **Thực tế: Non-Default** | TN = 3.678 | FP = 989 |
| **Thực tế: Default** | FN = 528 | TP = 798 |

**Phân tích:** `class_weight='balanced'` tăng Recall từ 0,2956 lên 0,6018 (+103%) nhưng giảm Precision từ 0,6610 xuống 0,4466 — phản ánh đánh đổi điển hình khi tăng độ nhạy phát hiện Default. PR-AUC của cả hai cấu hình tương đương (~0,51), xác nhận mô hình tuyến tính có năng lực phân biệt lớp hạn chế.

### 3.3.2. Kết quả huấn luyện và so sánh các mô hình — Decision Tree, Random Forest, XGBoost

*Nguồn: `reports/Model_Baseline_Report.md`, `reports/Week7_Ensemble_Models_Report.md`, Notebook `04_Model_Baseline.ipynb`, `05_Ensemble_Models.ipynb`*

Bảng 3.7. Bảng so sánh toàn bộ 7 mô hình Baseline và Ensemble trên tập Test (trước Tuning)

| Mô hình | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| Logistic Regression (Default) | 0,8106 | 0,6610 | 0,2956 | 0,4085 | 0,7492 | 0,5162 |
| Logistic Regression (Balanced) | 0,7469 | 0,4466 | 0,6018 | 0,5127 | 0,7514 | 0,5123 |
| Decision Tree (Default) | 0,7267 | 0,3884 | 0,4095 | 0,3987 | 0,6130 | 0,2897 |
| Decision Tree (Balanced) | 0,7262 | 0,3784 | 0,3695 | 0,3739 | 0,5986 | 0,2796 |
| Random Forest (Default) | 0,8143 | 0,6364 | 0,3748 | 0,4718 | 0,7659 | 0,5381 |
| Random Forest (Balanced) | 0,7973 | 0,5471 | 0,4864 | 0,5150 | 0,7661 | 0,5297 |
| **XGBoost (Baseline)** | **0,8201** | **0,6766** | **0,3582** | **0,4684** | **0,7792** | **0,5611** |

*[Chèn Hình 3.4: ROC Curve so sánh 7 mô hình — nguồn: `reports/figures/week7_roc_curve_comparison.png`]*

*[Chèn Hình 3.5: Precision-Recall Curve so sánh 7 mô hình — nguồn: `reports/figures/week7_pr_curve_comparison.png`]*

**Nhận xét chính:**
1. **Decision Tree** có PR-AUC thấp nhất (0,29–0,28) — cây đơn lẻ không phù hợp với dữ liệu phức tạp và mất cân bằng.
2. **Random Forest** cải thiện đáng kể so với Logistic Regression và Decision Tree về ROC-AUC và PR-AUC nhờ cơ chế Bagging.
3. **XGBoost Baseline** đạt PR-AUC cao nhất (0,5611) và ROC-AUC cao nhất (0,7792) — xác nhận tiềm năng của Gradient Boosting cho bài toán này, ngay cả khi chưa tối ưu tham số.

---

## 3.4. Thực nghiệm Xử lý mất cân bằng dữ liệu và Tối ưu siêu tham số

### 3.4.1. Kết quả so sánh hiệu năng Class Weighting và Threshold Tuning

*Nguồn: `reports/Week8_Tuning_Model_Selection_Report.md`, Notebook `06_Hyperparameter_Tuning.ipynb`*

**Class Weighting:**  
Tham số `class_weight='balanced'` được áp dụng cho cả Random Forest và XGBoost (qua `scale_pos_weight ≈ 3.52`). Kết quả cho thấy class weighting thường tăng Recall nhưng giảm Precision — phản ánh đánh đổi kinh điển trong phát hiện lớp thiểu số.

**SMOTE:**  
Thư viện `imbalanced-learn` không được cài đặt trong môi trường `.venv` của dự án trong giai đoạn thực nghiệm chính. Do đó, SMOTE không được thử nghiệm. Class weighting được sử dụng làm phương pháp xử lý mất cân bằng chính.

**Threshold Tuning:**  
Phân tích ngưỡng phân loại được thực hiện dựa trên **out-of-fold predictions** (không dùng Test set). Kết quả tối ưu ngưỡng theo OOF F1-Score:

| Mô hình | Ngưỡng tối ưu (OOF F1) |
|---|---|
| Random Forest (Default) Tuned | 0,30 |
| Random Forest (Balanced) Tuned | 0,55 |
| XGBoost Tuned | **0,60** |

### 3.4.2. Kết quả tối ưu siêu tham số (Hyperparameter Tuning)

**Phương pháp:** `RandomizedSearchCV(n_iter=25, scoring='average_precision', cv=StratifiedKFold(5))`

Bảng 3.8. Siêu tham số tối ưu và điểm CV cho 3 mô hình Ensemble sau Tuning

| Mô hình | CV PR-AUC (best) | Tham số tối ưu chính |
|---|---|---|
| RF (Default) Tuned | 0,5656 (±0,0088) | n_estimators=250, max_depth=10, max_features=0.5 |
| RF (Balanced) Tuned | 0,5627 (±0,0096) | n_estimators=250, max_depth=10, max_features=0.5 |
| **XGBoost Tuned** | **0,5646 (±0,0122)** | n_estimators=250, lr=0.03, max_depth=6, subsample=0.6, colsample_bytree=0.9, gamma=0.3, reg_alpha=0.5, reg_lambda=1.0 |

**Kết quả so sánh Trước/Sau Tuning cho XGBoost:**

Bảng 3.9. Hiệu năng XGBoost trên tập Test: trước và sau Hyperparameter Tuning

| Chỉ số | Trước Tuning | Sau Tuning | Thay đổi |
|---|---|---|---|
| Accuracy | 0,8201 | **0,7686** | -0,0515 |
| Precision | 0,6766 | **0,4820** | -0,1946 |
| Recall | 0,3582 | **0,6161** | **+0,2579** |
| F1-Score | 0,4684 | **0,5409** | +0,0725 |
| ROC-AUC | 0,7792 | **0,7769** | -0,0023 |
| PR-AUC | 0,5611 | **0,5620** | **+0,0009** |

**Phân tích:** Sau tuning với threshold=0,60, XGBoost Tuned hi sinh Accuracy và Precision để đổi lấy Recall tăng mạnh từ 0,3582 lên 0,6161 (+25,79 điểm phần trăm). Điều này thể hiện rõ đánh đổi nghiệp vụ: phát hiện thêm 61,61% khách hàng vỡ nợ thực sự, chấp nhận cảnh báo nhầm một số khách hàng tốt (FP tăng). PR-AUC vẫn đạt cao nhất toàn hệ thống (0,5620).

---

## 3.5. Bảng tổng hợp đánh giá mô hình và Lựa chọn mô hình

### 3.5.1. Bảng so sánh đa chỉ số — Toàn bộ 10 cấu hình mô hình

*Nguồn: `reports/Model_Baseline_Report.md`, `reports/Week7_Ensemble_Models_Report.md`, `reports/Week8_Tuning_Model_Selection_Report.md`*

Bảng 3.10. Bảng tổng hợp so sánh hiệu năng toàn bộ mô hình trên tập Test (5.993 mẫu)

| Mô hình | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| LR Default | 0,8106 | 0,6610 | 0,2956 | 0,4085 | 0,7492 | 0,5162 |
| LR Balanced | 0,7469 | 0,4466 | 0,6018 | 0,5127 | 0,7514 | 0,5123 |
| DT Default | 0,7267 | 0,3884 | 0,4095 | 0,3987 | 0,6130 | 0,2897 |
| DT Balanced | 0,7262 | 0,3784 | 0,3695 | 0,3739 | 0,5986 | 0,2796 |
| RF Default | 0,8143 | 0,6364 | 0,3748 | 0,4718 | 0,7659 | 0,5381 |
| RF Balanced | 0,7973 | 0,5471 | 0,4864 | 0,5150 | 0,7661 | 0,5297 |
| XGBoost Baseline | 0,8201 | 0,6766 | 0,3582 | 0,4684 | 0,7792 | 0,5611 |
| RF Default Tuned | 0,8206 | 0,6785 | 0,3597 | 0,4702 | 0,7773 | 0,5610 |
| RF Balanced Tuned | 0,7764 | 0,4956 | 0,5950 | 0,5408 | 0,7753 | 0,5584 |
| **XGBoost Tuned** ⭐ | **0,7686** | **0,4820** | **0,6161** | **0,5409** | **0,7769** | **0,5620** |

*[Chèn Hình 3.6: Feature Importance Random Forest — nguồn: `reports/figures/week7_random_forest_feature_importance.png`]*  
*[Chèn Hình 3.7: Feature Importance XGBoost — nguồn: `reports/figures/week7_xgboost_feature_importance.png`]*

### 3.5.2. Phân tích lý do lựa chọn XGBoost Tuned làm mô hình chính thức

Bảng 3.11. So sánh 3 mô hình Tuned theo tiêu chí lựa chọn

| Tiêu chí | RF Default Tuned | RF Balanced Tuned | **XGBoost Tuned** |
|---|---|---|---|
| **PR-AUC** (Test) | 0,5610 | 0,5584 | **0,5620** ★ |
| **CV PR-AUC** | 0,5656 | 0,5627 | **0,5646** |
| **Recall** | 0,3597 | 0,5950 | **0,6161** ★ |
| F1-Score | 0,4702 | 0,5408 | **0,5409** |
| ROC-AUC | 0,7773 | 0,7753 | 0,7769 |
| Tương thích SHAP TreeExplainer | ✓ | ✓ | ✓ |

**Quyết định lựa chọn:**  
**XGBoost Tuned với threshold = 0,60** được lựa chọn là mô hình chính thức (`final_candidate_model.pkl`) vì:
1. **PR-AUC cao nhất** (0,5620) trong tất cả các cấu hình đã thử nghiệm.
2. **Recall cao nhất** (0,6161) — phát hiện 61,61% khách hàng vỡ nợ thực tế, vượt trội so với mọi cấu hình khác.
3. CV PR-AUC ổn định (0,5646 ± 0,0122) — kết quả đáng tin cậy.
4. Tương thích hoàn hảo với SHAP TreeExplainer.

> **Lưu ý giới hạn:** Ngưỡng 0,60 được chọn dựa trên tối ưu OOF F1 trên tập Train (không dùng Test). Trong triển khai thực tế, ngưỡng cần điều chỉnh theo cost matrix cụ thể của từng tổ chức tín dụng.

---

## 3.6. Kết quả thực nghiệm giải thích mô hình bằng SHAP

*Nguồn: `reports/Week9_SHAP_Model_Interpretability_Report.md`, `reports/week9_shap_feature_importance.csv`, Notebook `07_Model_Interpretability.ipynb`*

**Thiết lập:** SHAP TreeExplainer áp dụng trên tập X_test (5.993 mẫu × 33 features). SHAP values trong không gian log-odds với expected_value = 0,089860.

### 3.6.1. Kết quả Global Feature Importance (Top 10)

Bảng 3.12. Top 10 đặc trưng quan trọng nhất theo Mean |SHAP Value| (trên X_test)

| Rank | Đặc trưng | Mean\|SHAP\| | Nhóm | Ý nghĩa |
|---|---|---|---|---|
| 1 | `MAX_PAY_DELAY` | **0,4494** | Feature mới | Số tháng trậm trả tối đa 6 tháng |
| 2 | `PAY_0` | 0,2797 | Gốc | Trạng thái thanh toán T9/2005 |
| 3 | `COUNT_LATE_PAYMENT` | 0,1211 | Feature mới | Số tháng bị trậm trả ≥ 1 |
| 4 | `BILL_AMT1` | 0,1126 | Gốc | Dư nợ hóa đơn T9/2005 |
| 5 | `UTILIZATION_RATE_SEPT` | 0,0942 | Feature mới | Tỷ lệ sử dụng hạn mức T9 |
| 6 | `LIMIT_BAL` | 0,0921 | Gốc | Hạn mức tín dụng |
| 7 | `PAY_AMT2` | 0,0817 | Gốc | Số tiền trả T8/2005 |
| 8 | `PAY_AMT3` | 0,0725 | Gốc | Số tiền trả T7/2005 |
| 9 | `PAY_AMT1` | 0,0719 | Gốc | Số tiền trả T9/2005 |
| 10 | `MEAN_PAY_AMT` | 0,0639 | Feature mới | Trung bình tiền trả 6 tháng |

*[Chèn Hình 3.8: SHAP Bar Plot — nguồn: `reports/figures/week9_shap_bar.png`]*

*[Chèn Hình 3.9: SHAP Beeswarm Plot — nguồn: `reports/figures/week9_shap_beeswarm.png`]*

**Nhận xét nổi bật:**
1. **Lịch sử trậm trả là yếu tố quyết định:** Nhóm `MAX_PAY_DELAY`, `PAY_0`, `COUNT_LATE_PAYMENT` chiếm phần lớn tổng trọng số SHAP, xác nhận rằng hành vi thanh toán là tín hiệu dự báo mạnh nhất.
2. **Feature Engineering có giá trị thực tế:** 4 trong 10 biến quan trọng nhất (`MAX_PAY_DELAY` rank 1, `COUNT_LATE_PAYMENT` rank 3, `UTILIZATION_RATE_SEPT` rank 5, `MEAN_PAY_AMT` rank 10) là biến được tạo mới ở Tuần 5. Đáng chú ý, `MAX_PAY_DELAY` (biến tổng hợp) có Mean|SHAP| = 0,4494, gấp 1,6 lần biến gốc `PAY_0` (0,2797).
3. **Hạn mức tín dụng là yếu tố bảo vệ:** `LIMIT_BAL` cao liên hệ với SHAP âm — giảm xác suất vỡ nợ.

### 3.6.2. Kết quả phân tích Dependence Plots — Top 5 đặc trưng

**MAX_PAY_DELAY (Rank 1):**  
SHAP âm khi MAX_PAY_DELAY = 0 (chưa từng trậm trả). Bước nhảy phi tuyến rõ rệt khi MAX_PAY_DELAY ≥ 2 tháng — SHAP tăng mạnh dương, rủi ro vỡ nợ tăng phi tuyến.  
*[Chèn Hình 3.10: Dependence Plot MAX_PAY_DELAY — nguồn: `reports/figures/week9_dependence_MAX_PAY_DELAY.png`]*

**PAY_0 (Rank 2):**  
PAY_0 ≤ 0 → SHAP âm (bảo vệ). PAY_0 = 2+ → SHAP dương lớn, rủi ro tăng mạnh.  
*[Chèn Hình 3.11: Dependence Plot PAY_0 — nguồn: `reports/figures/week9_dependence_PAY_0.png`]*

> ⚠️ **Lưu ý phương pháp:** Dependence Plots cho thấy **mối liên hệ trong mô hình**, không phải quan hệ nhân quả. Biểu đồ thể hiện: "khi đặc trưng X có giá trị cao, mô hình có xu hướng dự báo rủi ro cao hơn" — không phải "giá trị X cao **gây ra** vỡ nợ".

### 3.6.3. Kết quả Local Explanation — 3 ca điển hình

Bảng 3.13. Tóm tắt kết quả giải thích cá thể 3 hồ sơ đại diện

| Ca | Index | Xác suất | Ngưỡng | Dự báo | Thực tế | Đánh giá | Yếu tố rủi ro chính |
|---|---|---|---|---|---|---|---|
| High Risk | 3433 | **0,9616** | 0,60 | Default | Default | ✓ True Positive | MAX_PAY_DELAY, PAY_0, COUNT_LATE_PAYMENT |
| Low Risk | 1985 | **0,0284** | 0,60 | Non-Default | Non-Default | ✓ True Negative | LIMIT_BAL (âm), PAY_AMT2 (âm) |
| Near Threshold | 1753 | **0,6001** | 0,60 | Default | Non-Default | ✗ False Positive | MAX_PAY_DELAY, COUNT_LATE_PAYMENT |

*[Chèn Hình 3.12: Waterfall Plot — Ca High Risk — nguồn: `reports/figures/week9_waterfall_high_risk.png`]*  
*[Chèn Hình 3.13: Waterfall Plot — Ca Low Risk — nguồn: `reports/figures/week9_waterfall_low_risk.png`]*  
*[Chèn Hình 3.14: Waterfall Plot — Ca Near Threshold — nguồn: `reports/figures/week9_waterfall_near_threshold.png`]*

**Ca Near Threshold (idx=1753, prob=0,6001)** là ví dụ điển hình về trade-off khi chọn ngưỡng thấp (0,60 thay vì 0,50): mô hình phát hiện thêm nhiều Default thật, nhưng cũng phân loại sai một số khách hàng biên giới. Đây là hậu quả tất yếu của việc tối ưu Recall và là trade-off cần cân nhắc trong nghiệp vụ thực tế.

---

## 3.7. Cài đặt, Triển khai và Kiểm thử ứng dụng Web Prototype

*Nguồn: `reports/Week10_WebApp_Report.md`, `app.py`, `src/prediction.py`, `scripts/test_week10.py`*

### 3.7.1. Cài đặt giao diện người dùng và tích hợp mô hình ML

Ứng dụng Web Prototype (DSS — Decision Support System Prototype) được xây dựng bằng framework Streamlit, triển khai tại localhost (`http://localhost:8501`). Kiến trúc hai tầng:

**Tầng giao diện (app.py — 791 dòng):**  
- Tab 1 "Dự báo Rủi ro": Biểu mẫu nhập liệu 4 nhóm (23 trường), Gauge Chart tương tác (Plotly) hiển thị xác suất ước lượng, biểu đồ SHAP Bar thời gian thực.
- Tab 2 "Hướng dẫn & Thông tin": Kiến trúc hệ thống, giới hạn prototype.
- Sidebar: Thông số mô hình, bảng hiệu năng, Top 5 yếu tố rủi ro.

**Tầng suy luận (src/prediction.py — 319 dòng):**  
Thực hiện toàn bộ pipeline dự báo theo đúng thứ tự đã huấn luyện:

```
Nhập liệu thô → Categorical Mapping → Feature Engineering
→ RobustScaler.transform() → XGBoost.predict_proba()
→ Threshold 0.60 → Phân loại rủi ro (Low/Medium/High)
→ SHAP TreeExplainer (thời gian thực)
```

**Caching Streamlit (`@st.cache_resource`):**  
Mô hình và Scaler được nạp vào bộ nhớ một lần, cache toàn bộ phiên làm việc để giảm thời gian chờ.

**Hướng dẫn khởi chạy:**

```powershell
cd F:\DATN\project
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### 3.7.2. Kết quả kiểm thử Integration Test Suite

Bộ kiểm thử `scripts/test_week10.py` được thực thi và xác minh ngày 24/10/2026:

Bảng 3.14. Kết quả kiểm thử tích hợp 6 bài — tất cả PASS (Exit code: 0)

| # | Tên kiểm thử | Điều kiện PASS | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|
| 1 | Normal Customer | Feature count = 33, Non-Default | Prob = 11,89%, Non-Default, Low Risk | ✅ PASS |
| 2 | High-Risk Customer | Probability ≥ 60% | Prob = 78,22%, Default, High Risk | ✅ PASS |
| 3 | Low-Risk Customer | Probability < 30% | Prob = 18,96%, Non-Default, Low Risk | ✅ PASS |
| 4 | Feature Order Verification | 33 features khớp X_train_fe | VERIFIED (33 features match) | ✅ PASS |
| 5 | Direct Model Consistency | Difference < 1e-6 | Direct vs predict_single: Δ = 0,00e+00 | ✅ PASS |
| 6 | SHAP Explanation | SHAP shape = (33,) | Shape = (33,), E[f(X)] = 0,089860 | ✅ PASS |

---

## 3.8. Đánh giá tổng quan, Thảo luận và Hạn chế đề tài

### 3.8.1. Tổng hợp kết quả chính đạt được

1. **Tập dữ liệu**: UCI Credit Card (30.000 mẫu) được kiểm duyệt, làm sạch (29.965 mẫu sau loại trùng), chia Train/Test stratified 80/20, Feature Engineering 33 biến — không có Data Leakage.

2. **Mô hình tốt nhất**: XGBoost Tuned với threshold = 0,60 đạt PR-AUC = 0,5620 và Recall = 0,6161 — cao nhất trong toàn hệ thống 10 cấu hình.

3. **Đóng góp Feature Engineering**: 4/10 biến quan trọng nhất (SHAP) là biến tổng hợp. `MAX_PAY_DELAY` (biến mới) đứng rank 1, gấp 1,6× tầm quan trọng của biến gốc `PAY_0`.

4. **Giải thích mô hình**: SHAP TreeExplainer xác nhận lịch sử trậm trả (`MAX_PAY_DELAY`, `PAY_0`, `COUNT_LATE_PAYMENT`) là nhóm yếu tố có tác động mạnh nhất; nhân khẩu học (AGE, SEX) có ảnh hưởng yếu.

5. **Ứng dụng Web**: Streamlit DSS Prototype tích hợp toàn bộ pipeline, 6/6 integration test PASS.

### 3.8.2. Hạn chế đề tài và khả năng áp dụng thực tế

**Hạn chế về dữ liệu:**
- Dataset phản ánh hành vi tín dụng khách hàng thẻ tại Đài Loan, giai đoạn tháng 4–9/2005. Chưa thực hiện **external validation** trên dataset từ thị trường hoặc thời điểm khác — giới hạn khả năng tổng quát hóa.
- Tập dữ liệu không chứa thông tin về thu nhập, lịch sử tín dụng toàn diện hay các biến hành vi phi cấu trúc thường có trong hệ thống Credit Scoring thực tế.

**Hạn chế về phương pháp:**
- Ngưỡng 0,60 được chọn dựa trên tối ưu OOF F1 — không có cost matrix thực tế của ngân hàng. Trong triển khai thực, ngưỡng cần hiệu chỉnh theo tỷ lệ chi phí FP/FN cụ thể.
- SMOTE không được thử nghiệm trong thực nghiệm chính. Có thể cải thiện thêm Recall nhưng cần kiểm soát chặt để tránh Data Leakage.
- Hyperparameter Tuning với `n_iter=25` không đảm bảo global optimum.

**Hạn chế về ứng dụng:**
- Ứng dụng Web chỉ hỗ trợ **single prediction** — chưa có batch prediction hoặc import CSV.
- Không có cơ chế xác thực người dùng, lưu trữ lịch sử tra cứu hay giám sát model drift.
- Kết quả từ prototype mang tính **minh họa học thuật**, không thể sử dụng trực tiếp trong phê duyệt tín dụng thực tế mà không qua quy trình kiểm định và phê duyệt nghiệp vụ.

**Hạn chế về giải thích:**
- SHAP values trong không gian log-odds, không phải probability — cần diễn giải cẩn thận.
- Dependence Plots thể hiện liên hệ thống kê, không phải quan hệ nhân quả.
- Chưa phân tích SHAP interaction values để xác định tác động tương tác giữa các đặc trưng.

---

*Phần cuối Chương 3. Phần Kết luận và Hướng phát triển được trình bày trong Chương tiếp theo.*
