
# -*- coding: utf-8 -*-
"""
Script tao file Word Bao cao DATN - Chuong 1
Sinh vien: Nguyen Trong The - MSSV: 1150080117
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

def set_font(run, font_name='Times New Roman', size=13, bold=False, italic=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    # Fix for Vietnamese font rendering
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
    pf.line_spacing = Pt(line_spacing * 13)  # 1.5 x 13pt
    if left_indent:
        pf.left_indent = Cm(left_indent)
    if first_line_indent:
        pf.first_line_indent = Cm(first_line_indent)

def add_heading1(doc, text):
    """Heading 1 - Tên chương"""
    para = doc.add_paragraph()
    run = para.add_run(text)
    set_font(run, size=14, bold=True)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before = Pt(12)
    pf.space_after = Pt(12)
    pf.line_spacing = Pt(21)
    # Apply Heading 1 style for TOC
    para.style = doc.styles['Heading 1']
    # Re-apply formatting after style
    for r in para.runs:
        set_font(r, size=14, bold=True)
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return para

def add_heading2(doc, text):
    """Heading 2 - Mục cấp 1"""
    para = doc.add_paragraph()
    para.style = doc.styles['Heading 2']
    run = para.add_run(text)
    set_font(run, size=13, bold=True)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(12)
    pf.space_after = Pt(6)
    pf.line_spacing = Pt(19.5)
    return para

def add_heading3(doc, text):
    """Heading 3 - Mục cấp 2"""
    para = doc.add_paragraph()
    para.style = doc.styles['Heading 3']
    run = para.add_run(text)
    set_font(run, size=13, bold=True)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(6)
    pf.space_after = Pt(3)
    pf.line_spacing = Pt(19.5)
    return para

def add_body_para(doc, text, indent=True):
    """Đoạn văn bản thân bài"""
    para = doc.add_paragraph()
    run = para.add_run(text)
    set_font(run, size=13)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)
    pf.line_spacing = Pt(19.5)  # 1.5 x 13pt
    if indent:
        pf.first_line_indent = Cm(1.27)  # ~0.5 inch indent chuẩn
    return para

def add_formula_para(doc, text):
    """Đoạn công thức - căn giữa"""
    para = doc.add_paragraph()
    run = para.add_run(text)
    set_font(run, size=13, italic=False)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before = Pt(3)
    pf.space_after = Pt(3)
    pf.line_spacing = Pt(19.5)
    return para

def add_table_caption(doc, text):
    """Caption bảng"""
    para = doc.add_paragraph()
    run = para.add_run(text)
    set_font(run, size=13, bold=True)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before = Pt(6)
    pf.space_after = Pt(3)
    pf.line_spacing = Pt(19.5)
    return para

def set_cell_font(cell, text, bold=False, size=11, wrap=True):
    cell.text = ''
    para = cell.paragraphs[0]
    run = para.add_run(text)
    set_font(run, size=size, bold=bold)
    para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    para.paragraph_format.space_before = Pt(2)
    para.paragraph_format.space_after = Pt(2)
    para.paragraph_format.line_spacing = Pt(14)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP

def set_table_borders(table):
    """Thêm viền bảng"""
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '6')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), '000000')
        tblBorders.append(border)
    tblPr.append(tblBorders)

def shade_cell(cell, fill_color):
    """Tô màu nền cho cell"""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_color)
    tcPr.append(shd)

def add_page_number(doc):
    """Thêm số trang vào footer"""
    section = doc.sections[0]
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.clear()
    run = footer_para.add_run()
    set_font(run, size=12)
    footer_para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add page number field
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)

def setup_page(doc):
    """Cài đặt trang A4, lề chuẩn"""
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.left_margin = Cm(3.0)   # Lề trái 3cm
    section.right_margin = Cm(2.0)  # Lề phải 2cm
    section.top_margin = Cm(2.5)    # Lề trên 2.5cm
    section.bottom_margin = Cm(2.5) # Lề dưới 2.5cm

def add_toc(doc):
    """Thêm Mục lục tự động"""
    para = doc.add_paragraph()
    run = para.add_run('MỤC LỤC')
    set_font(run, size=14, bold=True)
    para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after = Pt(12)

    # Add TOC field
    para2 = doc.add_paragraph()
    run2 = para2.add_run()
    fldChar = OxmlElement('w:fldChar')
    fldChar.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'TOC \\o "1-3" \\h \\z \\u'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:t')
    fldChar3.text = 'Nhấn Ctrl+A rồi F9 để cập nhật mục lục.'
    fldChar4 = OxmlElement('w:fldChar')
    fldChar4.set(qn('w:fldCharType'), 'end')
    
    run2._r.append(fldChar)
    run2._r.append(instrText)
    run2._r.append(fldChar2)
    run2._r.append(fldChar3)
    run2._r.append(fldChar4)
    set_font(run2, size=12, italic=True)
    
    doc.add_page_break()

def create_chapter1():
    doc = Document()
    
    # Cài đặt trang
    setup_page(doc)
    
    # Cài đặt style mặc định
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    
    # Cài đặt header/footer
    section = doc.sections[0]
    header = section.header
    header_para = header.paragraphs[0]
    header_para.clear()
    run_h = header_para.add_run('Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng')
    set_font(run_h, size=10, italic=True)
    header_para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    add_page_number(doc)
    
    # === MỤC LỤC ===
    add_toc(doc)
    
    # ============================================================
    # CHƯƠNG 1
    # ============================================================
    add_heading1(doc, 'CHƯƠNG 1. TỔNG QUAN TÀI LIỆU VÀ CÁC CÔNG TRÌNH NGHIÊN CỨU LIÊN QUAN')
    
    add_body_para(doc,
        'Chương 1 trình bày nền tảng lý thuyết và tổng quan tài liệu của đề tài nghiên cứu. '
        'Trước tiên, các khái niệm cốt lõi về rủi ro tín dụng, chấm điểm tín dụng và những thách thức '
        'đặc thù trong bài toán dự báo vỡ nợ khách hàng cá nhân được làm rõ (Mục 1.1). '
        'Tiếp theo, chín công trình nghiên cứu tiêu biểu trong và ngoài nước được phân tích, '
        'đối chiếu nhằm xác định khoảng trống nghiên cứu và cơ sở khoa học cho hướng tiếp cận của đề tài (Mục 1.2). '
        'Mục 1.3 giới thiệu cơ sở lý thuyết của các thuật toán Machine Learning được lựa chọn. '
        'Mục 1.4 mô tả tập dữ liệu nghiên cứu. '
        'Mục 1.5 trình bày khái niệm và nguyên lý toán học của Explainable AI thông qua phương pháp SHAP.')
    
    # ============================================================
    # 1.1
    # ============================================================
    add_heading2(doc, '1.1. Tổng quan về rủi ro tín dụng và bài toán chấm điểm tín dụng')
    
    # 1.1.1
    add_heading3(doc, '1.1.1. Khái niệm rủi ro tín dụng (Credit Risk) và vỡ nợ (Default)')
    
    add_body_para(doc,
        'Trong hoạt động của các tổ chức tín dụng, rủi ro tín dụng (Credit Risk) được hiểu là khả năng '
        'tổn thất tài chính phát sinh khi người vay hoặc đối tác không thực hiện đầy đủ nghĩa vụ trả nợ '
        'theo thỏa thuận hợp đồng. Định nghĩa này được ghi nhận trong nhiều tài liệu quản trị rủi ro tài chính, '
        'trong đó Basel Committee on Banking Supervision (2000) xác định rủi ro tín dụng là nguy cơ mà '
        'một bên đối tác không thể hoàn trả các khoản nợ đã cam kết, dẫn đến tổn thất vốn cho tổ chức cho vay. '
        'Rủi ro tín dụng bao gồm ba thành phần chính: Xác suất vỡ nợ (Probability of Default - PD), '
        'Tổn thất khi vỡ nợ (Loss Given Default - LGD) và Dư nợ tại thời điểm vỡ nợ '
        '(Exposure at Default - EAD). Trong phạm vi đề tài này, PD được tập trung nghiên cứu dưới '
        'góc độ xác suất ước lượng từ mô hình học máy, không đồng nhất với PD theo chuẩn Basel '
        'của các tổ chức tín dụng chính thức (Yeh & Lien, 2009).')

    add_body_para(doc,
        'Vỡ nợ (Default) là trạng thái nghiệp vụ xảy ra khi người vay không thực hiện được nghĩa vụ '
        'thanh toán trong một khoảng thời gian nhất định. Trong nhiều khung nghiệp vụ quốc tế, thông lệ '
        'thường gặp là coi một khoản nợ bị phân loại là vỡ nợ khi quá hạn từ 90 ngày trở lên; tuy nhiên, '
        'ngưỡng cụ thể này có thể thay đổi tùy theo quy định của từng tổ chức, từng quốc gia và loại '
        'sản phẩm tín dụng. Trong tập dữ liệu nghiên cứu UCI Credit Card Clients được công bố bởi '
        'Yeh & Lien (2009), biến mục tiêu default.payment.next.month phản ánh việc khách hàng có '
        'bị vỡ nợ trong tháng kế tiếp hay không (nhận giá trị 0 hoặc 1), được thiết lập dựa trên '
        'chuẩn phân loại nội bộ của ngân hàng thương mại Đài Loan.')

    add_body_para(doc,
        'Cần phân biệt rõ hai khái niệm thường bị nhầm lẫn: rủi ro tín dụng (Credit Risk) và '
        'xác suất vỡ nợ (Probability of Default - PD). Rủi ro tín dụng là khái niệm rộng hơn, '
        'bao gồm toàn bộ nguy cơ tổn thất tài chính từ phía người vay, trong khi PD là một '
        'thước đo cụ thể, định lượng xác suất xảy ra sự kiện vỡ nợ trong một khoảng thời gian '
        'xác định. Trong bài toán phân loại nhị phân mà đề tài này theo đuổi, mô hình Machine '
        'Learning sẽ ước lượng xác suất vỡ nợ P(Y=1|X) cho mỗi khách hàng dựa trên bộ đặc trưng '
        'đầu vào X, từ đó hỗ trợ quá trình ra quyết định tín dụng.')

    add_body_para(doc,
        'Vai trò của dự báo khả năng vỡ nợ trong quản trị ngân hàng ngày càng trở nên thiết yếu. '
        'Một mô hình dự báo PD chính xác cho phép tổ chức tín dụng: (i) phân loại khách hàng theo '
        'mức độ rủi ro trước khi cấp tín dụng; (ii) trích lập dự phòng rủi ro phù hợp; '
        '(iii) tối ưu hóa danh mục cho vay và (iv) tuân thủ yêu cầu quản lý vốn theo các quy chuẩn '
        'hiện hành. Chính nhu cầu này là động lực thúc đẩy việc nghiên cứu và áp dụng các '
        'phương pháp học máy vào bài toán chấm điểm tín dụng.')

    # 1.1.2
    add_heading3(doc, '1.1.2. Vai trò của Chấm điểm tín dụng (Credit Scoring) trong quản trị rủi ro ngân hàng')
    
    add_body_para(doc,
        'Chấm điểm tín dụng (Credit Scoring) là hệ thống mô hình hóa định lượng nhằm chuyển đổi '
        'thông tin từ hồ sơ cá nhân, hạn mức tín dụng và lịch sử thanh toán của khách hàng thành '
        'một điểm số hoặc xác suất rủi ro có thể diễn giải được. Theo Thomas et al. (2002), '
        'Credit Scoring là tập hợp các kỹ thuật thống kê và học máy giúp phân loại khách hàng '
        'thành các nhóm rủi ro khác nhau, từ đó hỗ trợ quyết định cấp tín dụng một cách hệ thống.')
    
    add_body_para(doc,
        'Dữ liệu đầu vào của hệ thống chấm điểm tín dụng thường bao gồm: thông tin nhân khẩu học '
        '(tuổi, giới tính, trình độ học vấn, tình trạng hôn nhân), thông tin tài chính '
        '(hạn mức tín dụng, số dư nợ, số tiền hóa đơn hàng tháng, lịch sử thanh toán) '
        'và các chỉ số tổng hợp phản ánh hành vi tín dụng. Đầu ra của mô hình là điểm số '
        'hoặc xác suất rủi ro, là cơ sở để phân loại khách hàng theo các ngưỡng chấp nhận '
        'rủi ro đã được thiết lập.')
    
    add_body_para(doc,
        'Trong bối cảnh quản trị rủi ro ngân hàng, Credit Scoring đóng vai trò quan trọng ở '
        'nhiều khía cạnh. Thứ nhất, hệ thống này tự động hóa quá trình đánh giá, giảm đáng kể '
        'thời gian xử lý hồ sơ so với phương pháp thủ công dựa trên chuyên gia. '
        'Thứ hai, nó đảm bảo tính nhất quán trong ra quyết định - các khách hàng có hồ sơ '
        'tương tự sẽ nhận được đánh giá tương đồng, khắc phục sự thiên lệch chủ quan '
        'của thẩm định viên. Thứ ba, Credit Scoring cho phép phân tích đồng thời nhiều '
        'biến đầu vào, khai thác các mối quan hệ phức tạp mà con người khó nhận biết.')
    
    add_body_para(doc,
        'Tuy nhiên, Credit Scoring cũng có những giới hạn nhất định. Chất lượng dự báo phụ thuộc '
        'nhiều vào tính đại diện và chất lượng của dữ liệu huấn luyện. Khi cấu trúc hành vi '
        'khách hàng thay đổi theo thời gian (hiện tượng model drift), mô hình cần được cập nhật '
        'định kỳ. Ngoài ra, các mô hình phức tạp như Ensemble Learning hay Neural Network '
        'thường hoạt động như "hộp đen", gây khó khăn cho việc giải thích lý do từ chối '
        'một hồ sơ cụ thể - một yêu cầu pháp lý và nghiệp vụ thiết yếu. '
        'Liên hệ với bài toán của đề tài này: tập dữ liệu UCI Credit Card Clients '
        'được sử dụng để xây dựng mô hình chấm điểm tín dụng nhị phân, phân loại '
        'khách hàng thành hai nhóm: không vỡ nợ (y=0) và vỡ nợ trong kỳ tiếp theo (y=1).')

    # 1.1.3
    add_heading3(doc, '1.1.3. Thách thức trong dự báo rủi ro tín dụng cá nhân')
    
    add_body_para(doc,
        'Bài toán dự báo rủi ro tín dụng cá nhân mang nhiều đặc điểm phức tạp đặc thù, '
        'đòi hỏi quy trình phát triển mô hình phải được thiết kế cẩn thận. '
        'Dưới đây là các thách thức chính được nhận diện trong quá trình khảo sát tài liệu:')
    
    add_body_para(doc,
        '(1) Mất cân bằng dữ liệu (Class Imbalance): Trong dữ liệu tín dụng thực tế, '
        'tỷ lệ khách hàng vỡ nợ (lớp thiểu số) thường thấp hơn đáng kể so với khách hàng '
        'bình thường (lớp đa số). Trong tập dữ liệu UCI Credit Card Clients, tỷ lệ này '
        'xấp xỉ 22,12% vỡ nợ so với 77,88% không vỡ nợ (Yeh & Lien, 2009). '
        'Hiện tượng này khiến mô hình có xu hướng thiên về lớp đa số, dẫn đến Recall '
        'của lớp vỡ nợ thấp - tức là bỏ sót nhiều khách hàng có rủi ro thực sự.')

    add_body_para(doc,
        '(2) Quan hệ phi tuyến phức tạp: Mối quan hệ giữa các đặc trưng đầu vào và biến '
        'mục tiêu không nhất thiết là tuyến tính. Ví dụ, tác động của lịch sử chậm thanh toán '
        'đến xác suất vỡ nợ phụ thuộc vào tần suất, mức độ và bối cảnh của các lần chậm thanh '
        'toán đó. Các mô hình tuyến tính truyền thống như Logistic Regression có thể gặp '
        'hạn chế trong việc nắm bắt các tương tác đa chiều này.')

    add_body_para(doc,
        '(3) Dữ liệu lịch sử nhiều chiều: Bộ dữ liệu tín dụng thường chứa cả thông tin '
        'nhân khẩu học và chuỗi thời gian hành vi thanh toán nhiều tháng, tạo ra không gian '
        'đặc trưng có nhiều chiều. Việc lựa chọn đặc trưng phù hợp và phát hiện các đặc trưng '
        'tổng hợp có giá trị dự báo cao (Feature Engineering) đòi hỏi kiến thức nghiệp vụ '
        'kết hợp với kiểm chứng thực nghiệm.')

    add_body_para(doc,
        '(4) Rò rỉ dữ liệu (Data Leakage): Đây là nguy cơ nghiêm trọng trong xây dựng '
        'mô hình học máy, xảy ra khi thông tin từ tập kiểm tra (Test set) vô tình "rò rỉ" '
        'vào quá trình huấn luyện, dẫn đến kết quả đánh giá mô hình bị phóng đại. '
        'Các tình huống dễ phát sinh Data Leakage bao gồm: fit Scaler/Encoder trên toàn bộ '
        'dữ liệu trước khi chia Train/Test, hay áp dụng SMOTE trên dữ liệu trước khi tách '
        'tập Train và Test. Kiểm soát nghiêm ngặt Data Leakage là yêu cầu bắt buộc để '
        'đảm bảo kết quả đánh giá phản ánh đúng hiệu năng thực của mô hình.')

    add_body_para(doc,
        '(5) Kỹ thuật rút trích đặc trưng (Feature Engineering): Ngoài 23 biến gốc '
        'trong tập dữ liệu, việc tính toán các chỉ số tài chính tổng hợp như Tỷ lệ sử dụng '
        'hạn mức tín dụng (Credit Utilization Ratio), Tỷ lệ thanh toán trên số dư nợ '
        '(Payment Ratio) hay các xu hướng biến động hóa đơn có thể cải thiện đáng kể '
        'chất lượng dự báo. Tuy nhiên, bất kỳ phép tính nào sử dụng thống kê từ tập Test '
        'đều cần bị nghiêm cấm để tránh Data Leakage (Tripathi et al., 2020).')

    add_body_para(doc,
        '(6) Khả năng giải thích mô hình (Model Interpretability): Các mô hình Ensemble '
        'phức tạp như XGBoost hay Random Forest cho hiệu năng dự báo cao nhưng khó diễn '
        'giải cơ chế hoạt động. Trong lĩnh vực tài chính tín dụng, khả năng giải thích '
        'lý do từ chối hoặc chấp thuận một hồ sơ là yêu cầu nghiệp vụ và pháp lý thiết yếu, '
        'nhằm đảm bảo tính minh bạch và công bằng (Bussmann et al., 2021).')

    add_body_para(doc,
        '(7) Đánh đổi nghiệp vụ giữa False Positive và False Negative: '
        'Trong bài toán phát hiện vỡ nợ, hai loại lỗi phân loại có hậu quả khác nhau về mặt '
        'nghiệp vụ. False Negative (bỏ sót khách hàng thực sự vỡ nợ) dẫn đến tổn thất '
        'tài chính trực tiếp khi ngân hàng cấp tín dụng cho khách hàng rủi ro. '
        'False Positive (từ chối nhầm khách hàng lành mạnh) gây thiệt hại về cơ hội kinh doanh '
        'và ảnh hưởng đến trải nghiệm khách hàng. Việc điều chỉnh ngưỡng phân loại '
        '(Threshold Tuning) để cân bằng hai loại lỗi này theo ưu tiên nghiệp vụ là '
        'một thách thức thực tiễn quan trọng.')

    add_body_para(doc,
        '(8) Yêu cầu đánh giá bằng nhiều chỉ số: Chỉ dựa vào Accuracy để đánh giá mô hình '
        'trên dữ liệu mất cân bằng có thể gây hiểu nhầm - một mô hình luôn dự đoán "không vỡ nợ" '
        'đã đạt Accuracy ~77,88% mà không học được bất kỳ điều gì hữu ích. '
        'Do đó, cần sử dụng kết hợp Precision, Recall, F1-Score, ROC-AUC, PR-AUC '
        'và phân tích Confusion Matrix để có đánh giá toàn diện và khách quan về hiệu năng mô hình.')

    # ============================================================
    # 1.2
    # ============================================================
    add_heading2(doc, '1.2. Tổng quan các công trình nghiên cứu liên quan trong và ngoài nước')
    
    add_body_para(doc,
        'Nhằm xác định rõ cơ sở thực tiễn, tiến trình phát triển công nghệ và các khoảng trống '
        'nghiên cứu còn tồn tại, tác giả đã tiến hành khảo sát, phân tích chuyên sâu các công '
        'trình nghiên cứu khoa học tiêu biểu liên quan trực tiếp đến bài toán chấm điểm tín dụng '
        'và dự báo vỡ nợ thẻ tín dụng. Tổng cộng chín công trình được tổng hợp: năm công trình '
        'nước ngoài và bốn công trình trong nước, được lựa chọn dựa trên mức độ liên quan '
        'với đề tài, chất lượng công bố và tính đại diện về phương pháp.')

    # 1.2.1
    add_heading3(doc, '1.2.1. Các công trình nghiên cứu nước ngoài')

    # --- Công trình 1: Yeh & Lien 2009 ---
    para = doc.add_paragraph()
    run = para.add_run('a) Yeh & Lien (2009) - So sánh các kỹ thuật Khai phá Dữ liệu trong dự báo xác suất vỡ nợ khách hàng thẻ tín dụng')
    set_font(run, size=13, bold=True, italic=True)
    set_para_format(para, space_before=6, space_after=3, line_spacing=1.5, first_line_indent=0)
    
    add_body_para(doc,
        'I-Cheng Yeh và Che-hui Lien (2009) công bố công trình "The comparisons of data mining '
        'techniques for the predictive accuracy of probability of default of credit card clients" '
        'trên tạp chí Expert Systems with Applications (Elsevier), Vol. 36, Issue 2, tr. 2473-2480. '
        'Đây là một trong những nghiên cứu nền tảng và có ảnh hưởng sâu rộng nhất trong lĩnh vực '
        'dự báo rủi ro tín dụng thẻ tín dụng (Yeh & Lien, 2009).')

    add_body_para(doc,
        'Bối cảnh và dữ liệu: Nghiên cứu được thực hiện trong giai đoạn khủng hoảng tín dụng '
        'tại Đài Loan, sử dụng tập dữ liệu gồm 30.000 bản ghi khách hàng thẻ tín dụng thu thập '
        'tại một ngân hàng thương mại, với 23 biến dự báo bao gồm thông tin nhân khẩu học, '
        'hạn mức tín dụng, lịch sử trả nợ 6 tháng và số tiền hóa đơn/thanh toán. '
        'Tập dữ liệu này sau khi được công bố đã trở thành benchmark phổ biến nhất thế giới '
        'cho bài toán rủi ro tín dụng thẻ.')

    add_body_para(doc,
        'Phương pháp và kết quả: Các thuật toán được so sánh bao gồm Mạng Nơ-ron nhân tạo (ANN), '
        'Cây quyết định (Decision Trees), Naive Bayes, K-Nearest Neighbors (K-NN), '
        'Hồi quy Logistic và Discriminant Analysis. Kết quả cho thấy mạng ANN đạt hiệu năng tổng thể '
        'cao nhất với Accuracy ~81,7% và AUC ~0,78. Công trình khẳng định rằng các phương pháp '
        'khai phá dữ liệu vượt trội so với phương pháp thống kê truyền thống trong bài toán này.')

    add_body_para(doc,
        'Ưu điểm: Công trình có đóng góp kép: vừa cung cấp tập dữ liệu thực tế công khai quy mô '
        'lớn (30.000 mẫu) với cấu trúc đặc trưng tài chính phong phú, vừa tiến hành so sánh bài '
        'bản giữa các phương pháp học máy và phương pháp thống kê truyền thống, tạo chuẩn tham '
        'chiếu cho các nghiên cứu sau.')

    add_body_para(doc,
        'Hạn chế: Nghiên cứu chưa khảo sát các thuật toán Gradient Boosting hiện đại như XGBoost '
        'hay LightGBM. Công trình cũng chưa áp dụng các kỹ thuật xử lý mất cân bằng lớp '
        '(Class Imbalance) chuyên sâu. Mô hình Mạng Nơ-ron mang tính chất "hộp đen", '
        'thiếu phương pháp giải thích trực quan cho cán bộ tín dụng. Ngoài ra, '
        'nghiên cứu chưa phát triển phần mềm ứng dụng giao diện hỗ trợ ra quyết định.')

    add_body_para(doc,
        'Đóng góp đối với đề tài: Công trình đặt ra nhu cầu nâng cao hiệu năng bằng các thuật '
        'toán Ensemble tiên tiến (XGBoost, Random Forest), kết hợp xử lý mất cân bằng, '
        'giải thích mô hình bằng SHAP và phát triển Web Prototype. '
        'Đây cũng là nguồn dữ liệu gốc mà đề tài hiện tại sử dụng.')

    # --- Công trình 2: Ala'raj & Abbod 2016 ---
    para = doc.add_paragraph()
    run = para.add_run("b) Ala'raj & Abbod (2016) - Khung phân loại đồng thuận kết hợp trong chấm điểm tín dụng")
    set_font(run, size=13, bold=True, italic=True)
    set_para_format(para, space_before=6, space_after=3, line_spacing=1.5, first_line_indent=0)

    add_body_para(doc,
        "Suleiman Ala'raj và Maysam F. Abbod (2016) công bố công trình \"A new consensus "
        "classification framework for credit scoring\" trên tạp chí Knowledge-Based Systems "
        "(Elsevier), Vol. 92, tr. 83-95. Công trình đề xuất một khung phân loại đồng thuận "
        "(Consensus Framework) nhằm nâng cao độ chính xác dự báo trong bài toán chấm điểm "
        "tín dụng (Ala'raj & Abbod, 2016).")

    add_body_para(doc,
        'Bối cảnh và dữ liệu: Nghiên cứu sử dụng năm tập dữ liệu tín dụng quốc tế bao gồm '
        'German Credit, Australian Credit và UCI Credit Card Clients, '
        'nhằm đảm bảo tính tổng quát của khung phương pháp được đề xuất.')

    add_body_para(doc,
        'Phương pháp và kết quả: Khung đồng thuận kết hợp Ensemble Learning, '
        'Thuật toán di truyền (Genetic Algorithm) để lựa chọn đặc trưng, '
        'Support Vector Machines (SVM), Decision Tree và Logistic Regression. '
        'Kết quả cho thấy khung phân loại đồng thuận cải thiện chỉ số ROC-AUC đạt mức >0,80 '
        "trên tập UCI Credit Card, đồng thời giảm tỷ lệ phân loại sai khách hàng rủi ro.")

    add_body_para(doc,
        'Ưu điểm và hạn chế: Đóng góp quy trình kết hợp mô hình phân tầng khoa học, '
        'đánh giá trên nhiều tập dữ liệu đa dạng. Tuy nhiên, chi phí tính toán cực kỳ lớn; '
        'cấu trúc mô hình phức tạp khó triển khai thời gian thực; thiếu cơ chế giải thích '
        'Explainable AI cho người dùng nghiệp vụ. Đây là khoảng trống quan trọng mà '
        "đề tài hiện tại hướng đến bổ sung thông qua việc tích hợp SHAP (Ala'raj & Abbod, 2016).")

    # --- Công trình 3: Shen et al. 2019 ---
    para = doc.add_paragraph()
    run = para.add_run('c) Shen et al. (2019) - Mô hình Ensemble tối ưu bầy đàn trong chấm điểm tín dụng')
    set_font(run, size=13, bold=True, italic=True)
    set_para_format(para, space_before=6, space_after=3, line_spacing=1.5, first_line_indent=0)

    add_body_para(doc,
        'Fenyu Shen, Xiaoqian Zhao, Zhiwei Li, Kai Li và Gang Kou (2019) công bố công trình '
        '"A novel ensemble classification model based on neural networks and particle swarm '
        'optimization for credit scoring" trên tạp chí Applied Soft Computing (Elsevier), '
        'Vol. 84, Article 105742. Công trình đề xuất phương pháp tối ưu hóa trọng số mô hình '
        'Ensemble bằng thuật toán bầy đàn Particle Swarm Optimization (PSO) (Shen et al., 2019).')

    add_body_para(doc,
        'Bối cảnh và dữ liệu: Nghiên cứu hướng đến tối ưu hóa mô hình chấm điểm tín dụng '
        'cá nhân và cho vay ngang hàng (P2P Lending), sử dụng tập dữ liệu UCI Credit Card '
        'Clients và tập dữ liệu P2P Lending để kiểm chứng.')

    add_body_para(doc,
        'Phương pháp và kết quả: Kết hợp Neural Networks, Particle Swarm Optimization (PSO), '
        'Random Forest và XGBoost. Kết quả cải thiện rõ rệt F1-Score và ROC-AUC, '
        'vượt trội hơn các mô hình học máy đơn lẻ trong việc phát hiện khách hàng vỡ nợ. '
        'Phương pháp tối ưu siêu tham số tự động và hiệu quả, xử lý tốt các biến nhiễu.')

    add_body_para(doc,
        'Ưu điểm và hạn chế: Sự kết hợp giữa Neural Network và PSO tạo nên mô hình có độ '
        'phức tạp tính toán rất cao (mang đặc tính "hộp đen"); chưa phân tích đánh đổi chi phí '
        'nghiệp vụ False Positive/False Negative; thiếu tính giải thích được '
        '(Explainability), làm cho mô hình khó áp dụng thực tế tại ngân hàng '
        '(Shen et al., 2019). Điều này nhấn mạnh tầm quan trọng của Explainable AI '
        'mà đề tài hiện tại hướng đến.')

    # --- Công trình 4: Bussmann et al. 2021 ---
    para = doc.add_paragraph()
    run = para.add_run('d) Bussmann et al. (2021) - Ứng dụng Explainable AI (SHAP) trong Quản trị Rủi ro Tín dụng')
    set_font(run, size=13, bold=True, italic=True)
    set_para_format(para, space_before=6, space_after=3, line_spacing=1.5, first_line_indent=0)

    add_body_para(doc,
        'Niklas Bussmann, Paolo Giudici, Dimitri Marinelli và Jochen Papenbrock (2021) '
        'công bố công trình "Explainable AI in credit risk management" trên tạp chí '
        'Frontiers in Artificial Intelligence, Vol. 4, Article 670486. '
        'Đây là một trong những nghiên cứu đầu tiên hệ thống hóa việc ứng dụng SHAP '
        'trong quản trị rủi ro tín dụng theo các yêu cầu pháp lý (Bussmann et al., 2021).')

    add_body_para(doc,
        'Bối cảnh và dữ liệu: Nghiên cứu được thúc đẩy bởi yêu cầu minh bạch theo quy định '
        'ngân hàng Châu Âu (GDPR/Basel) khi ứng dụng AI trong đánh giá tín dụng doanh nghiệp '
        'và cá nhân. Dữ liệu sử dụng bao gồm dữ liệu tín dụng ngân hàng Châu Âu '
        'và tập dữ liệu UCI Credit Card Clients.')

    add_body_para(doc,
        'Phương pháp và kết quả: Ứng dụng phương pháp SHAP (SHapley Additive exPlanations) '
        'kết hợp với XGBoost và Random Forest, bổ sung Shapley Lorenz Curves để trực quan hóa. '
        'Kết quả chứng minh SHAP giúp minh bạch hóa cơ chế hoạt động của mô hình XGBoost '
        'mà không làm giảm độ chính xác dự báo; đo lường chính xác mức độ đóng góp của '
        'từng thuộc tính ở cả cấp độ cá nhân và tổng thể.')

    add_body_para(doc,
        'Ưu điểm và hạn chế: Góp phần giảm thiểu rào cản "hộp đen" của các mô hình '
        'Machine Learning phức tạp trong quản trị rủi ro tài chính. Tuy nhiên, '
        'nghiên cứu tập trung vào mặt lý thuyết và phương pháp luận, '
        'chưa đóng gói mô hình và giao diện giải thích thành ứng dụng phần mềm Web tương tác '
        '(Bussmann et al., 2021). Đây chính là hướng mà đề tài hiện tại kế thừa '
        'để xây dựng giao diện ứng dụng hỗ trợ ra quyết định (Decision Support System Prototype).')

    # --- Công trình 5: Tripathi et al. 2020 ---
    para = doc.add_paragraph()
    run = para.add_run('e) Tripathi et al. (2020) - Mô hình chấm điểm tín dụng kết hợp Lọc đặc trưng và Ensemble Learning')
    set_font(run, size=13, bold=True, italic=True)
    set_para_format(para, space_before=6, space_after=3, line_spacing=1.5, first_line_indent=0)

    add_body_para(doc,
        'Deepak Tripathi, Damodar Reddy Edla và Venkatanareshbabu Kupagal (2020) công bố '
        'công trình "Credit scoring model using hybrid feature selection and ensemble learning '
        'techniques" trên tạp chí Computational Intelligence (Wiley), Vol. 36, Issue 3, '
        'tr. 1073-1094. Công trình đề xuất phương pháp trích lọc đặc trưng lai '
        '(Hybrid Feature Selection) kết hợp Ensemble Learning (Tripathi et al., 2020).')

    add_body_para(doc,
        'Bối cảnh và dữ liệu: Bài toán chấm điểm tín dụng cá nhân và lọc đặc trưng dư thừa, '
        'sử dụng German Credit, Australian Credit và UCI Credit Card làm tập dữ liệu kiểm thử.')

    add_body_para(doc,
        'Phương pháp và kết quả: Kết hợp Chi-square và Information Gain để lọc đặc trưng, '
        'sau đó áp dụng Random Forest, XGBoost, Bagging và Boosting. '
        'Kết quả tăng chỉ số Precision và Recall, loại bỏ các đặc trưng dư thừa '
        'giúp giảm chi phí tính toán. Quy trình lọc đặc trưng bài bản, '
        'tối ưu hóa kích thước không gian đặc trưng.')

    add_body_para(doc,
        'Ưu điểm và hạn chế: Chưa phân tích kỹ nguy cơ Data Leakage trong quá trình '
        'trích rút đặc trưng; chưa có công cụ giải thích trực quan. '
        'Tồn tại này đặt ra yêu cầu kiểm soát nghiêm ngặt Data Leakage khi xây dựng '
        'và lọc các đặc trưng tài chính mới - một yêu cầu trọng tâm của đề tài hiện tại '
        '(Tripathi et al., 2020).')

    # 1.2.2
    add_heading3(doc, '1.2.2. Các công trình nghiên cứu trong nước (Việt Nam)')

    # --- Công trình 6 ---
    para = doc.add_paragraph()
    run = para.add_run('a) Nguyễn Thị Cẩm Nhung & Đinh Ngạn (2019) - Mô hình chấm điểm tín dụng cá nhân tại Ngân hàng Thương mại Việt Nam')
    set_font(run, size=13, bold=True, italic=True)
    set_para_format(para, space_before=6, space_after=3, line_spacing=1.5, first_line_indent=0)

    add_body_para(doc,
        'Nguyễn Thị Cẩm Nhung và Đinh Ngạn (2019) công bố công trình "Xây dựng mô hình chấm điểm '
        'tín dụng cá nhân tại Ngân hàng Thương mại Cổ phần Ngoại thương Việt Nam" '
        'trên Tạp chí Khoa học & Đào tạo Ngân hàng, Số 204, tr. 45-54. '
        'Đây là một trong những nghiên cứu tiêu biểu trong nước về ứng dụng mô hình định lượng '
        'vào phê duyệt tín dụng (Nguyễn Thị Cẩm Nhung & Đinh Ngạn, 2019).')

    add_body_para(doc,
        'Bối cảnh và dữ liệu: Đánh giá rủi ro vỡ nợ của khách hàng vay tiêu dùng cá nhân '
        'tại Ngân hàng Thương mại Việt Nam (Vietcombank), sử dụng dữ liệu thực tế '
        '5.000 khoản vay cá nhân.')

    add_body_para(doc,
        'Phương pháp và kết quả: Áp dụng Hồi quy Logistic (Logistic Regression), '
        'biến đổi WoE (Weight of Evidence) và Chỉ số IV (Information Value) '
        'để xây dựng bảng điểm tín dụng (Scorecard). '
        'Kết quả đạt độ chính xác phân loại ~76%, xác định các biến thu nhập '
        'và lịch sử trả nợ có ảnh hưởng quyết định.')

    add_body_para(doc,
        'Ưu điểm và hạn chế: Tính thực tiễn cao, bám sát nghiệp vụ phê duyệt tín dụng '
        'tại ngân hàng Việt Nam. Tuy nhiên, chỉ áp dụng mô hình Logistic Regression tuyến tính '
        'truyền thống; chưa thử nghiệm các thuật toán Học máy hiện đại (Random Forest, XGBoost); '
        'chưa xử lý mất cân bằng lớp; chưa có công cụ giải thích trực quan. '
        'Công trình mở ra khoảng trống ứng dụng các thuật toán Machine Learning phi tuyến '
        'tiên tiến để so sánh hiệu năng với Logistic Regression '
        '(Nguyễn Thị Cẩm Nhung & Đinh Ngạn, 2019).')

    # --- Công trình 7 ---
    para = doc.add_paragraph()
    run = para.add_run('b) Lê Văn Thắng & Nguyễn Hoài Nam (2020) - Thuật toán học máy trong dự báo rủi ro vỡ nợ khách hàng cá nhân')
    set_font(run, size=13, bold=True, italic=True)
    set_para_format(para, space_before=6, space_after=3, line_spacing=1.5, first_line_indent=0)

    add_body_para(doc,
        'Lê Văn Thắng và Nguyễn Hoài Nam (2020) công bố công trình "Ứng dụng các thuật toán học máy '
        'trong dự báo rủi ro vỡ nợ của khách hàng cá nhân" trên Tạp chí Kinh tế và Phát triển, '
        'Số 278, tr. 32-41. Công trình bước đầu đưa các thuật toán Ensemble Learning '
        'vào bài toán tín dụng tại Việt Nam '
        '(Lê Văn Thắng & Nguyễn Hoài Nam, 2020).')

    add_body_para(doc,
        'Bối cảnh và dữ liệu: Dự báo rủi ro tín dụng thẻ và cho vay tiêu dùng tại các '
        'tổ chức tài chính Việt Nam, sử dụng dữ liệu thực nghiệm 10.000 khách hàng cá nhân.')

    add_body_para(doc,
        'Phương pháp và kết quả: So sánh Decision Tree, Random Forest, '
        'Support Vector Machines (SVM) và Logistic Regression. '
        'Mô hình Random Forest đạt Accuracy 82,3% và ROC-AUC 0,81, '
        'vượt trội so với Hồi quy Logistic truyền thống.')

    add_body_para(doc,
        'Ưu điểm và hạn chế: Bước đầu đưa Ensemble Learning vào bài toán tín dụng Việt Nam. '
        'Tuy nhiên, chưa thực hiện Feature Engineering chuyên sâu về tỷ lệ sử dụng hạn mức; '
        'chưa khảo sát thuật toán XGBoost; chưa có phần mềm prototype minh họa. '
        'Cần nghiên cứu bổ sung mô hình XGBoost, kỹ thuật trích rút đặc trưng nghiệp vụ '
        'và đóng gói giao diện thử nghiệm '
        '(Lê Văn Thắng & Nguyễn Hoài Nam, 2020).')

    # --- Công trình 8 ---
    para = doc.add_paragraph()
    run = para.add_run('c) Trần Thị Thanh Thủy (2021) - Khảo sát XGBoost và Random Forest trong đánh giá rủi ro tín dụng ngân hàng')
    set_font(run, size=13, bold=True, italic=True)
    set_para_format(para, space_before=6, space_after=3, line_spacing=1.5, first_line_indent=0)

    add_body_para(doc,
        'Trần Thị Thanh Thủy (2021) công bố công trình "Nghiên cứu ứng dụng thuật toán XGBoost '
        'và Random Forest trong đánh giá rủi ro tín dụng tại các ngân hàng thương mại Việt Nam" '
        'trên Tạp chí Ngân hàng (Ngân hàng Nhà nước Việt Nam), Số 15, tr. 18-25 '
        '(Trần Thị Thanh Thủy, 2021).')

    add_body_para(doc,
        'Bối cảnh và dữ liệu: Đánh giá rủi ro vỡ nợ khách hàng thẻ tín dụng và cho vay tiêu dùng, '
        'sử dụng tập dữ liệu tín dụng khách hàng cá nhân bao gồm tập UCI Credit Card '
        'và dữ liệu thực nghiệm tại Việt Nam.')

    add_body_para(doc,
        'Phương pháp và kết quả: So sánh Random Forest, XGBoost, áp dụng Cross-Validation '
        'và Grid Search Tuning. XGBoost đạt ROC-AUC 0,825, cải thiện đáng kể so với '
        'Random Forest và Logistic Regression; đề xuất quy trình chuẩn hóa dữ liệu tín dụng.')

    add_body_para(doc,
        'Ưu điểm và hạn chế: Đưa thuật toán XGBoost hiện đại vào nghiên cứu rủi ro tín dụng; '
        'quy trình tối ưu siêu tham số bài bản. Tuy nhiên, mô hình XGBoost vẫn coi như "hộp đen", '
        'chưa áp dụng Explainable AI (SHAP) để giải thích lý do dự báo cho cán bộ ngân hàng; '
        'chưa xây dựng Web prototype. Công trình thể hiện rõ nhu cầu bổ sung SHAP '
        'để minh bạch hóa mô hình XGBoost và phát triển prototype DSS '
        '(Trần Thị Thanh Thủy, 2021).')

    # --- Công trình 9 ---
    para = doc.add_paragraph()
    run = para.add_run('d) Phạm Long & Nguyễn Thị Hoàng Yến (2022) - Xử lý mất cân bằng dữ liệu trong chấm điểm tín dụng cá nhân')
    set_font(run, size=13, bold=True, italic=True)
    set_para_format(para, space_before=6, space_after=3, line_spacing=1.5, first_line_indent=0)

    add_body_para(doc,
        'Phạm Long và Nguyễn Thị Hoàng Yến (2022) công bố công trình "Đánh giá hiệu quả '
        'của các mô hình Học máy có giám sát trong chấm điểm tín dụng cá nhân" '
        'trên Tạp chí Nghiên cứu Kinh tế và Kinh doanh Châu Á (JABES - '
        'Trường ĐH Kinh tế TP.HCM), Số 33(4), tr. 55-70 '
        '(Phạm Long & Nguyễn Thị Hoàng Yến, 2022).')

    add_body_para(doc,
        'Bối cảnh và dữ liệu: Đánh giá khả năng trả nợ của khách hàng vay tiêu dùng cá nhân, '
        'sử dụng dữ liệu tín dụng cá nhân thực nghiệm tại Việt Nam (15.000 bản ghi).')

    add_body_para(doc,
        'Phương pháp và kết quả: Áp dụng Logistic Regression, Random Forest, XGBoost, '
        'SMOTE và Threshold Tuning. Áp dụng SMOTE giúp nâng chỉ số Recall của mô hình '
        'XGBoost từ 54% lên 72%, giảm rủi ro bỏ sót khách hàng vỡ nợ.')

    add_body_para(doc,
        'Ưu điểm và hạn chế: Đi sâu xử lý vấn đề mất cân bằng lớp (Class Imbalance) - '
        'đặc thù quan trọng của dữ liệu tín dụng. Tuy nhiên, chưa phân tích kỹ nguy cơ '
        'Data Leakage trong quá trình áp dụng SMOTE; chưa sử dụng thước đo PR-AUC; '
        'chưa đưa ra công cụ trực quan hóa giải thích. '
        'Tồn tại này đặt ra yêu cầu kiểm soát Data Leakage nghiêm ngặt khi áp dụng '
        'SMOTE/Class Weight và kết hợp với XAI (SHAP) '
        '(Phạm Long & Nguyễn Thị Hoàng Yến, 2022).')

    # 1.2.3 - Bảng so sánh
    add_heading3(doc, '1.2.3. Bảng so sánh và tổng hợp các công trình nghiên cứu')
    
    add_body_para(doc,
        'Để giúp Giảng viên và Hội đồng đánh giá có cái nhìn tổng quan, hệ thống về các '
        'nghiên cứu đã thực hiện, tác giả tổng hợp đặc điểm kỹ thuật của các công trình '
        'trong và ngoài nước trong Bảng 1.1 và Bảng 1.2 dưới đây:')

    # --- BẢNG 1.1 ---
    add_table_caption(doc, 'Bảng 1.1. Tổng hợp so sánh các công trình nghiên cứu ngoài nước tiêu biểu')

    headers1 = ['STT', 'Công trình', 'Năm', 'Tập dữ liệu', 'Phương pháp/\nMô hình ML', 'Xử lý\nImbalance', 'XAI/\nSHAP', 'Hạn chế chính', 'Đóng góp\ncho đề tài']
    col_widths1 = [Cm(0.7), Cm(2.8), Cm(0.8), Cm(2.5), Cm(3.0), Cm(1.3), Cm(1.0), Cm(2.5), Cm(2.5)]
    
    table1 = doc.add_table(rows=6, cols=9)
    table1.style = 'Table Grid'
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table1)
    
    for i, width in enumerate(col_widths1):
        for row in table1.rows:
            row.cells[i].width = width
    
    # Header row
    header_row = table1.rows[0]
    for i, h in enumerate(headers1):
        shade_cell(header_row.cells[i], 'D9D9D9')
        set_cell_font(header_row.cells[i], h, bold=True, size=10)
    
    # Data rows
    data1 = [
        ['1', 'Yeh & Lien\n(2009)', '2009', 'UCI Credit Card\n(30.000 bản ghi)', 'ANN, DT, NB, KNN,\nLogistic, Discriminant', 'Không', 'Không', 'Thiếu Ensemble\nhiện đại, không\ncó Explainability', 'Cung cấp dataset\nbenchmark; đặt\nnhu cầu XGBoost\nvà SHAP'],
        ['2', "Ala'raj &\nAbbod (2016)", '2016', 'German, Australian,\nUCI Credit Card', 'Ensemble,\nGenetic Algo,\nSVM, DT, LR', 'Không', 'Không', 'Chi phí tính toán\nlớn; thiếu giải\nthích nghiệp vụ', "Cần XAI để\nminh bạch hóa\nEnsemble model"],
        ['3', 'Shen et al.\n(2019)', '2019', 'UCI Credit Card,\nP2P Lending', 'Neural Networks,\nPSO, RF, XGBoost', 'Không rõ', 'Không', 'Hộp đen, thiếu\nExplainability;\nkhông phân tích\nFP/FN', 'Nhấn mạnh\ntầm quan trọng\ncủa XAI'],
        ['4', 'Bussmann\net al. (2021)', '2021', 'Dữ liệu ngân hàng\nChâu Âu,\nUCI Credit Card', 'XGBoost, RF,\nSHAP, Shapley\nLorenz Curves', 'Không rõ', 'Có\n(SHAP Global\n& Local)', 'Chưa đóng gói\nthành ứng dụng\nWeb tương tác', 'Định hướng kế\nthừa SHAP để\nxây dựng DSS\nPrototype'],
        ['5', 'Tripathi\net al. (2020)', '2020', 'German, Australian,\nUCI Credit Card', 'Chi-sq, Info Gain,\nRF, XGBoost,\nBagging, Boosting', 'Không rõ', 'Không', 'Chưa kiểm soát\nData Leakage;\nthiếu công cụ\ngiải thích', 'Yêu cầu kiểm\nsoát nghiêm\nngặt Leakage\nkhi Feature Eng.'],
    ]
    
    for i, row_data in enumerate(data1):
        row = table1.rows[i+1]
        for j, cell_text in enumerate(row_data):
            set_cell_font(row.cells[j], cell_text, size=9)
    
    doc.add_paragraph()  # Khoảng cách

    # --- BẢNG 1.2 ---
    add_table_caption(doc, 'Bảng 1.2. Tổng hợp so sánh các công trình nghiên cứu trong nước tiêu biểu')

    headers2 = ['STT', 'Công trình', 'Năm', 'Tập dữ liệu', 'Phương pháp/\nMô hình ML', 'Xử lý\nImbalance', 'XAI/\nSHAP', 'Hạn chế chính', 'Đóng góp\ncho đề tài']
    col_widths2 = col_widths1[:]
    
    table2 = doc.add_table(rows=5, cols=9)
    table2.style = 'Table Grid'
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table2)
    
    for i, width in enumerate(col_widths2):
        for row in table2.rows:
            row.cells[i].width = width
    
    header_row2 = table2.rows[0]
    for i, h in enumerate(headers2):
        shade_cell(header_row2.cells[i], 'D9D9D9')
        set_cell_font(header_row2.cells[i], h, bold=True, size=10)
    
    data2 = [
        ['6', 'Nguyễn T.C.\nNhung &\nĐinh Ngạn\n(2019)', '2019', 'Dữ liệu nội bộ\nVietcombank\n(5.000 khoản vay)', 'Logistic Reg.,\nWoE, IV', 'Không', 'Không', 'Chỉ dùng LR\ntuyến tính;\nchưa có\nEnsemble/XAI', 'Mở ra khoảng\ntrống ứng dụng\nML phi tuyến\ntại VN'],
        ['7', 'Lê V. Thắng\n& Nguyễn H.\nNam (2020)', '2020', 'Dữ liệu nội bộ\nVN (10.000\nkhách hàng)', 'DT, RF,\nSVM, LR', 'Không', 'Không', 'Chưa có\nXGBoost;\nthiếu Feature\nEng. chuyên sâu', 'Cần bổ sung\nXGBoost &\nFeature Eng.\nnghiệp vụ'],
        ['8', 'Trần T.T.\nThủy (2021)', '2021', 'UCI Credit Card\n+ dữ liệu thực\nnghiệm VN', 'RF, XGBoost,\nCross-Val,\nGrid Search', 'Không rõ', 'Không', 'XGBoost vẫn\nlà hộp đen;\nchưa có SHAP\nvà Web UI', 'Thể hiện rõ\nnhu cầu bổ\nsung SHAP\nvà DSS'],
        ['9', 'Phạm Long\n& Nguyễn T.\nH. Yến (2022)', '2022', 'Dữ liệu nội bộ\nVN (15.000\nbản ghi)', 'LR, RF, XGBoost,\nSMOTE,\nThreshold Tuning', 'Có (SMOTE,\nClass Weight)', 'Không', 'Chưa kiểm soát\nData Leakage\nkhi dùng SMOTE;\nchưa dùng PR-AUC', 'Yêu cầu kiểm\nsoát Leakage\nnghiêm ngặt\n+ tích hợp XAI'],
    ]
    
    for i, row_data in enumerate(data2):
        row = table2.rows[i+1]
        for j, cell_text in enumerate(row_data):
            set_cell_font(row.cells[j], cell_text, size=9)

    doc.add_paragraph()

    # 1.2.4
    add_heading3(doc, '1.2.4. Nhận xét tổng quan, khoảng trống nghiên cứu và lý do chọn đề tài')

    add_body_para(doc,
        'Từ việc phân tích, đối chiếu toàn diện chín công trình nghiên cứu tiêu biểu trong '
        'và ngoài nước ở trên, tác giả rút ra các nhận xét tổng hợp về mặt phương pháp luận '
        'và các khoảng trống nghiên cứu (Research Gaps) như sau:')

    add_body_para(doc,
        '(1) Về kiểm soát rò rỉ dữ liệu (Data Leakage): Trong phạm vi các công trình được '
        'khảo sát, một số nghiên cứu như Tripathi et al. (2020) và Phạm Long & '
        'Nguyễn Thị Hoàng Yến (2022), mặc dù đã áp dụng kỹ thuật tạo đặc trưng và cân bằng lớp, '
        'nhưng chưa phân tích hoặc nhấn mạnh chi tiết việc kiểm soát Data Leakage. '
        'Đề tài này thiết lập quy trình kiểm soát rò rỉ dữ liệu chặt chẽ: dữ liệu được chia '
        'thành tập Train và Test trước khi thực hiện các bước preprocessing có tham số học '
        'từ dữ liệu; Scaler/Encoder chỉ được fit trên tập Train và sau đó dùng để transform '
        'tập Test; kỹ thuật SMOTE (nếu áp dụng) chỉ được thực hiện trong tập Train '
        'hoặc trong Cross-Validation pipeline.')

    add_body_para(doc,
        '(2) Về phương pháp Machine Learning và đánh giá đa chỉ số: Qua các tài liệu được '
        'tổng hợp tại Việt Nam, nhiều nghiên cứu chủ yếu sử dụng Logistic Regression hoặc '
        'Random Forest đơn lẻ (Nguyễn Thị Cẩm Nhung & Đinh Ngạn, 2019; '
        'Lê Văn Thắng & Nguyễn Hoài Nam, 2020). Các nghiên cứu có sử dụng XGBoost '
        '(Trần Thị Thanh Thủy, 2021) thường tập trung đánh giá qua Accuracy hoặc ROC-AUC, '
        'chưa đi sâu phân tích đánh đổi nghiệp vụ giữa False Positive (từ chối nhầm khách hàng tốt) '
        'và False Negative (duyệt nhầm khách hàng vỡ nợ) thông qua ma trận nhầm lẫn '
        '(Confusion Matrix) và đường cong PR-AUC. Đề tài này áp dụng hệ thống đa chỉ số '
        'đánh giá nhằm khắc phục hạn chế trên.')

    add_body_para(doc,
        '(3) Về tính giải thích được của mô hình (Explainable AI - XAI): '
        'Qua các công trình được khảo sát, các nghiên cứu ứng dụng mô hình học máy phức tạp '
        '(Shen et al., 2019; Trần Thị Thanh Thủy, 2021) thường gặp rào cản "hộp đen", '
        'thiếu cơ chế giải thích minh bạch lý do dự báo cho cán bộ tín dụng. '
        'Mặc dù Bussmann et al. (2021) đã nghiên cứu ứng dụng SHAP trong quản trị rủi ro '
        'tín dụng, nghiên cứu này chủ yếu tập trung vào mặt lý thuyết và phương pháp luận '
        'mà chưa kết hợp đóng gói thành ứng dụng giao diện thử nghiệm. '
        'Đề tài hiện tại kế thừa phương pháp SHAP và tích hợp vào giao diện '
        'Web Prototype nhằm cụ thể hóa khả năng giải thích mô hình cho người dùng cuối.')

    add_body_para(doc,
        '(4) Về khả năng đóng gói ứng dụng (Software Prototype): '
        'Trong phạm vi khảo sát, phần lớn các công trình chủ yếu tập trung vào phân tích '
        'thực nghiệm trên môi trường Notebook. Trong phạm vi tài liệu tham khảo, '
        'ít có nghiên cứu kết hợp đóng gói mô hình Machine Learning cùng giao diện '
        'giải thích SHAP thành một ứng dụng Web hỗ trợ ra quyết định '
        '(Decision Support System - DSS Prototype) hoàn chỉnh phục vụ thử nghiệm minh họa '
        'cho người dùng cuối. Đề tài hiện tại đặt mục tiêu xây dựng DSS Prototype này.')

    add_body_para(doc,
        'Trên cơ sở phân tích trên, lý do thực hiện đề tài được xác định như sau: '
        'Trong phạm vi tài liệu tham khảo, Machine Learning thể hiện tiềm năng vượt trội '
        'trong bài toán đánh giá rủi ro tín dụng. Tuy nhiên, vẫn còn tồn tại các khoảng trống '
        'liên quan đến kiểm soát rò rỉ dữ liệu (Data Leakage), phân tích đánh đổi nghiệp vụ '
        '(False Positive vs False Negative), minh bạch hóa mô hình bằng SHAP '
        'và khả năng đóng gói thành phần mềm thử nghiệm. '
        'Đề tài này lựa chọn xây dựng một quy trình hoàn chỉnh kết hợp hài hòa từ: '
        'Kiểm duyệt dữ liệu (Data Audit) → Tiền xử lý chống Data Leakage → '
        'Kỹ thuật trích rút đặc trưng (Feature Engineering) → '
        'Huấn luyện & So sánh đa mô hình (Logistic Regression, Decision Tree, '
        'Random Forest, XGBoost) → Xử lý Class Imbalance & Threshold Tuning → '
        'Giải thích mô hình bằng SHAP → Đóng gói ứng dụng Web Prototype (Streamlit). '
        'Đề tài hướng tới mục tiêu cung cấp một giải pháp hỗ trợ ra quyết định '
        'mang tính thực tiễn, khoa học và minh bạch cho bài toán '
        'đánh giá rủi ro tín dụng khách hàng thẻ tín dụng.')

    # ============================================================
    # 1.3
    # ============================================================
    add_heading2(doc, '1.3. Tổng quan về Machine Learning trong bài toán chấm điểm tín dụng')

    add_heading3(doc, '1.3.1. Bài toán Phân loại nhị phân (Binary Classification)')
    
    add_body_para(doc,
        'Học máy có giám sát (Supervised Machine Learning) là phương pháp huấn luyện mô hình '
        'từ tập dữ liệu có nhãn, trong đó mỗi mẫu dữ liệu X đã được gắn nhãn phân loại y. '
        'Mục tiêu là học ánh xạ f: X → y sao cho mô hình có thể dự đoán nhãn '
        'cho các mẫu mới chưa gặp trong quá trình huấn luyện. '
        'Phân loại (Classification) là dạng bài toán học máy có giám sát '
        'trong đó biến đầu ra y nhận các giá trị rời rạc (lớp), '
        'phân biệt với bài toán hồi quy khi y là giá trị liên tục.')

    add_body_para(doc,
        'Phân loại nhị phân (Binary Classification) là trường hợp đặc biệt của bài toán '
        'phân loại khi biến mục tiêu y chỉ nhận hai giá trị phân biệt. '
        'Trong bài toán đánh giá rủi ro tín dụng của đề tài này, bài toán được '
        'hình thức hóa như sau:')

    add_formula_para(doc, 'y ∈ {0, 1}')
    
    para = doc.add_paragraph()
    run = para.add_run('Trong đó:')
    set_font(run, size=13)
    set_para_format(para, space_before=0, space_after=3, line_spacing=1.5, first_line_indent=1.27)
    
    add_formula_para(doc, 'y = 0:  Khách hàng không vỡ nợ trong kỳ tiếp theo')
    add_formula_para(doc, 'y = 1:  Khách hàng vỡ nợ trong kỳ tiếp theo')

    add_body_para(doc,
        'Đầu vào của mô hình là véc-tơ đặc trưng X = (x₁, x₂, ..., xₚ) biểu diễn '
        'thông tin nhân khẩu học, hạn mức tín dụng và lịch sử thanh toán của khách hàng. '
        'Mô hình học f(X) sẽ ước lượng xác suất P(Y=1|X) - tức là xác suất khách hàng '
        'sẽ vỡ nợ trong kỳ tiếp theo dựa trên hồ sơ hiện tại. '
        'Từ xác suất này, áp dụng ngưỡng phân loại (threshold) τ để phân loại: '
        'nếu P(Y=1|X) ≥ τ thì dự đoán y=1 (vỡ nợ), ngược lại dự đoán y=0.')

    # 1.3.2
    add_heading3(doc, '1.3.2. Mô hình Hồi quy Logistic (Logistic Regression - Baseline)')
    
    add_body_para(doc,
        'Hồi quy Logistic (Logistic Regression) là mô hình phân loại tuyến tính kinh điển, '
        'được sử dụng rộng rãi trong lĩnh vực tài chính tín dụng nhờ tính đơn giản, '
        'nhanh và dễ giải thích. Mặc dù có tên gọi là "hồi quy", đây thực chất là '
        'mô hình phân loại ước lượng xác suất thuộc một lớp nhất định.')

    add_body_para(doc,
        'Nguyên lý hoạt động: Mô hình tổ hợp tuyến tính các đặc trưng đầu vào thành '
        'giá trị z (log-odds), sau đó áp dụng hàm sigmoid để chuyển đổi z '
        'thành xác suất trong khoảng (0, 1):')

    add_formula_para(doc, 'z = β₀ + β₁X₁ + β₂X₂ + ... + βₚXₚ')
    add_formula_para(doc, 'P(Y = 1|X) = σ(z) = 1 / (1 + e^(−z))')
    
    para = doc.add_paragraph()
    run = para.add_run('Trong đó:')
    set_font(run, size=13)
    set_para_format(para, space_before=0, space_after=3, line_spacing=1.5, first_line_indent=1.27)
    
    add_body_para(doc,
        '- β₀ là hệ số chặn (bias/intercept);')
    add_body_para(doc,
        '- β₁, β₂, ..., βₚ là các hệ số hồi quy tương ứng với từng đặc trưng X₁, X₂, ..., Xₚ;')
    add_body_para(doc,
        '- σ(z) là hàm sigmoid (logistic function), có giá trị trong khoảng (0, 1), '
        'biểu thị xác suất ước lượng P(Y=1|X).')

    add_body_para(doc,
        'Vai trò Baseline: Trong quy trình phát triển mô hình học máy, '
        'Logistic Regression được sử dụng làm mô hình cơ sở (Baseline) để đối chiếu '
        'với các mô hình phức tạp hơn. Nếu một mô hình phức tạp không vượt trội '
        'đáng kể so với Logistic Regression, cần xem xét lại về tính hợp lý của '
        'việc tăng độ phức tạp.')

    add_body_para(doc,
        'Ưu điểm: (i) Dễ hiểu và dễ giải thích - hệ số β phản ánh trực tiếp tác động biên '
        'của từng đặc trưng đến log-odds; (ii) Tốc độ huấn luyện và dự đoán nhanh; '
        '(iii) Ổn định về mặt thống kê; (iv) Phù hợp khi quan hệ giữa đặc trưng '
        'và nhãn gần tuyến tính.')

    add_body_para(doc,
        'Hạn chế: (i) Giả định quan hệ tuyến tính giữa log-odds và đặc trưng, '
        'không nắm bắt tốt các mối quan hệ phi tuyến phức tạp; '
        '(ii) Nhạy cảm với các đặc trưng tương quan cao (multicollinearity); '
        '(iii) Hiệu năng thường thấp hơn các thuật toán Ensemble trên '
        'tập dữ liệu có cấu trúc phức tạp (Thomas et al., 2002).')

    # 1.3.3
    add_heading3(doc, '1.3.3. Mô hình Cây quyết định (Decision Tree Classifier)')
    
    add_body_para(doc,
        'Cây quyết định (Decision Tree) là mô hình học máy có giám sát có cấu trúc '
        'phân cấp dạng cây, hoạt động theo nguyên lý phân chia dữ liệu đệ quy '
        'dựa trên các điều kiện kiểm tra đặc trưng. Mô hình dễ trực quan hóa '
        'và có khả năng diễn giải cao, phù hợp với bài toán phân loại tín dụng.')

    add_body_para(doc,
        'Cấu trúc cây: Một Cây quyết định bao gồm ba loại thành phần chính: '
        '(i) Nút gốc (Root Node) - nút đầu tiên của cây, đại diện cho điều kiện '
        'phân chia toàn bộ tập dữ liệu; '
        '(ii) Nút nhánh (Internal Node) - mỗi nút nhánh kiểm tra một điều kiện '
        'trên một đặc trưng cụ thể và phân chia dữ liệu thành các tập con; '
        '(iii) Nút lá (Leaf Node) - nút cuối cùng, chứa nhãn phân loại được '
        'gán cho các mẫu dữ liệu đạt đến nút đó.')

    add_body_para(doc,
        'Tiêu chí phân chia: Tại mỗi nút, thuật toán chọn đặc trưng và ngưỡng '
        'phân chia tối ưu dựa trên các tiêu chí: Gini Impurity (đo mức độ hỗn tạp '
        'của một nút - giá trị nhỏ hơn nghĩa là nút thuần hơn) hoặc '
        'Information Gain/Entropy (đo lượng thông tin thu được khi biết giá trị '
        'của một đặc trưng). Mục tiêu là tìm phân chia giảm thiểu tối đa '
        'sự hỗn tạp của các tập con.')

    add_body_para(doc,
        'Ưu điểm: (i) Dễ giải thích và trực quan - có thể in ra cây để '
        'cán bộ tín dụng theo dõi luồng quyết định; '
        '(ii) Không yêu cầu chuẩn hóa dữ liệu đầu vào; '
        '(iii) Xử lý tốt cả đặc trưng số và đặc trưng phân loại; '
        '(iv) Học được các quan hệ phi tuyến thông qua cấu trúc phân cấp.')

    add_body_para(doc,
        'Hạn chế: Nhược điểm chính của Decision Tree đơn lẻ là hiện tượng overfit '
        '(học thuộc dữ liệu huấn luyện quá mức) khi cây có độ sâu lớn, '
        'dẫn đến hiệu năng kém trên dữ liệu mới. Cây cũng có thể rất nhạy cảm '
        'với nhiễu trong dữ liệu. Giới hạn này là động lực dẫn đến sự ra đời '
        'của các phương pháp Ensemble như Random Forest.')

    # 1.3.4
    add_heading3(doc, '1.3.4. Mô hình Rừng ngẫu nhiên (Random Forest Classifier)')
    
    add_body_para(doc,
        'Random Forest (Rừng ngẫu nhiên) là một thuật toán học máy Ensemble '
        'được đề xuất bởi Breiman (2001), xây dựng dựa trên ý tưởng kết hợp '
        'nhiều Cây quyết định độc lập để đưa ra dự đoán chung chính xác hơn. '
        'Phương pháp này thuộc nhóm Bagging (Bootstrap Aggregating) và '
        'là một trong những thuật toán Ensemble phổ biến nhất hiện nay.')

    add_body_para(doc,
        'Nguyên lý Bagging và Random Feature Selection: '
        'Quá trình xây dựng Random Forest gồm hai cơ chế đặc trưng: '
        '(i) Bagging - mỗi cây trong rừng được huấn luyện trên một tập dữ liệu '
        'bootstrap (lấy mẫu có hoàn lại từ tập huấn luyện gốc), '
        'tạo ra sự đa dạng giữa các cây; '
        '(ii) Random Feature Selection - tại mỗi nút phân chia, '
        'thay vì xem xét toàn bộ đặc trưng, thuật toán chỉ xét một tập con '
        'ngẫu nhiên của các đặc trưng (thường là √p với p là tổng số đặc trưng), '
        'giảm tương quan giữa các cây và tăng khả năng tổng quát hóa.')

    add_body_para(doc,
        'Cơ chế Voting: Sau khi huấn luyện N cây quyết định (N thường từ 100-1000), '
        'kết quả cuối cùng được tổng hợp bằng cơ chế bầu chọn đa số (Majority Voting): '
        'nhãn lớp được gán nhiều nhất bởi các cây đơn lẻ sẽ là dự đoán cuối cùng. '
        'Xác suất vỡ nợ được tính bằng tỷ lệ số cây dự đoán y=1 '
        'trên tổng số N cây trong rừng.')

    add_body_para(doc,
        'Ưu điểm: (i) Độ chính xác cao và ổn định, khắc phục hiện tượng overfit '
        'của Decision Tree đơn lẻ; (ii) Cung cấp Feature Importance - đo lường '
        'mức độ đóng góp của từng đặc trưng vào chất lượng dự báo; '
        '(iii) Xử lý tốt dữ liệu chiều cao và nhiễu; '
        '(iv) Kết quả ổn định theo các lần chạy khác nhau nhờ quá trình '
        'tổng hợp nhiều mô hình.')

    add_body_para(doc,
        'Hạn chế: (i) Chi phí tính toán và lưu trữ lớn khi số cây nhiều; '
        '(ii) Kết quả khó giải thích chi tiết hơn so với một cây đơn lẻ '
        '- đây là đặc tính "hộp trắng một phần" (semi-black box); '
        '(iii) Không phải lúc nào cũng vượt trội so với Gradient Boosting '
        'trên các bài toán tín dụng có dữ liệu có cấu trúc '
        '(Lê Văn Thắng & Nguyễn Hoài Nam, 2020).')

    # 1.3.5
    add_heading3(doc, '1.3.5. Mô hình XGBoost (Extreme Gradient Boosting)')
    
    add_body_para(doc,
        'XGBoost (Extreme Gradient Boosting) được phát triển bởi Chen & Guestrin (2016) '
        'và nhanh chóng trở thành thuật toán hàng đầu trong các cuộc thi Machine Learning '
        'cũng như ứng dụng thực tiễn trong lĩnh vực tài chính tín dụng '
        '(Chen & Guestrin, 2016). XGBoost thuộc nhóm Gradient Boosting - '
        'phương pháp Ensemble xây dựng các mô hình tuần tự, mỗi mô hình '
        'tập trung sửa các lỗi của mô hình trước đó.')

    add_body_para(doc,
        'Nguyên lý Gradient Boosting và xây dựng tuần tự: '
        'Không giống Bagging (xây dựng cây độc lập song song), '
        'Boosting xây dựng các cây tuần tự: cây thứ k được huấn luyện '
        'để giảm thiểu phần dư (residuals) hay đạo hàm của hàm mất mát '
        'so với tổng dự đoán của k-1 cây trước. '
        'Dự đoán cuối cùng là tổng có trọng số của tất cả các cây:')

    add_formula_para(doc, 'ŷᵢ = Σₖ fₖ(Xᵢ)')
    
    add_body_para(doc,
        'Trong đó fₖ là cây thứ k và tổng cộng K cây được xây dựng. '
        'XGBoost tối ưu hàm mục tiêu bao gồm cả hàm mất mát (Loss) '
        'và thành phần Regularization để kiểm soát độ phức tạp mô hình:')

    add_formula_para(doc, 'Obj = L(y, ŷ) + Ω(f)')

    add_body_para(doc,
        'Regularization: XGBoost tích hợp cả L1 (Lasso) và L2 (Ridge) regularization '
        'vào hàm mục tiêu, giúp kiểm soát mức độ phức tạp của từng cây '
        'và giảm thiểu overfit hiệu quả hơn các thuật toán Gradient Boosting '
        'truyền thống.')

    add_body_para(doc,
        'Ưu điểm: (i) Hiệu năng dự báo cao, thường vượt trội so với '
        'Random Forest trên dữ liệu tín dụng có cấu trúc '
        '(Trần Thị Thanh Thủy, 2021); '
        '(ii) Tích hợp sẵn cơ chế xử lý dữ liệu thiếu (missing values); '
        '(iii) Có tham số class_weight hỗ trợ xử lý mất cân bằng lớp; '
        '(iv) Tốc độ huấn luyện nhanh nhờ song song hóa tính toán; '
        '(v) Cung cấp Feature Importance dựa trên Gain và Coverage.')

    add_body_para(doc,
        'Hạn chế: (i) Cần tinh chỉnh nhiều siêu tham số (learning_rate, '
        'max_depth, n_estimators, subsample...); '
        '(ii) Bản thân mô hình XGBoost vẫn mang tính "hộp đen" - '
        'cần kết hợp với phương pháp XAI (như SHAP) để giải thích '
        'cơ chế dự báo cho người dùng nghiệp vụ; '
        '(iii) Dễ overfit nếu không kiểm soát số cây và regularization phù hợp '
        '(Chen & Guestrin, 2016).')

    add_body_para(doc,
        'Vai trò trong bài toán Credit Risk: XGBoost là thuật toán trọng tâm '
        'trong đề tài, được kỳ vọng sẽ đạt hiệu năng dự báo cao nhất so với '
        'các mô hình baseline. Khi kết hợp với SHAP, XGBoost không chỉ cho '
        'kết quả chính xác mà còn cung cấp giải thích chi tiết về '
        'yếu tố nào ảnh hưởng đến quyết định dự báo cho từng khách hàng cụ thể. '
        'Lưu ý: Kết quả thực nghiệm so sánh các mô hình sẽ được trình bày '
        'trong Chương 3 của khóa luận.')

    # ============================================================
    # 1.4
    # ============================================================
    add_heading2(doc, '1.4. Tập dữ liệu nghiên cứu UCI Credit Card Clients')

    add_heading3(doc, '1.4.1. Nguồn gốc và ý nghĩa tập dữ liệu nghiên cứu')
    
    add_body_para(doc,
        'Tập dữ liệu nghiên cứu được sử dụng trong đề tài là '
        '"Default of Credit Card Clients Dataset", '
        'do I-Cheng Yeh và Che-hui Lien thu thập và công bố gắn liền với '
        'công trình nghiên cứu của các tác giả trên tạp chí '
        'Expert Systems with Applications năm 2009 (Yeh & Lien, 2009). '
        'Tập dữ liệu được lưu trữ chính thức tại UCI Machine Learning Repository '
        'và cũng có thể truy cập qua bản sao (mirror) trên nền tảng Kaggle '
        '(UCI Machine Learning Repository, 2016). '
        'Cần phân biệt rõ: UCI Machine Learning Repository là nguồn học thuật gốc, '
        'còn Kaggle là nền tảng cộng đồng lưu trữ lại bộ dữ liệu này '
        'để thuận tiện cho việc tải về và thực nghiệm.')

    add_body_para(doc,
        'Bối cảnh thu thập dữ liệu: Tập dữ liệu được thu thập từ một ngân hàng thương mại '
        'tại Đài Loan trong giai đoạn tháng 4 đến tháng 9 năm 2005, '
        'phản ánh thông tin của 30.000 khách hàng thẻ tín dụng. '
        'Bối cảnh thu thập gắn liền với giai đoạn khủng hoảng tín dụng thẻ '
        'tại Đài Loan khi tỷ lệ vỡ nợ tăng cao, tạo nền dữ liệu thực tế '
        'có giá trị nghiên cứu cao.')

    add_body_para(doc,
        'Đặc điểm tổng quan: Tập dữ liệu bao gồm:')
    
    add_body_para(doc, '- Số lượng bản ghi: 30.000 khách hàng thẻ tín dụng;')
    add_body_para(doc, '- Số biến dự báo (đặc trưng): 23 biến;')
    add_body_para(doc, '- Biến mục tiêu: default.payment.next.month (0 = không vỡ nợ, 1 = vỡ nợ);')
    add_body_para(doc, '- Tỷ lệ vỡ nợ: khoảng 22,12% (6.636 khách hàng vỡ nợ).')

    add_body_para(doc,
        'Ý nghĩa nghiên cứu: Tập dữ liệu này được đánh giá cao trong cộng đồng nghiên cứu '
        'vì một số lý do: (i) Quy mô đủ lớn (30.000 mẫu) để huấn luyện và đánh giá '
        'các mô hình học máy một cách đáng tin cậy; '
        '(ii) Cấu trúc đặc trưng đa dạng bao gồm cả thông tin nhân khẩu học '
        'và chuỗi hành vi thanh toán theo thời gian; '
        '(iii) Tỷ lệ mất cân bằng lớp (22,12% vỡ nợ) phản ánh đặc thù thực tế '
        'của dữ liệu tín dụng; '
        '(iv) Được sử dụng làm benchmark trong nhiều nghiên cứu quốc tế '
        '(Ala\'raj & Abbod, 2016; Shen et al., 2019; Bussmann et al., 2021), '
        'tạo điều kiện so sánh kết quả giữa các công trình.')

    # 1.4.2
    add_heading3(doc, '1.4.2. Mô tả chi tiết các biến dự báo và biến mục tiêu')
    
    add_body_para(doc,
        'Các biến trong tập dữ liệu có thể phân thành năm nhóm chính '
        'như trình bày trong Bảng 1.3 dưới đây:')

    add_table_caption(doc, 'Bảng 1.3. Mô tả chi tiết các biến trong tập dữ liệu UCI Credit Card Clients')

    var_headers = ['Tên biến', 'Nhóm', 'Kiểu dữ liệu', 'Ý nghĩa']
    var_col_widths = [Cm(3.2), Cm(3.5), Cm(2.5), Cm(7.8)]
    
    var_data = [
        # Nhóm A
        ('ID', 'A. Thông tin cơ bản', 'Số nguyên', 'Mã định danh khách hàng (không dùng làm đặc trưng dự báo)'),
        ('LIMIT_BAL', 'A. Thông tin cơ bản', 'Số thực', 'Hạn mức tín dụng của khách hàng và gia đình (Đài Tệ)'),
        ('SEX', 'A. Thông tin cơ bản', 'Phân loại', 'Giới tính: 1 = Nam, 2 = Nữ'),
        ('EDUCATION', 'A. Thông tin cơ bản', 'Phân loại', 'Trình độ học vấn: 1 = Thạc sĩ trở lên, 2 = Đại học, 3 = THPT, 4 = Khác'),
        ('MARRIAGE', 'A. Thông tin cơ bản', 'Phân loại', 'Tình trạng hôn nhân: 1 = Đã kết hôn, 2 = Độc thân, 3 = Khác'),
        ('AGE', 'A. Thông tin cơ bản', 'Số nguyên', 'Tuổi của khách hàng (năm)'),
        # Nhóm B
        ('PAY_0', 'B. Lịch sử thanh toán', 'Số nguyên', 'Tình trạng thanh toán tháng 9/2005: -1=đúng hạn, 1=trễ 1 tháng, 2=trễ 2 tháng, ...'),
        ('PAY_2', 'B. Lịch sử thanh toán', 'Số nguyên', 'Tình trạng thanh toán tháng 8/2005'),
        ('PAY_3', 'B. Lịch sử thanh toán', 'Số nguyên', 'Tình trạng thanh toán tháng 7/2005'),
        ('PAY_4', 'B. Lịch sử thanh toán', 'Số nguyên', 'Tình trạng thanh toán tháng 6/2005'),
        ('PAY_5', 'B. Lịch sử thanh toán', 'Số nguyên', 'Tình trạng thanh toán tháng 5/2005'),
        ('PAY_6', 'B. Lịch sử thanh toán', 'Số nguyên', 'Tình trạng thanh toán tháng 4/2005'),
        # Nhóm C
        ('BILL_AMT1', 'C. Số tiền hóa đơn', 'Số thực', 'Số dư nợ hóa đơn tháng 9/2005 (Đài Tệ)'),
        ('BILL_AMT2', 'C. Số tiền hóa đơn', 'Số thực', 'Số dư nợ hóa đơn tháng 8/2005 (Đài Tệ)'),
        ('BILL_AMT3', 'C. Số tiền hóa đơn', 'Số thực', 'Số dư nợ hóa đơn tháng 7/2005 (Đài Tệ)'),
        ('BILL_AMT4', 'C. Số tiền hóa đơn', 'Số thực', 'Số dư nợ hóa đơn tháng 6/2005 (Đài Tệ)'),
        ('BILL_AMT5', 'C. Số tiền hóa đơn', 'Số thực', 'Số dư nợ hóa đơn tháng 5/2005 (Đài Tệ)'),
        ('BILL_AMT6', 'C. Số tiền hóa đơn', 'Số thực', 'Số dư nợ hóa đơn tháng 4/2005 (Đài Tệ)'),
        # Nhóm D
        ('PAY_AMT1', 'D. Số tiền thanh toán', 'Số thực', 'Số tiền đã thanh toán thực tế tháng 9/2005 (Đài Tệ)'),
        ('PAY_AMT2', 'D. Số tiền thanh toán', 'Số thực', 'Số tiền đã thanh toán thực tế tháng 8/2005 (Đài Tệ)'),
        ('PAY_AMT3', 'D. Số tiền thanh toán', 'Số thực', 'Số tiền đã thanh toán thực tế tháng 7/2005 (Đài Tệ)'),
        ('PAY_AMT4', 'D. Số tiền thanh toán', 'Số thực', 'Số tiền đã thanh toán thực tế tháng 6/2005 (Đài Tệ)'),
        ('PAY_AMT5', 'D. Số tiền thanh toán', 'Số thực', 'Số tiền đã thanh toán thực tế tháng 5/2005 (Đài Tệ)'),
        ('PAY_AMT6', 'D. Số tiền thanh toán', 'Số thực', 'Số tiền đã thanh toán thực tế tháng 4/2005 (Đài Tệ)'),
        # Nhóm E - Biến mục tiêu
        ('default.payment.\nnext.month', 'E. Biến mục tiêu', 'Nhị phân', 'Vỡ nợ trong tháng tiếp theo: 0 = Không vỡ nợ (~77,88%), 1 = Vỡ nợ (~22,12%)'),
    ]

    table3 = doc.add_table(rows=len(var_data)+1, cols=4)
    table3.style = 'Table Grid'
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table3)
    
    for i, width in enumerate(var_col_widths):
        for row in table3.rows:
            row.cells[i].width = width
    
    # Header
    header_row3 = table3.rows[0]
    for i, h in enumerate(var_headers):
        shade_cell(header_row3.cells[i], 'D9D9D9')
        set_cell_font(header_row3.cells[i], h, bold=True, size=10)
    
    # Data
    current_group = ''
    for i, (varname, group, dtype, meaning) in enumerate(var_data):
        row = table3.rows[i+1]
        # Tô màu nhóm xen kẽ
        fill = 'EBF3FB' if group.startswith('A') or group.startswith('C') or group.startswith('E') else 'FFFFFF'
        for cell in row.cells:
            shade_cell(cell, fill)
        set_cell_font(row.cells[0], varname, bold=True, size=9)
        set_cell_font(row.cells[1], group, size=9)
        set_cell_font(row.cells[2], dtype, size=9)
        set_cell_font(row.cells[3], meaning, size=9)

    doc.add_paragraph()

    # ============================================================
    # 1.5
    # ============================================================
    add_heading2(doc, '1.5. Trí tuệ nhân tạo có thể giải thích (Explainable AI) và phương pháp SHAP')

    add_heading3(doc, '1.5.1. Khái niệm và sự cần thiết của Explainable AI trong lĩnh vực tài chính')
    
    add_body_para(doc,
        'Trí tuệ nhân tạo có thể giải thích (Explainable Artificial Intelligence - XAI) '
        'là lĩnh vực nghiên cứu tập trung vào việc phát triển các phương pháp và công cụ '
        'giúp con người hiểu được cơ chế hoạt động và lý do ra quyết định của '
        'các mô hình Machine Learning. Thuật ngữ này xuất phát từ thực tế rằng '
        'nhiều mô hình học máy hiện đại - đặc biệt là các mô hình Ensemble, '
        'Neural Network hay Deep Learning - đạt hiệu năng dự báo cao nhưng '
        'hoạt động như "hộp đen" (black box): người dùng không thể quan sát '
        'hay lý giải được quá trình nội tại dẫn đến một kết quả cụ thể.')

    add_body_para(doc,
        'Tại sao mô hình Machine Learning có thể khó giải thích: '
        'Các mô hình phức tạp như XGBoost hay Random Forest đưa ra dự đoán '
        'thông qua hàng trăm hoặc hàng nghìn cây quyết định tương tác với nhau. '
        'Không có một quy tắc đơn giản nào mô tả chính xác tại sao '
        'một tổ hợp giá trị đặc trưng cụ thể lại dẫn đến xác suất vỡ nợ cao hay thấp. '
        'Điều này tạo ra khoảng cách giữa hiệu năng dự báo và '
        'khả năng diễn giải kết quả.')

    add_body_para(doc,
        'Tầm quan trọng của XAI trong lĩnh vực tín dụng: '
        'Trong lĩnh vực tài chính tín dụng, khả năng giải thích mô hình '
        'không chỉ là yêu cầu kỹ thuật mà còn là yêu cầu pháp lý và đạo đức. '
        'Thứ nhất, tính minh bạch (Transparency): các quy định tài chính '
        'ở nhiều quốc gia yêu cầu tổ chức tín dụng phải giải thích được '
        'lý do từ chối hồ sơ vay cho khách hàng. '
        'Thứ hai, khả năng kiểm tra và kiểm toán (Auditability): '
        'hội đồng quản trị rủi ro và cơ quan quản lý cần kiểm tra được '
        'mô hình có hoạt động công bằng và không phân biệt đối xử. '
        'Thứ ba, hỗ trợ cán bộ và người sử dụng: '
        'thay vì chỉ nhận "xác suất vỡ nợ = 0,73", '
        'cán bộ tín dụng cần biết yếu tố nào đang làm tăng '
        'hay giảm rủi ro của khách hàng cụ thể '
        '(Bussmann et al., 2021).')

    add_body_para(doc,
        'Giới hạn của việc giải thích mô hình: '
        'Cần lưu ý rằng XAI không biến mô hình "hộp đen" thành "hộp trắng" hoàn toàn. '
        'Các phương pháp XAI như SHAP cung cấp xấp xỉ về đóng góp của từng đặc trưng, '
        'không phải mô tả chính xác cơ chế nội tại. '
        'Ngoài ra, kết quả giải thích cần được diễn giải trong bối cảnh '
        'kiến thức nghiệp vụ của người dùng - không nên đọc kết quả SHAP '
        'như các mệnh đề nhân-quả tuyệt đối.')

    # 1.5.2
    add_heading3(doc, '1.5.2. Nguyên lý toán học Shapley Values và kỹ thuật SHAP (Global & Local Explanations)')
    
    add_body_para(doc,
        'Phương pháp SHAP (SHapley Additive exPlanations) được giới thiệu bởi '
        'Lundberg & Lee (2017) như một phương pháp thống nhất để giải thích '
        'dự đoán của các mô hình Machine Learning, dựa trên nền tảng toán học '
        'của Shapley Values từ lý thuyết trò chơi hợp tác '
        '(Lundberg & Lee, 2017).')

    add_body_para(doc,
        'Shapley Values - Ý tưởng phân bổ đóng góp: '
        'Trong lý thuyết trò chơi, Shapley Value giải quyết bài toán phân bổ '
        'phần thưởng công bằng cho các "người chơi" (features) trong một trò chơi hợp tác '
        '(tập mô hình). Áp dụng vào Machine Learning: '
        'với mỗi đặc trưng i trong tập đặc trưng N, '
        'SHAP giá trị φᵢ của đặc trưng i được tính là '
        'đóng góp trung bình có trọng số của đặc trưng i '
        'khi thêm vào tất cả các tập con có thể của các đặc trưng còn lại:')

    add_formula_para(doc, 'φᵢ = Σ_{S ⊆ N\\{i}}  [|S|! (|N| − |S| − 1)! / |N|!] × [f(S ∪ {i}) − f(S)]')
    
    para = doc.add_paragraph()
    run = para.add_run('Trong đó:')
    set_font(run, size=13)
    set_para_format(para, space_before=0, space_after=3, line_spacing=1.5, first_line_indent=1.27)
    
    add_body_para(doc, '- S là một tập con của các đặc trưng không chứa đặc trưng i;')
    add_body_para(doc, '- N là tập tất cả các đặc trưng;')
    add_body_para(doc, '- f(S) là giá trị dự đoán của mô hình khi chỉ sử dụng tập đặc trưng S;')
    add_body_para(doc, '- f(S ∪ {i}) − f(S) là phần đóng góp cận biên của đặc trưng i khi thêm vào tập S;')
    add_body_para(doc, '- Tổng được lấy trung bình theo trọng số trên tất cả các tập con S có thể.')

    add_body_para(doc,
        'Shapley Values thỏa mãn các tính chất toán học quan trọng: '
        'Hiệu quả (Efficiency) - tổng tất cả SHAP values bằng độ lệch '
        'giữa dự đoán cụ thể và dự đoán trung bình; '
        'Đối xứng (Symmetry) - hai đặc trưng đóng góp như nhau sẽ nhận SHAP value bằng nhau; '
        'Giả tưởng (Dummy) - đặc trưng không ảnh hưởng đến mô hình nhận SHAP value bằng 0; '
        'Cộng tính (Additivity) - SHAP values có thể cộng lại từ các mô hình đơn giản.')

    add_body_para(doc,
        'SHAP - Triển khai thực tiễn: '
        'Lundberg & Lee (2017) đề xuất SHAP như một phương pháp giải thích cộng tính '
        '(Additive Feature Attribution): dự đoán của mô hình cho mẫu x '
        'được phân tích thành:')

    add_formula_para(doc, 'f(x) = φ₀ + Σᵢ φᵢ')
    
    add_body_para(doc,
        'Trong đó φ₀ là giá trị dự đoán cơ sở (base value - dự đoán trung bình trên tập dữ liệu) '
        'và φᵢ là đóng góp của đặc trưng i vào dự đoán cụ thể cho mẫu x. '
        'Giá trị φᵢ dương nghĩa là đặc trưng i đẩy dự đoán lên cao hơn '
        'mức trung bình (tăng xác suất vỡ nợ), '
        'φᵢ âm nghĩa là đặc trưng i kéo dự đoán xuống thấp hơn '
        '(giảm xác suất vỡ nợ).')

    add_body_para(doc,
        'Global Explanation - Giải thích tổng thể: '
        'SHAP Global Explanation tổng hợp SHAP values trên toàn bộ tập dữ liệu '
        'để đánh giá mức độ đóng góp trung bình của từng đặc trưng '
        'vào khả năng dự báo của mô hình. '
        'Các trực quan hóa thường dùng bao gồm: '
        'SHAP Summary Plot (beeswarm) thể hiện phân phối SHAP values của từng đặc trưng; '
        'SHAP Feature Importance Plot xếp hạng các đặc trưng theo '
        'giá trị |φᵢ| trung bình trên toàn tập. '
        'Kết quả Global Explanation giúp xác định đặc trưng nào '
        'quan trọng nhất cho mô hình trong bối cảnh đánh giá rủi ro tín dụng.')

    add_body_para(doc,
        'Local Explanation - Giải thích cá thể: '
        'SHAP Local Explanation phân tích đóng góp của từng đặc trưng '
        'cho một dự đoán cụ thể của một khách hàng cụ thể. '
        'Các trực quan hóa thường dùng bao gồm: '
        'Force Plot thể hiện trực quan các đặc trưng đẩy dự đoán '
        'lên (màu đỏ) hoặc xuống (màu xanh) so với base value; '
        'Waterfall Plot cho thấy từng bước đóng góp lũy tích của '
        'các đặc trưng từ base value đến dự đoán cuối cùng. '
        'Kết quả Local Explanation có thể được cán bộ tín dụng sử dụng '
        'để giải thích lý do phân loại rủi ro cho từng khách hàng cụ thể, '
        'đáp ứng yêu cầu minh bạch trong hoạt động tín dụng '
        '(Bussmann et al., 2021).')

    add_body_para(doc,
        'Lưu ý: Việc ứng dụng SHAP trong thực nghiệm, bao gồm các biểu đồ '
        'SHAP thực tế và phân tích kết quả Global/Local Explanation '
        'của mô hình được lựa chọn, sẽ được trình bày chi tiết trong Chương 3 '
        'của khóa luận sau khi hoàn thành giai đoạn thực nghiệm.')

    # ============================================================
    # TÀI LIỆU THAM KHẢO
    # ============================================================
    doc.add_page_break()
    
    para = doc.add_paragraph()
    run = para.add_run('TÀI LIỆU THAM KHẢO')
    set_font(run, size=14, bold=True)
    para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after = Pt(12)

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
        "13. Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients. Expert Systems with Applications, 36(2), 2473–2480. https://doi.org/10.1016/j.eswa.2007.12.020",
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

    # Lưu file
    output_path = r'F:\DATN\project\reports\Bao_Cao_DATN_NguyenTrongThe_Chuong1.docx'
    doc.save(output_path)
    print(f"[OK] File da duoc luu tai: {output_path}")
    return output_path

if __name__ == '__main__':
    path = create_chapter1()
    print(f"[OK] Hoan thanh! File Word: {path}")
