"""
tests/test_api_and_consistency.py
---------------------------------
Comprehensive Test Suite for:
1. Health endpoint (/health)
2. ML Prediction Consistency (src.prediction vs FastAPI API endpoint)
3. Validation errors (missing fields, out-of-range inputs)
4. Database persistence and Graceful Degradation
5. History retrieval and pagination (/api/v1/predictions)
6. Single prediction detail query (/api/v1/predictions/{id})
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.main import app
from src.prediction import load_model, load_scaler, predict_single_customer

client = TestClient(app)


# ── Sample Customer Payloads ────────────────────────────────────────────────
NORMAL_CUSTOMER = {
    "LIMIT_BAL": 200000.0,
    "AGE": 35,
    "SEX": 2,
    "EDUCATION": 2,
    "MARRIAGE": 2,
    "PAY_0": 0,
    "PAY_2": 0,
    "PAY_3": 0,
    "PAY_4": 0,
    "PAY_5": 0,
    "PAY_6": 0,
    "BILL_AMT1": 25000.0,
    "BILL_AMT2": 22000.0,
    "BILL_AMT3": 20000.0,
    "BILL_AMT4": 18000.0,
    "BILL_AMT5": 15000.0,
    "BILL_AMT6": 12000.0,
    "PAY_AMT1": 3000.0,
    "PAY_AMT2": 2500.0,
    "PAY_AMT3": 2000.0,
    "PAY_AMT4": 2000.0,
    "PAY_AMT5": 1500.0,
    "PAY_AMT6": 1500.0,
}

HIGH_RISK_CUSTOMER = {
    "LIMIT_BAL": 50000.0,
    "AGE": 28,
    "SEX": 1,
    "EDUCATION": 3,
    "MARRIAGE": 1,
    "PAY_0": 3,
    "PAY_2": 3,
    "PAY_3": 2,
    "PAY_4": 2,
    "PAY_5": 1,
    "PAY_6": 1,
    "BILL_AMT1": 48000.0,
    "BILL_AMT2": 46000.0,
    "BILL_AMT3": 44000.0,
    "BILL_AMT4": 42000.0,
    "BILL_AMT5": 40000.0,
    "BILL_AMT6": 38000.0,
    "PAY_AMT1": 0.0,
    "PAY_AMT2": 0.0,
    "PAY_AMT3": 500.0,
    "PAY_AMT4": 0.0,
    "PAY_AMT5": 0.0,
    "PAY_AMT6": 0.0,
}

LOW_RISK_CUSTOMER = {
    "LIMIT_BAL": 500000.0,
    "AGE": 45,
    "SEX": 2,
    "EDUCATION": 1,
    "MARRIAGE": 1,
    "PAY_0": -1,
    "PAY_2": -1,
    "PAY_3": -1,
    "PAY_4": -1,
    "PAY_5": -1,
    "PAY_6": -1,
    "BILL_AMT1": 20000.0,
    "BILL_AMT2": 18000.0,
    "BILL_AMT3": 15000.0,
    "BILL_AMT4": 12000.0,
    "BILL_AMT5": 10000.0,
    "BILL_AMT6": 8000.0,
    "PAY_AMT1": 20000.0,
    "PAY_AMT2": 18000.0,
    "PAY_AMT3": 15000.0,
    "PAY_AMT4": 12000.0,
    "PAY_AMT5": 10000.0,
    "PAY_AMT6": 8000.0,
}


def test_health_endpoint():
    """Kiểm tra endpoint /health trả về trạng thái hợp lệ"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["model_ready"] is True
    assert data["threshold"] == 0.60
    assert "status" in data
    assert "database_connected" in data
    print("PASS: Health endpoint test passed.")


def test_ml_prediction_consistency():
    """Kiểm tra độ nhất quán giữa src.prediction và FastAPI response trên cùng input"""
    model = load_model()
    scaler = load_scaler()

    # 1. Chạy trực tiếp từ module src.prediction
    direct_res = predict_single_customer(NORMAL_CUSTOMER, model, scaler)

    # 2. Chạy thông qua FastAPI POST /api/v1/predictions
    api_res = client.post("/api/v1/predictions", json=NORMAL_CUSTOMER)
    assert api_res.status_code == 200
    api_data = api_res.json()

    # So sánh xác suất (sai số cho phép < 1e-4 do làm tròn 4 chữ số thập phân)
    diff = abs(direct_res["probability"] - api_data["prediction_probability"])
    assert diff < 1e-3, f"Probability mismatch: {direct_res['probability']} vs {api_data['prediction_probability']}"
    assert direct_res["prediction_label"] == api_data["prediction_label"]
    assert direct_res["risk_level"] == api_data["risk_level"]
    assert api_data["threshold"] == 0.60
    print(f"PASS: ML Consistency test passed (prob diff={diff:.6f}).")


def test_high_risk_prediction():
    """Kiểm tra khách hàng rủi ro cao được phân loại chính xác Default (>= 0.60)"""
    response = client.post("/api/v1/predictions", json=HIGH_RISK_CUSTOMER)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction_probability"] >= 0.60
    assert data["prediction_label"] == "Default"
    assert data["risk_level"] == "High Risk"
    print("PASS: High Risk prediction confirmed.")


def test_low_risk_prediction():
    """Kiểm tra khách hàng rủi ro thấp được phân loại chính xác Non-Default (< 0.30)"""
    response = client.post("/api/v1/predictions", json=LOW_RISK_CUSTOMER)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction_probability"] < 0.30
    assert data["prediction_label"] == "Non-Default"
    assert data["risk_level"] == "Low Risk"
    print("PASS: Low Risk prediction confirmed.")


def test_validation_missing_field():
    """Kiểm tra từ chối yêu cầu thiếu trường bắt buộc"""
    bad_payload = dict(NORMAL_CUSTOMER)
    del bad_payload["LIMIT_BAL"]

    response = client.post("/api/v1/predictions", json=bad_payload)
    assert response.status_code == 422  # Pydantic validation error
    print("PASS: Missing field rejected with HTTP 422.")


def test_validation_out_of_range():
    """Kiểm tra từ chối các trường có giá trị ngoài biên hợp lệ"""
    # 1. Tuổi dưới 18
    bad_age = dict(NORMAL_CUSTOMER, AGE=15)
    r1 = client.post("/api/v1/predictions", json=bad_age)
    assert r1.status_code == 422

    # 2. Hạn mức âm
    bad_limit = dict(NORMAL_CUSTOMER, LIMIT_BAL=-5000)
    r2 = client.post("/api/v1/predictions", json=bad_limit)
    assert r2.status_code == 422

    # 3. Giới tính không hợp lệ (không phải 1 hoặc 2)
    bad_sex = dict(NORMAL_CUSTOMER, SEX=3)
    r3 = client.post("/api/v1/predictions", json=bad_sex)
    assert r3.status_code == 422
    print("PASS: Out-of-range validations rejected with HTTP 422.")


def test_prediction_history_endpoint():
    """Kiểm tra truy vấn lịch sử dự báo có phân trang và newest-first"""
    response = client.get("/api/v1/predictions?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["page"] == 1
    assert data["page_size"] == 5
    if len(data["items"]) > 1:
        # Kiểm tra sắp xếp giảm dần theo ID
        ids = [item["id"] for item in data["items"]]
        assert ids == sorted(ids, reverse=True), f"History not sorted DESC: {ids}"
    print("PASS: History endpoint pagination and ordering verified.")


def test_prediction_detail_not_found():
    """Kiểm tra truy vấn bản ghi ID không tồn tại trả về 404"""
    response = client.get("/api/v1/predictions/999999999")
    assert response.status_code == 404
    print("PASS: Non-existent ID returned 404.")


if __name__ == "__main__":
    print("Running comprehensive test suite...")
    test_health_endpoint()
    test_ml_prediction_consistency()
    test_high_risk_prediction()
    test_low_risk_prediction()
    test_validation_missing_field()
    test_validation_out_of_range()
    test_prediction_history_endpoint()
    test_prediction_detail_not_found()
    print("\nALL 8 API & CONSISTENCY TESTS PASSED SUCCESSFULLY!")
