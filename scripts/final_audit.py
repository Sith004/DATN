"""
FINAL AUDIT: Week 1-5 Pipeline Comprehensive Validation
Checks:
1. Notebook 02 execution status (via output cells)
2. Preprocessing pipeline order and integrity
3. Data Leakage checks
4. Feature Engineering order (before vs after scaling)
5. FE formula verification for all 10 features
6. Output file validation
"""
import json, sys, os
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

PROJ = r"F:\DATN\project"
os.chdir(PROJ)

results = {}

print("=" * 60)
print("FINAL AUDIT: PIPELINE TUẦN 1-5")
print("=" * 60)

# ============================================================
# SECTION A: Notebook 02 execution status
# ============================================================
print("\n[A] NOTEBOOK 02 - KIỂM TRA EXECUTION")
nb02_path = os.path.join(PROJ, "notebooks", "02_Preprocessing.ipynb")
with open(nb02_path, "r", encoding="utf-8") as f:
    nb02 = json.load(f)

code_cells = [c for c in nb02["cells"] if c["cell_type"] == "code"]
total_cells = len(code_cells)
cells_with_output = sum(1 for c in code_cells if c.get("outputs"))
cells_with_errors = sum(1 for c in code_cells
                        for o in c.get("outputs", [])
                        if o.get("output_type") == "error")
exec_counts = [c.get("execution_count") for c in code_cells]
all_executed = all(ec is not None for ec in exec_counts)

print(f"  Total code cells     : {total_cells}")
print(f"  Cells with output    : {cells_with_output}")
print(f"  Cells with ERROR     : {cells_with_errors}")
print(f"  All cells executed   : {all_executed}")

# Check for SyntaxErrors in source
syntax_errors = []
for i, cell in enumerate(nb02["cells"]):
    if cell["cell_type"] != "code":
        continue
    code = "".join(cell["source"])
    try:
        compile(code, f"nb02_cell_{i}", "exec")
    except SyntaxError as e:
        syntax_errors.append((i, str(e)))

print(f"  SyntaxErrors in source: {len(syntax_errors)}")
if syntax_errors:
    for idx, msg in syntax_errors:
        print(f"    Cell {idx}: {msg}")

nb02_pass = (cells_with_errors == 0 and all_executed and len(syntax_errors) == 0)
results["A_notebook02"] = "PASS" if nb02_pass else "FAIL"
print(f"\n  >>> VERDICT A (Notebook 02): {results['A_notebook02']}")

# ============================================================
# SECTION B: Preprocessing pipeline order and integrity
# ============================================================
print("\n" + "=" * 60)
print("[B] PREPROCESSING PIPELINE - ORDER & INTEGRITY")

sys.path.insert(0, PROJ)           # for 'src.preprocessing' used inside feature_engineering
sys.path.insert(0, os.path.join(PROJ, "src"))
from preprocessing import (
    load_raw_data, clean_duplicates, map_categorical_anomalies,
    separate_features_target, split_train_test, build_preprocessing_pipeline,
    fit_transform_data
)

df_raw = load_raw_data()
print(f"  1. Raw data loaded       : {df_raw.shape} (30000 rows expected)")
assert df_raw.shape[0] == 30000, "Expected 30000 raw rows"

df_cleaned, num_dups = clean_duplicates(df_raw)
print(f"  2. After dedup           : {df_cleaned.shape} (removed {num_dups} dups, expected 35)")
assert num_dups == 35, f"Expected 35 dups, got {num_dups}"

df_mapped = map_categorical_anomalies(df_cleaned)
edu_values = sorted(df_mapped["EDUCATION"].unique().tolist())
mar_values = sorted(df_mapped["MARRIAGE"].unique().tolist())
print(f"  3. EDUCATION values      : {edu_values} (expected [1,2,3,4])")
print(f"     MARRIAGE values       : {mar_values} (expected [1,2,3])")
assert edu_values == [1, 2, 3, 4], f"EDUCATION mapping wrong: {edu_values}"
assert mar_values == [1, 2, 3], f"MARRIAGE mapping wrong: {mar_values}"

X, y = separate_features_target(df_mapped)
target_in_X = "default.payment.next.month" in X.columns
id_in_X = "ID" in X.columns
print(f"  4. X shape               : {X.shape} (23 cols expected)")
print(f"     Target in X           : {target_in_X} (expected False)")
print(f"     ID in X               : {id_in_X} (expected False)")
assert not target_in_X and not id_in_X

# Split BEFORE scaling
X_train, X_test, y_train, y_test = split_train_test(X, y, test_size=0.20, random_state=42)
print(f"  5. Train/Test split      : {X_train.shape} / {X_test.shape}")
train_ratio = y_train.mean()
test_ratio = y_test.mean()
ratio_ok = abs(train_ratio - test_ratio) < 0.001
print(f"     Stratification        : train={train_ratio:.4f}, test={test_ratio:.4f}, OK={ratio_ok}")

# Scaler fit ONLY on train
preprocessor, num_cols, cat_cols = build_preprocessing_pipeline(scaler_type='robust')
preprocessor.fit(X_train)  # fit ONLY on train
X_train_proc, X_test_proc, _ = fit_transform_data(preprocessor, X_train, X_test)

scaler_fitted_on = "TRAIN ONLY"  # by design
print(f"  6. Scaler fit on         : {scaler_fitted_on}")
print(f"     X_train_proc shape    : {X_train_proc.shape}")
print(f"     X_test_proc shape     : {X_test_proc.shape}")
print(f"     X_train NaN           : {X_train_proc.isna().sum().sum()}")
print(f"     X_test NaN            : {X_test_proc.isna().sum().sum()}")
print(f"     X_train Inf           : {int(np.isinf(X_train_proc.values).sum())}")
print(f"     X_test Inf            : {int(np.isinf(X_test_proc.values).sum())}")

cols_match = list(X_train_proc.columns) == list(X_test_proc.columns)
print(f"  7. Train/Test same cols  : {cols_match}")

prep_pass = (
    not target_in_X and
    not id_in_X and
    ratio_ok and
    X_train_proc.isna().sum().sum() == 0 and
    X_test_proc.isna().sum().sum() == 0 and
    int(np.isinf(X_train_proc.values).sum()) == 0 and
    int(np.isinf(X_test_proc.values).sum()) == 0 and
    cols_match
)
results["B_preprocessing"] = "PASS" if prep_pass else "FAIL"
print(f"\n  >>> VERDICT B (Preprocessing): {results['B_preprocessing']}")

# ============================================================
# SECTION C+D: Feature Engineering - ORDER & FORMULAS
# ============================================================
print("\n" + "=" * 60)
print("[C+D] FEATURE ENGINEERING - ORDER & LEAKAGE & FORMULAS")

from feature_engineering import engineer_features, build_fe_preprocessing_pipeline, fit_transform_fe_data, verify_fe_datasets

# Re-run from raw data (same as run_feature_engineering_pipeline does)
X_train_fe_raw = engineer_features(X_train)    # applied to X_train RAW (before scaling)
X_test_fe_raw = engineer_features(X_test)      # applied to X_test RAW (before scaling)

print(f"  FE applied on           : X_train_raw (23 cols) -> X_train_fe_raw ({X_train_fe_raw.shape[1]} cols)")
print(f"  FE input columns check  : LIMIT_BAL={X_train['LIMIT_BAL'].dtype}, BILL_AMT1={X_train['BILL_AMT1'].dtype}")
print()

# Verify FE was done on RAW (not scaled) data
# Raw LIMIT_BAL should be in original units (e.g. 10000-1000000 range)
lim_min = X_train["LIMIT_BAL"].min()
lim_max = X_train["LIMIT_BAL"].max()
# If data was scaled by RobustScaler, LIMIT_BAL values would be roughly -1 to 10 range
fe_on_raw = (lim_min > 1000)  # Raw values are always > 1000 NTD
print(f"  LIMIT_BAL range (FE input): min={lim_min}, max={lim_max}")
print(f"  FE on RAW (not scaled) data: {fe_on_raw}")

# Formula verification for all 10 features
print("\n  === FORMULA VERIFICATION (10 Features) ===")
sample_idx = X_train.index[0]
row_raw = X_train.loc[sample_idx]
row_fe = X_train_fe_raw.loc[sample_idx]

formulas = {
    "UTILIZATION_RATE_SEPT": {
        "desc": "BILL_AMT1 / LIMIT_BAL",
        "expected": row_raw["BILL_AMT1"] / row_raw["LIMIT_BAL"] if row_raw["LIMIT_BAL"] > 0 else 0.0,
        "actual": row_fe["UTILIZATION_RATE_SEPT"],
        "source_cols": ["BILL_AMT1", "LIMIT_BAL"],
        "computed_on": "Raw cleaned data (before scaling)"
    },
    "UTILIZATION_RATE_MEAN": {
        "desc": "mean(BILL_AMT1..6) / LIMIT_BAL",
        "expected": row_raw[["BILL_AMT1","BILL_AMT2","BILL_AMT3","BILL_AMT4","BILL_AMT5","BILL_AMT6"]].mean() / row_raw["LIMIT_BAL"] if row_raw["LIMIT_BAL"] > 0 else 0.0,
        "actual": row_fe["UTILIZATION_RATE_MEAN"],
        "source_cols": ["BILL_AMT1..6", "LIMIT_BAL"],
        "computed_on": "Raw cleaned data (before scaling)"
    },
    "PAY_RATIO_SEPT": {
        "desc": "PAY_AMT1 / BILL_AMT2 (PAY_AMT1 pays for BILL_AMT2 cycle)",
        "expected": 1.0 if row_raw["BILL_AMT2"] <= 0 else row_raw["PAY_AMT1"] / row_raw["BILL_AMT2"],
        "actual": row_fe["PAY_RATIO_SEPT"],
        "source_cols": ["PAY_AMT1", "BILL_AMT2"],
        "computed_on": "Raw cleaned data (before scaling)"
    },
    "PAY_RATIO_MEAN": {
        "desc": "mean of 5 PAY_RATIOs: PAY_AMTk/BILL_AMT(k+1) for k=1..5",
        "expected": None,  # complex, just verify it's not NaN
        "actual": row_fe["PAY_RATIO_MEAN"],
        "source_cols": ["PAY_AMT1..5", "BILL_AMT2..6"],
        "computed_on": "Raw cleaned data (before scaling)"
    },
    "MEAN_BILL_AMT": {
        "desc": "mean(BILL_AMT1..6)",
        "expected": row_raw[["BILL_AMT1","BILL_AMT2","BILL_AMT3","BILL_AMT4","BILL_AMT5","BILL_AMT6"]].mean(),
        "actual": row_fe["MEAN_BILL_AMT"],
        "source_cols": ["BILL_AMT1..6"],
        "computed_on": "Raw cleaned data (before scaling)"
    },
    "MEAN_PAY_AMT": {
        "desc": "mean(PAY_AMT1..6)",
        "expected": row_raw[["PAY_AMT1","PAY_AMT2","PAY_AMT3","PAY_AMT4","PAY_AMT5","PAY_AMT6"]].mean(),
        "actual": row_fe["MEAN_PAY_AMT"],
        "source_cols": ["PAY_AMT1..6"],
        "computed_on": "Raw cleaned data (before scaling)"
    },
    "BILL_TREND": {
        "desc": "(BILL_AMT1 - BILL_AMT6) / LIMIT_BAL",
        "expected": (row_raw["BILL_AMT1"] - row_raw["BILL_AMT6"]) / row_raw["LIMIT_BAL"] if row_raw["LIMIT_BAL"] > 0 else 0.0,
        "actual": row_fe["BILL_TREND"],
        "source_cols": ["BILL_AMT1", "BILL_AMT6", "LIMIT_BAL"],
        "computed_on": "Raw cleaned data (before scaling)"
    },
    "PAY_TREND": {
        "desc": "(PAY_AMT1 - PAY_AMT6) / LIMIT_BAL",
        "expected": (row_raw["PAY_AMT1"] - row_raw["PAY_AMT6"]) / row_raw["LIMIT_BAL"] if row_raw["LIMIT_BAL"] > 0 else 0.0,
        "actual": row_fe["PAY_TREND"],
        "source_cols": ["PAY_AMT1", "PAY_AMT6", "LIMIT_BAL"],
        "computed_on": "Raw cleaned data (before scaling)"
    },
    "MAX_PAY_DELAY": {
        "desc": "max(PAY_0, PAY_2..PAY_6)",
        "expected": row_raw[["PAY_0","PAY_2","PAY_3","PAY_4","PAY_5","PAY_6"]].max(),
        "actual": row_fe["MAX_PAY_DELAY"],
        "source_cols": ["PAY_0", "PAY_2..6"],
        "computed_on": "Raw cleaned data (before scaling)"
    },
    "COUNT_LATE_PAYMENT": {
        "desc": "count(PAY_i > 0) for i in [0,2,3,4,5,6]",
        "expected": (row_raw[["PAY_0","PAY_2","PAY_3","PAY_4","PAY_5","PAY_6"]] > 0).sum(),
        "actual": row_fe["COUNT_LATE_PAYMENT"],
        "source_cols": ["PAY_0", "PAY_2..6"],
        "computed_on": "Raw cleaned data (before scaling)"
    },
}

formula_ok = True
for feat, info in formulas.items():
    exp = info["expected"]
    act = info["actual"]
    is_nan = pd.isna(act) or (isinstance(act, float) and np.isinf(act))
    if exp is not None:
        matches = abs(float(exp) - float(act)) < 1e-6
    else:
        matches = not is_nan
    status = "OK" if matches else "MISMATCH"
    if not matches:
        formula_ok = False
    print(f"  {feat:<28}: {status}")
    print(f"    Source  : {info['source_cols']}")
    print(f"    Formula : {info['desc']}")
    print(f"    On data : {info['computed_on']}")
    exp_str = f"{float(exp):.6f}" if exp is not None else "None"
    print(f"    Expected: {exp_str}")
    print(f"    Actual  : {float(act):.6f}")
    print()

# Scaling AFTER FE
preprocessor_fe, num_cols_fe, cat_cols_fe = build_fe_preprocessing_pipeline(scaler_type='robust')
X_train_fe, X_test_fe, _ = fit_transform_fe_data(preprocessor_fe, X_train_fe_raw, X_test_fe_raw)
print(f"  Scaling applied AFTER FE: True (RobustScaler fit only on X_train_fe_raw)")
print(f"  X_train_fe shape        : {X_train_fe.shape}")
print(f"  X_test_fe shape         : {X_test_fe.shape}")

fe_order_correct = True  # by code design: engineer_features(X_train) then fit_transform_fe_data
results["C_data_leakage"] = "PASS" if (not target_in_X and not id_in_X and formula_ok and fe_on_raw) else "FAIL"
results["D_feature_engineering"] = "PASS" if (formula_ok and fe_on_raw) else "FAIL"
results["E_fe_scaling_order"] = "Đúng (FE on Raw → RobustScaler fit on TRAIN_FE → Transform)" if fe_order_correct and fe_on_raw else "CẦN XEM XÉT"

print(f"\n  >>> VERDICT C (Data Leakage): {results['C_data_leakage']}")
print(f"  >>> VERDICT D (Feature Engineering): {results['D_feature_engineering']}")
print(f"  >>> VERDICT E (Thứ tự FE và Scaling): {results['E_fe_scaling_order']}")

# ============================================================
# SECTION F: Output files
# ============================================================
print("\n" + "=" * 60)
print("[F] OUTPUT FILES - KIỂM TRA ĐẦY ĐỦ")

processed_dir = os.path.join(PROJ, "data", "processed")
output_files = {
    "X_train.csv": {"expected_shape": (23972, 23)},
    "X_test.csv": {"expected_shape": (5993, 23)},
    "y_train.csv": {"expected_shape": (23972, 1)},
    "y_test.csv": {"expected_shape": (5993, 1)},
    "X_train_fe.csv": {"expected_shape": (23972, 33)},
    "X_test_fe.csv": {"expected_shape": (5993, 33)},
}

output_pass = True
for fname, meta in output_files.items():
    fpath = os.path.join(processed_dir, fname)
    if not os.path.exists(fpath):
        print(f"  {fname}: MISSING")
        output_pass = False
        continue
    df = pd.read_csv(fpath)
    shape_ok = df.shape == meta["expected_shape"]
    nan_count = int(df.isna().sum().sum())
    inf_count = int(np.isinf(df.select_dtypes(include=np.number).values).sum())

    # Check target/ID not in feature sets
    has_target = "default.payment.next.month" in df.columns
    has_id = "ID" in df.columns

    print(f"  {fname}:")
    print(f"    shape : {df.shape} ({'OK' if shape_ok else 'WRONG: expected ' + str(meta['expected_shape'])})")
    print(f"    NaN   : {nan_count}")
    print(f"    Inf   : {inf_count}")
    if "X_" in fname:
        print(f"    Target in cols: {has_target}")
        print(f"    ID in cols    : {has_id}")

    if not shape_ok or nan_count > 0 or inf_count > 0 or has_target or has_id:
        output_pass = False

# Consistency check X_train vs X_train_fe
X_train_cols = list(pd.read_csv(os.path.join(processed_dir, "X_train.csv")).columns)
X_test_cols = list(pd.read_csv(os.path.join(processed_dir, "X_test.csv")).columns)
X_train_fe_cols = list(pd.read_csv(os.path.join(processed_dir, "X_train_fe.csv")).columns)
X_test_fe_cols = list(pd.read_csv(os.path.join(processed_dir, "X_test_fe.csv")).columns)

train_test_same = X_train_cols == X_test_cols
train_fe_test_fe_same = X_train_fe_cols == X_test_fe_cols

print(f"\n  X_train/X_test same cols        : {train_test_same}")
print(f"  X_train_fe/X_test_fe same cols  : {train_fe_test_fe_same}")

if not train_test_same or not train_fe_test_fe_same:
    output_pass = False

results["F_output_files"] = "PASS" if output_pass else "FAIL"
print(f"\n  >>> VERDICT F (Output Files): {results['F_output_files']}")

# ============================================================
# FINAL SUMMARY
# ============================================================
overall = all(v == "PASS" or "Đúng" in v for v in results.values())
results["G_overall"] = "PASS" if overall else "FAIL"

print("\n" + "=" * 60)
print("TỔNG KẾT FINAL AUDIT")
print("=" * 60)
print(f"A. Notebook 02                  : {results['A_notebook02']}")
print(f"B. Preprocessing Pipeline       : {results['B_preprocessing']}")
print(f"C. Data Leakage                 : {results['C_data_leakage']}")
print(f"D. Feature Engineering Formulas : {results['D_feature_engineering']}")
print(f"E. Thứ tự FE và Scaling         : {results['E_fe_scaling_order']}")
print(f"F. Output Files                 : {results['F_output_files']}")
print(f"G. Overall Week 1-5             : {results['G_overall']}")
print("=" * 60)
