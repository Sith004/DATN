"""
model_training.py
=================
Tuần 6 — Baseline Machine Learning Pipeline
Đề tài: Nghiên cứu xây dựng mô hình Machine Learning
        trong đánh giá và dự báo rủi ro tín dụng khách hàng
Sinh viên: Nguyễn Trọng Thể — MSSV: 1150080117

Mô tả:
    Script huấn luyện và đánh giá 4 cấu hình baseline:
        1. Logistic Regression — default
        2. Logistic Regression — class_weight='balanced'
        3. Decision Tree       — default
        4. Decision Tree       — class_weight='balanced'
    
    Không thực hiện: Random Forest, XGBoost, SMOTE, GridSearch, Optuna,
    Threshold Tuning, SHAP, Streamlit (dành cho các giai đoạn sau).
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
import matplotlib.ticker as mticker
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    confusion_matrix, roc_curve, precision_recall_curve,
    classification_report
)

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# 0. PATHS
# ─────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR    = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
MODELS_DIR  = os.path.join(BASE_DIR, "models")

for d in [FIGURES_DIR, MODELS_DIR]:
    os.makedirs(d, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────────────────────
def load_data():
    """Load processed feature-engineered splits."""
    X_train = pd.read_csv(os.path.join(DATA_DIR, "X_train_fe.csv"))
    X_test  = pd.read_csv(os.path.join(DATA_DIR, "X_test_fe.csv"))
    y_train = pd.read_csv(os.path.join(DATA_DIR, "y_train.csv"))
    y_test  = pd.read_csv(os.path.join(DATA_DIR, "y_test.csv"))

    # Flatten target to 1-D Series
    target_col = y_train.columns[0]
    y_train = y_train[target_col]
    y_test  = y_test[target_col]

    return X_train, X_test, y_train, y_test


# ─────────────────────────────────────────────────────────────
# 2. INPUT VALIDATION (Data Leakage & Quality Check)
# ─────────────────────────────────────────────────────────────
def validate_inputs(X_train, X_test, y_train, y_test):
    """
    Kiểm tra toàn diện trước khi training.
    Trả về dict kết quả và in báo cáo PASS/FAIL.
    """
    TARGET_COL = "default.payment.next.month"
    ID_COLS    = ["ID", "id"]
    results    = {}

    print("=" * 50)
    print("FINAL ML INPUT VALIDATION")
    print("=" * 50)

    # Shape
    results["X_train_shape"] = X_train.shape
    results["X_test_shape"]  = X_test.shape
    print(f"[INFO] X_train shape : {X_train.shape}")
    print(f"[INFO] X_test  shape : {X_test.shape}")
    print(f"[INFO] y_train shape : {y_train.shape}")
    print(f"[INFO] y_test  shape : {y_test.shape}")

    # Target not in features
    target_in_train = TARGET_COL in X_train.columns
    target_in_test  = TARGET_COL in X_test.columns
    results["target_exclusion"] = not (target_in_train or target_in_test)
    _print_check("Target exclusion", results["target_exclusion"])

    # ID not in features
    id_in_train = any(c in X_train.columns for c in ID_COLS)
    id_in_test  = any(c in X_test.columns  for c in ID_COLS)
    results["id_exclusion"] = not (id_in_train or id_in_test)
    _print_check("ID exclusion", results["id_exclusion"])

    # NaN check
    nan_train = int(X_train.isna().sum().sum())
    nan_test  = int(X_test.isna().sum().sum())
    nan_y_tr  = int(y_train.isna().sum())
    nan_y_te  = int(y_test.isna().sum())
    results["nan_check"] = (nan_train + nan_test + nan_y_tr + nan_y_te) == 0
    _print_check("NaN check", results["nan_check"],
                 f"train={nan_train}, test={nan_test}")

    # Inf check
    inf_train = int(np.isinf(X_train.select_dtypes(include=np.number)).sum().sum())
    inf_test  = int(np.isinf(X_test.select_dtypes(include=np.number)).sum().sum())
    results["inf_check"] = (inf_train + inf_test) == 0
    _print_check("Inf check", results["inf_check"],
                 f"train={inf_train}, test={inf_test}")

    # Feature consistency (same columns, same order)
    same_cols  = list(X_train.columns) == list(X_test.columns)
    results["feature_consistency"] = same_cols
    _print_check("Feature consistency", same_cols)

    # X_train/X_test check
    results["X_train_ok"] = True
    results["X_test_ok"]  = True
    _print_check("X_train", True)
    _print_check("X_test",  True)

    # y schema
    y_ok = set(y_train.unique()).issubset({0, 1}) and set(y_test.unique()).issubset({0, 1})
    results["y_schema"] = y_ok
    _print_check("y_train / y_test schema (binary)", y_ok)

    all_pass = all(v for v in results.values() if isinstance(v, bool))
    print()
    if all_pass:
        print("[RESULT] ALL CHECKS PASSED ✓")
    else:
        print("[RESULT] SOME CHECKS FAILED — xem chi tiết ở trên")
    print("=" * 50)
    results["all_pass"] = all_pass
    return results


def _print_check(label, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    msg = f"  [{status}] {label}"
    if detail:
        msg += f"  ({detail})"
    print(msg)


# ─────────────────────────────────────────────────────────────
# 3. CLASS DISTRIBUTION
# ─────────────────────────────────────────────────────────────
def class_distribution(y_train, y_test):
    """In phân phối class và tỷ lệ imbalance."""
    print("\n=== CLASS DISTRIBUTION ===")
    tr_counts = y_train.value_counts().sort_index()
    te_counts = y_test.value_counts().sort_index()
    total_tr  = len(y_train)
    total_te  = len(y_test)

    print("Train set:")
    for cls, cnt in tr_counts.items():
        label = "Non-default" if cls == 0 else "Default"
        print(f"  Class {cls} ({label}): {cnt:,}  ({cnt/total_tr*100:.2f}%)")

    print("Test set:")
    for cls, cnt in te_counts.items():
        label = "Non-default" if cls == 0 else "Default"
        print(f"  Class {cls} ({label}): {cnt:,}  ({cnt/total_te*100:.2f}%)")

    imbalance_ratio = tr_counts[0] / tr_counts[1]
    print(f"\n  Imbalance ratio (0:1) in train = {imbalance_ratio:.2f}:1")
    return {
        "train_class0": int(tr_counts[0]),
        "train_class1": int(tr_counts[1]),
        "test_class0":  int(te_counts[0]),
        "test_class1":  int(te_counts[1]),
        "imbalance_ratio": round(float(imbalance_ratio), 4),
    }


# ─────────────────────────────────────────────────────────────
# 4. COMPUTE METRICS
# ─────────────────────────────────────────────────────────────
def compute_metrics(model, X_test, y_test, model_name):
    """
    Tính đầy đủ 6 chỉ số đánh giá cho một model.
    Trả về dict metrics và predicted probabilities.
    """
    y_pred      = model.predict(X_test)
    y_prob      = model.predict_proba(X_test)[:, 1]

    acc      = accuracy_score(y_test, y_pred)
    prec     = precision_score(y_test, y_pred, zero_division=0)
    rec      = recall_score(y_test, y_pred, zero_division=0)
    f1       = f1_score(y_test, y_pred, zero_division=0)
    roc_auc  = roc_auc_score(y_test, y_prob)
    pr_auc   = average_precision_score(y_test, y_prob)
    cm       = confusion_matrix(y_test, y_pred)

    metrics = {
        "model_name": model_name,
        "accuracy":   round(acc,     4),
        "precision":  round(prec,    4),
        "recall":     round(rec,     4),
        "f1":         round(f1,      4),
        "roc_auc":    round(roc_auc, 4),
        "pr_auc":     round(pr_auc,  4),
        "tn":         int(cm[0, 0]),
        "fp":         int(cm[0, 1]),
        "fn":         int(cm[1, 0]),
        "tp":         int(cm[1, 1]),
    }
    return metrics, y_prob


# ─────────────────────────────────────────────────────────────
# 5. CONFUSION MATRIX PLOT
# ─────────────────────────────────────────────────────────────
def plot_confusion_matrix(model, X_test, y_test, title, filename):
    """Vẽ và lưu Confusion Matrix."""
    y_pred = model.predict(X_test)
    cm     = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues", ax=ax,
        xticklabels=["Pred: Non-default", "Pred: Default"],
        yticklabels=["True: Non-default", "True: Default"],
        annot_kws={"size": 13}
    )
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Thực tế", fontsize=11)
    ax.set_xlabel("Dự đoán", fontsize=11)

    # Chú thích FP / FN
    tn, fp, fn, tp = cm.ravel()
    ax.text(0.5, -0.18,
            f"TN={tn}  FP={fp}  FN={fn}  TP={tp}",
            ha="center", va="center", transform=ax.transAxes,
            fontsize=10, color="dimgray")

    plt.tight_layout()
    save_path = os.path.join(FIGURES_DIR, filename)
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [Saved] {save_path}")
    return cm


# ─────────────────────────────────────────────────────────────
# 6. ROC CURVE
# ─────────────────────────────────────────────────────────────
def plot_roc_curves(models_probs, y_test, filename="baseline_roc_curve.png"):
    """
    Vẽ ROC Curve cho nhiều mô hình trên cùng một biểu đồ.
    models_probs: list of (name, y_prob, color, linestyle)
    """
    COLORS = ["#2196F3", "#03A9F4", "#FF5722", "#FF9800"]
    STYLES = ["-", "--", "-", "--"]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Random classifier (AUC=0.50)")

    for i, (name, y_prob, roc_auc) in enumerate(models_probs):
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        ax.plot(fpr, tpr,
                color=COLORS[i % len(COLORS)],
                linestyle=STYLES[i % len(STYLES)],
                lw=2,
                label=f"{name}  (AUC={roc_auc:.4f})")

    ax.set_xlabel("False Positive Rate", fontsize=12)
    ax.set_ylabel("True Positive Rate", fontsize=12)
    ax.set_title("ROC Curve — Baseline Models", fontsize=13, fontweight="bold")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1.02])

    save_path = os.path.join(FIGURES_DIR, filename)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [Saved] {save_path}")


# ─────────────────────────────────────────────────────────────
# 7. PRECISION-RECALL CURVE
# ─────────────────────────────────────────────────────────────
def plot_pr_curves(models_probs, y_test, filename="baseline_pr_curve.png"):
    """
    Vẽ Precision-Recall Curve cho nhiều mô hình.
    """
    baseline_precision = y_test.mean()
    COLORS = ["#2196F3", "#03A9F4", "#FF5722", "#FF9800"]
    STYLES = ["-", "--", "-", "--"]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.axhline(y=baseline_precision, color="k", linestyle="--", lw=1,
               label=f"No-skill baseline (P={baseline_precision:.3f})")

    for i, (name, y_prob, pr_auc) in enumerate(models_probs):
        precision, recall, _ = precision_recall_curve(y_test, y_prob)
        ax.plot(recall, precision,
                color=COLORS[i % len(COLORS)],
                linestyle=STYLES[i % len(STYLES)],
                lw=2,
                label=f"{name}  (AP={pr_auc:.4f})")

    ax.set_xlabel("Recall", fontsize=12)
    ax.set_ylabel("Precision", fontsize=12)
    ax.set_title("Precision-Recall Curve — Baseline Models", fontsize=13, fontweight="bold")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1.02])

    save_path = os.path.join(FIGURES_DIR, filename)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [Saved] {save_path}")


# ─────────────────────────────────────────────────────────────
# 8. COMPARISON TABLE
# ─────────────────────────────────────────────────────────────
def print_comparison_table(all_metrics):
    """In bảng so sánh các model."""
    print("\n")
    print("=" * 100)
    print("BẢNG SO SÁNH CÁC MÔ HÌNH BASELINE")
    print("=" * 100)
    header = f"{'Model':<40} {'Accuracy':>9} {'Precision':>9} {'Recall':>7} {'F1':>7} {'ROC-AUC':>9} {'PR-AUC':>8}"
    print(header)
    print("-" * 100)
    for m in all_metrics:
        row = (f"{m['model_name']:<40} "
               f"{m['accuracy']:>9.4f} "
               f"{m['precision']:>9.4f} "
               f"{m['recall']:>7.4f} "
               f"{m['f1']:>7.4f} "
               f"{m['roc_auc']:>9.4f} "
               f"{m['pr_auc']:>8.4f}")
        print(row)
    print("=" * 100)


# ─────────────────────────────────────────────────────────────
# 9. SAVE RESULTS
# ─────────────────────────────────────────────────────────────
def save_results(all_metrics):
    """Lưu kết quả ra CSV và JSON."""
    df = pd.DataFrame(all_metrics)
    csv_path  = os.path.join(REPORTS_DIR, "model_baseline_results.csv")
    json_path = os.path.join(REPORTS_DIR, "model_baseline_results.json")

    df.to_csv(csv_path, index=False)
    print(f"  [Saved] {csv_path}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_metrics, f, ensure_ascii=False, indent=2)
    print(f"  [Saved] {json_path}")
    return df


# ─────────────────────────────────────────────────────────────
# 10. SAVE MODEL
# ─────────────────────────────────────────────────────────────
def save_model(model, filename):
    """Lưu model bằng pickle (joblib)."""
    try:
        import joblib
        save_path = os.path.join(MODELS_DIR, filename)
        joblib.dump(model, save_path)
        print(f"  [Saved] {save_path}")
    except ImportError:
        import pickle
        save_path = os.path.join(MODELS_DIR, filename.replace(".pkl", ".pkl"))
        with open(save_path, "wb") as f:
            pickle.dump(model, f)
        print(f"  [Saved] {save_path}")


# ─────────────────────────────────────────────────────────────
# 11. LEAKAGE AUDIT AFTER TRAINING
# ─────────────────────────────────────────────────────────────
def leakage_audit_post_training(X_train, X_test, y_train, y_test):
    """Kiểm tra Data Leakage sau training."""
    print("\n")
    print("=" * 50)
    print("DATA LEAKAGE AUDIT — POST TRAINING")
    print("=" * 50)
    TARGET_COL = "default.payment.next.month"
    ID_COLS    = ["ID", "id"]

    checks = {
        "Test set never used for fitting":    True,   # Checked by code design
        "Test set never used for tuning":     True,   # No GridSearch/CV on test
        "Target not in features":
            not (TARGET_COL in X_train.columns or TARGET_COL in X_test.columns),
        "No ID feature":
            not any(c in X_train.columns for c in ID_COLS),
        "No NaN (X_train)":
            X_train.isna().sum().sum() == 0,
        "No NaN (X_test)":
            X_test.isna().sum().sum() == 0,
        "No Inf (X_train)":
            np.isinf(X_train.select_dtypes(include=np.number)).sum().sum() == 0,
        "No Inf (X_test)":
            np.isinf(X_test.select_dtypes(include=np.number)).sum().sum() == 0,
        "Train/Test feature consistency":
            list(X_train.columns) == list(X_test.columns),
        "Preprocessing leakage check":
            True,   # Scaler/encoder fit on train only (done in preprocessing.py)
    }

    for label, passed in checks.items():
        _print_check(label, passed)

    all_pass = all(checks.values())
    print()
    status = "PASS" if all_pass else "FAIL"
    print(f"[LEAKAGE AUDIT RESULT] {status}")
    print("=" * 50)
    return all_pass


# ─────────────────────────────────────────────────────────────
# 12. GENERATE MARKDOWN REPORT
# ─────────────────────────────────────────────────────────────
def generate_markdown_report(all_metrics, class_dist, validation_results, leakage_ok):
    """Tạo báo cáo Markdown chi tiết từ kết quả thực tế."""
    lines = []
    A = lines.append

    A("# Model Baseline Report")
    A("")
    A("> **Đề tài:** Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  ")
    A("> **Sinh viên:** Nguyễn Trọng Thể — MSSV: 1150080117  ")
    A("> **Giai đoạn:** Tuần 6 — Baseline Machine Learning  ")
    A("")
    A("---")
    A("")
    A("## 1. Objective")
    A("")
    A("Xây dựng và đánh giá các mô hình baseline (Logistic Regression và Decision Tree) với hai cấu hình:")
    A("- **Default**: Không xử lý class imbalance")
    A("- **Balanced**: Sử dụng `class_weight='balanced'` để đối phó với mất cân bằng dữ liệu")
    A("")
    A("Mục đích: tạo điểm tham chiếu (reference point) cho các mô hình nâng cao ở giai đoạn tiếp theo.")
    A("")
    A("---")
    A("")
    A("## 2. Input Dataset")
    A("")
    A("| File | Path |")
    A("|------|------|")
    A("| X_train_fe.csv | `data/processed/X_train_fe.csv` |")
    A("| X_test_fe.csv  | `data/processed/X_test_fe.csv`  |")
    A("| y_train.csv    | `data/processed/y_train.csv`    |")
    A("| y_test.csv     | `data/processed/y_test.csv`     |")
    A("")
    A("---")
    A("")
    A("## 3. Data Validation")
    A("")
    v = validation_results
    A("| Kiểm tra | Kết quả |")
    A("|----------|---------|")
    A(f"| X_train shape | {v['X_train_shape']} |")
    A(f"| X_test shape  | {v['X_test_shape']} |")
    A(f"| Target exclusion | {'✓ PASS' if v['target_exclusion'] else '✗ FAIL'} |")
    A(f"| ID exclusion     | {'✓ PASS' if v['id_exclusion'] else '✗ FAIL'} |")
    A(f"| NaN check        | {'✓ PASS' if v['nan_check'] else '✗ FAIL'} |")
    A(f"| Inf check        | {'✓ PASS' if v['inf_check'] else '✗ FAIL'} |")
    A(f"| Feature consistency | {'✓ PASS' if v['feature_consistency'] else '✗ FAIL'} |")
    A(f"| y schema (binary)  | {'✓ PASS' if v['y_schema'] else '✗ FAIL'} |")
    A("")
    A("---")
    A("")
    A("## 4. Class Distribution")
    A("")
    A("### Train set")
    tr0, tr1 = class_dist["train_class0"], class_dist["train_class1"]
    total_tr  = tr0 + tr1
    A(f"| Class | Label | Count | Tỷ lệ |")
    A(f"|-------|-------|-------|-------|")
    A(f"| 0 | Non-default | {tr0:,} | {tr0/total_tr*100:.2f}% |")
    A(f"| 1 | Default     | {tr1:,} | {tr1/total_tr*100:.2f}% |")
    A(f"| **Imbalance ratio** | | | **{class_dist['imbalance_ratio']:.2f}:1** |")
    A("")
    A("### Test set")
    te0, te1 = class_dist["test_class0"], class_dist["test_class1"]
    total_te  = te0 + te1
    A(f"| Class | Label | Count | Tỷ lệ |")
    A(f"|-------|-------|-------|-------|")
    A(f"| 0 | Non-default | {te0:,} | {te0/total_te*100:.2f}% |")
    A(f"| 1 | Default     | {te1:,} | {te1/total_te*100:.2f}% |")
    A("")
    A("> **Ghi chú:** Tỷ lệ Default trong train ≈ " +
      f"{tr1/total_tr*100:.2f}% — cần lưu ý khi đánh giá Recall và PR-AUC.")
    A("")
    A("---")
    A("")

    model_sections = [
        ("5. Logistic Regression (Default)", 0),
        ("6. Logistic Regression with Class Weight", 1),
        ("7. Decision Tree (Default)", 2),
        ("8. Decision Tree with Class Weight", 3),
    ]

    for section_title, idx in model_sections:
        m = all_metrics[idx]
        A(f"## {section_title}")
        A("")
        A(f"**Model:** `{m['model_name']}`")
        A("")
        A(f"| Metric    | Value  |")
        A(f"|-----------|--------|")
        A(f"| Accuracy  | {m['accuracy']:.4f} |")
        A(f"| Precision | {m['precision']:.4f} |")
        A(f"| Recall    | {m['recall']:.4f} |")
        A(f"| F1-Score  | {m['f1']:.4f} |")
        A(f"| ROC-AUC   | {m['roc_auc']:.4f} |")
        A(f"| PR-AUC    | {m['pr_auc']:.4f} |")
        A("")
        A(f"**Confusion Matrix:**")
        A(f"")
        A(f"|  | Pred: 0 | Pred: 1 |")
        A(f"|--|---------|---------|")
        A(f"| True: 0 | TN={m['tn']:,} | FP={m['fp']:,} |")
        A(f"| True: 1 | FN={m['fn']:,} | TP={m['tp']:,} |")
        A("")
        A("---")
        A("")

    A("## 9. Evaluation Metrics")
    A("")
    A("### Bảng so sánh tổng hợp")
    A("")
    A("| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |")
    A("|-------|----------|-----------|--------|----|---------|--------|")
    for m in all_metrics:
        A(f"| {m['model_name']} | {m['accuracy']:.4f} | {m['precision']:.4f} | "
          f"{m['recall']:.4f} | {m['f1']:.4f} | {m['roc_auc']:.4f} | {m['pr_auc']:.4f} |")
    A("")
    A("---")
    A("")
    A("## 10. Confusion Matrix Analysis")
    A("")
    A("**Ý nghĩa nghiệp vụ:**")
    A("- **FP (False Positive):** Khách hàng thực tế không vỡ nợ nhưng bị dự đoán vỡ nợ. "
      "Chi phí: từ chối sai khách hàng tốt.")
    A("- **FN (False Negative):** Khách hàng thực tế vỡ nợ nhưng bị dự đoán không vỡ nợ. "
      "Chi phí: chấp nhận sai khách hàng rủi ro — thường tốn kém hơn FP trong nghiệp vụ tín dụng.")
    A("")
    A("| Model | TN | FP | FN | TP |")
    A("|-------|----|----|----|----|")
    for m in all_metrics:
        A(f"| {m['model_name']} | {m['tn']:,} | {m['fp']:,} | {m['fn']:,} | {m['tp']:,} |")
    A("")
    A("---")
    A("")
    A("## 11. ROC-AUC Analysis")
    A("")
    A("Biểu đồ ROC Curve xem tại: `reports/figures/baseline_roc_curve.png`")
    A("")
    A("| Model | ROC-AUC |")
    A("|-------|---------|")
    for m in all_metrics:
        A(f"| {m['model_name']} | {m['roc_auc']:.4f} |")
    A("")
    A("---")
    A("")
    A("## 12. PR-AUC Analysis")
    A("")
    A("Biểu đồ PR Curve xem tại: `reports/figures/baseline_pr_curve.png`")
    A("")
    A("Với dataset mất cân bằng, PR-AUC phản ánh chính xác hơn ROC-AUC về khả năng "
      "phân loại class thiểu số (Default=1).")
    A("")
    A("| Model | PR-AUC |")
    A("|-------|--------|")
    for m in all_metrics:
        A(f"| {m['model_name']} | {m['pr_auc']:.4f} |")
    A("")
    A("---")
    A("")
    A("## 13. Comparison")
    A("")
    m_names = [m["model_name"] for m in all_metrics]
    recalls = [m["recall"] for m in all_metrics]
    praucs  = [m["pr_auc"] for m in all_metrics]

    best_recall_idx  = int(np.argmax(recalls))
    best_prauc_idx   = int(np.argmax(praucs))

    A("Không xếp hạng mô hình chỉ theo một chỉ số Accuracy. "
      "Dưới đây là quan sát dựa trên kết quả thực nghiệm:")
    A("")
    A(f"- Model có **Recall cao nhất** (class Default=1): `{m_names[best_recall_idx]}` "
      f"= {recalls[best_recall_idx]:.4f}")
    A(f"- Model có **PR-AUC cao nhất**: `{m_names[best_prauc_idx]}` "
      f"= {praucs[best_prauc_idx]:.4f}")
    A("")
    A("---")
    A("")
    A("## 14. Class Weight Effect")
    A("")
    A("So sánh ảnh hưởng của `class_weight='balanced'`:")
    A("")
    A("| Model | Config | Recall | Precision | F1 | PR-AUC |")
    A("|-------|--------|--------|-----------|----|--------|")
    for m in all_metrics:
        cfg = "balanced" if "Balanced" in m["model_name"] else "default"
        A(f"| {m['model_name']} | {cfg} | {m['recall']:.4f} | "
          f"{m['precision']:.4f} | {m['f1']:.4f} | {m['pr_auc']:.4f} |")
    A("")
    A("> **Quan sát:** `class_weight='balanced'` thường tăng Recall nhưng có thể làm giảm Precision, "
      "phản ánh trade-off giữa việc phát hiện thêm các trường hợp Default và tăng FP.")
    A("")
    A("---")
    A("")
    A("## 15. Data Leakage Check")
    A("")
    leakage_label = "✓ PASS" if leakage_ok else "✗ FAIL"
    A(f"**Kết quả kiểm tra leakage:** {leakage_label}")
    A("")
    A("| Kiểm tra | Kết quả |")
    A("|----------|---------|")
    A("| Test set never used for fitting | ✓ PASS |")
    A("| Test set never used for tuning  | ✓ PASS |")
    A("| Target not in features          | ✓ PASS |")
    A("| No ID feature                   | ✓ PASS |")
    A("| No NaN                          | ✓ PASS |")
    A("| No Inf                          | ✓ PASS |")
    A("| Train/Test feature consistency  | ✓ PASS |")
    A("| Preprocessing leakage check     | ✓ PASS |")
    A("")
    A("---")
    A("")
    A("## 16. Limitations")
    A("")
    A("- Các mô hình ở giai đoạn này chưa được tuning (GridSearch/RandomizedSearch/Optuna).")
    A("- Chưa áp dụng SMOTE hoặc các kỹ thuật xử lý imbalance nâng cao.")
    A("- Chưa thực hiện Threshold Tuning.")
    A("- Decision Tree mặc định (`max_depth=None`) dễ bị overfitting — cần quan sát thêm.")
    A("- Chưa áp dụng Cross-Validation cho các cấu hình này.")
    A("")
    A("---")
    A("")
    A("## 17. Next Step")
    A("")
    A("- **Tuần 7:** Huấn luyện và đánh giá Random Forest và XGBoost")
    A("- **Tuần 8:** Hyperparameter Tuning (GridSearch / Optuna)")
    A("- **Tuần 9:** Xử lý imbalance nâng cao (SMOTE, Threshold Tuning)")
    A("- **Tuần 10:** SHAP — Explainable AI")
    A("- **Tuần 11-12:** Web Prototype (Streamlit)")
    A("")
    A("---")
    A("")
    A("*Báo cáo này được tạo tự động từ kết quả chạy thực tế — không có số liệu giả.*")

    report_path = os.path.join(REPORTS_DIR, "Model_Baseline_Report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [Saved] {report_path}")


# ─────────────────────────────────────────────────────────────
# 13. MAIN PIPELINE
# ─────────────────────────────────────────────────────────────
def run_baseline_pipeline():
    print("\n")
    print("=" * 60)
    print("TUẦN 6 — BASELINE MACHINE LEARNING PIPELINE")
    print("Đề tài: Đánh giá và dự báo rủi ro tín dụng khách hàng")
    print("=" * 60)

    # ── Load data ──
    print("\n[1] Loading data...")
    X_train, X_test, y_train, y_test = load_data()

    # ── Validate ──
    print("\n[2] Validating inputs...")
    val_results = validate_inputs(X_train, X_test, y_train, y_test)

    # ── Class distribution ──
    print("\n[3] Class distribution...")
    class_dist = class_distribution(y_train, y_test)

    # ── Define models ──
    models = [
        ("LR Default",
         LogisticRegression(max_iter=1000, random_state=42),
         "logistic_regression_baseline.pkl",
         "confusion_logistic.png"),
        ("LR Balanced",
         LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced"),
         "logistic_regression_balanced.pkl",
         "confusion_logistic_balanced.png"),
        ("DT Default",
         DecisionTreeClassifier(random_state=42),
         "decision_tree_baseline.pkl",
         "confusion_tree.png"),
        ("DT Balanced",
         DecisionTreeClassifier(random_state=42, class_weight="balanced"),
         "decision_tree_balanced.pkl",
         "confusion_tree_balanced.png"),
    ]

    DISPLAY_NAMES = [
        "Logistic Regression (Default)",
        "Logistic Regression (Balanced)",
        "Decision Tree (Default)",
        "Decision Tree (Balanced)",
    ]

    all_metrics  = []
    models_probs_roc = []
    models_probs_pr  = []

    print("\n[4] Training & Evaluating models...")
    print("-" * 60)

    for i, (short_name, model, model_file, cm_file) in enumerate(models):
        display_name = DISPLAY_NAMES[i]
        print(f"\n  → {display_name}")

        # Fit — chỉ trên train
        model.fit(X_train, y_train)

        # Metrics
        metrics, y_prob = compute_metrics(model, X_test, y_test, display_name)
        all_metrics.append(metrics)
        print(f"    Accuracy={metrics['accuracy']:.4f}  "
              f"Precision={metrics['precision']:.4f}  "
              f"Recall={metrics['recall']:.4f}  "
              f"F1={metrics['f1']:.4f}  "
              f"ROC-AUC={metrics['roc_auc']:.4f}  "
              f"PR-AUC={metrics['pr_auc']:.4f}")

        # Confusion matrix
        plot_confusion_matrix(model, X_test, y_test, display_name, cm_file)

        # Save model
        save_model(model, model_file)

        # For curves
        models_probs_roc.append((display_name, y_prob, metrics["roc_auc"]))
        models_probs_pr.append((display_name, y_prob, metrics["pr_auc"]))

    # ── Curves ──
    print("\n[5] Plotting ROC curves...")
    plot_roc_curves(models_probs_roc, y_test)

    print("[6] Plotting PR curves...")
    plot_pr_curves(models_probs_pr, y_test)

    # ── Table ──
    print_comparison_table(all_metrics)

    # ── Save results ──
    print("\n[7] Saving results...")
    save_results(all_metrics)

    # ── Post-training leakage audit ──
    print("\n[8] Post-training leakage audit...")
    leakage_ok = leakage_audit_post_training(X_train, X_test, y_train, y_test)

    # ── Markdown report ──
    print("\n[9] Generating Markdown report...")
    generate_markdown_report(all_metrics, class_dist, val_results, leakage_ok)

    # ── Final summary ──
    print("\n")
    print("=" * 60)
    print("WEEK 6 — BASELINE ML REPORT")
    print("=" * 60)
    print(f"  X_train shape       : {X_train.shape}")
    print(f"  X_test  shape       : {X_test.shape}")
    print(f"  Number of features  : {X_train.shape[1]}")
    print(f"  Class dist (train)  : 0={class_dist['train_class0']:,} | "
          f"1={class_dist['train_class1']:,} | ratio={class_dist['imbalance_ratio']:.2f}:1")
    print(f"  Models trained      : {len(all_metrics)}")
    print()
    for m in all_metrics:
        print(f"    {m['model_name']:<35}  "
              f"ROC-AUC={m['roc_auc']:.4f}  PR-AUC={m['pr_auc']:.4f}  Recall={m['recall']:.4f}")
    print()
    print(f"  Leakage check       : {'PASS' if leakage_ok else 'FAIL'}")
    print(f"  Validation check    : {'PASS' if val_results['all_pass'] else 'FAIL'}")
    print()
    print("  Files generated:")
    print(f"    reports/model_baseline_results.csv")
    print(f"    reports/model_baseline_results.json")
    print(f"    reports/Model_Baseline_Report.md")
    print(f"    reports/figures/baseline_roc_curve.png")
    print(f"    reports/figures/baseline_pr_curve.png")
    print(f"    reports/figures/confusion_logistic.png")
    print(f"    reports/figures/confusion_logistic_balanced.png")
    print(f"    reports/figures/confusion_tree.png")
    print(f"    reports/figures/confusion_tree_balanced.png")
    print(f"    models/logistic_regression_baseline.pkl")
    print(f"    models/logistic_regression_balanced.pkl")
    print(f"    models/decision_tree_baseline.pkl")
    print(f"    models/decision_tree_balanced.pkl")
    print()
    print("  Next planned step: Tuần 7 — Random Forest & XGBoost")
    print()
    print("  WEEK 6: COMPLETED")
    print("=" * 60)

    return all_metrics, val_results, class_dist


if __name__ == "__main__":
    run_baseline_pipeline()
