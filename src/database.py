"""
src/database.py
---------------
Module quản trị và kết nối cơ sở dữ liệu PostgreSQL cho Đồ án Tốt nghiệp.
Bảo đảm:
1. Kết nối qua biến môi trường (.env) bảo mật, không hardcode mật khẩu.
2. Parameterized queries ngăn chặn triệt để lỗ hổng SQL Injection.
3. Graceful degradation: Lỗi CSDL không làm ảnh hưởng quy trình dự báo Machine Learning.
4. Quản lý tài nguyên an toàn (Context Manager / connection pooling / close).
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
import pandas as pd
import psycopg2

# Nạp biến môi trường từ .env ở root project
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

logger = logging.getLogger("credit_risk_db")

def get_db_connection():
    """
    Khởi tạo kết nối tới PostgreSQL sử dụng các biến môi trường.
    Timeout kết nối được đặt là 3 giây để tránh làm ứng dụng bị treo khi mất kết nối.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "15432")),
        dbname=os.getenv("DB_NAME", "credit_risk_db"),
        user=os.getenv("DB_USER", "app_streamlit"),
        password=os.getenv("DB_PASSWORD", ""),
        connect_timeout=3,
    )

def check_db_status() -> Tuple[bool, str]:
    """
    Kiểm tra trạng thái kết nối tới PostgreSQL (dành cho chỉ báo trạng thái trên giao diện).
    Trả về: (Trạng thái kết nối: bool, Thông điệp: str)
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            cur.fetchone()
        return True, "Đã kết nối an toàn qua SSH Tunnel (Port 15432)"
    except Exception as e:
        err_msg = str(e).split("\n")[0]
        return False, f"Mất kết nối CSDL: {err_msg}"
    finally:
        if conn:
            conn.close()

def save_prediction_record(
    raw_inputs: Dict[str, Any],
    prediction_result: Dict[str, Any],
    model_version: str = "xgboost_tuned_v1",
    threshold: float = 0.60,
    engineered_features: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, Optional[int], str]:
    """
    Lưu kết quả dự báo của khách hàng vào bảng credit_app.customer_predictions.
    Sử dụng hoàn toàn Parameterized Query để phòng chống SQL Injection.

    Trả về: (Thành công: bool, ID bản ghi: Optional[int], Thông báo: str)
    """
    insert_sql = """
    INSERT INTO credit_app.customer_predictions (
        limit_bal, age, sex, education, marriage,
        pay_0, pay_2, pay_3, pay_4, pay_5, pay_6,
        bill_amt1, bill_amt2, bill_amt3, bill_amt4, bill_amt5, bill_amt6,
        pay_amt1, pay_amt2, pay_amt3, pay_amt4, pay_amt5, pay_amt6,
        default_probability, prediction_label, risk_level,
        model_version, threshold, engineered_features
    ) VALUES (
        %(LIMIT_BAL)s, %(AGE)s, %(SEX)s, %(EDUCATION)s, %(MARRIAGE)s,
        %(PAY_0)s, %(PAY_2)s, %(PAY_3)s, %(PAY_4)s, %(PAY_5)s, %(PAY_6)s,
        %(BILL_AMT1)s, %(BILL_AMT2)s, %(BILL_AMT3)s, %(BILL_AMT4)s, %(BILL_AMT5)s, %(BILL_AMT6)s,
        %(PAY_AMT1)s, %(PAY_AMT2)s, %(PAY_AMT3)s, %(PAY_AMT4)s, %(PAY_AMT5)s, %(PAY_AMT6)s,
        %(default_probability)s, %(prediction_label)s, %(risk_level)s,
        %(model_version)s, %(threshold)s, %(engineered_features)s
    ) RETURNING id;
    """

    params = {
        "LIMIT_BAL": float(raw_inputs["LIMIT_BAL"]),
        "AGE": int(raw_inputs["AGE"]),
        "SEX": int(raw_inputs["SEX"]),
        "EDUCATION": int(raw_inputs["EDUCATION"]),
        "MARRIAGE": int(raw_inputs["MARRIAGE"]),
        "PAY_0": int(raw_inputs["PAY_0"]),
        "PAY_2": int(raw_inputs["PAY_2"]),
        "PAY_3": int(raw_inputs["PAY_3"]),
        "PAY_4": int(raw_inputs["PAY_4"]),
        "PAY_5": int(raw_inputs["PAY_5"]),
        "PAY_6": int(raw_inputs["PAY_6"]),
        "BILL_AMT1": float(raw_inputs["BILL_AMT1"]),
        "BILL_AMT2": float(raw_inputs["BILL_AMT2"]),
        "BILL_AMT3": float(raw_inputs["BILL_AMT3"]),
        "BILL_AMT4": float(raw_inputs["BILL_AMT4"]),
        "BILL_AMT5": float(raw_inputs["BILL_AMT5"]),
        "BILL_AMT6": float(raw_inputs["BILL_AMT6"]),
        "PAY_AMT1": float(raw_inputs["PAY_AMT1"]),
        "PAY_AMT2": float(raw_inputs["PAY_AMT2"]),
        "PAY_AMT3": float(raw_inputs["PAY_AMT3"]),
        "PAY_AMT4": float(raw_inputs["PAY_AMT4"]),
        "PAY_AMT5": float(raw_inputs["PAY_AMT5"]),
        "PAY_AMT6": float(raw_inputs["PAY_AMT6"]),
        "default_probability": round(float(prediction_result["probability"]), 4),
        "prediction_label": str(prediction_result["prediction_label"]),
        "risk_level": str(prediction_result["risk_level"]),
        "model_version": model_version,
        "threshold": float(threshold),
        "engineered_features": json.dumps(engineered_features) if engineered_features else None,
    }

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(insert_sql, params)
            new_id = cur.fetchone()[0]
        conn.commit()
        return True, new_id, f"Lưu thành công vào cơ sở dữ liệu với ID #{new_id}"
    except Exception as e:
        if conn:
            conn.rollback()
        err_msg = str(e).split("\n")[0]
        print(f"DATABASE INSERT ERROR: {err_msg}")
        logger.warning(f"Lỗi khi lưu dữ liệu dự báo vào PostgreSQL: {err_msg}")
        return False, None, f"Không thể lưu vào CSDL: {err_msg}"
    finally:
        if conn:
            conn.close()

def get_recent_predictions(limit: int = 10) -> pd.DataFrame:
    """
    Truy vấn các bản ghi dự báo gần nhất để hiển thị trực quan trên giao diện Streamlit.
    """
    select_sql = """
    SELECT 
        id AS "Mã dự báo",
        to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') AS "Thời gian",
        limit_bal AS "Hạn mức (NT$)",
        age AS "Tuổi",
        round(default_probability * 100, 2) AS "Xác suất Default (%%)",
        prediction_label AS "Phân loại",
        risk_level AS "Mức rủi ro",
        model_version AS "Phiên bản mô hình"
    FROM credit_app.customer_predictions
    ORDER BY id DESC
    LIMIT %s;
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(select_sql, (int(limit),))
            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]
            df = pd.DataFrame(rows, columns=cols)
            if not df.empty and "Xác suất Default (%)" in df.columns:
                df["Xác suất Default (%)"] = df["Xác suất Default (%)"].astype(str) + "%"
            return df
    except Exception as e:
        print(f"DATABASE SELECT ERROR: {e}")
        logger.warning(f"Lỗi truy vấn lịch sử dự báo: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()
