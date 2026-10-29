# ĐỒ ÁN TỐT NGHIỆP: NGHIÊN CỨU XÂY DỰNG MÔ HÌNH MACHINE LEARNING TRONG ĐÁNH GIÁ VÀ DỰ BÁO RỦI RO TÍN DỤNG KHÁCH HÀNG

**Sinh viên thực hiện**: Nguyễn Trọng Thể  
**Mã số sinh viên**: 1150080117  
**Tập dữ liệu**: UCI Credit Card Default Dataset (`data/UCI_Credit_Card.csv`)  

---

## 📌 Tiến độ Dự án (Project Progress Status)

- [x] **Tuần 1–3: Data Audit & Exploratory Data Analysis (EDA)**
- [x] **Tuần 4: Preprocessing & Data Leakage Control**
- [x] **Tuần 5: Feature Engineering & Preprocessing Pipeline**
- [x] **Automated End-to-End Pipeline Validation (Status: PASS)**
- [x] **Tuần 6: Baseline Machine Learning (Logistic Regression & Decision Tree — COMPLETED)**
- [x] **Tuần 7: Random Forest & XGBoost — COMPLETED**
- [x] **Tuần 8: Hyperparameter Tuning & Model Selection — COMPLETED (XGBoost Tuned selected, threshold=0.60)**
- [x] **Tuần 9: Model Interpretability (SHAP / XAI) — COMPLETED (TreeExplainer, Global + Local + Dependence)**
- [x] **Tuần 10: Web Application Development (Streamlit Dashboard) — COMPLETED (app.py 791 lines, 6/6 tests PASS, SHAP real-time)**

---

## 🚀 Hướng dẫn Chạy lại Toàn bộ Pipeline (Tuần 1 – Tuần 5)

Để tự động kiểm tra và chạy lại toàn bộ quy trình từ đầu đến hết Tuần 5 bằng môi trường ảo `.venv` của dự án:

```powershell
# Chạy toàn bộ pipeline từ Data Audit -> EDA -> Preprocessing -> Feature Engineering -> Automated Validation
.\.venv\Scripts\python.exe -m src.run_pipeline
```

Hoặc chạy độc lập script kiểm định Pipeline:

```powershell
.\.venv\Scripts\python.exe -m src.validate_pipeline
```

---

## 📂 Cấu trúc Thư mục Dự án (Project Structure)

```text
F:\DATN\project
├── .venv/                         # Môi trường ảo Python của dự án
├── data/
│   ├── raw/                       # Tập dữ liệu thô gốc (UCI_Credit_Card.csv)
│   └── processed/                 # Các tập dữ liệu đã qua tiền xử lý & FE
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       ├── y_test.csv
│       ├── X_train_fe.csv         # Tập TRAIN sau Feature Engineering (23,972 x 33)
│       └── X_test_fe.csv          # Tập TEST sau Feature Engineering (5,993 x 33)
├── notebooks/                     # Jupyter Notebooks hoàn chỉnh có output
│   ├── 01_Data_Audit_EDA.ipynb
│   ├── 02_Preprocessing.ipynb
│   ├── 03_Feature_Engineering.ipynb
│   ├── 04_Model_Baseline.ipynb    # Tuần 6: Baseline ML (LR + DT)
│   ├── 05_Ensemble_Models.ipynb   # Tuần 7: Random Forest + XGBoost
│   ├── 06_Hyperparameter_Tuning.ipynb  # Tuần 8: Tuning + Model Selection
│   └── 07_Model_Interpretability.ipynb  # [NEW] Tuần 9: SHAP / XAI
├── src/                           # Các mô-đun Python cốt lõi
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── validate_pipeline.py
│   ├── run_pipeline.py            # Master runner tự động hóa toàn bộ
│   ├── model_training.py          # Tuần 6: Baseline ML Training Pipeline
│   ├── ensemble_models.py         # Tuần 7: RF + XGBoost
│   ├── model_tuning.py            # Tuần 8: Hyperparameter Tuning
│   └── prediction.py              # [NEW] Tuần 10: Inference module cho Web App
├── models/                        # Các model đã huấn luyện
│   ├── logistic_regression_baseline.pkl
│   ├── logistic_regression_balanced.pkl
│   ├── decision_tree_baseline.pkl
│   ├── decision_tree_balanced.pkl
│   ├── random_forest_baseline.pkl
│   ├── random_forest_balanced.pkl
│   ├── random_forest_tuned.pkl
│   ├── random_forest_balanced_tuned.pkl
│   ├── xgboost_baseline.pkl
│   ├── xgboost_tuned.pkl
│   ├── final_candidate_model.pkl  # Official model (XGBoost Tuned, threshold=0.60)
│   └── robust_scaler.pkl          # [NEW] Tuần 10: RobustScaler fit trên X_train_fe
├── reports/                       # Báo cáo kết quả theo từng giai đoạn
│   ├── figures/                   # Biểu đồ (EDA + Baseline + Week7 + Week8 + Week9 SHAP)
│   ├── EDA_Report.md
│   ├── Preprocessing_Report.md
│   ├── Feature_Engineering_Report.md
│   ├── Pipeline_Validation_Report.md
│   ├── Model_Baseline_Report.md
│   ├── Week7_Ensemble_Models_Report.md
│   ├── Week8_Tuning_Model_Selection_Report.md
│   ├── Week9_SHAP_Model_Interpretability_Report.md
│   ├── Week10_WebApp_Report.md            # [NEW] Tuần 10: Web App Documentation
│   ├── model_baseline_results.csv
│   ├── week7_model_comparison.csv
│   ├── week8_model_comparison.csv
│   ├── week9_shap_feature_importance.csv
│   └── week9_local_interpretation.csv
├── requirements.txt               # Danh sách thư viện phụ thuộc
└── README.md
```
