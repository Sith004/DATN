import os
files = [
    'notebooks/05_Ensemble_Models.ipynb',
    'src/ensemble_models.py',
    'reports/Week7_Ensemble_Models_Report.md',
    'reports/week7_model_comparison.csv',
    'reports/figures/week7_rf_default_confusion_matrix.png',
    'reports/figures/week7_rf_balanced_confusion_matrix.png',
    'reports/figures/week7_xgboost_confusion_matrix.png',
    'reports/figures/week7_roc_curve_comparison.png',
    'reports/figures/week7_pr_curve_comparison.png',
    'reports/figures/week7_random_forest_feature_importance.png',
    'reports/figures/week7_xgboost_feature_importance.png',
    'reports/figures/week7_full_comparison.png',
    'models/random_forest_baseline.pkl',
    'models/random_forest_balanced.pkl',
    'models/xgboost_baseline.pkl',
]
print('FILE CHECK:')
all_ok = True
for f in files:
    ok = os.path.exists(f)
    sz = os.path.getsize(f) if ok else 0
    status = 'OK' if ok else 'MISS'
    if ok:
        print(f'  [{status}] {f}  ({sz:,} bytes)')
    else:
        print(f'  [{status}] {f}')
    all_ok = all_ok and ok
print()
print('ALL FILES OK' if all_ok else 'SOME FILES MISSING')
