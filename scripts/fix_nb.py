import json

with open('notebooks/05_Ensemble_Models.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

fixed = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        if isinstance(cell['source'], list):
            src = ''.join(cell['source'])
        else:
            src = cell['source']
        
        if 'lr_roc_val' in src and 'all_df' in src and '.iloc[0]' not in src:
            src = src.replace(
                "lr_roc_val  = float(all_df[all_df['Model']=='Logistic Regression (Default)']['ROC-AUC'])",
                "lr_roc_val  = float(all_df[all_df['Model']=='Logistic Regression (Default)']['ROC-AUC'].iloc[0])"
            )
            src = src.replace(
                "lr_pr_val   = float(all_df[all_df['Model']=='Logistic Regression (Default)']['PR-AUC'])",
                "lr_pr_val   = float(all_df[all_df['Model']=='Logistic Regression (Default)']['PR-AUC'].iloc[0])"
            )
            cell['source'] = src
            print('Fixed cell.')
            fixed = True
            break

if not fixed:
    print('Cell not found or already fixed.')

with open('notebooks/05_Ensemble_Models.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('Notebook saved.')
