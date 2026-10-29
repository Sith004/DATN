"""
src/prediction.py
-----------------
Week 10 — Credit Risk Prediction Module for Streamlit App.

Provides:
- Feature Engineering (identical logic to training Week 5)
- Scaler loading/fitting from training data
- Single-customer prediction with XGBoost Tuned model
- SHAP explanation for individual prediction

CRITICAL: The feature engineering logic here is COPIED EXACTLY from
src/feature_engineering.py to ensure consistency with the training pipeline.
Do NOT modify the formulas.

Feature order (33 features, verified from X_train_fe.csv and week8_model_selection_meta.json):
 1. LIMIT_BAL         14. PAY_AMT6          27. PAY_2
 2. AGE               15. UTILIZATION_RATE_SEPT  28. PAY_3
 3. BILL_AMT1         16. UTILIZATION_RATE_MEAN  29. PAY_4
 4. BILL_AMT2         17. PAY_RATIO_SEPT    30. PAY_5
 5. BILL_AMT3         18. PAY_RATIO_MEAN    31. PAY_6
 6. BILL_AMT4         19. MEAN_BILL_AMT     32. MAX_PAY_DELAY
 7. BILL_AMT5         20. MEAN_PAY_AMT      33. COUNT_LATE_PAYMENT
 8. BILL_AMT6         21. BILL_TREND
 9. PAY_AMT1          22. PAY_TREND
10. PAY_AMT2          23. SEX
11. PAY_AMT3          24. EDUCATION
12. PAY_AMT4          25. MARRIAGE
13. PAY_AMT5          26. PAY_0
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pickle
import json
import joblib

# ── Paths ──────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH       = PROJECT_ROOT / "models" / "final_candidate_model.pkl"
SCALER_PATH      = PROJECT_ROOT / "models" / "robust_scaler.pkl"
META_PATH        = PROJECT_ROOT / "reports" / "week8_model_selection_meta.json"
X_TRAIN_FE_PATH  = PROJECT_ROOT / "data" / "processed" / "X_train_fe.csv"
SHAP_SUMMARY     = PROJECT_ROOT / "reports" / "week9_shap_summary.json"

# ── Official threshold (Week 8 selection) ──────────────────────────────────
OFFICIAL_THRESHOLD = 0.60

# ── Exact 33 feature order (from X_train_fe.csv and week8_model_selection_meta.json) ──
FEATURE_ORDER = [
    "LIMIT_BAL", "AGE",
    "BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6",
    "PAY_AMT1",  "PAY_AMT2",  "PAY_AMT3",  "PAY_AMT4",  "PAY_AMT5",  "PAY_AMT6",
    "UTILIZATION_RATE_SEPT", "UTILIZATION_RATE_MEAN",
    "PAY_RATIO_SEPT", "PAY_RATIO_MEAN",
    "MEAN_BILL_AMT", "MEAN_PAY_AMT",
    "BILL_TREND", "PAY_TREND",
    "SEX", "EDUCATION", "MARRIAGE",
    "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6",
    "MAX_PAY_DELAY", "COUNT_LATE_PAYMENT",
]

# Numerical columns scaled by RobustScaler (22 columns)
NUM_COLS = [
    "LIMIT_BAL", "AGE",
    "BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6",
    "PAY_AMT1",  "PAY_AMT2",  "PAY_AMT3",  "PAY_AMT4",  "PAY_AMT5",  "PAY_AMT6",
    "UTILIZATION_RATE_SEPT", "UTILIZATION_RATE_MEAN",
    "PAY_RATIO_SEPT", "PAY_RATIO_MEAN",
    "MEAN_BILL_AMT", "MEAN_PAY_AMT",
    "BILL_TREND", "PAY_TREND",
]

# Categorical/ordinal columns — passthrough (11 columns)
CAT_COLS = [
    "SEX", "EDUCATION", "MARRIAGE",
    "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6",
    "MAX_PAY_DELAY", "COUNT_LATE_PAYMENT",
]


# ── Feature Engineering (IDENTICAL to src/feature_engineering.py::engineer_features) ──
def engineer_features_single(raw_inputs: dict) -> dict:
    """
    Apply the EXACT same feature engineering as the training pipeline.
    Input: dict of raw feature values (23 original features).
    Output: dict of 33 features (23 original + 10 engineered).

    Formula source: src/feature_engineering.py::engineer_features()
    DO NOT modify these formulas.
    """
    d = dict(raw_inputs)  # copy

    LIMIT_BAL = d["LIMIT_BAL"]

    # 1. UTILIZATION_RATE_SEPT
    d["UTILIZATION_RATE_SEPT"] = (
        0.0 if LIMIT_BAL <= 0 else d["BILL_AMT1"] / LIMIT_BAL
    )

    # 2. MEAN_BILL_AMT (needed for UTILIZATION_RATE_MEAN)
    bill_cols = ["BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6"]
    mean_bill = np.mean([d[c] for c in bill_cols])
    d["MEAN_BILL_AMT"] = mean_bill

    # 3. UTILIZATION_RATE_MEAN
    d["UTILIZATION_RATE_MEAN"] = (
        0.0 if LIMIT_BAL <= 0 else mean_bill / LIMIT_BAL
    )

    # 4. PAY_RATIO_SEPT
    d["PAY_RATIO_SEPT"] = (
        1.0 if d["BILL_AMT2"] <= 0 else d["PAY_AMT1"] / d["BILL_AMT2"]
    )

    # 5. PAY_RATIO_MEAN
    r1 = 1.0 if d["BILL_AMT2"] <= 0 else d["PAY_AMT1"] / d["BILL_AMT2"]
    r2 = 1.0 if d["BILL_AMT3"] <= 0 else d["PAY_AMT2"] / d["BILL_AMT3"]
    r3 = 1.0 if d["BILL_AMT4"] <= 0 else d["PAY_AMT3"] / d["BILL_AMT4"]
    r4 = 1.0 if d["BILL_AMT5"] <= 0 else d["PAY_AMT4"] / d["BILL_AMT5"]
    r5 = 1.0 if d["BILL_AMT6"] <= 0 else d["PAY_AMT5"] / d["BILL_AMT6"]
    d["PAY_RATIO_MEAN"] = (r1 + r2 + r3 + r4 + r5) / 5.0

    # 6. MAX_PAY_DELAY
    pay_status = [d["PAY_0"], d["PAY_2"], d["PAY_3"], d["PAY_4"], d["PAY_5"], d["PAY_6"]]
    d["MAX_PAY_DELAY"] = int(max(pay_status))

    # 7. COUNT_LATE_PAYMENT
    d["COUNT_LATE_PAYMENT"] = int(sum(1 for v in pay_status if v > 0))

    # 8. MEAN_PAY_AMT
    pay_amt_cols = ["PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6"]
    d["MEAN_PAY_AMT"] = np.mean([d[c] for c in pay_amt_cols])

    # 9. BILL_TREND
    d["BILL_TREND"] = (
        0.0 if LIMIT_BAL <= 0 else (d["BILL_AMT1"] - d["BILL_AMT6"]) / LIMIT_BAL
    )

    # 10. PAY_TREND
    d["PAY_TREND"] = (
        0.0 if LIMIT_BAL <= 0 else (d["PAY_AMT1"] - d["PAY_AMT6"]) / LIMIT_BAL
    )

    return d


# ── Categorical mapping (IDENTICAL to src/preprocessing.py::map_categorical_anomalies) ──
def map_categorical(edu: int, marriage: int):
    """
    Apply the same categorical mapping as training preprocessing.
    EDUCATION: {0,5,6} → 4
    MARRIAGE:  {0}     → 3
    """
    edu_map    = {0: 4, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4}
    marr_map   = {0: 3, 1: 1, 2: 2, 3: 3}
    edu_mapped = edu_map.get(edu, edu)
    mar_mapped = marr_map.get(marriage, marriage)
    return edu_mapped, mar_mapped


# ── Scaler: build and save from X_train_fe.csv ────────────────────────────
def build_and_save_scaler() -> object:
    """
    Fit a RobustScaler on X_train_fe (numerical columns only) and save to disk.
    This preserves the original training distribution for scaling new inputs.

    Called once to create models/robust_scaler.pkl.
    """
    from sklearn.preprocessing import RobustScaler

    print(f"Loading X_train_fe from {X_TRAIN_FE_PATH} ...")
    X_train_fe = pd.read_csv(X_TRAIN_FE_PATH, usecols=NUM_COLS)

    scaler = RobustScaler()
    scaler.fit(X_train_fe[NUM_COLS])

    joblib.dump(scaler, SCALER_PATH)
    print(f"Scaler saved to {SCALER_PATH}")
    return scaler


def load_scaler():
    """Load the pre-fitted RobustScaler. Build it if not yet created."""
    if not SCALER_PATH.exists():
        print("[INFO] Scaler not found — building from X_train_fe.csv ...")
        return build_and_save_scaler()
    return joblib.load(SCALER_PATH)


# ── Model loading ──────────────────────────────────────────────────────────
def load_model():
    """Load the official XGBoost Tuned model."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model


# ── Full inference pipeline ────────────────────────────────────────────────
def predict_single_customer(raw_inputs: dict, model, scaler):
    """
    End-to-end prediction for a single customer.

    Steps:
      1. Apply categorical mapping (same as training preprocessing)
      2. Apply feature engineering (same formulas as training Week 5)
      3. Build 33-feature DataFrame in correct order
      4. Scale numerical features with pre-fitted RobustScaler
      5. Predict probability with XGBoost model
      6. Apply threshold 0.60

    Returns dict:
        probability      : float  (0-1)
        prediction_label : str    ("Default" | "Non-Default")
        risk_level       : str    ("High Risk" | "Medium Risk" | "Low Risk")
        feature_vector   : pd.DataFrame  (1 x 33, scaled)
        feature_vector_raw: pd.DataFrame (1 x 33, unscaled — for SHAP display)
    """
    # Step 1: Categorical mapping
    edu_mapped, mar_mapped = map_categorical(raw_inputs["EDUCATION"], raw_inputs["MARRIAGE"])
    inputs_mapped = dict(raw_inputs)
    inputs_mapped["EDUCATION"] = edu_mapped
    inputs_mapped["MARRIAGE"]  = mar_mapped

    # Step 2: Feature engineering
    inputs_fe = engineer_features_single(inputs_mapped)

    # Step 3: Build DataFrame with exact 33-feature order
    row_raw = {feat: inputs_fe[feat] for feat in FEATURE_ORDER}
    df_raw  = pd.DataFrame([row_raw], columns=FEATURE_ORDER)

    # Step 4: Scale numerical columns
    df_scaled = df_raw.copy()
    df_scaled[NUM_COLS] = scaler.transform(df_raw[NUM_COLS])

    # Step 5: Predict probability
    probability = float(model.predict_proba(df_scaled)[0, 1])

    # Step 6: Apply threshold
    prediction_label = "Default" if probability >= OFFICIAL_THRESHOLD else "Non-Default"

    # Step 7: Risk level (application-layer interpretation)
    if probability >= OFFICIAL_THRESHOLD:
        risk_level = "High Risk"
    elif probability >= 0.30:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    return {
        "probability":        probability,
        "prediction_label":   prediction_label,
        "risk_level":         risk_level,
        "feature_vector":     df_scaled,
        "feature_vector_raw": df_raw,
    }


# ── SHAP explanation ───────────────────────────────────────────────────────
def compute_shap_single(model, feature_vector_scaled: pd.DataFrame):
    """
    Compute SHAP values for a single customer using TreeExplainer.
    Returns (shap_values_array, expected_value, feature_names).

    SHAP values are in log-odds space (raw XGBoost margin output).
    Positive SHAP → pushes toward Default.
    Negative SHAP → pushes toward Non-Default.
    """
    try:
        import shap
        explainer   = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(feature_vector_scaled)
        expected_val = float(explainer.expected_value)
        return shap_values[0], expected_val, list(feature_vector_scaled.columns)
    except Exception as e:
        return None, None, None


def get_top_shap_contributors(shap_values, feature_names, raw_values, n=5):
    """
    Given SHAP values for one sample, return top N positive and negative contributors.

    Returns list of dicts: [{feature, shap_value, raw_value, direction}, ...]
    sorted by |shap_value| descending.
    """
    if shap_values is None:
        return []

    records = []
    for feat, sv, rv in zip(feature_names, shap_values, raw_values):
        records.append({
            "feature":    feat,
            "shap_value": float(sv),
            "raw_value":  float(rv),
            "direction":  "↑ Risk" if sv > 0 else "↓ Risk",
        })

    records.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
    return records[:n]


# ── Model metadata ─────────────────────────────────────────────────────────
def load_model_meta() -> dict:
    """Load week8_model_selection_meta.json."""
    if META_PATH.exists():
        with open(META_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# ── Entrypoint for building scaler ─────────────────────────────────────────
if __name__ == "__main__":
    build_and_save_scaler()
    print("Done. Run: streamlit run app.py")
