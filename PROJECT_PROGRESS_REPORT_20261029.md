# BÁO CÁO TIẾN ĐỘ VÀ KIỂM ĐỊNH KỸ THUẬT DỰ ÁN ĐỒ ÁN TỐT NGHIỆP
# (TECHNICAL PROJECT AUDIT & PROGRESS REPORT — CẬP NHẬT 29/10/2026)

---

## 1. Project Overview (Tổng quan Dự án)

- **Tên đề tài:** NGHIÊN CỨU XÂY DỰNG MÔ HÌNH MACHINE LEARNING TRONG ĐÁNH GIÁ VÀ DỰ BÁO RỦI RO TÍN DỤNG KHÁCH HÀNG
- **Sinh viên thực hiện:** Nguyễn Trọng Thể
- **Mã số sinh viên (MSSV):** 1150080117
- **Lớp / Khóa:** 11_ĐH_THMT — Khóa 2022 – 2026 (K11)
- **Khoa / Trường:** Khoa Công nghệ Thông tin — Trường Đại học Tài nguyên và Môi trường TP.HCM (HCMUNRE)
- **Giảng viên hướng dẫn (GVHD):** TS. Dương Thị Thúy Nga
- **Tập dữ liệu nghiên cứu:** Default of Credit Card Clients Dataset (UCI Machine Learning Repository)
  - Xuất xứ: Khách hàng thẻ tín dụng tại Đài Loan, thu thập từ 04/2005 đến 09/2005.
  - Quy mô dữ liệu thô: 30,000 bản ghi, 25 cột (23 biến đầu vào dự báo, 1 cột ID, 1 biến mục tiêu `default.payment.next.month`).
  - Mất cân bằng lớp: 6,636 Default (22.12%) vs 23,364 Non-Default (77.88%) — Tỷ lệ mất cân bằng ~ 3.52:1.
  - Sau tiền xử lý loại bỏ 35 bản ghi trùng lặp (duplicate): Còn 29,965 bản ghi (Train: 23,972 mẫu; Test: 5,993 mẫu theo Stratified Split 80/20).
- **Mục tiêu nghiên cứu:** Xây dựng, huấn luyện, tối ưu và so sánh thực nghiệm các mô hình Machine Learning (Logistic Regression, Decision Tree, Random Forest, XGBoost) trong bài toán phân loại rủi ro tín dụng cá nhân; ứng dụng Explainable AI (SHAP) để giải thích quyết định dự báo ở cấp độ tổng thể (Global) và cá thể (Local); phát triển ứng dụng Web Prototype (Streamlit) đóng vai trò Hệ thống hỗ trợ ra quyết định (Decision Support System - DSS).

---

## 2. Actual Project Root and Environment (Thư mục gốc và Môi trường)

- **Thư mục không gian làm việc tổng thể:** `F:\DATN`
- **Thư mục gốc thực tế của mã nguồn và dự án Machine Learning:** `F:\DATN\project`
- **Thư mục tài liệu, đề cương và biểu mẫu:** `F:\DATN\docs`
- **Đường dẫn Python thực tế:** `F:\DATN\project\.venv\Scripts\python.exe`
- **Phiên bản Python xác minh thực tế:** Python 3.14.4 (tags/v3.14.4:23116f9, Apr 7 2026, 14:10:54) [MSC v.1944 64 bit (AMD64)] trên hệ điều hành Windows.
- **Các thư viện cốt lõi đã xác minh trong môi trường ảo `.venv`:**
  - `scikit-learn`: 1.9.1
  - `xgboost`: 3.4.1
  - `shap`: 0.52.0
  - `streamlit`: 1.65.0
  - `pandas`: 3.0.5
  - `numpy`: 2.5.3
  - `python-docx`: 1.2.0
  - `matplotlib`: 3.11.2
  - `seaborn`: 0.13.2
  - `joblib`: 1.6.0

---

## 3. Project Structure and Important Files (Cấu trúc và Tệp quan trọng)

### Cây thư mục thực tế toàn dự án

```text
F:\DATN\
├── docs/                                          # THƯ MỤC TÀI LIỆU KHÓA LUẬN VÀ ĐỀ CƯƠNG
│   ├── Bao_Cao_DATN_NguyenTrongThe_Full.docx     # Khóa luận tốt nghiệp hoàn chỉnh (2.27 MB, 706 đoạn văn, 25 bảng, 15 ảnh)
│   ├── Bao_Cao_DATN_NguyenTrongThe.docx          # Bản thảo ban đầu (Chương 1)
│   ├── Chuong_2_Phuong_Phap_Thuc_Hien.docx       # Bản thảo Word Chương 2 (48.6 KB)
│   ├── Chuong_3_Cai_Dat_Thuc_Nghiem_Danh_Gia.docx # Bản thảo Word Chương 3 (2.16 MB)
│   ├── DCCT_NguyenTrongThe_1150080117.docx       # Đề cương chi tiết
│   ├── DCCT_NguyenTrongThe_THMT.docx             # Bản nộp bộ môn
│   ├── De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx  # Kế hoạch 12 tuần chính thức
│   └── Mẫu Đề cương Đồ án tốt nghiệp Đợt 1 26-27.docx
│
├── project/                                       # THƯ MỤC GỐC CHÍNH CỦA DỰ ÁN CODE & ML
│   ├── .venv/                                     # Môi trường ảo Python 3.14.4 cô lập
│   ├── app.py                                     # Giao diện Web Prototype Streamlit DSS (Tuần 10 - 791 dòng)
│   ├── requirements.txt                           # Danh sách thư viện phụ thuộc
│   ├── README.md                                  # Tài liệu hướng dẫn và theo dõi tiến độ
│   ├── DCCT_NguyenTrongThe_1150080117_final.docx  # Bản sao đề cương
│   │
│   ├── data/                                      # Dữ liệu dự án
│   │   ├── raw/
│   │   │   └── UCI_Credit_Card.csv                # Dữ liệu gốc (2,897,209 bytes, 30,000 x 25)
│   │   └── processed/                             # Dữ liệu đã xử lý & chống Data Leakage
│   │       ├── X_train.csv                        # Tập train gốc tiền xử lý (23,972 x 23)
│   │       ├── X_test.csv                         # Tập test gốc tiền xử lý (5,993 x 23)
│   │       ├── y_train.csv                        # Nhãn train (23,972 x 1)
│   │       ├── y_test.csv                         # Nhãn test (5,993 x 1)
│   │       ├── X_train_fe.csv                     # Tập train sau Feature Engineering (23,972 x 33)
│   │       └── X_test_fe.csv                      # Tập test sau Feature Engineering (5,993 x 33)
│   │
│   ├── notebooks/                                 # 7 Jupyter Notebooks hoàn chỉnh, 0 lỗi
│   │   ├── 01_Data_Audit_EDA.ipynb                # Tuần 1-3: Data Audit & Phân tích EDA
│   │   ├── 02_Preprocessing.ipynb                 # Tuần 4: Tiền xử lý & chống Data Leakage
│   │   ├── 03_Feature_Engineering.ipynb           # Tuần 5: Xây dựng 10 đặc trưng tài chính mới
│   │   ├── 04_Model_Baseline.ipynb                # Tuần 6: Logistic Regression & Decision Tree
│   │   ├── 05_Ensemble_Models.ipynb               # Tuần 7: Random Forest & XGBoost Baseline
│   │   ├── 06_Hyperparameter_Tuning.ipynb         # Tuần 8: Tối ưu siêu tham số & Lựa chọn mô hình
│   │   └── 07_Model_Interpretability.ipynb        # Tuần 9: Giải thích mô hình với SHAP (XAI)
│   │
│   ├── src/                                       # Mô-đun mã nguồn cốt lõi
│   │   ├── preprocessing.py                       # Làm sạch, mapping, chia dữ liệu
│   │   ├── feature_engineering.py                 # Công thức tạo 10 biến tài chính mới
│   │   ├── validate_pipeline.py                   # Script tự động kiểm định rò rỉ dữ liệu
│   │   ├── run_pipeline.py                        # Master pipeline runner
│   │   ├── model_training.py                      # Pipeline huấn luyện Baseline Tuần 6
│   │   ├── ensemble_models.py                     # Pipeline huấn luyện Ensemble Tuần 7
│   │   ├── model_tuning.py                        # Pipeline Tuning & Out-of-fold Threshold Tuần 8
│   │   └── prediction.py                          # Module phục vụ suy luận & SHAP Web App Tuần 10
│   │
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
│   │
│   ├── reports/                                   # Báo cáo kỹ thuật chi tiết theo tuần
│   │   ├── figures/                               # 42 biểu đồ PNG chất lượng cao (EDA, ML, SHAP)
│   │   ├── EDA_Report.md                          # Báo cáo khám phá dữ liệu Tuần 1-3
│   │   ├── Preprocessing_Report.md                # Báo cáo tiền xử lý Tuần 4
│   │   ├── Feature_Engineering_Report.md          # Báo cáo biến tạo mới Tuần 5
│   │   ├── Pipeline_Validation_Report.md          # Báo cáo kiểm định chống rò rỉ dữ liệu
│   │   ├── Model_Baseline_Report.md               # Báo cáo mô hình cơ sở Tuần 6
│   │   ├── Week7_Ensemble_Models_Report.md        # Báo cáo Random Forest & XGBoost Tuần 7
│   │   ├── Week8_Tuning_Model_Selection_Report.md # Báo cáo tối ưu và chọn mô hình Tuần 8
│   │   ├── Week9_SHAP_Model_Interpretability_Report.md # Báo cáo Explainable AI SHAP Tuần 9
│   │   ├── Week10_WebApp_Report.md                # Báo cáo Web Prototype Streamlit Tuần 10
│   │   ├── Chuong_2_Phuong_Phap_Thuc_Hien.md      # Bản nháp Markdown Chương 2
│   │   ├── Chuong_3_Cai_Dat_Thuc_Nghiem_Danh_Gia.md # Bản nháp Markdown Chương 3
│   │   ├── WEEK11_CHAPTERS_VERIFICATION.md        # Biên bản kiểm định nội dung Chương 2 & 3
│   │   ├── WEEK11_WORD_EXPORT_CHECKLIST.md        # Checklist xuất bản Word Tuần 11
│   │   ├── WEEK11_FULL_THESIS_INTEGRATION_REPORT.md # Báo cáo tích hợp toàn văn Khóa luận
│   │   ├── model_baseline_results.csv / .json     # Kết quả định lượng Tuần 6
│   │   ├── week7_model_comparison.csv             # Kết quả đối sánh Tuần 7
│   │   ├── week8_model_comparison.csv             # Kết quả trước/sau tuning Tuần 8
│   │   ├── week8_cv_results.csv / tuning_results.csv
│   │   ├── week8_model_selection_meta.json        # Metadata cấu hình mô hình chính thức
│   │   ├── week9_shap_feature_importance.csv      # Bảng tầm quan trọng biến theo SHAP
│   │   ├── week9_local_interpretation.csv         # Phân tích 3 ca cá thể theo SHAP
│   │   └── week9_shap_summary.json                # Tóm tắt toàn diện SHAP
│   │
│   ├── scripts/                                   # Các tiện ích và script kiểm tra độc lập
│   │   ├── test_week10.py                         # Test suite kiểm tra pipeline dự báo Web App (6/6 PASS)
│   │   ├── check_docx.py                          # Script kiểm tra cấu trúc Word
│   │   ├── tao_chuong1.py                         # Script tự động định dạng Word Chương 1
│   │   ├── export_chuong2_word.py                 # Script xuất Word Chương 2
│   │   ├── export_chuong3_word.py                 # Script xuất Word Chương 3
│   │   ├── integrate_full_thesis.py               # Master script hợp nhất toàn văn Khóa luận
│   │   ├── run_week9_shap.py                      # Script tính toán SHAP và xuất biểu đồ Tuần 9
│   │   ├── verify_week9.py                        # Script kiểm tra artifacts Tuần 9
│   │   └── final_audit.py                         # Script kiểm định pipeline Tuần 1-5
│   │
│   └── docs/                                      # Bản sao tài liệu đồng bộ trong thư mục project
│       └── Bao_Cao_DATN_NguyenTrongThe_Full.docx  # Bản sao đồng bộ của Khóa luận (2.27 MB)
```

---

## 4. Progress Summary — Week 1–12 (Tiến độ chi tiết Tuần 1 đến 12)

Đối chiếu trực tiếp với Sơ đồ Gantt tại tệp [De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx](file:///F:/DATN/docs/De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx):

| Week | Planned Tasks | Actual Evidence | Status | Remaining Work |
|---|---|---|---|---|
| **Tuần 1** | Tiếp nhận đề tài, thống nhất mục tiêu với GVHD, lập đề cương chi tiết đồ án tốt nghiệp. | [De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx](file:///F:/DATN/docs/De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx), `DCCT_NguyenTrongThe_1150080117_final.docx`. | `COMPLETED` | Không có. Đã thống nhất đề tài và hoàn thành đề cương. |
| **Tuần 2** | Nghiên cứu tổng quan tài liệu về Credit Risk, Credit Scoring, Machine Learning và SHAP (XAI). | [Bao_Cao_DATN_NguyenTrongThe_Chuong1.docx](file:///F:/DATN/project/reports/Bao_Cao_DATN_NguyenTrongThe_Chuong1.docx) (340 đoạn văn, 3 bảng, 9 công trình liên quan, 27 tài liệu tham khảo), `scripts/tao_chuong1.py`. | `COMPLETED` | Không có. Đã hoàn thiện và tích hợp vào Khóa luận. |
| **Tuần 3** | Thu thập dữ liệu UCI Credit Card, thực hiện kiểm duyệt dữ liệu (Data Audit) và Phân tích khám phá (EDA). | [01_Data_Audit_EDA.ipynb](file:///F:/DATN/project/notebooks/01_Data_Audit_EDA.ipynb), [EDA_Report.md](file:///F:/DATN/project/reports/EDA_Report.md), `phase1_data_audit_report.json`, 7 biểu đồ phân phối/tương quan trong `reports/figures/`. | `COMPLETED` | Không có. |
| **Tuần 4** | Tiền xử lý dữ liệu: phân chia Train/Test chống Data Leakage, làm sạch giá trị dị thường, chuẩn hóa. | [02_Preprocessing.ipynb](file:///F:/DATN/project/notebooks/02_Preprocessing.ipynb), `src/preprocessing.py`, [Preprocessing_Report.md](file:///F:/DATN/project/reports/Preprocessing_Report.md), 4 tệp dữ liệu đã làm sạch (`X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`). | `COMPLETED` | Không có. Stratified split 80/20 thực hiện trước scaling. |
| **Tuần 5** | Nghiên cứu Feature Engineering: tạo 10 chỉ số tài chính mới và kiểm định chống rò rỉ dữ liệu. | [03_Feature_Engineering.ipynb](file:///F:/DATN/project/notebooks/03_Feature_Engineering.ipynb), `src/feature_engineering.py`, `src/validate_pipeline.py`, [Feature_Engineering_Report.md](file:///F:/DATN/project/reports/Feature_Engineering_Report.md), `X_train_fe.csv` (23,972x33), `X_test_fe.csv` (5,993x33). | `COMPLETED` | Không có. Pipeline tự động pass 100%. |
| **Tuần 6** | Huấn luyện mô hình cơ sở (Logistic Regression) và Decision Tree. Đánh giá kết quả ban đầu. | [04_Model_Baseline.ipynb](file:///F:/DATN/project/notebooks/04_Model_Baseline.ipynb), `src/model_training.py`, [Model_Baseline_Report.md](file:///F:/DATN/project/reports/Model_Baseline_Report.md), `model_baseline_results.csv`, 4 tệp `.pkl` trong `models/`. | `COMPLETED` | Không có. |
| **Tuần 7** | Huấn luyện Random Forest và XGBoost. Thực nghiệm xử lý Class Imbalance và đánh giá đối sánh. | [05_Ensemble_Models.ipynb](file:///F:/DATN/project/notebooks/05_Ensemble_Models.ipynb), `src/ensemble_models.py`, [Week7_Ensemble_Models_Report.md](file:///F:/DATN/project/reports/Week7_Ensemble_Models_Report.md), `week7_model_comparison.csv`, 10 biểu đồ so sánh ROC/PR/Confusion Matrix. | `COMPLETED` | Không có. |
| **Tuần 8** | Tối ưu siêu tham số (RandomizedSearchCV), Out-of-fold threshold tuning, lựa chọn mô hình chính thức. | [06_Hyperparameter_Tuning.ipynb](file:///F:/DATN/project/notebooks/06_Hyperparameter_Tuning.ipynb), `src/model_tuning.py`, [Week8_Tuning_Model_Selection_Report.md](file:///F:/DATN/project/reports/Week8_Tuning_Model_Selection_Report.md), `week8_model_comparison.csv`, [final_candidate_model.pkl](file:///F:/DATN/project/models/final_candidate_model.pkl). | `COMPLETED` | Không có. Đã chốt XGBoost Tuned (Thresh=0.60, PR-AUC=0.5620). |
| **Tuần 9** | Thực nghiệm giải thích mô hình bằng SHAP (Global Feature Importance, Beeswarm, Dependence, Local Waterfall). | [07_Model_Interpretability.ipynb](file:///F:/DATN/project/notebooks/07_Model_Interpretability.ipynb), `scripts/run_week9_shap.py`, [Week9_SHAP_Model_Interpretability_Report.md](file:///F:/DATN/project/reports/Week9_SHAP_Model_Interpretability_Report.md), `week9_shap_summary.json`, 11 biểu đồ SHAP. | `COMPLETED` | Không có. Xác định được Top 5 nhân tố chi phối rủi ro. |
| **Tuần 10** | Thiết kế và cài đặt ứng dụng Web Prototype (Streamlit) tích hợp mô hình ML và giao diện SHAP. | [app.py](file:///F:/DATN/project/app.py) (791 dòng), [src/prediction.py](file:///F:/DATN/project/src/prediction.py), [scripts/test_week10.py](file:///F:/DATN/project/scripts/test_week10.py) (6/6 tests PASS), [Week10_WebApp_Report.md](file:///F:/DATN/project/reports/Week10_WebApp_Report.md), `models/robust_scaler.pkl`. | `COMPLETED` | Không có. Đã có tài liệu kỹ thuật đầy đủ và test suite tự động. |
| **Tuần 11** | Kiểm thử ứng dụng Prototype, hoàn thiện Báo cáo Khóa luận tốt nghiệp theo đúng chuẩn trình bày của Khoa CNTT. | [Bao_Cao_DATN_NguyenTrongThe_Full.docx](file:///F:/DATN/docs/Bao_Cao_DATN_NguyenTrongThe_Full.docx) (2.27 MB, 706 đoạn văn, 25 bảng, 15 ảnh), [WEEK11_FULL_THESIS_INTEGRATION_REPORT.md](file:///F:/DATN/project/reports/WEEK11_FULL_THESIS_INTEGRATION_REPORT.md), [WEEK11_CHAPTERS_VERIFICATION.md](file:///F:/DATN/project/reports/WEEK11_CHAPTERS_VERIFICATION.md), [WEEK11_WORD_EXPORT_CHECKLIST.md](file:///F:/DATN/project/reports/WEEK11_WORD_EXPORT_CHECKLIST.md), `scripts/test_week10.py` (6/6 PASS). | `COMPLETED` | Không có. Bản khóa luận toàn văn đã tích hợp xong toàn bộ 3 chương, kết luận và tài liệu tham khảo. |
| **Tuần 12** | Gửi báo cáo cho GVHD xem xét, chỉnh sửa theo góp ý, hoàn thiện slide báo cáo và chuẩn bị bảo vệ đồ án tốt nghiệp. | Tệp khóa luận hoàn chỉnh `Bao_Cao_DATN_NguyenTrongThe_Full.docx` đã sẵn sàng gửi GVHD. Kịch bản chạy demo Streamlit và bộ test đã chuẩn bị sẵn. | `IN PROGRESS` | 1. Gửi file khóa luận cho GVHD (TS. Dương Thị Thúy Nga); 2. Thiết kế slide thuyết trình (20–25 slides PPTX); 3. Quay video/chuẩn bị kịch bản demo bảo vệ. |

---

## 5. Notebook Execution and Verification Status (Trạng thái Notebook)

Kiểm tra định lượng trực tiếp toàn bộ 7 Jupyter Notebooks bằng công cụ kiểm định tự động:

| STT | Tên Notebook | Mã tuần | Số cell Code | Ô có Output | Số lỗi (Errors) | Execution Count | Trạng thái kỹ thuật |
|---|---|---|---|---|---|---|---|
| 1 | `01_Data_Audit_EDA.ipynb` | W1–3 | 7 | 7 / 7 (100%) | 0 | 1 → 7 | `PASS` — Khám phá dữ liệu, missing, correlation |
| 2 | `02_Preprocessing.ipynb` | W4 | 18 | 18 / 18 (100%) | 0 | 19 → 36 | `PASS` — Split 80/20, dedup 35 dòng, mapping |
| 3 | `03_Feature_Engineering.ipynb` | W5 | 7 | 7 / 7 (100%) | 0 | 1 → 7 | `PASS` — 10 biến tài chính, RobustScaler |
| 4 | `04_Model_Baseline.ipynb` | W6 | 17 | 17 / 17 (100%) | 0 | 1 → 17 | `PASS` — Logistic Regression & Decision Tree |
| 5 | `05_Ensemble_Models.ipynb` | W7 | 17 | 17 / 17 (100%) | 0 | 1 → 17 | `PASS` — Random Forest & XGBoost Baseline |
| 6 | `06_Hyperparameter_Tuning.ipynb` | W8 | 26 | 25 / 26 (96.2%)* | 0 | 1 → 26 | `PASS` — Tuning siêu tham số, OOF threshold |
| 7 | `07_Model_Interpretability.ipynb` | W9 | 19 | 9 / 19 (47.4%)** | 0 | 1 → 19 | `PASS` — SHAP TreeExplainer, Global/Local XAI |

- *\*Ghi chú ô không có output tại Notebook 06:* Cell 15 là khai báo hàm tiện ích `def savefig(filename):`, chỉ chứa định nghĩa hàm nên không xuất output, execution count hợp lệ liên tục.
- *\*\*Ghi chú về Notebook 07:* Toàn bộ 19/19 code cell đều có execution count hợp lệ (từ 1 đến 19) và 0 lỗi. Các cell từ 11 đến 30 thực hiện vẽ các đồ thị SHAP (Bar, Beeswarm, Dependence, Waterfall), sử dụng lệnh `plt.savefig()` lưu ảnh trực tiếp vào đĩa `reports/figures/` và đóng figure (`plt.close()`) nhằm tránh xung đột backend GUI hiển thị trên hệ điều hành Windows.

---

## 6. Machine Learning Pipeline Status (Quy trình Pipeline)

### 6.1. Kiểm soát rò rỉ dữ liệu (Data Leakage Control) — TUÂN THỦ 100%
1. **Phân chia tập dữ liệu trước khi xử lý:** Hàm `split_train_test()` phân tách độc lập tập Train (23,972 mẫu) và Test (5,993 mẫu) với tỷ lệ phân tầng (Stratified) 80/20 cố định `random_state=42`.
2. **Feature Engineering trên từng bản ghi độc lập:** Toàn bộ 10 đặc trưng tạo mới được tính toán cục bộ theo từng dòng của từng khách hàng, dựa vào công thức tài chính nội bộ giữa các kỳ thanh toán, không sử dụng bất kỳ tham số thống kê tổng thể xuyên dòng nào (không dùng mean hay max trên toàn tập dữ liệu).
3. **Chuẩn hóa (Scaling) cô lập hoàn toàn:** `RobustScaler` được huấn luyện (`fit`) DUY NHẤT trên tập huấn luyện `X_train_fe` (23,972 mẫu, 22 biến liên tục) và chỉ dùng lệnh `transform` trên tập kiểm thử `X_test_fe`.
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
  2. Về mặt quản trị rủi ro ngân hàng, tổn thất do bỏ lọt khách hàng vỡ nợ (False Negative) gây rủi ro nợ xấu nghiêm trọng hơn việc từ chối nhầm một khách hàng tốt (False Positive). Tại ngưỡng `threshold = 0.60`, mô hình nâng độ nhạy **Recall lên 61.61%** (bắt được 817 / 1,326 ca vỡ nợ thực tế trong tập test) trong khi vẫn duy trì **F1-Score cao nhất đạt 0.5409**.
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
- **Trạng thái kiểm thử:** Script kiểm thử tích hợp [scripts/test_week10.py](file:///F:/DATN/project/scripts/test_week10.py) đã thực thi trực tiếp trên Python 3.14.4 và **VƯỢT QUA 100% (6/6 Test Cases)**:
  - *Test 1:* Khách hàng thông thường (Normal): Prob = 11.89%, Non-Default, Low Risk → `PASS`.
  - *Test 2:* Khách hàng rủi ro cao (High-Risk): Prob = 78.22%, Default, High Risk → `PASS`.
  - *Test 3:* Khách hàng rủi ro thấp (Low-Risk): Prob = 18.96%, Non-Default, Low Risk → `PASS`.
  - *Test 4:* Kiểm tra thứ tự và số lượng 33 features: Khớp tuyệt đối với `X_train_fe.csv` → `PASS`.
  - *Test 5:* Kiểm tra tính nhất quán giữa hàm dự báo ứng dụng và mô hình trực tiếp: Sai khác = 0.00e+00 → `PASS`.
  - *Test 6:* Kiểm tra tính toán SHAP cá thể thời gian thực: TreeExplainer trả về mảng (33,), kỳ vọng 0.08986 → `PASS`.
- **Tài liệu kỹ thuật:** Báo cáo [Week10_WebApp_Report.md](file:///F:/DATN/project/reports/Week10_WebApp_Report.md) (21,777 bytes) đã hoàn thành, mô tả đầy đủ kiến trúc, giao diện, kịch bản kiểm thử và các lưu ý triển khai.
- **Trạng thái vận hành:** Ứng dụng sẵn sàng phục vụ trình diễn và bảo vệ đồ án.

---

## 9. Thesis Report and Documentation Status (Báo cáo và Tài liệu Khóa luận)

### 9.1. Tình trạng tài liệu hiện có
1. **Đề cương chi tiết (Gantt Chart & Syllabus):**
   - Tệp: [De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx](file:///F:/DATN/docs/De_Cuong_Chi_Tiet_Do_An_Tot_Nghiep_Credit_Risk_ML_FINAL_GANTT.docx)
   - Trạng thái: Hoàn thiện đầy đủ thông tin đề tài, mục tiêu, bố cục 3 chương và kế hoạch 12 tuần.
2. **Khóa luận tốt nghiệp toàn văn hoàn chỉnh (Full Thesis Word Document):**
   - Tệp chính thức: [`F:\DATN\docs\Bao_Cao_DATN_NguyenTrongThe_Full.docx`](file:///F:/DATN/docs/Bao_Cao_DATN_NguyenTrongThe_Full.docx) (và bản sao đồng bộ tại `project/docs/Bao_Cao_DATN_NguyenTrongThe_Full.docx`).
   - Dung lượng: **2,274,517 bytes (~2.27 MB)**.
   - Thống kê cấu trúc đã kiểm định qua thư viện `python-docx`:
     - **Số đoạn văn (Paragraphs):** 706 đoạn.
     - **Số bảng biểu (Tables):** 25 bảng biểu hoàn chỉnh có viền đơn, tô màu header chuẩn.
     - **Số hình ảnh thực tế (Pictures):** 15 ảnh (gồm 14 đồ thị thực nghiệm độ phân giải cao nhúng từ `reports/figures/` và logo).
     - **Số phân vùng (Sections):** 3 phân vùng (Trang bìa, phần thủ tục hành chính, nội dung học thuật).
     - **Các chương lớn (Heading 1):**
       1. `CHƯƠNG 1. TỔNG QUAN TÀI LIỆU VÀ CÁC CÔNG TRÌNH NGHIÊN CỨU LIÊN QUAN`
       2. `CHƯƠNG 2. PHƯƠNG PHÁP THỰC HIỆN`
       3. `CHƯƠNG 3. CÀI ĐẶT THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ`
       4. `KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN`
       5. `TÀI LIỆU THAM KHẢO`
3. **Các biên bản và báo cáo kiểm định chất lượng tài liệu:**
   - [reports/WEEK11_CHAPTERS_VERIFICATION.md](file:///F:/DATN/project/reports/WEEK11_CHAPTERS_VERIFICATION.md): Đối chiếu 47 chỉ số thực nghiệm giữa mã nguồn và văn bản khóa luận.
   - [reports/WEEK11_WORD_EXPORT_CHECKLIST.md](file:///F:/DATN/project/reports/WEEK11_WORD_EXPORT_CHECKLIST.md): Biên bản đối chiếu 7 tiêu chí chất lượng và ánh xạ 14 hình ảnh, 25 bảng.
   - [reports/WEEK11_FULL_THESIS_INTEGRATION_REPORT.md](file:///F:/DATN/project/reports/WEEK11_FULL_THESIS_INTEGRATION_REPORT.md): Báo cáo nghiệm thu hợp nhất tài liệu toàn văn.

---

## 10. Outstanding Issues and Risks (Vấn đề tồn tại và Rủi ro)

### Mức P0 (Nghiêm trọng — Có thể làm sai kết quả hoặc dự án không chạy)
- **KHÔNG CÓ LỖI P0 NÀO.**
  - Không có Data Leakage trong toàn bộ pipeline.
  - Toàn bộ 7 Notebooks và mã nguồn Python chạy không phát sinh lỗi.
  - Mô hình và Scaler đã lưu tương thích hoàn toàn với môi trường Python 3.14.4.
  - Ứng dụng Web Streamlit và module dự báo pass 100% các bài test kiểm thử tích hợp (6/6 PASS).
  - Khóa luận tốt nghiệp đã được hợp nhất hoàn chỉnh thành file Word có đầy đủ 3 chương, 25 bảng và 14 hình ảnh.

### Mức P1 (Bắt buộc để hoàn thành Đồ án tốt nghiệp — Tuần 12)
1. **[P1 - Slide bảo vệ] Thiết kế Slide thuyết trình PowerPoint phục vụ Hội đồng bảo vệ:**
   - Hiện trạng: Chưa có file slide trong dự án.
   - Kế hoạch: Xây dựng bộ Slide PowerPoint (20–25 slide) cô đọng các điểm sáng của đề tài: Đặt vấn đề, Feature Engineering 10 biến tài chính, Lựa chọn mô hình XGBoost Tuned, Giải thích XAI bằng SHAP và Trình diễn ứng dụng DSS Prototype.
2. **[P1 - Kịch bản Demo] Chuẩn bị kịch bản và dữ liệu mẫu trình diễn Web App:**
   - Hiện trạng: Web App hoạt động tốt, đã có 3 ca thử nghiệm trong `test_week10.py`.
   - Kế hoạch: Soạn tài liệu hướng dẫn demo nhanh (hoặc video quay sẵn dự phòng) với 3 tình huống khách hàng (rủi ro thấp, trung bình, cao) để trình chiếu mượt mà trước hội đồng.
3. **[P1 - Thẩm duyệt GVHD] Gửi Báo cáo Khóa luận hoàn chỉnh cho TS. Dương Thị Thúy Nga:**
   - Hiện trạng: Bản Word hoàn chỉnh đã sẵn sàng tại `F:\DATN\docs\Bao_Cao_DATN_NguyenTrongThe_Full.docx`.
   - Kế hoạch: Chuyển bản thảo cho GVHD xem xét, tiếp nhận phản hồi và chỉnh sửa văn phong nếu có yêu cầu.

### Mức P2 (Cải thiện chất lượng, trình bày và hoàn thiện kỹ thuật)
1. **[P2 - Kỹ thuật] Lưu ý về script kiểm tra nội bộ `scripts/final_audit.py`:**
   - Trong script `scripts/final_audit.py`, dòng 325 có điều kiện kiểm tra `has_target = "default.payment.next.month" in df.columns` áp dụng chung cho cả `y_train.csv` và `y_test.csv`. Do tệp nhãn `y` bắt buộc chứa cột mục tiêu, script in thông báo `FAIL` giả định tại mục Output Files dù dữ liệu thực tế hoàn toàn chuẩn xác. Không ảnh hưởng đến pipeline.
2. **[P2 - Xuất bản PDF] Xuất file PDF từ file Word hoàn chỉnh:**
   - Xuất bản PDF từ `Bao_Cao_DATN_NguyenTrongThe_Full.docx` để cố định layout trang in, sẵn sàng nộp lưu chiểu và in ấn quyển bìa mạ vàng.

---

## 11. Prioritized Next Actions (Kế hoạch hành động ưu tiên)

1. **Hành động 1 (Ưu tiên P1 — Ngay lập tức):** Gửi tệp khóa luận [Bao_Cao_DATN_NguyenTrongThe_Full.docx](file:///F:/DATN/docs/Bao_Cao_DATN_NguyenTrongThe_Full.docx) cho GVHD TS. Dương Thị Thúy Nga để xin ý kiến đánh giá và duyệt nội dung.
2. **Hành động 2 (Ưu tiên P1 — Nhiệm vụ cốt lõi Tuần 12):** Thiết kế bộ Slide thuyết trình bảo vệ đồ án tốt nghiệp (20–25 slide PowerPoint) dựa trên các bảng biểu và hình ảnh đồ thị trong Báo cáo Khóa luận.
3. **Hành động 3 (Ưu tiên P1 — Nhiệm vụ Tuần 12):** Soạn thảo kịch bản thuyết minh và chuẩn bị môi trường chạy demo Web App Streamlit (hoặc quay video backup độ phân giải cao).
4. **Hành động 4 (Ưu tiên P2):** Điền chính xác ngày tháng bảo vệ chính thức trên trang bìa và trang đề cương chi tiết sau khi Khoa CNTT công bố lịch bảo vệ.

---

## 12. Exact Current Checkpoint (Điểm dừng chính xác của Dự án)

- **Công việc cuối cùng đã hoàn thành và có bằng chứng xác thực:**
  - Hoàn thành hợp nhất toàn bộ Khóa luận tốt nghiệp (Week 11): Tệp [Bao_Cao_DATN_NguyenTrongThe_Full.docx](file:///F:/DATN/docs/Bao_Cao_DATN_NguyenTrongThe_Full.docx) (2.27 MB, 706 đoạn văn, 25 bảng biểu, 15 hình ảnh, 3 chương đầy đủ).
  - Toàn bộ 7 Notebooks và quy trình Machine Learning từ Tuần 1 đến Tuần 9 đã được nghiệm thu không phát sinh lỗi.
  - Ứng dụng Web Prototype Streamlit và test suite [scripts/test_week10.py](file:///F:/DATN/project/scripts/test_week10.py) đã thực thi trực tiếp trên Python 3.14.4 và **PASS 6/6 test cases**.
- **Công việc đang làm dở / Đang chờ triển khai:**
  - Triển khai các hạng mục của Tuần 12: Thiết kế Slide thuyết trình bảo vệ và kịch bản demo ứng dụng Web.
- **Việc cần thực hiện tiếp theo:**
  - Soạn nội dung slide báo cáo tốt nghiệp (PowerPoint).
  - Chuẩn bị kịch bản thuyết trình bảo vệ trước Hội đồng.
- **Tệp cần mở để tiếp tục làm việc:**
  - Khóa luận hoàn chỉnh: [F:\DATN\docs\Bao_Cao_DATN_NguyenTrongThe_Full.docx](file:///F:/DATN/docs/Bao_Cao_DATN_NguyenTrongThe_Full.docx)
  - Ứng dụng Web Prototype: [F:\DATN\project\app.py](file:///F:/DATN/project/app.py)
  - Báo cáo hợp nhất Tuần 11: [F:\DATN\project\reports\WEEK11_FULL_THESIS_INTEGRATION_REPORT.md](file:///F:/DATN/project/reports/WEEK11_FULL_THESIS_INTEGRATION_REPORT.md)
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
  - **TUYỆT ĐỐI KHÔNG** chạy lại quy trình Feature Engineering hoặc tiền xử lý dữ liệu vì các tệp dữ liệu đã qua xử lý trong `data/processed/` đã được kiểm định nghiêm ngặt và không có rò rỉ dữ liệu.
  - **TUYỆT ĐỐI KHÔNG** tạo lại văn bản Chương 1, Chương 2, Chương 3 từ đầu vì bản Word hoàn chỉnh `Bao_Cao_DATN_NguyenTrongThe_Full.docx` đã được biên soạn và kiểm định chất lượng nghiêm ngặt (706 đoạn văn, 25 bảng, 14 biểu đồ thực nghiệm).

---

## 13. Context Handoff for the Next AI Session (Hướng dẫn Bàn giao cho Phiên tiếp theo)

*Đoạn hướng dẫn dưới đây được thiết kế sẵn sàng để bạn sao chép trực tiếp vào khung chat của phiên làm việc AI tiếp theo (Antigravity hoặc ChatGPT):*

```text
Xin chào, tôi đang tiếp tục thực hiện Đồ án Tốt nghiệp với đề tài:
"NGHIÊN CỨU XÂY DỰNG MÔ HÌNH MACHINE LEARNING TRONG ĐÁNH GIÁ VÀ DỰ BÁO RỦI RO TÍN DỤNG KHÁCH HÀNG"
- Sinh viên: Nguyễn Trọng Thể — MSSV: 1150080117 — Lớp: 11_ĐH_THMT — K11
- Khoa CNTT — Trường ĐH Tài nguyên và Môi trường TP.HCM (HCMUNRE)
- Giảng viên hướng dẫn: TS. Dương Thị Thúy Nga
- Thư mục gốc dự án: F:\DATN\project
- Thư mục tài liệu: F:\DATN\docs
- Môi trường Python: F:\DATN\project\.venv\Scripts\python.exe (Python 3.14.4)
- Báo cáo kiểm định kỹ thuật đầy đủ: F:\DATN\project\PROJECT_PROGRESS_REPORT_20261029.md

TRẠNG THÁI HIỆN TẠI ĐÃ XÁC MINH (TUẦN 1 ĐẾN TUẦN 11 ĐÃ HOÀN THÀNH 100%):
1. Dữ liệu & Tiền xử lý (Tuần 1–5): Dataset UCI Credit Card (29,965 bản ghi sau làm sạch). 0 Data Leakage. 10 đặc trưng tài chính mới (Feature Engineering). 7/7 Notebooks chạy không lỗi.
2. Mô hình & XAI (Tuần 6–9): Huấn luyện và đánh giá 10 cấu hình mô hình (LR, DT, RF, XGBoost). Mô hình chính thức: XGBoost Tuned kết hợp threshold=0.60 (PR-AUC=0.5620, Recall=0.6161, F1=0.5409, ROC-AUC=0.7769) lưu tại models/final_candidate_model.pkl. Phân tích SHAP TreeExplainer toàn diện.
3. Ứng dụng Web Prototype DSS (Tuần 10): app.py (791 dòng) và src/prediction.py hoạt động tốt, PASS 6/6 test cases trong scripts/test_week10.py. Đã có reports/Week10_WebApp_Report.md.
4. Báo cáo Khóa luận Word hoàn chỉnh (Tuần 11): Tệp F:\DATN\docs\Bao_Cao_DATN_NguyenTrongThe_Full.docx (2.27 MB, 706 đoạn văn, 25 bảng biểu, 15 ảnh) đã hoàn thành đầy đủ Trang bìa, Thủ tục hành chính, Chương 1, Chương 2, Chương 3, Kết luận và Tài liệu tham khảo, khớp 100% Đề cương chi tiết (DCCT).

NHIỆM VỤ TIẾP THEO (GIAI ĐOẠN TUẦN 12):
1. Thiết kế bộ Slide thuyết trình bảo vệ Đồ án tốt nghiệp (PowerPoint 20–25 slide) tóm tắt các kết quả nghiên cứu và thực nghiệm nổi bật.
2. Soạn kịch bản thuyết minh và kịch bản demo ứng dụng Web Prototype Streamlit phục vụ Hội đồng chấm khóa luận.
3. Chỉnh sửa văn phong hoặc bổ sung nhỏ nếu GVHD (TS. Dương Thị Thúy Nga) có góp ý sau khi xem bản toàn văn.

NGUYÊN TẮC BẮT BUỘC:
- KHÔNG huấn luyện lại (retrain) mô hình ML.
- KHÔNG chạy lại pipeline tiền xử lý hoặc Feature Engineering.
- KHÔNG sửa đổi hoặc viết lại cấu trúc 3 chương khóa luận đã hoàn thành trong Bao_Cao_DATN_NguyenTrongThe_Full.docx.
- Hãy đọc file PROJECT_PROGRESS_REPORT_20261029.md và bắt đầu ngay từ các nhiệm vụ của Tuần 12 (Slide thuyết trình và Kịch bản bảo vệ).
```
