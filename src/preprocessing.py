import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, StandardScaler
from sklearn.pipeline import Pipeline

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def load_raw_data(filepath=None):
    """
    Tải tập dữ liệu thô từ đĩa.
    """
    if filepath is None:
        filepath = os.path.join('data', 'raw', 'UCI_Credit_Card.csv')
        if not os.path.exists(filepath):
            filepath = os.path.join('data', 'UCI_Credit_Card.csv')
            
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại {filepath}")
        
    df = pd.read_csv(filepath)
    return df

def clean_duplicates(df):
    """
    Kiểm tra và loại bỏ 35 dòng trùng lặp ở mức thuộc tính (bỏ qua cột ID).
    """
    feature_cols = [c for c in df.columns if c != 'ID']
    dup_mask = df.duplicated(subset=feature_cols, keep='first')
    num_dups = int(dup_mask.sum())
    
    df_cleaned = df[~dup_mask].copy().reset_index(drop=True)
    return df_cleaned, num_dups

def map_categorical_anomalies(df):
    """
    Chuyển đổi các mã danh mục chưa quy ước:
    - EDUCATION: 0, 5, 6 -> 4 (Others)
    - MARRIAGE: 0 -> 3 (Others)
    """
    df_mapped = df.copy()
    
    # EDUCATION mapping
    edu_map = {0: 4, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4}
    df_mapped['EDUCATION'] = df_mapped['EDUCATION'].map(edu_map)
    
    # MARRIAGE mapping
    marr_map = {0: 3, 1: 1, 2: 2, 3: 3}
    df_mapped['MARRIAGE'] = df_mapped['MARRIAGE'].map(marr_map)
    
    return df_mapped

def separate_features_target(df, target_col='default.payment.next.month', id_col='ID'):
    """
    Tách không gian thuộc tính X và biến mục tiêu y.
    Loại cột ID khỏi X để phòng rò rỉ thông tin index.
    """
    X = df.drop(columns=[id_col, target_col])
    y = df[target_col].copy()
    return X, y

def split_train_test(X, y, test_size=0.20, random_state=42):
    """
    Chia tập TRAIN/TEST theo tỷ lệ 80/20 có phân tầng (stratify=y).
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )
    return X_train, X_test, y_train, y_test

def build_preprocessing_pipeline(scaler_type='robust'):
    """
    Xây dựng ColumnTransformer để xử lý dữ liệu số và danh mục:
    - RobustScaler cho các biến numerical (giảm ảnh hưởng của extreme outliers ở PAY_AMT).
    - Passthrough cho các biến categorical/ordinal (SEX, EDUCATION, MARRIAGE, PAY_0..6).
    """
    num_cols = ['LIMIT_BAL', 'AGE'] + [f'BILL_AMT{i}' for i in range(1, 7)] + [f'PAY_AMT{i}' for i in range(1, 7)]
    cat_cols = ['SEX', 'EDUCATION', 'MARRIAGE', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
    
    if scaler_type == 'robust':
        scaler = RobustScaler()
    elif scaler_type == 'standard':
        scaler = StandardScaler()
    else:
        scaler = RobustScaler()
        
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', scaler, num_cols),
            ('cat', 'passthrough', cat_cols)
        ],
        remainder='drop'
    )
    
    return preprocessor, num_cols, cat_cols

def fit_transform_data(preprocessor, X_train, X_test):
    """
    FIT PREPROCESSING CHỈ TRÊN TRAIN, transform cả TRAIN và TEST.
    """
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)
    
    feature_names = preprocessor.get_feature_names_out()
    
    X_train_df = pd.DataFrame(X_train_proc, columns=feature_names, index=X_train.index)
    X_test_df = pd.DataFrame(X_test_proc, columns=feature_names, index=X_test.index)
    
    return X_train_df, X_test_df, preprocessor

def save_processed_data(X_train_df, X_test_df, y_train, y_test, output_dir=None):
    """
    Lưu dữ liệu đã tiền xử lý vào thư mục data/processed.
    """
    if output_dir is None:
        output_dir = os.path.join('data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    
    X_train_df.to_csv(os.path.join(output_dir, 'X_train.csv'), index=False)
    X_test_df.to_csv(os.path.join(output_dir, 'X_test.csv'), index=False)
    y_train.to_csv(os.path.join(output_dir, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(output_dir, 'y_test.csv'), index=False)
    
    print(f"Saved processed datasets to {output_dir}")

def run_preprocessing_pipeline():
    """
    Thực thi toàn bộ quy trình pipeline từ thô đến tập xử lý hoàn chỉnh.
    """
    print("=== STARTING PREPROCESSING PIPELINE ===")
    df_raw = load_raw_data()
    print(f"1. Raw dataset shape: {df_raw.shape[0]} rows x {df_raw.shape[1]} columns")
    
    df_cleaned, num_dups = clean_duplicates(df_raw)
    print(f"2. Removed {num_dups} duplicate rows. Cleaned shape: {df_cleaned.shape[0]} rows")
    
    df_mapped = map_categorical_anomalies(df_cleaned)
    print("3. Standardized category codes: EDUCATION (0,5,6 -> 4) and MARRIAGE (0 -> 3)")
    
    X, y = separate_features_target(df_mapped)
    print(f"4. Separated ID from X. X shape: {X.shape}, y shape: {y.shape}")
    
    X_train, X_test, y_train, y_test = split_train_test(X, y, test_size=0.20, random_state=42)
    print(f"5. Train/Test Split (80/20): TRAIN = {len(X_train)} ({y_train.mean()*100:.2f}% target), TEST = {len(X_test)} ({y_test.mean()*100:.2f}% target)")
    
    preprocessor, num_cols, cat_cols = build_preprocessing_pipeline(scaler_type='robust')
    X_train_proc, X_test_proc, fitted_preprocessor = fit_transform_data(preprocessor, X_train, X_test)
    print("6. Fit RobustScaler ONLY on TRAIN. Successfully transformed TRAIN and TEST.")
    
    save_processed_data(X_train_proc, X_test_proc, y_train, y_test)
    print("=== PREPROCESSING PIPELINE COMPLETE ===")
    
    return X_train_proc, X_test_proc, y_train, y_test

if __name__ == '__main__':
    run_preprocessing_pipeline()
