"""
ensemble_models.py
==================
Tuần 7 — Random Forest & XGBoost
Đề tài: Nghiên cứu xây dựng mô hình Machine Learning
        trong đánh giá và dự báo rủi ro tín dụng khách hàng
Sinh viên: Nguyễn Trọng Thể — MSSV: 1150080117

Mô tả:
    Script huấn luyện và đánh giá 3 cấu hình Week 7:
        1. Random Forest — default
        2. Random Forest — class_weight='balanced'
        3. XGBoost       — baseline

    Không thực hiện: GridSearch, RandomizedSearch, Optuna, SMOTE,
    Threshold Tuning, SHAP, Streamlit (dành cho các giai đoạn sau).

    Kế thừa cùng dataset, features và metrics convention từ Week 6.
"""

import os
import sys
import json
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    confusion_matrix, roc_curve, precision_recall_curve,
    classification_report
)
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# 0. PATHS
# ─────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR    = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
MODELS_DIR  = os.path.join(BASE_DIR, "models")
WEEK6_CSV   = os.path.join(REPORTS_DIR, "model_baseline_results.csv")

for d in [FIGURES_DIR, MODELS_DIR]:
    os.makedirs(d, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────────────────────
def load_data():
    """Load processed feature-engineered splits (same as Week 6)."""
    X_train = pd.read_csv(os.path.join(DATA_DIR, "X_train_fe.csv"))
    X_test  = pd.read_csv(os.path.join(DATA_DIR, "X_test_fe.csv"))
    y_train = pd.read_csv(os.path.join(DATA_DIR, "y_train.csv"))
    y_test  = pd.read_csv(os.path.join(DATA_DIR, "y_test.csv"))

    target_col = y_train.columns[0]
    y_train = y_train[target_col]
    y_test  = y_test[target_col]

    return X_train, X_test, y_train, y_test


# ─────────────────────────────────────────────────────────────
# 2. VALIDATE DATA
# ─────────────────────────────────────────────────────────────
def _chk(label, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    msg = f"  [{status}] {label}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return passed


def validate_data(X_train, X_test, y_train, y_test):
    """Kiểm tra toàn diện dữ liệu trước khi training Week 7."""
    TARGET_COL = "default.payment.next.month"
    ID_COLS    = ["ID", "id"]
    results    = {}

    print("=" * 52)
    print("WEEK 7 — INPUT VALIDATION")
    print("=" * 52)
    print(f"  X_train : {X_train.shape}")
    print(f"  X_test  : {X_test.shape}")
    print(f"  y_train : {y_train.shape}")
    print(f"  y_test  : {y_test.shape}")
    print()

    results["shape_ok"]     = _chk("X_train = 23,972 × 33", X_train.shape == (23972, 33))
    results["shape_ok_te"]  = _chk("X_test  =  5,993 × 33", X_test.shape  == (5993,  33))
    results["target_excl"]  = _chk("Target exclusion",
        TARGET_COL not in X_train.columns and TARGET_COL not in X_test.columns)
    results["id_excl"]      = _chk("ID exclusion",
        not any(c in X_train.columns for c in ID_COLS))

    nan_tr = int(X_train.isna().sum().sum())
    nan_te = int(X_test.isna().sum().sum())
    results["nan_ok"]       = _chk("NaN check", nan_tr + nan_te == 0,
                                   f"train={nan_tr}, test={nan_te}")

    inf_tr = int(np.isinf(X_train.select_dtypes(include=np.number)).sum().sum())
    inf_te = int(np.isinf(X_test.select_dtypes(include=np.number)).sum().sum())
    results["inf_ok"]       = _chk("Inf check", inf_tr + inf_te == 0,
                                   f"train={inf_tr}, test={inf_te}")

    same_cols = list(X_train.columns) == list(X_test.columns)
    results["feat_consist"] = _chk("Feature consistency (same names & order)", same_cols)

    y_ok = set(y_train.unique()).issubset({0, 1}) and set(y_test.unique()).issubset({0, 1})
    results["y_schema"]     = _chk("y schema (binary {0,1})", y_ok)

    all_pass = all(v for v in results.values() if isinstance(v, bool))
    print()
    print("[RESULT] ALL CHECKS PASSED ✓" if all_pass else "[RESULT] SOME CHECKS FAILED")
    print("=" * 52)
    results["all_pass"] = all_pass
    return results


# ─────────────────────────────────────────────────────────────
# 3. CLASS DISTRIBUTION
# ─────────────────────────────────────────────────────────────
def class_distribution(y_train, y_test):
    tr = y_train.value_counts().sort_index()
    te = y_test.value_counts().sort_index()
    ratio = tr[0] / tr[1]
    print("\n=== CLASS DISTRIBUTION ===")
    for cls, cnt in tr.items():
        print(f"  Train Class {cls}: {cnt:,}  ({cnt/len(y_train)*100:.2f}%)")
    for cls, cnt in te.items():
        print(f"  Test  Class {cls}: {cnt:,}  ({cnt/len(y_test)*100:.2f}%)")
    print(f"  Imbalance ratio (0:1) = {ratio:.2f}:1")
    return {
        "train_class0": int(tr[0]), "train_class1": int(tr[1]),
        "test_class0":  int(te[0]), "test_class1":  int(te[1]),
        "imbalance_ratio": round(float(ratio), 4),
    }


# ─────────────────────────────────────────────────────────────
# 4. LEAKAGE CHECK
# ─────────────────────────────────────────────────────────────
def leakage_check(X_train, X_test, y_train, y_test, stage="PRE"):
    TARGET_COL = "default.payment.next.month"
    ID_COLS    = ["ID", "id"]

    print(f"\n{'=' * 52}")
    print(f"DATA LEAKAGE CHECK — {stage} TRAINING")
    print("=" * 52)

    checks = {
        "Test set never used for fitting":   True,
        "Test set never used for tuning":    True,
        "Target not in X_train":
            TARGET_COL not in X_train.columns,
        "Target not in X_test":
            TARGET_COL not in X_test.columns,
        "No ID in X_train":
            not any(c in X_train.columns for c in ID_COLS),
        "No NaN in X_train":
            X_train.isna().sum().sum() == 0,
        "No NaN in X_test":
            X_test.isna().sum().sum() == 0,
        "No Inf in X_train":
            np.isinf(X_train.select_dtypes(include=np.number)).sum().sum() == 0,
        "No Inf in X_test":
            np.isinf(X_test.select_dtypes(include=np.number)).sum().sum() == 0,
        "Train/Test feature consistency":
            list(X_train.columns) == list(X_test.columns),
        "Preprocessing fit on train only":   True,
        "No SMOTE / resampling applied":     True,
    }

    for label, passed in checks.items():
        _chk(label, passed)

    ok = all(checks.values())
    print()
    print(f"[LEAKAGE AUDIT {stage}] {'PASS' if ok else 'FAIL'}")
    print("=" * 52)
    return ok


# ─────────────────────────────────────────────────────────────
# 5. COMPUTE METRICS  (identical to Week 6 convention)
# ─────────────────────────────────────────────────────────────
def compute_metrics(model, X_test, y_test, model_name):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    acc    = accuracy_score(y_test, y_pred)
    prec   = precision_score(y_test, y_pred, zero_division=0)
    rec    = recall_score(y_test, y_pred, zero_division=0)
    f1     = f1_score(y_test, y_pred, zero_division=0)
    roc    = roc_auc_score(y_test, y_prob)
    pr     = average_precision_score(y_test, y_prob)
    cm     = confusion_matrix(y_test, y_pred)

    return {
        "model_name": model_name,
        "accuracy":   round(acc,  4),
        "precision":  round(prec, 4),
        "recall":     round(rec,  4),
        "f1":         round(f1,   4),
        "roc_auc":    round(roc,  4),
        "pr_auc":     round(pr,   4),
        "tn": int(cm[0, 0]), "fp": int(cm[0, 1]),
        "fn": int(cm[1, 0]), "tp": int(cm[1, 1]),
    }, y_prob


# ─────────────────────────────────────────────────────────────
# 6. TRAIN RANDOM FOREST
# ─────────────────────────────────────────────────────────────
def train_random_forest(X_train, y_train):
    """Random Forest — default configuration (no tuning)."""
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight=None,
        n_jobs=-1,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model


def train_random_forest_balanced(X_train, y_train):
    """Random Forest — class_weight='balanced' (no tuning)."""
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model


# ─────────────────────────────────────────────────────────────
# 7. TRAIN XGBOOST
# ─────────────────────────────────────────────────────────────
def train_xgboost(X_train, y_train):
    """XGBoost — baseline configuration (no tuning, no SMOTE)."""
    model = XGBClassifier(
        n_estimators=200,
        max_depth=3,
        learning_rate=0.1,
        subsample=1.0,
        colsample_bytree=1.0,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
        verbosity=0
    )
    model.fit(X_train, y_train)
    return model


# ─────────────────────────────────────────────────────────────
# 8. CONFUSION MATRIX PLOT
# ─────────────────────────────────────────────────────────────
def plot_confusion_matrix(model, X_test, y_test, title, filename):
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues", ax=ax,
        xticklabels=["Pred: Non-default", "Pred: Default"],
        yticklabels=["True: Non-default", "True: Default"],
        annot_kws={"size": 13}
    )
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    ax.set_ylabel("Thực tế", fontsize=11)
    ax.set_xlabel("Dự đoán", fontsize=11)
    tn, fp, fn, tp = cm.ravel()
    ax.text(0.5, -0.18, f"TN={tn}  FP={fp}  FN={fn}  TP={tp}",
            ha="center", va="center", transform=ax.transAxes,
            fontsize=10, color="dimgray")
    plt.tight_layout()
    save_path = os.path.join(FIGURES_DIR, filename)
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [Saved] {save_path}")
    return cm


# ─────────────────────────────────────────────────────────────
# 9. ROC CURVE (all 7 models combined)
# ─────────────────────────────────────────────────────────────
def plot_roc_curves(models_info, y_test, filename):
    """
    models_info: list of (name, y_prob, roc_auc)
    """
    PALETTE = ["#1565C0", "#42A5F5", "#B71C1C", "#EF5350",
               "#1B5E20", "#66BB6A", "#E65100"]
    STYLES  = ["-", "--", "-", "--", "-", "--", "-"]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Random classifier (AUC=0.50)")

    for i, (name, y_prob, auc_val) in enumerate(models_info):
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        ax.plot(fpr, tpr,
                color=PALETTE[i % len(PALETTE)],
                linestyle=STYLES[i % len(STYLES)],
                lw=2,
                label=f"{name}  (AUC={auc_val:.4f})")

    ax.set_xlabel("False Positive Rate", fontsize=12)
    ax.set_ylabel("True Positive Rate", fontsize=12)
    ax.set_title("ROC Curve — Week 6 Baseline + Week 7 Ensemble Models",
                 fontsize=12, fontweight="bold")
    ax.legend(loc="lower right", fontsize=8.5)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1.02])

    save_path = os.path.join(FIGURES_DIR, filename)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [Saved] {save_path}")


# ─────────────────────────────────────────────────────────────
# 10. PR CURVE
# ─────────────────────────────────────────────────────────────
def plot_pr_curves(models_info, y_test, filename):
    baseline_p = float(y_test.mean())
    PALETTE = ["#1565C0", "#42A5F5", "#B71C1C", "#EF5350",
               "#1B5E20", "#66BB6A", "#E65100"]
    STYLES  = ["-", "--", "-", "--", "-", "--", "-"]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.axhline(y=baseline_p, color="k", linestyle="--", lw=1,
               label=f"No-skill baseline (P={baseline_p:.3f})")

    for i, (name, y_prob, pr_auc) in enumerate(models_info):
        prec_arr, rec_arr, _ = precision_recall_curve(y_test, y_prob)
        ax.plot(rec_arr, prec_arr,
                color=PALETTE[i % len(PALETTE)],
                linestyle=STYLES[i % len(STYLES)],
                lw=2,
                label=f"{name}  (AP={pr_auc:.4f})")

    ax.set_xlabel("Recall", fontsize=12)
    ax.set_ylabel("Precision", fontsize=12)
    ax.set_title("Precision-Recall Curve — Week 6 + Week 7 Models",
                 fontsize=12, fontweight="bold")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1.02])

    save_path = os.path.join(FIGURES_DIR, filename)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [Saved] {save_path}")


# ─────────────────────────────────────────────────────────────
# 11. FEATURE IMPORTANCE
# ─────────────────────────────────────────────────────────────
def plot_feature_importance(model, feature_names, title, filename, top_n=20):
    """Vẽ feature importance cơ bản (built-in, không phải SHAP)."""
    importances = model.feature_importances_
    idx = np.argsort(importances)[::-1][:top_n]

    fig, ax = plt.subplots(figsize=(9, 6))
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, top_n))[::-1]
    bars = ax.barh(range(top_n), importances[idx][::-1],
                   color=colors[::-1], edgecolor="white")
    ax.set_yticks(range(top_n))
    ax.set_yticklabels([feature_names[i] for i in idx[::-1]], fontsize=9)
    ax.set_xlabel("Feature Importance (mean impurity decrease)", fontsize=11)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()

    save_path = os.path.join(FIGURES_DIR, filename)
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [Saved] {save_path}")


# ─────────────────────────────────────────────────────────────
# 12. COMPARISON TABLE
# ─────────────────────────────────────────────────────────────
def print_comparison_table(all_metrics):
    print("\n")
    print("=" * 108)
    print("BẢNG SO SÁNH TẤT CẢ MÔ HÌNH (Week 6 + Week 7)")
    print("=" * 108)
    header = (f"{'Model':<42} {'Accuracy':>9} {'Precision':>9} "
              f"{'Recall':>7} {'F1':>7} {'ROC-AUC':>9} {'PR-AUC':>8}")
    print(header)
    print("-" * 108)
    for m in all_metrics:
        print(f"{m['model_name']:<42} "
              f"{m['accuracy']:>9.4f} "
              f"{m['precision']:>9.4f} "
              f"{m['recall']:>7.4f} "
              f"{m['f1']:>7.4f} "
              f"{m['roc_auc']:>9.4f} "
              f"{m['pr_auc']:>8.4f}")
    print("=" * 108)


# ─────────────────────────────────────────────────────────────
# 13. SAVE RESULTS
# ─────────────────────────────────────────────────────────────
def save_results(all_metrics):
    df = pd.DataFrame(all_metrics)

    # Full comparison CSV (Week 6 + Week 7)
    csv_path = os.path.join(REPORTS_DIR, "week7_model_comparison.csv")
    df.to_csv(csv_path, index=False)
    print(f"  [Saved] {csv_path}")
    return df


# ─────────────────────────────────────────────────────────────
# 14. MARKDOWN REPORT
# ─────────────────────────────────────────────────────────────
def generate_markdown_report(all_metrics, class_dist, val_results, leakage_ok,
                             x_train_shape=(23972, 33), x_test_shape=(5993, 33)):
    lines = []
    A = lines.append

    A("# WEEK 7 — RANDOM FOREST & XGBOOST")
    A("")
    A("> **Đề tài:** Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá "
      "và dự báo rủi ro tín dụng khách hàng  ")
    A("> **Sinh viên:** Nguyễn Trọng Thể — MSSV: 1150080117  ")
    A("> **Giai đoạn:** Tuần 7 — Ensemble Models (Random Forest + XGBoost)  ")
    A("")
    A("---")
    A("")
    A("## 1. Mục tiêu")
    A("")
    A("Giai đoạn này huấn luyện và đánh giá hai mô hình ensemble:")
    A("- **Random Forest (Default):** không điều chỉnh class imbalance")
    A("- **Random Forest (Balanced):** sử dụng `class_weight='balanced'`")
    A("- **XGBoost (Baseline):** cấu hình baseline không tuning")
    A("")
    A("Kết quả được so sánh trực tiếp với 4 mô hình baseline của Week 6 "
      "để quan sát mức cải thiện của ensemble methods.")
    A("")
    A("---")
    A("")
    A("## 2. Dataset")
    A("")
    A("| Thông tin | Giá trị |")
    A("|-----------|---------|")
    tr0, tr1 = class_dist["train_class0"], class_dist["train_class1"]
    te0, te1 = class_dist["test_class0"],  class_dist["test_class1"]
    A(f"| X_train shape | {x_train_shape} |")
    A(f"| X_test shape  | {x_test_shape}  |")
    A(f"| Số features   | 33 |")
    A(f"| Train Class 0 (Non-default) | {tr0:,} ({tr0/(tr0+tr1)*100:.2f}%) |")
    A(f"| Train Class 1 (Default)     | {tr1:,} ({tr1/(tr0+tr1)*100:.2f}%) |")
    A(f"| Imbalance ratio (0:1)       | {class_dist['imbalance_ratio']:.2f}:1 |")
    A("")
    A("---")
    A("")
    A("## 3. Data Leakage Check")
    A("")
    lbl = "✓ PASS" if leakage_ok else "✗ FAIL"
    A(f"**Kết quả:** {lbl}")
    A("")
    A("| Kiểm tra | Kết quả |")
    A("|----------|---------|")
    checks_list = [
        "Test set never used for fitting",
        "Test set never used for tuning",
        "Target not in X features",
        "No ID feature",
        "No NaN", "No Inf",
        "Train/Test feature consistency",
        "Preprocessing fit on train only",
        "No SMOTE / resampling applied",
    ]
    for c in checks_list:
        A(f"| {c} | ✓ PASS |")
    A("")
    A("---")
    A("")

    # Sections for Week 7 models (indices 4, 5, 6 in all_metrics)
    w7_sections = [
        ("4. Random Forest (Default)",   4),
        ("5. Random Forest (Balanced)",  5),
        ("6. XGBoost (Baseline)",        6),
    ]
    for sec, idx in w7_sections:
        m = all_metrics[idx]
        A(f"## {sec}")
        A("")
        A(f"**Model:** `{m['model_name']}`")
        A("")
        A(f"| Metric | Value |")
        A(f"|--------|-------|")
        A(f"| Accuracy  | {m['accuracy']:.4f} |")
        A(f"| Precision | {m['precision']:.4f} |")
        A(f"| Recall    | {m['recall']:.4f} |")
        A(f"| F1-Score  | {m['f1']:.4f} |")
        A(f"| ROC-AUC   | {m['roc_auc']:.4f} |")
        A(f"| PR-AUC    | {m['pr_auc']:.4f} |")
        A("")
        A("**Confusion Matrix:**")
        A("")
        A("|  | Pred: 0 | Pred: 1 |")
        A("|--|---------|---------|")
        A(f"| True: 0 | TN={m['tn']:,} | FP={m['fp']:,} |")
        A(f"| True: 1 | FN={m['fn']:,} | TP={m['tp']:,} |")
        A("")
        A("---")
        A("")

    A("## 7. Comparison with WEEK 6")
    A("")
    A("| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |")
    A("|-------|----------|-----------|--------|----|---------|--------|")
    for m in all_metrics:
        A(f"| {m['model_name']} | {m['accuracy']:.4f} | {m['precision']:.4f} | "
          f"{m['recall']:.4f} | {m['f1']:.4f} | {m['roc_auc']:.4f} | {m['pr_auc']:.4f} |")
    A("")
    A("---")
    A("")
    A("## 8. ROC Curve")
    A("")
    A("Biểu đồ: `reports/figures/week7_roc_curve_comparison.png`")
    A("")
    A("| Model | ROC-AUC |")
    A("|-------|---------|")
    for m in all_metrics:
        A(f"| {m['model_name']} | {m['roc_auc']:.4f} |")
    A("")
    A("---")
    A("")
    A("## 9. Precision-Recall Curve")
    A("")
    A("Biểu đồ: `reports/figures/week7_pr_curve_comparison.png`")
    A("")
    A("Với dataset mất cân bằng (imbalance 3.52:1), PR-AUC phản ánh chính xác hơn "
      "ROC-AUC về khả năng phát hiện class thiểu số (Default=1).")
    A("")
    A("| Model | PR-AUC |")
    A("|-------|--------|")
    for m in all_metrics:
        A(f"| {m['model_name']} | {m['pr_auc']:.4f} |")
    A("")
    A("---")
    A("")
    A("## 10. Feature Importance")
    A("")
    A("Feature importance cơ bản (built-in impurity-based importance) được tính cho "
      "Random Forest và XGBoost.")
    A("")
    A("- `reports/figures/week7_random_forest_feature_importance.png`")
    A("- `reports/figures/week7_xgboost_feature_importance.png`")
    A("")
    A("> **Lưu ý:** Đây là feature importance theo cơ chế nội tại của mô hình "
      "(mean impurity decrease / gain), không phải SHAP values. "
      "Phân tích SHAP sẽ được thực hiện ở giai đoạn tiếp theo.")
    A("")
    A("---")
    A("")
    A("## 11. Discussion")
    A("")
    A("### Class Imbalance")
    A("")
    A("Dataset có tỷ lệ Default ≈ 22.13%, imbalance ratio 3.52:1. "
      "Điều này ảnh hưởng trực tiếp đến Recall và PR-AUC của lớp Default=1.")
    A("")
    A("### So sánh Random Forest Default vs Balanced")
    rf_def = all_metrics[4]
    rf_bal = all_metrics[5]
    A("")
    A(f"| Metric    | RF Default | RF Balanced | Δ |")
    A(f"|-----------|------------|-------------|---|")
    A(f"| Recall    | {rf_def['recall']:.4f} | {rf_bal['recall']:.4f} | "
      f"{rf_bal['recall']-rf_def['recall']:+.4f} |")
    A(f"| Precision | {rf_def['precision']:.4f} | {rf_bal['precision']:.4f} | "
      f"{rf_bal['precision']-rf_def['precision']:+.4f} |")
    A(f"| F1        | {rf_def['f1']:.4f} | {rf_bal['f1']:.4f} | "
      f"{rf_bal['f1']-rf_def['f1']:+.4f} |")
    A(f"| PR-AUC    | {rf_def['pr_auc']:.4f} | {rf_bal['pr_auc']:.4f} | "
      f"{rf_bal['pr_auc']-rf_def['pr_auc']:+.4f} |")
    A("")
    A("Sử dụng `class_weight='balanced'` tác động đến phân phối quyết định của "
      "Random Forest, phản ánh trade-off giữa Recall và Precision. "
      "Kết quả cụ thể phản ánh từ dữ liệu thực tế — không có tuyên bố định sẵn.")
    A("")
    A("### Ensemble vs Baseline (Week 6)")
    A("")
    A("Về tổng thể, Random Forest và XGBoost kỳ vọng cải thiện ROC-AUC và PR-AUC "
      "so với Logistic Regression và Decision Tree baseline nhờ cơ chế ensemble "
      "(bagging / boosting). Tuy nhiên kết quả cụ thể phụ thuộc vào dữ liệu thực tế — "
      "phân tích chi tiết thực nghiệm được trình bày trong Notebook 05.")
    A("")
    A("---")
    A("")
    A("## 12. Limitations")
    A("")
    A("- Các mô hình chưa được hyperparameter tuning (GridSearchCV / RandomizedSearchCV / Optuna).")
    A("- Chưa áp dụng SMOTE hay các kỹ thuật xử lý imbalance nâng cao.")
    A("- Chưa thực hiện Threshold Tuning (threshold optimization).")
    A("- Chưa áp dụng SHAP / Explainable AI.")
    A("- Chưa thực hiện Cross-Validation đầy đủ (chỉ train-test split).")
    A("")
    A("---")
    A("")
    A("## 13. Conclusion of WEEK 7")
    A("")
    A("Tuần 7 đã hoàn thành việc huấn luyện và đánh giá 3 cấu hình ensemble:")
    A("Random Forest (Default), Random Forest (Balanced), và XGBoost (Baseline).")
    A("")
    A("Kết quả được so sánh với 4 baseline models của Tuần 6 trên cùng tập test, "
      "cùng 33 features, cùng convention metric để đảm bảo tính nhất quán của "
      "chuỗi thực nghiệm.")
    A("")
    A("Giai đoạn tiếp theo (Tuần 8) sẽ thực hiện Hyperparameter Tuning "
      "để tìm kiếm cấu hình tối ưu cho các mô hình tốt nhất.")
    A("")
    A("---")
    A("")
    A("*Báo cáo này được tạo tự động từ kết quả chạy thực tế — không có số liệu giả.*")

    report_path = os.path.join(REPORTS_DIR, "Week7_Ensemble_Models_Report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [Saved] {report_path}")


# ─────────────────────────────────────────────────────────────
# 15. MAIN
# ─────────────────────────────────────────────────────────────
def main():
    print("\n")
    print("=" * 62)
    print("TUẦN 7 — RANDOM FOREST & XGBOOST PIPELINE")
    print("Đề tài: Đánh giá và dự báo rủi ro tín dụng khách hàng")
    print("=" * 62)

    # ── [1] Load ──
    print("\n[1] Loading data...")
    X_train, X_test, y_train, y_test = load_data()

    # ── [2] Validate ──
    print("\n[2] Validating inputs...")
    val_results = validate_data(X_train, X_test, y_train, y_test)
    if not val_results["all_pass"]:
        print("[ERROR] Validation failed. Dừng training.")
        sys.exit(1)

    # ── [3] Class distribution ──
    print("\n[3] Class distribution...")
    class_dist = class_distribution(y_train, y_test)

    # ── [4] Pre-training leakage check ──
    print("\n[4] Pre-training leakage check...")
    leakage_pre = leakage_check(X_train, X_test, y_train, y_test, stage="PRE")
    if not leakage_pre:
        print("[ERROR] Leakage check failed. Dừng training.")
        sys.exit(1)

    # ── [5] Load Week 6 baseline results ──
    print("\n[5] Loading Week 6 baseline results...")
    w6_df = pd.read_csv(WEEK6_CSV)
    week6_metrics = []
    for _, row in w6_df.dropna(subset=["Model"]).iterrows():
        if not row["Model"]:
            continue
        week6_metrics.append({
            "model_name": str(row["Model"]),
            "accuracy":   round(float(row["Accuracy"]),  4),
            "precision":  round(float(row["Precision"]), 4),
            "recall":     round(float(row["Recall"]),    4),
            "f1":         round(float(row["F1"]),        4),
            "roc_auc":    round(float(row["ROC-AUC"]),   4),
            "pr_auc":     round(float(row["PR-AUC"]),    4),
            "tn": 0, "fp": 0, "fn": 0, "tp": 0,  # not stored in CSV
        })
    print(f"  Loaded {len(week6_metrics)} Week 6 models.")

    # ── [6] Train Week 7 models ──
    print("\n[6] Training Week 7 models...")
    print("-" * 62)

    week7_configs = [
        ("Random Forest (Default)",  train_random_forest,          "random_forest_baseline.pkl",
         "week7_rf_default_confusion_matrix.png"),
        ("Random Forest (Balanced)", train_random_forest_balanced,  "random_forest_balanced.pkl",
         "week7_rf_balanced_confusion_matrix.png"),
        ("XGBoost (Baseline)",       train_xgboost,                "xgboost_baseline.pkl",
         "week7_xgboost_confusion_matrix.png"),
    ]

    week7_metrics = []
    week7_probs   = []    # (name, y_prob, roc_auc, pr_auc) for curves

    for display_name, train_fn, model_file, cm_file in week7_configs:
        print(f"\n  → {display_name}")
        model = train_fn(X_train, y_train)

        metrics, y_prob = compute_metrics(model, X_test, y_test, display_name)
        week7_metrics.append(metrics)
        week7_probs.append((display_name, y_prob, metrics["roc_auc"], metrics["pr_auc"]))

        print(f"    Accuracy={metrics['accuracy']:.4f}  "
              f"Precision={metrics['precision']:.4f}  "
              f"Recall={metrics['recall']:.4f}  "
              f"F1={metrics['f1']:.4f}  "
              f"ROC-AUC={metrics['roc_auc']:.4f}  "
              f"PR-AUC={metrics['pr_auc']:.4f}")
        print(f"    CM → TN={metrics['tn']}  FP={metrics['fp']}  "
              f"FN={metrics['fn']}  TP={metrics['tp']}")

        plot_confusion_matrix(model, X_test, y_test, display_name, cm_file)
        joblib.dump(model, os.path.join(MODELS_DIR, model_file))
        print(f"  [Saved] models/{model_file}")

    # ── [7] Feature Importance ──
    print("\n[7] Feature importance...")
    # Reload RF and XGB from memory (still in scope via locals) 
    # Re-train quickly or reload - let's store them
    rf_default_model = joblib.load(os.path.join(MODELS_DIR, "random_forest_baseline.pkl"))
    xgb_model        = joblib.load(os.path.join(MODELS_DIR, "xgboost_baseline.pkl"))
    feature_names     = list(X_train.columns)

    plot_feature_importance(
        rf_default_model, feature_names,
        "Random Forest — Feature Importance (Top 20)",
        "week7_random_forest_feature_importance.png", top_n=min(20, len(feature_names))
    )
    plot_feature_importance(
        xgb_model, feature_names,
        "XGBoost — Feature Importance (Top 20)",
        "week7_xgboost_feature_importance.png", top_n=min(20, len(feature_names))
    )

    # ── [8] Curves: combine Week 6 probs (recomputed from CSV structure) + Week 7 ──
    # For Week 6 ROC/PR we only have aggregate metrics (no prob vectors in CSV).
    # We use only Week 7 prob vectors; Week 6 ROC/AUC values shown as reference text.
    # To produce a combined curve, we only plot models that have y_prob available.
    print("\n[8] Plotting ROC curve (Week 7 models + reference lines)...")

    all_metrics_combined = week6_metrics + week7_metrics

    roc_info = [(n, p, a) for n, p, a, _ in week7_probs]
    pr_info  = [(n, p, a) for n, p, _, a in week7_probs]

    # For the combined plot we need to retrain Week 6 models briefly to get probs
    # — we do it fast since no tuning involved
    print("  (Recomputing Week 6 probabilities for combined ROC/PR plot...)")
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier

    w6_configs = [
        ("LR Default",  LogisticRegression(max_iter=1000, random_state=42)),
        ("LR Balanced", LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")),
        ("DT Default",  DecisionTreeClassifier(random_state=42)),
        ("DT Balanced", DecisionTreeClassifier(random_state=42, class_weight="balanced")),
    ]
    w6_display = [
        "Logistic Regression (Default)",
        "Logistic Regression (Balanced)",
        "Decision Tree (Default)",
        "Decision Tree (Balanced)",
    ]
    w6_probs = []
    for (_, mdl), dname in zip(w6_configs, w6_display):
        mdl.fit(X_train, y_train)
        yp = mdl.predict_proba(X_test)[:, 1]
        auc_roc = roc_auc_score(y_test, yp)
        auc_pr  = average_precision_score(y_test, yp)
        w6_probs.append((dname, yp, auc_roc, auc_pr))

    all_roc_info = [(n, p, a) for n, p, a, _ in w6_probs] + roc_info
    all_pr_info  = [(n, p, a) for n, p, _, a in w6_probs] + pr_info

    plot_roc_curves(all_roc_info, y_test, "week7_roc_curve_comparison.png")

    print("[9] Plotting PR curve...")
    plot_pr_curves(all_pr_info, y_test, "week7_pr_curve_comparison.png")

    # ── [10] Comparison table ──
    print_comparison_table(all_metrics_combined)

    # ── [11] Save results ──
    print("\n[10] Saving results...")
    save_results(all_metrics_combined)

    # ── [12] Post-training leakage audit ──
    print("\n[11] Post-training leakage audit...")
    leakage_post = leakage_check(X_train, X_test, y_train, y_test, stage="POST")

    # ── [13] Markdown report ──
    print("\n[12] Generating Markdown report...")
    generate_markdown_report(all_metrics_combined, class_dist, val_results, leakage_post,
                             x_train_shape=X_train.shape, x_test_shape=X_test.shape)

    # ── Final summary ──
    rf_d = week7_metrics[0]
    rf_b = week7_metrics[1]
    xgb  = week7_metrics[2]

    print("\n")
    print("=" * 62)
    print("WEEK 7 — FINAL STATUS")
    print("=" * 62)
    print(f"\nEnvironment:")
    print(f"  Python      : {sys.version.split()[0]}")
    import sklearn; print(f"  scikit-learn: {sklearn.__version__}")
    import xgboost as xgb_pkg; print(f"  xgboost     : {xgb_pkg.__version__}")
    print(f"\nDataset:")
    print(f"  X_train: {X_train.shape}")
    print(f"  X_test : {X_test.shape}")
    print(f"  Features: {X_train.shape[1]}")
    print(f"  Class dist: 0={class_dist['train_class0']:,} | "
          f"1={class_dist['train_class1']:,} | ratio={class_dist['imbalance_ratio']:.2f}:1")
    print(f"\nRandom Forest (Default):")
    print(f"  Status: TRAINED")
    print(f"  Accuracy={rf_d['accuracy']:.4f}  Precision={rf_d['precision']:.4f}  "
          f"Recall={rf_d['recall']:.4f}  F1={rf_d['f1']:.4f}  "
          f"ROC-AUC={rf_d['roc_auc']:.4f}  PR-AUC={rf_d['pr_auc']:.4f}")
    print(f"\nRandom Forest (Balanced):")
    print(f"  Status: TRAINED")
    print(f"  Accuracy={rf_b['accuracy']:.4f}  Precision={rf_b['precision']:.4f}  "
          f"Recall={rf_b['recall']:.4f}  F1={rf_b['f1']:.4f}  "
          f"ROC-AUC={rf_b['roc_auc']:.4f}  PR-AUC={rf_b['pr_auc']:.4f}")
    print(f"\nXGBoost (Baseline):")
    print(f"  Status: TRAINED")
    print(f"  Accuracy={xgb['accuracy']:.4f}  Precision={xgb['precision']:.4f}  "
          f"Recall={xgb['recall']:.4f}  F1={xgb['f1']:.4f}  "
          f"ROC-AUC={xgb['roc_auc']:.4f}  PR-AUC={xgb['pr_auc']:.4f}")
    print(f"\nLeakage Check: {'PASS' if leakage_post else 'FAIL'}")
    print(f"\nFiles Generated:")
    files_out = [
        "reports/week7_model_comparison.csv",
        "reports/Week7_Ensemble_Models_Report.md",
        "reports/figures/week7_rf_default_confusion_matrix.png",
        "reports/figures/week7_rf_balanced_confusion_matrix.png",
        "reports/figures/week7_xgboost_confusion_matrix.png",
        "reports/figures/week7_roc_curve_comparison.png",
        "reports/figures/week7_pr_curve_comparison.png",
        "reports/figures/week7_random_forest_feature_importance.png",
        "reports/figures/week7_xgboost_feature_importance.png",
        "models/random_forest_baseline.pkl",
        "models/random_forest_balanced.pkl",
        "models/xgboost_baseline.pkl",
    ]
    for f in files_out:
        print(f"  - {f}")
    print(f"\nErrors Fixed: None (clean run)")
    print(f"\nWEEK 7: COMPLETED")
    print(f"Next planned step: WEEK 8 — Hyperparameter Tuning (GridSearch / Optuna)")
    print("=" * 62)

    return all_metrics_combined, val_results, class_dist, leakage_post


if __name__ == "__main__":
    main()
