# BÁO CÁO HỢP NHẤT TOÀN DIỆN KHÓA LUẬN TỐT NGHIỆP
## WEEK11_FULL_THESIS_INTEGRATION_REPORT.md

**Ngày thực hiện:** 24/10/2026  
**Người thực hiện:** AI Research Assistant & Technical Writer  
**Sinh viên:** Nguyễn Trọng Thể — MSSV: 1150080117 — Lớp: THMT (Khóa 2022–2026)  
**Giảng viên hướng dẫn:** TS. Dương Thị Thúy Nga  
**Đề tài:** NGHIÊN CỨU XÂY DỰNG MÔ HÌNH MACHINE LEARNING TRONG ĐÁNH GIÁ VÀ DỰ BÁO RỦI RO TÍN DỤNG KHÁCH HÀNG  
**Trường:** Đại học Tài nguyên và Môi trường TP.HCM — Khoa Công nghệ Thông tin  

---

## 1. Mục tiêu và Tóm tắt Giai đoạn (Phase 4)

Giai đoạn Week 11 — Phase 4 thực hiện nhiệm vụ hợp nhất toàn bộ các thành phần của khóa luận tốt nghiệp thành một tài liệu Microsoft Word (.docx) duy nhất, hoàn chỉnh, chuyên nghiệp và chuẩn mực theo quy định đào tạo. Quá trình hợp nhất bảo toàn nguyên vẹn 100% các kết quả học thuật, công thức toán học, bảng biểu đối sánh và 14 hình ảnh thực nghiệm độ phân giải cao đã được xác minh ở các tuần trước.

---

## 2. Các nguồn tài liệu và thành phần sử dụng

Quá trình tích hợp sử dụng trực tiếp các tài liệu nguồn đã được kiểm định:

| STT | Tài liệu nguồn | Vai trò trong quá trình tích hợp |
|:---:|---|---|
| 1 | `F:\DATN\docs\Bao_Cao_DATN_NguyenTrongThe.docx` | Cung cấp Trang bìa chính (Bìa ngoài), Trang bìa phụ (Bìa trong), Lời cảm ơn, Lời cam đoan, Khung nhận xét GVHD & GVPB, và toàn bộ nội dung học thuật Chương 1 (Mục 1.1–1.5.2 kèm 3 bảng biểu nghiên cứu). |
| 2 | `F:\DATN\docs\Chuong_2_Phuong_Phap_Thuc_Hien.docx` / `scripts/export_chuong2_word.py` | Cung cấp toàn bộ nội dung phương pháp luận Chương 2 (Mục 2.1–2.9.2, 4 bảng, công thức toán học, sơ đồ pipeline). |
| 3 | `F:\DATN\docs\Chuong_3_Cai_Dat_Thuc_Nghiem_Danh_Gia.docx` / `scripts/export_chuong3_word.py` | Cung cấp toàn bộ kết quả thực nghiệm Chương 3 (Mục 3.1–3.8.2, 17 bảng số liệu, kết quả kiểm thử Web DSS 6/6 PASS). |
| 4 | `reports/figures/*.png` (14 file ảnh gốc) | Nhúng trực tiếp 14 đồ thị thực nghiệm gốc (ROC, PR, Feature Importance, SHAP Bar, Beeswarm, Dependence, Waterfall). |
| 5 | `reports/WEEK11_WORD_EXPORT_CHECKLIST.md` | Biên bản kiểm định chất lượng đối chiếu số liệu và thông số môi trường đã xác minh. |
| 6 | `reports/WEEK11_CHAPTERS_VERIFICATION.md` | Báo cáo đối chiếu 47 chỉ số thực nghiệm và mã nguồn pipeline. |

---

## 3. Tệp tin đầu ra chính thức

Tài liệu khóa luận tốt nghiệp hợp nhất đã được khởi tạo và lưu trữ tại hai đường dẫn:

1. **Đường dẫn chính thức theo yêu cầu:**  
   [`F:\DATN\project\docs\Bao_Cao_DATN_NguyenTrongThe_Full.docx`](file:///f:/DATN/project/docs/Bao_Cao_DATN_NguyenTrongThe_Full.docx)  
   - Kích thước: **2.274.517 bytes (~2,27 MB)**  
   - Thời gian cập nhật: 24/10/2026 14:53:09  

2. **Bản sao dự phòng đồng bộ tại Documentation Root:**  
   [`F:\DATN\docs\Bao_Cao_DATN_NguyenTrongThe_Full.docx`](file:///f:/DATN/docs/Bao_Cao_DATN_NguyenTrongThe_Full.docx)  
   - Kích thước: **2.274.517 bytes (~2,27 MB)**  

---

## 4. Thống kê cấu trúc chi tiết bản khóa luận hợp nhất

Qua kiểm tra định lượng trực tiếp trên cấu trúc OpenXML của tệp tin `Bao_Cao_DATN_NguyenTrongThe_Full.docx`:

- **Tổng số đoạn văn (Paragraphs):** **706 đoạn văn**.
- **Tổng số bảng biểu (Tables):** **25 bảng biểu hoàn chỉnh** (có viền đơn chuẩn, tiêu đề bảng in đậm căn giữa, dòng tiêu đề tô nền `#EAECEF`).
- **Tổng số hình ảnh thực tế (Pictures):** **14 hình ảnh đồ thị thực nghiệm** (được nhúng dưới dạng Inline Shapes từ file PNG thực tế tại `reports/figures/`, không có hình ảnh giả).
- **Tổng số phân vùng văn bản (Sections):** **3 sections** (bảo toàn cấu trúc trang bìa, phần thủ tục hành chính và phần nội dung học thuật có đánh số trang).
- **Phân cấp tiêu đề (Heading Hierarchy):**
  - **Heading 1 (Tên chương / Phần lớn):** **5 mục** (Chương 1, Chương 2, Chương 3, Kết luận và Hướng phát triển, Tài liệu tham khảo).
  - **Heading 2 (Mục cấp 1):** **25 mục** (1.1–1.5, 2.1–2.9, 3.1–3.8, và 3 mục Kết luận).
  - **Heading 3 (Mục cấp 2):** **55 tiểu mục** chi tiết theo đúng Đề cương chi tiết (DCCT).

---

## 5. Danh mục các Bảng biểu và Hình ảnh trong bản hợp nhất

### 5.1. Bảng biểu (25 bảng)
- **Bảng Từ viết tắt:** Bảng danh mục 20 từ viết tắt chuyên ngành AI/ML và Tài chính ngân hàng (21 dòng × 3 cột).
- **Chương 1 (3 bảng):**
  - Bảng 1.1: Tổng hợp các công trình nghiên cứu nước ngoài tiêu biểu (6 dòng × 9 cột).
  - Bảng 1.2: Tổng hợp các công trình nghiên cứu trong nước (5 dòng × 9 cột).
  - Bảng 1.3: Mô tả chi tiết 23 biến dự báo và biến mục tiêu tập UCI Credit Card (26 dòng × 4 cột).
- **Chương 2 (4 bảng):**
  - Bảng 2.1: Các giai đoạn trong quy trình thực nghiệm Machine Learning Pipeline (9 dòng × 3 cột).
  - Bảng 2.2: Bộ tiêu chí kiểm soát rò rỉ dữ liệu — Data Leakage Audit 7 tiêu chí (8 dòng × 3 cột).
  - Bảng 2.3: Danh mục 10 đặc trưng tài chính tổng hợp đề xuất trích xuất (11 dòng × 4 cột).
  - Bảng 2.4: Ma trận nhầm lẫn chuẩn trong phân loại rủi ro tín dụng nhị phân (3 dòng × 3 cột).
- **Chương 3 (17 bảng):**
  - Bảng 3.1: Danh mục thư viện khoa học dữ liệu và phiên bản thực nghiệm đã xác minh (8 dòng × 3 cột).
  - Bảng 3.2: Cấu trúc thư mục và mã nguồn dự án (7 dòng × 2 cột).
  - Bảng 3.3: Phân bố biến mục tiêu vỡ nợ trước xử lý (4 dòng × 4 cột).
  - Bảng 3.4: Thống kê mô tả và hệ số Skewness các biến số học tiêu biểu (6 dòng × 7 cột).
  - Bảng 3.5: Kết quả phân chia Train/Test 80/20 phân tầng (4 dòng × 6 cột).
  - Bảng 3.6: Kết quả kiểm định chất lượng ma trận đặc trưng sau FE (8 dòng × 4 cột).
  - Bảng 3.7: Thống kê mô tả 10 đặc trưng tổng hợp mới trên tập Train (11 dòng × 6 cột).
  - Bảng 3.8: Kết quả mô hình Logistic Regression trên tập Test (3 dòng × 7 cột).
  - Bảng 3.9: So sánh ma trận nhầm lẫn LR Default vs LR Balanced (3 dòng × 3 cột).
  - Bảng 3.10: So sánh hiệu năng 7 mô hình Baseline và Ensemble trên tập Test (8 dòng × 7 cột).
  - Bảng 3.11: Siêu tham số tối ưu và điểm CV PR-AUC sau RandomizedSearchCV (4 dòng × 3 cột).
  - Bảng 3.12: So sánh hiệu năng XGBoost trước và sau khi Tuning (7 dòng × 4 cột).
  - Bảng 3.13: Bảng tổng hợp đối sánh toàn bộ 10 cấu hình mô hình trên tập Test (11 dòng × 7 cột).
  - Bảng 3.14: So sánh 3 mô hình Ensemble Tuned theo tiêu chí tuyển chọn (7 dòng × 4 cột).
  - Bảng 3.15: Top 10 đặc trưng quan trọng nhất theo Mean |SHAP Value| (11 dòng × 5 cột).
  - Bảng 3.16: Tóm tắt kết quả phân tích giải thích cá thể cho 3 hồ sơ đại diện (4 dòng × 8 cột).
  - Bảng 3.17: Kết quả thực thi bộ kiểm thử tích hợp Web Prototype 6 bài test PASS (7 dòng × 5 cột).

### 5.2. Hình ảnh đồ thị thực nghiệm (14 hình)
- **Hình 3.1:** Biểu đồ phân bố biến mục tiêu thể hiện mức độ mất cân bằng lớp (`target_distribution.png`).
- **Hình 3.2:** Phân bố đặc trưng nhân khẩu học theo giới tính, học vấn, hôn nhân (`demographic_distribution.png`).
- **Hình 3.3:** Ma trận tương quan Pearson giữa các đặc trưng đầu vào và nhãn vỡ nợ (`correlation_heatmap.png`).
- **Hình 3.4:** Đường cong ROC so sánh năng lực phân loại của 7 mô hình học máy (`week7_roc_curve_comparison.png`).
- **Hình 3.5:** Đường cong Precision-Recall so sánh hiệu năng trên lớp thiểu số (`week7_pr_curve_comparison.png`).
- **Hình 3.6:** Mức độ quan trọng đặc trưng trích xuất từ Random Forest (`week7_random_forest_feature_importance.png`).
- **Hình 3.7:** Mức độ quan trọng đặc trưng trích xuất từ XGBoost Baseline (`week7_xgboost_feature_importance.png`).
- **Hình 3.8:** Biểu đồ thanh SHAP Global Feature Importance theo Mean |SHAP| (`week9_shap_bar.png`).
- **Hình 3.9:** Biểu đồ SHAP Beeswarm Plot thể hiện độ lớn và chiều hướng tác động (`week9_shap_beeswarm.png`).
- **Hình 3.10:** Biểu đồ phụ thuộc SHAP Dependence Plot của đặc trưng `MAX_PAY_DELAY` (`week9_dependence_MAX_PAY_DELAY.png`).
- **Hình 3.11:** Biểu đồ phụ thuộc SHAP Dependence Plot của đặc trưng `PAY_0` (`week9_dependence_PAY_0.png`).
- **Hình 3.12:** Biểu đồ SHAP Waterfall giải thích hồ sơ Rủi ro cao (Index 3433, Prob = 96,16%) (`week9_waterfall_high_risk.png`).
- **Hình 3.13:** Biểu đồ SHAP Waterfall giải thích hồ sơ Rủi ro thấp (Index 1985, Prob = 2,84%) (`week9_waterfall_low_risk.png`).
- **Hình 3.14:** Biểu đồ SHAP Waterfall giải thích hồ sơ Biên giới ngưỡng (Index 1753, Prob = 60,01%) (`week9_waterfall_near_threshold.png`).

---

## 6. Kết quả kiểm tra theo Bộ 9 tiêu chí của Bước E

| # | Tiêu chí kiểm tra | Kết quả thực tế | Trạng thái |
|:---:|---|---|:---:|
| 1 | File mở được bình thường, có đầy đủ các chương | Mở trơn tru bằng thư viện python-docx và Microsoft Word, không phát sinh lỗi XML. | ✅ PASS |
| 2 | Số lượng bảng và hình không bị mất mát | Đủ 25 bảng biểu và 14 hình ảnh thực tế, khớp 100% danh mục thiết kế. | ✅ PASS |
| 3 | Không có chương hoặc mục bị lặp | Cấu trúc đề mục tuần tự từ Chương 1, 2, 3 đến Kết luận; không có mục nào bị trùng lặp. | ✅ PASS |
| 4 | Không có trang trống bất thường | Sử dụng ngắt trang chủ động (`doc.add_page_break()`) ở đầu mỗi chương và danh mục. | ✅ PASS |
| 5 | Tiêu đề và thứ tự chương chính xác | Thứ tự chương: Chương 1 → Chương 2 → Chương 3 → Kết luận → Tài liệu tham khảo. | ✅ PASS |
| 6 | Bảng biểu hiển thị rõ ràng, không mất chữ | Các bảng có độ rộng cột chuẩn, căn lề hợp lý, font chữ 9–11pt vừa vặn khổ A4. | ✅ PASS |
| 7 | Hình ảnh hiển thị sắc nét | Các hình ảnh PNG gốc được giữ nguyên tỷ lệ, kích thước 14–15cm vừa vặn lề hữu dụng. | ✅ PASS |
| 8 | Tài liệu tham khảo nhất quán | 13 tài liệu tham khảo chuẩn APA được trình bày ở cuối tài liệu với định dạng hanging indent. | ✅ PASS |
| 9 | Các nội dung hạn chế được ghi nhận rõ | Đã trình bày minh bạch 4 hạn chế học thuật trong Chương 3 và phần Kết luận. | ✅ PASS |

---

## 7. Hướng dẫn các thao tác cần thực hiện khi mở file trong Microsoft Word

Khi sinh viên mở tệp tin [`Bao_Cao_DATN_NguyenTrongThe_Full.docx`](file:///f:/DATN/project/docs/Bao_Cao_DATN_NguyenTrongThe_Full.docx) trên máy tính bằng phần mềm Microsoft Word:

1. **Cập nhật Mục lục tự động:**
   - Nhấn tổ hợp phím `Ctrl + A` (chọn toàn bộ văn bản).
   - Nhấn phím `F9` (hoặc click chuột phải vào vùng Mục lục, chọn **Update Field** → chọn **Update entire table**).
   - Microsoft Word sẽ tự động quét lại toàn bộ các đề mục Heading 1, 2, 3 và đồng bộ chính xác số trang theo bố cục hiển thị thực tế của máy in.
2. **Ký tên và điền thông tin hành chính:**
   - Tại trang **Lời cảm ơn** và **Lời cam đoan**: Ký tên và ghi rõ họ tên sinh viên thực hiện (*Nguyễn Trọng Thể*).
   - Trang **Nhận xét của Giảng viên hướng dẫn** và **Giảng viên phản biện**: Giữ nguyên khung nhận xét để nộp cho thầy cô đánh giá và cho điểm theo quy chế.
3. **In ấn / Xuất file PDF:**
   - Tài liệu đã được thiết lập sẵn lề chuẩn đóng gáy đồ án: **Lề trái 3,0 cm; Lề phải 2,0 cm; Lề trên 2,5 cm; Lề dưới 2,5 cm; Khổ giấy A4**. Sinh viên có thể chọn trực tiếp lệnh `File -> Save As -> PDF` để nộp bản mềm.

---

## 8. Kết luận và Tuân thủ an toàn

- **Quy tắc an toàn được bảo đảm tuyệt đối:**
  - File gốc `Bao_Cao_DATN_NguyenTrongThe.docx` được giữ nguyên vẹn, không bị ghi đè.
  - Các file Word độc lập `Chuong_2_Phuong_Phap_Thuc_Hien.docx` và `Chuong_3_Cai_Dat_Thuc_Nghiem_Danh_Gia.docx` được bảo lưu hoàn toàn.
  - Không sửa mã nguồn ứng dụng, notebook, bộ dữ liệu hay mô hình đã huấn luyện.
  - Không huấn luyện lại mô hình.
- File khóa luận hợp nhất `Bao_Cao_DATN_NguyenTrongThe_Full.docx` đã được tạo thành công, kiểm định hoàn chỉnh và sẵn sàng cho các bước chuẩn bị bảo vệ đồ án tốt nghiệp.
