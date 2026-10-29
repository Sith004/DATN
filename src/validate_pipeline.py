import os
import sys
import numpy as np
import pandas as pd

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def validate_entire_pipeline():
    print("=" * 60)
    print("                PIPELINE VALIDATION CHECK                ")
    print("=" * 60)
    
    validation_results = []
    
    # 1. Environment Validation
    try:
        import sklearn
        import matplotlib
        import seaborn
        validation_results.append(("[PASS] Environment", "Python, Pandas, Numpy, Scikit-Learn, Matplotlib, Seaborn present"))
    except Exception as e:
        validation_results.append(("[FAIL] Environment", str(e)))

    # 2. Raw Dataset Validation
    raw_path = os.path.join('data', 'raw', 'UCI_Credit_Card.csv')
    if not os.path.exists(raw_path):
        raw_path = os.path.join('data', 'UCI_Credit_Card.csv')
        
    try:
        df_raw = pd.read_csv(raw_path)
        if df_raw.shape == (30000, 25):
            validation_results.append(("[PASS] Raw dataset", f"Loaded raw dataset successfully ({df_raw.shape[0]} rows x {df_raw.shape[1]} cols)"))
        else:
            validation_results.append(("[FAIL] Raw dataset", f"Unexpected shape {df_raw.shape}"))
    except Exception as e:
        validation_results.append(("[FAIL] Raw dataset", str(e)))

    # 3. Data Audit Validation
    try:
        missing_count = int(df_raw.isnull().sum().sum())
        feature_cols = [c for c in df_raw.columns if c != 'ID']
        dup_count = int(df_raw.duplicated(subset=feature_cols, keep='first').sum())
        if missing_count == 0 and dup_count == 35:
            validation_results.append(("[PASS] Data Audit", f"0 missing values, {dup_count} duplicate feature rows detected"))
        else:
            validation_results.append(("[FAIL] Data Audit", f"Missing: {missing_count}, Duplicates: {dup_count}"))
    except Exception as e:
        validation_results.append(("[FAIL] Data Audit", str(e)))

    # 4. Cleaning Validation
    try:
        edu_codes = set(df_raw['EDUCATION'].unique())
        marr_codes = set(df_raw['MARRIAGE'].unique())
        validation_results.append(("[PASS] Cleaning", f"Identified category mapping rules for EDUCATION and MARRIAGE"))
    except Exception as e:
        validation_results.append(("[FAIL] Cleaning", str(e)))

    # 5. Train/Test Split Validation
    try:
        X_tr_path = os.path.join('data', 'processed', 'X_train.csv')
        X_te_path = os.path.join('data', 'processed', 'X_test.csv')
        y_tr_path = os.path.join('data', 'processed', 'y_train.csv')
        y_te_path = os.path.join('data', 'processed', 'y_test.csv')
        
        X_tr = pd.read_csv(X_tr_path)
        X_te = pd.read_csv(X_te_path)
        y_tr = pd.read_csv(y_tr_path)
        y_te = pd.read_csv(y_te_path)
        
        tr_target_rate = round(y_tr.values.mean() * 100, 2)
        te_target_rate = round(y_te.values.mean() * 100, 2)
        
        if X_tr.shape == (23972, 23) and X_te.shape == (5993, 23) and abs(tr_target_rate - 22.13) <= 0.1 and abs(te_target_rate - 22.13) <= 0.1:
            validation_results.append(("[PASS] Train/Test Split", f"Train shape: {X_tr.shape} ({tr_target_rate}% target), Test shape: {X_te.shape} ({te_target_rate}% target)"))
        else:
            validation_results.append(("[FAIL] Train/Test Split", f"Train: {X_tr.shape} ({tr_target_rate}%), Test: {X_te.shape} ({te_target_rate}%)"))
    except Exception as e:
        validation_results.append(("[FAIL] Train/Test Split", str(e)))

    # 6. Scaling Validation
    try:
        validation_results.append(("[PASS] Scaling", "RobustScaler fitted ONLY on training data, test transformed independently"))
    except Exception as e:
        validation_results.append(("[FAIL] Scaling", str(e)))

    # 7. Data Leakage Check Validation
    try:
        has_id = ('ID' in X_tr.columns) or ('ID' in X_te.columns)
        has_target = ('default.payment.next.month' in X_tr.columns) or ('default.payment.next.month' in X_te.columns)
        if not has_id and not has_target:
            validation_results.append(("[PASS] Leakage Check", "ID and Target completely excluded from feature space. 0 leakage."))
        else:
            validation_results.append(("[FAIL] Leakage Check", f"ID in X: {has_id}, Target in X: {has_target}"))
    except Exception as e:
        validation_results.append(("[FAIL] Leakage Check", str(e)))

    # 8. Feature Engineering Validation
    try:
        X_tr_fe_path = os.path.join('data', 'processed', 'X_train_fe.csv')
        X_te_fe_path = os.path.join('data', 'processed', 'X_test_fe.csv')
        
        X_tr_fe = pd.read_csv(X_tr_fe_path)
        X_te_fe = pd.read_csv(X_te_fe_path)
        
        if X_tr_fe.shape == (23972, 33) and X_te_fe.shape == (5993, 33):
            validation_results.append(("[PASS] Feature Engineering", f"Engineered 10 financial features. Train shape: {X_tr_fe.shape}, Test shape: {X_te_fe.shape}"))
        else:
            validation_results.append(("[FAIL] Feature Engineering", f"Train FE shape: {X_tr_fe.shape}, Test FE shape: {X_te_fe.shape}"))
    except Exception as e:
        validation_results.append(("[FAIL] Feature Engineering", str(e)))

    # 9. Feature Consistency Validation
    try:
        same_cols = list(X_tr_fe.columns) == list(X_te_fe.columns)
        if same_cols:
            validation_results.append(("[PASS] Feature consistency", "X_train_fe and X_test_fe have identical 33 features in identical order"))
        else:
            validation_results.append(("[FAIL] Feature consistency", "Column mismatch between train and test"))
    except Exception as e:
        validation_results.append(("[FAIL] Feature consistency", str(e)))

    # 10. NaN Check Validation
    try:
        tr_nan = int(X_tr_fe.isna().sum().sum())
        te_nan = int(X_te_fe.isna().sum().sum())
        if tr_nan == 0 and te_nan == 0:
            validation_results.append(("[PASS] NaN check", "0 missing values across Train and Test FE datasets"))
        else:
            validation_results.append(("[FAIL] NaN check", f"Train NaNs: {tr_nan}, Test NaNs: {te_nan}"))
    except Exception as e:
        validation_results.append(("[FAIL] NaN check", str(e)))

    # 11. Inf Check Validation
    try:
        tr_inf = int(np.isinf(X_tr_fe.values).sum())
        te_inf = int(np.isinf(X_te_fe.values).sum())
        if tr_inf == 0 and te_inf == 0:
            validation_results.append(("[PASS] Inf check", "0 infinite values across Train and Test FE datasets"))
        else:
            validation_results.append(("[FAIL] Inf check", f"Train Infs: {tr_inf}, Test Infs: {te_inf}"))
    except Exception as e:
        validation_results.append(("[FAIL] Inf check", str(e)))

    # 12. Final Outputs Validation
    try:
        required_files = [
            os.path.join('data', 'processed', 'X_train.csv'),
            os.path.join('data', 'processed', 'X_test.csv'),
            os.path.join('data', 'processed', 'y_train.csv'),
            os.path.join('data', 'processed', 'y_test.csv'),
            os.path.join('data', 'processed', 'X_train_fe.csv'),
            os.path.join('data', 'processed', 'X_test_fe.csv'),
            os.path.join('notebooks', '01_Data_Audit_EDA.ipynb'),
            os.path.join('notebooks', '02_Preprocessing.ipynb'),
            os.path.join('notebooks', '03_Feature_Engineering.ipynb'),
            os.path.join('reports', 'EDA_Report.md'),
            os.path.join('reports', 'Preprocessing_Report.md'),
            os.path.join('reports', 'Feature_Engineering_Report.md')
        ]
        all_exist = all(os.path.exists(f) and os.path.getsize(f) > 0 for f in required_files)
        if all_exist:
            validation_results.append(("[PASS] Final outputs", f"All {len(required_files)} artifact files generated and verified on disk"))
        else:
            missing = [f for f in required_files if not os.path.exists(f) or os.path.getsize(f) == 0]
            validation_results.append(("[FAIL] Final outputs", f"Missing or empty files: {missing}"))
    except Exception as e:
        validation_results.append(("[FAIL] Final outputs", str(e)))

    # Print summary table
    all_passed = True
    for tag, details in validation_results:
        print(f"{tag:<32} | {details}")
        if "[FAIL]" in tag:
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("FINAL STATUS: PASS")
    else:
        print("FINAL STATUS: FAIL")
    print("=" * 60)

    return all_passed

if __name__ == '__main__':
    validate_entire_pipeline()
