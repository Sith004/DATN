import os
import pandas as pd

def convert_xls_to_csv():
    xls_path = os.path.join('data', 'default of credit card clients.xls')
    csv_path = os.path.join('data', 'UCI_Credit_Card.csv')
    
    if not os.path.exists(xls_path):
        raise FileNotFoundError(f"Source file not found at {xls_path}")
        
    print(f"Reading {xls_path}...")
    # Row 0 contains column descriptions, Row 1 contains actual column headers X1..X23 / ID / default
    df = pd.read_excel(xls_path, header=1)
    
    # Clean up column names: rename 'default payment next month' or 'default.payment.next.month'
    df.columns = [str(col).strip() for col in df.columns]
    
    # Standardize target column name if needed
    target_col = None
    for col in df.columns:
        if 'default' in col.lower():
            target_col = col
            break
            
    if target_col and target_col != 'default.payment.next.month':
        df.rename(columns={target_col: 'default.payment.next.month'}, inplace=True)
        
    print(f"Dataset shape: {df.shape}")
    print("Columns:", list(df.columns))
    
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV to {csv_path}")

if __name__ == '__main__':
    convert_xls_to_csv()
