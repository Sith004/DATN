# ==============================================================================
# DOCKERFILE - FASTAPI BACKEND (ML CREDIT RISK PREDICTION)
# Đề tài Đồ án Tốt nghiệp: Nguyễn Trọng Thể - MSSV: 1150080117
# ==============================================================================

FROM python:3.11-slim

# Thiết lập biến môi trường Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Cài đặt curl để phục vụ Healthcheck nếu cần
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn và mô hình Machine Learning đã huấn luyện
COPY models/ ./models/
COPY src/ ./src/
COPY api/ ./api/

# Kiểm tra sức khỏe dịch vụ
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Mở cổng mặc định
EXPOSE 8000

# Chạy Uvicorn với biến $PORT động hỗ trợ Render, Railway, Koyeb, Cloud Run
CMD ["sh", "-c", "exec uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
