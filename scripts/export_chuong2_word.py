# -*- coding: utf-8 -*-
"""
Export Chuong 2: PHUONG PHAP THUC HIEN sang Microsoft Word (.docx)
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
    pf.line_spacing = Pt(19.5)  # 1.5 lines
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

def add_formula_para(doc, formula_text, label=None):
    para = doc.add_paragraph()
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before = Pt(4)
    pf.space_after = Pt(6)
    pf.line_spacing = Pt(19.5)
    
    run = para.add_run(formula_text)
    set_font(run, size=12, italic=True)
    
    if label:
        run_lbl = para.add_run(f"    ({label})")
        set_font(run_lbl, size=12, bold=False, italic=False)
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

def add_chapter_2_content(doc):
    add_heading1(doc, "CHƯƠNG 2. PHƯƠNG PHÁP THỰC HIỆN")
    
    add_body_para(doc, "Chương 2 trình bày chi tiết toàn bộ cơ sở phương pháp luận và các giải pháp kỹ thuật được áp dụng trong quá trình thực hiện đề tài. Nội dung bao quát từ giai đoạn kiểm duyệt dữ liệu, phân tích khám phá (EDA), thiết kế tiền xử lý, kiểm soát rò rỉ dữ liệu (Data Leakage Control), đề xuất 10 biến trích rút đặc trưng (Feature Engineering), đến kiến trúc các thuật toán Machine Learning (Logistic Regression, Decision Tree, Random Forest, XGBoost), phương pháp xử lý mất cân bằng lớp và tối ưu siêu tham số, kỹ thuật giải thích mô hình bằng SHAP, cùng thiết kế kiến trúc hệ thống Web Prototype hỗ trợ ra quyết định tín dụng. Các quyết định kỹ thuật đều được luận giải minh bạch nhằm bảo đảm tính tái lập (reproducibility) và tính vững chắc của thực nghiệm.", indent=True)
    
    # 2.1
    add_heading2(doc, "2.1. Quy trình tổng thể xây dựng mô hình Machine Learning (ML Pipeline)")
    add_body_para(doc, "Quy trình nghiên cứu được tổ chức theo kiến trúc pipeline tuần tự, tuân thủ nghiêm ngặt nguyên tắc kiểm soát rò rỉ dữ liệu xuyên suốt từ bước nạp dữ liệu đến suy luận mô hình. Toàn bộ thực nghiệm được chia thành 8 giai đoạn liên kết chặt chẽ:")
    
    # Pipeline steps table
    add_table_caption(doc, "Bảng 2.1: Các giai đoạn trong quy trình thực nghiệm Machine Learning Pipeline")
    t_pipe = doc.add_table(rows=9, cols=3)
    t_pipe.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_pipe)
    
    col_w = [Cm(2.0), Cm(5.0), Cm(9.0)]
    pipe_headers = ["Giai đoạn", "Tên bước thực hiện", "Nội dung kỹ thuật và đầu ra chính"]
    for i, h in enumerate(pipe_headers):
        set_cell(t_pipe.cell(0, i), h, bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_pipe.cell(0, i).width = col_w[i]
        
    pipe_data = [
        ("Bước 1", "Kiểm duyệt dữ liệu & EDA", "Kiểm tra tính toàn vẹn 30.000 mẫu, phát hiện 35 dòng trùng lặp, mã ngoại lệ EDUCATION/MARRIAGE, ma trận tương quan Pearson."),
        ("Bước 2", "Tiền xử lý dữ liệu", "Loại bỏ ID, làm sạch trùng lặp, phân chia Train/Test (80/20 stratified), fit RobustScaler duy nhất trên tập Train."),
        ("Bước 3", "Feature Engineering", "Trích xuất 10 đặc trưng tài chính mới (tỷ lệ thanh toán, dư nợ trung bình, quỹ đạo trả nợ), kiểm định ma trận 33 đặc trưng."),
        ("Bước 4", "Mô hình Cơ sở (Baseline)", "Xây dựng 4 mô hình cơ sở: Logistic Regression (Default/Balanced) và Decision Tree (Default/Balanced) làm mốc so sánh."),
        ("Bước 5", "Ensemble Models", "Xây dựng Random Forest (Default/Balanced) và XGBoost Baseline; đánh giá năng lực của cơ chế Bagging và Boosting."),
        ("Bước 6", "Tối ưu hóa & Chọn mô hình", "RandomizedSearchCV kết hợp Stratified 5-Fold CV, phân tích ngưỡng Out-Of-Fold (OOF), chọn XGBoost Tuned (threshold = 0,60)."),
        ("Bước 7", "Giải thích mô hình SHAP", "Ứng dụng TreeExplainer phân tích tầm quan trọng toàn cục (Global Beeswarm/Bar) và giải thích từng ca cá thể (Local Waterfall)."),
        ("Bước 8", "Xây dựng Web Prototype", "Thiết kế giao diện Streamlit DSS Prototype, tích hợp pipeline dự báo và SHAP thời gian thực, thực thi 6/6 Integration Tests.")
    ]
    for row_idx, data in enumerate(pipe_data, start=1):
        set_cell(t_pipe.cell(row_idx, 0), data[0], bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_pipe.cell(row_idx, 1), data[1], bold=False, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_pipe.cell(row_idx, 2), data[2], bold=False, size=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        for c in range(3):
            t_pipe.cell(row_idx, c).width = col_w[c]

    add_body_para(doc, "Nguyên tắc cốt lõi xuyên suốt toàn bộ pipeline là sự độc lập tuyệt đối của tập Kiểm tra (Test set). Tập Test chỉ được sử dụng một lần duy nhất tại bước đánh giá cuối cùng; không tham gia vào việc học tham số chuẩn hóa, không tham gia vào lựa chọn siêu tham số hay điều chỉnh ngưỡng phân loại.")
    
    # 2.2
    add_heading2(doc, "2.2. Kiểm duyệt dữ liệu và Phương pháp phân tích khám phá (Data Audit & EDA Methods)")
    
    add_heading3(doc, "2.2.1. Phương pháp kiểm duyệt chất lượng dữ liệu (Data Audit)")
    add_body_para(doc, "Kiểm duyệt dữ liệu là tiền đề kiểm soát chất lượng đầu vào nhằm phát hiện sớm các dị thường có thể làm suy giảm độ chính xác hoặc sai lệch hành vi mô hình. Bốn nội dung kiểm duyệt trọng tâm bao gồm:")
    add_bullet_item(doc, "Kiểm tra kích thước ma trận dữ liệu, cấu trúc kiểu dữ liệu (data types), kiểm định ô khuyết (NULL/NaN). Kết quả kiểm tra là căn cứ xác định có cần cơ chế gán giá trị khuyết (imputation) hay không.", bold_prefix="Kiểm tra tính toàn vẹn cơ bản: ")
    add_bullet_item(doc, "Phân biệt hai cấp độ: (1) Trùng lặp hoàn toàn kể cả cột ID; (2) Trùng lặp đặc trưng hành vi (bỏ qua cột ID). Với các nhóm trùng lặp đặc trưng, cần đối chiếu tính nhất quán của biến mục tiêu; nếu xảy ra xung đột nhãn (conflicting labels), cần loại bỏ mẫu mâu thuẫn để tránh gây nhiễu cho mô hình.", bold_prefix="Kiểm tra dòng trùng lặp (Duplicate Audit): ")
    add_bullet_item(doc, "So sánh tập giá trị thực tế trong các cột phân loại (SEX, EDUCATION, MARRIAGE) với bộ mô tả trong từ điển dữ liệu UCI. Các giá trị ngoài danh mục chính thức cần được phân loại và xử lý chuẩn hóa.", bold_prefix="Kiểm tra mã danh mục chưa tài liệu hóa (Undocumented Categories): ")
    add_bullet_item(doc, "Tính toán thống kê mô tả (Mean, Median, Độ lệch chuẩn, Min, Max, Skewness, Kurtosis) của các biến liên tục. Hệ số Skewness cực đại cho thấy sự tồn tại của ngoại lệ lớn, đòi hỏi kỹ thuật chuẩn hóa phù hợp.", bold_prefix="Kiểm tra phân bố lệch và giá trị ngoại lệ: ")
    
    add_heading3(doc, "2.2.2. Phương pháp phân tích tương quan và trực quan hóa phân phối")
    add_body_para(doc, "Quy trình phân tích khám phá EDA được triển khai theo hai chiều:")
    add_bullet_item(doc, "Trực quan hóa hình dạng phân phối từng đặc trưng thông qua biểu đồ Histogram và Boxplot. Xác định tỷ lệ mất cân bằng biến mục tiêu (Imbalance Ratio) để định hình chiến lược học máy thích ứng.", bold_prefix="Phân tích đơn biến (Univariate Analysis): ")
    add_bullet_item(doc, "Sử dụng ma trận tương quan Pearson r(X, Y) để đo mức độ tương quan tuyến tính giữa các biến đầu vào với nhãn vỡ nợ, đồng thời phát hiện sớm hiện tượng đa cộng tuyến (Multicollinearity) giữa các kỳ sao kê BILL_AMT1..6. Tiến hành phân tích tỷ lệ vỡ nợ theo từng phân nhóm nhân khẩu học và phân tầng hạn mức tín dụng.", bold_prefix="Phân tích đa biến và tương quan (Bivariate & Multivariate Analysis): ")
    
    # 2.3
    add_heading2(doc, "2.3. Phương pháp Tiền xử lý dữ liệu và Quy tắc chống Data Leakage")
    
    add_heading3(doc, "2.3.1. Quy tắc phân chia tập Train/Test và kiểm soát rò rỉ dữ liệu")
    add_body_para(doc, "Hiện tượng rò rỉ dữ liệu (Data Leakage) xảy ra khi thông tin từ tập kiểm tra vô tình xuất hiện trong quá trình huấn luyện, dẫn đến kết quả đánh giá quá lạc quan nhưng thất bại khi ứng dụng trên dữ liệu thực tế. Để ngăn ngừa triệt để nguy cơ này, quy trình tiền xử lý tuân thủ các nguyên tắc sau:")
    add_bullet_item(doc, "Tập dữ liệu sau khi làm sạch được phân chia theo tỷ lệ 80% huấn luyện (Train) và 20% kiểm tra (Test). Chiến lược phân tầng (Stratification) được áp dụng dựa trên nhãn biến mục tiêu nhằm bảo toàn nguyên vẹn tỷ lệ mất cân bằng (khoảng 22,12% Default) trên cả hai tập.", bold_prefix="Phân chia phân tầng (Stratified Split): ")
    
    add_formula_para(doc, "Dataset_clean  →  train_test_split(80%, stratify = y, random_state = 42)  →  {X_train, X_test, y_train, y_test}", label="2.1")
    
    add_bullet_item(doc, "Mọi phép biến đổi tham số hóa (tính Median, IQR của RobustScaler) bắt buộc chỉ được fit trên X_train. Tập X_test chỉ được áp dụng phép biến đổi transform với tham số đã học, tuyệt đối không fit lại.", bold_prefix="Nguyên tắc Fit-Only-On-Train: ")
    
    # Table 2.2: 7 leakage criteria
    add_table_caption(doc, "Bảng 2.2: Bộ tiêu chí kiểm soát rò rỉ dữ liệu (Data Leakage Audit)")
    t_leak = doc.add_table(rows=8, cols=3)
    t_leak.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_leak)
    col_w_leak = [Cm(1.5), Cm(10.5), Cm(4.0)]
    for i, h in enumerate(["STT", "Tiêu chí kiểm soát Data Leakage", "Trạng thái kiểm tra"]):
        set_cell(t_leak.cell(0, i), h, bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_leak.cell(0, i).width = col_w_leak[i]
        
    leak_items = [
        ("1", "Cột định danh ID bị loại bỏ hoàn toàn, không tham gia làm đặc trưng học.", "ĐẠT (PASS)"),
        ("2", "Phân chia Train/Test hoàn thành trước mọi bước chuẩn hóa (Scaling/Encoding).", "ĐẠT (PASS)"),
        ("3", "Mã hóa phân loại không sử dụng nhãn hay tần suất học từ tập Test.", "ĐẠT (PASS)"),
        ("4", "Bộ chuẩn hóa RobustScaler chỉ học Median và IQR duy nhất từ X_train.", "ĐẠT (PASS)"),
        ("5", "Các kỹ thuật cân bằng dữ liệu (nếu có) chỉ thực hiện trong nội bộ fold train.", "ĐẠT (PASS)"),
        ("6", "Nhãn của tập Test không tham gia vào bất kỳ công đoạn xử lý đặc trưng nào.", "ĐẠT (PASS)"),
        ("7", "Số liệu thống kê của tập Test không rò rỉ ngược lại tập Train.", "ĐẠT (PASS)")
    ]
    for r_idx, lk in enumerate(leak_items, start=1):
        set_cell(t_leak.cell(r_idx, 0), lk[0], bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_leak.cell(r_idx, 1), lk[1], bold=False, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_leak.cell(r_idx, 2), lk[2], bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
        for c in range(3):
            t_leak.cell(r_idx, c).width = col_w_leak[c]

    add_heading3(doc, "2.3.2. Phương pháp xử lý giá trị ngoại lệ và giá trị bất thường")
    add_body_para(doc, "Đối với 35 dòng trùng lặp đặc trưng (cùng hành vi tài chính nhưng khác mã ID), kết quả kiểm tra xác nhận 100% các cặp này đều có nhãn mục tiêu đồng nhất (không có conflicting labels). Do đó, giải pháp khoa học là loại bỏ các dòng trùng lặp dư thừa, giữ lại một bản ghi đại diện, đưa tập dữ liệu về kích thước chuẩn 29.965 quan sát.", indent=True)
    add_body_para(doc, "Đối với các mã danh mục ngoài mô tả chuẩn: cột EDUCATION chứa các mã {0, 5, 6} được gom về nhóm 4 (Others), đưa biến về 4 mức chuẩn {1: Sau đại học, 2: Đại học, 3: Phổ thông, 4: Khác}. Cột MARRIAGE chứa mã {0} được gom về nhóm 3 (Khác), đưa về 3 mức chuẩn {1: Đã kết hôn, 2: Độc thân, 3: Khác}. Giải pháp gom nhóm giúp bảo toàn kích thước mẫu thay vì loại bỏ dữ liệu.", indent=True)
    add_body_para(doc, "Đối với các giá trị âm trong BILL_AMT1..6: Đây là hiện tượng nghiệp vụ bình thường trong thẻ tín dụng khi khách hàng thanh toán dư hoặc nhận tiền hoàn lại (refund/cashback), do đó được giữ nguyên giá trị thực tế. Tương tự, giá trị 0 trong PAY_AMT1..6 phản ánh khách hàng không thanh toán trong kỳ, mang thông tin rủi ro cốt lõi nên được bảo lưu.", indent=True)
    
    add_heading3(doc, "2.3.3. Phương pháp chuẩn hóa (Scaling) và mã hóa đặc trưng duy nhất trên tập Train")
    add_body_para(doc, "Phân tích EDA phát hiện các biến thanh toán (PAY_AMT1..6) có hệ số Skewness rất cao (từ 10,6 đến 30,5) với các giá trị ngoại lệ cực lớn. Trong điều kiện này, phương pháp Standard (Z-score) hoặc MinMax sẽ bị kéo lệch nghiêm trọng bởi các giá trị ngoại lệ. Do đó, phương pháp RobustScaler được lựa chọn làm giải pháp chuẩn hóa chính thức.", indent=True)
    add_body_para(doc, "RobustScaler loại bỏ giá trị trung vị (Median) và co giãn theo khoảng tứ phân vị (Interquartile Range - IQR), mang lại tính trơ vững trước ngoại lệ cực đại:", indent=True)
    
    add_formula_para(doc, "x_scaled = (x - Median(X_train)) / IQR(X_train),  trong đó IQR = Q75(X_train) - Q25(X_train)", label="2.2")
    
    add_body_para(doc, "Phạm vi áp dụng chuẩn hóa: Chỉ áp dụng cho 22 biến số học liên tục (gồm LIMIT_BAL, AGE, BILL_AMT1..6, PAY_AMT1..6 và các biến tài chính mới). Đối với 9 biến phân loại và thứ tự (SEX, EDUCATION, MARRIAGE, PAY_0, PAY_2..6), phương pháp Passthrough được áp dụng để bảo tồn bản chất thứ tự số tháng chậm trả.", indent=True)
    
    # 2.4
    add_heading2(doc, "2.4. Đề xuất Kỹ thuật trích rút đặc trưng (Feature Engineering Proposals)")
    
    add_heading3(doc, "2.4.1. Đề xuất các biến chỉ số tài chính")
    add_body_para(doc, "Tập dữ liệu gốc gồm 23 biến độc lập phản ánh thông tin sao kê thô. Để giúp các thuật toán học máy nắm bắt được quy luật hành vi dài hạn và mối quan hệ giữa các chu kỳ thanh toán, đề tài đề xuất trích xuất 10 đặc trưng tài chính mới dựa trên nghiệp vụ thẻ tín dụng ngân hàng.")
    add_body_para(doc, "Lưu ý quan trọng về chu kỳ thanh toán: Hóa đơn tháng 8 (BILL_AMT2) đến hạn vào tháng 9 và số tiền thực trả được ghi nhận tại PAY_AMT1. Vì vậy, tỷ lệ thanh toán đúng nghiệp vụ phải là PAY_AMT1 chia cho BILL_AMT2 (không phải chia cho BILL_AMT1).")
    
    # Table 2.3: 10 FE variables
    add_table_caption(doc, "Bảng 2.3: Danh mục 10 đặc trưng tài chính tổng hợp được đề xuất trích xuất")
    t_fe = doc.add_table(rows=11, cols=4)
    t_fe.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_fe)
    col_w_fe = [Cm(1.2), Cm(4.8), Cm(5.0), Cm(5.0)]
    fe_heads = ["STT", "Tên đặc trưng đề xuất", "Công thức toán học", "Ý nghĩa kinh tế và nghiệp vụ"]
    for i, h in enumerate(fe_heads):
        set_cell(t_fe.cell(0, i), h, bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
        t_fe.cell(0, i).width = col_w_fe[i]
        
    fe_data = [
        ("1", "UTILIZATION_RATE_SEPT", "BILL_AMT1 / LIMIT_BAL", "Tỷ lệ sử dụng hạn mức tín dụng kỳ gần nhất (tháng 9/2005)."),
        ("2", "MEAN_BILL_AMT", "(1/6) * Σ (BILL_AMTi), i=1..6", "Quy mô dư nợ bình quân trong toàn bộ chu kỳ 6 tháng."),
        ("3", "UTILIZATION_RATE_MEAN", "MEAN_BILL_AMT / LIMIT_BAL", "Tỷ lệ sử dụng hạn mức bình quân 6 tháng, đo áp lực nợ lâu dài."),
        ("4", "PAY_RATIO_SEPT", "PAY_AMT1 / BILL_AMT2", "Tỷ lệ thanh toán kỳ tháng 9 so với dư nợ sao kê tháng 8."),
        ("5", "PAY_RATIO_MEAN", "(1/5) * Σ (PAY_AMTk / BILL_AMTk+1)", "Tỷ lệ thanh toán bình quân qua 5 chu kỳ kế tiếp."),
        ("6", "MAX_PAY_DELAY", "max(PAY_0, PAY_2, ..., PAY_6)", "Số tháng chậm trả tối đa, phản ánh mức độ vi phạm nợ đỉnh điểm."),
        ("7", "COUNT_LATE_PAYMENT", "Σ 1(PAY_i > 0), i in {0, 2..6}", "Tần suất số kỳ phát sinh chậm trả nợ trong 6 tháng."),
        ("8", "MEAN_PAY_AMT", "(1/6) * Σ (PAY_AMTi), i=1..6", "Khả năng chi trả bằng tiền mặt trung bình mỗi tháng."),
        ("9", "BILL_TREND", "(BILL_AMT1 - BILL_AMT6) / LIMIT_BAL", "Quỹ đạo tăng trưởng dư nợ tương đối so với hạn mức tín dụng."),
        ("10", "PAY_TREND", "(PAY_AMT1 - PAY_AMT6) / LIMIT_BAL", "Quỹ đạo thay đổi khả năng chi trả của khách hàng qua thời gian.")
    ]
    for r_idx, d in enumerate(fe_data, start=1):
        set_cell(t_fe.cell(r_idx, 0), d[0], bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_fe.cell(r_idx, 1), d[1], bold=True, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_fe.cell(r_idx, 2), d[2], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(t_fe.cell(r_idx, 3), d[3], bold=False, size=9, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        for c in range(4):
            t_fe.cell(r_idx, c).width = col_w_fe[c]
            
    add_body_para(doc, "Xử lý các trường hợp biên (Edge Cases): Khi mẫu số LIMIT_BAL ≤ 0, gán tỷ lệ bằng 0,0 để tránh lỗi chia cho 0. Khi số dư nợ hóa đơn BILL_AMT{k+1} ≤ 0 (khách hàng không có nợ trong kỳ), quy ước tỷ lệ thanh toán đạt 1,0 (hoàn thành 100% nghĩa vụ). Toàn bộ 10 biến mới được kết hợp với 23 biến gốc làm sạch, tạo thành không gian 33 đặc trưng.", indent=True)
    
    add_heading3(doc, "2.4.2. Phương pháp đánh giá thực nghiệm tính hiệu quả của các đặc trưng đề xuất")
    add_body_para(doc, "Hiệu quả của các biến trích rút được đánh giá thông qua ba cơ chế: (1) Kiểm định tính toàn vẹn không phát sinh ô khuyết NaN hoặc Inf; (2) So sánh thứ hạng đóng góp trong cây quyết định (Feature Importance); (3) Định lượng mức độ đóng góp thông qua giá trị SHAP (Shapley Values) toàn cục tại Chương 3.")
    
    # 2.5
    add_heading2(doc, "2.5. Các thuật toán Machine Learning đề xuất")
    
    add_heading3(doc, "2.5.1. Logistic Regression (Mô hình Cơ sở)")
    add_body_para(doc, "Hồi quy Logistic là thuật toán phân loại tuyến tính cổ điển, đóng vai trò mô hình mốc (Baseline) để so sánh. Mô hình ánh xạ tổ hợp tuyến tính của các biến đầu vào sang xác suất thông qua hàm sigmoid:")
    add_formula_para(doc, "P(Y = 1 | X) = σ(z) = 1 / (1 + e^(-z)),  với z = β0 + Σ βj * Xj", label="2.3")
    add_body_para(doc, "Đề tài khảo sát hai cấu hình: (1) LR Default — sử dụng trọng số mặc định; (2) LR Balanced — sử dụng trọng số class_weight='balanced' nhằm phạt nặng hơn lỗi bỏ sót khách hàng vỡ nợ.")
    
    add_heading3(doc, "2.5.2. Decision Tree Classifier")
    add_body_para(doc, "Cây quyết định phân chia không gian dữ liệu bằng cách đệ quy lựa chọn ngưỡng tối ưu theo tiêu chí độ vẩn đục Gini (Gini Impurity):")
    add_formula_para(doc, "Gini(p) = 1 - Σ (pk)^2,  k in {0, 1}", label="2.4")
    add_body_para(doc, "Mô hình được thử nghiệm ở cả hai trạng thái trọng số (Default và Balanced) để đo lường độ nhạy của cấu trúc cây đơn lẻ trước mất cân bằng dữ liệu.")
    
    add_heading3(doc, "2.5.3. Random Forest Classifier")
    add_body_para(doc, "Random Forest là mô hình Ensemble theo phương pháp đóng bao (Bagging). Mô hình xây dựng tập hợp N cây quyết định độc lập trên các mẫu con bootstrap, tại mỗi nút chỉ xem xét ngẫu nhiên một tập con đặc trưng (thường là căn bậc hai của số đặc trưng). Dự báo cuối cùng là biểu quyết đa số (Majority Voting):")
    add_formula_para(doc, "y_pred = mode{ h1(X), h2(X), ..., hN(X) }", label="2.5")
    add_body_para(doc, "Cơ chế này triệt tiêu phương sai (variance) của các cây đơn lẻ, giảm hiện tượng quá khớp (overfitting) và tự động cung cấp thước đo mức độ quan trọng đặc trưng (Mean Decrease in Impurity).")
    
    add_heading3(doc, "2.5.4. XGBoost (Extreme Gradient Boosting)")
    add_body_para(doc, "XGBoost (Chen & Guestrin, 2016) là thuật toán Gradient Boosting hiện đại, tối ưu hóa hàm mất mát thông qua xấp xỉ Taylor bậc hai kết hợp chính quy hóa hàm mục tiêu:")
    add_formula_para(doc, "L = Σ l(yi, y_hat_i) + Σ [ γ * T + 0.5 * λ * ||w||^2 ]", label="2.6")
    add_body_para(doc, "Trong đó T là số nút lá, w là trọng số các lá, γ và λ là các hệ số phạt độ phức tạp của cây. Để thích ứng với dữ liệu mất cân bằng, tham số scale_pos_weight được cấu hình bằng tỷ lệ giữa số mẫu đa số và thiểu số (khoảng 3,52) nhằm tăng cường độ nhạy với lớp thiểu số.")
    
    # 2.6
    add_heading2(doc, "2.6. Phương pháp thực nghiệm xử lý Mất cân bằng dữ liệu (Class Imbalance Methods)")
    
    add_heading3(doc, "2.6.1. Phân tích lý thuyết tác động của mất cân bằng dữ liệu")
    add_body_para(doc, "Trong bài toán rủi ro tín dụng thẻ, tỷ lệ khách hàng vỡ nợ chiếm khoảng 22,12% (tỷ lệ mất cân bằng xấp xỉ 3,52:1). Tình trạng này dẫn đến hiện tượng 'Nghịch lý độ chính xác' (Accuracy Paradox): Một mô hình tầm thường luôn dự đoán tất cả khách hàng đều không vỡ nợ vẫn đạt Accuracy lên tới 77,88%, nhưng lại hoàn toàn vô giá trị trong việc phát hiện rủi ro (Recall của lớp vỡ nợ bằng 0).")
    
    add_heading3(doc, "2.6.2. Đề xuất áp dụng Class Weighting, Threshold Tuning và cơ chế kiểm soát SMOTE")
    add_bullet_item(doc, "Điều chỉnh ma trận hàm mất mát bằng cách gán trọng số lớn hơn cho lớp thiểu số theo công thức w_k = N / (K * N_k). Giải pháp này không làm thay đổi phân phối mẫu thực tế và hoàn toàn tương thích với Cross-Validation.", bold_prefix="Phương pháp gán trọng số (Class Weighting): ")
    add_bullet_item(doc, "Thay vì sử dụng ngưỡng xác suất mặc định 0,50, đề tài phân tích và tối ưu ngưỡng trên các dự báo Out-Of-Fold (OOF) trong quá trình Cross-Validation trên tập Train, bảo đảm không gây rò rỉ dữ liệu sang tập Test.", bold_prefix="Điều chỉnh ngưỡng quyết định (Threshold Tuning): ")
    add_bullet_item(doc, "Về mặt nguyên tắc lý thuyết, nếu áp dụng kỹ thuật tạo mẫu tổng hợp SMOTE, thuật toán bắt buộc chỉ được thực thi bên trong từng fold huấn luyện của Cross-Validation, tuyệt đối không áp dụng trên tập Test để tránh rò rỉ phân phối. Trong điều kiện môi trường thực nghiệm của đề tài, thư viện imbalanced-learn không được cài đặt sẵn, do đó đề tài tập trung khai thác chuyên sâu Class Weighting và Threshold Tuning làm phương án trọng tâm.", bold_prefix="Vị trí và nguyên tắc đối với SMOTE: ")
    
    # 2.7
    add_heading2(doc, "2.7. Phương pháp Đánh giá mô hình, Tối ưu hóa và Lựa chọn mô hình")
    
    add_heading3(doc, "2.7.1. Định nghĩa hệ thống chỉ số đánh giá đa chiều")
    add_body_para(doc, "Để đánh giá toàn diện mô hình trên dữ liệu mất cân bằng, hệ thống chỉ số được xây dựng dựa trên Ma trận nhầm lẫn (Confusion Matrix):")
    
    # Table 2.4: Confusion Matrix layout
    add_table_caption(doc, "Bảng 2.4: Ma trận nhầm lẫn chuẩn trong phân loại rủi ro tín dụng nhị phân")
    t_cm = doc.add_table(rows=3, cols=3)
    t_cm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_cm)
    col_w_cm = [Cm(5.0), Cm(5.5), Cm(5.5)]
    set_cell(t_cm.cell(0, 0), "Thực tế \\ Dự báo", bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
    set_cell(t_cm.cell(0, 1), "Dự báo: Vỡ nợ (1)", bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
    set_cell(t_cm.cell(0, 2), "Dự báo: Không vỡ nợ (0)", bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, fill_color="EAECEF")
    
    set_cell(t_cm.cell(1, 0), "Thực tế: Vỡ nợ (1)", bold=True, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_cell(t_cm.cell(1, 1), "True Positive (TP) — Bắt đúng rủi ro", bold=False, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell(t_cm.cell(1, 2), "False Negative (FN) — Bỏ sót rủi ro (Nguy hiểm)", bold=False, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    
    set_cell(t_cm.cell(2, 0), "Thực tế: Không vỡ nợ (0)", bold=True, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_cell(t_cm.cell(2, 1), "False Positive (FP) — Cảnh báo nhầm", bold=False, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell(t_cm.cell(2, 2), "True Negative (TN) — Xác nhận an toàn", bold=False, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    for r in range(3):
        for c in range(3):
            t_cm.cell(r, c).width = col_w_cm[c]
            
    add_body_para(doc, "Các chỉ số đánh giá cốt lõi bao gồm:")
    add_bullet_item(doc, "Accuracy = (TP + TN) / (TP + TN + FP + FN). Chỉ số phản ánh tỷ lệ dự đoán chính xác chung nhưng bị méo mó khi dữ liệu mất cân bằng.", bold_prefix="Độ chính xác tổng thể (Accuracy): ")
    add_bullet_item(doc, "Precision = TP / (TP + FP). Đo lường mức độ tin cậy khi mô hình phát tín hiệu cảnh báo vỡ nợ.", bold_prefix="Độ chuẩn xác (Precision): ")
    add_bullet_item(doc, "Recall = TP / (TP + FN). Đo lường tỷ lệ bắt trúng khách hàng vỡ nợ thực tế trong toàn bộ danh mục.", bold_prefix="Độ nhạy (Recall): ")
    add_bullet_item(doc, "F1-Score = 2 * (Precision * Recall) / (Precision + Recall). Trung bình điều hòa dung hòa giữa Precision và Recall.", bold_prefix="Điểm F1 tổng hợp (F1-Score): ")
    add_bullet_item(doc, "ROC-AUC đo diện tích dưới đường cong ROC (TPR vs FPR). PR-AUC (Precision-Recall AUC / Average Precision) đo diện tích dưới đường cong Precision-Recall. Trong dữ liệu mất cân bằng, PR-AUC là thước đo phản ánh khách quan và chính xác nhất chất lượng xếp hạng xác suất của mô hình đối với lớp thiểu số.", bold_prefix="Chỉ số đường cong (ROC-AUC và PR-AUC): ")
    
    add_heading3(doc, "2.7.2. Phương pháp phân tích Ma trận nhầm lẫn và đánh đổi nghiệp vụ")
    add_body_para(doc, "Trong nghiệp vụ ngân hàng, chi phí tài chính của hai loại lỗi phân loại là hoàn toàn bất đối xứng. Bỏ sót một khách hàng vỡ nợ (FN) dẫn đến tổn thất vốn gốc trực tiếp, trong khi từ chối nhầm một khách hàng an toàn (FP) chỉ gây ra chi phí cơ hội hoặc ảnh hưởng đến trải nghiệm khách hàng. Do đó, đề tài ưu tiên tối đa chỉ số Recall của lớp vỡ nợ và PR-AUC thay vì chỉ tối ưu Accuracy.", indent=True)
    
    add_heading3(doc, "2.7.3. Phương pháp Cross-Validation và Tối ưu siêu tham số")
    add_body_para(doc, "Quy trình kiểm thực chéo áp dụng StratifiedKFold với 5 phân lớp (5-fold) nhằm bảo đảm tỷ lệ mất cân bằng được phân bố đồng đều giữa các fold huấn luyện và xác thực. Phương pháp RandomizedSearchCV với 25 vòng lặp ngẫu nhiên (n_iter = 25) được lựa chọn để tìm kiếm tổ hợp siêu tham số tối ưu theo tiêu chí PR-AUC, cân đối giữa hiệu quả tối ưu và thời gian tính toán.", indent=True)
    
    add_heading3(doc, "2.7.4. Tiêu chí lựa chọn mô hình phù hợp nhất cho đề tài")
    add_body_para(doc, "Mô hình ứng cử viên cuối cùng được tuyển chọn dựa trên 5 tiêu chuẩn theo thứ tự ưu tiên: (1) PR-AUC trên tập Test cao nhất; (2) Điểm CV PR-AUC ổn định (độ lệch chuẩn thấp); (3) Recall lớp vỡ nợ vượt trội; (4) Điểm F1 cân bằng; (5) Tương thích với công cụ giải thích SHAP TreeExplainer.", indent=True)
    
    # 2.8
    add_heading2(doc, "2.8. Phương pháp giải thích mô hình với SHAP")
    
    add_heading3(doc, "2.8.1. Phương pháp phân tích đóng góp đặc trưng cấp tổng thể (Global Explanation)")
    add_body_para(doc, "SHAP (SHapley Additive exPlanations, Lundberg & Lee, 2017) là khung phương pháp giải thích mô hình học máy dựa trên lý thuyết trò chơi hợp tác. Dự báo của mô hình được biểu diễn dưới dạng tổng cộng tính của giá trị cơ sở (Base Value / Expected Value) và đóng góp của từng đặc trưng:")
    add_formula_para(doc, "f(x) = φ0 + Σ φi,  với φi là giá trị Shapley của đặc trưng thứ i", label="2.7")
    add_body_para(doc, "Đối với các mô hình dựa trên cấu trúc cây (XGBoost, Random Forest), thuật toán SHAP TreeExplainer tính toán chính xác giá trị Shapley trong thời gian đa thức O(TLD^2) thay vì xấp xỉ hàm mũ như KernelExplainer. Mức độ quan trọng toàn cục được tính bằng trung bình trị tuyệt đối Mean |SHAP Value| trên toàn bộ tập kiểm tra độc lập.", indent=True)
    
    add_heading3(doc, "2.8.2. Phương pháp phân tích đóng góp đặc trưng cấp cá thể (Local Explanation)")
    add_body_para(doc, "Ở cấp độ hồ sơ cá thể, biểu đồ thác nước (Waterfall Plot) trực quan hóa quá trình dịch chuyển xác suất từ mức kỳ vọng trung bình sang kết quả dự báo cụ thể của từng khách hàng. Mỗi đặc trưng làm tăng hoặc giảm log-odds vỡ nợ được thể hiện trực quan bằng các thanh mũi tên đỏ (tăng rủi ro) hoặc xanh (giảm rủi ro).", indent=True)
    add_body_para(doc, "Lưu ý phương pháp luận: Các giá trị SHAP của mô hình XGBoost được tính toán trên không gian log-odds (biên thô), sau đó ánh xạ qua hàm sigmoid sang xác suất. Đồng thời, các biểu đồ phụ thuộc (Dependence Plots) phản ánh mối quan hệ thống kê mô hình đã học được, không đồng nghĩa với quan hệ nhân quả (causality) trong kinh tế học.", indent=True)
    
    # 2.9
    add_heading2(doc, "2.9. Phân tích Yêu cầu và Thiết kế Kiến trúc ứng dụng Web Prototype")
    
    add_heading3(doc, "2.9.1. Đặc tả yêu cầu chức năng, phi chức năng và luồng xử lý hệ thống")
    add_body_para(doc, "Hệ thống Web Prototype được xây dựng nhằm mô phỏng một công cụ hỗ trợ ra quyết định tín dụng (Credit Decision Support System - DSS Prototype) phục vụ công tác thẩm định:")
    add_bullet_item(doc, "Biểu mẫu nhập liệu 23 trường thông tin khách hàng, tự động trích xuất 10 đặc trưng tài chính mới, chuẩn hóa dữ liệu qua RobustScaler, dự báo xác suất vỡ nợ, phân loại mức độ rủi ro (Thấp / Trung bình / Cao), và trực quan hóa Top 10 yếu tố SHAP tác động trực tiếp.", bold_prefix="Yêu cầu chức năng: ")
    add_bullet_item(doc, "Thời gian phản hồi suy luận dưới 3 giây; tính nhất quán tuyệt đối giữa môi trường huấn luyện và phục vụ (Training-Serving Consistency); giao diện trực quan, rõ ràng phục vụ trình diễn và nghiệm thu.", bold_prefix="Yêu cầu phi chức năng: ")
    add_bullet_item(doc, "Nhập liệu người dùng → Kiểm tra hợp lệ dữ liệu → Ánh xạ danh mục → Trích xuất 10 đặc trưng mới → RobustScaler.transform() → XGBoost.predict_proba() → So khớp ngưỡng 0,60 → Phân tầng rủi ro → Tính toán SHAP TreeExplainer thời gian thực → Trực quan hóa kết quả.", bold_prefix="Luồng xử lý tuần tự: ")
    
    add_heading3(doc, "2.9.2. Thiết kế kiến trúc phần mềm DSS Prototype và nguyên tắc phân loại rủi ro thử nghiệm")
    add_body_para(doc, "Kiến trúc hệ thống được phân tách thành hai tầng độc lập:", indent=True)
    add_bullet_item(doc, "Được xây dựng trên nền tảng framework Streamlit, chịu trách nhiệm tiếp nhận tương tác người dùng, hiển thị đồng hồ đo xác suất rủi ro (Plotly Gauge Chart) và biểu đồ phân tích SHAP tương tác.", bold_prefix="Tầng giao diện (Frontend - app.py): ")
    add_bullet_item(doc, "Module thuần Python độc lập, thực thi toàn bộ logic suy luận, nạp mô hình XGBoost và RobustScaler đã huấn luyện, thực thi Feature Engineering và giải thích SHAP mà không phụ thuộc vào giao diện đồ họa.", bold_prefix="Tầng xử lý logic suy luận (Backend - src/prediction.py): ")
    add_body_para(doc, "Cơ chế phân loại rủi ro thử nghiệm được định nghĩa dựa trên ngưỡng tối ưu 0,60: Nhóm Rủi ro Thấp (Xác suất < 30%), Nhóm Rủi ro Trung bình (Xác suất từ 30% đến 60%), và Nhóm Rủi ro Cao (Xác suất ≥ 60%, kích hoạt cảnh báo vỡ nợ).", indent=True)
    
    # Done chapter 2 content

def build_chapter_2():
    doc = Document()
    setup_page(doc)
    add_page_number(doc)
    
    # Header title
    title_p = doc.add_paragraph()
    set_para_format(title_p, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=2, line_spacing=1.3)
    r_sub = title_p.add_run("BÁO CÁO ĐỒ ÁN TỐT NGHIỆP\n")
    set_font(r_sub, size=12, bold=True, color=(100, 100, 100))
    
    add_chapter_2_content(doc)
    
    out_dir = r"F:\DATN\docs"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Chuong_2_Phuong_Phap_Thuc_Hien.docx")
    doc.save(out_path)
    print(f"SUCCESS: Saved Chuong 2 Word to {out_path}")
    return out_path

if __name__ == "__main__":
    build_chapter_2()
