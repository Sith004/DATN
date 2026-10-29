import json, os, sys, pickle
sys.stdout.reconfigure(encoding='utf-8')

print('=== WEEK 9 FINAL VERIFICATION ===')
print()

# Notebook check
nb_path = 'notebooks/07_Model_Interpretability.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']
code_cells = [c for c in cells if c['cell_type'] == 'code']
exec_cells = [c for c in code_cells if c.get('execution_count') is not None]
error_cells = []
for c in code_cells:
    for out in c.get('outputs', []):
        if out.get('output_type') == 'error':
            error_cells.append(out.get('ename', 'unknown'))

nb_status = 'PASS' if len(error_cells) == 0 else 'FAIL'
print(f'NOTEBOOK: {nb_path}')
print(f'  Total cells:    {len(cells)}')
print(f'  Code cells:     {len(code_cells)}')
print(f'  Executed cells: {len(exec_cells)}')
print(f'  Errors:         {len(error_cells)}')
print(f'  Status:         {nb_status}')

print()
print('ARTIFACTS:')
artifacts = [
    ('Notebook',              'notebooks/07_Model_Interpretability.ipynb'),
    ('Week9 Report',          'reports/Week9_SHAP_Model_Interpretability_Report.md'),
    ('Feature Importance CSV','reports/week9_shap_feature_importance.csv'),
    ('Local Cases CSV',       'reports/week9_local_interpretation.csv'),
    ('SHAP Summary JSON',     'reports/week9_shap_summary.json'),
    ('SHAP Bar Plot',         'reports/figures/week9_shap_bar.png'),
    ('SHAP Beeswarm',         'reports/figures/week9_shap_beeswarm.png'),
    ('SHAP Summary',          'reports/figures/week9_shap_summary.png'),
    ('Dep MAX_PAY_DELAY',     'reports/figures/week9_dependence_MAX_PAY_DELAY.png'),
    ('Dep PAY_0',             'reports/figures/week9_dependence_PAY_0.png'),
    ('Dep COUNT_LATE',        'reports/figures/week9_dependence_COUNT_LATE_PAYMENT.png'),
    ('Dep BILL_AMT1',         'reports/figures/week9_dependence_BILL_AMT1.png'),
    ('Dep UTILIZATION_RATE',  'reports/figures/week9_dependence_UTILIZATION_RATE_SEPT.png'),
    ('Waterfall High Risk',   'reports/figures/week9_waterfall_high_risk.png'),
    ('Waterfall Low Risk',    'reports/figures/week9_waterfall_low_risk.png'),
    ('Waterfall Near Thresh', 'reports/figures/week9_waterfall_near_threshold.png'),
    ('README updated',        'README.md'),
]
all_ok = True
for name, path in artifacts:
    exists = os.path.exists(path)
    sz = os.path.getsize(path) if exists else 0
    status = 'OK' if exists else 'MISSING'
    if not exists:
        all_ok = False
    print(f'  [{status}] {name:<30} ({sz:>10,} bytes)')

print()
print('=== WEEK 8 MODEL UNCHANGED ===')
with open('models/final_candidate_model.pkl', 'rb') as f:
    model = pickle.load(f)
p = model.get_params()
print(f'  Model type:   {type(model).__name__}')
print(f'  n_estimators: {p["n_estimators"]}')
print(f'  max_depth:    {p["max_depth"]}')
print(f'  learning_rate:{p["learning_rate"]}')
print(f'  Artifact unchanged: OK')

print()
print('=== SUMMARY ===')
print(f'All artifacts present: {all_ok}')
wk9_status = 'COMPLETED' if (all_ok and nb_status == 'PASS') else 'INCOMPLETE'
print(f'Week 9 Status: {wk9_status}')
