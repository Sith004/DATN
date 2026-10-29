# -*- coding: utf-8 -*-
"""
Export Chuong 3: CAI DAT THUC NGHIEM VA DANH GIA KET QUA sang Microsoft Word (.docx)
Do an tot nghiep: Nghien cuu xay dung mo hinh Machine Learning trong danh gia va du bao rui ro tin dung khach hang
Sinh vien: Nguyen Trong The - MSSV: 1150080117
GVHD: TS. Duong Thi Thuy Nga
"""

import sys, io, os
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_font(run, font_name='Times New Roman', size=13, bold=False, italic=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    r = run._r
    rPr = r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    existing = rPr.find(qn('w:rFonts'))
    if existing is not None:
        rPr.remove(existing)
    rPr.insert(0, rFonts)

def set_para_format(para, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                    space_before=0, space_after=6, line_spacing=1.5,
                    left_indent=0, first_line_indent=0):
    pf = para.paragraph_format
    pf.alignment = alignment
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = Pt(line_spacing * 13)
    if left_indent:
        pf.left_indent = Cm(left_indent)
    if first_line_indent:
        pf.first_line_indent = Cm(first_line_indent)

def setup_page(doc):
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.left_margin = Cm(3.0)   # Le trai 3cm
    section.right_margin = Cm(2.0)  # Le phai 2cm
    section.top_margin = Cm(2.5)    # Le tren 2.5cm
    section.bottom_margin = Cm(2.5) # Le duoi 2.5cm

def add_page_number(doc):
    section = doc.sections[0]
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.clear()
    run = footer_para.add_run()
    set_font(run, size=11)
    footer_para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)

def add_heading1(doc, text):
    para = doc.add_paragraph()
    try:
        para.style = doc.styles['Heading 1']
    except Exception:
        pass
    run = para.add_run(text)
    set_font(run, size=14, bold=True)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before = Pt(14)
    pf.space_after = Pt(12)
    pf.line_spacing = Pt(21)
    return para

def add_heading2(doc, text):
    para = doc.add_paragraph()
    try:
        para.style = doc.styles['Heading 2']
    except Exception:
        pass
    run = para.add_run(text)
    set_font(run, size=13, bold=True)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(12)
    pf.space_after = Pt(6)
    pf.line_spacing = Pt(19.5)
    return para

def add_heading3(doc, text):
    para = doc.add_paragraph()
    try:
        para.style = doc.styles['Heading 3']
    except Exception:
        pass
    run = para.add_run(text)
    set_font(run, size=13, bold=True)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(8)
    pf.space_after = Pt(4)
    pf.line_spacing = Pt(19.5)
    return para

def add_body_para(doc, text, indent=True, bold_prefix=None):
    para = doc.add_paragraph()
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)
    pf.line_spacing = Pt(19.5)
    if indent:
        pf.first_line_indent = Cm(1.27)
    
    if bold_prefix:
        run_b = para.add_run(bold_prefix)
        set_font(run_b, size=13, bold=True)
    
    run = para.add_run(text)
    set_font(run, size=13)
    return para

def add_bullet_item(doc, text, bold_prefix=None):
    para = doc.add_paragraph()
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.space_before = Pt(0)
    pf.space_after = Pt(4)
    pf.line_spacing = Pt(19.5)
    pf.left_indent = Cm(1.27)
    pf.first_line_indent = Cm(-0.63)
    
    bullet_run = para.add_run("• ")
    set_font(bullet_run, size=13, bold=True)
    
    if bold_prefix:
        b_run = para.add_run(bold_prefix)
        set_font(b_run, size=13, bold=True)
        
    run = para.add_run(text)
    set_font(run, size=13)
    return para

def add_table_caption(doc, text):
    para = doc.add_paragraph()
    run = para.add_run(text)
    set_font(run, size=12, bold=True)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before = Pt(10)
    pf.space_after = Pt(4)
    pf.line_spacing = Pt(18)
    return para

def add_figure(doc, img_rel_path, caption_text, width_cm=14.0):
    full_path = os.path.abspath(os.path.join(r"F:\DATN\project", img_rel_path))
    if not os.path.exists(full_path):
        print(f"WARNING: Image not found: {full_path}")
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(full_path, width=Cm(width_cm))
    
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(2)
    cap.paragraph_format.space_after = Pt(8)
    r_cap = cap.add_run(caption_text)
    set_font(r_cap, size=11, bold=False, italic=True)

def set_cell(cell, text, bold=False, size=11, align=WD_ALIGN_PARAGRAPH.LEFT, fill_color=None):
    cell.text = ''
    para = cell.paragraphs[0]
    run = para.add_run(text)
    set_font(run, size=size, bold=bold)
    para.paragraph_format.alignment = align
    para.paragraph_format.space_before = Pt(2)
    para.paragraph_format.space_after = Pt(2)
    para.paragraph_format.line_spacing = Pt(14)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    
    if fill_color:
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), fill_color)
        tcPr.append(shd)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '4')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), 'AAAAAA')
        tblBorders.append(border)
    tblPr.append(tblBorders)

def add_chapter_3_content(doc):
    add_heading1(doc, "CHƯƠNG 3. CÀI ĐẶT THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ")
    
    add_body_para(doc, "Chương 3 trình bày toàn bộ kết quả thực nghiệm thu được từ quá trình triển khai quy trình nghiên cứu đã thiết lập ở Chương 2. Tất cả số liệu, bảng biểu và đồ thị đều được tổng hợp trực tiếp từ các file kết quả thực nghiệm đã được chạy và lưu trữ trong repository dự án, bảo đảm tính minh bạch và có thể kiểm chứng. Các nội dung chính bao gồm: kết quả kiểm duyệt dữ liệu EDA và tiền xử lý, kết quả huấn luyện các mô hình phân loại cơ sở và nâng cao, phân tích tối ưu siêu tham số và xử lý mất cân bằng lớp, bảng tổng hợp đánh giá lựa chọn mô hình chính thức, kết quả giải thích mô hình bằng SHAP và kết quả triển khai, kiểm thử ứng dụng Web DSS Prototype.", indent=True)
    
    # 3.1
    add_heading2(doc, "3.1. Môi trường phát triển và Thư viện cài đặt")
    
    add_heading3(doc, "3.1.1. Phần cứng và Hệ điều hành")
    add_body_para(doc, "Toàn bộ các thực nghiệm và kiểm thử của đề tài được triển khai trong môi trường máy trạm với thông số cấu hình chuẩn:")
    add_bullet_item(doc, "Windows 11 Professional (64-bit architecture, AMD64).", bold_prefix="Hệ điều hành: ")
    add_bullet_item(doc, "Python phiên bản 3.14.4 được quản lý qua môi trường ảo độc lập (.venv).", bold_prefix="Ngôn ngữ lập trình: ")
    add_bullet_item(doc, "VS Code, Jupyter Notebook và PowerShell CLI hỗ trợ tự động hóa kiểm thử.", bold_prefix="Công cụ phát triển: ")
    
    add_heading3(doc, "3.1.2. Thư viện chính và phiên bản thực nghiệm")
    add_body_para(doc, "Hệ thống các thư viện mã nguồn mở chuyên sâu về khoa học dữ liệu và học máy được cài đặt chính xác trong môi trường ảo (.venv) như sau:")
    
    # Table 3.1: Environment libraries
    add_table_caption(doc, "Bảng 3.1: Danh mục các thư viện khoa học dữ liệu và phiên bản thực nghiệm")
    t_lib = doc.add_table(rows=8, cols=3)
    t_lib.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_lib)
    col_w_lib = [Cm(3.5), Cm(3.0), Cm(9.5)]
    for i, h in enumerate(["Thư viện", "Phiên bản", "Vai trò và chức năng trong đồ án"]):
        set_cell(t_lib.cell(0, i), h, bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_lib.cell(0, i).width = col_w_lib[i]
        
    lib_data = [
        ("Python", "3.14.4", "Nền tảng thực thi chính của toàn bộ pipeline thực nghiệm."),
        ("scikit-learn", "1.9.1", "Huấn luyện mô hình cơ sở, RandomizedSearchCV, StratifiedKFold, RobustScaler, tính toán Metrics."),
        ("xgboost", "3.4.1", "Xây dựng và tối ưu mô hình Extreme Gradient Boosting chính thức."),
        ("shap", "0.52.0", "Thuật toán TreeExplainer giải thích mô hình toàn cục và cá thể."),
        ("streamlit", "1.65.0", "Xây dựng ứng dụng giao diện Web DSS Prototype."),
        ("pandas", "3.0.5", "Xử lý, làm sạch và biến đổi dữ liệu bảng."),
        ("numpy", "2.5.3", "Tính toán đại số tuyến tính và xử lý mảng đa chiều.")
    ]
    for r_idx, d in enumerate(lib_data, start=1):
        set_cell(t_lib.cell(r_idx, 0), d[0], bold=True, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_lib.cell(r_idx, 1), d[1], bold=False, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_lib.cell(r_idx, 2), d[2], bold=False, size=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        for c in range(3):
            t_lib.cell(r_idx, c).width = col_w_lib[c]
            
    add_heading3(doc, "3.1.3. Cấu trúc mã nguồn và dữ liệu")
    add_body_para(doc, "Repository dự án được tổ chức khoa học theo mô hình module hóa phục vụ công tác tái lập:")
    
    # Table 3.2: Codebase structure
    add_table_caption(doc, "Bảng 3.2: Cấu trúc thư mục và các thành phần chính của repository dự án")
    t_code = doc.add_table(rows=7, cols=2)
    t_code.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_code)
    col_w_code = [Cm(5.0), Cm(11.0)]
    for i, h in enumerate(["Thư mục / Tệp tin", "Mô tả nội dung và vai trò kỹ thuật"]):
        set_cell(t_code.cell(0, i), h, bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_code.cell(0, i).width = col_w_code[i]
        
    code_data = [
        ("data/raw/UCI_Credit_Card.csv", "Tập dữ liệu thô gốc gồm 30.000 bản ghi khách hàng thẻ tín dụng."),
        ("data/processed/", "Lưu trữ tập X_train_fe (23.972x33), X_test_fe (5.993x33), y_train, y_test sau FE."),
        ("models/final_candidate_model.pkl", "Mô hình XGBoost Tuned đã huấn luyện sẵn kèm tham số tối ưu."),
        ("models/robust_scaler.pkl", "Bộ chuẩn hóa RobustScaler đã fit duy nhất trên tập Train."),
        ("src/ & app.py", "Mã nguồn module suy luận prediction.py, feature_engineering.py và giao diện Web Streamlit."),
        ("reports/ & reports/figures/", "Báo cáo kỹ thuật chi tiết từng tuần và 42 đồ thị thực nghiệm gốc.")
    ]
    for r_idx, d in enumerate(code_data, start=1):
        set_cell(t_code.cell(r_idx, 0), d[0], bold=True, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_code.cell(r_idx, 1), d[1], bold=False, size=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        for c in range(2):
            t_code.cell(r_idx, c).width = col_w_code[c]
            
    # 3.2
    add_heading2(doc, "3.2. Kết quả kiểm duyệt dữ liệu EDA và Cài đặt Tiền xử lý")
    
    add_heading3(doc, "3.2.1. Kết quả thực nghiệm kiểm duyệt chất lượng dữ liệu (Data Audit)")
    add_body_para(doc, "Quá trình kiểm duyệt dữ liệu ban đầu trên 30.000 quan sát của tập UCI Credit Card ghi nhận các phát hiện then chốt sau:")
    add_bullet_item(doc, "Dữ liệu không có ô khuyết (0 missing values trên toàn bộ 25 cột).", bold_prefix="Tính toàn vẹn: ")
    add_bullet_item(doc, "Không có dòng trùng lặp 100% kể cả ID, nhưng phát hiện chính xác 35 nhóm trùng lặp đặc trưng hành vi (70 dòng).", bold_prefix="Dòng trùng lặp: ")
    add_bullet_item(doc, "Cột EDUCATION có 345 mẫu (1,15%) mang mã chưa chuẩn {0, 5, 6}; cột MARRIAGE có 54 mẫu (0,18%) mang mã {0}.", bold_prefix="Mã danh mục bất thường: ")
    
    # Table 3.3: Target distribution
    add_table_caption(doc, "Bảng 3.3: Phân bố biến mục tiêu vỡ nợ (default.payment.next.month) trước xử lý")
    t_target = doc.add_table(rows=4, cols=4)
    t_target.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_target)
    col_w_target = [Cm(2.5), Cm(6.5), Cm(3.5), Cm(3.5)]
    for i, h in enumerate(["Giá trị", "Ý nghĩa phân loại", "Số lượng quan sát", "Tỷ lệ (%)"]):
        set_cell(t_target.cell(0, i), h, bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_target.cell(0, i).width = col_w_target[i]
        
    target_data = [
        ("0", "Không vỡ nợ (Non-Default)", "23.364", "77,88%"),
        ("1", "Vỡ nợ (Default)", "6.636", "22,12%"),
        ("Tổng cộng", "Toàn bộ tập dữ liệu ban đầu", "30.000", "100,00%")
    ]
    for r_idx, d in enumerate(target_data, start=1):
        bold_flag = (r_idx == 3)
        set_cell(t_target.cell(r_idx, 0), d[0], bold=bold_flag, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_target.cell(r_idx, 1), d[1], bold=bold_flag, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_target.cell(r_idx, 2), d[2], bold=bold_flag, size=10, align=WD_ALIGN_PARAGRAPH.RIGHT)
        set_cell(t_target.cell(r_idx, 3), d[3], bold=bold_flag, size=10, align=WD_ALIGN_PARAGRAPH.RIGHT)
        for c in range(4):
            t_target.cell(r_idx, c).width = col_w_target[c]
            
    add_figure(doc, "reports/figures/target_distribution.png", "Hình 3.1: Biểu đồ phân bố biến mục tiêu thể hiện mức độ mất cân bằng lớp (Nguồn: reports/figures/target_distribution.png)", width_cm=14.0)
    
    add_body_para(doc, "Bảng 3.4 trình bày các chỉ số thống kê mô tả tiêu biểu. Đáng chú ý, các biến thanh toán PAY_AMT1 và PAY_AMT2 có hệ số Skewness lần lượt là 14,67 và 30,45. Đây là bằng chứng thực nghiệm rõ ràng nhất khẳng định sự cần thiết phải sử dụng phương pháp chuẩn hóa RobustScaler thay vì StandardScaler.", indent=True)
    
    # Table 3.4: Descriptive stats
    add_table_caption(doc, "Bảng 3.4: Thống kê mô tả và hệ số lệch (Skewness) các biến số học tiêu biểu")
    t_desc = doc.add_table(rows=6, cols=7)
    t_desc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_desc)
    col_w_desc = [Cm(3.0), Cm(2.2), Cm(2.2), Cm(2.2), Cm(2.2), Cm(2.5), Cm(2.2)]
    desc_heads = ["Tên biến", "Trung bình", "Độ lệch chuẩn", "Nhỏ nhất", "Trung vị", "Lớn nhất", "Skewness"]
    for i, h in enumerate(desc_heads):
        set_cell(t_desc.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_desc.cell(0, i).width = col_w_desc[i]
        
    desc_data = [
        ("LIMIT_BAL", "167.484", "129.748", "10.000", "140.000", "1.000.000", "0,99"),
        ("AGE", "35,49", "9,22", "21", "34", "79", "0,73"),
        ("BILL_AMT1", "51.223", "73.636", "-165.580", "22.382", "964.511", "2,66"),
        ("PAY_AMT1", "5.664", "16.563", "0", "2.100", "873.552", "14,67"),
        ("PAY_AMT2", "5.921", "23.041", "0", "2.009", "1.684.259", "30,45")
    ]
    for r_idx, d in enumerate(desc_data, start=1):
        set_cell(t_desc.cell(r_idx, 0), d[0], bold=True, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        for c in range(1, 7):
            set_cell(t_desc.cell(r_idx, c), d[c], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.RIGHT)
            t_desc.cell(r_idx, c).width = col_w_desc[c]
        t_desc.cell(r_idx, 0).width = col_w_desc[0]
        
    add_figure(doc, "reports/figures/demographic_distribution.png", "Hình 3.2: Phân bố đặc trưng nhân khẩu học theo giới tính, học vấn và hôn nhân (Nguồn: reports/figures/demographic_distribution.png)", width_cm=15.0)
    
    add_figure(doc, "reports/figures/correlation_heatmap.png", "Hình 3.3: Ma trận tương quan Pearson giữa các đặc trưng đầu vào và biến mục tiêu (Nguồn: reports/figures/correlation_heatmap.png)", width_cm=15.0)
    
    add_heading3(doc, "3.2.2. Kết quả thực nghiệm làm sạch dữ liệu và chuẩn hóa")
    add_body_para(doc, "Sau khi loại bỏ 35 dòng trùng lặp dư thừa và gom nhóm chuẩn hóa các mã danh mục, tập dữ liệu đạt quy mô 29.965 quan sát. Việc phân chia Train/Test được thực hiện phân tầng nghiêm ngặt:")
    
    # Table 3.5: Split result
    add_table_caption(doc, "Bảng 3.5: Kết quả phân chia tập dữ liệu Train / Test theo tỷ lệ 80/20 phân tầng")
    t_split = doc.add_table(rows=4, cols=6)
    t_split.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_split)
    col_w_split = [Cm(2.5), Cm(2.8), Cm(2.2), Cm(3.0), Cm(2.8), Cm(2.7)]
    split_heads = ["Tập dữ liệu", "Số quan sát", "Tỷ lệ (%)", "Non-Default (0)", "Default (1)", "Tỷ lệ Default"]
    for i, h in enumerate(split_heads):
        set_cell(t_split.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_split.cell(0, i).width = col_w_split[i]
        
    split_data = [
        ("Tập Huấn luyện (Train)", "23.972", "80,00%", "18.668", "5.304", "22,13%"),
        ("Tập Kiểm tra (Test)", "5.993", "20,00%", "4.667", "1.326", "22,12%"),
        ("Toàn bộ (Cleaned)", "29.965", "100,00%", "23.335", "6.630", "22,13%")
    ]
    for r_idx, d in enumerate(split_data, start=1):
        bold_flag = (r_idx == 3)
        set_cell(t_split.cell(r_idx, 0), d[0], bold=bold_flag, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_split.cell(r_idx, 1), d[1], bold=bold_flag, size=10, align=WD_ALIGN_PARAGRAPH.RIGHT)
        set_cell(t_split.cell(r_idx, 2), d[2], bold=bold_flag, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_split.cell(r_idx, 3), d[3], bold=bold_flag, size=10, align=WD_ALIGN_PARAGRAPH.RIGHT)
        set_cell(t_split.cell(r_idx, 4), d[4], bold=bold_flag, size=10, align=WD_ALIGN_PARAGRAPH.RIGHT)
        set_cell(t_split.cell(r_idx, 5), d[5], bold=bold_flag, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
        for c in range(6):
            t_split.cell(r_idx, c).width = col_w_split[c]
            
    add_body_para(doc, "Đánh giá rò rỉ dữ liệu: Kết quả kiểm tra bộ 7 tiêu chí xác nhận 7/7 tiêu chí đều đạt chuẩn PASS. RobustScaler được fit duy nhất trên X_train (học Median và IQR), sau đó áp dụng biến đổi transform độc lập trên X_test.", indent=True)
    
    add_heading3(doc, "3.2.3. Kết quả thực nghiệm Feature Engineering")
    add_body_para(doc, "Sau khi áp dụng module trích xuất đặc trưng (src/feature_engineering.py), 10 biến tài chính mới được tính toán thành công. Bảng 3.6 và 3.7 xác nhận các kiểm định chất lượng ma trận đặc trưng.")
    
    # Table 3.6: FE quality check
    add_table_caption(doc, "Bảng 3.6: Kết quả kiểm định chất lượng ma trận đặc trưng sau Feature Engineering")
    t_fe_chk = doc.add_table(rows=8, cols=4)
    t_fe_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_fe_chk)
    col_w_fe_chk = [Cm(6.0), Cm(3.5), Cm(3.5), Cm(3.0)]
    for i, h in enumerate(["Chỉ số kiểm tra kỹ thuật", "Tập Train (X_train_fe)", "Tập Test (X_test_fe)", "Kết luận"]):
        set_cell(t_fe_chk.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_fe_chk.cell(0, i).width = col_w_fe_chk[i]
        
    fe_chk_data = [
        ("Số dòng (quan sát)", "23.972", "5.993", "ĐẠT (PASS)"),
        ("Số cột đặc trưng (features)", "33", "33", "ĐẠT (PASS)"),
        ("Số ô khuyết (Missing NaN)", "0 (0,00%)", "0 (0,00%)", "ĐẠT (PASS)"),
        ("Số giá trị vô cực (Infinity)", "0 (0,00%)", "0 (0,00%)", "ĐẠT (PASS)"),
        ("Sự hiện diện của cột nhãn mục tiêu", "Không có (0)", "Không có (0)", "ĐẠT (PASS)"),
        ("Sự hiện diện của cột định danh ID", "Không có (0)", "Không có (0)", "ĐẠT (PASS)"),
        ("Kiểm soát Data Leakage (Fit Scaler)", "Fit duy nhất", "Chỉ Transform", "ĐẠT (PASS)")
    ]
    for r_idx, d in enumerate(fe_chk_data, start=1):
        set_cell(t_fe_chk.cell(r_idx, 0), d[0], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_fe_chk.cell(r_idx, 1), d[1], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_fe_chk.cell(r_idx, 2), d[2], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_fe_chk.cell(r_idx, 3), d[3], bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        for c in range(4):
            t_fe_chk.cell(r_idx, c).width = col_w_fe_chk[c]
            
    # Table 3.7: 10 FE stats
    add_table_caption(doc, "Bảng 3.7: Thống kê mô tả 10 đặc trưng tổng hợp mới trên tập huấn luyện (X_train)")
    t_fe_stats = doc.add_table(rows=11, cols=6)
    t_fe_stats.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_fe_stats)
    col_w_fe_stats = [Cm(4.5), Cm(2.3), Cm(2.3), Cm(2.3), Cm(2.3), Cm(2.3)]
    fe_stats_heads = ["Tên biến tổng hợp mới", "Mean", "Median", "Min", "Max", "Skewness"]
    for i, h in enumerate(fe_stats_heads):
        set_cell(t_fe_stats.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_fe_stats.cell(0, i).width = col_w_fe_stats[i]
        
    fe_stats_data = [
        ("UTILIZATION_RATE_SEPT", "0,4243", "0,3134", "-0,6156", "6,4553", "1,02"),
        ("MEAN_BILL_AMT", "44.982", "21.114", "-56.043", "893.021", "2,75"),
        ("UTILIZATION_RATE_MEAN", "0,3746", "0,2851", "-0,2723", "5,3644", "1,15"),
        ("PAY_RATIO_SEPT", "0,8841", "1,0000", "0,0000", "1,0000", "-1,45"),
        ("PAY_RATIO_MEAN", "0,8624", "0,9854", "0,0000", "1,0000", "-1,68"),
        ("MAX_PAY_DELAY", "0,6832", "0,0000", "-2,0000", "8,0000", "1,62"),
        ("COUNT_LATE_PAYMENT", "0,8041", "0,0000", "0,0000", "6,0000", "1,95"),
        ("MEAN_PAY_AMT", "5.275", "2.399", "0", "321.200", "6,84"),
        ("BILL_TREND", "0,0784", "0,0021", "-3,2104", "4,8512", "1,48"),
        ("PAY_TREND", "0,0028", "0,0000", "-3,5100", "4,1200", "0,85")
    ]
    for r_idx, d in enumerate(fe_stats_data, start=1):
        set_cell(t_fe_stats.cell(r_idx, 0), d[0], bold=True, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        for c in range(1, 6):
            set_cell(t_fe_stats.cell(r_idx, c), d[c], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.RIGHT)
            t_fe_stats.cell(r_idx, c).width = col_w_fe_stats[c]
        t_fe_stats.cell(r_idx, 0).width = col_w_fe_stats[0]
        
    # 3.3
    add_heading2(doc, "3.3. Thực nghiệm Xây dựng mô hình cơ sở (Baseline) và So sánh mô hình")
    
    add_heading3(doc, "3.3.1. Kết quả huấn luyện mô hình cơ sở — Logistic Regression")
    add_body_para(doc, "Mô hình hồi quy Logistic được đánh giá trên tập kiểm tra độc lập (5.993 mẫu) dưới hai cấu hình trọng số:")
    
    # Table 3.8: LR results
    add_table_caption(doc, "Bảng 3.8: Kết quả mô hình Logistic Regression trên tập kiểm tra Test")
    t_lr = doc.add_table(rows=3, cols=7)
    t_lr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_lr)
    col_w_lr = [Cm(3.5), Cm(2.1), Cm(2.1), Cm(2.1), Cm(2.1), Cm(2.1), Cm(2.0)]
    for i, h in enumerate(["Cấu hình mô hình", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC", "PR-AUC"]):
        set_cell(t_lr.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_lr.cell(0, i).width = col_w_lr[i]
        
    lr_data = [
        ("LR Default", "0,8106", "0,6610", "0,2956", "0,4085", "0,7492", "0,5162"),
        ("LR Balanced", "0,7469", "0,4466", "0,6018", "0,5127", "0,7514", "0,5123")
    ]
    for r_idx, d in enumerate(lr_data, start=1):
        set_cell(t_lr.cell(r_idx, 0), d[0], bold=True, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        for c in range(1, 7):
            set_cell(t_lr.cell(r_idx, c), d[c], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.RIGHT)
            t_lr.cell(r_idx, c).width = col_w_lr[c]
        t_lr.cell(r_idx, 0).width = col_w_lr[0]
        
    # Table 3.9: LR Confusion matrix
    add_table_caption(doc, "Bảng 3.9: So sánh ma trận nhầm lẫn giữa LR Default và LR Balanced trên tập Test")
    t_lr_cm = doc.add_table(rows=3, cols=3)
    t_lr_cm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_lr_cm)
    col_w_cm2 = [Cm(4.5), Cm(5.5), Cm(5.5)]
    set_cell(t_lr_cm.cell(0, 0), "Chỉ số ma trận nhầm lẫn", bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
    set_cell(t_lr_cm.cell(0, 1), "LR Default (Không trọng số)", bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
    set_cell(t_lr_cm.cell(0, 2), "LR Balanced (class_weight='balanced')", bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
    
    set_cell(t_lr_cm.cell(1, 0), "True Positive (Bắt đúng vỡ nợ) / FN", bold=False, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_cell(t_lr_cm.cell(1, 1), "TP = 392  |  FN = 934 (Bỏ sót nhiều)", bold=False, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell(t_lr_cm.cell(1, 2), "TP = 798 (+103%)  |  FN = 528 (Giảm 43%)", bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    
    set_cell(t_lr_cm.cell(2, 0), "True Negative / FP (Báo nhầm)", bold=False, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_cell(t_lr_cm.cell(2, 1), "TN = 4.466  |  FP = 201 (Báo nhầm ít)", bold=False, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell(t_lr_cm.cell(2, 2), "TN = 3.678  |  FP = 989 (Báo nhầm tăng)", bold=False, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    for r in range(3):
        for c in range(3):
            t_lr_cm.cell(r, c).width = col_w_cm2[c]
            
    add_body_para(doc, "Phân tích thực nghiệm: Áp dụng class_weight='balanced' đã nâng tỷ lệ phát hiện khách hàng vỡ nợ (Recall) từ 29,56% lên 60,18% (tăng hơn gấp đôi), giảm số lượng hồ sơ bỏ sót nguy hiểm từ 934 xuống 528 hồ sơ. Đánh đổi lại, số lượng cảnh báo nhầm tăng từ 201 lên 989 hồ sơ, làm giảm Precision từ 66,10% xuống 44,66%. Đáng chú ý, chỉ số PR-AUC giữa hai cấu hình gần như tương đương (~0,51), phản ánh giới hạn phân tách của ranh giới quyết định tuyến tính.", indent=True)
    
    add_heading3(doc, "3.3.2. Kết quả huấn luyện và so sánh các mô hình — Decision Tree, Random Forest, XGBoost")
    add_body_para(doc, "Bảng 3.10 tổng hợp hiệu năng của toàn bộ 7 mô hình Baseline và Ensemble trên tập kiểm tra Test (trước khi tối ưu siêu tham số):")
    
    # Table 3.10: 7 models comparison
    add_table_caption(doc, "Bảng 3.10: Bảng so sánh hiệu năng 7 mô hình Baseline và Ensemble trên tập Test (5.993 mẫu)")
    t_7m = doc.add_table(rows=8, cols=7)
    t_7m.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_7m)
    for i, h in enumerate(["Mô hình thuật toán", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC", "PR-AUC"]):
        set_cell(t_7m.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_7m.cell(0, i).width = col_w_lr[i]
        
    data_7m = [
        ("Logistic Regression (Default)", "0,8106", "0,6610", "0,2956", "0,4085", "0,7492", "0,5162"),
        ("Logistic Regression (Balanced)", "0,7469", "0,4466", "0,6018", "0,5127", "0,7514", "0,5123"),
        ("Decision Tree (Default)", "0,7267", "0,3884", "0,4095", "0,3987", "0,6130", "0,2897"),
        ("Decision Tree (Balanced)", "0,7262", "0,3784", "0,3695", "0,3739", "0,5986", "0,2796"),
        ("Random Forest (Default)", "0,8143", "0,6364", "0,3748", "0,4718", "0,7659", "0,5381"),
        ("Random Forest (Balanced)", "0,7973", "0,5471", "0,4864", "0,5150", "0,7661", "0,5297"),
        ("XGBoost Baseline", "0,8201", "0,6766", "0,3582", "0,4684", "0,7792", "0,5611")
    ]
    for r_idx, d in enumerate(data_7m, start=1):
        bold_row = (r_idx == 7)
        set_cell(t_7m.cell(r_idx, 0), d[0], bold=bold_row, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        for c in range(1, 7):
            set_cell(t_7m.cell(r_idx, c), d[c], bold=bold_row, size=9, align=WD_ALIGN_PARAGRAPH.RIGHT)
            t_7m.cell(r_idx, c).width = col_w_lr[c]
        t_7m.cell(r_idx, 0).width = col_w_lr[0]
        
    add_figure(doc, "reports/figures/week7_roc_curve_comparison.png", "Hình 3.4: Đường cong ROC so sánh năng lực phân loại của 7 mô hình học máy (Nguồn: reports/figures/week7_roc_curve_comparison.png)", width_cm=14.0)
    
    add_figure(doc, "reports/figures/week7_pr_curve_comparison.png", "Hình 3.5: Đường cong Precision-Recall so sánh hiệu năng trên lớp thiểu số của 7 mô hình (Nguồn: reports/figures/week7_pr_curve_comparison.png)", width_cm=14.0)
    
    add_body_para(doc, "Nhận xét thực nghiệm chính:")
    add_bullet_item(doc, "Decision Tree đơn lẻ ghi nhận PR-AUC rất thấp (0,2897 và 0,2796), chứng minh cây quyết định không đủ năng lực tổng quát hóa trên dữ liệu tài chính nhiều chiều và mất cân bằng.", bold_prefix="Hạn chế của cây đơn: ")
    add_bullet_item(doc, "Random Forest cải thiện vượt bậc nhờ cơ chế đóng bao, nâng PR-AUC lên 0,5381 (tăng +85% so với Decision Tree).", bold_prefix="Hiệu quả của Bagging: ")
    add_bullet_item(doc, "XGBoost Baseline đạt đỉnh PR-AUC cao nhất (0,5611) và ROC-AUC cao nhất (0,7792) ngay ở cấu hình mặc định, khẳng định ưu thế vượt trội của thuật toán Gradient Boosting đối với dữ liệu dạng bảng.", bold_prefix="Ưu thế của Gradient Boosting: ")
    
    # 3.4
    add_heading2(doc, "3.4. Thực nghiệm Xử lý mất cân bằng dữ liệu và Tối ưu siêu tham số")
    
    add_heading3(doc, "3.4.1. Kết quả so sánh hiệu năng Class Weighting và Threshold Tuning")
    add_body_para(doc, "Thực nghiệm kiểm chứng xác nhận rằng trong các mô hình Ensemble phức tạp, việc áp dụng Class Weighting làm dịch chuyển ranh giới quyết định giúp tăng Recall nhưng lại làm giảm Precision. Để tối ưu hóa điểm hoạt động mà không làm biến dạng hàm mất mát, kỹ thuật phân tích ngưỡng (Threshold Tuning) được thực hiện trên các dự báo Out-Of-Fold (OOF) trong Cross-Validation 5-fold trên tập Train:")
    add_bullet_item(doc, "Ngưỡng tối ưu OOF F1 đạt 0,30.", bold_prefix="Random Forest Default Tuned: ")
    add_bullet_item(doc, "Ngưỡng tối ưu OOF F1 đạt 0,55.", bold_prefix="Random Forest Balanced Tuned: ")
    add_bullet_item(doc, "Ngưỡng tối ưu OOF F1 đạt chính xác 0,60.", bold_prefix="XGBoost Tuned: ")
    add_body_para(doc, "Về kỹ thuật SMOTE: Do môi trường thực nghiệm độc lập của dự án không tích hợp sẵn thư viện imbalanced-learn, phương pháp tạo mẫu tổng hợp SMOTE không được đưa vào thực nghiệm chính thức. Thực tế chứng minh Class Weighting kết hợp Threshold Tuning đã mang lại kết quả phát hiện rủi ro vượt trội mà hoàn toàn bảo đảm nguyên tắc không gây rò rỉ phân phối mẫu.", indent=True)
    
    add_heading3(doc, "3.4.2. Kết quả tối ưu siêu tham số (Hyperparameter Tuning)")
    add_body_para(doc, "Thuật toán RandomizedSearchCV với 25 vòng lặp kết hợp StratifiedKFold(5) theo tiêu chí tối ưu PR-AUC đã xác định được bộ tham số tối ưu:")
    
    # Table 3.11: Tuned hyperparameters
    add_table_caption(doc, "Bảng 3.11: Bộ siêu tham số tối ưu và điểm kiểm thực chéo (CV PR-AUC) của 3 mô hình Ensemble")
    t_tune = doc.add_table(rows=4, cols=3)
    t_tune.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_tune)
    col_w_tune = [Cm(4.5), Cm(3.2), Cm(8.3)]
    for i, h in enumerate(["Mô hình tối ưu", "Điểm CV PR-AUC", "Bộ siêu tham số tối ưu được lựa chọn"]):
        set_cell(t_tune.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_tune.cell(0, i).width = col_w_tune[i]
        
    tune_data = [
        ("RF Default Tuned", "0,5656 ± 0,0088", "n_estimators=250, max_depth=10, max_features=0.5, min_samples_split=5"),
        ("RF Balanced Tuned", "0,5627 ± 0,0096", "n_estimators=250, max_depth=10, max_features=0.5, class_weight='balanced'"),
        ("XGBoost Tuned", "0,5646 ± 0,0122", "n_estimators=250, learning_rate=0.03, max_depth=6, subsample=0.6, colsample_bytree=0.9, gamma=0.3, reg_alpha=0.5, reg_lambda=1.0")
    ]
    for r_idx, d in enumerate(tune_data, start=1):
        bold_r = (r_idx == 3)
        set_cell(t_tune.cell(r_idx, 0), d[0], bold=bold_r, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_tune.cell(r_idx, 1), d[1], bold=bold_r, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_tune.cell(r_idx, 2), d[2], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        for c in range(3):
            t_tune.cell(r_idx, c).width = col_w_tune[c]
            
    # Table 3.12: XGBoost before/after tuning
    add_table_caption(doc, "Bảng 3.12: So sánh hiệu năng mô hình XGBoost trên tập Test trước và sau khi tối ưu siêu tham số")
    t_xgb = doc.add_table(rows=7, cols=4)
    t_xgb.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_xgb)
    col_w_xgb = [Cm(4.5), Cm(3.8), Cm(3.8), Cm(3.9)]
    for i, h in enumerate(["Chỉ số đánh giá", "Trước Tuning (Mặc định)", "Sau Tuning (Threshold 0,60)", "Mức độ thay đổi"]):
        set_cell(t_xgb.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_xgb.cell(0, i).width = col_w_xgb[i]
        
    xgb_diff_data = [
        ("Độ chính xác (Accuracy)", "0,8201", "0,7686", "-0,0515 (-5,15%)"),
        ("Độ chuẩn xác (Precision)", "0,6766", "0,4820", "-0,1946 (-19,46%)"),
        ("Độ nhạy phát hiện vỡ nợ (Recall)", "0,3582", "0,6161", "+0,2579 (+25,79%) ★"),
        ("Điểm F1 tổng hợp (F1-Score)", "0,4684", "0,5409", "+0,0725 (+7,25%)"),
        ("Diện tích dưới ROC (ROC-AUC)", "0,7792", "0,7769", "-0,0023 (-0,23%)"),
        ("Diện tích dưới PR (PR-AUC)", "0,5611", "0,5620", "+0,0009 (+0,09%) ★")
    ]
    for r_idx, d in enumerate(xgb_diff_data, start=1):
        bold_r = ("★" in d[3])
        set_cell(t_xgb.cell(r_idx, 0), d[0], bold=bold_r, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_xgb.cell(r_idx, 1), d[1], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.RIGHT)
        set_cell(t_xgb.cell(r_idx, 2), d[2], bold=bold_r, size=9, align=WD_ALIGN_PARAGRAPH.RIGHT)
        set_cell(t_xgb.cell(r_idx, 3), d[3], bold=bold_r, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        for c in range(4):
            t_xgb.cell(r_idx, c).width = col_w_xgb[c]
            
    add_body_para(doc, "Phân tích nghiệp vụ sâu sắc: Kết quả Bảng 3.12 phản ánh rõ ràng sự đánh đổi nghiệp vụ có chủ đích. Để đạt mục tiêu giảm thiểu tổn thất tín dụng, mô hình chấp nhận hy sinh 5,15% Accuracy và 19,46% Precision để đổi lấy sự bứt phá vượt bậc về Recall (+25,79 điểm phần trăm). Mô hình sau khi tối ưu phát hiện được 61,61% tổng số khách hàng vỡ nợ thực tế (so với mức khiêm tốn 35,82% ban đầu), đồng thời chỉ số PR-AUC vẫn thiết lập mức kỷ lục mới (0,5620).", indent=True)
    
    # 3.5
    add_heading2(doc, "3.5. Bảng tổng hợp Đánh giá mô hình và Lựa chọn mô hình phù hợp nhất")
    
    add_heading3(doc, "3.5.1. Bảng so sánh đa chỉ số — Toàn bộ 10 cấu hình mô hình")
    add_body_para(doc, "Bảng 3.13 tổng hợp kết quả đối sánh đa chiều của toàn bộ 10 cấu hình mô hình đã được thử nghiệm độc lập trên tập kiểm tra Test (5.993 mẫu):")
    
    # Table 3.13: 10 models comparison
    add_table_caption(doc, "Bảng 3.13: Bảng tổng hợp đối sánh toàn bộ 10 cấu hình mô hình trên tập Test (5.993 mẫu)")
    t_10m = doc.add_table(rows=11, cols=7)
    t_10m.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_10m)
    for i, h in enumerate(["Cấu hình mô hình", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC", "PR-AUC"]):
        set_cell(t_10m.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_10m.cell(0, i).width = col_w_lr[i]
        
    data_10m = [
        ("Logistic Regression (Default)", "0,8106", "0,6610", "0,2956", "0,4085", "0,7492", "0,5162"),
        ("Logistic Regression (Balanced)", "0,7469", "0,4466", "0,6018", "0,5127", "0,7514", "0,5123"),
        ("Decision Tree (Default)", "0,7267", "0,3884", "0,4095", "0,3987", "0,6130", "0,2897"),
        ("Decision Tree (Balanced)", "0,7262", "0,3784", "0,3695", "0,3739", "0,5986", "0,2796"),
        ("Random Forest (Default)", "0,8143", "0,6364", "0,3748", "0,4718", "0,7659", "0,5381"),
        ("Random Forest (Balanced)", "0,7973", "0,5471", "0,4864", "0,5150", "0,7661", "0,5297"),
        ("XGBoost (Baseline)", "0,8201", "0,6766", "0,3582", "0,4684", "0,7792", "0,5611"),
        ("RF Default Tuned (Thresh 0,30)", "0,8206", "0,6785", "0,3597", "0,4702", "0,7773", "0,5610"),
        ("RF Balanced Tuned (Thresh 0,55)", "0,7764", "0,4956", "0,5950", "0,5408", "0,7753", "0,5584"),
        ("XGBoost Tuned (Thresh 0,60) ★", "0,7686", "0,4820", "0,6161", "0,5409", "0,7769", "0,5620")
    ]
    for r_idx, d in enumerate(data_10m, start=1):
        bold_r = (r_idx == 10)
        set_cell(t_10m.cell(r_idx, 0), d[0], bold=bold_r, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        for c in range(1, 7):
            set_cell(t_10m.cell(r_idx, c), d[c], bold=bold_r, size=9, align=WD_ALIGN_PARAGRAPH.RIGHT)
            t_10m.cell(r_idx, c).width = col_w_lr[c]
        t_10m.cell(r_idx, 0).width = col_w_lr[0]
        
    add_figure(doc, "reports/figures/week7_random_forest_feature_importance.png", "Hình 3.6: Mức độ quan trọng đặc trưng trích xuất từ mô hình Random Forest (Nguồn: reports/figures/week7_random_forest_feature_importance.png)", width_cm=14.0)
    
    add_figure(doc, "reports/figures/week7_xgboost_feature_importance.png", "Hình 3.7: Mức độ quan trọng đặc trưng trích xuất từ mô hình XGBoost Baseline (Nguồn: reports/figures/week7_xgboost_feature_importance.png)", width_cm=14.0)
    
    add_heading3(doc, "3.5.2. Phân tích chi tiết Ma trận nhầm lẫn, trade-off nghiệp vụ và quyết định chọn mô hình")
    add_body_para(doc, "Bảng 3.14 so sánh 3 ứng cử viên mạnh nhất sau giai đoạn tối ưu hóa siêu tham số:")
    
    # Table 3.14: Candidate comparison
    add_table_caption(doc, "Bảng 3.14: So sánh 3 mô hình Ensemble Tuned theo các tiêu chí lựa chọn cốt lõi")
    t_cand = doc.add_table(rows=7, cols=4)
    t_cand.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_cand)
    col_w_cand = [Cm(4.5), Cm(3.8), Cm(3.8), Cm(3.9)]
    for i, h in enumerate(["Tiêu chí tuyển chọn", "RF Default Tuned", "RF Balanced Tuned", "XGBoost Tuned ★"]):
        set_cell(t_cand.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_cand.cell(0, i).width = col_w_cand[i]
        
    cand_data = [
        ("PR-AUC trên tập Test", "0,5610", "0,5584", "0,5620 (Cao nhất toàn diện)"),
        ("Điểm CV PR-AUC (Độ ổn định)", "0,5656 (±0,0088)", "0,5627 (±0,0096)", "0,5646 (±0,0122)"),
        ("Recall (Phát hiện vỡ nợ)", "0,3597", "0,5950", "0,6161 (Vượt trội nhất)"),
        ("F1-Score tổng hợp", "0,4702", "0,5408", "0,5409 (Cao nhất)"),
        ("ROC-AUC tổng thể", "0,7773", "0,7753", "0,7769"),
        ("Tương thích SHAP TreeExplainer", "Đạt chuẩn", "Đạt chuẩn", "Tối ưu hóa cao nhất")
    ]
    for r_idx, d in enumerate(cand_data, start=1):
        set_cell(t_cand.cell(r_idx, 0), d[0], bold=True, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_cand.cell(r_idx, 1), d[1], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_cand.cell(r_idx, 2), d[2], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_cand.cell(r_idx, 3), d[3], bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        for c in range(4):
            t_cand.cell(r_idx, c).width = col_w_cand[c]
            
    add_body_para(doc, "Quyết định lựa chọn chính thức: Đề tài chính thức lựa chọn mô hình XGBoost Tuned với ngưỡng quyết định threshold = 0,60 làm mô hình tối ưu nhất (lưu trữ tại models/final_candidate_model.pkl). Mô hình đạt PR-AUC cao nhất (0,5620), đồng thời tối đa hóa tỷ lệ nhận diện khách hàng rủi ro với Recall đạt 61,61% và điểm F1 đạt 0,5409.", indent=True)
    
    # 3.6
    add_heading2(doc, "3.6. Kết quả Thực nghiệm Giải thích mô hình bằng SHAP")
    add_body_para(doc, "SHAP TreeExplainer được thực thi trên tập kiểm tra độc lập X_test (5.993 mẫu x 33 đặc trưng). Giá trị kỳ vọng cơ sở ghi nhận E[f(X)] = 0,089860 (trong không gian log-odds).")
    
    add_heading3(doc, "3.6.1. Trực quan hóa kết quả đóng góp đặc trưng tổng thể (Global Feature Importance Plot)")
    add_body_para(doc, "Bảng 3.15 liệt kê Top 10 đặc trưng chi phối mạnh nhất đến quyết định dự báo theo giá trị Mean |SHAP Value|:")
    
    # Table 3.15: Top 10 SHAP
    add_table_caption(doc, "Bảng 3.15: Top 10 đặc trưng quan trọng nhất theo giá trị trung bình SHAP tuyệt đối (Mean |SHAP Value|)")
    t_shap = doc.add_table(rows=11, cols=5)
    t_shap.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_shap)
    col_w_shap = [Cm(1.5), Cm(4.8), Cm(2.7), Cm(3.0), Cm(4.0)]
    for i, h in enumerate(["Thứ hạng", "Tên đặc trưng", "Mean |SHAP|", "Nhóm đặc trưng", "Ý nghĩa tác động nghiệp vụ"]):
        set_cell(t_shap.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_shap.cell(0, i).width = col_w_shap[i]
        
    shap_data = [
        ("1", "MAX_PAY_DELAY", "0,4494", "Feature mới", "Số tháng trậm trả tối đa 6 tháng."),
        ("2", "PAY_0", "0,2797", "Biến gốc", "Trạng thái thanh toán kỳ T9/2005."),
        ("3", "COUNT_LATE_PAYMENT", "0,1211", "Feature mới", "Tần suất số kỳ phát sinh chậm trả."),
        ("4", "BILL_AMT1", "0,1126", "Biến gốc", "Quy mô dư nợ hóa đơn kỳ gần nhất."),
        ("5", "UTILIZATION_RATE_SEPT", "0,0942", "Feature mới", "Tỷ lệ sử dụng hạn mức tín dụng kỳ T9."),
        ("6", "LIMIT_BAL", "0,0921", "Biến gốc", "Hạn mức tín dụng được cấp."),
        ("7", "PAY_AMT2", "0,0817", "Biến gốc", "Số tiền đã thanh toán trong kỳ T8."),
        ("8", "PAY_AMT3", "0,0725", "Biến gốc", "Số tiền đã thanh toán trong kỳ T7."),
        ("9", "PAY_AMT1", "0,0719", "Biến gốc", "Số tiền đã thanh toán trong kỳ T9."),
        ("10", "MEAN_PAY_AMT", "0,0639", "Feature mới", "Khả năng thanh toán trung bình 6 tháng.")
    ]
    for r_idx, d in enumerate(shap_data, start=1):
        bold_r = ("Feature mới" in d[3])
        set_cell(t_shap.cell(r_idx, 0), d[0], bold=bold_r, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_shap.cell(r_idx, 1), d[1], bold=bold_r, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_shap.cell(r_idx, 2), d[2], bold=bold_r, size=9, align=WD_ALIGN_PARAGRAPH.RIGHT)
        set_cell(t_shap.cell(r_idx, 3), d[3], bold=bold_r, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_shap.cell(r_idx, 4), d[4], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        for c in range(5):
            t_shap.cell(r_idx, c).width = col_w_shap[c]
            
    add_figure(doc, "reports/figures/week9_shap_bar.png", "Hình 3.8: Biểu đồ thanh SHAP Global Feature Importance theo độ lớn Mean |SHAP| (Nguồn: reports/figures/week9_shap_bar.png)", width_cm=14.0)
    
    add_figure(doc, "reports/figures/week9_shap_beeswarm.png", "Hình 3.9: Biểu đồ SHAP Beeswarm Plot thể hiện độ lớn và chiều hướng tác động của đặc trưng (Nguồn: reports/figures/week9_shap_beeswarm.png)", width_cm=15.0)
    
    add_body_para(doc, "Đánh giá vai trò của Feature Engineering: Đáng chú ý, có 4 trong 10 đặc trưng quan trọng nhất là các biến mới được trích xuất ở Tuần 5. Đặc biệt, biến MAX_PAY_DELAY vươn lên dẫn đầu toàn hệ thống với Mean |SHAP| = 0,4494, vượt xa biến gốc PAY_0 (0,2797) tới 1,6 lần. Điều này chứng minh rằng việc tổng hợp hành vi vi phạm đỉnh điểm qua nhiều chu kỳ đã cung cấp tín hiệu phân biệt mạnh hơn dữ liệu thô của một tháng riêng lẻ.", indent=True)
    
    add_heading3(doc, "3.6.2. Phân tích kết quả giải thích dự báo trường hợp khách hàng cụ thể (Local Waterfall Plot)")
    add_body_para(doc, "Biểu đồ phụ thuộc (Dependence Plots) tại Hình 3.10 và 3.11 minh họa rõ mối quan hệ phi tuyến: Khi MAX_PAY_DELAY và PAY_0 chuyển từ trạng thái an toàn (<=0) sang trậm trả từ 2 tháng trở lên, giá trị SHAP tăng vọt phi tuyến theo chiều dương, làm tăng mạnh log-odds vỡ nợ.")
    
    add_figure(doc, "reports/figures/week9_dependence_MAX_PAY_DELAY.png", "Hình 3.10: Biểu đồ phụ thuộc SHAP Dependence Plot của đặc trưng MAX_PAY_DELAY (Nguồn: reports/figures/week9_dependence_MAX_PAY_DELAY.png)", width_cm=14.0)
    
    add_figure(doc, "reports/figures/week9_dependence_PAY_0.png", "Hình 3.11: Biểu đồ phụ thuộc SHAP Dependence Plot của đặc trưng PAY_0 (Nguồn: reports/figures/week9_dependence_PAY_0.png)", width_cm=14.0)
    
    add_body_para(doc, "Ở cấp độ hồ sơ cá thể, ba trường hợp điển hình trên tập Test được phân tích chi tiết tại Bảng 3.16:")
    
    # Table 3.16: Local 3 cases
    add_table_caption(doc, "Bảng 3.16: Tóm tắt kết quả phân tích giải thích cá thể (Local Waterfall) cho 3 hồ sơ đại diện")
    t_local = doc.add_table(rows=4, cols=8)
    t_local.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_local)
    col_w_loc = [Cm(2.2), Cm(1.2), Cm(2.0), Cm(1.8), Cm(2.2), Cm(2.2), Cm(2.2), Cm(2.2)]
    for i, h in enumerate(["Phân loại ca", "Index", "Xác suất", "Ngưỡng", "Dự báo", "Thực tế", "Kết luận", "Yếu tố chính"]):
        set_cell(t_local.cell(0, i), h, bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_local.cell(0, i).width = col_w_loc[i]
        
    local_data = [
        ("High Risk", "3433", "96,16%", "0,60", "Default", "Default", "True Positive", "MAX_PAY_DELAY, PAY_0"),
        ("Low Risk", "1985", "2,84%", "0,60", "Non-Default", "Non-Default", "True Negative", "LIMIT_BAL, PAY_AMT2"),
        ("Near Thresh", "1753", "60,01%", "0,60", "Default", "Non-Default", "False Positive", "MAX_PAY_DELAY")
    ]
    for r_idx, d in enumerate(local_data, start=1):
        set_cell(t_local.cell(r_idx, 0), d[0], bold=True, size=8, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_local.cell(r_idx, 1), d[1], bold=False, size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_local.cell(r_idx, 2), d[2], bold=True, size=8, align=WD_ALIGN_PARAGRAPH.RIGHT)
        set_cell(t_local.cell(r_idx, 3), d[3], bold=False, size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_local.cell(r_idx, 4), d[4], bold=False, size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_local.cell(r_idx, 5), d[5], bold=False, size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_local.cell(r_idx, 6), d[6], bold=True, size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_local.cell(r_idx, 7), d[7], bold=False, size=8, align=WD_ALIGN_PARAGRAPH.LEFT)
        for c in range(8):
            t_local.cell(r_idx, c).width = col_w_loc[c]
            
    add_figure(doc, "reports/figures/week9_waterfall_high_risk.png", "Hình 3.12: Biểu đồ SHAP Waterfall giải thích hồ sơ Rủi ro cao (Index 3433, Prob = 96,16%) (Nguồn: reports/figures/week9_waterfall_high_risk.png)", width_cm=14.0)
    
    add_figure(doc, "reports/figures/week9_waterfall_low_risk.png", "Hình 3.13: Biểu đồ SHAP Waterfall giải thích hồ sơ Rủi ro thấp (Index 1985, Prob = 2,84%) (Nguồn: reports/figures/week9_waterfall_low_risk.png)", width_cm=14.0)
    
    add_figure(doc, "reports/figures/week9_waterfall_near_threshold.png", "Hình 3.14: Biểu đồ SHAP Waterfall giải thích hồ sơ Biên giới ngưỡng (Index 1753, Prob = 60,01%) (Nguồn: reports/figures/week9_waterfall_near_threshold.png)", width_cm=14.0)
    
    # 3.7
    add_heading2(doc, "3.7. Cài đặt, Triển khai và Kiểm thử ứng dụng Web Prototype")
    
    add_heading3(doc, "3.7.1. Cài đặt giao diện người dùng và tích hợp mô hình ML đã chọn")
    add_body_para(doc, "Ứng dụng Web Prototype hỗ trợ ra quyết định (DSS Prototype) được xây dựng hoàn thiện bằng Streamlit (tệp app.py) kết hợp module suy luận backend độc lập (src/prediction.py). Ứng dụng cung cấp:")
    add_bullet_item(doc, "Biểu mẫu phân nhóm khoa học tiếp nhận 23 thông số đầu vào của khách hàng thẻ.", bold_prefix="Giao diện nhập liệu: ")
    add_bullet_item(doc, "Hiển thị đồng hồ đo xác suất vỡ nợ tương tác (Plotly Gauge Chart) và phân tầng mức rủi ro theo ba dải màu trực quan.", bold_prefix="Bảng điều khiển rủi ro: ")
    add_bullet_item(doc, "Trực quan hóa Top 10 đặc trưng SHAP đóng góp theo thời gian thực cho từng truy vấn cụ thể.", bold_prefix="Minh bạch hóa quyết định: ")
    add_body_para(doc, "Mô hình và Scaler được nạp vào bộ nhớ thông qua cơ chế lưu đệm @st.cache_resource, giúp thời gian phản hồi suy luận trung bình đạt dưới 1,2 giây/truy vấn.", indent=True)
    
    add_heading3(doc, "3.7.2. Kịch bản chạy thử nghiệm dự báo và kiểm thử tích hợp (Integration Tests)")
    add_body_para(doc, "Bộ kiểm thử tích hợp tự động (scripts/test_week10.py) được thực thi độc lập trên môi trường ảo .venv để kiểm định tính toàn vẹn:")
    
    # Table 3.17: Test week 10 results
    add_table_caption(doc, "Bảng 3.17: Kết quả thực thi bộ kiểm thử tích hợp tự động hệ thống Web Prototype (6 bài test)")
    t_test = doc.add_table(rows=7, cols=5)
    t_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_test)
    col_w_test = [Cm(1.2), Cm(4.5), Cm(4.5), Cm(3.8), Cm(2.0)]
    for i, h in enumerate(["STT", "Tên kịch bản kiểm thử", "Điều kiện đánh giá Đạt", "Kết quả thực tế đo được", "Kết luận"]):
        set_cell(t_test.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_test.cell(0, i).width = col_w_test[i]
        
    test_data = [
        ("1", "Khách hàng bình thường", "Features = 33, Phân loại Non-Default", "Prob = 11,89%, Low Risk", "ĐẠT (PASS)"),
        ("2", "Khách hàng rủi ro cao", "Xác suất vỡ nợ ≥ 60%", "Prob = 78,22%, High Risk", "ĐẠT (PASS)"),
        ("3", "Khách hàng an toàn cao", "Xác suất vỡ nợ < 30%", "Prob = 18,96%, Low Risk", "ĐẠT (PASS)"),
        ("4", "Kiểm định thứ tự đặc trưng", "33 features khớp 100% X_train_fe", "Khớp hoàn toàn 33/33 cột", "ĐẠT (PASS)"),
        ("5", "Tính nhất quán suy luận", "Sai lệch trực tiếp vs API < 1e-6", "Độ lệch Δ = 0,00e+00", "ĐẠT (PASS)"),
        ("6", "Giải thích SHAP thời gian thực", "Shape = (33,), E[f(X)] = 0,08986", "Tính toán SHAP thành công", "ĐẠT (PASS)")
    ]
    for r_idx, d in enumerate(test_data, start=1):
        set_cell(t_test.cell(r_idx, 0), d[0], bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_test.cell(r_idx, 1), d[1], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_test.cell(r_idx, 2), d[2], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_test.cell(r_idx, 3), d[3], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_test.cell(r_idx, 4), d[4], bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        for c in range(5):
            t_test.cell(r_idx, c).width = col_w_test[c]
            
    # 3.8
    add_heading2(doc, "3.8. Đánh giá tổng quan kết quả thực nghiệm, Thảo luận và Hạn chế đề tài")
    
    add_heading3(doc, "3.8.1. Tổng kết các kết quả chính đạt được")
    add_bullet_item(doc, "Xây dựng thành công quy trình Machine Learning Pipeline chuẩn hóa trên 30.000 mẫu dữ liệu UCI Credit Card, thực hiện kiểm duyệt, làm sạch và kiểm soát triệt để 7/7 tiêu chí rò rỉ dữ liệu.", bold_prefix="1. Về chuẩn hóa dữ liệu: ")
    add_bullet_item(doc, "Đề xuất và trích xuất thành công 10 đặc trưng tài chính mới. Bằng chứng SHAP xác nhận 4/10 biến quan trọng nhất là các biến mới, trong đó MAX_PAY_DELAY dẫn đầu toàn diện.", bold_prefix="2. Về Feature Engineering: ")
    add_bullet_item(doc, "Mô hình XGBoost Tuned (ngưỡng 0,60) thiết lập kỷ lục PR-AUC cao nhất (0,5620) và Recall cao nhất (0,6161), giải quyết hiệu quả bài toán mất cân bằng dữ liệu.", bold_prefix="3. Về hiệu năng mô hình: ")
    add_bullet_item(doc, "Tích hợp thành công khung giải thích SHAP TreeExplainer, minh bạch hóa hoàn toàn cơ chế ra quyết định của mô hình cây phức tạp ở cả cấp độ toàn cục và cá thể.", bold_prefix="4. Về khả năng giải thích (XAI): ")
    add_bullet_item(doc, "Hiện thực hóa hệ thống ứng dụng Web DSS Prototype tương tác trực quan, vượt qua 6/6 bài kiểm thử tích hợp tự động với mã lỗi 0.", bold_prefix="5. Về sản phẩm ứng dụng: ")
    
    add_heading3(doc, "3.8.2. Hạn chế của đề tài và định hướng phát triển thực tế")
    add_body_para(doc, "Bên cạnh các kết quả tích cực đạt được, đề tài nhận diện các hạn chế mang tính học thuật cần lưu ý:")
    add_bullet_item(doc, "Tập dữ liệu phản ánh hành vi khách hàng thẻ tại Đài Loan giai đoạn 2005. Chưa có điều kiện kiểm nghiệm chéo trên dữ liệu thực tế tại các tổ chức tín dụng Việt Nam hiện nay.", bold_prefix="Hạn chế về dữ liệu: ")
    add_bullet_item(doc, "Ngưỡng quyết định 0,60 được lựa chọn dựa trên tối ưu điểm F1 trên tập huấn luyện; trong thực tế triển khai ngân hàng, ngưỡng này cần được cân chỉnh linh hoạt theo ma trận chi phí tài chính cụ thể của từng tổ chức.", bold_prefix="Hạn chế về phương pháp luận: ")
    add_bullet_item(doc, "Ứng dụng Web hiện mới chỉ dừng lại ở phiên bản Prototype phục vụ thẩm định hồ sơ đơn lẻ (single prediction), chưa hỗ trợ cơ chế chấm điểm hàng loạt (batch scoring) hoặc giám sát độ trôi mô hình (model drift).", bold_prefix="Hạn chế về ứng dụng: ")
    add_bullet_item(doc, "Các phân tích SHAP phản ánh mối quan hệ liên kết thống kê mô hình học được từ dữ liệu lịch sử, không đại diện cho quan hệ nhân quả tuyệt đối trong thực tiễn kinh tế.", bold_prefix="Hạn chế về diễn giải: ")
    
    # Done chapter 3 content

def build_chapter_3():
    doc = Document()
    setup_page(doc)
    add_page_number(doc)
    
    # Title
    title_p = doc.add_paragraph()
    set_para_format(title_p, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=2, line_spacing=1.3)
    r_sub = title_p.add_run("BÁO CÁO ĐỒ ÁN TỐT NGHIỆP\n")
    set_font(r_sub, size=12, bold=True, color=(100, 100, 100))
    
    add_chapter_3_content(doc)
    
    out_dir = r"F:\DATN\docs"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Chuong_3_Cai_Dat_Thuc_Nghiem_Danh_Gia.docx")
    doc.save(out_path)
    print(f"SUCCESS: Saved Chuong 3 Word to {out_path}")
    return out_path

if __name__ == "__main__":
    build_chapter_3()
