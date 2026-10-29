"""
api/routes/health.py
--------------------
Health check endpoint reporting readiness of API, XGBoost ML model, and PostgreSQL.
"""

from fastapi import APIRouter, status
from api.schemas.prediction import HealthCheckResponse
from api.services.prediction_service import PredictionService

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Kiểm tra trạng thái hệ thống",
    description="Kiểm tra tính sẵn sàng của API, mô hình Machine Learning XGBoost và kết nối PostgreSQL."
)
def get_health_status():
    service = PredictionService.get_instance()
    return service.check_health()
