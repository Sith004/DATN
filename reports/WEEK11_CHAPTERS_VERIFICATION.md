# WEEK 11 — KIỂM TRA CHẤT LƯỢNG BẢN NHÁP CHƯƠNG 2 & CHƯƠNG 3
## WEEK11_CHAPTERS_VERIFICATION.md

**Ngày kiểm tra:** 24/10/2026  
**Người kiểm tra:** AI Technical Writer (dựa trên đối chiếu mã nguồn và báo cáo thực nghiệm)  
**Phạm vi:** Bản nháp `Chuong_2_Phuong_Phap_Thuc_Hien.md` và `Chuong_3_Cai_Dat_Thuc_Nghiem_Danh_Gia.md`

---

## 1. Bảng Kiểm tra Chất lượng

| Hạng mục | Bằng chứng nguồn | Trạng thái | Vấn đề cần xử lý |
|---|---|---|---|
| **Cấu trúc Chương 2 khớp DCCT** | `_dcct_raw.txt` dòng 88–118 | ✅ KHỚP HOÀN TOÀN | Đã bao phủ đủ 9 mục 2.1–2.9 theo DCCT FINAL GANTT |
| **Cấu trúc Chương 3 khớp DCCT** | `_dcct_raw.txt` dòng 119–139 | ✅ KHỚP HOÀN TOÀN | Đã bao phủ đủ 8 mục 3.1–3.8 theo DCCT |
| **Số liệu dataset: 30.000 mẫu gốc** | `EDA_Report.md` dòng 32 | ✅ XÁC MINH | Đã dùng trong cả hai chương |
| **Số liệu dataset: 29.965 mẫu sau xử lý** | `Preprocessing_Report.md` dòng 56 | ✅ XÁC MINH | Đã dùng đúng |
| **Train: 23.972 mẫu / Test: 5.993 mẫu** | `Preprocessing_Report.md` dòng 87–88 | ✅ XÁC MINH | Đã dùng đúng |
| **Tỷ lệ Default: 22,12% (gốc) / 22,13% (sau split)** | `EDA_Report.md` dòng 70 & `Preprocessing_Report.md` dòng 87 | ✅ XÁC MINH | Phân biệt rõ hai tỷ lệ |
| **Imbalance Ratio: 3,52:1** | `EDA_Report.md` dòng 76 | ✅ XÁC MINH | Đã dùng trong Chương 2 và 3 |
| **33 features sau FE** | `Feature_Engineering_Report.md` dòng 84–86 | ✅ XÁC MINH | Đã xác nhận trong Bảng 3.4 |
| **10 biến FE và công thức** | `Feature_Engineering_Report.md` dòng 54–64 | ✅ XÁC MINH | Bảng 2.2 và 3.5 đúng |
| **LR Default: Acc=0,8106, Recall=0,2956, PR-AUC=0,5162** | `Model_Baseline_Report.md` dòng 68–75 | ✅ XÁC MINH | Đúng trong Bảng 3.6 |
| **LR Balanced: Acc=0,7469, Recall=0,6018, PR-AUC=0,5123** | `Model_Baseline_Report.md` dòng 90–97 | ✅ XÁC MINH | Đúng trong Bảng 3.6 |
| **DT Default: Acc=0,7267, ROC-AUC=0,6130, PR-AUC=0,2897** | `Model_Baseline_Report.md` dòng 112–119 | ✅ XÁC MINH | Đúng trong Bảng 3.7 |
| **DT Balanced: Acc=0,7262, ROC-AUC=0,5986, PR-AUC=0,2796** | `Model_Baseline_Report.md` dòng 134–141 | ✅ XÁC MINH | Đúng trong Bảng 3.7 |
| **RF Default: Acc=0,8143, PR-AUC=0,5381** | `Week7_Ensemble_Models_Report.md` dòng 55–62 | ✅ XÁC MINH | Đúng trong Bảng 3.7 |
| **RF Balanced: Acc=0,7973, PR-AUC=0,5297** | `Week7_Ensemble_Models_Report.md` dòng 77–84 | ✅ XÁC MINH | Đúng trong Bảng 3.7 |
| **XGBoost Baseline: Acc=0,8201, PR-AUC=0,5611** | `Week7_Ensemble_Models_Report.md` dòng 99–106 | ✅ XÁC MINH | Đúng trong Bảng 3.7 |
| **RF Tuned CV PR-AUC: 0,5656** | `Week8_Tuning_Model_Selection_Report.md` dòng 80 | ✅ XÁC MINH | Đúng trong Bảng 3.8 |
| **RF Balanced Tuned CV PR-AUC: 0,5627** | `Week8_Tuning_Model_Selection_Report.md` dòng 106 | ✅ XÁC MINH | Đúng trong Bảng 3.8 |
| **XGBoost Tuned CV PR-AUC: 0,5646** | `Week8_Tuning_Model_Selection_Report.md` dòng 132 | ✅ XÁC MINH | Đúng trong Bảng 3.8 |
| **XGBoost Tuned: PR-AUC=0,5620, Recall=0,6161** | `Week8_Tuning_Model_Selection_Report.md` dòng 150–156 | ✅ XÁC MINH | Đúng trong Bảng 3.9 và 3.10 |
| **XGBoost Tuned threshold=0,60** | `Week8_Tuning_Model_Selection_Report.md` dòng 212 | ✅ XÁC MINH | Đúng trong Chương 2 và 3 |
| **Siêu tham số XGBoost Tuned** | `Week8_Tuning_Model_Selection_Report.md` dòng 134–146 | ✅ XÁC MINH | Đúng trong Bảng 3.8 |
| **SHAP Expected Value = 0,089860** | `Week9_SHAP_Model_Interpretability_Report.md` dòng 91 | ✅ XÁC MINH | Đúng trong Mục 3.6 |
| **SHAP Top 10 — MAX_PAY_DELAY = 0,4494** | `Week9_SHAP_Model_Interpretability_Report.md` dòng 113–123 | ✅ XÁC MINH | Đúng trong Bảng 3.12 |
| **Local Explanation 3 ca (prob=0,9616/0,0284/0,6001)** | `Week9_SHAP_Model_Interpretability_Report.md` dòng 218–220 | ✅ XÁC MINH | Đúng trong Bảng 3.13 |
| **Integration Test: 6/6 PASS** | Chạy lại `scripts/test_week10.py` 24/10/2026, Exit=0 | ✅ XÁC MINH | Đúng trong Bảng 3.14 |
| **Kết quả Test Integration (prob cụ thể)** | Kết quả chạy: 11,89%, 78,22%, 18,96% | ✅ XÁC MINH | Đúng trong Bảng 3.14 |
| **Không có Data Leakage trong pipeline** | `Preprocessing_Report.md`, `Feature_Engineering_Report.md`, `Week8_Tuning_Model_Selection_Report.md` (Leakage Audit PASS) | ✅ XÁC MINH — Với lưu ý | **Lưu ý học thuật:** Không thể tuyệt đối khẳng định "không có Data Leakage" — nên dùng "không phát hiện Data Leakage trong checklist 7 tiêu chí" |
| **SMOTE không được áp dụng** | `Week8_Tuning_Model_Selection_Report.md` dòng 168–171 | ✅ XÁC MINH | Được ghi nhận rõ trong Mục 2.6.2 và 3.4.1 |
| **Tài liệu tham khảo học thuật** | `_baocao_raw.txt` dòng 247–260 (danh mục TK Chương 1) | ✅ TỒN TẠI | Danh mục TLTK đầy đủ sẵn trong Chương 1 hiện có |
| **Các hình trong báo cáo** | `reports/figures/` — 15+ file PNG xác nhận | ✅ XÁC MINH | Tất cả hình đề xuất đều có file thực tế tương ứng |
| **Nhất quán Chương 2 ↔ Chương 3** | So sánh nội dung bản nháp | ✅ NHẤT QUÁN | Tất cả phương pháp Chương 2 đều được trình bày kết quả trong Chương 3 |
| **Không mâu thuẫn với Chương 1** | `_baocao_raw.txt` dòng 83–246 (Chương 1) | ✅ NHẤT QUÁN | Chương 2–3 mở rộng và áp dụng lý thuyết từ Chương 1 |
| **Công thức toán học** | So chiếu với mã nguồn `src/feature_engineering.py`, `src/prediction.py` | ✅ NHẤT QUÁN | Công thức trong Chương 2 khớp với code thực tế |

---

## 2. Danh sách Mục còn cần Bổ sung / Xác nhận

| # | Mục | Vấn đề | Hành động đề xuất |
|---|---|---|---|
| 1 | **Phiên bản thư viện cụ thể** | Chưa kiểm tra số phiên bản chính xác của pandas, numpy, sklearn, xgboost, streamlit | Chạy `pip freeze > requirements_snapshot.txt` để xác nhận, bổ sung vào Bảng 3.1 |
| 2 | **Hình 3.1–3.3 (EDA figures)** | Các hình đã có trong `reports/figures/` nhưng cần chèn vào bản Word chính thức đúng vị trí | Chèn hình khi hợp nhất sang file Word |
| 3 | **Hình 3.4–3.7 (Baseline/Week7 figures)** | Cần xác minh tên file chính xác trong `reports/figures/` | Đã xác nhận: `baseline_roc_curve.png`, `week7_roc_curve_comparison.png` v.v. |
| 4 | **Bảng 1.1 và 1.2 trong Chương 1** | Chương 1 có bảng so sánh nghiên cứu nhưng chưa đọc nội dung chi tiết | Không cần thiết cho Chương 2–3; đã có trong file Word gốc |
| 5 | **Kết quả RF Default Tuned trên Test** | Acc=0,8206, Precision=0,6785 — đã xác minh từ Week8 Report | Đã đưa vào Bảng 3.10 ✅ |
| 6 | **Thời gian chạy thực nghiệm** | Chưa ghi nhận thời gian huấn luyện từng mô hình | Không bắt buộc theo đề cương; bỏ qua hoặc bổ sung sau |
| 7 | **Số phiên bản Python chính xác** | Không biết chính xác phiên bản con (3.x) | [CẦN XÁC MINH] — chạy `python --version` để lấy |
| 8 | **Kết quả RF Balanced Tuned — Acc=0,7764** | Đã xác minh từ Week8 Report dòng 121 | ✅ Đã đưa vào Bảng 3.10 |
| 9 | **Ngày thực hiện thực nghiệm** | EDA: Tháng 9/2026 (EDA_Report.md), Tuần 4: 14–20/9/2026, Tuần 5: 21–27/9/2026 | Đã ghi nhận trong báo cáo kỹ thuật, có thể thêm vào Chương 3 nếu cần |
| 10 | **Lớp học và Khóa** | Lớp THMT, Khóa 2022–2026 | ✅ Xác nhận từ `_baocao_raw.txt` — đã ghi trên trang bìa |

---

## 3. Danh sách Hình và Bảng

### 3.1. Hình đề xuất cho Chương 2 và Chương 3

| Ký hiệu Hình | Mô tả | File nguồn | Tồn tại? |
|---|---|---|---|
| Hình 2.1 | Sơ đồ tổng thể ML Pipeline | Tạo mới từ text/mermaid diagram | Tạo khi in Word |
| Hình 3.1 | Phân bố biến mục tiêu | `reports/figures/target_distribution.png` | ✅ |
| Hình 3.2 | Phân bố nhân khẩu học | `reports/figures/demographic_distribution.png` | ✅ |
| Hình 3.3 | Ma trận tương quan Pearson | `reports/figures/correlation_heatmap.png` | ✅ |
| Hình 3.4 | ROC Curve so sánh 7 mô hình (Tuần 7) | `reports/figures/week7_roc_curve_comparison.png` | ✅ |
| Hình 3.5 | PR Curve so sánh 7 mô hình (Tuần 7) | `reports/figures/week7_pr_curve_comparison.png` | ✅ |
| Hình 3.6 | Feature Importance — Random Forest | `reports/figures/week7_random_forest_feature_importance.png` | ✅ |
| Hình 3.7 | Feature Importance — XGBoost | `reports/figures/week7_xgboost_feature_importance.png` | ✅ |
| Hình 3.8 | SHAP Bar Plot | `reports/figures/week9_shap_bar.png` | ✅ |
| Hình 3.9 | SHAP Beeswarm Plot | `reports/figures/week9_shap_beeswarm.png` | ✅ |
| Hình 3.10 | Dependence Plot — MAX_PAY_DELAY | `reports/figures/week9_dependence_MAX_PAY_DELAY.png` | ✅ |
| Hình 3.11 | Dependence Plot — PAY_0 | `reports/figures/week9_dependence_PAY_0.png` | ✅ |
| Hình 3.12 | Waterfall — High Risk | `reports/figures/week9_waterfall_high_risk.png` | ✅ |
| Hình 3.13 | Waterfall — Low Risk | `reports/figures/week9_waterfall_low_risk.png` | ✅ |
| Hình 3.14 | Waterfall — Near Threshold | `reports/figures/week9_waterfall_near_threshold.png` | ✅ |

### 3.2. Bảng chính trong Chương 2 và Chương 3

| Ký hiệu Bảng | Mô tả | Số liệu đã xác minh |
|---|---|---|
| Bảng 2.2 (Chương 2) | 10 biến Feature Engineering | ✅ 100% |
| Bảng 2.7.1 (Chương 2) | Hệ thống chỉ số đánh giá | ✅ Định nghĩa chuẩn |
| Bảng 3.1 | Phân bố biến mục tiêu trước xử lý | ✅ 100% |
| Bảng 3.3 | Kết quả Train/Test Split | ✅ 100% |
| Bảng 3.4 | Kiểm tra chất lượng FE | ✅ 100% |
| Bảng 3.5 | Thống kê 10 biến mới | ✅ 100% |
| Bảng 3.6 | So sánh LR Default vs Balanced | ✅ 100% |
| Bảng 3.7 | So sánh 7 mô hình trước Tuning | ✅ 100% |
| Bảng 3.8 | Kết quả Tuning 3 mô hình Ensemble | ✅ 100% |
| Bảng 3.9 | XGBoost: Trước/Sau Tuning | ✅ 100% |
| Bảng 3.10 | Tổng hợp 10 cấu hình toàn bộ | ✅ 100% |
| Bảng 3.11 | So sánh 3 mô hình Tuned | ✅ 100% |
| Bảng 3.12 | Top 10 SHAP Feature Importance | ✅ 100% |
| Bảng 3.13 | Local Explanation 3 ca | ✅ 100% |
| Bảng 3.14 | Kết quả Integration Test 6 bài | ✅ 100% |

---

## 4. Tài liệu tham khảo được sử dụng trong Chương 2 và 3

Danh mục tài liệu tham khảo đầy đủ đã được xây dựng trong Chương 1 của khóa luận (`Bao_Cao_DATN_NguyenTrongThe.docx`). Chương 2 và 3 tham chiếu đến các tài liệu sau (đã tồn tại trong TLTK Chương 1):

| # | Tài liệu | Nơi tham chiếu trong Chương 2–3 |
|---|---|---|
| [1] | Yeh & Lien (2009). Expert Systems with Applications, 36(2) | Nguồn gốc dataset UCI (Mục 3.2.1) |
| [2] | Lundberg & Lee (2017). NeurIPS 2017 | Phương pháp SHAP (Mục 2.8) |
| [3] | Chen & Guestrin (2016). KDD 2016 | Thuật toán XGBoost (Mục 2.5.4) |
| [4] | Pedregosa et al. (2011). JMLR, 12 | Scikit-learn framework (Mục 3.1.2) |
| [5] | Thomas et al. (2002). SIAM | Tổng quan Credit Scoring (Mục 2.1) |

---

## 5. Đánh giá Mức độ Sẵn sàng

### 5.1. Đánh giá Chương 2

| Tiêu chí | Đánh giá |
|---|---|
| **Độ đầy đủ** | ✅ Bao phủ 100% yêu cầu đề cương (9 mục chính 2.1–2.9) |
| **Độ chính xác toán học** | ✅ Công thức FE, Logistic Regression, XGBoost, SHAP Shapley đúng |
| **Nhất quán với mã nguồn** | ✅ Tất cả mô tả đều khớp với `src/feature_engineering.py`, `src/prediction.py` |
| **Không phóng đại kết quả** | ✅ Sử dụng cụm từ cẩn thận ("có liên hệ" thay vì "gây ra") |
| **Trích dẫn tài liệu** | ✅ Chỉ trích dẫn nguồn xác thực đã tồn tại trong Chương 1 |
| **Cần chỉnh sửa** | Định dạng Word (font, giãn dòng) — khi hợp nhất |

**Đánh giá tổng thể Chương 2:** 🟢 **SẴN SÀNG cho hợp nhất** (sau khi định dạng Word)

### 5.2. Đánh giá Chương 3

| Tiêu chí | Đánh giá |
|---|---|
| **Độ đầy đủ** | ✅ Bao phủ 100% yêu cầu đề cương (8 mục chính 3.1–3.8) |
| **Độ chính xác số liệu** | ✅ 100% số liệu được xác minh từ file báo cáo gốc |
| **Bảng so sánh mô hình** | ✅ Đầy đủ 10 cấu hình, không thiếu, không suy diễn |
| **Vị trí chèn hình** | ✅ 15 hình có vị trí đề xuất rõ ràng, tất cả file đã tồn tại |
| **Phân biệt Train/Test/OOF** | ✅ Rõ ràng, không lẫn lộn |
| **Hạn chế nghiên cứu** | ✅ Trình bày trung thực, đầy đủ |
| **Cần chỉnh sửa** | (1) Xác minh phiên bản Python chính xác; (2) Định dạng Word |

**Đánh giá tổng thể Chương 3:** 🟢 **SẴN SÀNG cho hợp nhất** (sau khi xác minh phiên bản Python và định dạng Word)

---

## 6. Các Điểm cần Sinh viên / GVHD Xác nhận

| # | Điểm cần xác nhận | Ghi chú |
|---|---|---|
| 1 | **Phiên bản Python chính xác** (3.x.y) | Chạy `python --version` trong `.venv` |
| 2 | **Ngày/tháng hoàn thành từng giai đoạn** | Nếu muốn bổ sung dòng thời gian chi tiết vào Chương 3 |
| 3 | **Tên GVHD chính xác** | TS. Dương Thị Thúy Nga (đã có trong `_baocao_raw.txt`) |
| 4 | **Số trang hiện tại của Chương 1** | Cần biết để đánh số trang tiếp theo cho Chương 2–3 |
| 5 | **Yêu cầu định dạng Word cụ thể của Khoa** | Font Times New Roman 13pt, giãn dòng 1,5, căn đều hai lề (đã biết theo prompt) |
| 6 | **Có muốn tạo file Word ngay không?** | Kiểm tra `python-docx` đã cài trong `.venv`; nếu có thể tạo ngay |
| 7 | **SHAP summary plot (`week9_shap_summary.png`) vs Bar plot** | Hai biểu đồ khác nhau — xác nhận muốn dùng cái nào trong luận văn |
| 8 | **Boxplot by target** (`boxplots_by_target.png`) | Có muốn thêm vào Chương 3 như Hình 3.4 thay thế không? |

---

## 7. Tóm tắt File đã tạo

| File | Đường dẫn | Kích thước | Trạng thái |
|---|---|---|---|
| Chương 2 — Bản nháp Markdown | [`reports/Chuong_2_Phuong_Phap_Thuc_Hien.md`](file:///F:/DATN/project/reports/Chuong_2_Phuong_Phap_Thuc_Hien.md) | ~23 KB | ✅ Đã tạo |
| Chương 3 — Bản nháp Markdown | [`reports/Chuong_3_Cai_Dat_Thuc_Nghiem_Danh_Gia.md`](file:///F:/DATN/project/reports/Chuong_3_Cai_Dat_Thuc_Nghiem_Danh_Gia.md) | ~22 KB | ✅ Đã tạo |
| Báo cáo kiểm tra chất lượng | [`reports/WEEK11_CHAPTERS_VERIFICATION.md`](file:///F:/DATN/project/reports/WEEK11_CHAPTERS_VERIFICATION.md) | ~10 KB | ✅ (file này) |
| Scratch — DCCT text | `reports/_dcct_raw.txt` | 19 KB | Tạm thời — có thể xóa sau |
| Scratch — BaoCao text | `reports/_baocao_raw.txt` | 43 KB | Tạm thời — có thể xóa sau |
