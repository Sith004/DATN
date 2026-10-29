"""
Week 10 - Test suite for prediction pipeline
"""
import sys
sys.path.insert(0, '.')
import pandas as pd
from src.prediction import (
    engineer_features_single, map_categorical,
    load_model, load_scaler, predict_single_customer,
    compute_shap_single, FEATURE_ORDER
)

model  = load_model()
scaler = load_scaler()

print("=" * 60)
print("TEST 1: Normal Customer")
print("=" * 60)
raw = {
    'LIMIT_BAL': 200000, 'AGE': 35, 'SEX': 2,
    'EDUCATION': 2, 'MARRIAGE': 2,
    'PAY_0': 0, 'PAY_2': 0, 'PAY_3': 0, 'PAY_4': 0, 'PAY_5': 0, 'PAY_6': 0,
    'BILL_AMT1': 25000, 'BILL_AMT2': 22000, 'BILL_AMT3': 20000,
    'BILL_AMT4': 18000, 'BILL_AMT5': 15000, 'BILL_AMT6': 12000,
    'PAY_AMT1': 3000, 'PAY_AMT2': 2500, 'PAY_AMT3': 2000,
    'PAY_AMT4': 2000, 'PAY_AMT5': 1500, 'PAY_AMT6': 1500,
}
r1 = predict_single_customer(raw, model, scaler)
print(f"Probability: {r1['probability']:.4f}")
print(f"Label: {r1['prediction_label']}")
print(f"Risk: {r1['risk_level']}")
print(f"Feature count: {r1['feature_vector'].shape[1]}")
assert r1['feature_vector'].shape[1] == 33, "FEATURE COUNT MISMATCH!"
print("PASS")

print()
print("=" * 60)
print("TEST 2: High-Risk Customer")
print("=" * 60)
raw_high = {
    'LIMIT_BAL': 50000, 'AGE': 28, 'SEX': 1,
    'EDUCATION': 3, 'MARRIAGE': 1,
    'PAY_0': 3, 'PAY_2': 3, 'PAY_3': 2, 'PAY_4': 2, 'PAY_5': 1, 'PAY_6': 1,
    'BILL_AMT1': 48000, 'BILL_AMT2': 46000, 'BILL_AMT3': 44000,
    'BILL_AMT4': 42000, 'BILL_AMT5': 40000, 'BILL_AMT6': 38000,
    'PAY_AMT1': 0, 'PAY_AMT2': 0, 'PAY_AMT3': 500,
    'PAY_AMT4': 0, 'PAY_AMT5': 0, 'PAY_AMT6': 0,
}
r2 = predict_single_customer(raw_high, model, scaler)
print(f"Probability: {r2['probability']:.4f}")
print(f"Label: {r2['prediction_label']}")
print(f"Risk: {r2['risk_level']}")
assert r2['probability'] > 0.60, f"Expected high risk, got {r2['probability']:.4f}"
print("PASS - high risk confirmed")

print()
print("=" * 60)
print("TEST 3: Low-Risk Customer")
print("=" * 60)
raw_low = {
    'LIMIT_BAL': 500000, 'AGE': 45, 'SEX': 2,
    'EDUCATION': 1, 'MARRIAGE': 1,
    'PAY_0': -1, 'PAY_2': -1, 'PAY_3': -1, 'PAY_4': -1, 'PAY_5': -1, 'PAY_6': -1,
    'BILL_AMT1': 20000, 'BILL_AMT2': 18000, 'BILL_AMT3': 15000,
    'BILL_AMT4': 12000, 'BILL_AMT5': 10000, 'BILL_AMT6': 8000,
    'PAY_AMT1': 20000, 'PAY_AMT2': 18000, 'PAY_AMT3': 15000,
    'PAY_AMT4': 12000, 'PAY_AMT5': 10000, 'PAY_AMT6': 8000,
}
r3 = predict_single_customer(raw_low, model, scaler)
print(f"Probability: {r3['probability']:.4f}")
print(f"Label: {r3['prediction_label']}")
print(f"Risk: {r3['risk_level']}")
assert r3['probability'] < 0.30, f"Expected low risk, got {r3['probability']:.4f}"
print("PASS - low risk confirmed")

print()
print("=" * 60)
print("TEST 4: Feature Order Verification")
print("=" * 60)
X_train_cols = list(pd.read_csv('data/processed/X_train_fe.csv', nrows=0).columns)
assert FEATURE_ORDER == X_train_cols, "FEATURE ORDER MISMATCH!"
print(f"Feature order: VERIFIED ({len(X_train_cols)} features match X_train_fe.csv)")
print("PASS")

print()
print("=" * 60)
print("TEST 5: Direct Model Consistency")
print("=" * 60)
fv_scaled = r1['feature_vector']
direct_prob = float(model.predict_proba(fv_scaled)[0, 1])
diff = abs(direct_prob - r1['probability'])
print(f"Direct model prob:              {direct_prob:.8f}")
print(f"predict_single_customer prob:   {r1['probability']:.8f}")
print(f"Difference:                     {diff:.2e}")
assert diff < 1e-6, f"MISMATCH: {diff}"
print("PASS - predictions are identical")

print()
print("=" * 60)
print("TEST 6: SHAP Explanation")
print("=" * 60)
shap_vals, exp_val, feat_names = compute_shap_single(model, fv_scaled)
if shap_vals is not None:
    print(f"SHAP values shape: {shap_vals.shape}")
    print(f"Expected value: {exp_val:.6f}")
    print(f"Feature names count: {len(feat_names)}")
    print(f"Sum of SHAP: {sum(shap_vals):.4f}")
    print("PASS - SHAP computed successfully")
else:
    print("WARN - SHAP failed, but app will fallback gracefully")

print()
print("=" * 60)
print("ALL TESTS COMPLETED")
print("=" * 60)
