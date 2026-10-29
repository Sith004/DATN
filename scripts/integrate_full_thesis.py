# -*- coding: utf-8 -*-
"""
Script Hop nhat Toan bo Khoa luan Tot nghiep (Full Graduation Thesis Integration)
Bao gom:
- Trang bia 1, Trang bia 2
- Loi cam on, Loi cam doan
- Nhan xet GVHD, Nhan xet GVPB
- Muc luc toan dien (Ch1, Ch2, Ch3, Ket luan, Tai lieu tham khao)
- Danh muc Tu viet tat
- Danh muc Bang bieu
- Danh muc Hinh ve
- Chuong 1: Tong quan tai lieu va cac cong trinh nghien cuu lien quan
- Chuong 2: Phuong phap thuc hien
- Chuong 3: Cai dat thuc nghiem va danh gia ket qua
- Ket luan va Huong phat trien
- Tai lieu tham khao

Sinh vien: Nguyen Trong The - MSSV: 1150080117
GVHD: TS. Duong Thi Thuy Nga
"""

import sys, io, os
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import docx
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from export_chuong2_word import (
    add_chapter_2_content, set_font, set_para_format,
    add_heading1, add_heading2, add_heading3, add_body_para,
    add_bullet_item, add_formula_para, add_table_caption,
    set_cell, set_table_borders
)
from export_chuong3_word import add_chapter_3_content, add_figure

def add_toc_entry(doc, title, page_str, level=1):
    para = doc.add_paragraph()
    try:
        para.style = doc.styles[f'toc {level}']
    except Exception:
        pass
    
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(1)
    pf.space_after = Pt(2)
    pf.line_spacing = Pt(16)
    
    if level == 1:
        pf.left_indent = Cm(0)
        bold = True
        size = 12
    elif level == 2:
        pf.left_indent = Cm(0.8)
        bold = False
        size = 11.5
    else:
        pf.left_indent = Cm(1.6)
        bold = False
        size = 11
        
    run_t = para.add_run(title)
    set_font(run_t, size=size, bold=bold)
    
    run_tab = para.add_run("\t")
    set_font(run_tab, size=size)
    
    run_p = para.add_run(str(page_str))
    set_font(run_p, size=size, bold=bold)
    return para

def add_list_of_abbreviations(doc):
    add_heading1(doc, "DANH MỤC TỪ VIẾT TẮT")
    add_body_para(doc, "Dưới đây là danh mục các thuật ngữ khoa học và từ viết tắt chuyên ngành được sử dụng trong đồ án tốt nghiệp:", indent=False)
    
    t_abbr = doc.add_table(rows=21, cols=3)
    t_abbr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_abbr)
    col_w = [Cm(2.5), Cm(6.5), Cm(7.0)]
    
    headers = ["Ký hiệu", "Thuật ngữ Tiếng Anh", "Ý nghĩa Tiếng Việt"]
    for i, h in enumerate(headers):
        set_cell(t_abbr.cell(0, i), h, bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_abbr.cell(0, i).width = col_w[i]
        
    abbr_data = [
        ("AI", "Artificial Intelligence", "Trí tuệ nhân tạo"),
        ("ANN", "Artificial Neural Network", "Mạng nơ-ron nhân tạo"),
        ("AUC", "Area Under Curve", "Diện tích dưới đường cong"),
        ("CV", "Cross-Validation", "Kiểm thực chéo"),
        ("DSS", "Decision Support System", "Hệ thống hỗ trợ ra quyết định"),
        ("DT", "Decision Tree", "Cây quyết định"),
        ("EAD", "Exposure at Default", "Dư nợ tại thời điểm vỡ nợ"),
        ("EDA", "Exploratory Data Analysis", "Phân tích khám phá dữ liệu"),
        ("FE", "Feature Engineering", "Kỹ thuật trích rút đặc trưng"),
        ("FN", "False Negative", "Bỏ sót rủi ro (Dương tính giả)"),
        ("FP", "False Positive", "Cảnh báo nhầm (Dương tính sai)"),
        ("IQR", "Interquartile Range", "Khoảng tứ phân vị (Q75 - Q25)"),
        ("LGD", "Loss Given Default", "Tổn thất khi vỡ nợ"),
        ("LR", "Logistic Regression", "Hồi quy Logistic"),
        ("ML", "Machine Learning", "Học máy"),
        ("OOF", "Out-Of-Fold", "Dự báo ngoài tập fold"),
        ("PD", "Probability of Default", "Xác suất vỡ nợ"),
        ("PR-AUC", "Precision-Recall AUC", "Diện tích dưới đường cong Precision-Recall"),
        ("RF", "Random Forest", "Rừng ngẫu nhiên"),
        ("SHAP", "SHapley Additive exPlanations", "Khung giải thích cộng tính Shapley")
    ]
    for r_idx, d in enumerate(abbr_data, start=1):
        set_cell(t_abbr.cell(r_idx, 0), d[0], bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_abbr.cell(r_idx, 1), d[1], bold=False, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_abbr.cell(r_idx, 2), d[2], bold=False, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
        for c in range(3):
            t_abbr.cell(r_idx, c).width = col_w[c]

def add_list_of_tables(doc):
    add_heading1(doc, "DANH MỤC BẢNG")
    
    tables_list = [
        ("Bảng 1.1", "Tổng hợp các công trình nghiên cứu nước ngoài tiêu biểu", "11"),
        ("Bảng 1.2", "Tổng hợp các công trình nghiên cứu trong nước (Việt Nam)", "12"),
        ("Bảng 1.3", "Mô tả chi tiết các biến trong tập dữ liệu UCI Credit Card Clients", "20"),
        ("Bảng 2.1", "Các giai đoạn trong quy trình thực nghiệm Machine Learning Pipeline", "24"),
        ("Bảng 2.2", "Bộ tiêu chí kiểm soát rò rỉ dữ liệu (Data Leakage Audit)", "26"),
        ("Bảng 2.3", "Danh mục 10 đặc trưng tài chính tổng hợp được đề xuất trích xuất", "28"),
        ("Bảng 2.4", "Ma trận nhầm lẫn chuẩn trong phân loại rủi ro tín dụng nhị phân", "30"),
        ("Bảng 3.1", "Danh mục các thư viện khoa học dữ liệu và phiên bản thực nghiệm", "34"),
        ("Bảng 3.2", "Cấu trúc thư mục và các thành phần chính của repository dự án", "35"),
        ("Bảng 3.3", "Phân bố biến mục tiêu vỡ nợ (default.payment.next.month) trước xử lý", "36"),
        ("Bảng 3.4", "Thống kê mô tả và hệ số lệch (Skewness) các biến số học tiêu biểu", "37"),
        ("Bảng 3.5", "Kết quả phân chia tập dữ liệu Train / Test theo tỷ lệ 80/20 phân tầng", "38"),
        ("Bảng 3.6", "Kết quả kiểm định chất lượng ma trận đặc trưng sau Feature Engineering", "39"),
        ("Bảng 3.7", "Thống kê mô tả 10 đặc trưng tổng hợp mới trên tập huấn luyện (X_train)", "40"),
        ("Bảng 3.8", "Kết quả mô hình Logistic Regression trên tập kiểm tra Test", "41"),
        ("Bảng 3.9", "So sánh ma trận nhầm lẫn giữa LR Default và LR Balanced trên tập Test", "42"),
        ("Bảng 3.10", "Bảng so sánh hiệu năng 7 mô hình Baseline và Ensemble trên tập Test", "43"),
        ("Bảng 3.11", "Bộ siêu tham số tối ưu và điểm kiểm thực chéo (CV PR-AUC) của 3 mô hình Ensemble", "45"),
        ("Bảng 3.12", "So sánh hiệu năng mô hình XGBoost trên tập Test trước và sau khi tối ưu siêu tham số", "46"),
        ("Bảng 3.13", "Bảng tổng hợp đối sánh toàn bộ 10 cấu hình mô hình trên tập Test", "47"),
        ("Bảng 3.14", "So sánh 3 mô hình Ensemble Tuned theo các tiêu chí lựa chọn cốt lõi", "48"),
        ("Bảng 3.15", "Top 10 đặc trưng quan trọng nhất theo giá trị trung bình SHAP tuyệt đối (Mean |SHAP|)", "49"),
        ("Bảng 3.16", "Tóm tắt kết quả phân tích giải thích cá thể (Local Waterfall) cho 3 hồ sơ đại diện", "51"),
        ("Bảng 3.17", "Kết quả thực thi bộ kiểm thử tích hợp tự động hệ thống Web Prototype (6 bài test)", "53")
    ]
    
    for tbl_num, tbl_name, page_num in tables_list:
        add_toc_entry(doc, f"{tbl_num}: {tbl_name}", page_num, level=2)

def add_list_of_figures(doc):
    add_heading1(doc, "DANH MỤC HÌNH VẼ")
    
    figures_list = [
        ("Hình 3.1", "Biểu đồ phân bố biến mục tiêu thể hiện mức độ mất cân bằng lớp", "36"),
        ("Hình 3.2", "Phân bố đặc trưng nhân khẩu học theo giới tính, học vấn và hôn nhân", "37"),
        ("Hình 3.3", "Ma trận tương quan Pearson giữa các đặc trưng đầu vào và biến mục tiêu", "38"),
        ("Hình 3.4", "Đường cong ROC so sánh năng lực phân loại của 7 mô hình học máy", "43"),
        ("Hình 3.5", "Đường cong Precision-Recall so sánh hiệu năng trên lớp thiểu số của 7 mô hình", "44"),
        ("Hình 3.6", "Mức độ quan trọng đặc trưng trích xuất từ mô hình Random Forest", "47"),
        ("Hình 3.7", "Mức độ quan trọng đặc trưng trích xuất từ mô hình XGBoost Baseline", "48"),
        ("Hình 3.8", "Biểu đồ thanh SHAP Global Feature Importance theo độ lớn Mean |SHAP|", "50"),
        ("Hình 3.9", "Biểu đồ SHAP Beeswarm Plot thể hiện độ lớn và chiều hướng tác động của đặc trưng", "50"),
        ("Hình 3.10", "Biểu đồ phụ thuộc SHAP Dependence Plot của đặc trưng MAX_PAY_DELAY", "51"),
        ("Hình 3.11", "Biểu đồ phụ thuộc SHAP Dependence Plot của đặc trưng PAY_0", "51"),
        ("Hình 3.12", "Biểu đồ SHAP Waterfall giải thích hồ sơ Rủi ro cao (Index 3433, Prob = 96,16%)", "52"),
        ("Hình 3.13", "Biểu đồ SHAP Waterfall giải thích hồ sơ Rủi ro thấp (Index 1985, Prob = 2,84%)", "52"),
        ("Hình 3.14", "Biểu đồ SHAP Waterfall giải thích hồ sơ Biên giới ngưỡng (Index 1753, Prob = 60,01%)", "53")
    ]
    
    for fig_num, fig_name, page_num in figures_list:
        add_toc_entry(doc, f"{fig_num}: {fig_name}", page_num, level=2)

def add_full_table_of_contents(doc):
    # Header title
    para = doc.add_paragraph()
    run = para.add_run('MỤC LỤC')
    set_font(run, size=14, bold=True)
    para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after = Pt(6)
    
    # Instruction note
    p_note = doc.add_paragraph()
    r_note = p_note.add_run('(Nhấn Ctrl+A rồi nhấn F9 trong Microsoft Word để tự động cập nhật số trang và cấu trúc mục lục)')
    set_font(r_note, size=11, italic=True, color=(120, 120, 120))
    p_note.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_note.paragraph_format.space_before = Pt(0)
    p_note.paragraph_format.space_after = Pt(12)
    
    # Static structured TOC entries
    toc_items = [
        ("LỜI CẢM ƠN", "i", 1),
        ("LỜI CAM ĐOAN", "ii", 1),
        ("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", "iii", 1),
        ("NHẬN XÉT CỦA GIẢNG VIÊN PHẢN BIỆN", "iv", 1),
        ("MỤC LỤC", "v", 1),
        ("DANH MỤC TỪ VIẾT TẮT", "vi", 1),
        ("DANH MỤC BẢNG", "vii", 1),
        ("DANH MỤC HÌNH VẼ", "viii", 1),
        
        ("CHƯƠNG 1. TỔNG QUAN TÀI LIỆU VÀ CÁC CÔNG TRÌNH NGHIÊN CỨU LIÊN QUAN", "1", 1),
        ("1.1. Tổng quan về rủi ro tín dụng và bài toán chấm điểm tín dụng", "1", 2),
        ("1.1.1. Khái niệm rủi ro tín dụng (Credit Risk) và vỡ nợ (Default)", "1", 3),
        ("1.1.2. Vai trò của Chấm điểm tín dụng (Credit Scoring) trong quản trị rủi ro ngân hàng", "2", 3),
        ("1.1.3. Thách thức trong dự báo rủi ro tín dụng cá nhân", "3", 3),
        ("1.2. Tổng quan các công trình nghiên cứu liên quan trong và ngoài nước", "4", 2),
        ("1.2.1. Các công trình nghiên cứu nước ngoài", "4", 3),
        ("1.2.2. Các công trình nghiên cứu trong nước (Việt Nam)", "7", 3),
        ("1.2.3. Bảng so sánh và tổng hợp các công trình nghiên cứu", "9", 3),
        ("1.2.4. Nhận xét tổng quan, khoảng trống nghiên cứu và lý do chọn đề tài", "11", 3),
        ("1.3. Tổng quan về Machine Learning trong bài toán chấm điểm tín dụng", "12", 2),
        ("1.3.1. Bài toán Phân loại nhị phân (Binary Classification)", "12", 3),
        ("1.3.2. Mô hình Hồi quy Logistic (Logistic Regression - Baseline)", "13", 3),
        ("1.3.3. Mô hình Cây quyết định (Decision Tree Classifier)", "14", 3),
        ("1.3.4. Mô hình Rừng ngẫu nhiên (Random Forest Classifier)", "15", 3),
        ("1.3.5. Mô hình XGBoost (Extreme Gradient Boosting)", "16", 3),
        ("1.4. Tập dữ liệu nghiên cứu UCI Credit Card Clients", "17", 2),
        ("1.4.1. Nguồn gốc và ý nghĩa tập dữ liệu nghiên cứu", "17", 3),
        ("1.4.2. Mô tả chi tiết các biến dự báo và biến mục tiêu", "18", 3),
        ("1.5. Trí tuệ nhân tạo có thể giải thích (Explainable AI) và phương pháp SHAP", "19", 2),
        ("1.5.1. Khái niệm và sự cần thiết của Explainable AI trong lĩnh vực tài chính", "19", 3),
        ("1.5.2. Nguyên lý toán học Shapley Values và kỹ thuật SHAP (Global & Local Explanations)", "20", 3),
        
        ("CHƯƠNG 2. PHƯƠNG PHÁP THỰC HIỆN", "23", 1),
        ("2.1. Quy trình tổng thể xây dựng mô hình Machine Learning (ML Pipeline)", "23", 2),
        ("2.2. Kiểm duyệt dữ liệu và Phương pháp phân tích khám phá (Data Audit & EDA Methods)", "24", 2),
        ("2.2.1. Phương pháp kiểm duyệt chất lượng dữ liệu (Data Audit)", "24", 3),
        ("2.2.2. Phương pháp phân tích tương quan và trực quan hóa phân phối", "25", 3),
        ("2.3. Phương pháp Tiền xử lý dữ liệu và Quy tắc chống Data Leakage", "25", 2),
        ("2.3.1. Quy tắc phân chia tập Train/Test và kiểm soát rò rỉ dữ liệu", "25", 3),
        ("2.3.2. Phương pháp xử lý giá trị ngoại lệ và giá trị bất thường", "27", 3),
        ("2.3.3. Phương pháp chuẩn hóa (Scaling) và mã hóa đặc trưng duy nhất trên tập Train", "27", 3),
        ("2.4. Đề xuất Kỹ thuật trích rút đặc trưng (Feature Engineering Proposals)", "28", 2),
        ("2.4.1. Đề xuất các biến chỉ số tài chính", "28", 3),
        ("2.4.2. Phương pháp đánh giá thực nghiệm tính hiệu quả của các đặc trưng đề xuất", "29", 3),
        ("2.5. Các thuật toán Machine Learning đề xuất", "29", 2),
        ("2.5.1. Logistic Regression (Mô hình Cơ sở)", "29", 3),
        ("2.5.2. Decision Tree Classifier", "30", 3),
        ("2.5.3. Random Forest Classifier", "30", 3),
        ("2.5.4. XGBoost (Extreme Gradient Boosting)", "30", 3),
        ("2.6. Phương pháp thực nghiệm xử lý Mất cân bằng dữ liệu (Class Imbalance Methods)", "31", 2),
        ("2.6.1. Phân tích lý thuyết tác động của mất cân bằng dữ liệu", "31", 3),
        ("2.6.2. Đề xuất áp dụng Class Weighting, Threshold Tuning và cơ chế kiểm soát SMOTE", "31", 3),
        ("2.7. Phương pháp Đánh giá mô hình, Tối ưu hóa và Lựa chọn mô hình", "32", 2),
        ("2.7.1. Định nghĩa hệ thống chỉ số đánh giá đa chiều", "32", 3),
        ("2.7.2. Phương pháp phân tích Ma trận nhầm lẫn và đánh đổi nghiệp vụ", "33", 3),
        ("2.7.3. Phương pháp Cross-Validation và Tối ưu siêu tham số", "33", 3),
        ("2.7.4. Tiêu chí lựa chọn mô hình phù hợp nhất cho đề tài", "33", 3),
        ("2.8. Phương pháp giải thích mô hình với SHAP", "34", 2),
        ("2.8.1. Phương pháp phân tích đóng góp đặc trưng cấp tổng thể (Global Explanation)", "34", 3),
        ("2.8.2. Phương pháp phân tích đóng góp đặc trưng cấp cá thể (Local Explanation)", "34", 3),
        ("2.9. Phân tích Yêu cầu và Thiết kế Kiến trúc ứng dụng Web Prototype", "35", 2),
        ("2.9.1. Đặc tả yêu cầu chức năng, phi chức năng và luồng xử lý hệ thống", "35", 3),
        ("2.9.2. Thiết kế kiến trúc phần mềm DSS Prototype và nguyên tắc phân loại rủi ro thử nghiệm", "35", 3),
        
        ("CHƯƠNG 3. CÀI ĐẶT THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ", "36", 1),
        ("3.1. Môi trường phát triển và Thư viện cài đặt", "36", 2),
        ("3.1.1. Phần cứng và Hệ điều hành", "36", 3),
        ("3.1.2. Thư viện chính và phiên bản thực nghiệm", "36", 3),
        ("3.1.3. Cấu trúc mã nguồn và dữ liệu", "37", 3),
        ("3.2. Kết quả kiểm duyệt dữ liệu EDA và Cài đặt Tiền xử lý", "37", 2),
        ("3.2.1. Kết quả thực nghiệm kiểm duyệt chất lượng dữ liệu (Data Audit)", "37", 3),
        ("3.2.2. Kết quả thực nghiệm làm sạch dữ liệu và chuẩn hóa", "40", 3),
        ("3.2.3. Kết quả thực nghiệm Feature Engineering", "40", 3),
        ("3.3. Thực nghiệm Xây dựng mô hình cơ sở (Baseline) và So sánh mô hình", "42", 2),
        ("3.3.1. Kết quả huấn luyện mô hình cơ sở — Logistic Regression", "42", 3),
        ("3.3.2. Kết quả huấn luyện và so sánh các mô hình — Decision Tree, Random Forest, XGBoost", "44", 3),
        ("3.4. Thực nghiệm Xử lý mất cân bằng dữ liệu và Tối ưu siêu tham số", "46", 2),
        ("3.4.1. Kết quả so sánh hiệu năng Class Weighting và Threshold Tuning", "46", 3),
        ("3.4.2. Kết quả tối ưu siêu tham số (Hyperparameter Tuning)", "47", 3),
        ("3.5. Bảng tổng hợp Đánh giá mô hình và Lựa chọn mô hình phù hợp nhất", "48", 2),
        ("3.5.1. Bảng so sánh đa chỉ số — Toàn bộ 10 cấu hình mô hình", "48", 3),
        ("3.5.2. Phân tích chi tiết Ma trận nhầm lẫn, trade-off nghiệp vụ và quyết định chọn mô hình", "50", 3),
        ("3.6. Kết quả Thực nghiệm Giải thích mô hình bằng SHAP", "51", 2),
        ("3.6.1. Trực quan hóa kết quả đóng góp đặc trưng tổng thể (Global Feature Importance Plot)", "51", 3),
        ("3.6.2. Phân tích kết quả giải thích dự báo trường hợp khách hàng cụ thể (Local Waterfall Plot)", "53", 3),
        ("3.7. Cài đặt, Triển khai và Kiểm thử ứng dụng Web Prototype", "55", 2),
        ("3.7.1. Cài đặt giao diện người dùng và tích hợp mô hình ML đã chọn", "55", 3),
        ("3.7.2. Kịch bản chạy thử nghiệm dự báo và kiểm thử tích hợp (Integration Tests)", "56", 3),
        ("3.8. Đánh giá tổng quan kết quả thực nghiệm, Thảo luận và Hạn chế đề tài", "57", 2),
        ("3.8.1. Tổng kết các kết quả chính đạt được", "57", 3),
        ("3.8.2. Hạn chế của đề tài và định hướng phát triển thực tế", "58", 3),
        
        ("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "60", 1),
        ("1. Kết luận và tổng kết các kết quả nghiên cứu đạt được", "60", 2),
        ("2. Hạn chế của đề tài", "61", 2),
        ("3. Hướng phát triển trong tương lai", "62", 2),
        
        ("TÀI LIỆU THAM KHẢO", "63", 1)
    ]
    
    for title, page_str, level in toc_items:
        add_toc_entry(doc, title, page_str, level=level)

def add_conclusion_and_future_work(doc):
    add_heading1(doc, "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")
    
    add_body_para(doc, "Đồ án tốt nghiệp với đề tài 'Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng' đã hoàn thành đầy đủ các mục tiêu nghiên cứu và nhiệm vụ thực nghiệm đề ra theo đề cương chi tiết. Dưới đây là tổng kết toàn diện các kết quả đạt được, các hạn chế học thuật còn tồn tại và các định hướng phát triển trong tương lai.", indent=True)
    
    add_heading2(doc, "1. Kết luận và tổng kết các kết quả nghiên cứu đạt được")
    add_body_para(doc, "Thông qua quá trình triển khai thực nghiệm khoa học, bài bản và tuân thủ nghiêm ngặt chuẩn mực kỹ thuật, đề tài đã đạt được 5 kết quả đóng góp cốt lõi sau:")
    
    add_bullet_item(doc, "Đề tài đã xây dựng thành công quy trình xử lý dữ liệu và học máy 8 bước khép kín từ khâu kiểm duyệt chất lượng dữ liệu thô (Data Audit), phân tích khám phá (EDA), làm sạch dữ liệu, phân chia Train/Test phân tầng 80/20, đến chuẩn hóa dữ liệu bằng RobustScaler. Đặc biệt, bộ kiểm tra 7 tiêu chí rò rỉ dữ liệu (Data Leakage Audit) đã được thiết lập và kiểm chứng thực nghiệm đạt chuẩn 100% PASS, bảo đảm tính độc lập tuyệt đối của tập kiểm tra và tính tin cậy của mọi kết quả đánh giá.", bold_prefix="Thứ nhất, về quy trình phương pháp luận và kiểm soát Data Leakage: ")
    
    add_bullet_item(doc, "Dựa trên nghiên cứu chuyên sâu về chu kỳ sao kê và hành vi thanh toán thẻ tín dụng, đề tài đã đề xuất và trích xuất thành công 10 đặc trưng tài chính mới phản ánh lịch sử chậm trả đỉnh điểm, tần suất vi phạm, tỷ lệ thanh toán và quỹ đạo nợ 6 tháng. Bằng chứng định lượng từ thuật toán SHAP xác nhận 4 trong 10 đặc trưng quan trọng nhất toàn hệ thống là các biến mới này, trong đó đặc trưng MAX_PAY_DELAY vươn lên dẫn đầu toàn diện, khẳng định giá trị thực tiễn vượt bậc của Feature Engineering so với việc chỉ sử dụng dữ liệu thô.", bold_prefix="Thứ hai, về giá trị thực tiễn của kỹ thuật trích rút đặc trưng (Feature Engineering): ")
    
    add_bullet_item(doc, "Đề tài đã tiến hành huấn luyện, so sánh và kiểm định đa chỉ số đối với 10 cấu hình mô hình học máy (gồm Logistic Regression, Decision Tree, Random Forest và XGBoost). Mô hình XGBoost Tuned kết hợp điều chỉnh ngưỡng quyết định threshold = 0,60 được lựa chọn là mô hình tối ưu nhất cho bài toán. Mô hình thiết lập kỷ lục PR-AUC cao nhất (0,5620) và Recall phát hiện vỡ nợ đạt 61,61% (tăng +25,79 điểm phần trăm so với cấu hình mặc định), giải quyết xuất sắc bài toán mất cân bằng dữ liệu (tỷ lệ 3,52:1) theo định hướng ưu tiên giảm thiểu tổn thất tín dụng cho ngân hàng.", bold_prefix="Thứ ba, về năng lực dự báo và tối ưu hóa mô hình Machine Learning: ")
    
    add_bullet_item(doc, "Việc tích hợp khung phương pháp SHAP TreeExplainer đã giải quyết triệt để rào cản 'hộp đen' của các mô hình Gradient Boosting phức tạp. Đề tài đã cung cấp góc nhìn toàn diện từ cấp độ toàn cục (Global Beeswarm/Bar Plots) đến cấp độ từng hồ sơ cá thể (Local Waterfall Plots), giúp chuyên viên thẩm định và nhà quản trị rủi ro nắm bắt chính xác lý do tại sao một khách hàng bị phân loại rủi ro cao, đáp ứng các tiêu chuẩn khắt khe về tính minh bạch và đạo đức AI trong lĩnh vực ngân hàng.", bold_prefix="Thứ tư, về khả năng giải thích và minh bạch hóa quyết định (Explainable AI): ")
    
    add_bullet_item(doc, "Đề tài đã hiện thực hóa mô hình nghiên cứu thành một sản phẩm ứng dụng Web DSS Prototype hoàn chỉnh dựa trên nền tảng Streamlit, phân tách kiến trúc hai tầng độc lập bảo đảm tính nhất quán Training-Serving. Hệ thống đã vượt qua 100% các bài kiểm thử tích hợp tự động (6/6 bài test PASS) với mã lỗi 0, minh chứng năng lực triển khai thực tế và tiềm năng ứng dụng cao trong môi trường vận hành.", bold_prefix="Thứ năm, về sản phẩm ứng dụng và khả năng triển khai thực nghiệm: ")
    
    add_heading2(doc, "2. Hạn chế của đề tài")
    add_body_para(doc, "Bên cạnh các thành tựu nổi bật, tác giả nghiêm túc nhận diện các giới hạn khách quan và học thuật của nghiên cứu:")
    
    add_bullet_item(doc, "Tập dữ liệu nghiên cứu UCI Credit Card phản ánh hành vi của khách hàng thẻ tín dụng tại Đài Loan trong giai đoạn tháng 4 đến tháng 9 năm 2005. Do hạn chế về khả năng tiếp cận dữ liệu bảo mật ngân hàng, đề tài chưa có điều kiện kiểm nghiệm chéo (external validation) trên tập dữ liệu khách hàng thực tế tại thị trường tín dụng Việt Nam đương đại.", bold_prefix="Hạn chế về tính tổng quát hóa của dữ liệu: ")
    
    add_bullet_item(doc, "Ngưỡng quyết định 0,60 được xác định dựa trên việc tối ưu điểm F1-Score trên các dự báo Out-Of-Fold của tập huấn luyện. Trong môi trường kinh doanh ngân hàng thực tế, ngưỡng này cần được tinh chỉnh dựa trên một ma trận chi phí tổn thất tài chính cụ thể (Cost Matrix), phản ánh chính xác chi phí trích lập dự phòng rủi ro và chi phí cơ hội của từng phân khúc tín dụng.", bold_prefix="Hạn chế về mô hình hóa chi phí nghiệp vụ: ")
    
    add_bullet_item(doc, "Ứng dụng Web hiện tại mới chỉ được thiết kế dưới dạng Prototype thử nghiệm phục vụ thẩm định hồ sơ đơn lẻ (single prediction). Hệ thống chưa hỗ trợ xử lý luồng dữ liệu lớn theo lô (batch scoring), chưa tích hợp cơ chế giám sát độ trôi dữ liệu (data drift / concept drift) và chưa có hệ thống phân quyền, bảo mật nhiều cấp.", bold_prefix="Hạn chế về quy mô hệ thống ứng dụng: ")
    
    add_bullet_item(doc, "Các phân tích từ SHAP Dependence Plots thể hiện mối liên hệ tương quan phi tuyến mà mô hình đã học được từ dữ liệu lịch sử, không mang bản chất quan hệ nhân quả tuyệt đối (causal relationship). Cần cẩn trọng khi diễn giải chính sách nghiệp vụ dựa trên các chỉ số này.", bold_prefix="Hạn chế về diễn giải thống kê: ")
    
    add_heading2(doc, "3. Hướng phát triển trong tương lai")
    add_body_para(doc, "Từ các hạn chế đã nhận diện, các hướng nghiên cứu và phát triển tiếp theo được đề xuất bao gồm:")
    
    add_bullet_item(doc, "Mở rộng thu thập và đánh giá mô hình trên các bộ dữ liệu tín dụng thực tế tại Việt Nam, bao gồm dữ liệu vay tiêu dùng cá nhân, vay mua nhà, vay mua ô tô và cho vay ngang hàng (P2P Lending) để kiểm chứng tính bền vững của các đặc trưng tài chính đề xuất.", bold_prefix="Mở rộng không gian dữ liệu thực nghiệm: ")
    
    add_bullet_item(doc, "Tích hợp các kỹ thuật học máy nhạy cảm chi phí (Cost-sensitive Learning) trực tiếp vào hàm mục tiêu của thuật toán XGBoost, kết hợp ước lượng Xác suất vỡ nợ (PD) với Tỷ lệ tổn thất khi vỡ nợ (LGD) và Dư nợ tại thời điểm vỡ nợ (EAD) theo chuẩn mực quốc tế Basel II/III.", bold_prefix="Nghiên cứu mô hình hóa nhạy cảm chi phí nâng cao: ")
    
    add_bullet_item(doc, "Nghiên cứu khai thác sâu hơn các giá trị tương tác SHAP (SHAP Interaction Values) để định lượng tác động kết hợp giữa các cặp biến rủi ro, ví dụ như sự tương tác giữa hạn mức tín dụng và số tháng chậm trả nợ.", bold_prefix="Ứng dụng kỹ thuật XAI nâng cao: ")
    
    add_bullet_item(doc, "Nâng cấp kiến trúc phần mềm sang mô hình Microservices, xây dựng API suy luận hiệu năng cao bằng FastAPI, kết nối hệ quản trị cơ sở dữ liệu quan hệ (PostgreSQL) và tích hợp các công cụ giám sát mô hình liên tục (MLOps) như MLflow hoặc Evidently AI.", bold_prefix="Hoàn thiện kiến trúc hệ thống phục vụ thực tế: ")

def add_references(doc):
    add_heading1(doc, "TÀI LIỆU THAM KHẢO")
    
    references = [
        "1. Ala'raj, S., & Abbod, M. F. (2016). A new consensus classification framework for credit scoring. Knowledge-Based Systems, 92, 83–95. https://doi.org/10.1016/j.knosys.2015.10.018",
        "2. Bussmann, N., Giudici, P., Marinelli, D., & Papenbrock, J. (2021). Explainable AI in credit risk management. Frontiers in Artificial Intelligence, 4, Article 670486. https://doi.org/10.3389/frai.2021.670486",
        "3. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (pp. 785–794). https://doi.org/10.1145/2939672.2939785",
        "4. Lê, V. T., & Nguyễn, H. N. (2020). Ứng dụng các thuật toán học máy trong dự báo rủi ro vỡ nợ của khách hàng cá nhân. Tạp chí Kinh tế và Phát triển, (278), 32–41.",
        "5. Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 4765–4774.",
        "6. Nguyễn, T. C. N., & Đinh, N. (2019). Xây dựng mô hình chấm điểm tín dụng cá nhân tại Ngân hàng Thương mại Cổ phần Ngoại thương Việt Nam. Tạp chí Khoa học & Đào tạo Ngân hàng, (204), 45–54.",
        "7. Phạm, L., & Nguyễn, T. H. Y. (2022). Đánh giá hiệu quả của các mô hình Học máy có giám sát trong chấm điểm tín dụng cá nhân. Tạp chí Nghiên cứu Kinh tế và Kinh doanh Châu Á (JABES), 33(4), 55–70.",
        "8. Shen, F., Zhao, X., Li, Z., Li, K., & Kou, G. (2019). A novel ensemble classification model based on neural networks and particle swarm optimization for credit scoring. Applied Soft Computing, 84, Article 105742. https://doi.org/10.1016/j.asoc.2019.105742",
        "9. Thomas, L. C., Edelman, D. B., & Thomas, W. H. (2002). Credit scoring and its applications. Society for Industrial and Applied Mathematics (SIAM). https://doi.org/10.1137/1.9780898718317",
        "10. Trần, T. T. T. (2021). Nghiên cứu ứng dụng thuật toán XGBoost và Random Forest trong đánh giá rủi ro tín dụng tại các ngân hàng thương mại Việt Nam. Tạp chí Ngân hàng, (15), 18–25.",
        "11. Tripathi, D., Edla, D. R., & Kupagal, V. (2020). Credit scoring model using hybrid feature selection and ensemble learning techniques. Computational Intelligence, 36(3), 1073–1094. https://doi.org/10.1111/coin.12288",
        "12. UCI Machine Learning Repository. (2016). Default of Credit Card Clients Dataset [Kaggle mirror]. https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset",
        "13. Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients. Expert Systems with Applications, 36(2), 2473–2480. https://doi.org/10.1016/j.eswa.2007.12.020"
    ]
    
    for ref in references:
        para = doc.add_paragraph()
        run = para.add_run(ref)
        set_font(run, size=12)
        pf = para.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.space_before = Pt(0)
        pf.space_after = Pt(4)
        pf.line_spacing = Pt(18)
        pf.left_indent = Cm(1.0)
        pf.first_line_indent = Cm(-1.0)  # hanging indent

def integrate_full_thesis():
    source_base_path = r"F:\DATN\docs\Bao_Cao_DATN_NguyenTrongThe.docx"
    print(f"Loading base document from: {source_base_path}")
    doc = Document(source_base_path)
    
    # 1. Find and clear old references at the end of Chapter 1
    # Paragraph 325 to end
    paras_to_remove = []
    found_ref = False
    for i, p in enumerate(doc.paragraphs):
        if "TÀI LIỆU THAM KHẢO" in p.text:
            found_ref = True
        if found_ref:
            paras_to_remove.append(p)
            
    print(f"Removing {len(paras_to_remove)} old reference paragraphs at end of Ch1...")
    for p in paras_to_remove:
        p_elem = p._p
        parent = p_elem.getparent()
        if parent is not None:
            parent.remove(p_elem)
            
    # 2. Find TOC section and replace with full TOC, List of Abbreviations, Tables, Figures
    toc_idx = None
    ch1_idx = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "MỤC LỤC" and toc_idx is None:
            toc_idx = i
        if p.style.name == "Heading 1" and "CHƯƠNG 1" in p.text and ch1_idx is None:
            ch1_idx = i
            break
            
    print(f"TOC index: {toc_idx}, Chapter 1 index: {ch1_idx}")
    
    if toc_idx is not None and ch1_idx is not None:
        ch1_para = doc.paragraphs[ch1_idx]
        between_paras = doc.paragraphs[toc_idx+1:ch1_idx]
        print(f"Removing {len(between_paras)} old front-matter paragraphs between TOC and Chapter 1...")
        for p in between_paras:
            p_elem = p._p
            parent = p_elem.getparent()
            if parent is not None:
                parent.remove(p_elem)
                
        def ins_para(text="", style=None):
            return ch1_para.insert_paragraph_before(text, style=style)
            
        # Add instruction under MỤC LỤC
        p_note = ins_para()
        r_note = p_note.add_run("(Nhấn Ctrl+A rồi nhấn F9 trong Microsoft Word để tự động cập nhật số trang và cấu trúc mục lục)")
        set_font(r_note, size=11, italic=True, color=(120, 120, 120))
        p_note.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_note.paragraph_format.space_before = Pt(0)
        p_note.paragraph_format.space_after = Pt(12)
        
        toc_items = [
            ("LỜI CẢM ƠN", "i", 1),
            ("LỜI CAM ĐOAN", "ii", 1),
            ("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", "iii", 1),
            ("NHẬN XÉT CỦA GIẢNG VIÊN PHẢN BIỆN", "iv", 1),
            ("MỤC LỤC", "v", 1),
            ("DANH MỤC TỪ VIẾT TẮT", "vi", 1),
            ("DANH MỤC BẢNG", "vii", 1),
            ("DANH MỤC HÌNH VẼ", "viii", 1),
            
            ("CHƯƠNG 1. TỔNG QUAN TÀI LIỆU VÀ CÁC CÔNG TRÌNH NGHIÊN CỨU LIÊN QUAN", "1", 1),
            ("1.1. Tổng quan về rủi ro tín dụng và bài toán chấm điểm tín dụng", "1", 2),
            ("1.1.1. Khái niệm rủi ro tín dụng (Credit Risk) và vỡ nợ (Default)", "1", 3),
            ("1.1.2. Vai trò của Chấm điểm tín dụng (Credit Scoring) trong quản trị rủi ro ngân hàng", "2", 3),
            ("1.1.3. Thách thức trong dự báo rủi ro tín dụng cá nhân", "3", 3),
            ("1.2. Tổng quan các công trình nghiên cứu liên quan trong và ngoài nước", "4", 2),
            ("1.2.1. Các công trình nghiên cứu nước ngoài", "4", 3),
            ("1.2.2. Các công trình nghiên cứu trong nước (Việt Nam)", "7", 3),
            ("1.2.3. Bảng so sánh và tổng hợp các công trình nghiên cứu", "9", 3),
            ("1.2.4. Nhận xét tổng quan, khoảng trống nghiên cứu và lý do chọn đề tài", "11", 3),
            ("1.3. Tổng quan về Machine Learning trong bài toán chấm điểm tín dụng", "12", 2),
            ("1.3.1. Bài toán Phân loại nhị phân (Binary Classification)", "12", 3),
            ("1.3.2. Mô hình Hồi quy Logistic (Logistic Regression - Baseline)", "13", 3),
            ("1.3.3. Mô hình Cây quyết định (Decision Tree Classifier)", "14", 3),
            ("1.3.4. Mô hình Rừng ngẫu nhiên (Random Forest Classifier)", "15", 3),
            ("1.3.5. Mô hình XGBoost (Extreme Gradient Boosting)", "16", 3),
            ("1.4. Tập dữ liệu nghiên cứu UCI Credit Card Clients", "17", 2),
            ("1.4.1. Nguồn gốc và ý nghĩa tập dữ liệu nghiên cứu", "17", 3),
            ("1.4.2. Mô tả chi tiết các biến dự báo và biến mục tiêu", "18", 3),
            ("1.5. Trí tuệ nhân tạo có thể giải thích (Explainable AI) và phương pháp SHAP", "19", 2),
            ("1.5.1. Khái niệm và sự cần thiết của Explainable AI trong lĩnh vực tài chính", "19", 3),
            ("1.5.2. Nguyên lý toán học Shapley Values và kỹ thuật SHAP (Global & Local Explanations)", "20", 3),
            
            ("CHƯƠNG 2. PHƯƠNG PHÁP THỰC HIỆN", "23", 1),
            ("2.1. Quy trình tổng thể xây dựng mô hình Machine Learning (ML Pipeline)", "23", 2),
            ("2.2. Kiểm duyệt dữ liệu và Phương pháp phân tích khám phá (Data Audit & EDA Methods)", "24", 2),
            ("2.2.1. Phương pháp kiểm duyệt chất lượng dữ liệu (Data Audit)", "24", 3),
            ("2.2.2. Phương pháp phân tích tương quan và trực quan hóa phân phối", "25", 3),
            ("2.3. Phương pháp Tiền xử lý dữ liệu và Quy tắc chống Data Leakage", "25", 2),
            ("2.3.1. Quy tắc phân chia tập Train/Test và kiểm soát rò rỉ dữ liệu", "25", 3),
            ("2.3.2. Phương pháp xử lý giá trị ngoại lệ và giá trị bất thường", "27", 3),
            ("2.3.3. Phương pháp chuẩn hóa (Scaling) và mã hóa đặc trưng duy nhất trên tập Train", "27", 3),
            ("2.4. Đề xuất Kỹ thuật trích rút đặc trưng (Feature Engineering Proposals)", "28", 2),
            ("2.4.1. Đề xuất các biến chỉ số tài chính", "28", 3),
            ("2.4.2. Phương pháp đánh giá thực nghiệm tính hiệu quả của các đặc trưng đề xuất", "29", 3),
            ("2.5. Các thuật toán Machine Learning đề xuất", "29", 2),
            ("2.5.1. Logistic Regression (Mô hình Cơ sở)", "29", 3),
            ("2.5.2. Decision Tree Classifier", "30", 3),
            ("2.5.3. Random Forest Classifier", "30", 3),
            ("2.5.4. XGBoost (Extreme Gradient Boosting)", "30", 3),
            ("2.6. Phương pháp thực nghiệm xử lý Mất cân bằng dữ liệu (Class Imbalance Methods)", "31", 2),
            ("2.6.1. Phân tích lý thuyết tác động của mất cân bằng dữ liệu", "31", 3),
            ("2.6.2. Đề xuất áp dụng Class Weighting, Threshold Tuning và cơ chế kiểm soát SMOTE", "31", 3),
            ("2.7. Phương pháp Đánh giá mô hình, Tối ưu hóa và Lựa chọn mô hình", "32", 2),
            ("2.7.1. Định nghĩa hệ thống chỉ số đánh giá đa chiều", "32", 3),
            ("2.7.2. Phương pháp phân tích Ma trận nhầm lẫn và đánh đổi nghiệp vụ", "33", 3),
            ("2.7.3. Phương pháp Cross-Validation và Tối ưu siêu tham số", "33", 3),
            ("2.7.4. Tiêu chí lựa chọn mô hình phù hợp nhất cho đề tài", "33", 3),
            ("2.8. Phương pháp giải thích mô hình với SHAP", "34", 2),
            ("2.8.1. Phương pháp phân tích đóng góp đặc trưng cấp tổng thể (Global Explanation)", "34", 3),
            ("2.8.2. Phương pháp phân tích đóng góp đặc trưng cấp cá thể (Local Explanation)", "34", 3),
            ("2.9. Phân tích Yêu cầu và Thiết kế Kiến trúc ứng dụng Web Prototype", "35", 2),
            ("2.9.1. Đặc tả yêu cầu chức năng, phi chức năng và luồng xử lý hệ thống", "35", 3),
            ("2.9.2. Thiết kế kiến trúc phần mềm DSS Prototype và nguyên tắc phân loại rủi ro thử nghiệm", "35", 3),
            
            ("CHƯƠNG 3. CÀI ĐẶT THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ", "36", 1),
            ("3.1. Môi trường phát triển và Thư viện cài đặt", "36", 2),
            ("3.1.1. Phần cứng và Hệ điều hành", "36", 3),
            ("3.1.2. Thư viện chính và phiên bản thực nghiệm", "36", 3),
            ("3.1.3. Cấu trúc mã nguồn và dữ liệu", "37", 3),
            ("3.2. Kết quả kiểm duyệt dữ liệu EDA và Cài đặt Tiền xử lý", "37", 2),
            ("3.2.1. Kết quả thực nghiệm kiểm duyệt chất lượng dữ liệu (Data Audit)", "37", 3),
            ("3.2.2. Kết quả thực nghiệm làm sạch dữ liệu và chuẩn hóa", "40", 3),
            ("3.2.3. Kết quả thực nghiệm Feature Engineering", "40", 3),
            ("3.3. Thực nghiệm Xây dựng mô hình cơ sở (Baseline) và So sánh mô hình", "42", 2),
            ("3.3.1. Kết quả huấn luyện mô hình cơ sở — Logistic Regression", "42", 3),
            ("3.3.2. Kết quả huấn luyện và so sánh các mô hình — Decision Tree, Random Forest, XGBoost", "44", 3),
            ("3.4. Thực nghiệm Xử lý mất cân bằng dữ liệu và Tối ưu siêu tham số", "46", 2),
            ("3.4.1. Kết quả so sánh hiệu năng Class Weighting và Threshold Tuning", "46", 3),
            ("3.4.2. Kết quả tối ưu siêu tham số (Hyperparameter Tuning)", "47", 3),
            ("3.5. Bảng tổng hợp Đánh giá mô hình và Lựa chọn mô hình phù hợp nhất", "48", 2),
            ("3.5.1. Bảng so sánh đa chỉ số — Toàn bộ 10 cấu hình mô hình", "48", 3),
            ("3.5.2. Phân tích chi tiết Ma trận nhầm lẫn, trade-off nghiệp vụ và quyết định chọn mô hình", "50", 3),
            ("3.6. Kết quả Thực nghiệm Giải thích mô hình bằng SHAP", "51", 2),
            ("3.6.1. Trực quan hóa kết quả đóng góp đặc trưng tổng thể (Global Feature Importance Plot)", "51", 3),
            ("3.6.2. Phân tích kết quả giải thích dự báo trường hợp khách hàng cụ thể (Local Waterfall Plot)", "53", 3),
            ("3.7. Cài đặt, Triển khai và Kiểm thử ứng dụng Web Prototype", "55", 2),
            ("3.7.1. Cài đặt giao diện người dùng và tích hợp mô hình ML đã chọn", "55", 3),
            ("3.7.2. Kịch bản chạy thử nghiệm dự báo và kiểm thử tích hợp (Integration Tests)", "56", 3),
            ("3.8. Đánh giá tổng quan kết quả thực nghiệm, Thảo luận và Hạn chế đề tài", "57", 2),
            ("3.8.1. Tổng kết các kết quả chính đạt được", "57", 3),
            ("3.8.2. Hạn chế của đề tài và định hướng phát triển thực tế", "58", 3),
            
            ("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "60", 1),
            ("1. Kết luận và tổng kết các kết quả nghiên cứu đạt được", "60", 2),
            ("2. Hạn chế của đề tài", "61", 2),
            ("3. Hướng phát triển trong tương lai", "62", 2),
            
            ("TÀI LIỆU THAM KHẢO", "63", 1)
        ]
        
        for t_title, p_num, lvl in toc_items:
            p_item = ins_para()
            pf_item = p_item.paragraph_format
            pf_item.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf_item.space_before = Pt(1)
            pf_item.space_after = Pt(2)
            pf_item.line_spacing = Pt(16)
            
            if lvl == 1:
                pf_item.left_indent = Cm(0)
                b = True
                sz = 12
            elif lvl == 2:
                pf_item.left_indent = Cm(0.8)
                b = False
                sz = 11.5
            else:
                pf_item.left_indent = Cm(1.6)
                b = False
                sz = 11
                
            r_t = p_item.add_run(t_title)
            set_font(r_t, size=sz, bold=b)
            r_tab = p_item.add_run("\t")
            set_font(r_tab, size=sz)
            r_p = p_item.add_run(p_num)
            set_font(r_p, size=sz, bold=b)
            
        # Page break before List of Abbreviations
        p_pb1 = ins_para()
        p_pb1.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)
        
        # Add DANH MỤC TỪ VIẾT TẮT
        p_abbr_t = ins_para()
        r_abbr_t = p_abbr_t.add_run("DANH MỤC TỪ VIẾT TẮT")
        set_font(r_abbr_t, size=14, bold=True)
        p_abbr_t.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_abbr_t.paragraph_format.space_before = Pt(12)
        p_abbr_t.paragraph_format.space_after = Pt(12)
        
        p_abbr_desc = ins_para()
        r_abbr_d = p_abbr_desc.add_run("Dưới đây là danh mục các thuật ngữ khoa học và từ viết tắt chuyên ngành được sử dụng trong đồ án tốt nghiệp:")
        set_font(r_abbr_d, size=13)
        p_abbr_desc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_abbr_desc.paragraph_format.space_before = Pt(0)
        p_abbr_desc.paragraph_format.space_after = Pt(6)
        p_abbr_desc.paragraph_format.line_spacing = Pt(19.5)
        
        # Create table normally using doc.add_table
        t_obj = doc.add_table(rows=1, cols=3)
        t_obj.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(t_obj)
        
        col_w = [Cm(2.5), Cm(6.5), Cm(7.0)]
        for i, h in enumerate(["Ký hiệu", "Thuật ngữ Tiếng Anh", "Ý nghĩa Tiếng Việt"]):
            c = t_obj.rows[0].cells[i]
            set_cell(c, h, bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
            c.width = col_w[i]
            
        abbr_data = [
            ("AI", "Artificial Intelligence", "Trí tuệ nhân tạo"),
            ("ANN", "Artificial Neural Network", "Mạng nơ-ron nhân tạo"),
            ("AUC", "Area Under Curve", "Diện tích dưới đường cong"),
            ("CV", "Cross-Validation", "Kiểm thực chéo"),
            ("DSS", "Decision Support System", "Hệ thống hỗ trợ ra quyết định"),
            ("DT", "Decision Tree", "Cây quyết định"),
            ("EAD", "Exposure at Default", "Dư nợ tại thời điểm vỡ nợ"),
            ("EDA", "Exploratory Data Analysis", "Phân tích khám phá dữ liệu"),
            ("FE", "Feature Engineering", "Kỹ thuật trích rút đặc trưng"),
            ("FN", "False Negative", "Bỏ sót rủi ro (Dương tính giả)"),
            ("FP", "False Positive", "Cảnh báo nhầm (Dương tính sai)"),
            ("IQR", "Interquartile Range", "Khoảng tứ phân vị (Q75 - Q25)"),
            ("LGD", "Loss Given Default", "Tổn thất khi vỡ nợ"),
            ("LR", "Logistic Regression", "Hồi quy Logistic"),
            ("ML", "Machine Learning", "Học máy"),
            ("OOF", "Out-Of-Fold", "Dự báo ngoài tập fold"),
            ("PD", "Probability of Default", "Xác suất vỡ nợ"),
            ("PR-AUC", "Precision-Recall AUC", "Diện tích dưới đường cong Precision-Recall"),
            ("RF", "Random Forest", "Rừng ngẫu nhiên"),
            ("SHAP", "SHapley Additive exPlanations", "Khung giải thích cộng tính Shapley")
        ]
        
        for d in abbr_data:
            r = t_obj.add_row()
            set_cell(r.cells[0], d[0], bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
            set_cell(r.cells[1], d[1], bold=False, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
            set_cell(r.cells[2], d[2], bold=False, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c_idx in range(3):
                r.cells[c_idx].width = col_w[c_idx]
                
        # Move table before ch1_para
        ch1_para._p.addprevious(t_obj._tbl)
        
        # Page break before List of Tables
        p_pb2 = ins_para()
        p_pb2.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)
        
        # DANH MỤC BẢNG
        p_tbl_t = ins_para()
        r_tbl_t = p_tbl_t.add_run("DANH MỤC BẢNG")
        set_font(r_tbl_t, size=14, bold=True)
        p_tbl_t.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_tbl_t.paragraph_format.space_before = Pt(12)
        p_tbl_t.paragraph_format.space_after = Pt(12)
        
        tables_list = [
            ("Bảng 1.1", "Tổng hợp các công trình nghiên cứu nước ngoài tiêu biểu", "11"),
            ("Bảng 1.2", "Tổng hợp các công trình nghiên cứu trong nước (Việt Nam)", "12"),
            ("Bảng 1.3", "Mô tả chi tiết các biến trong tập dữ liệu UCI Credit Card Clients", "20"),
            ("Bảng 2.1", "Các giai đoạn trong quy trình thực nghiệm Machine Learning Pipeline", "24"),
            ("Bảng 2.2", "Bộ tiêu chí kiểm soát rò rỉ dữ liệu (Data Leakage Audit)", "26"),
            ("Bảng 2.3", "Danh mục 10 đặc trưng tài chính tổng hợp được đề xuất trích xuất", "28"),
            ("Bảng 2.4", "Ma trận nhầm lẫn chuẩn trong phân loại rủi ro tín dụng nhị phân", "30"),
            ("Bảng 3.1", "Danh mục các thư viện khoa học dữ liệu và phiên bản thực nghiệm", "34"),
            ("Bảng 3.2", "Cấu trúc thư mục và các thành phần chính của repository dự án", "35"),
            ("Bảng 3.3", "Phân bố biến mục tiêu vỡ nợ (default.payment.next.month) trước xử lý", "36"),
            ("Bảng 3.4", "Thống kê mô tả và hệ số lệch (Skewness) các biến số học tiêu biểu", "37"),
            ("Bảng 3.5", "Kết quả phân chia tập dữ liệu Train / Test theo tỷ lệ 80/20 phân tầng", "38"),
            ("Bảng 3.6", "Kết quả kiểm định chất lượng ma trận đặc trưng sau Feature Engineering", "39"),
            ("Bảng 3.7", "Thống kê mô tả 10 đặc trưng tổng hợp mới trên tập huấn luyện (X_train)", "40"),
            ("Bảng 3.8", "Kết quả mô hình Logistic Regression trên tập kiểm tra Test", "41"),
            ("Bảng 3.9", "So sánh ma trận nhầm lẫn giữa LR Default và LR Balanced trên tập Test", "42"),
            ("Bảng 3.10", "Bảng so sánh hiệu năng 7 mô hình Baseline và Ensemble trên tập Test", "43"),
            ("Bảng 3.11", "Bộ siêu tham số tối ưu và điểm kiểm thực chéo (CV PR-AUC) của 3 mô hình Ensemble", "45"),
            ("Bảng 3.12", "So sánh hiệu năng mô hình XGBoost trên tập Test trước và sau khi tối ưu siêu tham số", "46"),
            ("Bảng 3.13", "Bảng tổng hợp đối sánh toàn bộ 10 cấu hình mô hình trên tập Test", "47"),
            ("Bảng 3.14", "So sánh 3 mô hình Ensemble Tuned theo các tiêu chí lựa chọn cốt lõi", "48"),
            ("Bảng 3.15", "Top 10 đặc trưng quan trọng nhất theo giá trị trung bình SHAP tuyệt đối (Mean |SHAP|)", "49"),
            ("Bảng 3.16", "Tóm tắt kết quả phân tích giải thích cá thể (Local Waterfall) cho 3 hồ sơ đại diện", "51"),
            ("Bảng 3.17", "Kết quả thực thi bộ kiểm thử tích hợp tự động hệ thống Web Prototype (6 bài test)", "53")
        ]
        for t_num, t_name, p_num in tables_list:
            p_i = ins_para()
            p_i.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_i.paragraph_format.space_before = Pt(1)
            p_i.paragraph_format.space_after = Pt(2)
            p_i.paragraph_format.line_spacing = Pt(16)
            p_i.paragraph_format.left_indent = Cm(0.8)
            r_n = p_i.add_run(f"{t_num}: {t_name}")
            set_font(r_n, size=11)
            r_tb = p_i.add_run("\t")
            set_font(r_tb, size=11)
            r_pn = p_i.add_run(p_num)
            set_font(r_pn, size=11)
            
        # Page break before List of Figures
        p_pb3 = ins_para()
        p_pb3.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)
        
        # DANH MỤC HÌNH VẼ
        p_fig_t = ins_para()
        r_fig_t = p_fig_t.add_run("DANH MỤC HÌNH VẼ")
        set_font(r_fig_t, size=14, bold=True)
        p_fig_t.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig_t.paragraph_format.space_before = Pt(12)
        p_fig_t.paragraph_format.space_after = Pt(12)
        
        figures_list = [
            ("Hình 3.1", "Biểu đồ phân bố biến mục tiêu thể hiện mức độ mất cân bằng lớp", "36"),
            ("Hình 3.2", "Phân bố đặc trưng nhân khẩu học theo giới tính, học vấn và hôn nhân", "37"),
            ("Hình 3.3", "Ma trận tương quan Pearson giữa các đặc trưng đầu vào và biến mục tiêu", "38"),
            ("Hình 3.4", "Đường cong ROC so sánh năng lực phân loại của 7 mô hình học máy", "43"),
            ("Hình 3.5", "Đường cong Precision-Recall so sánh hiệu năng trên lớp thiểu số của 7 mô hình", "44"),
            ("Hình 3.6", "Mức độ quan trọng đặc trưng trích xuất từ mô hình Random Forest", "47"),
            ("Hình 3.7", "Mức độ quan trọng đặc trưng trích xuất từ mô hình XGBoost Baseline", "48"),
            ("Hình 3.8", "Biểu đồ thanh SHAP Global Feature Importance theo độ lớn Mean |SHAP|", "50"),
            ("Hình 3.9", "Biểu đồ SHAP Beeswarm Plot thể hiện độ lớn và chiều hướng tác động của đặc trưng", "50"),
            ("Hình 3.10", "Biểu đồ phụ thuộc SHAP Dependence Plot của đặc trưng MAX_PAY_DELAY", "51"),
            ("Hình 3.11", "Biểu đồ phụ thuộc SHAP Dependence Plot của đặc trưng PAY_0", "51"),
            ("Hình 3.12", "Biểu đồ SHAP Waterfall giải thích hồ sơ Rủi ro cao (Index 3433, Prob = 96,16%)", "52"),
            ("Hình 3.13", "Biểu đồ SHAP Waterfall giải thích hồ sơ Rủi ro thấp (Index 1985, Prob = 2,84%)", "52"),
            ("Hình 3.14", "Biểu đồ SHAP Waterfall giải thích hồ sơ Biên giới ngưỡng (Index 1753, Prob = 60,01%)", "53")
        ]
        for f_num, f_name, p_num in figures_list:
            p_i = ins_para()
            p_i.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_i.paragraph_format.space_before = Pt(1)
            p_i.paragraph_format.space_after = Pt(2)
            p_i.paragraph_format.line_spacing = Pt(16)
            p_i.paragraph_format.left_indent = Cm(0.8)
            r_n = p_i.add_run(f"{f_num}: {f_name}")
            set_font(r_n, size=11)
            r_tb = p_i.add_run("\t")
            set_font(r_tb, size=11)
            r_pn = p_i.add_run(p_num)
            set_font(r_pn, size=11)
            
        # Page break before Chapter 1
        p_pb4 = ins_para()
        p_pb4.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)

    # 3. Chapter 1 is already in doc!
    print("Chapter 1 is retained intact.")
    
    # 4. Append Chapter 2
    print("Appending Chapter 2...")
    doc.add_page_break()
    add_chapter_2_content(doc)
    
    # 5. Append Chapter 3
    print("Appending Chapter 3...")
    doc.add_page_break()
    add_chapter_3_content(doc)
    
    # 6. Append Conclusion and Future Work
    print("Appending Conclusion and Future Work...")
    doc.add_page_break()
    add_conclusion_and_future_work(doc)
    
    # 7. Append References
    print("Appending References...")
    doc.add_page_break()
    add_references(doc)
    
    # 8. Save to destinations
    target1 = r"F:\DATN\project\docs\Bao_Cao_DATN_NguyenTrongThe_Full.docx"
    os.makedirs(os.path.dirname(target1), exist_ok=True)
    doc.save(target1)
    print(f"SUCCESS: Saved full thesis to {target1}")
    
    target2 = r"F:\DATN\docs\Bao_Cao_DATN_NguyenTrongThe_Full.docx"
    os.makedirs(os.path.dirname(target2), exist_ok=True)
    doc.save(target2)
    print(f"SUCCESS: Saved full thesis copy to {target2}")
    
    return target1, target2

if __name__ == "__main__":
    integrate_full_thesis()
