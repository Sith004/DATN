# BÁO CÁO TIẾN ĐỘ VÀ KIỂM ĐỊNH KỸ THUẬT DỰ ÁN ĐỒ ÁN TỐT NGHIỆP
# (TECHNICAL PROJECT AUDIT & PROGRESS REPORT)

---

## 1. Project Overview (Tổng quan Dự án)

- **Tên đề tài:** NGHIÊN CỨU XÂY DỰNG MÔ HÌNH MACHINE LEARNING TRONG ĐÁNH GIÁ VÀ DỰ BÁO RỦI RO TÍN DỤNG KHÁCH HÀNG
- **Sinh viên thực hiện:** Nguyễn Trọng Thể
- **Mã số sinh viên (MSSV):** 1150080117
- **Lớp / Khóa:** 11_ĐH_THMT — Khóa 2022 – 2026 (K11)
- **Khoa / Trường:** Khoa Công nghệ Thông tin — Trường Đại học Tài nguyên và Môi trường TP.HCM (HCMUNRE)
- **Giảng viên hướng dẫn (GVHD):** TS. Dương Thị Thúy Nga
- **Tập dữ liệu nghiên cứu:** Default of Credit Card Clients Dataset (UCI Machine Learning Repository)
  - Xuất xứ: Khách hàng thẻ tín dụng tại Đài Loan, dữ liệu thu thập từ tháng 04/2005 đến tháng 09/2005.
  - Quy mô dữ liệu gốc: 30,000 dòng, 25 cột (23 biến đầu vào dự báo, 1 cột ID, 1 biến mục tiêu `default.payment.next.month`).
  - Tỷ lệ mất cân bằng dữ liệu gốc: 6,636 Default (22.12%) vs 23,364 Non-Default (77.88%).
  - Sau khi loại bỏ 35 bản ghi trùng lặp (duplicate): Còn 29,965 bản ghi (Train: 23,972 mẫu; Test: 5,993 mẫu).
- **Mục tiêu nghiên cứu:** Xây dựng, huấn luyện, tối ưu và so sánh thực nghiệm các mô hình Machine Learning (Logistic Regression, Decision Tree, Random Forest, XGBoost) trong bài toán phân loại rủi ro tín dụng; ứng dụng Explainable AI (SHAP) để giải thích quyết định; phát triển ứng dụng Web Prototype (Streamlit) hỗ trợ ra quyết định tín dụng.

---

## 2. Actual Project Root and Environment (Thư mục gốc và Môi trường)

- **Thư mục gốc thực tế của mã nguồn và dự án ML:** `F:\DATN\project`
- **Thư mục tài liệu, đề cương và biểu mẫu:** `F:\DATN\docs`
- **Đường dẫn Python thực tế:** `F:\DATN\project\.venv\Scripts\python.exe`
- **Phiên bản Python:** Python 3.14.0 (64-bit, Windows)
- **Các thư viện cốt lõi đã xác minh trong môi trường ảo `.venv`:**
  - `numpy`: 2.5.3
  - `pandas`: 3.0.5
  - `scikit-learn`: 1.9.1
  - `xgboost`: 3.4.1
  - `shap`: 0.52.0
  - `streamlit`: 1.65.0
  - `plotly`: 7.1.0
  - `matplotlib`: 3.11.2
  - `seaborn`: 0.13.2
  - `python-docx`: 1.2.0
  - `joblib`: 1.6.0

---

## 3. Project Structure and Important Files (Cấu trúc và Tệp quan trọng)

### Cây thư mục thực tế

```text
F:\DATN\
├── docs/                                          # Tài liệu đề cương, biểu mẫu đồ án tốt nghiệp
│   ├── De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx  # Kế hoạch 12 tuần chính thức
│   ├── Bao_Cao_DATN_NguyenTrongThe.docx           # Bản thảo Báo cáo Khóa luận (Chương 1 hoàn chỉnh)
│   ├── DCCT_NguyenTrongThe_1150080117.docx
│   ├── DCCT_NguyenTrongThe_THMT.docx
│   └── Mẫu Đề cương Đồ án tốt nghiệp Đợt 1 26-27.docx
├── project/                                       # THƯ MỤC GỐC CHÍNH CỦA DỰ ÁN CODE & ML
│   ├── .venv/                                     # Môi trường ảo Python cô lập
│   ├── app.py                                     # Ứng dụng Streamlit Web DSS Prototype (Tuần 10 - 791 dòng)
│   ├── requirements.txt                           # Danh sách phụ thuộc tối thiểu
│   ├── README.md                                  # Tài liệu tổng quan dự án
│   ├── DCCT_NguyenTrongThe_1150080117_final.docx  # Bản sao đề cương chi tiết
│   ├── data/
│   │   ├── raw/
│   │   │   └── UCI_Credit_Card.csv                # Dữ liệu gốc (2,897,209 bytes, 30,000 x 25)
│   │   └── processed/
│   │       ├── X_train.csv                        # Tập train gốc tiền xử lý (23,972 x 23)
│   │       ├── X_test.csv                         # Tập test gốc tiền xử lý (5,993 x 23)
│   │       ├── y_train.csv                        # Nhãn train (23,972 x 1)
│   │       ├── y_test.csv                         # Nhãn test (5,993 x 1)
│   │       ├── X_train_fe.csv                     # Tập train sau Feature Engineering (23,972 x 33)
│   │       └── X_test_fe.csv                      # Tập test sau Feature Engineering (5,993 x 33)
│   ├── notebooks/                                 # 7 Jupyter Notebooks hoàn chỉnh, 0 lỗi
│   │   ├── 01_Data_Audit_EDA.ipynb                # Tuần 1-3: Data Audit & Phân tích EDA
│   │   ├── 02_Preprocessing.ipynb                 # Tuần 4: Tiền xử lý & chống Data Leakage
│   │   ├── 03_Feature_Engineering.ipynb           # Tuần 5: Xây dựng 10 đặc trưng tài chính mới
│   │   ├── 04_Model_Baseline.ipynb                # Tuần 6: Logistic Regression & Decision Tree
│   │   ├── 05_Ensemble_Models.ipynb               # Tuần 7: Random Forest & XGBoost Baseline
│   │   ├── 06_Hyperparameter_Tuning.ipynb         # Tuần 8: Tối ưu siêu tham số & Lựa chọn mô hình
│   │   └── 07_Model_Interpretability.ipynb        # Tuần 9: Giải thích mô hình với SHAP (XAI)
│   ├── src/                                       # Mô-đun mã nguồn cốt lõi
│   │   ├── preprocessing.py                       # Pipeline làm sạch, mapping, chia dữ liệu
│   │   ├── feature_engineering.py                 # Công thức tạo 10 biến tài chính mới
│   │   ├── validate_pipeline.py                   # Script tự động kiểm định rò rỉ dữ liệu
│   │   ├── run_pipeline.py                        # Master pipeline runner
│   │   ├── model_training.py                      # Pipeline huấn luyện mô hình Baseline Tuần 6
│   │   ├── ensemble_models.py                     # Pipeline huấn luyện Ensemble Models Tuần 7
│   │   ├── model_tuning.py                        # Pipeline Tuning & Out-of-fold Threshold Tuần 8
│   │   └── prediction.py                          # Module phục vụ suy luận & SHAP Web App Tuần 10
│   ├── models/                                    # 12 mô hình và scaler đã lưu (.pkl)
│   │   ├── logistic_regression_baseline.pkl
│   │   ├── logistic_regression_balanced.pkl
│   │   ├── decision_tree_baseline.pkl
│   │   ├── decision_tree_balanced.pkl
│   │   ├── random_forest_baseline.pkl
│   │   ├── random_forest_balanced.pkl
│   │   ├── random_forest_tuned.pkl
│   │   ├── random_forest_balanced_tuned.pkl
│   │   ├── xgboost_baseline.pkl
│   │   ├── xgboost_tuned.pkl
│   │   ├── robust_scaler.pkl                      # Scaler chuẩn hóa 22 biến số liên tục
│   │   └── final_candidate_model.pkl              # MÔ HÌNH CHÍNH THỨC: XGBoost Tuned (Thresh=0.60)
│   ├── reports/                                   # Báo cáo kỹ thuật chi tiết theo tuần
│   │   ├── figures/                               # 42 biểu đồ PNG chất lượng cao (EDA, ML, SHAP)
│   │   ├── EDA_Report.md                          # Báo cáo khám phá dữ liệu Tuần 1-3
│   │   ├── Preprocessing_Report.md                # Báo cáo tiền xử lý Tuần 4
│   │   ├── Feature_Engineering_Report.md          # Báo cáo biến tạo mới Tuần 5
│   │   ├── Pipeline_Validation_Report.md          # Báo cáo kiểm định chống rò rỉ dữ liệu
│   │   ├── Model_Baseline_Report.md               # Báo cáo mô hình cơ sở Tuần 6
│   │   ├── Week7_Ensemble_Models_Report.md        # Báo cáo mô hình Random Forest & XGBoost Tuần 7
│   │   ├── Week8_Tuning_Model_Selection_Report.md # Báo cáo tối ưu và chọn mô hình Tuần 8
│   │   ├── Week9_SHAP_Model_Interpretability_Report.md # Báo cáo Explainable AI SHAP Tuần 9
│   │   ├── Bao_Cao_DATN_NguyenTrongThe_Chuong1.docx    # Báo cáo Khóa luận Word Chương 1
│   │   ├── model_baseline_results.csv / .json     # Kết quả định lượng Tuần 6
│   │   ├── week7_model_comparison.csv             # Kết quả đối sánh Tuần 7
│   │   ├── week8_model_comparison.csv             # Kết quả trước/sau tuning Tuần 8
│   │   ├── week8_cv_results.csv / tuning_results.csv
│   │   ├── week8_model_selection_meta.json        # Metadata cấu hình mô hình chính thức
│   │   ├── week9_shap_feature_importance.csv      # Bảng tầm quan trọng biến theo SHAP
│   │   ├── week9_local_interpretation.csv         # Phân tích 3 ca cá thể theo SHAP
│   │   └── week9_shap_summary.json                # Tóm tắt toàn diện SHAP
│   └── scripts/                                   # Các tiện ích và script kiểm tra độc lập
│       ├── test_week10.py                         # Test suite kiểm tra pipeline dự báo Web App
│       ├── final_audit.py                         # Script kiểm định pipeline Tuần 1-5
│       ├── run_week9_shap.py                      # Script chạy SHAP và xuất biểu đồ Tuần 9
│       ├── verify_week9.py                        # Script kiểm tra artifacts Tuần 9
│       └── tao_chuong1.py                         # Script tự động định dạng Word Chương 1
```

---

## 4. Progress Summary — Week 1–12 (Tiến độ chi tiết Tuần 1 đến 12)

Đối chiếu trực tiếp với Kế hoạch Đề cương Đồ án Tốt nghiệp tại tệp [De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx](file:///F:/DATN/docs/De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx):

| Week | Planned Tasks | Actual Evidence | Status | Remaining Work |
|---|---|---|---|---|
| **Tuần 1** | Tiếp nhận đề tài, thống nhất mục tiêu với GVHD, lập đề cương chi tiết đồ án tốt nghiệp. | [De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx](file:///F:/DATN/docs/De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx), `DCCT_NguyenTrongThe_1150080117_final.docx`. | `COMPLETED` | Bổ sung ngày nộp chính thức theo lịch của Khoa. |
| **Tuần 2** | Nghiên cứu tổng quan tài liệu về Credit Risk, Credit Scoring, Machine Learning và SHAP (XAI). | [Bao_Cao_DATN_NguyenTrongThe_Chuong1.docx](file:///F:/DATN/project/reports/Bao_Cao_DATN_NguyenTrongThe_Chuong1.docx) (340 đoạn văn, 3 bảng, 9 công trình liên quan, 27 tài liệu tham khảo), `scripts/tao_chuong1.py`. | `COMPLETED` | Không có. Đã đạt chuẩn định dạng học thuật. |
| **Tuần 3** | Thu thập dữ liệu UCI Credit Card, thực hiện kiểm duyệt dữ liệu (Data Audit) và Phân tích khám phá (EDA). | [01_Data_Audit_EDA.ipynb](file:///F:/DATN/project/notebooks/01_Data_Audit_EDA.ipynb), [EDA_Report.md](file:///F:/DATN/project/reports/EDA_Report.md), `phase1_data_audit_report.json`, 7 biểu đồ phân phối/tương quan trong `reports/figures/`. | `COMPLETED` | Không có. |
| **Tuần 4** | Tiền xử lý dữ liệu: phân chia Train/Test chống Data Leakage, làm sạch giá trị dị thường, chuẩn hóa. | [02_Preprocessing.ipynb](file:///F:/DATN/project/notebooks/02_Preprocessing.ipynb), `src/preprocessing.py`, [Preprocessing_Report.md](file:///F:/DATN/project/reports/Preprocessing_Report.md), 4 tệp dữ liệu đã làm sạch (`X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`). | `COMPLETED` | Không có. Stratified split 80/20 thực hiện trước scaling. |
| **Tuần 5** | Nghiên cứu Feature Engineering: tạo 10 chỉ số tài chính mới và kiểm định chống rò rỉ dữ liệu. | [03_Feature_Engineering.ipynb](file:///F:/DATN/project/notebooks/03_Feature_Engineering.ipynb), `src/feature_engineering.py`, `src/validate_pipeline.py`, [Feature_Engineering_Report.md](file:///F:/DATN/project/reports/Feature_Engineering_Report.md), `X_train_fe.csv` (23,972x33), `X_test_fe.csv` (5,993x33). | `COMPLETED` | Không có. Pipeline tự động pass 100%. |
| **Tuần 6** | Huấn luyện mô hình cơ sở (Logistic Regression) và Decision Tree. Đánh giá kết quả ban đầu. | [04_Model_Baseline.ipynb](file:///F:/DATN/project/notebooks/04_Model_Baseline.ipynb), `src/model_training.py`, [Model_Baseline_Report.md](file:///F:/DATN/project/reports/Model_Baseline_Report.md), `model_baseline_results.csv`, 4 tệp `.pkl` trong `models/`. | `COMPLETED` | Không có. |
| **Tuần 7** | Huấn luyện Random Forest và XGBoost. Thực nghiệm xử lý Class Imbalance và đánh giá đối sánh. | [05_Ensemble_Models.ipynb](file:///F:/DATN/project/notebooks/05_Ensemble_Models.ipynb), `src/ensemble_models.py`, [Week7_Ensemble_Models_Report.md](file:///F:/DATN/project/reports/Week7_Ensemble_Models_Report.md), `week7_model_comparison.csv`, 10 biểu đồ so sánh ROC/PR/Confusion Matrix. | `COMPLETED` | Không có. |
| **Tuần 8** | Tối ưu siêu tham số (RandomizedSearchCV), Out-of-fold threshold tuning, lựa chọn mô hình chính thức. | [06_Hyperparameter_Tuning.ipynb](file:///F:/DATN/project/notebooks/06_Hyperparameter_Tuning.ipynb), `src/model_tuning.py`, [Week8_Tuning_Model_Selection_Report.md](file:///F:/DATN/project/reports/Week8_Tuning_Model_Selection_Report.md), `week8_model_comparison.csv`, [final_candidate_model.pkl](file:///F:/DATN/project/models/final_candidate_model.pkl). | `COMPLETED` | Không có. Đã chốt XGBoost Tuned (Thresh=0.60, PR-AUC=0.5620). |
| **Tuần 9** | Thực nghiệm giải thích mô hình bằng SHAP (Global Feature Importance, Beeswarm, Dependence, Local Waterfall). | [07_Model_Interpretability.ipynb](file:///F:/DATN/project/notebooks/07_Model_Interpretability.ipynb), `scripts/run_week9_shap.py`, [Week9_SHAP_Model_Interpretability_Report.md](file:///F:/DATN/project/reports/Week9_SHAP_Model_Interpretability_Report.md), `week9_shap_summary.json`, 11 biểu đồ SHAP. | `COMPLETED` | Không có. Xác định được Top 5 nhân tố chi phối rủi ro. |
| **Tuần 10** | Thiết kế và cài đặt ứng dụng Web Prototype (Streamlit) tích hợp mô hình ML và giao diện SHAP. | [app.py](file:///F:/DATN/project/app.py) (791 dòng), [src/prediction.py](file:///F:/DATN/project/src/prediction.py), [scripts/test_week10.py](file:///F:/DATN/project/scripts/test_week10.py) (6/6 tests PASS), `models/robust_scaler.pkl`. | `COMPLETED` (Kỹ thuật) / `PARTIALLY COMPLETED` (Tài liệu) | Tạo tài liệu tổng kết `reports/Week10_WebApp_Report.md` và tick hoàn thành Tuần 10 trong `README.md`. |
| **Tuần 11** | Kiểm thử ứng dụng Prototype, hoàn thiện Báo cáo Khóa luận tốt nghiệp (Chương 2, 3 và Kết luận). | Đã có: Kịch bản test 6 ca (`test_week10.py` PASS); Đầy đủ số liệu thực nghiệm, biểu đồ từ Tuần 3-10; `Bao_Cao_DATN_NguyenTrongThe.docx` (mới chỉ có Chương 1). | `PARTIALLY COMPLETED` | Biên soạn Chương 2, Chương 3, Kết luận và hợp nhất thành file Word Khóa luận hoàn chỉnh. |
| **Tuần 12** | Gửi báo cáo cho GVHD xem xét, chỉnh sửa theo góp ý, hoàn thiện slide báo cáo và chuẩn bị bảo vệ đồ án. | Chưa triển khai. Đang chờ hoàn thành toàn văn Báo cáo Tuần 11. | `NOT STARTED` | Thiết kế slide bảo vệ, video/kịch bản demo Streamlit, chuẩn bị bảo vệ trước hội đồng. |

---

## 5. Notebook Execution and Verification Status (Trạng thái Notebook)

Toàn bộ 7 Jupyter Notebooks trong thư mục `notebooks/` đã được kiểm tra cấu trúc JSON, trạng thái thực thi (`execution_count`), đầu ra các ô (`outputs`) và mã lỗi (`error`):

| STT | Tên Notebook | Mã tuần | Số cell Code | Ô có Output | Số lỗi (Errors) | Execution Count | Trạng thái kỹ thuật |
|---|---|---|---|---|---|---|---|
| 1 | `01_Data_Audit_EDA.ipynb` | W1–3 | 7 | 7 / 7 (100%) | 0 | 1 → 7 | `PASS` — Khám phá dữ liệu, missing, correlation |
| 2 | `02_Preprocessing.ipynb` | W4 | 18 | 18 / 18 (100%) | 0 | 19 → 36 | `PASS` — Split 80/20, dedup 35 dòng, mapping |
| 3 | `03_Feature_Engineering.ipynb` | W5 | 7 | 7 / 7 (100%) | 0 | 1 → 7 | `PASS` — 10 biến tài chính, RobustScaler |
| 4 | `04_Model_Baseline.ipynb` | W6 | 17 | 17 / 17 (100%) | 0 | 1 → 17 | `PASS` — Logistic Regression & Decision Tree |
| 5 | `05_Ensemble_Models.ipynb` | W7 | 17 | 17 / 17 (100%) | 0 | 1 → 17 | `PASS` — Random Forest & XGBoost Baseline |
| 6 | `06_Hyperparameter_Tuning.ipynb` | W8 | 26 | 25 / 26 (96.2%)* | 0 | 1 → 26 | `PASS` — Tuning siêu tham số, OOF threshold |
| 7 | `07_Model_Interpretability.ipynb` | W9 | 19 | 19 / 19 (100%)** | 0 | 1 → 19 | `PASS` — SHAP TreeExplainer, Global/Local XAI |

*\*Ghi chú ô không có output tại Notebook 06:* Cell 15 là hàm định nghĩa `def savefig(filename):`, chỉ chứa khai báo hàm nên theo nguyên lý không xuất output, execution count hợp lệ (EC=16).  
*\*\*Ghi chú về Notebook 07:* 19/19 code cell đều có execution count hợp lệ (EC 1 đến 19). Các ô vẽ biểu đồ SHAP lưu trực tiếp ảnh vào đĩa `reports/figures/` thông qua script chạy ngầm backend Agg để tránh xung đột render GUI trên Windows.

---

## 6. Machine Learning Pipeline Status (Quy trình Pipeline)

### 6.1. Kiểm soát rò rỉ dữ liệu (Data Leakage Control) — XÁC NHẬN TUÂN THỦ 100%
1. **Phân chia tập dữ liệu trước khi xử lý:** Hàm `split_train_test()` chia tách độc lập tập Train (23,972 mẫu) và Test (5,993 mẫu) với tỷ lệ phân tầng (Stratified) 80/20 cố định `random_state=42`.
2. **Feature Engineering trên dữ liệu thô độc lập:** Các đặc trưng tạo mới được tính toán trực tiếp trên từng tập riêng biệt dựa trên công thức tài chính nội bộ của khách hàng (theo từng dòng), không sử dụng bất kỳ tham số thống kê tổng thể nào (không dùng mean hay max xuyên dòng của toàn tập dữ liệu).
3. **Chuẩn hóa (Scaling) cô lập:** `RobustScaler` được huấn luyện (`fit`) DUY NHẤT trên tập huấn luyện `X_train_fe` (23,972 mẫu, 22 biến liên tục) và chỉ dùng lệnh `transform` trên tập kiểm thử `X_test_fe`.
4. **Loại trừ biến rò rỉ:** Cột định danh `ID` và cột nhãn `default.payment.next.month` được tách khỏi tập đặc trưng `X` ngay từ giai đoạn đầu.

### 6.2. 10 Đặc trưng tài chính tạo mới (Feature Engineering)
| # | Tên đặc trưng | Công thức tính toán | Ý nghĩa kinh tế / Quản trị rủi ro |
|---|---|---|---|
| 1 | `UTILIZATION_RATE_SEPT` | `BILL_AMT1 / LIMIT_BAL` | Tỷ lệ sử dụng hạn mức tín dụng tháng gần nhất (T9/2005) |
| 2 | `UTILIZATION_RATE_MEAN` | `mean(BILL_AMT1..6) / LIMIT_BAL` | Tỷ lệ sử dụng hạn mức trung bình trong 6 tháng |
| 3 | `PAY_RATIO_SEPT` | `PAY_AMT1 / BILL_AMT2` | Tỷ lệ thanh toán nợ kỳ gần nhất so với kỳ liền trước |
| 4 | `PAY_RATIO_MEAN` | `mean(PAY_AMTk / BILL_AMT{k+1})` | Tỷ lệ thanh toán trung bình 5 kỳ liên tiếp |
| 5 | `MEAN_BILL_AMT` | `mean(BILL_AMT1..6)` | Dư nợ trung bình 6 tháng |
| 6 | `MEAN_PAY_AMT` | `mean(PAY_AMT1..6)` | Số tiền thanh toán trung bình 6 tháng |
| 7 | `BILL_TREND` | `(BILL_AMT1 - BILL_AMT6) / LIMIT_BAL` | Xu hướng tăng giảm dư nợ so với hạn mức |
| 8 | `PAY_TREND` | `(PAY_AMT1 - PAY_AMT6) / LIMIT_BAL` | Xu hướng tăng giảm số tiền thanh toán thực tế |
| 9 | `MAX_PAY_DELAY` | `max(PAY_0, PAY_2..6)` | Số tháng trễ hạn thanh toán nghiêm trọng nhất trong quá khứ |
| 10 | `COUNT_LATE_PAYMENT` | `sum(PAY_i > 0)` | Tần suất (số lần) khách hàng phát sinh trễ hạn trong 6 tháng |

---

## 7. Model Evaluation and Existing Results (Kết quả Đánh giá Mô hình)

### 7.1. Bảng đối sánh hiệu năng toàn diện trên tập Test (5,993 mẫu)

| Giai đoạn | Tên mô hình | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|---|
| **Tuần 6** | Logistic Regression (Default) | 0.8106 | 0.6610 | 0.2956 | 0.4085 | 0.7492 | 0.5162 |
| **Tuần 6** | Logistic Regression (Balanced) | 0.7469 | 0.4466 | 0.6018 | 0.5127 | 0.7514 | 0.5123 |
| **Tuần 6** | Decision Tree (Default) | 0.7267 | 0.3884 | 0.4095 | 0.3987 | 0.6130 | 0.2897 |
| **Tuần 6** | Decision Tree (Balanced) | 0.7262 | 0.3784 | 0.3695 | 0.3739 | 0.5986 | 0.2796 |
| **Tuần 7** | Random Forest (Default) | 0.8143 | 0.6364 | 0.3748 | 0.4718 | 0.7659 | 0.5380 |
| **Tuần 7** | Random Forest (Balanced) | 0.7973 | 0.5471 | 0.4864 | 0.5150 | 0.7661 | 0.5297 |
| **Tuần 7** | XGBoost (Baseline) | 0.8201 | 0.6766 | 0.3582 | 0.4684 | 0.7792 | 0.5611 |
| **Tuần 8** | Random Forest (Tuned Default) | 0.8206 | 0.6785 | 0.3597 | 0.4702 | 0.7773 | 0.5610 |
| **Tuần 8** | Random Forest (Tuned Balanced)| 0.7764 | 0.4956 | 0.5950 | 0.5408 | 0.7753 | 0.5584 |
| **Tuần 8** | **XGBoost Tuned (Chính thức, Thresh=0.60)** | **0.7686** | **0.4820** | **0.6161** | **0.5409** | **0.7769** | **0.5620** |

### 7.2. Quyết định lựa chọn mô hình chính thức
- **Mô hình được chọn:** `XGBoost Tuned` kết hợp ngưỡng phân loại thực nghiệm `threshold = 0.60` (lưu tại `models/final_candidate_model.pkl`).
- **Lý do lựa chọn khoa học và thực tiễn:**
  1. Trong bài toán rủi ro tín dụng với dữ liệu mất cân bằng (22.1% default), chỉ số **PR-AUC (Precision-Recall Area Under Curve)** phản ánh chính xác nhất năng lực phân tách khách hàng vỡ nợ. XGBoost Tuned đạt PR-AUC cao nhất toàn bộ hệ thống (**0.5620**).
  2. Về mặt quản trị rủi ro ngân hàng, tổn thất do bỏ lọt khách hàng vỡ nợ (False Negative) nghiêm trọng hơn rất nhiều so với việc từ chối nhầm một khách hàng tốt (False Positive). Tại ngưỡng `threshold = 0.60`, mô hình nâng độ nhạy **Recall lên 61.61%** (bắt được 817 / 1,326 ca vỡ nợ thực tế trong tập test) trong khi vẫn duy trì **F1-Score cao nhất đạt 0.5409**.
  3. Siêu tham số tối ưu (5-Fold Stratified CV, scoring average_precision):
     - `n_estimators`: 250, `learning_rate`: 0.03, `max_depth`: 6
     - `subsample`: 0.6, `colsample_bytree`: 0.9, `gamma`: 0.3
     - `reg_alpha`: 0.5, `reg_lambda`: 1.0, `min_child_weight`: 1

### 7.3. Kết quả Explainable AI (SHAP) — Tuần 9
Phân tích đóng góp đặc trưng bằng SHAP TreeExplainer trên 5,993 mẫu tập Test:
- **Top 5 nhân tố chi phối rủi ro hàng đầu:**
  1. `MAX_PAY_DELAY` (Mean|SHAP| = 0.4494) — Đặc trưng tạo mới tại Tuần 5
  2. `PAY_0` (Mean|SHAP| = 0.2797) — Biến lịch sử trễ hạn tháng gần nhất
  3. `COUNT_LATE_PAYMENT` (Mean|SHAP| = 0.1211) — Đặc trưng tạo mới tại Tuần 5
  4. `BILL_AMT1` (Mean|SHAP| = 0.1126) — Dư nợ kỳ gần nhất
  5. `UTILIZATION_RATE_SEPT` (Mean|SHAP| = 0.0942) — Đặc trưng tạo mới tại Tuần 5
- **Ý nghĩa:** Có tới 3 trong 5 biến quan trọng nhất là các đặc trưng tài chính tạo mới (Feature Engineering), chứng minh giá trị học thuật và đóng góp thực tiễn vượt trội của giai đoạn Tuần 5.

---

## 8. Web Application Status (Trạng thái Ứng dụng Web Prototype)

- **Tệp khởi chạy:** [app.py](file:///F:/DATN/project/app.py) (791 dòng)
- **Mô-đun dự báo backend:** [src/prediction.py](file:///F:/DATN/project/src/prediction.py) (319 dòng)
- **Lệnh chạy:**
  ```powershell
  cd F:\DATN\project
  .\.venv\Scripts\python.exe -m streamlit run app.py
  ```
- **Kiến trúc luồng xử lý:**
  `Input người dùng (23 trường)` → `Categorical Mapping` → `Feature Engineering (10 biến)` → `RobustScaler (22 biến liên tục)` → `XGBoost Tuned Model` → `Xác suất Default` → `Ngưỡng nhị phân 0.60` → `Phân loại mức rủi ro (Low <30%, Medium 30-59%, High ≥60%)` → `Giải thích SHAP TreeExplainer (Bar Plot + Diễn giải)`.
- **Trạng thái kiểm thử:** Script kiểm thử tích hợp [scripts/test_week10.py](file:///F:/DATN/project/scripts/test_week10.py) đã thực thi và **VƯỢT QUA 100% (6/6 Test Cases)**:
  - *Test 1:* Khách hàng thông thường (Normal): Prob = 11.89%, Non-Default, Low Risk → `PASS`.
  - *Test 2:* Khách hàng rủi ro cao (High-Risk): Prob = 78.22%, Default, High Risk → `PASS`.
  - *Test 3:* Khách hàng rủi ro thấp (Low-Risk): Prob = 18.96%, Non-Default, Low Risk → `PASS`.
  - *Test 4:* Kiểm tra thứ tự và số lượng 33 features: Khớp tuyệt đối với `X_train_fe.csv` → `PASS`.
  - *Test 5:* Kiểm tra tính nhất quán giữa hàm dự báo ứng dụng và mô hình trực tiếp: Sai khác = 0.00e+00 → `PASS`.
  - *Test 6:* Kiểm tra tính toán SHAP cá thể thời gian thực: TreeExplainer trả về mảng (33,), kỳ vọng 0.08986 → `PASS`.
- **Trạng thái vận hành:** Ứng dụng sẵn sàng hoạt động ổn định trên máy cục bộ để phục vụ chấm điểm và bảo vệ đồ án. Hiện chưa chạy nền (daemon) liên tục để tiết kiệm tài nguyên bộ nhớ.

---

## 9. Thesis Report and Documentation Status (Báo cáo và Tài liệu Khóa luận)

### 9.1. Tình trạng tài liệu hiện có
- **Đề cương chi tiết (Gantt Chart & Syllabus):**
  - Tệp: [De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx](file:///F:/DATN/docs/De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx)
  - Trạng thái: Hoàn thiện đầy đủ thông tin đề tài, mục tiêu, bố cục 3 chương và kế hoạch 12 tuần theo quy chuẩn Khoa CNTT.
- **Báo cáo Khóa luận Word hiện tại:**
  - Tệp: [Bao_Cao_DATN_NguyenTrongThe.docx](file:///F:/DATN/docs/Bao_Cao_DATN_NguyenTrongThe.docx) (và bản sao `reports/Bao_Cao_DATN_NguyenTrongThe_Chuong1.docx`).
  - Quy mô: 340 đoạn văn, 3 bảng biểu, 131,652 bytes.
  - Nội dung đã hoàn thành:
    - Trang bìa và thông tin sinh viên/GVHD (TS. Dương Thị Thúy Nga, SV Nguyễn Trọng Thể, MSSV 1150080117).
    - Lời mở đầu.
    - **Chương 1: TỔNG QUAN TÀI LIỆU VÀ CÁC CÔNG TRÌNH NGHIÊN CỨU LIÊN QUAN** (Mục 1.1 đến 1.5): Trình bày đầy đủ khái niệm rủi ro tín dụng, chấm điểm tín dụng, tổng quan 9 công trình nghiên cứu trong/ngoài nước, lý thuyết 4 thuật toán ML (Logistic Regression, Decision Tree, Random Forest, XGBoost), mô tả tập dữ liệu UCI Credit Card, nguyên lý toán học của Shapley values và SHAP.

### 9.2. Các phần còn thiếu trong tài liệu Word (Cần hoàn thành tại Tuần 11)
- **Chương 2: PHƯƠNG PHÁP THỰC HIỆN** (Theo đề cương chi tiết mục 2.1 đến 2.9):
  - 2.1: Quy trình tổng thể ML Pipeline.
  - 2.2: Phương pháp Data Audit & EDA.
  - 2.3: Phương pháp tiền xử lý và quy tắc chống Data Leakage.
  - 2.4: Đề xuất 10 biến tài chính mới (Feature Engineering).
  - 2.5: Mô hình thuật toán đề xuất (LR, DT, RF, XGBoost).
  - 2.6: Phương pháp xử lý mất cân bằng (Class Weighting, Threshold Tuning).
  - 2.7: Hệ thống chỉ số đánh giá, Confusion Matrix và kỹ thuật Tuning.
  - 2.8: Phương pháp giải thích mô hình với SHAP.
  - 2.9: Phân tích yêu cầu và thiết kế kiến trúc DSS Prototype.
- **Chương 3: CÀI ĐẶT THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ** (Theo đề cương chi tiết mục 3.1 đến 3.8):
  - 3.1: Môi trường phát triển và thư viện.
  - 3.2: Kết quả thực nghiệm EDA, tiền xử lý và Feature Engineering.
  - 3.3: Kết quả thực nghiệm Baseline (Tuần 6) và Ensemble (Tuần 7).
  - 3.4: Kết quả xử lý mất cân bằng và Tối ưu siêu tham số (Tuần 8).
  - 3.5: Bảng tổng hợp đối sánh toàn diện và quyết định chọn XGBoost Tuned.
  - 3.6: Kết quả thực nghiệm giải thích mô hình bằng SHAP (Tuần 9).
  - 3.7: Cài đặt và kiểm thử ứng dụng Web Prototype (Tuần 10).
  - 3.8: Thảo luận, đánh giá và hạn chế của đề tài.
- **KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN:** Tóm tắt kết quả đạt được, đóng góp của đề tài và định hướng mở rộng.

*Lưu ý quan trọng:* Toàn bộ số liệu, biểu đồ, kết quả thực nghiệm và văn bản nháp của Chương 2 và Chương 3 đã có sẵn 100% trong các tệp Markdown (`reports/*.md`) và CSV (`reports/*.csv`), chỉ cần chuyển đổi và tổng hợp sang định dạng Word (`.docx`) theo chuẩn Khoa CNTT.

---

## 10. Outstanding Issues and Risks (Vấn đề tồn tại và Rủi ro)

Phân loại mức độ ưu tiên theo chuẩn kỹ thuật:

### Mức P0 (Nghiêm trọng — Có thể làm sai kết quả hoặc dự án không chạy)
- **KHÔNG CÓ LỖI P0 NÀO.**
  - Không có Data Leakage trong pipeline.
  - Toàn bộ 7 Notebooks và mã nguồn Python chạy không phát sinh lỗi.
  - Mô hình và Scaler đã lưu tương thích hoàn hảo với môi trường Python hiện hành.
  - Ứng dụng Web Streamlit và module dự báo pass 100% các bài test kiểm thử.

### Mức P1 (Bắt buộc để hoàn thành Đồ án tốt nghiệp)
1. **[P1 - Tài liệu] Biên soạn Chương 2, Chương 3 và Kết luận vào Báo cáo Khóa luận Word:**
   - Hiện trạng: File Word `Bao_Cao_DATN_NguyenTrongThe.docx` mới chỉ có Chương 1.
   - Giải pháp: Xây dựng script Python sinh tự động nội dung Word (tương tự kiến trúc `scripts/tao_chuong1.py`) hoặc sử dụng công cụ tạo file docx để kết hợp toàn bộ nội dung từ các báo cáo Markdown Tuần 3 đến Tuần 10 vào Chương 2 và 3, chèn 42 biểu đồ từ `reports/figures/` và các bảng số liệu chính xác.
2. **[P1 - Báo cáo] Lập báo cáo tổng kết Tuần 10:**
   - Hiện trạng: Thiếu file `reports/Week10_WebApp_Report.md` và checkbox Tuần 10 trong `README.md` vẫn đang để trống `[ ]`.
   - Giải pháp: Tạo file `reports/Week10_WebApp_Report.md` ghi nhận kiến trúc, 6 ca kiểm thử, kết quả chạy thực tế của ứng dụng Web Prototype và tick `[x]` trong `README.md`.
3. **[P1 - Tuần 12] Chuẩn bị Slide thuyết trình và Kịch bản bảo vệ Đồ án tốt nghiệp:**
   - Hiện trạng: Chưa có thư mục slide bảo vệ.
   - Giải pháp: Thiết kế Slide PowerPoint (20–25 slide) tóm tắt các kết quả nổi bật: Vấn đề nghiên cứu, Feature Engineering, Mô hình XGBoost Tuned, SHAP XAI và Demo Web Prototype.

### Mức P2 (Cải thiện chất lượng, trình bày và hoàn thiện kỹ thuật)
1. **[P2 - Kỹ thuật] Lưu ý về script kiểm tra nội bộ `scripts/final_audit.py`:**
   - *Phát hiện kỹ thuật của Auditor:* Trong script `scripts/final_audit.py` (dòng 325), tác giả viết điều kiện kiểm tra `has_target = "default.payment.next.month" in df.columns` và áp dụng chung cho cả `y_train.csv` và `y_test.csv`. Do bản chất các tệp nhãn `y` bắt buộc phải chứa cột `default.payment.next.month`, script đã in cảnh báo `FAIL` giả định tại mục Output Files dù dữ liệu thực tế hoàn toàn chuẩn xác. Cần cập nhật logic script audit này nếu chạy lại để tránh hiểu lầm.
2. **[P2 - Cấu hình] Khai báo bổ sung trong `requirements.txt`:**
   - Bổ sung `python-docx>=1.1.0` vào `requirements.txt` (dù đã được cài đặt sẵn trong `.venv`) để đảm bảo tính tái lập 100% trên môi trường mới.

---

## 11. Prioritized Next Actions (Kế hoạch hành động ưu tiên)

1. **Hành động 1 (Ưu tiên P1 — Ngay lập tức):** Tạo báo cáo tổng kết kỹ thuật Tuần 10 [reports/Week10_WebApp_Report.md](file:///F:/DATN/project/reports/Week10_WebApp_Report.md) và cập nhật tick `[x]` Tuần 10 trong [README.md](file:///F:/DATN/project/README.md).
2. **Hành động 2 (Ưu tiên P1 — Trọng tâm Tuần 11):** Biên soạn nội dung **Chương 2 (Phương pháp thực hiện)** cho Báo cáo Khóa luận tốt nghiệp theo cấu trúc mục 2.1–2.9 của Đề cương chi tiết.
3. **Hành động 3 (Ưu tiên P1 — Trọng tâm Tuần 11):** Biên soạn nội dung **Chương 3 (Cài đặt thực nghiệm và Đánh giá kết quả)** cho Báo cáo Khóa luận tốt nghiệp theo cấu trúc mục 3.1–3.8 của Đề cương chi tiết, tích hợp đầy đủ bảng biểu và đồ thị.
4. **Hành động 4 (Ưu tiên P1 — Tuần 11):** Soạn thảo phần **Lời cảm ơn, Kết luận và Hướng phát triển**, hợp nhất với Chương 1 thành tệp Báo cáo toàn văn hoàn chỉnh: `docs/Bao_Cao_DATN_NguyenTrongThe_Full.docx`.
5. **Hành động 5 (Ưu tiên P1 — Tuần 12):** Thiết kế bộ Slide thuyết trình (PowerPoint) và kịch bản demo ứng dụng Web Prototype phục vụ Hội đồng bảo vệ.

---

## 12. Exact Current Checkpoint (Điểm dừng chính xác của Dự án)

- **Công việc cuối cùng đã hoàn thành và có bằng chứng xác thực:**
  - Hoàn thành toàn diện mã nguồn và kiểm thử Ứng dụng Web Prototype Tuần 10: Tệp [app.py](file:///F:/DATN/project/app.py) (791 dòng) và [src/prediction.py](file:///F:/DATN/project/src/prediction.py) (319 dòng). Đã thực thi script kiểm thử [scripts/test_week10.py](file:///F:/DATN/project/scripts/test_week10.py) với kết quả **PASS 6/6 test cases**.
- **Công việc đang làm dở:**
  - Biên soạn văn bản Khóa luận tốt nghiệp Word: Đã có Chương 1 tại [Bao_Cao_DATN_NguyenTrongThe.docx](file:///F:/DATN/docs/Bao_Cao_DATN_NguyenTrongThe.docx), đang chờ viết và tích hợp Chương 2, Chương 3 và Kết luận.
- **Việc cần thực hiện tiếp theo:**
  - Khởi tạo tài liệu [reports/Week10_WebApp_Report.md](file:///F:/DATN/project/reports/Week10_WebApp_Report.md) để khép lại hoàn toàn Tuần 10.
  - Bắt đầu biên soạn văn bản Chương 2 và Chương 3 cho Báo cáo Khóa luận tốt nghiệp (Nhiệm vụ trọng tâm Tuần 11).
- **Tệp cần mở để tiếp tục làm việc:**
  - Đề cương chi tiết: [F:\DATN\docs\De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx](file:///F:/DATN/docs/De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx)
  - Mẫu kịch bản sinh Word: [F:\DATN\project\scripts\tao_chuong1.py](file:///F:/DATN/project/scripts/tao_chuong1.py)
  - Các báo cáo kết quả thực nghiệm: `F:\DATN\project\reports\*.md`
- **Lệnh chạy cần thiết nếu muốn kiểm tra hoặc demo:**
  - *Chạy ứng dụng Web Streamlit:*
    ```powershell
    cd F:\DATN\project
    .\.venv\Scripts\python.exe -m streamlit run app.py
    ```
  - *Chạy lại bộ kiểm thử Unit Test Web App:*
    ```powershell
    cd F:\DATN\project
    .\.venv\Scripts\python.exe scripts\test_week10.py
    ```
- **Các lưu ý quan trọng để tránh lặp lại công việc đã hoàn thành:**
  - **TUYỆT ĐỐI KHÔNG** huấn luyện lại (retrain) các mô hình ML. Mô hình chính thức đã được tối ưu và đóng gói sẵn tại `models/final_candidate_model.pkl` (XGBoost Tuned, threshold=0.60).
  - **TUYỆT ĐỐI KHÔNG** chạy lại quy trình Feature Engineering hoặc tiền xử lý dữ liệu vì các tệp dữ liệu đã qua xử lý trong `data/processed/` đã được kiểm định nghiêm ngặt và không có rò rỉ dữ liệu (0 leakage).
  - Không thay đổi công thức 10 biến trong `src/prediction.py` vì đã được kiểm chứng khớp 100% với `src/feature_engineering.py`.

---

## 13. Context Handoff for the Next AI Session (Hướng dẫn Bàn giao cho Phiên tiếp theo)

*Đoạn hướng dẫn dưới đây được thiết kế sẵn sàng để bạn sao chép trực tiếp vào khung chat của phiên làm việc AI tiếp theo (Antigravity hoặc ChatGPT):*

```text
Xin chào, tôi đang tiếp tục thực hiện Đồ án Tốt nghiệp với đề tài:
"NGHIÊN CỨU XÂY DỰNG MÔ HÌNH MACHINE LEARNING TRONG ĐÁNH GIÁ VÀ DỰ BÁO RỦI RO TÍN DỤNG KHÁCH HÀNG"
- Sinh viên: Nguyễn Trọng Thể — MSSV: 1150080117 — Lớp: 11_ĐH_THMT — K11
- Khoa CNTT — Trường ĐH Tài nguyên và Môi trường TP.HCM (HCMUNRE)
- GVHD: TS. Dương Thị Thúy Nga
- Thư mục gốc dự án: F:\DATN\project
- Môi trường Python: F:\DATN\project\.venv\Scripts\python.exe
- Báo cáo tiến độ đầy đủ đã lập tại: F:\DATN\project\PROJECT_PROGRESS_REPORT.md

TRẠNG THÁI HIỆN TẠI ĐÃ XÁC MINH:
1. Tuần 1 đến Tuần 9: ĐÃ HOÀN THÀNH 100% (Data Audit, EDA, Preprocessing 0 leakage, Feature Engineering 10 biến tài chính, Baseline LR/DT, Ensemble RF/XGBoost, Hyperparameter Tuning & Threshold 0.60, Explainable AI SHAP). Mô hình chính thức là XGBoost Tuned (models/final_candidate_model.pkl, PR-AUC = 0.5620, Recall = 0.6161, F1 = 0.5409).
2. Tuần 10: Ứng dụng Web Prototype Streamlit (app.py) và module backend (src/prediction.py) đã hoàn thành và PASS 100% 6 bài test trong scripts/test_week10.py. Chỉ còn thiếu file báo cáo kỹ thuật reports/Week10_WebApp_Report.md và tick [x] trong README.md.
3. Tài liệu Khóa luận tốt nghiệp: File F:\DATN\docs\Bao_Cao_DATN_NguyenTrongThe.docx mới chỉ có Chương 1 (Tổng quan tài liệu). Chưa có Chương 2 và Chương 3 trong file Word.

NHIỆM VỤ TIẾP THEO (TUẦN 11):
1. Tạo file báo cáo tổng kết Tuần 10: reports/Week10_WebApp_Report.md và cập nhật README.md.
2. Biên soạn nội dung Chương 2 (Phương pháp thực hiện) và Chương 3 (Cài đặt thực nghiệm và Đánh giá kết quả) cho Khóa luận tốt nghiệp theo đúng Đề cương chi tiết (F:\DATN\docs\De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx), tích hợp toàn bộ bảng số liệu và 42 biểu đồ có sẵn trong reports/.
3. Hợp nhất thành bản Báo cáo Khóa luận Word hoàn chỉnh (Bao_Cao_DATN_NguyenTrongThe_Full.docx).

Vui lòng duy trì nguyên tắc: KHÔNG huấn luyện lại mô hình, KHÔNG chạy lại pipeline dữ liệu, KHÔNG thay đổi cấu trúc thư mục hiện có. Hãy đọc file PROJECT_PROGRESS_REPORT.md và bắt đầu ngay từ nhiệm vụ hoàn thiện tài liệu Tuần 11.
```
