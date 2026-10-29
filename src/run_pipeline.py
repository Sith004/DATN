import os
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_full_pipeline():
    print("==================================================")
    print(" STARTING AUTOMATED END-TO-END PIPELINE RUNNER  ")
    print(" Project: F:\\DATN\\project")
    print(" Topic: Machine Learning in Credit Risk Assessment")
    print(" Scope: Week 1 to Week 5 (Data Audit -> FE -> Validation)")
    print("==================================================\n")

    # Step 1: Week 1-3 Data Audit & EDA
    print(">>> [STEP 1/4] Running Week 1-3: Data Audit & EDA...")
    from scripts.data_audit import run_data_audit
    run_data_audit()
    
    from scripts.generate_eda_assets import generate_eda_assets
    generate_eda_assets()
    
    import scripts.create_eda_notebook
    print("✓ Step 1 Complete: Data Audit, EDA Assets & 01_Data_Audit_EDA.ipynb generated.\n")

    # Step 2: Week 4 Preprocessing
    print(">>> [STEP 2/4] Running Week 4: Preprocessing & Data Leakage Control...")
    from src.preprocessing import run_preprocessing_pipeline
    run_preprocessing_pipeline()
    
    import scripts.build_preprocessing_notebook
    print("✓ Step 2 Complete: Preprocessing Pipeline & 02_Preprocessing.ipynb generated.\n")

    # Step 3: Week 5 Feature Engineering
    print(">>> [STEP 3/4] Running Week 5: Feature Engineering...")
    from src.feature_engineering import run_feature_engineering_pipeline
    run_feature_engineering_pipeline()
    
    import scripts.build_fe_notebook
    print("✓ Step 3 Complete: Feature Engineering Pipeline & 03_Feature_Engineering.ipynb generated.\n")

    # Step 4: Automated Validation
    print(">>> [STEP 4/4] Running Automated Pipeline Validation...")
    from src.validate_pipeline import validate_entire_pipeline
    success = validate_entire_pipeline()
    
    if success:
        print("\nALL WEEKS (1-5) COMPLETED SUCCESSFULLY WITH STATUS: PASS")
    else:
        print("\nPIPELINE VALIDATION COMPLETED WITH FAILURES.")
        sys.exit(1)

if __name__ == '__main__':
    run_full_pipeline()
