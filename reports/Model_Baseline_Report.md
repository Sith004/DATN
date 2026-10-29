# Model Baseline Report

> **Đề tài:** Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  
> **Sinh viên:** Nguyễn Trọng Thể — MSSV: 1150080117  
> **Giai đoạn:** Tuần 6 — Baseline Machine Learning  

---

## 1. Objective

Xây dựng và đánh giá các mô hình baseline (Logistic Regression và Decision Tree) với hai cấu hình:
- **Default**: Không xử lý class imbalance
- **Balanced**: Sử dụng `class_weight='balanced'` để đối phó với mất cân bằng dữ liệu

Mục đích: tạo điểm tham chiếu (reference point) cho các mô hình nâng cao ở giai đoạn tiếp theo.

---

## 2. Input Dataset

| File | Path |
|------|------|
| X_train_fe.csv | `data/processed/X_train_fe.csv` |
| X_test_fe.csv  | `data/processed/X_test_fe.csv`  |
| y_train.csv    | `data/processed/y_train.csv`    |
| y_test.csv     | `data/processed/y_test.csv`     |

---

## 3. Data Validation

| Kiểm tra | Kết quả |
|----------|---------|
| X_train shape | (23972, 33) |
| X_test shape  | (5993, 33) |
| Target exclusion | ✓ PASS |
| ID exclusion     | ✓ PASS |
| NaN check        | ✓ PASS |
| Inf check        | ✓ PASS |
| Feature consistency | ✓ PASS |
| y schema (binary)  | ✓ PASS |

---

## 4. Class Distribution

### Train set
| Class | Label | Count | Tỷ lệ |
|-------|-------|-------|-------|
| 0 | Non-default | 18,668 | 77.87% |
| 1 | Default     | 5,304 | 22.13% |
| **Imbalance ratio** | | | **3.52:1** |

### Test set
| Class | Label | Count | Tỷ lệ |
|-------|-------|-------|-------|
| 0 | Non-default | 4,667 | 77.87% |
| 1 | Default     | 1,326 | 22.13% |

> **Ghi chú:** Tỷ lệ Default trong train ≈ 22.13% — cần lưu ý khi đánh giá Recall và PR-AUC.

---

## 5. Logistic Regression (Default)

**Model:** `Logistic Regression (Default)`

| Metric    | Value  |
|-----------|--------|
| Accuracy  | 0.8106 |
| Precision | 0.6610 |
| Recall    | 0.2956 |
| F1-Score  | 0.4085 |
| ROC-AUC   | 0.7492 |
| PR-AUC    | 0.5162 |

**Confusion Matrix:**

|  | Pred: 0 | Pred: 1 |
|--|---------|---------|
| True: 0 | TN=4,466 | FP=201 |
| True: 1 | FN=934 | TP=392 |

---

## 6. Logistic Regression with Class Weight

**Model:** `Logistic Regression (Balanced)`

| Metric    | Value  |
|-----------|--------|
| Accuracy  | 0.7469 |
| Precision | 0.4466 |
| Recall    | 0.6018 |
| F1-Score  | 0.5127 |
| ROC-AUC   | 0.7514 |
| PR-AUC    | 0.5123 |

**Confusion Matrix:**

|  | Pred: 0 | Pred: 1 |
|--|---------|---------|
| True: 0 | TN=3,678 | FP=989 |
| True: 1 | FN=528 | TP=798 |

---

## 7. Decision Tree (Default)

**Model:** `Decision Tree (Default)`

| Metric    | Value  |
|-----------|--------|
| Accuracy  | 0.7267 |
| Precision | 0.3884 |
| Recall    | 0.4095 |
| F1-Score  | 0.3987 |
| ROC-AUC   | 0.6130 |
| PR-AUC    | 0.2897 |

**Confusion Matrix:**

|  | Pred: 0 | Pred: 1 |
|--|---------|---------|
| True: 0 | TN=3,812 | FP=855 |
| True: 1 | FN=783 | TP=543 |

---

## 8. Decision Tree with Class Weight

**Model:** `Decision Tree (Balanced)`

| Metric    | Value  |
|-----------|--------|
| Accuracy  | 0.7262 |
| Precision | 0.3784 |
| Recall    | 0.3695 |
| F1-Score  | 0.3739 |
| ROC-AUC   | 0.5986 |
| PR-AUC    | 0.2796 |

**Confusion Matrix:**

|  | Pred: 0 | Pred: 1 |
|--|---------|---------|
| True: 0 | TN=3,862 | FP=805 |
| True: 1 | FN=836 | TP=490 |

---

## 9. Evaluation Metrics

### Bảng so sánh tổng hợp

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|-------|----------|-----------|--------|----|---------|--------|
| Logistic Regression (Default) | 0.8106 | 0.6610 | 0.2956 | 0.4085 | 0.7492 | 0.5162 |
| Logistic Regression (Balanced) | 0.7469 | 0.4466 | 0.6018 | 0.5127 | 0.7514 | 0.5123 |
| Decision Tree (Default) | 0.7267 | 0.3884 | 0.4095 | 0.3987 | 0.6130 | 0.2897 |
| Decision Tree (Balanced) | 0.7262 | 0.3784 | 0.3695 | 0.3739 | 0.5986 | 0.2796 |

---

## 10. Confusion Matrix Analysis

**Ý nghĩa nghiệp vụ:**
- **FP (False Positive):** Khách hàng thực tế không vỡ nợ nhưng bị dự đoán vỡ nợ. Chi phí: từ chối sai khách hàng tốt.
- **FN (False Negative):** Khách hàng thực tế vỡ nợ nhưng bị dự đoán không vỡ nợ. Chi phí: chấp nhận sai khách hàng rủi ro — thường tốn kém hơn FP trong nghiệp vụ tín dụng.

| Model | TN | FP | FN | TP |
|-------|----|----|----|----|
| Logistic Regression (Default) | 4,466 | 201 | 934 | 392 |
| Logistic Regression (Balanced) | 3,678 | 989 | 528 | 798 |
| Decision Tree (Default) | 3,812 | 855 | 783 | 543 |
| Decision Tree (Balanced) | 3,862 | 805 | 836 | 490 |

---

## 11. ROC-AUC Analysis

Biểu đồ ROC Curve xem tại: `reports/figures/baseline_roc_curve.png`

| Model | ROC-AUC |
|-------|---------|
| Logistic Regression (Default) | 0.7492 |
| Logistic Regression (Balanced) | 0.7514 |
| Decision Tree (Default) | 0.6130 |
| Decision Tree (Balanced) | 0.5986 |

---

## 12. PR-AUC Analysis

Biểu đồ PR Curve xem tại: `reports/figures/baseline_pr_curve.png`

Với dataset mất cân bằng, PR-AUC phản ánh chính xác hơn ROC-AUC về khả năng phân loại class thiểu số (Default=1).

| Model | PR-AUC |
|-------|--------|
| Logistic Regression (Default) | 0.5162 |
| Logistic Regression (Balanced) | 0.5123 |
| Decision Tree (Default) | 0.2897 |
| Decision Tree (Balanced) | 0.2796 |

---

## 13. Comparison

Không xếp hạng mô hình chỉ theo một chỉ số Accuracy. Dưới đây là quan sát dựa trên kết quả thực nghiệm:

- Model có **Recall cao nhất** (class Default=1): `Logistic Regression (Balanced)` = 0.6018
- Model có **PR-AUC cao nhất**: `Logistic Regression (Default)` = 0.5162

---

## 14. Class Weight Effect

So sánh ảnh hưởng của `class_weight='balanced'`:

| Model | Config | Recall | Precision | F1 | PR-AUC |
|-------|--------|--------|-----------|----|--------|
| Logistic Regression (Default) | default | 0.2956 | 0.6610 | 0.4085 | 0.5162 |
| Logistic Regression (Balanced) | balanced | 0.6018 | 0.4466 | 0.5127 | 0.5123 |
| Decision Tree (Default) | default | 0.4095 | 0.3884 | 0.3987 | 0.2897 |
| Decision Tree (Balanced) | balanced | 0.3695 | 0.3784 | 0.3739 | 0.2796 |

> **Quan sát:** `class_weight='balanced'` thường tăng Recall nhưng có thể làm giảm Precision, phản ánh trade-off giữa việc phát hiện thêm các trường hợp Default và tăng FP.

---

## 15. Data Leakage Check

**Kết quả kiểm tra leakage:** ✓ PASS

| Kiểm tra | Kết quả |
|----------|---------|
| Test set never used for fitting | ✓ PASS |
| Test set never used for tuning  | ✓ PASS |
| Target not in features          | ✓ PASS |
| No ID feature                   | ✓ PASS |
| No NaN                          | ✓ PASS |
| No Inf                          | ✓ PASS |
| Train/Test feature consistency  | ✓ PASS |
| Preprocessing leakage check     | ✓ PASS |

---

## 16. Limitations

- Các mô hình ở giai đoạn này chưa được tuning (GridSearch/RandomizedSearch/Optuna).
- Chưa áp dụng SMOTE hoặc các kỹ thuật xử lý imbalance nâng cao.
- Chưa thực hiện Threshold Tuning.
- Decision Tree mặc định (`max_depth=None`) dễ bị overfitting — cần quan sát thêm.
- Chưa áp dụng Cross-Validation cho các cấu hình này.

---

## 17. Next Step

- **Tuần 7:** Huấn luyện và đánh giá Random Forest và XGBoost
- **Tuần 8:** Hyperparameter Tuning (GridSearch / Optuna)
- **Tuần 9:** Xử lý imbalance nâng cao (SMOTE, Threshold Tuning)
- **Tuần 10:** SHAP — Explainable AI
- **Tuần 11-12:** Web Prototype (Streamlit)

---

*Báo cáo này được tạo tự động từ kết quả chạy thực tế — không có số liệu giả.*