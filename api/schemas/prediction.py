"""
api/schemas/prediction.py
-------------------------
Pydantic Schemas for Credit Risk Prediction API.
Strict validation matching the UCI Credit Card dataset specifications.
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, field_validator


class CustomerPredictionRequest(BaseModel):
    """
    Schema for 23 raw input attributes required by the ML inference pipeline.
    """
    LIMIT_BAL: float = Field(
        ...,
        gt=0,
        description="Hạn mức tín dụng được cấp (NT$)",
        examples=[200000.0]
    )
    AGE: int = Field(
        ...,
        ge=18,
        le=100,
        description="Độ tuổi khách hàng (18 - 100 tuổi)",
        examples=[35]
    )
    SEX: int = Field(
        ...,
        description="Giới tính (1: Nam, 2: Nữ)",
        examples=[2]
    )
    EDUCATION: int = Field(
        ...,
        description="Học vấn (1: Sau ĐH, 2: Đại học, 3: THPT, 4: Khác)",
        examples=[2]
    )
    MARRIAGE: int = Field(
        ...,
        description="Tình trạng hôn nhân (1: Đã kết hôn, 2: Độc thân, 3: Khác)",
        examples=[2]
    )

    # Lịch sử trạng thái thanh toán từ T9/2005 (PAY_0) đến T4/2005 (PAY_6)
    PAY_0: int = Field(..., ge=-2, le=8, description="Trạng thái thanh toán T9/2005 (-2..8)", examples=[0])
    PAY_2: int = Field(..., ge=-2, le=8, description="Trạng thái thanh toán T8/2005 (-2..8)", examples=[0])
    PAY_3: int = Field(..., ge=-2, le=8, description="Trạng thái thanh toán T7/2005 (-2..8)", examples=[0])
    PAY_4: int = Field(..., ge=-2, le=8, description="Trạng thái thanh toán T6/2005 (-2..8)", examples=[0])
    PAY_5: int = Field(..., ge=-2, le=8, description="Trạng thái thanh toán T5/2005 (-2..8)", examples=[0])
    PAY_6: int = Field(..., ge=-2, le=8, description="Trạng thái thanh toán T4/2005 (-2..8)", examples=[0])

    # Dư nợ hóa đơn từ T9/2005 (BILL_AMT1) đến T4/2005 (BILL_AMT6)
    BILL_AMT1: float = Field(..., description="Dư nợ hóa đơn T9/2005 (NT$)", examples=[25000.0])
    BILL_AMT2: float = Field(..., description="Dư nợ hóa đơn T8/2005 (NT$)", examples=[22000.0])
    BILL_AMT3: float = Field(..., description="Dư nợ hóa đơn T7/2005 (NT$)", examples=[20000.0])
    BILL_AMT4: float = Field(..., description="Dư nợ hóa đơn T6/2005 (NT$)", examples=[18000.0])
    BILL_AMT5: float = Field(..., description="Dư nợ hóa đơn T5/2005 (NT$)", examples=[15000.0])
    BILL_AMT6: float = Field(..., description="Dư nợ hóa đơn T4/2005 (NT$)", examples=[12000.0])

    # Số tiền đã thanh toán từ T9/2005 (PAY_AMT1) đến T4/2005 (PAY_AMT6)
    PAY_AMT1: float = Field(..., ge=0, description="Số tiền thanh toán T9/2005 (NT$)", examples=[3000.0])
    PAY_AMT2: float = Field(..., ge=0, description="Số tiền thanh toán T8/2005 (NT$)", examples=[2500.0])
    PAY_AMT3: float = Field(..., ge=0, description="Số tiền thanh toán T7/2005 (NT$)", examples=[2000.0])
    PAY_AMT4: float = Field(..., ge=0, description="Số tiền thanh toán T6/2005 (NT$)", examples=[2000.0])
    PAY_AMT5: float = Field(..., ge=0, description="Số tiền thanh toán T5/2005 (NT$)", examples=[1500.0])
    PAY_AMT6: float = Field(..., ge=0, description="Số tiền thanh toán T4/2005 (NT$)", examples=[1500.0])

    @field_validator("SEX")
    @classmethod
    def validate_sex(cls, v: int) -> int:
        if v not in (1, 2):
            raise ValueError("SEX phải là 1 (Nam) hoặc 2 (Nữ)")
        return v

    @field_validator("EDUCATION")
    @classmethod
    def validate_education(cls, v: int) -> int:
        if v not in (0, 1, 2, 3, 4, 5, 6):
            raise ValueError("EDUCATION phải thuộc khoảng 0..6 (1: Sau ĐH, 2: ĐH, 3: THPT, 4: Khác)")
        return v

    @field_validator("MARRIAGE")
    @classmethod
    def validate_marriage(cls, v: int) -> int:
        if v not in (0, 1, 2, 3):
            raise ValueError("MARRIAGE phải thuộc khoảng 0..3 (1: Đã kết hôn, 2: Độc thân, 3: Khác)")
        return v


class RiskFactorDetail(BaseModel):
    feature: str = Field(..., description="Tên đặc trưng")
    shap_value: float = Field(..., description="Giá trị đóng góp SHAP (log-odds)")
    raw_value: float = Field(..., description="Giá trị thực tế của đặc trưng")
    direction: str = Field(..., description="Chiều hướng tác động: '↑ Risk' hoặc '↓ Risk'")


class PredictionResultResponse(BaseModel):
    """
    Schema for prediction output returned to Mobile and clients.
    """
    prediction_probability: float = Field(..., description="Xác suất vỡ nợ (0.0000 - 1.0000)")
    prediction_label: str = Field(..., description="Nhãn phân loại: 'Default' hoặc 'Non-Default'")
    risk_level: str = Field(..., description="Mức độ rủi ro: 'Low Risk', 'Medium Risk', 'High Risk'")
    threshold: float = Field(default=0.60, description="Ngưỡng quyết định áp dụng")
    model_version: str = Field(default="xgboost_tuned_v1", description="Phiên bản mô hình")
    record_id: Optional[int] = Field(None, description="Mã bản ghi lưu trữ trong PostgreSQL (nếu có)")
    persisted: bool = Field(..., description="Trạng thái lưu trữ vào cơ sở dữ liệu")
    persistence_message: str = Field(..., description="Thông báo chi tiết về lưu trữ CSDL")
    top_risk_factors: Optional[List[RiskFactorDetail]] = Field(
        default=None,
        description="Top các đặc trưng ảnh hưởng lớn nhất theo giải thích SHAP"
    )


class PredictionHistoryItem(BaseModel):
    id: int = Field(..., description="Mã bản ghi dự báo")
    created_at: str = Field(..., description="Thời gian thực hiện dự báo (YYYY-MM-DD HH:MM:SS)")
    limit_bal: float = Field(..., description="Hạn mức tín dụng (NT$)")
    age: int = Field(..., description="Tuổi khách hàng")
    default_probability: float = Field(..., description="Xác suất vỡ nợ (0 - 1)")
    prediction_label: str = Field(..., description="Phân loại kết quả")
    risk_level: str = Field(..., description="Mức độ rủi ro")
    model_version: str = Field(..., description="Phiên bản mô hình")


class PredictionHistoryResponse(BaseModel):
    items: List[PredictionHistoryItem] = Field(default_factory=list, description="Danh sách lịch sử dự báo")
    total: int = Field(..., description="Tổng số bản ghi trả về")
    page: int = Field(1, description="Trang hiện tại")
    page_size: int = Field(10, description="Số bản ghi mỗi trang")


class HealthCheckResponse(BaseModel):
    status: str = Field(..., description="Trạng thái dịch vụ API ('healthy' hoặc 'degraded')")
    api_version: str = Field(default="1.0.0", description="Phiên bản REST API")
    model_ready: bool = Field(..., description="Trạng thái tải của mô hình XGBoost")
    model_name: str = Field(..., description="Tên mô hình Machine Learning")
    threshold: float = Field(..., description="Ngưỡng phân loại được cấu hình")
    database_connected: bool = Field(..., description="Trạng thái kết nối tới PostgreSQL")
    database_status_message: str = Field(..., description="Thông điệp kết nối cơ sở dữ liệu")
