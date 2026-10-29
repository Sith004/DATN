"""
api/main.py
-----------
Main FastAPI application entrypoint for Credit Risk Assessment Mobile App.
Runs alongside existing Streamlit app without interference.
"""

import sys
from pathlib import Path

# Ensure project root is in Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes.health import router as health_router
from api.routes.predictions import router as predictions_router

app = FastAPI(
    title="Hệ thống Dự báo Rủi ro Tín dụng - REST API",
    description=(
        "FastAPI Backend phục vụ ứng dụng Mobile Android (Flutter) và Streamlit DSS.\n"
        "Đề tài: Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng.\n"
        "Sinh viên thực hiện: Nguyễn Trọng Thể — MSSV: 1150080117"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS Middleware ──────────────────────────────────────────────────────────
# Cho phép ứng dụng Flutter và các client trên mạng LAN truy cập an toàn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Include Routers ──────────────────────────────────────────────────────────
app.include_router(health_router)
app.include_router(predictions_router)


@app.get("/", tags=["Root"])
def root_info():
    return {
        "project": "Hệ thống Đánh giá & Dự báo Rủi ro Tín dụng Cá nhân",
        "author": "Nguyễn Trọng Thể - 1150080117",
        "api_docs": "/docs",
        "health_check": "/health",
        "predictions_endpoint": "/api/v1/predictions",
    }


# ── Global Exception Handler ────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "Đã xảy ra lỗi trong quá trình xử lý yêu cầu.",
            "detail": str(exc),
        },
    )


if __name__ == "__main__":
    import uvicorn
    # Chạy trên 0.0.0.0 để điện thoại Android cùng mạng Wi-Fi có thể kết nối
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
