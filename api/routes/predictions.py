"""
api/routes/predictions.py
-------------------------
Prediction and history endpoints for Mobile and external clients.
Endpoints:
- POST /api/v1/predictions : Execute prediction and persist to PostgreSQL
- GET  /api/v1/predictions : Retrieve prediction history (pagination, newest-first)
- GET  /api/v1/predictions/{id} : Retrieve single prediction record by ID
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from api.schemas.prediction import (
    CustomerPredictionRequest,
    PredictionHistoryItem,
    PredictionHistoryResponse,
    PredictionResultResponse,
)
from api.services.prediction_service import PredictionService

router = APIRouter(prefix="/api/v1/predictions", tags=["Predictions"])


@router.post(
    "",
    response_model=PredictionResultResponse,
    status_code=status.HTTP_200_OK,
    summary="Thực hiện dự báo rủi ro tín dụng",
    description="Nhận 23 thuộc tính khách hàng, tiền xử lý, tính toán đặc trưng, suy luận xác suất vỡ nợ qua mô hình XGBoost Tuned và lưu vào PostgreSQL."
)
def create_prediction(request: CustomerPredictionRequest):
    service = PredictionService.get_instance()
    try:
        raw_inputs = request.model_dump()
        result = service.predict_and_persist(raw_inputs)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi trong quá trình suy luận mô hình: {str(e)}"
        )


@router.get(
    "",
    response_model=PredictionHistoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Truy vấn lịch sử dự báo",
    description="Lấy danh sách các lượt dự báo gần nhất đã lưu trong PostgreSQL (sắp xếp giảm dần theo thời gian, có phân trang)."
)
def get_prediction_history(
    page: int = Query(1, ge=1, description="Số thứ tự trang (bắt đầu từ 1)"),
    page_size: int = Query(10, ge=1, le=50, description="Số bản ghi mỗi trang (tối đa 50)")
):
    service = PredictionService.get_instance()
    offset = (page - 1) * page_size
    items_raw, total = service.get_history(limit=page_size, offset=offset)

    items = [PredictionHistoryItem(**item) for item in items_raw]

    return PredictionHistoryResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get(
    "/{prediction_id}",
    status_code=status.HTTP_200_OK,
    summary="Xem chi tiết một bản ghi dự báo",
    description="Truy vấn thông tin chi tiết một bản ghi dự báo theo mã ID."
)
def get_prediction_detail(prediction_id: int):
    service = PredictionService.get_instance()
    detail = service.get_prediction_by_id(prediction_id)
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy bản ghi dự báo với ID #{prediction_id}"
        )
    return detail
