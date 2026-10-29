"""
Week 9 — Model Interpretability / Risk Analysis (SHAP / XAI)
Student: Nguyen Trong The
Student ID: 1150080117
Topic: Ung dung Machine Learning trong danh gia va du bao rui ro tin dung khach hang
Week: 9

Script nay thuc hien toan bo SHAP analysis va export artifacts.
Khong train lai model.
"""

import os
import sys
import json
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Windows
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import shap
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PATHS
# ============================================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'final_candidate_model.pkl')
X_TRAIN_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'X_train_fe.csv')
X_TEST_PATH  = os.path.join(PROJECT_ROOT, 'data', 'processed', 'X_test_fe.csv')
Y_TEST_PATH  = os.path.join(PROJECT_ROOT, 'data', 'processed', 'y_test.csv')
FIG_DIR      = os.path.join(PROJECT_ROOT, 'reports', 'figures')
REPORT_DIR   = os.path.join(PROJECT_ROOT, 'reports')
os.makedirs(FIG_DIR, exist_ok=True)

THRESHOLD = 0.60

# ============================================================
# SECTION 1 — LOAD MODEL AND DATA
# ============================================================
print("=" * 60)
print("SECTION 1 — LOAD MODEL AND DATA")
print("=" * 60)

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
print(f"Model type: {type(model).__name__}")
p = model.get_params()
print(f"n_estimators: {p.get('n_estimators')}")
print(f"max_depth:    {p.get('max_depth')}")
print(f"learning_rate:{p.get('learning_rate')}")

X_train = pd.read_csv(X_TRAIN_PATH)
X_test  = pd.read_csv(X_TEST_PATH)
y_test  = pd.read_csv(Y_TEST_PATH).squeeze()

FEATURE_NAMES = list(X_test.columns)
print(f"\nX_train shape: {X_train.shape}")
print(f"X_test  shape: {X_test.shape}")
print(f"y_test  shape: {y_test.shape}")
print(f"Feature count: {len(FEATURE_NAMES)}")
assert X_test.shape == (5993, 33), f"MISMATCH: X_test shape {X_test.shape}"
print("Shape verification: PASS (5993 x 33)")

# Predict probabilities (NO retrain)
y_prob  = model.predict_proba(X_test)[:, 1]
y_pred  = (y_prob >= THRESHOLD).astype(int)
print(f"\nProbability range: [{y_prob.min():.4f}, {y_prob.max():.4f}]")
print(f"Decision Threshold: {THRESHOLD}")
print(f"Predicted Default count: {y_pred.sum()} / {len(y_pred)}")

# ============================================================
# SECTION 2 — SHAP TreeExplainer
# ============================================================
print("\n" + "=" * 60)
print("SECTION 2 — SHAP TreeExplainer")
print("=" * 60)

# Use X_test as explanation dataset (post-hoc interpretation on held-out test set)
explainer = shap.TreeExplainer(model)
print("Computing SHAP values on X_test (5993 samples)...")
shap_values = explainer.shap_values(X_test)
print(f"SHAP values shape: {shap_values.shape}")

expected_value = explainer.expected_value
print(f"Expected value (base rate, log-odds): {expected_value:.6f}")

# ============================================================
# SECTION 3 — GLOBAL FEATURE IMPORTANCE
# ============================================================
print("\n" + "=" * 60)
print("SECTION 3 — GLOBAL FEATURE IMPORTANCE")
print("=" * 60)

mean_abs_shap = np.abs(shap_values).mean(axis=0)
importance_df = pd.DataFrame({
    'Feature': FEATURE_NAMES,
    'Mean_Abs_SHAP': mean_abs_shap
}).sort_values('Mean_Abs_SHAP', ascending=False).reset_index(drop=True)
importance_df.index += 1  # Rank from 1
importance_df.index.name = 'Rank'

print("\nTop 10 SHAP Feature Importance:")
print(importance_df.head(10).to_string())

# Save CSV
csv_path = os.path.join(REPORT_DIR, 'week9_shap_feature_importance.csv')
importance_df.to_csv(csv_path)
print(f"\nSaved: {csv_path}")

# ============================================================
# SECTION 4 — SHAP BAR PLOT (Global Mean |SHAP|)
# ============================================================
print("\n" + "=" * 60)
print("SECTION 4 — SHAP BAR PLOT")
print("=" * 60)

top_n = 15
top_feats = importance_df.head(top_n)

fig, ax = plt.subplots(figsize=(10, 7))
bars = ax.barh(
    top_feats['Feature'][::-1],
    top_feats['Mean_Abs_SHAP'][::-1],
    color=plt.cm.RdYlBu_r(np.linspace(0.2, 0.85, top_n))
)
ax.set_xlabel('Mean |SHAP Value| (Average Impact on Model Output)', fontsize=11)
ax.set_title(f'Global Feature Importance — XGBoost Tuned (SHAP)\nTop {top_n} Features by Mean |SHAP Value|', fontsize=13, fontweight='bold')
ax.axvline(x=0, color='black', linewidth=0.5)
for bar, val in zip(bars, top_feats['Mean_Abs_SHAP'][::-1]):
    ax.text(val + 0.0005, bar.get_y() + bar.get_height()/2,
            f'{val:.4f}', va='center', ha='left', fontsize=8)
plt.tight_layout()
bar_path = os.path.join(FIG_DIR, 'week9_shap_bar.png')
plt.savefig(bar_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {bar_path}")

# ============================================================
# SECTION 5 — SHAP SUMMARY / BEESWARM PLOT
# ============================================================
print("\n" + "=" * 60)
print("SECTION 5 — SHAP SUMMARY / BEESWARM PLOT")
print("=" * 60)

# Beeswarm (dot) plot — top 15 features
shap_df = pd.DataFrame(shap_values, columns=FEATURE_NAMES)
top_features_order = importance_df['Feature'].tolist()[:15]

fig, ax = plt.subplots(figsize=(11, 8))
plt.sca(ax)
shap.summary_plot(
    shap_values,
    X_test,
    feature_names=FEATURE_NAMES,
    max_display=15,
    show=False,
    plot_size=None
)
plt.title('SHAP Summary Plot (Beeswarm) — XGBoost Tuned\nImpact of Top 15 Features on Model Output (Log-Odds)', 
          fontsize=12, fontweight='bold', pad=12)
plt.tight_layout()
beeswarm_path = os.path.join(FIG_DIR, 'week9_shap_beeswarm.png')
plt.savefig(beeswarm_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {beeswarm_path}")

# Also a bar summary
fig, ax = plt.subplots(figsize=(10, 7))
plt.sca(ax)
shap.summary_plot(
    shap_values,
    X_test,
    feature_names=FEATURE_NAMES,
    max_display=15,
    plot_type='bar',
    show=False,
    plot_size=None
)
plt.title('SHAP Global Feature Importance — XGBoost Tuned\nMean |SHAP Value| per Feature', 
          fontsize=12, fontweight='bold', pad=12)
plt.tight_layout()
summary_path = os.path.join(FIG_DIR, 'week9_shap_summary.png')
plt.savefig(summary_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {summary_path}")

# ============================================================
# SECTION 6 — DEPENDENCE PLOTS (Top 5 features)
# ============================================================
print("\n" + "=" * 60)
print("SECTION 6 — DEPENDENCE PLOTS")
print("=" * 60)

top5_features = importance_df['Feature'].tolist()[:5]
print(f"Top 5 features for dependence plots: {top5_features}")

for feat in top5_features:
    feat_idx = FEATURE_NAMES.index(feat)
    fig, ax = plt.subplots(figsize=(9, 5))
    plt.sca(ax)
    shap.dependence_plot(
        feat_idx,
        shap_values,
        X_test,
        feature_names=FEATURE_NAMES,
        ax=ax,
        show=False
    )
    ax.set_title(f'SHAP Dependence Plot: {feat}\n(Relationship between feature value and SHAP contribution)', 
                 fontsize=11, fontweight='bold')
    ax.set_xlabel(feat, fontsize=10)
    ax.set_ylabel(f'SHAP value for {feat}\n(Impact on model output)', fontsize=10)
    plt.tight_layout()
    safe_feat = feat.replace('/', '_').replace(' ', '_')
    dep_path = os.path.join(FIG_DIR, f'week9_dependence_{safe_feat}.png')
    plt.savefig(dep_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {dep_path}")

# ============================================================
# SECTION 7 — LOCAL INTERPRETABILITY (3 Representative Cases)
# ============================================================
print("\n" + "=" * 60)
print("SECTION 7 — LOCAL INTERPRETABILITY")
print("=" * 60)

y_test_arr = y_test.values if hasattr(y_test, 'values') else np.array(y_test)

# Case 1 — High Risk: highest probability among True Positives (actual=1, predicted=1)
tp_mask = (y_pred == 1) & (y_test_arr == 1)
if tp_mask.sum() > 0:
    tp_probs = y_prob[tp_mask]
    tp_indices = np.where(tp_mask)[0]
    case1_local_idx = tp_indices[np.argmax(tp_probs)]
else:
    # Fallback: highest predicted probability
    case1_local_idx = np.argmax(y_prob)
case1_prob = y_prob[case1_local_idx]
case1_actual = int(y_test_arr[case1_local_idx])

# Case 2 — Low Risk: lowest probability among True Negatives (actual=0, predicted=0)
tn_mask = (y_pred == 0) & (y_test_arr == 0)
if tn_mask.sum() > 0:
    tn_probs = y_prob[tn_mask]
    tn_indices = np.where(tn_mask)[0]
    case2_local_idx = tn_indices[np.argmin(tn_probs)]
else:
    case2_local_idx = np.argmin(y_prob)
case2_prob = y_prob[case2_local_idx]
case2_actual = int(y_test_arr[case2_local_idx])

# Case 3 — Near Threshold: closest to 0.60
diff_from_threshold = np.abs(y_prob - THRESHOLD)
case3_local_idx = np.argmin(diff_from_threshold)
# Avoid overlap
if case3_local_idx == case1_local_idx or case3_local_idx == case2_local_idx:
    diff_from_threshold[case1_local_idx] = 999
    diff_from_threshold[case2_local_idx] = 999
    case3_local_idx = np.argmin(diff_from_threshold)
case3_prob = y_prob[case3_local_idx]
case3_actual = int(y_test_arr[case3_local_idx])

cases = [
    {'name': 'High Risk',       'idx': case1_local_idx, 'prob': case1_prob, 'actual': case1_actual},
    {'name': 'Low Risk',        'idx': case2_local_idx, 'prob': case2_prob, 'actual': case2_actual},
    {'name': 'Near Threshold',  'idx': case3_local_idx, 'prob': case3_prob, 'actual': case3_actual},
]

print(f"\n{'Case':<20} {'X_test Index':>12} {'Probability':>12} {'Threshold':>10} {'Pred Class':>10} {'Actual':>8}")
print("-" * 80)
for c in cases:
    pred_class = 'Default' if c['prob'] >= THRESHOLD else 'Non-Default'
    actual_str = 'Default' if c['actual'] == 1 else 'Non-Default'
    print(f"{c['name']:<20} {c['idx']:>12} {c['prob']:>12.4f} {THRESHOLD:>10.2f} {pred_class:>10} {actual_str:>8}")

# Top SHAP contributors for each case
local_results = []
for c in cases:
    sv = shap_values[c['idx']]
    feat_vals = X_test.iloc[c['idx']]
    contrib_df = pd.DataFrame({'Feature': FEATURE_NAMES, 'SHAP': sv, 'Value': feat_vals.values})
    contrib_df = contrib_df.reindex(contrib_df['SHAP'].abs().sort_values(ascending=False).index)
    top_pos = contrib_df[contrib_df['SHAP'] > 0].head(3)['Feature'].tolist()
    top_neg = contrib_df[contrib_df['SHAP'] < 0].head(3)['Feature'].tolist()
    pred_class = 'Default' if c['prob'] >= THRESHOLD else 'Non-Default'
    actual_str = 'Default' if c['actual'] == 1 else 'Non-Default'
    local_results.append({
        'Case': c['name'],
        'X_test Index': c['idx'],
        'Probability': round(float(c['prob']), 4),
        'Threshold': THRESHOLD,
        'Predicted Class': pred_class,
        'Actual Class': actual_str,
        'Top Risk Factors (+SHAP)': ', '.join(top_pos),
        'Top Protective Factors (-SHAP)': ', '.join(top_neg)
    })
    print(f"\n  [{c['name']}] idx={c['idx']}, prob={c['prob']:.4f}, pred={pred_class}, actual={actual_str}")
    print(f"    Top positive SHAP contributors (push toward Default):   {top_pos}")
    print(f"    Top negative SHAP contributors (push toward Non-Default): {top_neg}")

# Save local results to CSV
local_df = pd.DataFrame(local_results)
local_csv_path = os.path.join(REPORT_DIR, 'week9_local_interpretation.csv')
local_df.to_csv(local_csv_path, index=False)
print(f"\nSaved: {local_csv_path}")

# ============================================================
# SECTION 8 — WATERFALL PLOTS
# ============================================================
print("\n" + "=" * 60)
print("SECTION 8 — WATERFALL PLOTS")
print("=" * 60)

waterfall_files = {
    'High Risk':      'week9_waterfall_high_risk.png',
    'Low Risk':       'week9_waterfall_low_risk.png',
    'Near Threshold': 'week9_waterfall_near_threshold.png',
}

for c in cases:
    sv = shap_values[c['idx']]
    feat_vals = X_test.iloc[c['idx']]
    pred_class = 'Default' if c['prob'] >= THRESHOLD else 'Non-Default'
    fname = waterfall_files[c['name']]

    # Build waterfall manually (works with all SHAP versions)
    contrib_df = pd.DataFrame({'Feature': FEATURE_NAMES, 'SHAP': sv, 'Value': feat_vals.values})
    contrib_df['AbsSHAP'] = contrib_df['SHAP'].abs()
    contrib_df = contrib_df.sort_values('AbsSHAP', ascending=False).head(12)
    contrib_df = contrib_df.sort_values('SHAP', ascending=True)

    colors = ['#e74c3c' if v > 0 else '#3498db' for v in contrib_df['SHAP']]
    labels = [f"{r['Feature']} = {r['Value']:.2f}" if abs(r['Value']) < 1e5 else f"{r['Feature']} = {r['Value']:.0f}" 
              for _, r in contrib_df.iterrows()]

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(range(len(contrib_df)), contrib_df['SHAP'].values, color=colors, edgecolor='white', linewidth=0.5)
    ax.set_yticks(range(len(contrib_df)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.axvline(x=0, color='black', linewidth=1)
    for bar, val in zip(bars, contrib_df['SHAP'].values):
        x_pos = val + 0.002 if val >= 0 else val - 0.002
        ha = 'left' if val >= 0 else 'right'
        ax.text(x_pos, bar.get_y() + bar.get_height()/2, f'{val:+.4f}', 
                va='center', ha=ha, fontsize=8)

    ax.set_xlabel('SHAP Value (Impact on model output, log-odds space)', fontsize=10)
    ax.set_title(
        f'SHAP Waterfall Plot — {c["name"]} Case\n'
        f'Probability = {c["prob"]:.4f} | Threshold = {THRESHOLD} | Predicted: {pred_class}',
        fontsize=11, fontweight='bold'
    )

    red_patch  = mpatches.Patch(color='#e74c3c', label='Pushes toward Default (+)')
    blue_patch = mpatches.Patch(color='#3498db', label='Pushes toward Non-Default (-)')
    ax.legend(handles=[red_patch, blue_patch], loc='lower right', fontsize=9)

    base_text = f'Base value (expected output): {expected_value:.4f}'
    ax.annotate(base_text, xy=(0.01, 0.01), xycoords='axes fraction', fontsize=8, color='gray')

    plt.tight_layout()
    wpath = os.path.join(FIG_DIR, fname)
    plt.savefig(wpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {wpath}")

# ============================================================
# SECTION 9 — SAVE SUMMARY RESULTS JSON
# ============================================================
print("\n" + "=" * 60)
print("SECTION 9 — SAVE SUMMARY RESULTS JSON")
print("=" * 60)

shap_summary = {
    'model': 'XGBoost Tuned',
    'threshold': THRESHOLD,
    'shap_method': 'TreeExplainer',
    'explanation_dataset': 'X_test (5993 samples, 33 features)',
    'note': 'Post-hoc model interpretation — no retraining performed',
    'expected_value': float(expected_value),
    'top10_features': importance_df.head(10)[['Feature', 'Mean_Abs_SHAP']].assign(
        Mean_Abs_SHAP=lambda x: x['Mean_Abs_SHAP'].round(6)
    ).to_dict('records'),
    'local_cases': local_results,
    'week': 9
}

json_path = os.path.join(REPORT_DIR, 'week9_shap_summary.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(shap_summary, f, indent=2, ensure_ascii=False)
print(f"Saved: {json_path}")

# ============================================================
# FINAL VERIFICATION
# ============================================================
print("\n" + "=" * 60)
print("FINAL ARTIFACT VERIFICATION")
print("=" * 60)

artifacts = [
    os.path.join(REPORT_DIR, 'week9_shap_feature_importance.csv'),
    os.path.join(REPORT_DIR, 'week9_local_interpretation.csv'),
    os.path.join(REPORT_DIR, 'week9_shap_summary.json'),
    os.path.join(FIG_DIR, 'week9_shap_bar.png'),
    os.path.join(FIG_DIR, 'week9_shap_beeswarm.png'),
    os.path.join(FIG_DIR, 'week9_shap_summary.png'),
    os.path.join(FIG_DIR, 'week9_dependence_PAY_0.png'),
    os.path.join(FIG_DIR, 'week9_waterfall_high_risk.png'),
    os.path.join(FIG_DIR, 'week9_waterfall_low_risk.png'),
    os.path.join(FIG_DIR, 'week9_waterfall_near_threshold.png'),
]

all_ok = True
for path in artifacts:
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    status = 'OK' if exists else 'MISSING'
    print(f"  [{status}] {os.path.basename(path)}  ({size:,} bytes)")
    all_ok = all_ok and exists

print()
if all_ok:
    print("ALL ARTIFACTS: OK")
else:
    print("WARNING: SOME ARTIFACTS MISSING")

print("\nSHAP analysis complete. No model retraining performed.")
print(f"Top 5 features: {importance_df['Feature'].tolist()[:5]}")
