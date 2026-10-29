# WEEK 7 — RANDOM FOREST & XGBOOST

> **Đề tài:** Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  
> **Sinh viên:** Nguyễn Trọng Thể — MSSV: 1150080117  
> **Giai đoạn:** Tuần 7 — Ensemble Models (Random Forest + XGBoost)  

---

## 1. Mục tiêu

Giai đoạn này huấn luyện và đánh giá hai mô hình ensemble:
- **Random Forest (Default):** không điều chỉnh class imbalance
- **Random Forest (Balanced):** sử dụng `class_weight='balanced'`
- **XGBoost (Baseline):** cấu hình baseline không tuning

Kết quả được so sánh trực tiếp với 4 mô hình baseline của Week 6 để quan sát mức cải thiện của ensemble methods.

---

## 2. Dataset

| Thông tin | Giá trị |
|-----------|---------|
| X_train shape | (23972, 33) |
| X_test shape  | (5993, 33)  |
| Số features   | 33 |
| Train Class 0 (Non-default) | 18,668 (77.87%) |
| Train Class 1 (Default)     | 5,304 (22.13%) |
| Imbalance ratio (0:1)       | 3.52:1 |

---

## 3. Data Leakage Check

**Kết quả:** ✓ PASS

| Kiểm tra | Kết quả |
|----------|---------|
| Test set never used for fitting | ✓ PASS |
| Test set never used for tuning | ✓ PASS |
| Target not in X features | ✓ PASS |
| No ID feature | ✓ PASS |
| No NaN | ✓ PASS |
| No Inf | ✓ PASS |
| Train/Test feature consistency | ✓ PASS |
| Preprocessing fit on train only | ✓ PASS |
| No SMOTE / resampling applied | ✓ PASS |

---

## 4. Random Forest (Default)

**Model:** `Random Forest (Default)`

| Metric | Value |
|--------|-------|
| Accuracy  | 0.8143 |
| Precision | 0.6364 |
| Recall    | 0.3748 |
| F1-Score  | 0.4718 |
| ROC-AUC   | 0.7659 |
| PR-AUC    | 0.5381 |

**Confusion Matrix:**

|  | Pred: 0 | Pred: 1 |
|--|---------|---------|
| True: 0 | TN=4,383 | FP=284 |
| True: 1 | FN=829 | TP=497 |

---

## 5. Random Forest (Balanced)

**Model:** `Random Forest (Balanced)`

| Metric | Value |
|--------|-------|
| Accuracy  | 0.7973 |
| Precision | 0.5471 |
| Recall    | 0.4864 |
| F1-Score  | 0.5150 |
| ROC-AUC   | 0.7661 |
| PR-AUC    | 0.5297 |

**Confusion Matrix:**

|  | Pred: 0 | Pred: 1 |
|--|---------|---------|
| True: 0 | TN=4,133 | FP=534 |
| True: 1 | FN=681 | TP=645 |

---

## 6. XGBoost (Baseline)

**Model:** `XGBoost (Baseline)`

| Metric | Value |
|--------|-------|
| Accuracy  | 0.8201 |
| Precision | 0.6766 |
| Recall    | 0.3582 |
| F1-Score  | 0.4684 |
| ROC-AUC   | 0.7792 |
| PR-AUC    | 0.5611 |

**Confusion Matrix:**

|  | Pred: 0 | Pred: 1 |
|--|---------|---------|
| True: 0 | TN=4,440 | FP=227 |
| True: 1 | FN=851 | TP=475 |

---

## 7. Comparison with WEEK 6

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|-------|----------|-----------|--------|----|---------|--------|
| Logistic Regression (Default) | 0.8106 | 0.6610 | 0.2956 | 0.4085 | 0.7492 | 0.5162 |
| Logistic Regression (Balanced) | 0.7469 | 0.4466 | 0.6018 | 0.5127 | 0.7514 | 0.5123 |
| Decision Tree (Default) | 0.7267 | 0.3884 | 0.4095 | 0.3987 | 0.6130 | 0.2897 |
| Decision Tree (Balanced) | 0.7262 | 0.3784 | 0.3695 | 0.3739 | 0.5986 | 0.2796 |
| Random Forest (Default) | 0.8143 | 0.6364 | 0.3748 | 0.4718 | 0.7659 | 0.5381 |
| Random Forest (Balanced) | 0.7973 | 0.5471 | 0.4864 | 0.5150 | 0.7661 | 0.5297 |
| XGBoost (Baseline) | 0.8201 | 0.6766 | 0.3582 | 0.4684 | 0.7792 | 0.5611 |

---

## 8. ROC Curve

Biểu đồ: `reports/figures/week7_roc_curve_comparison.png`

| Model | ROC-AUC |
|-------|---------|
| Logistic Regression (Default) | 0.7492 |
| Logistic Regression (Balanced) | 0.7514 |
| Decision Tree (Default) | 0.6130 |
| Decision Tree (Balanced) | 0.5986 |
| Random Forest (Default) | 0.7659 |
| Random Forest (Balanced) | 0.7661 |
| XGBoost (Baseline) | 0.7792 |

---

## 9. Precision-Recall Curve

Biểu đồ: `reports/figures/week7_pr_curve_comparison.png`

Với dataset mất cân bằng (imbalance 3.52:1), PR-AUC phản ánh chính xác hơn ROC-AUC về khả năng phát hiện class thiểu số (Default=1).

| Model | PR-AUC |
|-------|--------|
| Logistic Regression (Default) | 0.5162 |
| Logistic Regression (Balanced) | 0.5123 |
| Decision Tree (Default) | 0.2897 |
| Decision Tree (Balanced) | 0.2796 |
| Random Forest (Default) | 0.5381 |
| Random Forest (Balanced) | 0.5297 |
| XGBoost (Baseline) | 0.5611 |

---

## 10. Feature Importance

Feature importance cơ bản (built-in impurity-based importance) được tính cho Random Forest và XGBoost.

- `reports/figures/week7_random_forest_feature_importance.png`
- `reports/figures/week7_xgboost_feature_importance.png`

> **Lưu ý:** Đây là feature importance theo cơ chế nội tại của mô hình (mean impurity decrease / gain), không phải SHAP values. Phân tích SHAP sẽ được thực hiện ở giai đoạn tiếp theo.

---

## 11. Discussion

### Class Imbalance

Dataset có tỷ lệ Default ≈ 22.13%, imbalance ratio 3.52:1. Điều này ảnh hưởng trực tiếp đến Recall và PR-AUC của lớp Default=1.

### So sánh Random Forest Default vs Balanced

| Metric    | RF Default | RF Balanced | Δ |
|-----------|------------|-------------|---|
| Recall    | 0.3748 | 0.4864 | +0.1116 |
| Precision | 0.6364 | 0.5471 | -0.0893 |
| F1        | 0.4718 | 0.5150 | +0.0432 |
| PR-AUC    | 0.5381 | 0.5297 | -0.0084 |

Sử dụng `class_weight='balanced'` tác động đến phân phối quyết định của Random Forest, phản ánh trade-off giữa Recall và Precision. Kết quả cụ thể phản ánh từ dữ liệu thực tế — không có tuyên bố định sẵn.

### Ensemble vs Baseline (Week 6)

Về tổng thể, Random Forest và XGBoost kỳ vọng cải thiện ROC-AUC và PR-AUC so với Logistic Regression và Decision Tree baseline nhờ cơ chế ensemble (bagging / boosting). Tuy nhiên kết quả cụ thể phụ thuộc vào dữ liệu thực tế — phân tích chi tiết thực nghiệm được trình bày trong Notebook 05.

---

## 12. Limitations

- Các mô hình chưa được hyperparameter tuning (GridSearchCV / RandomizedSearchCV / Optuna).
- Chưa áp dụng SMOTE hay các kỹ thuật xử lý imbalance nâng cao.
- Chưa thực hiện Threshold Tuning (threshold optimization).
- Chưa áp dụng SHAP / Explainable AI.
- Chưa thực hiện Cross-Validation đầy đủ (chỉ train-test split).

---

## 13. Conclusion of WEEK 7

Tuần 7 đã hoàn thành việc huấn luyện và đánh giá 3 cấu hình ensemble:
Random Forest (Default), Random Forest (Balanced), và XGBoost (Baseline).

Kết quả được so sánh với 4 baseline models của Tuần 6 trên cùng tập test, cùng 33 features, cùng convention metric để đảm bảo tính nhất quán của chuỗi thực nghiệm.

Giai đoạn tiếp theo (Tuần 8) sẽ thực hiện Hyperparameter Tuning để tìm kiếm cấu hình tối ưu cho các mô hình tốt nhất.

---

*Báo cáo này được tạo tự động từ kết quả chạy thực tế — không có số liệu giả.*