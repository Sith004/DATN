# WEEK 11 — BẢN KIỂM TRA CHẤT LƯỢNG VÀ KẾ HOẠCH XUẤT FILE WORD
## WEEK11_WORD_EXPORT_CHECKLIST.md

**Ngày thực hiện:** 24/10/2026  
**Người kiểm tra:** AI Technical Writer & Auditor  
**Phạm vi:** 
- Bản nháp nguồn: `reports/Chuong_2_Phuong_Phap_Thuc_Hien.md` và `reports/Chuong_3_Cai_Dat_Thuc_Nghiem_Danh_Gia.md`
- Đích xuất bản Word: `docs/Chuong_2_Phuong_Phap_Thuc_Hien.docx` và `docs/Chuong_3_Cai_Dat_Thuc_Nghiem_Danh_Gia.docx`

---

## 1. Kết quả kiểm tra đối chiếu 7 tiêu chí chất lượng

| # | Tiêu chí kiểm tra | Bằng chứng đối chiếu | Đánh giá | Ghi chú xử lý khi xuất Word |
|---|---|---|---|---|
| 1 | **Cấu trúc đề mục khớp Đề cương chi tiết (DCCT)** | `reports/_dcct_raw.txt` (dòng 88–139) | ✅ **100% Khớp** | Chương 2 gồm đủ 9 mục (2.1–2.9). Chương 3 gồm đủ 8 mục (3.1–3.8). Không thiếu mục nào. |
| 2 | **Số liệu, công thức và bảng biểu có nguồn kiểm chứng** | `reports/EDA_Report.md`, `Preprocessing_Report.md`, `Feature_Engineering_Report.md`, `src/feature_engineering.py` | ✅ **Đã xác minh** | Tất cả 10 công thức FE, 7 tiêu chí leakage, kích thước 30.000 -> 29.965 mẫu, 23.972/5.993 split đều có nguồn gốc rõ ràng. |
| 3 | **Các chỉ số mô hình lấy đúng từ kết quả thực tế** | `reports/week7_model_comparison.csv`, `reports/week8_model_comparison.csv`, `reports/week8_tuning_results.csv` | ✅ **Đã xác minh** | Toàn bộ 10 cấu hình mô hình (LR Default/Balanced, DT Default/Balanced, RF Default/Balanced, XGBoost Baseline, RF Tuned, RF Balanced Tuned, XGBoost Tuned) khớp từng số thập phân. |
| 4 | **Hình ảnh được lấy từ file có thật (không tạo hình giả)** | Thư mục `reports/figures/` (42 file PNG thực tế) | ✅ **100% File thật** | Tất cả 14 hình được chèn đều trỏ trực tiếp đến file PNG có thật trong `reports/figures/`. |
| 5 | **Trích dẫn và tài liệu tham khảo có thật** | `reports/_baocao_raw.txt` (dòng 109–135 và 247–260) | ✅ **Đã xác minh** | Các trích dẫn (Yeh & Lien 2009, Chen & Guestrin 2016, Lundberg & Lee 2017) hoàn toàn có thật và đã được định nghĩa trong Chương 1. |
| 6 | **Không mâu thuẫn giữa Chương 2 và Chương 3** | Đối chiếu chéo giữa hai bản nháp | ✅ **Hoàn toàn nhất quán** | Mọi phương pháp nêu ở Chương 2 (RobustScaler, 10 biến FE, 4 thuật toán, class_weight, threshold 0.60, SHAP TreeExplainer, Web DSS) đều được phản ánh kết quả tương ứng ở Chương 3. |
| 7 | **Không khẳng định quá mức (Data Leakage, Nhân quả, Ứng dụng)** | Nội dung mục 2.3.1, 2.8.2, 3.6.2, 3.8.2 | ✅ **Đạt chuẩn học thuật** | Đã ghi nhận rõ: "Không phát hiện rò rỉ dữ liệu trong bộ kiểm tra 7 tiêu chí"; SHAP Dependence thể hiện liên hệ thống kê, không phải quan hệ nhân quả; Web App là Prototype học thuật, chưa thể thay thế phê duyệt tín dụng thực tế. |

---

## 2. Thông tin môi trường thực nghiệm đã xác minh bổ sung

Trong lần kiểm tra trước, phiên bản cụ thể của Python và các thư viện được đánh dấu `[CẦN XÁC MINH]`. Tại bước này, hệ thống đã thực thi lệnh kiểm tra trực tiếp trên môi trường ảo `.venv`:

| Phần mềm / Thư viện | Phiên bản thực tế đã xác minh | Ghi chú cập nhật |
|---|---|---|
| **Python** | **3.14.4** (64-bit AMD64) | Đã cập nhật vào Bảng 3.1 trong file Word |
| **scikit-learn** | **1.9.1** | Đã cập nhật vào Bảng 3.1 trong file Word |
| **xgboost** | **3.4.1** | Đã cập nhật vào Bảng 3.1 trong file Word |
| **streamlit** | **1.65.0** | Đã cập nhật vào Bảng 3.1 trong file Word |
| **shap** | **0.52.0** | Đã cập nhật vào Bảng 3.1 trong file Word |
| **pandas** | **3.0.5** | Đã cập nhật vào Bảng 3.1 trong file Word |
| **numpy** | **2.5.3** | Đã cập nhật vào Bảng 3.1 trong file Word |
| **python-docx** | **1.2.0** | Thư viện tạo tài liệu Word |

---

## 3. Danh mục Ánh xạ Hình ảnh (Figure Mapping) đưa vào Word

Tất cả hình ảnh được chèn từ đường dẫn thực tế `reports/figures/`, định dạng căn giữa, có chú thích bên dưới (Italic, size 12):

| Ký hiệu trong Word | Tên hình ảnh | Đường dẫn file nguồn | Kích thước nhúng |
|---|---|---|---|
| **Hình 3.1** | Biểu đồ phân bố biến mục tiêu trước xử lý | `reports/figures/target_distribution.png` | Rộng 14 cm |
| **Hình 3.2** | Biểu đồ phân bố đặc trưng nhân khẩu học | `reports/figures/demographic_distribution.png` | Rộng 15 cm |
| **Hình 3.3** | Ma trận tương quan Pearson giữa các đặc trưng | `reports/figures/correlation_heatmap.png` | Rộng 15 cm |
| **Hình 3.4** | Đường cong ROC so sánh 7 mô hình Baseline và Ensemble | `reports/figures/week7_roc_curve_comparison.png` | Rộng 14 cm |
| **Hình 3.5** | Đường cong Precision-Recall so sánh 7 mô hình | `reports/figures/week7_pr_curve_comparison.png` | Rộng 14 cm |
| **Hình 3.6** | Mức độ quan trọng đặc trưng — Random Forest | `reports/figures/week7_random_forest_feature_importance.png` | Rộng 14 cm |
| **Hình 3.7** | Mức độ quan trọng đặc trưng — XGBoost Baseline | `reports/figures/week7_xgboost_feature_importance.png` | Rộng 14 cm |
| **Hình 3.8** | SHAP Global Feature Importance (Bar Plot) | `reports/figures/week9_shap_bar.png` | Rộng 14 cm |
| **Hình 3.9** | SHAP Beeswarm Plot trên toàn bộ tập Test | `reports/figures/week9_shap_beeswarm.png` | Rộng 15 cm |
| **Hình 3.10** | SHAP Dependence Plot cho đặc trưng MAX_PAY_DELAY | `reports/figures/week9_dependence_MAX_PAY_DELAY.png` | Rộng 14 cm |
| **Hình 3.11** | SHAP Dependence Plot cho đặc trưng PAY_0 | `reports/figures/week9_dependence_PAY_0.png` | Rộng 14 cm |
| **Hình 3.12** | SHAP Waterfall Plot — Ca rủi ro cao (Index 3433) | `reports/figures/week9_waterfall_high_risk.png` | Rộng 14 cm |
| **Hình 3.13** | SHAP Waterfall Plot — Ca rủi ro thấp (Index 1985) | `reports/figures/week9_waterfall_low_risk.png` | Rộng 14 cm |
| **Hình 3.14** | SHAP Waterfall Plot — Ca biên giới ngưỡng (Index 1753) | `reports/figures/week9_waterfall_near_threshold.png` | Rộng 14 cm |

---

## 4. Danh mục Bảng biểu đưa vào Word

| Ký hiệu Bảng | Tên Bảng | Số cột | Số dòng | Nội dung chính |
|---|---|:---:|:---:|---|
| **Bảng 2.1** | Checklist 7 tiêu chí kiểm soát rò rỉ dữ liệu | 3 | 8 | 7 tiêu chí kiểm soát Data Leakage |
| **Bảng 2.2** | 10 đặc trưng tài chính tổng hợp đề xuất | 4 | 11 | Tên biến, công thức toán học, ý nghĩa nghiệp vụ |
| **Bảng 2.3** | Ma trận nhầm lẫn chuẩn trong bài toán phân loại nhị phân | 3 | 3 | Cấu trúc TP, FP, TN, FN |
| **Bảng 3.1** | Môi trường phần mềm và thư viện thực nghiệm | 3 | 9 | Python 3.14.4 và các thư viện khoa học dữ liệu |
| **Bảng 3.2** | Cấu trúc tập dữ liệu và mã nguồn dự án | 2 | 10 | Phân bổ các tệp tin trong repository |
| **Bảng 3.3** | Phân bố biến mục tiêu trước xử lý | 4 | 4 | 30.000 mẫu, 77,88% vs 22,12% |
| **Bảng 3.4** | Thống kê mô tả các biến số học tiêu biểu | 7 | 6 | Mean, Std, Min, Median, Max, Skewness |
| **Bảng 3.5** | Kết quả phân chia tập dữ liệu Train / Test | 6 | 4 | 23.972 mẫu (Train) / 5.993 mẫu (Test) |
| **Bảng 3.6** | Kết quả kiểm định chất lượng ma trận đặc trưng sau FE | 4 | 8 | 33 biến, không NaN, không Inf, không rò rỉ |
| **Bảng 3.7** | Thống kê mô tả 10 đặc trưng tổng hợp mới | 6 | 11 | Mean, Median, Min, Max, Skewness |
| **Bảng 3.8** | Kết quả mô hình Logistic Regression trên tập Test | 7 | 3 | LR Default vs LR Balanced |
| **Bảng 3.9** | Ma trận nhầm lẫn của mô hình Logistic Regression | 3 | 3 | LR Default & LR Balanced confusion matrix |
| **Bảng 3.10** | So sánh hiệu năng 7 mô hình Baseline và Ensemble | 7 | 8 | LR, DT, RF, XGBoost |
| **Bảng 3.11** | Siêu tham số tối ưu và điểm CV sau RandomizedSearchCV | 3 | 4 | Tham số RF Tuned, RF Balanced Tuned, XGBoost Tuned |
| **Bảng 3.12** | Hiệu năng mô hình XGBoost trước và sau khi Tuning | 4 | 7 | Thay đổi Acc, Precision, Recall, F1, ROC-AUC, PR-AUC |
| **Bảng 3.13** | Bảng tổng hợp so sánh toàn diện 10 cấu hình mô hình | 7 | 11 | Bảng đối sánh hoàn chỉnh toàn đồ án |
| **Bảng 3.14** | So sánh 3 mô hình Tuned theo tiêu chí lựa chọn | 4 | 7 | Luận chứng lựa chọn XGBoost Tuned |
| **Bảng 3.15** | Top 10 đặc trưng quan trọng nhất theo Mean \|SHAP Value\| | 5 | 11 | Thứ hạng, Mean \|SHAP\|, nguồn gốc đặc trưng |
| **Bảng 3.16** | Tóm tắt kết quả giải thích cá thể 3 hồ sơ đại diện | 8 | 4 | High Risk, Low Risk, Near Threshold |
| **Bảng 3.17** | Kết quả kiểm thử tích hợp ứng dụng Web (6 bài test) | 5 | 7 | 6/6 test PASS với mã lỗi 0 |

---

## 5. Danh sách Vấn đề và Giải pháp Xử lý

| # | Vấn đề phát hiện | Giải pháp thực hiện trong file Word |
|---|---|---|
| 1 | Các khối sơ đồ ASCII (như sơ đồ Pipeline ở Mục 2.1) hiển thị kém trên Word nếu để dạng text thô. | Chuyển thành bảng quy trình có viền rõ ràng, định dạng font Consolas/Courier New hoặc bảng phân bước có đánh số chuyên nghiệp. |
| 2 | Công thức toán LaTeX phức tạp (ví dụ công thức Shapley, hàm mục tiêu XGBoost, công thức Gini) | Trình bày dạng ký hiệu chuẩn Unicode / Toán học hiển thị đẹp mắt, căn giữa dòng, cỡ chữ 13pt rõ ràng. |
| 3 | Dung lượng file Word khi chèn 14 hình ảnh chất lượng cao | Hình ảnh được nén tối ưu hiển thị ở độ rộng 14–15cm (vừa vặn khung lề trang A4: 21cm - 3cm trái - 2cm phải = 16cm lề hữu dụng). |
| 4 | Định dạng trang theo quy chuẩn khóa luận tốt nghiệp | Lề chuẩn: Trái 3,0 cm; Phải 2,0 cm; Trên 2,5 cm; Dưới 2,5 cm. Font Times New Roman 13pt, line spacing 1,5 line (19.5pt), căn đều (Justified), thụt đầu dòng 1,27 cm. |
| 5 | Phân cấp tiêu đề (Heading hierarchy) | Heading 1 (Chương): 14pt Đậm, Giữa; Heading 2: 13pt Đậm, Trái; Heading 3: 13pt Đậm, Trái; gán chuẩn Heading style để hỗ trợ tự động tạo Mục lục (Table of Contents). |
