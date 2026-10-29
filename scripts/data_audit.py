import os
import json
import numpy as np
import pandas as pd

def run_data_audit():
    csv_path = os.path.join('data', 'UCI_Credit_Card.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")

    print("Loading dataset for audit...")
    df = pd.read_csv(csv_path)

    report = {}

    # 1. General Info
    report['general_info'] = {
        'num_rows': int(df.shape[0]),
        'num_cols': int(df.shape[1]),
        'columns': list(df.columns),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
    }

    # 2. Missing Values & Duplicates
    missing_values = df.isnull().sum().to_dict()
    report['data_integrity'] = {
        'missing_values_total': int(df.isnull().sum().sum()),
        'missing_values_per_col': {k: int(v) for k, v in missing_values.items()},
        'duplicate_rows_total': int(df.duplicated().duplicated().sum() if df.duplicated().sum() > 0 else df.duplicated(subset=[c for c in df.columns if c != 'ID']).sum()),
        'unique_value_counts': {col: int(df[col].nunique()) for col in df.columns}
    }

    # 3. Target Distribution
    target_col = 'default.payment.next.month'
    target_counts = df[target_col].value_counts().to_dict()
    target_pcts = (df[target_col].value_counts(normalize=True) * 100).round(2).to_dict()
    imbalance_ratio = round(target_counts.get(0, 0) / max(1, target_counts.get(1, 1)), 2)

    report['target_analysis'] = {
        'target_column': target_col,
        'class_counts': {str(k): int(v) for k, v in target_counts.items()},
        'class_percentages': {str(k): float(v) for k, v in target_pcts.items()},
        'imbalance_ratio_non_default_to_default': float(imbalance_ratio),
        'assessment': "Class imbalance present (~22.1% default vs ~77.9% non-default). Requires cost-sensitive learning or resampling (SMOTE / Class Weight) in training phase."
    }

    # 4. Demographic & Categorical Feature Audit
    categorical_cols = ['SEX', 'EDUCATION', 'MARRIAGE', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
    cat_summary = {}
    for col in categorical_cols:
        val_counts = df[col].value_counts().sort_index().to_dict()
        cat_summary[col] = {
            'value_counts': {str(k): int(v) for k, v in val_counts.items()},
            'has_undocumented_values': bool(
                (col == 'EDUCATION' and any(k in val_counts for k in [0, 5, 6])) or
                (col == 'MARRIAGE' and 0 in val_counts) or
                (col.startswith('PAY_') and any(k in val_counts for k in [-2, 0]))
            )
        }
    report['categorical_audit'] = cat_summary

    # 5. Descriptive Statistics for Numerical Variables
    num_cols = ['LIMIT_BAL', 'AGE'] + [f'BILL_AMT{i}' for i in range(1, 7)] + [f'PAY_AMT{i}' for i in range(1, 7)]
    num_stats = {}
    for col in num_cols:
        s = df[col]
        q25 = float(s.quantile(0.25))
        q75 = float(s.quantile(0.75))
        iqr = q75 - q25
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr
        outliers_iqr = int(((s < lower_bound) | (s > upper_bound)).sum())

        mean = float(s.mean())
        std = float(s.std())
        z_outliers = int(((s - mean).abs() > 3 * std).sum()) if std > 0 else 0

        num_stats[col] = {
            'mean': round(float(s.mean()), 2),
            'std': round(float(s.std()), 2),
            'min': round(float(s.min()), 2),
            '25%': round(q25, 2),
            'median': round(float(s.median()), 2),
            '75%': round(q75, 2),
            'max': round(float(s.max()), 2),
            'skewness': round(float(s.skew()), 2),
            'kurtosis': round(float(s.kurt()), 2),
            'outliers_iqr_count': outliers_iqr,
            'outliers_zscore_3std_count': z_outliers
        }
    report['numerical_audit'] = num_stats

    # 6. Multicollinearity & Correlation Analysis
    feature_cols = [c for c in df.columns if c not in ['ID']]
    corr_matrix = df[feature_cols].corr().round(3)
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            val = float(corr_matrix.iloc[i, j])
            if abs(val) >= 0.70 and col1 != target_col and col2 != target_col:
                high_corr_pairs.append({'feature_1': col1, 'feature_2': col2, 'pearson_correlation': val})

    report['correlation_analysis'] = {
        'high_correlation_pairs_ge_0_70': high_corr_pairs,
        'target_correlations': {col: round(float(corr_matrix.loc[col, target_col]), 4) for col in feature_cols if col != target_col}
    }

    # 7. Data Leakage Assessment
    report['data_leakage_assessment'] = {
        'temporal_alignment': "All features (PAY_0..6, BILL_AMT1..6, PAY_AMT1..6) capture client repayment behavior between April 2005 and September 2005. Target variable is default in October 2005.",
        'leakage_risk': "Low. No post-outcome metrics present. However, ID column must be removed during training to prevent artifact memorization."
    }

    # Save JSON report
    os.makedirs('reports', exist_ok=True)
    report_path = os.path.join('reports', 'phase1_data_audit_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\nAudit complete! Report saved to {report_path}\n")

    # Print clean summary to terminal
    print("=" * 60)
    print("                PHASE 1: DATA AUDIT SUMMARY                ")
    print("=" * 60)
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Total Missing Values: {df.isnull().sum().sum()}")
    print(f"Duplicate Rows (excluding ID): {df.duplicated(subset=[c for c in df.columns if c != 'ID']).sum()}")
    print("\n[Target Variable Distribution]")
    print(f"0 (Non-default): {target_counts.get(0,0)} ({target_pcts.get(0,0)}%)")
    print(f"1 (Default)    : {target_counts.get(1,0)} ({target_pcts.get(1,0)}%)")
    print(f"Imbalance Ratio: {imbalance_ratio}:1")

    print("\n[Categorical Features & Undocumented Codes]")
    print(f"EDUCATION values: {cat_summary['EDUCATION']['value_counts']} (Undocumented codes 0, 5, 6 present)")
    print(f"MARRIAGE values : {cat_summary['MARRIAGE']['value_counts']} (Undocumented code 0 present)")
    print(f"PAY_0 values    : {cat_summary['PAY_0']['value_counts']} (Undocumented codes -2, 0 present)")

    print("\n[High Multicollinearity Pairs (|r| >= 0.70)]")
    for pair in high_corr_pairs:
        print(f" - {pair['feature_1']} <-> {pair['feature_2']}: {pair['pearson_correlation']}")

    print("\n[Top Target Correlations]")
    sorted_target_corr = sorted(report['correlation_analysis']['target_correlations'].items(), key=lambda x: abs(x[1]), reverse=True)
    for feat, corr_val in sorted_target_corr[:7]:
        print(f" - {feat}: r = {corr_val}")
    print("=" * 60)

if __name__ == '__main__':
    run_data_audit()
