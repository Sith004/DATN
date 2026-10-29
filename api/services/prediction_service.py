"""
api/services/prediction_service.py
----------------------------------
Thin service layer connecting FastAPI to existing ML and DB modules.
Reuses:
- src.prediction (load_model, load_scaler, predict_single_customer, compute_shap_single)
- src.database (check_db_status, save_prediction_record, get_db_connection)
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from src.database import check_db_status, get_db_connection, save_prediction_record
from src.prediction import (
    OFFICIAL_THRESHOLD,
    compute_shap_single,
    get_top_shap_contributors,
    load_model,
    load_scaler,
    predict_single_customer,
)

logger = logging.getLogger("api_prediction_service")


class PredictionService:
    _instance: Optional["PredictionService"] = None

    def __init__(self):
        logger.info("Initializing PredictionService: loading XGBoost model & RobustScaler...")
        self.model = load_model()
        self.scaler = load_scaler()
        self.threshold = OFFICIAL_THRESHOLD
        self.model_version = "xgboost_tuned_v1"
        logger.info("PredictionService initialized successfully.")

    @classmethod
    def get_instance(cls) -> "PredictionService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def predict_and_persist(self, raw_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs ML prediction pipeline and attempts PostgreSQL persistence.
        Guarantees:
        - Exact ML inference logic from src.prediction.
        - Graceful degradation: DB errors do not fail the prediction response.
        - Parameterized query for DB insert.
        """
        # 1. Run inference using official model & scaler
        ml_result = predict_single_customer(raw_inputs, self.model, self.scaler)

        prob = ml_result["probability"]
        label = ml_result["prediction_label"]
        risk = ml_result["risk_level"]
        df_scaled = ml_result["feature_vector"]
        df_raw = ml_result["feature_vector_raw"]

        # 2. Compute Top SHAP contributors (Explainable AI)
        top_factors = []
        try:
            shap_vals, _, feat_names = compute_shap_single(self.model, df_scaled)
            if shap_vals is not None:
                raw_values = [df_raw[col].iloc[0] for col in feat_names]
                top_factors = get_top_shap_contributors(shap_vals, feat_names, raw_values, n=5)
        except Exception as e:
            logger.warning(f"Error computing SHAP values in API service: {e}")

        # 3. Save to PostgreSQL with Graceful Degradation
        engineered_payload = {
            "features_33": df_raw.to_dict(orient="records")[0] if not df_raw.empty else {},
        }
        db_saved, record_id, db_msg = save_prediction_record(
            raw_inputs=raw_inputs,
            prediction_result=ml_result,
            model_version=self.model_version,
            threshold=self.threshold,
            engineered_features=engineered_payload,
        )

        return {
            "prediction_probability": round(prob, 4),
            "prediction_label": label,
            "risk_level": risk,
            "threshold": self.threshold,
            "model_version": self.model_version,
            "record_id": record_id,
            "persisted": db_saved,
            "persistence_message": db_msg,
            "top_risk_factors": top_factors,
        }

    def get_history(self, limit: int = 10, offset: int = 0) -> Tuple[List[Dict[str, Any]], int]:
        """
        Retrieves prediction history from PostgreSQL with newest-first ordering.
        Parameterized query.
        """
        select_sql = """
        SELECT 
            id,
            to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at,
            limit_bal,
            age,
            round(default_probability, 4) AS default_probability,
            prediction_label,
            risk_level,
            model_version
        FROM credit_app.customer_predictions
        ORDER BY id DESC
        LIMIT %s OFFSET %s;
        """
        count_sql = "SELECT COUNT(*) FROM credit_app.customer_predictions;"

        conn = None
        items = []
        total = 0
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute(count_sql)
                total = cur.fetchone()[0]

                cur.execute(select_sql, (int(limit), int(offset)))
                rows = cur.fetchall()
                for row in rows:
                    items.append({
                        "id": row[0],
                        "created_at": row[1],
                        "limit_bal": float(row[2]),
                        "age": int(row[3]),
                        "default_probability": float(row[4]),
                        "prediction_label": str(row[5]),
                        "risk_level": str(row[6]),
                        "model_version": str(row[7]),
                    })
        except Exception as e:
            logger.warning(f"Error reading prediction history: {e}")
        finally:
            if conn:
                conn.close()

        return items, total

    def get_prediction_by_id(self, pred_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves detail of a specific prediction by record ID.
        Parameterized query.
        """
        select_sql = """
        SELECT 
            id,
            to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at,
            limit_bal,
            age,
            sex,
            education,
            marriage,
            round(default_probability, 4) AS default_probability,
            prediction_label,
            risk_level,
            model_version,
            threshold
        FROM credit_app.customer_predictions
        WHERE id = %s;
        """
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute(select_sql, (int(pred_id),))
                row = cur.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "created_at": row[1],
                        "limit_bal": float(row[2]),
                        "age": int(row[3]),
                        "sex": int(row[4]),
                        "education": int(row[5]),
                        "marriage": int(row[6]),
                        "default_probability": float(row[7]),
                        "prediction_label": str(row[8]),
                        "risk_level": str(row[9]),
                        "model_version": str(row[10]),
                        "threshold": float(row[11]),
                    }
        except Exception as e:
            logger.warning(f"Error fetching prediction by ID {pred_id}: {e}")
        finally:
            if conn:
                conn.close()
        return None

    def check_health(self) -> Dict[str, Any]:
        """
        Checks readiness of API, ML model, and PostgreSQL database.
        """
        model_ready = self.model is not None and self.scaler is not None
        db_connected, db_msg = check_db_status()

        return {
            "status": "healthy" if (model_ready and db_connected) else "degraded",
            "api_version": "1.0.0",
            "model_ready": model_ready,
            "model_name": "XGBoost Tuned (Final Candidate)",
            "threshold": self.threshold,
            "database_connected": db_connected,
            "database_status_message": db_msg,
        }
