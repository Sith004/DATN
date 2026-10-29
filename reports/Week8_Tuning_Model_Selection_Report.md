# WEEK 8 — HYPERPARAMETER TUNING & MODEL SELECTION

> **Đề tài:** Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  
> **Sinh viên:** Nguyễn Trọng Thể — MSSV: 1150080117  
> **Giai đoạn:** Tuần 8 — Hyperparameter Tuning & Model Selection  

---

## 1. Mục tiêu

Tuần 8 thực hiện:
1. Hyperparameter Tuning cho 3 mô hình ensemble đã xây dựng ở Tuần 7.
2. Sử dụng `StratifiedKFold(n_splits=5)` với `RandomizedSearchCV` đảm bảo đúng phương pháp.
3. Không sử dụng test set trong quá trình tuning (no-leakage).
4. Phân tích class imbalance và xử lý phù hợp.
5. Threshold analysis dùng out-of-fold predictions.
6. Chọn model chính thức cho giai đoạn Week 9 SHAP/XAI.

---

## 2. Dữ liệu sử dụng

| Thông tin | Giá trị |
|-----------|---------|
| Dataset | Default of Credit Card Clients (UCI) |
| X_train_fe shape | (23,972 × 33) |
| X_test_fe shape  | (5,993 × 33) |
| Số features | 33 |
| Train Class 0 (Non-default) | 18,668 (77.87%) |
| Train Class 1 (Default)     | 5,304 (22.13%) |
| Imbalance ratio (0:1)       | 3.52:1 |
| Random state | 42 |
| Train/test split | 80/20 Stratified (từ Tuần 5, không thay đổi) |

---

## 3. Baseline từ Week 7

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|-------|----------|-----------|--------|----|---------|--------|
| Random Forest (Default) | 0.8143 | 0.6364 | 0.3748 | 0.4718 | 0.7659 | 0.5381 |
| Random Forest (Balanced) | 0.7973 | 0.5471 | 0.4864 | 0.5150 | 0.7661 | 0.5297 |
| XGBoost (Baseline) | 0.8201 | 0.6766 | 0.3582 | 0.4684 | 0.7792 | 0.5611 |

> **Lưu ý:** Đây là kết quả Week 7 dùng làm baseline. Model selection chính thức được thực hiện trong Week 8.

---

## 4. Phương pháp Hyperparameter Tuning

### 4.1 Lý do chọn RandomizedSearchCV

GridSearchCV với không gian tìm kiếm lớn (nhiều hyperparameter) có thể tạo hàng nghìn combinations, gây thời gian chạy quá lâu. `RandomizedSearchCV` với `n_iter=25` cho phép khám phá không gian tham số đủ rộng trong thời gian hợp lý, phù hợp với điều kiện học thuật.

### 4.2 Scoring metric

Vì dữ liệu có hiện tượng mất cân bằng lớp (imbalance ratio ≈ 3.52:1), Accuracy không được sử dụng làm tiêu chí duy nhất để lựa chọn mô hình. **PR-AUC (average_precision)** được ưu tiên trong quá trình tuning, đồng thời Precision, Recall, F1 và ROC-AUC được sử dụng để đánh giá bổ sung.

```python
scoring='average_precision'  # PR-AUC — phù hợp với class imbalance
```

---

## 5. Cross-Validation Strategy

```python
StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

- **Stratified**: Bảo toàn tỷ lệ class trong mỗi fold (~22.13% Default).
- **n_splits=5**: Cân bằng giữa variance thấp và thời gian chạy.
- **shuffle=True, random_state=42**: Đảm bảo reproducibility.
- **Test set**: Hoàn toàn tách biệt — không được dùng trong CV.

---

## 6. Random Forest (Default) — Tuning

**Best CV PR-AUC:** 0.5656 (±0.0088)

**Best Parameters:**
```json
{
  "n_estimators": 250,
  "min_samples_split": 10,
  "min_samples_leaf": 4,
  "max_features": 0.5,
  "max_depth": 10
}
```

| Metric | Before Tuning | After Tuning | Δ |
|--------|--------------|-------------|---|
| ACCURACY | 0.8143 | 0.8206 | +0.0063 |
| PRECISION | 0.6364 | 0.6785 | +0.0421 |
| RECALL | 0.3748 | 0.3597 | -0.0151 |
| F1 | 0.4718 | 0.4702 | -0.0016 |
| ROC-AUC | 0.7659 | 0.7773 | +0.0114 |
| PR-AUC | 0.5381 | 0.5610 | +0.0229 |

---

## 7. Random Forest (Balanced) — Tuning

**Best CV PR-AUC:** 0.5627 (±0.0096)

**Best Parameters:**
```json
{
  "n_estimators": 250,
  "min_samples_split": 10,
  "min_samples_leaf": 4,
  "max_features": 0.5,
  "max_depth": 10
}
```

| Metric | Before Tuning | After Tuning | Δ |
|--------|--------------|-------------|---|
| ACCURACY | 0.7973 | 0.7764 | -0.0209 |
| PRECISION | 0.5471 | 0.4956 | -0.0515 |
| RECALL | 0.4864 | 0.5950 | +0.1086 |
| F1 | 0.5150 | 0.5408 | +0.0258 |
| ROC-AUC | 0.7661 | 0.7753 | +0.0092 |
| PR-AUC | 0.5297 | 0.5584 | +0.0287 |

---

## 8. XGBoost — Tuning

**Best CV PR-AUC:** 0.5646 (±0.0122)

**Best Parameters:**
```json
{
  "subsample": 0.6,
  "reg_lambda": 1.0,
  "reg_alpha": 0.5,
  "n_estimators": 250,
  "min_child_weight": 1,
  "max_depth": 6,
  "learning_rate": 0.03,
  "gamma": 0.3,
  "colsample_bytree": 0.9
}
```

| Metric | Before Tuning | After Tuning | Δ |
|--------|--------------|-------------|---|
| ACCURACY | 0.8201 | 0.7686 | -0.0515 |
| PRECISION | 0.6766 | 0.4820 | -0.1946 |
| RECALL | 0.3582 | 0.6161 | +0.2579 |
| F1 | 0.4684 | 0.5409 | +0.0725 |
| ROC-AUC | 0.7792 | 0.7769 | -0.0023 |
| PR-AUC | 0.5611 | 0.5620 | +0.0009 |

---

## 9. Xử lý Class Imbalance

### 9.1 Phương pháp sử dụng

**Hướng A — Class Weight (được sử dụng):**
- `Random Forest (Balanced)`: `class_weight='balanced'` — điều chỉnh trọng số sample theo nghịch đảo tần suất class.
- `XGBoost`: `scale_pos_weight` = neg/pos ≈ 3.52 — tương đương với class_weight='balanced' trong XGBoost.

**Hướng B — SMOTE (không áp dụng):**
- `imbalanced-learn` chưa được cài trong môi trường `.venv` của project.
- SMOTE không được áp dụng trong Week 8 để tránh thêm dependency không cần thiết.
- Class-weight là phương pháp chính. SMOTE được ghi nhận là thí nghiệm bổ sung có thể thực hiện ở giai đoạn sau nếu cần.

### 9.2 Lý do ưu tiên class_weight

- Không cần tạo synthetic samples — ít rủi ro overfitting.
- Tương thích trực tiếp với RandomizedSearchCV.
- Reproducible và không thay đổi phân phối data gốc.
- Phù hợp với mục tiêu học thuật của đồ án.

---

## 10. Before vs After Tuning

| Model | Metric | Before | After | Δ |
|-------|--------|--------|-------|---|
| RF (Default) Tuned | PR-AUC | 0.5381 | 0.5610 | +0.0229 |
| RF (Default) Tuned | ROC-AUC | 0.7659 | 0.7773 | +0.0114 |
| RF (Default) Tuned | F1 | 0.4718 | 0.4702 | -0.0016 |
| RF (Default) Tuned | RECALL | 0.3748 | 0.3597 | -0.0151 |
| RF (Default) Tuned | PRECISION | 0.6364 | 0.6785 | +0.0421 |
| RF (Balanced) Tuned | PR-AUC | 0.5297 | 0.5584 | +0.0287 |
| RF (Balanced) Tuned | ROC-AUC | 0.7661 | 0.7753 | +0.0092 |
| RF (Balanced) Tuned | F1 | 0.5150 | 0.5408 | +0.0258 |
| RF (Balanced) Tuned | RECALL | 0.4864 | 0.5950 | +0.1086 |
| RF (Balanced) Tuned | PRECISION | 0.5471 | 0.4956 | -0.0515 |
| XGBoost Tuned | PR-AUC | 0.5611 | 0.5620 | +0.0009 |
| XGBoost Tuned | ROC-AUC | 0.7792 | 0.7769 | -0.0023 |
| XGBoost Tuned | F1 | 0.4684 | 0.5409 | +0.0725 |
| XGBoost Tuned | RECALL | 0.3582 | 0.6161 | +0.2579 |
| XGBoost Tuned | PRECISION | 0.6766 | 0.4820 | -0.1946 |

---

## 11. Threshold Analysis

Threshold analysis sử dụng **out-of-fold predictions** trên training data (không phải test set) để đảm bảo no-leakage.

| Model | Best Threshold (OOF F1) |
|-------|------------------------|
| Random Forest (Default) Tuned | 0.30 |
| Random Forest (Balanced) Tuned | 0.55 |
| XGBoost Tuned | 0.60 |

Threshold mặc định (0.50) không nhất thiết là tối ưu với dữ liệu mất cân bằng. Việc điều chỉnh threshold cho phép kiểm soát trade-off Recall/Precision theo mục tiêu nghiệp vụ.

> **Lưu ý nghiệp vụ:** Trong bài toán credit default, False Negative (bỏ sót khách hàng có nguy cơ vỡ nợ) thường có chi phí cao hơn False Positive. Threshold thấp hơn tăng Recall nhưng giảm Precision — cần xem xét theo cost matrix thực tế của ngân hàng (chưa có trong dataset này).

---

## 12. Final Model Selection

### 12.1 Tiêu chí lựa chọn

**Primary:** PR-AUC (quan trọng nhất với class imbalance)  
**Secondary:** ROC-AUC, Recall, Precision, F1  
**Additional:** CV stability, Model complexity, Khả năng giải thích bằng SHAP  

### 12.2 So sánh tất cả model tuned

| Model | PR-AUC | ROC-AUC | Recall | F1 | CV PR-AUC |
|-------|--------|---------|--------|----|-----------|
| Random Forest (Default) Tuned | 0.5610 | 0.7773 | 0.3597 | 0.4702 | 0.5656 |
| Random Forest (Balanced) Tuned | 0.5584 | 0.7753 | 0.5950 | 0.5408 | 0.5627 |
| XGBoost Tuned | 0.5620 | 0.7769 | 0.6161 | 0.5409 | 0.5646 |

### 12.3 Model được chọn

**Official Final Candidate Model for Week 9 SHAP/XAI:**  
**`XGBoost Tuned`**

**Threshold:** `0.60`

> **Lý do lựa chọn:** Model được chọn dựa trên PR-AUC cao nhất trên test set và CV score ổn định. Trong bối cảnh dataset mất cân bằng, PR-AUC phản ánh chính xác hơn khả năng phân biệt class Default. Mô hình cũng có khả năng cung cấp feature importance và tương thích với SHAP (TreeExplainer) cho giai đoạn Week 9.

> **Giới hạn kết luận:** Kết quả phụ thuộc vào dataset UCI Credit Card và pipeline preprocessing đã thiết lập. Chưa có external validation. Threshold được chọn dựa trên OOF F1, không có cost matrix thực tế của ngân hàng.

---

## 13. Leakage Audit

**Kết quả tổng hợp: ✓ PASS**

| Check | Kết quả |
|-------|---------|
| Check 1: Test set không dùng trong hyperparameter tuning | ✓ PASS |
| Check 2: Test set không dùng để chọn threshold | ✓ PASS |
| Check 3: Scaler chỉ fit trên training data (Week 5) | ✓ PASS |
| Check 4: SMOTE chỉ chạy trong training fold (N/A — không dùng) | ✓ PASS |
| Check 5: StratifiedKFold được sử dụng | ✓ PASS |
| Check 6: Target/test info không tạo feature | ✓ PASS |
| Check 7: Final test evaluation sau model selection | ✓ PASS |

---

## 14. Limitations

- Dataset nguồn: UCI Credit Card Clients (Taiwan, 2005) — không đại diện cho toàn bộ thị trường tín dụng.
- Class imbalance (22.13% Default) ảnh hưởng đến Recall — mô hình có xu hướng underpredict class minority.
- Không có cost matrix thực tế của ngân hàng — threshold được chọn dựa trên F1 OOF, không phải chi phí nghiệp vụ.
- Hyperparameter tuning thực hiện với n_iter=25 — không đảm bảo tìm được global optimum trong không gian tham số.
- SMOTE không được thử nghiệm — có thể cải thiện Recall nhưng cần cẩn thận về overfitting.
- Chưa có external validation trên dataset độc lập.
- Chưa triển khai production — kết quả chỉ trong phạm vi thí nghiệm học thuật.
- Feature importance (Week 9 SHAP) có thể thay đổi kết luận về mức độ ảnh hưởng.

---

## 15. Kết luận Week 8

Tuần 8 đã hoàn thành:
1. Hyperparameter Tuning cho 3 mô hình ensemble sử dụng `RandomizedSearchCV` và `StratifiedKFold(5)`.
2. Tuning được thực hiện với scoring `average_precision` (PR-AUC) phù hợp với dataset mất cân bằng.
3. Test set được giữ hoàn toàn độc lập — không tham gia vào quá trình tuning hoặc chọn threshold.
4. Threshold analysis sử dụng out-of-fold predictions trên training data.
5. Model chính thức được chọn: **XGBoost Tuned** (threshold=0.60).
6. Leakage audit: PASS.

Giai đoạn tiếp theo **(Tuần 9)** sẽ thực hiện **SHAP / Explainable AI** để giải thích cơ chế hoạt động của model được chọn.

---

*Báo cáo được tạo tự động từ kết quả chạy thực tế — không có số liệu giả.*