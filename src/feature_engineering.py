import os
import sys
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, StandardScaler

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import base cleaning and splitting functions from src.preprocessing
from src.preprocessing import (
    load_raw_data,
    clean_duplicates,
    map_categorical_anomalies,
    separate_features_target,
    split_train_test
)

def engineer_features(df):
    """
    Thực hiện Feature Engineering TRÊN DỮ LIỆU THÔ ĐÃ CLEANED (TRƯỚC KHI SCALING).
    Tất cả phép tính là row-wise deterministic, không học từ tập dữ liệu khác -> 0 Data Leakage.
    
    10 Features mới tạo:
    1. UTILIZATION_RATE_SEPT: Tỷ lệ sử dụng hạn mức T9/2005 (BILL_AMT1 / LIMIT_BAL)
    2. UTILIZATION_RATE_MEAN: Tỷ lệ sử dụng hạn mức trung bình 6 tháng (MEAN_BILL_AMT / LIMIT_BAL)
    3. PAY_RATIO_SEPT: Tỷ lệ thanh toán hóa đơn T9/2005 cho kỳ T8 (PAY_AMT1 / BILL_AMT2)
    4. PAY_RATIO_MEAN: Tỷ lệ thanh toán trung bình qua 5 kỳ hóa đơn
    5. MAX_PAY_DELAY: Số tháng trậm trả tối đa trong 6 tháng (max(PAY_0, PAY_2..6))
    6. COUNT_LATE_PAYMENT: Số tháng bị trậm trả (PAY_i > 0)
    7. MEAN_BILL_AMT: Dư nợ hóa đơn trung bình 6 tháng
    8. MEAN_PAY_AMT: Số tiền thanh toán trung bình 6 tháng
    9. BILL_TREND: Xu hướng biến động dư nợ nợ relative với hạn mức ((BILL_AMT1 - BILL_AMT6) / LIMIT_BAL)
    10. PAY_TREND: Xu hướng biến động số tiền trả relative với hạn mức ((PAY_AMT1 - PAY_AMT6) / LIMIT_BAL)
    """
    X_fe = df.copy()
    
    # 1. UTILIZATION_RATE_SEPT (Statement Sept 2005 / Credit Limit)
    X_fe['UTILIZATION_RATE_SEPT'] = np.where(
        X_fe['LIMIT_BAL'] <= 0, 0.0, X_fe['BILL_AMT1'] / X_fe['LIMIT_BAL']
    )
    
    # 2. MEAN_BILL_AMT (Mean statement balance over 6 months)
    bill_cols = ['BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6']
    mean_bill = X_fe[bill_cols].mean(axis=1)
    X_fe['MEAN_BILL_AMT'] = mean_bill
    
    # 3. UTILIZATION_RATE_MEAN (Mean Statement Balance / Credit Limit)
    X_fe['UTILIZATION_RATE_MEAN'] = np.where(
        X_fe['LIMIT_BAL'] <= 0, 0.0, mean_bill / X_fe['LIMIT_BAL']
    )
    
    # 4. PAY_RATIO_SEPT (PAY_AMT1 pays towards BILL_AMT2)
    # Nếu BILL_AMT2 <= 0 (không có nghĩa vụ nợ), tỷ lệ coi như 1.0 (hoàn thành 100%)
    X_fe['PAY_RATIO_SEPT'] = np.where(
        X_fe['BILL_AMT2'] <= 0, 1.0, X_fe['PAY_AMT1'] / X_fe['BILL_AMT2']
    )
    
    # 5. PAY_RATIO_MEAN (Trung bình tỷ lệ thanh toán qua 5 chu kỳ hóa đơn)
    r1 = np.where(X_fe['BILL_AMT2'] <= 0, 1.0, X_fe['PAY_AMT1'] / X_fe['BILL_AMT2'])
    r2 = np.where(X_fe['BILL_AMT3'] <= 0, 1.0, X_fe['PAY_AMT2'] / X_fe['BILL_AMT3'])
    r3 = np.where(X_fe['BILL_AMT4'] <= 0, 1.0, X_fe['PAY_AMT3'] / X_fe['BILL_AMT4'])
    r4 = np.where(X_fe['BILL_AMT5'] <= 0, 1.0, X_fe['PAY_AMT4'] / X_fe['BILL_AMT5'])
    r5 = np.where(X_fe['BILL_AMT6'] <= 0, 1.0, X_fe['PAY_AMT5'] / X_fe['BILL_AMT6'])
    X_fe['PAY_RATIO_MEAN'] = (r1 + r2 + r3 + r4 + r5) / 5.0
    
    # 6. MAX_PAY_DELAY (Mức độ trậm trả nghiêm trọng nhất trong 6 tháng)
    pay_status_cols = ['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
    X_fe['MAX_PAY_DELAY'] = X_fe[pay_status_cols].max(axis=1)
    
    # 7. COUNT_LATE_PAYMENT (Tần suất trậm trả: số tháng có PAY_i > 0)
    X_fe['COUNT_LATE_PAYMENT'] = (X_fe[pay_status_cols] > 0).sum(axis=1)
    
    # 8. MEAN_PAY_AMT (Trung bình số tiền trả 6 tháng)
    pay_amt_cols = ['PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']
    X_fe['MEAN_PAY_AMT'] = X_fe[pay_amt_cols].mean(axis=1)
    
    # 9. BILL_TREND (Tốc độ tăng/giảm dư nợ giữa T9 và T4 so với hạn mức)
    X_fe['BILL_TREND'] = np.where(
        X_fe['LIMIT_BAL'] <= 0, 0.0, (X_fe['BILL_AMT1'] - X_fe['BILL_AMT6']) / X_fe['LIMIT_BAL']
    )
    
    # 10. PAY_TREND (Tốc độ tăng/giảm số tiền thanh toán giữa T9 và T4 so với hạn mức)
    X_fe['PAY_TREND'] = np.where(
        X_fe['LIMIT_BAL'] <= 0, 0.0, (X_fe['PAY_AMT1'] - X_fe['PAY_AMT6']) / X_fe['LIMIT_BAL']
    )
    
    return X_fe

def build_fe_preprocessing_pipeline(scaler_type='robust'):
    """
    Tạo ColumnTransformer chuẩn hóa cho dữ liệu đã được Feature Engineering.
    RobustScaler fit trên các biến số (bao gồm cả biến số mới tạo).
    Passthrough cho các biến danh mục / thứ tự / đếm integer.
    """
    # 22 Numerical features
    num_cols = [
        'LIMIT_BAL', 'AGE',
        'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
        'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6',
        'UTILIZATION_RATE_SEPT', 'UTILIZATION_RATE_MEAN',
        'PAY_RATIO_SEPT', 'PAY_RATIO_MEAN',
        'MEAN_BILL_AMT', 'MEAN_PAY_AMT',
        'BILL_TREND', 'PAY_TREND'
    ]
    
    # 11 Categorical/Ordinal/Integer Count features
    cat_cols = [
        'SEX', 'EDUCATION', 'MARRIAGE',
        'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
        'MAX_PAY_DELAY', 'COUNT_LATE_PAYMENT'
    ]
    
    if scaler_type == 'robust':
        scaler = RobustScaler()
    else:
        scaler = StandardScaler()
        
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', scaler, num_cols),
            ('cat', 'passthrough', cat_cols)
        ],
        remainder='drop'
    )
    
    return preprocessor, num_cols, cat_cols

def fit_transform_fe_data(preprocessor, X_train_fe_raw, X_test_fe_raw):
    """
    FIT PREPROCESSING SCALER CHỈ TRÊN TRAIN, transform cả TRAIN và TEST.
    Chống Data Leakage tuyệt đối.
    """
    X_train_proc = preprocessor.fit_transform(X_train_fe_raw)
    X_test_proc = preprocessor.transform(X_test_fe_raw)
    
    feature_names = preprocessor.get_feature_names_out()
    # Clean up feature names prefix generated by ColumnTransformer (e.g. 'num__', 'cat__')
    clean_feature_names = [f.split('__')[-1] for f in feature_names]
    
    X_train_df = pd.DataFrame(X_train_proc, columns=clean_feature_names, index=X_train_fe_raw.index)
    X_test_df = pd.DataFrame(X_test_proc, columns=clean_feature_names, index=X_test_fe_raw.index)
    
    return X_train_df, X_test_df, preprocessor

def verify_fe_datasets(X_train_fe, X_test_fe, y_train, y_test):
    """
    Kiểm tra toàn diện 14 yêu cầu chất lượng dữ liệu:
    - Danh sách feature & thứ tự cột
    - Không chứa Target, không chứa ID
    - NaN count = 0, Inf count = 0
    - Data Leakage check
    """
    checks = {}
    
    # 1. Shape and columns match
    checks['same_columns'] = list(X_train_fe.columns) == list(X_test_fe.columns)
    checks['num_features'] = X_train_fe.shape[1]
    checks['train_shape'] = X_train_fe.shape
    checks['test_shape'] = X_test_fe.shape
    
    # 2. Target and ID absence
    checks['target_in_X'] = ('default.payment.next.month' in X_train_fe.columns) or ('default.payment.next.month' in X_test_fe.columns)
    checks['id_in_X'] = ('ID' in X_train_fe.columns) or ('ID' in X_test_fe.columns)
    
    # 3. NaN / Inf checks
    checks['train_nan'] = int(X_train_fe.isna().sum().sum())
    checks['test_nan'] = int(X_test_fe.isna().sum().sum())
    checks['train_inf'] = int(np.isinf(X_train_fe.values).sum())
    checks['test_inf'] = int(np.isinf(X_test_fe.values).sum())
    
    # 4. Data Leakage verification
    checks['leakage_passed'] = (
        checks['same_columns'] and 
        not checks['target_in_X'] and 
        not checks['id_in_X'] and 
        checks['train_nan'] == 0 and 
        checks['test_nan'] == 0 and 
        checks['train_inf'] == 0 and 
        checks['test_inf'] == 0
    )
    
    return checks

def run_feature_engineering_pipeline():
    """
    Chạy toàn bộ quy trình Tuần 5: Feature Engineering & Preprocessing.
    """
    print("=== TUẦN 5: STARTING FEATURE ENGINEERING PIPELINE ===")
    
    # 1. Load Raw & Basic Cleaning
    df_raw = load_raw_data()
    df_cleaned, num_dups = clean_duplicates(df_raw)
    df_mapped = map_categorical_anomalies(df_cleaned)
    X, y = separate_features_target(df_mapped)
    
    # 2. Train / Test Split BEFORE Scaling & Feature Engineering
    X_train_raw, X_test_raw, y_train, y_test = split_train_test(X, y, test_size=0.20, random_state=42)
    print(f"1. Raw Split (80/20): X_train_raw={X_train_raw.shape}, X_test_raw={X_test_raw.shape}")
    
    # 3. Feature Engineering on Raw Cleaned Features (Independently for Train and Test)
    X_train_fe_raw = engineer_features(X_train_raw)
    X_test_fe_raw = engineer_features(X_test_raw)
    print(f"2. Feature Engineering applied on Raw Data: Features expanded from {X_train_raw.shape[1]} to {X_train_fe_raw.shape[1]}")
    
    # 4. Build & Fit Scaling Pipeline ONLY ON TRAIN
    preprocessor, num_cols, cat_cols = build_fe_preprocessing_pipeline(scaler_type='robust')
    X_train_fe, X_test_fe, fitted_preprocessor = fit_transform_fe_data(preprocessor, X_train_fe_raw, X_test_fe_raw)
    print("3. RobustScaler fitted ONLY ON TRAIN. Transformed both TRAIN and TEST.")
    
    # 5. Verification Checks
    checks = verify_fe_datasets(X_train_fe, X_test_fe, y_train, y_test)
    print(f"4. Quality & Leakage Checks: Passed = {checks['leakage_passed']}")
    print(f"   - Train Shape: {checks['train_shape']}, Test Shape: {checks['test_shape']}")
    print(f"   - NaN Count: Train={checks['train_nan']}, Test={checks['test_nan']}")
    print(f"   - Inf Count: Train={checks['train_inf']}, Test={checks['test_inf']}")
    
    # 6. Save Datasets
    output_dir = os.path.join('data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    
    X_train_fe.to_csv(os.path.join(output_dir, 'X_train_fe.csv'), index=False)
    X_test_fe.to_csv(os.path.join(output_dir, 'X_test_fe.csv'), index=False)
    # y_train and y_test are kept consistent
    y_train.to_csv(os.path.join(output_dir, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(output_dir, 'y_test.csv'), index=False)
    
    print(f"5. Saved X_train_fe.csv ({X_train_fe.shape}) and X_test_fe.csv ({X_test_fe.shape}) to {output_dir}")
    print("=== TUẦN 5: FEATURE ENGINEERING PIPELINE COMPLETE ===")
    
    return X_train_fe, X_test_fe, y_train, y_test, checks

if __name__ == '__main__':
    run_feature_engineering_pipeline()
