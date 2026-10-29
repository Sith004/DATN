# BÁO CÁO KIỂM TRA VÀ ĐÁNH GIÁ TRƯỚC KHI COMMIT (PRE-COMMIT AUDIT)
**Đề tài**: Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  
**Sinh viên thực hiện**: Nguyễn Trọng Thể — MSSV: 1150080117  
**Thời gian kiểm tra**: 2026-10-29  
**Mục tiêu**: Kiểm tra, chuẩn hóa và bảo đảm an toàn trước khi khởi tạo/đồng bộ dự án lên GitHub `https://github.com/Sith004/DATN.git`

---

## 1. Xác thực Repository và Trạng thái Git Local / Remote

| Tiêu chí | Kết quả kiểm tra | Chi tiết / Bằng chứng |
| :--- | :--- | :--- |
| **Thư mục dự án** | `F:\DATN\project` | Đúng thư mục mã nguồn chính của đồ án. |
| **Trạng thái Git Local** | **CHƯA PHẢI GIT REPO** | Lệnh `git status` trả về: `fatal: not a git repository (or any of the parent directories): .git`. |
| **Remote đích** | `https://github.com/Sith004/DATN.git` | Đã kiểm tra qua `git ls-remote`: Remote phản hồi mã 0, hiện là **kho lưu trữ trống (empty repository)**. |
| **Công cụ Git** | `git version 2.55.0.windows.3`<br>`git-lfs/3.7.1` | Git và Git LFS đã được cài đặt sẵn trên máy Windows. |
| **Cấu hình định danh Git** | **Chưa có cấu hình** | Chưa có file `C:/Users/theng/.gitconfig`. Chưa cấu hình `user.name` và `user.email`. |

> [!WARNING]
> **ĐIỂM DỪNG BẮT BUỘC THEO NGUYÊN TẮC 2.1**: Thư mục hiện tại chưa được khởi tạo Git (`.git` không tồn tại). Theo nguyên tắc an toàn, hệ thống dừng lại để báo cáo và xin xác nhận của người dùng trước khi thực thi `git init`.

---

## 2. Kiểm tra An toàn và Bảo mật (Security & Secrets Audit)

| Thành phần | Phát hiện | Trạng thái bảo mật | Hành động xử lý |
| :--- | :--- | :--- | :--- |
| **File `.env`** | Chứa các biến `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`. | **ĐÃ BẢO VỆ** | File `.env` đã có trong `.gitignore`, không bị đưa lên Git. |
| **File `.env.example`** | Chưa có. | **CẦN BỔ SUNG** | Cần tạo `.env.example` chứa các placeholder mẫu (không chứa mật khẩu thật) để hỗ trợ môi trường khác triển khai. |
| **Mã nguồn kết nối DB (`src/database.py`)** | Sử dụng `os.getenv` hoàn toàn, parameterized queries chống SQL Injection. | **AN TOÀN** | Không có thông tin đăng nhập hardcode trong mã nguồn. |
| **Launcher (`Chay_Do_An.bat`)** | Thiết lập SSH tunnel tới Ubuntu IP `192.168.100.34`. | **AN TOÀN** | Không có mật khẩu hardcode. |
| **Chứng chỉ / Khóa bảo mật** | Các file `.pem`, `.key` trong `.venv/`. | **AN TOÀN** | Chỉ nằm trong `.venv` và đã được loại trừ khỏi Git qua `.gitignore`. |
| **Dữ liệu nhạy cảm / DB dump** | UCI Credit Card Dataset (dữ liệu học thuật công khai). Không có file dump `.sql` khách hàng thực tế. | **AN TOÀN** | Đáp ứng tiêu chuẩn phân phối học thuật. |

---

## 3. Kiểm tra Kích thước File và Artifacts (Large Files Audit)

GitHub có chính sách giới hạn kích thước file nghiêm ngặt:
- Cảnh báo đối với file > **50 MB**.
- **Chặn hoàn toàn (Push Rejection)** đối với file > **100 MB**.

### Kết quả rà soát các file lớn trong dự án:

1. **`models/random_forest_balanced.pkl`**: **109,445,961 bytes (~104.38 MB)**  
   🚨 **VƯỢT QUÁ GIỚI HẠN 100 MB CỦA GITHUB**. Nếu commit và push thông thường, GitHub sẽ trả về lỗi: `remote: error: GH001: Large files detected... exceeds GitHub's file size limit of 100.00 MB`.
2. **`models/random_forest_baseline.pkl`**: **100,343,705 bytes (~95.69 MB)**  
   ⚠️ Sát ngưỡng giới hạn cứng 100 MB và vượt ngưỡng cảnh báo 50 MB.
3. **Mô hình chính thức của khóa luận**:
   - `models/final_candidate_model.pkl`: **1,028,618 bytes (~1.03 MB)** (XGBoost Tuned chính thức) -> **Hoàn toàn an toàn**.
   - `models/xgboost_tuned.pkl`: **1,028,618 bytes (~1.03 MB)** -> **Hoàn toàn an toàn**.
   - `models/robust_scaler.pkl`: **1,399 bytes (~1.4 KB)** -> **Hoàn toàn an toàn**.
4. **Tập dữ liệu**:
   - `data/processed/X_train_fe.csv`: 11.5 MB
   - `data/processed/X_train.csv`: 7.5 MB
   - `data/default of credit card clients.xls`: 5.5 MB
   - `data/default_credit_card.zip`: 5.5 MB
   - `data/UCI_Credit_Card.csv`: 2.9 MB
   - `data/processed/X_test_fe.csv`: 2.9 MB  
   *(Tất cả đều dưới 15 MB, an toàn khi đưa lên Git)*.
5. **Jupyter Notebooks**:
   - `notebooks/01_Data_Audit_EDA.ipynb`: 2.9 MB (do chứa biểu đồ base64).
   - Các notebook từ tuần 2 đến tuần 9: từ 132 KB đến 867 KB.
   *(Tất cả đều an toàn)*.

### Đề xuất phương án xử lý 2 file Random Forest >95MB:
- **Phương án A (Khuyến nghị)**: Đưa 2 file thử nghiệm cũ của Tuần 7 (`models/random_forest_balanced.pkl` và `models/random_forest_baseline.pkl`) vào `.gitignore`. Lý do: Khóa luận đã hoàn thành việc chọn mô hình tại Tuần 8 với mô hình tối ưu nhất là XGBoost Tuned (`final_candidate_model.pkl`, 1.03 MB); hai file trên chỉ là mô hình thử nghiệm trung gian và có thể tái tạo bất kỳ lúc nào bằng lệnh `python -m src.ensemble_models`.
- **Phương án B**: Sử dụng `git lfs track "models/random_forest_*.pkl"` để lưu trữ qua Git LFS. Lưu ý rằng tài khoản GitHub miễn phí có giới hạn băng thông LFS 1 GB/tháng.

---

## 4. Kiểm thử Cơ sở và Tính toàn vẹn (Baseline Test)

- Đã thực thi kịch bản kiểm thử: `.\.venv\Scripts\python.exe scripts\test_week10.py`
- Kết quả kiểm thử: **PASS 6/6 TESTS**
  1. Test 1 (Khách hàng bình thường): **PASS** (Probability = 0.1189, Phân loại: Non-Default, Risk: Low Risk, 33 features).
  2. Test 2 (Khách hàng rủi ro cao): **PASS** (Probability = 0.7822, Phân loại: Default, Risk: High Risk).
  3. Test 3 (Khách hàng rủi ro thấp): **PASS** (Probability = 0.1896, Phân loại: Non-Default, Risk: Low Risk).
  4. Test 4 (Kiểm tra thứ tự 33 đặc trưng): **PASS** (Khớp hoàn toàn với `X_train_fe.csv`).
  5. Test 5 (Độ nhất quán trực tiếp của mô hình): **PASS** (Sai số = 0.00e+00).
  6. Test 6 (Giải thích mô hình SHAP cục bộ): **PASS** (SHAP TreeExplainer tính toán thành công).
- Ứng dụng Streamlit `app.py`: Đã kiểm tra cú pháp và cấu trúc, nguyên vẹn 100%.

---

## 5. Danh mục File Dự kiến Stage và Commit

### Các file sẽ được đưa lên GitHub:
- `src/`: Toàn bộ 8 module nguồn (`database.py`, `prediction.py`, `preprocessing.py`, `feature_engineering.py`, `model_training.py`, `ensemble_models.py`, `model_tuning.py`, `validate_pipeline.py`, `run_pipeline.py`).
- `notebooks/`: Toàn bộ 7 Jupyter Notebooks từ Tuần 1 đến Tuần 9 (`01_` đến `07_`).
- `models/`: Các mô hình đạt chuẩn kích thước (`final_candidate_model.pkl`, `xgboost_tuned.pkl`, `robust_scaler.pkl`, `xgboost_baseline.pkl`, `decision_tree_*.pkl`, `logistic_regression_*.pkl`, `random_forest_tuned.pkl`, `random_forest_balanced_tuned.pkl`).
- `data/`: Dữ liệu thô và dữ liệu đã tiền xử lý (`data/raw/`, `data/processed/`, file gốc).
- `reports/`: Toàn bộ báo cáo tiến độ tuần, biểu đồ minh họa (`figures/`), metadata CSV/JSON, và báo cáo pre-commit này.
- `scripts/`: Toàn bộ script tiện ích và kiểm thử.
- `docs/`: Tài liệu đồ án Word/PDF.
- Root: `app.py`, `Chay_Do_An.bat`, `requirements.txt`, `README.md`, `PROJECT_PROGRESS_REPORT.md`, `PROJECT_PROGRESS_REPORT_20261029.md`, `DCCT_NguyenTrongThe_1150080117_final.docx`, `.gitignore`, `.env.example`.

### Các file và thư mục loại trừ (`.gitignore`):
- `.env` (chứa mật khẩu kết nối database).
- `.venv/` (môi trường ảo Python, người dùng tự tạo qua `requirements.txt`).
- `__pycache__/`, `*.py[cod]`, `*.pyo`.
- `.pytest_cache/`, `.mypy_cache/`.
- `models/random_forest_balanced.pkl` (nếu chọn Phương án A).
- `models/random_forest_baseline.pkl` (nếu chọn Phương án A).
- `.vscode/`, `.idea/`, `Thumbs.db`, `.DS_Store`.

---

## 6. Kế hoạch Lệnh Git Dự kiến

Sau khi nhận được xác nhận của người dùng:
```powershell
# 1. Khởi tạo Git repository trong F:\DATN\project
cd F:\DATN\project
git init

# 2. Cấu hình danh tính commit cho repository
git config user.name "Nguyen Trong The"
git config user.email "1150080117@hcmunre.edu.vn"

# 3. Tạo .env.example và chuẩn hóa .gitignore (bổ sung loại trừ 2 file RF >100MB)

# 4. Gắn remote repository
git remote add origin https://github.com/Sith004/DATN.git

# 5. Đặt branch chính là main
git branch -M main

# 6. Stage có chọn lọc từng nhóm file (không dùng git add .)
git add .gitignore .env.example README.md requirements.txt app.py Chay_Do_An.bat
git add src/
git add scripts/
git add reports/
git add notebooks/
git add docs/
git add models/
git add data/
git add *.md *.docx

# 7. Kiểm tra staged diff
git status -s
git diff --cached --stat

# 8. Thực hiện commit chuẩn mực
git commit -m "chore: checkpoint credit risk ML project before mobile development"

# 9. Push lên remote GitHub
git push -u origin main
```
