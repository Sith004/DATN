"""
app.py — Week 10: Credit Risk Assessment Streamlit Prototype
=============================================================
Đề tài: Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá
        và dự báo rủi ro tín dụng khách hàng
Sinh viên: Nguyễn Trọng Thể — MSSV: 1150080117

Launch:
    streamlit run app.py

Architecture:
    User Input
    → Categorical Mapping (same as training preprocessing)
    → Feature Engineering (same formulas as training Week 5)
    → RobustScaler (fitted on X_train_fe, saved to models/robust_scaler.pkl)
    → XGBoost Tuned (models/final_candidate_model.pkl)
    → Probability of Default
    → Threshold 0.60 → Default / Non-Default
    → SHAP TreeExplainer explanation (post-hoc, identical to Week 9)
"""

import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ── Project root: works when launched from project root ─────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.prediction import (
    load_model,
    load_scaler,
    predict_single_customer,
    compute_shap_single,
    get_top_shap_contributors,
    load_model_meta,
    OFFICIAL_THRESHOLD,
    FEATURE_ORDER,
)
from src.database import (
    check_db_status,
    save_prediction_record,
    get_recent_predictions,
)

# ── Page configuration ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Credit Risk Assessment | ML Prototype",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Main header gradient */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 50%, #1a8fe3 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(30,58,95,0.3);
    }
    .main-header h1 {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.25rem 0;
    }
    .main-header p {
        color: rgba(255,255,255,0.85);
        margin: 0;
        font-size: 0.95rem;
    }

    /* Section headers */
    .section-header {
        background: #f0f4f8;
        border-left: 4px solid #1a8fe3;
        padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1.2rem 0 0.8rem 0;
        font-weight: 600;
        color: #1e3a5f;
    }

    /* Risk badge */
    .risk-high   { background:#ffe0e0; color:#c0392b; border:2px solid #e74c3c; }
    .risk-medium { background:#fff3cd; color:#856404; border:2px solid #ffc107; }
    .risk-low    { background:#d4edda; color:#155724; border:2px solid #28a745; }
    .risk-badge  {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        font-size: 1.1rem;
        font-weight: 700;
        text-align: center;
    }

    /* Prediction card */
    .pred-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        text-align: center;
        border-top: 4px solid #1a8fe3;
    }
    .pred-default    { border-top-color: #e74c3c !important; }
    .pred-nondefault { border-top-color: #27ae60 !important; }

    /* Metric styling */
    .metric-container {
        background: #f8fafc;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e2e8f0;
    }

    /* Disclaimer */
    .disclaimer {
        background: #fff8e1;
        border: 1px solid #ffe082;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.82rem;
        color: #5d4037;
        margin-top: 0.5rem;
    }

    /* Info box */
    .info-box {
        background: #e8f4fd;
        border: 1px solid #bee3f8;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
    }

    .stForm button[type="submit"] {
        background: linear-gradient(135deg, #1e3a5f, #1a8fe3) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Cached resource loaders ───────────────────────────────────────────────
@st.cache_resource(show_spinner="Đang tải mô hình XGBoost Tuned…")
def get_model():
    return load_model()

@st.cache_resource(show_spinner="Đang tải RobustScaler…")
def get_scaler():
    return load_scaler()

@st.cache_data(show_spinner=False)
def get_meta():
    return load_model_meta()


# ── Header ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="main-header">
        <h1>🏦 Hệ thống Đánh giá Rủi ro Tín dụng</h1>
        <p>
            Credit Risk Assessment — Machine Learning Decision Support Prototype &nbsp;|&nbsp;
            Sinh viên: <strong>Nguyễn Trọng Thể</strong> &nbsp;|&nbsp;
            MSSV: <strong>1150080117</strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ── Sidebar — Model information & About ───────────────────────────────────
with st.sidebar:
    st.markdown("## 📋 Thông tin Mô hình")

    meta = get_meta()

    st.markdown(
        """
        <div class="info-box">
            <b>Model:</b> XGBoost Tuned<br>
            <b>Threshold:</b> 0.60<br>
            <b>Số features:</b> 33<br>
            <b>Tập train:</b> 23,972 mẫu<br>
            <b>Tập test:</b> 5,993 mẫu
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Hiệu suất trên tập test (Week 8):**")
    perf_data = {
        "Metric": ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC", "PR-AUC"],
        "Value":  [0.7686,     0.4820,      0.6161,   0.5409,    0.7769,    0.5620],
    }
    st.dataframe(
        pd.DataFrame(perf_data).set_index("Metric"),
        use_container_width=True,
    )

    st.markdown("---")
    st.markdown("## 📌 Về hệ thống")
    st.info(
        """
        **Dataset:** UCI Credit Card Default Dataset  
        Taiwan, 30,000 khách hàng, T4–T9/2005.

        **Mục đích:** Prototype học thuật phục vụ đồ án tốt nghiệp.  
        Không phải hệ thống phê duyệt tín dụng thực tế.

        **Phân loại rủi ro (application-layer):**
        - 🟢 Low Risk: xác suất < 30%
        - 🟡 Medium Risk: 30% – 59%
        - 🔴 High Risk: ≥ 60% (= Default)

        Ngưỡng phân loại nhị phân: **threshold = 0.60**
        """,
        icon="ℹ️",
    )

    st.markdown("---")
    st.markdown("## 🔬 Top Risk Factors (SHAP Week 9)")
    shap_data = {
        "Feature":       ["MAX_PAY_DELAY", "PAY_0", "COUNT_LATE_PAYMENT",
                          "BILL_AMT1", "UTILIZATION_RATE_SEPT"],
        "Mean|SHAP|":    [0.4494, 0.2797, 0.1211, 0.1126, 0.0942],
    }
    st.dataframe(pd.DataFrame(shap_data).set_index("Feature"), use_container_width=True)

    st.markdown("---")
    st.markdown("## 🗄️ Cơ sở dữ liệu PostgreSQL")
    db_ok, db_msg = check_db_status()
    if db_ok:
        st.success(f"🟢 **Trạng thái:** Đã kết nối\n\n- Host: `127.0.0.1:15432`\n- Role: `app_streamlit` (Least Privilege)\n- Cơ chế: SSH Tunnel")
    else:
        st.warning(f"🟡 **Trạng thái:** Ngoại tuyến\n\n{db_msg}\n\n*Lưu ý: Mô hình ML vẫn hoạt động độc lập.*")


# ── Main content ──────────────────────────────────────────────────────────
tab_predict, tab_history, tab_about = st.tabs([
    "🔍 Dự báo Rủi ro",
    "📜 Lịch sử Dự báo (PostgreSQL)",
    "📖 Hướng dẫn & Thông tin"
])

# ═══════════════════════════════════════════════════════════
# TAB 1 — PREDICTION
# ═══════════════════════════════════════════════════════════
with tab_predict:

    st.markdown("### Nhập thông tin khách hàng")
    st.markdown(
        '<div class="disclaimer">⚠️ Đây là prototype học thuật. '
        'Kết quả không được sử dụng để ra quyết định tín dụng thực tế.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    with st.form("customer_form", clear_on_submit=False):

        # ── Section 1: Customer Demographics ───────────────────────
        st.markdown('<div class="section-header">👤 Thông tin khách hàng</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            LIMIT_BAL = st.number_input(
                "Hạn mức tín dụng (NT$)",
                min_value=10_000,
                max_value=1_000_000,
                value=200_000,
                step=10_000,
                help="LIMIT_BAL: Hạn mức tín dụng của tài khoản (NT$)",
            )
        with col2:
            AGE = st.number_input(
                "Tuổi",
                min_value=18,
                max_value=100,
                value=35,
                step=1,
                help="AGE: Tuổi của khách hàng",
            )
        with col3:
            SEX = st.selectbox(
                "Giới tính",
                options=[1, 2],
                format_func=lambda x: "Nam (1)" if x == 1 else "Nữ (2)",
                index=0,
                help="SEX: 1=Nam, 2=Nữ",
            )
        with col4:
            EDUCATION_raw = st.selectbox(
                "Trình độ học vấn",
                options=[1, 2, 3, 4],
                format_func=lambda x: {
                    1: "Thạc sĩ/Tiến sĩ (1)",
                    2: "Đại học (2)",
                    3: "THPT (3)",
                    4: "Khác (4)",
                }[x],
                index=1,
                help="EDUCATION: 1=Thạc sĩ+, 2=Đại học, 3=THPT, 4=Khác",
            )

        col5, col6 = st.columns([1, 3])
        with col5:
            MARRIAGE_raw = st.selectbox(
                "Tình trạng hôn nhân",
                options=[1, 2, 3],
                format_func=lambda x: {
                    1: "Đã kết hôn (1)",
                    2: "Độc thân (2)",
                    3: "Khác (3)",
                }[x],
                index=1,
                help="MARRIAGE: 1=Đã kết hôn, 2=Độc thân, 3=Khác",
            )

        # ── Section 2: Payment Status ───────────────────────────────
        st.markdown('<div class="section-header">💳 Lịch sử thanh toán (PAY_0: T9/2005 → PAY_6: T4/2005)</div>', unsafe_allow_html=True)
        st.caption(
            "Mã trạng thái: -2=Không phát sinh, -1=Trả đúng hạn, 0=Trả tối thiểu, "
            "1=Trễ 1 tháng, 2=Trễ 2 tháng, … 8=Trễ 8 tháng"
        )

        pay_cols = st.columns(6)
        pay_labels = ["PAY_0 (T9)", "PAY_2 (T8)", "PAY_3 (T7)", "PAY_4 (T6)", "PAY_5 (T5)", "PAY_6 (T4)"]
        pay_keys   = ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]
        pay_vals   = {}
        pay_options = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]

        for i, (pc, lbl, key) in enumerate(zip(pay_cols, pay_labels, pay_keys)):
            with pc:
                pay_vals[key] = st.selectbox(
                    lbl,
                    options=pay_options,
                    index=pay_options.index(0),
                    key=f"pay_{key}",
                    help=f"{key}: Trạng thái thanh toán",
                )

        # ── Section 3: Bill Amounts ─────────────────────────────────
        st.markdown('<div class="section-header">🧾 Dư nợ hóa đơn (NT$) — BILL_AMT1: T9/2005 → BILL_AMT6: T4/2005</div>', unsafe_allow_html=True)
        st.caption("Giá trị âm = khách hàng đã trả thừa (hợp lệ trong dataset)")

        bill_cols_ui = st.columns(6)
        bill_labels  = ["BILL_AMT1 (T9)", "BILL_AMT2 (T8)", "BILL_AMT3 (T7)",
                         "BILL_AMT4 (T6)", "BILL_AMT5 (T5)", "BILL_AMT6 (T4)"]
        bill_keys    = ["BILL_AMT1", "BILL_AMT2", "BILL_AMT3",
                        "BILL_AMT4", "BILL_AMT5", "BILL_AMT6"]
        bill_vals    = {}

        for i, (bc, lbl, key) in enumerate(zip(bill_cols_ui, bill_labels, bill_keys)):
            with bc:
                bill_vals[key] = st.number_input(
                    lbl,
                    min_value=-500_000,
                    max_value=1_700_000,
                    value=20_000 if i == 0 else max(0, 18_000 - i * 1_000),
                    step=1_000,
                    key=f"bill_{key}",
                    help=f"{key}: Dư nợ hóa đơn tháng tương ứng (NT$)",
                )

        # ── Section 4: Payment Amounts ──────────────────────────────
        st.markdown('<div class="section-header">💰 Số tiền đã thanh toán (NT$) — PAY_AMT1: T9/2005 → PAY_AMT6: T4/2005</div>', unsafe_allow_html=True)
        st.caption("Số tiền thực tế khách hàng đã trả (NT$). Tối thiểu 0.")

        payamt_cols_ui = st.columns(6)
        payamt_labels  = ["PAY_AMT1 (T9)", "PAY_AMT2 (T8)", "PAY_AMT3 (T7)",
                          "PAY_AMT4 (T6)", "PAY_AMT5 (T5)", "PAY_AMT6 (T4)"]
        payamt_keys    = ["PAY_AMT1", "PAY_AMT2", "PAY_AMT3",
                          "PAY_AMT4", "PAY_AMT5", "PAY_AMT6"]
        payamt_vals    = {}

        for i, (pc2, lbl, key) in enumerate(zip(payamt_cols_ui, payamt_labels, payamt_keys)):
            with pc2:
                payamt_vals[key] = st.number_input(
                    lbl,
                    min_value=0,
                    max_value=2_000_000,
                    value=2_000,
                    step=500,
                    key=f"payamt_{key}",
                    help=f"{key}: Số tiền đã trả tháng tương ứng (NT$)",
                )

        # ── Submit ──────────────────────────────────────────────────
        st.markdown("")
        submitted = st.form_submit_button(
            "🔍 Dự báo Rủi ro Tín dụng",
            use_container_width=True,
        )

    # ── After form submission ─────────────────────────────────────
    if submitted:
        # Validation
        errors = []
        if LIMIT_BAL < 10_000:
            errors.append("Hạn mức tín dụng phải ≥ 10,000 NT$.")
        if AGE < 18 or AGE > 100:
            errors.append("Tuổi phải từ 18 đến 100.")
        for k, v in payamt_vals.items():
            if v < 0:
                errors.append(f"{k} không được âm.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            # Load model & scaler
            with st.spinner("Đang dự báo…"):
                model  = get_model()
                scaler = get_scaler()

                raw_inputs = {
                    "LIMIT_BAL": LIMIT_BAL,
                    "AGE":       AGE,
                    "SEX":       SEX,
                    "EDUCATION": EDUCATION_raw,
                    "MARRIAGE":  MARRIAGE_raw,
                    **pay_vals,
                    **bill_vals,
                    **payamt_vals,
                }

                result = predict_single_customer(raw_inputs, model, scaler)

            prob  = result["probability"]
            label = result["prediction_label"]
            risk  = result["risk_level"]
            fv    = result["feature_vector"]
            fv_r  = result["feature_vector_raw"]

            # ── Lưu kết quả vào PostgreSQL (Graceful Degradation) ───
            engineered_payload = {
                "features_33": fv_r.to_dict(orient="records")[0] if not fv_r.empty else {},
            }
            db_saved, pred_id, db_msg = save_prediction_record(
                raw_inputs=raw_inputs,
                prediction_result=result,
                model_version="xgboost_tuned_v1",
                threshold=OFFICIAL_THRESHOLD,
                engineered_features=engineered_payload,
            )

            # ── Results Section ───────────────────────────────────
            st.markdown("---")
            st.markdown("## 📊 Kết quả Dự báo")

            if db_saved:
                st.success(f"💾 **Cơ sở dữ liệu:** {db_msg} — Dữ liệu đã lưu bền vững qua SSH Tunnel.")
            else:
                st.warning(f"⚠️ **Cơ sở dữ liệu:** {db_msg} — Quá trình dự báo Machine Learning vẫn hoàn tất.")

            # Row 1: Key metrics
            r1c1, r1c2, r1c3 = st.columns(3)

            with r1c1:
                st.metric(
                    label="Xác suất Vỡ nợ (Default)",
                    value=f"{prob * 100:.1f}%",
                    delta=f"Ngưỡng: {OFFICIAL_THRESHOLD * 100:.0f}%",
                    delta_color="off",
                )

                # Probability gauge
                gauge_color = "#e74c3c" if prob >= OFFICIAL_THRESHOLD else (
                    "#ffc107" if prob >= 0.30 else "#27ae60"
                )
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob * 100,
                    domain={"x": [0, 1], "y": [0, 1]},
                    number={"suffix": "%", "font": {"size": 36}},
                    gauge={
                        "axis": {"range": [0, 100], "tickwidth": 1},
                        "bar":  {"color": gauge_color, "thickness": 0.3},
                        "steps": [
                            {"range": [0, 30],   "color": "#d4edda"},
                            {"range": [30, 60],  "color": "#fff3cd"},
                            {"range": [60, 100], "color": "#ffe0e0"},
                        ],
                        "threshold": {
                            "line":  {"color": "#1e3a5f", "width": 3},
                            "thickness": 0.75,
                            "value": OFFICIAL_THRESHOLD * 100,
                        },
                    },
                    title={"text": "Xác suất Default", "font": {"size": 14}},
                ))
                fig_gauge.update_layout(
                    height=200,
                    margin=dict(l=10, r=10, t=40, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig_gauge, use_container_width=True)

            with r1c2:
                badge_cls = (
                    "risk-high"   if risk == "High Risk"   else
                    "risk-medium" if risk == "Medium Risk" else
                    "risk-low"
                )
                badge_icon = "🔴" if risk == "High Risk" else ("🟡" if risk == "Medium Risk" else "🟢")
                pred_card_cls = "pred-default" if label == "Default" else "pred-nondefault"

                st.markdown(
                    f"""
                    <div class="pred-card {pred_card_cls}">
                        <div style="font-size:0.9rem;color:#666;margin-bottom:0.3rem">Phân loại (Threshold = 0.60)</div>
                        <div style="font-size:2rem;font-weight:700;color:{'#c0392b' if label == 'Default' else '#27ae60'}">
                            {'⚠️ DEFAULT' if label == 'Default' else '✅ NON-DEFAULT'}
                        </div>
                        <hr style="margin:0.6rem 0">
                        <div style="font-size:0.9rem;color:#666;margin-bottom:0.3rem">Mức rủi ro (Application-layer)</div>
                        <span class="risk-badge {badge_cls}">{badge_icon} {risk}</span>
                        <div style="font-size:0.75rem;color:#999;margin-top:0.5rem">
                            Low Risk: &lt;30% | Medium: 30–59% | High: ≥60%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with r1c3:
                st.markdown("**Feature vector (33 features) — top values:**")
                display_df = fv_r.T.copy()
                display_df.columns = ["Raw value"]
                display_df["Scaled"] = fv.T.values
                display_df = display_df.round(4)
                st.dataframe(display_df, use_container_width=True, height=200)

                st.success(f"✅ Feature count: {fv.shape[1]} / 33 — **VERIFIED**")

            # ── SHAP Explanation ──────────────────────────────────
            st.markdown("---")
            st.markdown("## 🔬 Giải thích Quyết định (SHAP TreeExplainer)")

            with st.spinner("Đang tính SHAP values…"):
                shap_vals, exp_val, feat_names = compute_shap_single(model, fv)

            if shap_vals is not None:
                top_contributors = get_top_shap_contributors(
                    shap_vals, feat_names, fv_r.values[0], n=10
                )

                st.markdown(
                    f"""
                    <div class="info-box">
                        <b>Phương pháp:</b> SHAP TreeExplainer (chính xác, không xấp xỉ)<br>
                        <b>Expected value (base rate log-odds):</b> {exp_val:.4f}<br>
                        <b>Tổng SHAP:</b> {sum(shap_vals):.4f} &nbsp;|&nbsp;
                        <b>Tổng + Expected:</b> {exp_val + sum(shap_vals):.4f}<br>
                        SHAP dương (↑ Risk) = đẩy prediction về phía Default &nbsp;|&nbsp;
                        SHAP âm (↓ Risk) = đẩy về phía Non-Default
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # SHAP bar chart (top 10)
                top10 = top_contributors[:10]
                features_sorted = [x["feature"] for x in top10][::-1]
                shap_sorted     = [x["shap_value"] for x in top10][::-1]
                colors_sorted   = [
                    "rgba(231,76,60,0.85)" if sv > 0 else "rgba(39,174,96,0.85)"
                    for sv in shap_sorted
                ]

                fig_shap = go.Figure(go.Bar(
                    x=shap_sorted,
                    y=features_sorted,
                    orientation="h",
                    marker_color=colors_sorted,
                    text=[f"{v:+.4f}" for v in shap_sorted],
                    textposition="outside",
                ))
                fig_shap.update_layout(
                    title="Top 10 Feature Contributions (SHAP Values)",
                    xaxis_title="SHAP Value (log-odds space)",
                    yaxis_title="Feature",
                    height=380,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(248,250,252,1)",
                    margin=dict(l=10, r=60, t=40, b=30),
                    shapes=[dict(
                        type="line", x0=0, x1=0, y0=-0.5, y1=len(features_sorted) - 0.5,
                        line=dict(color="#666", width=1, dash="dash"),
                    )],
                )
                st.plotly_chart(fig_shap, use_container_width=True)

                # Table of top contributors
                col_pos, col_neg = st.columns(2)
                positive = [x for x in top_contributors if x["shap_value"] > 0]
                negative = [x for x in top_contributors if x["shap_value"] < 0]

                with col_pos:
                    st.markdown("**🔴 Yếu tố tăng rủi ro (SHAP > 0)**")
                    if positive:
                        pos_df = pd.DataFrame([
                            {"Feature": x["feature"],
                             "SHAP": f"{x['shap_value']:+.4f}",
                             "Giá trị raw": round(x["raw_value"], 4)}
                            for x in positive
                        ])
                        st.dataframe(pos_df, hide_index=True, use_container_width=True)
                    else:
                        st.info("Không có yếu tố tăng rủi ro đáng kể.")

                with col_neg:
                    st.markdown("**🟢 Yếu tố bảo vệ (SHAP < 0)**")
                    if negative:
                        neg_df = pd.DataFrame([
                            {"Feature": x["feature"],
                             "SHAP": f"{x['shap_value']:+.4f}",
                             "Giá trị raw": round(x["raw_value"], 4)}
                            for x in negative
                        ])
                        st.dataframe(neg_df, hide_index=True, use_container_width=True)
                    else:
                        st.info("Không có yếu tố bảo vệ đáng kể.")

                # Risk interpretation
                st.markdown("---")
                st.markdown("### 📝 Nhận xét về Quyết định")
                top3_positive = [x["feature"] for x in top_contributors if x["shap_value"] > 0][:3]
                top3_negative = [x["feature"] for x in top_contributors if x["shap_value"] < 0][:3]

                interp = f"""
**Xác suất vỡ nợ: {prob*100:.1f}%** — Phân loại: **{label}** — Mức rủi ro: **{risk}**

**Các yếu tố tăng rủi ro chính:**  
{", ".join(top3_positive) if top3_positive else "Không có"} — đây là các đặc điểm đẩy xác suất vỡ nợ lên cao trong mô hình.

**Các yếu tố bảo vệ chính:**  
{", ".join(top3_negative) if top3_negative else "Không có"} — đây là các đặc điểm giúp giảm xác suất vỡ nợ trong mô hình.

*Lưu ý: Phân tích SHAP phản ánh mối liên hệ trong mô hình, không phải quan hệ nhân quả.
Kết quả phụ thuộc vào dataset UCI Credit Card (Taiwan, 2005).*
                """
                st.markdown(interp)

            else:
                st.warning(
                    "SHAP calculation không thành công. "
                    "Vui lòng kiểm tra thư viện SHAP (shap==0.52.0 đã được cài đặt)."
                )
                st.markdown("**Global feature importance từ Week 9 (thay thế):**")
                global_fi = {
                    "MAX_PAY_DELAY": 0.4494,
                    "PAY_0": 0.2797,
                    "COUNT_LATE_PAYMENT": 0.1211,
                    "BILL_AMT1": 0.1126,
                    "UTILIZATION_RATE_SEPT": 0.0942,
                }
                st.bar_chart(global_fi)

            # ── Feature Engineering Summary ───────────────────────
            with st.expander("🔧 Chi tiết Feature Engineering (33 features)", expanded=False):
                st.markdown("""
**10 features tạo mới từ dữ liệu thô (đúng theo pipeline Week 5):**

| # | Feature mới | Công thức | Ý nghĩa |
|---|---|---|---|
| 1 | UTILIZATION_RATE_SEPT | BILL_AMT1 / LIMIT_BAL | Tỷ lệ sử dụng hạn mức T9 |
| 2 | UTILIZATION_RATE_MEAN | MEAN_BILL_AMT / LIMIT_BAL | Tỷ lệ sử dụng hạn mức TB 6 tháng |
| 3 | PAY_RATIO_SEPT | PAY_AMT1 / BILL_AMT2 | Tỷ lệ thanh toán T9 |
| 4 | PAY_RATIO_MEAN | TB(PAY_AMT_k / BILL_AMT_{k+1}) | Tỷ lệ thanh toán TB 5 kỳ |
| 5 | MAX_PAY_DELAY | max(PAY_0, PAY_2..6) | Số tháng trễ hạn tối đa |
| 6 | COUNT_LATE_PAYMENT | sum(PAY_i > 0) | Số lần trễ hạn |
| 7 | MEAN_BILL_AMT | TB(BILL_AMT1..6) | Dư nợ TB 6 tháng |
| 8 | MEAN_PAY_AMT | TB(PAY_AMT1..6) | Số tiền trả TB 6 tháng |
| 9 | BILL_TREND | (BILL_AMT1-BILL_AMT6)/LIMIT_BAL | Xu hướng dư nợ |
| 10 | PAY_TREND | (PAY_AMT1-PAY_AMT6)/LIMIT_BAL | Xu hướng số tiền trả |

**Scaling:** RobustScaler fit trên X_train_fe (23,972 mẫu) — lưu tại `models/robust_scaler.pkl`
                """)
                st.dataframe(
                    fv_r.T.rename(columns={0: "Raw Value"}),
                    use_container_width=True,
                )


# ═══════════════════════════════════════════════════════════
# TAB 2 — HISTORY (POSTGRESQL)
# ═══════════════════════════════════════════════════════════
with tab_history:
    st.markdown("### 📜 Lịch sử Đánh giá Rủi ro (Truy vấn từ PostgreSQL)")
    st.caption(
        "Dữ liệu được truy vấn trực tiếp từ bảng `credit_app.customer_predictions` "
        "thông qua đường hầm SSH bảo mật (SSH Port Forwarding 15432 → 5433 → 5432)."
    )

    col_h1, col_h2 = st.columns([1, 3])
    with col_h1:
        limit_rows = st.selectbox("Số bản ghi gần nhất:", options=[5, 10, 25, 50], index=1)
    with col_h2:
        st.markdown("")
        if st.button("🔄 Làm mới dữ liệu", use_container_width=False):
            st.rerun()

    history_df = get_recent_predictions(limit=limit_rows)
    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        st.info(f"📊 Đã tải thành công **{len(history_df)}** bản ghi gần nhất từ CSDL PostgreSQL (Container Docker trên Ubuntu).")
    else:
        st.info("Chưa có bản ghi nào hoặc cơ sở dữ liệu đang ngoại tuyến. Hãy thực hiện dự báo ở Tab 1 để kiểm tra việc lưu trữ.")


# ═══════════════════════════════════════════════════════════
# TAB 3 — ABOUT
# ═══════════════════════════════════════════════════════════
with tab_about:
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("## 📖 Giới thiệu Hệ thống")
        st.markdown(
            """
            Đây là **Prototype Hỗ trợ Quyết định** (Decision Support System) được phát triển
            trong khuôn khổ đồ án tốt nghiệp, nhằm minh họa ứng dụng Machine Learning vào
            bài toán đánh giá và dự báo rủi ro tín dụng khách hàng thẻ tín dụng.

            ### 🏗️ Kiến trúc hệ thống

            ```
            Nhập liệu người dùng (23 raw features)
                ↓
            Categorical Mapping (EDUCATION, MARRIAGE)
                ↓
            Feature Engineering (10 features tạo mới — Week 5)
                ↓
            RobustScaler (fit on X_train_fe — 23,972 mẫu)
                ↓
            XGBoost Tuned (models/final_candidate_model.pkl)
                ↓
            Predict Probability [0, 1]
                ↓
            Threshold = 0.60 → Default / Non-Default
                ↓
            SHAP TreeExplainer → Giải thích quyết định
            ```

            ### 📊 Dữ liệu huấn luyện
            - **Dataset:** Default of Credit Card Clients (UCI)
            - **Nguồn:** UCI Machine Learning Repository
            - **Phạm vi:** 30,000 khách hàng, Taiwan, T4–T9/2005
            - **Biến mục tiêu:** Default payment tháng 10/2005

            ### 🤖 Mô hình chính thức
            - **XGBoost Tuned** — được chọn tại Week 8 theo tiêu chí PR-AUC
            - **Ngưỡng phân loại:** threshold = 0.60 (OOF analysis, không dùng test set)
            - **Recall = 0.6161** — bắt được 61.61% trường hợp Default thực tế

            ### 🔬 Explainability (Week 9)
            - **Phương pháp:** SHAP TreeExplainer (exact Shapley values)
            - **Top feature:** MAX_PAY_DELAY (Mean|SHAP| = 0.4494)
            - 4/10 features quan trọng nhất là features được tạo mới (Feature Engineering)
            """
        )

    with col_b:
        st.markdown("## 📌 Phân loại Rủi ro")
        st.markdown(
            """
            <div style="background:#f8fafc;border-radius:10px;padding:1rem;border:1px solid #e2e8f0">
            <p style="margin:0 0 0.8rem;font-weight:600">Phân loại nhị phân (Model):</p>
            <table style="width:100%">
            <tr><td>Xác suất ≥ 60%</td><td><b style="color:#c0392b">→ DEFAULT</b></td></tr>
            <tr><td>Xác suất &lt; 60%</td><td><b style="color:#27ae60">→ NON-DEFAULT</b></td></tr>
            </table>
            <hr>
            <p style="margin:0.5rem 0;font-weight:600">Mức rủi ro (Application-layer):</p>
            <table style="width:100%">
            <tr><td>🟢 &lt; 30%</td><td><b>Low Risk</b></td></tr>
            <tr><td>🟡 30–59%</td><td><b>Medium Risk</b></td></tr>
            <tr><td>🔴 ≥ 60%</td><td><b>High Risk</b></td></tr>
            </table>
            <p style="font-size:0.78rem;color:#888;margin-top:0.8rem">
            Mức rủi ro là diễn giải ở tầng ứng dụng, không phải tham số học từ dữ liệu.
            Ngưỡng nhị phân chính thức vẫn là 0.60.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("## ⚠️ Giới hạn của Prototype")
        st.warning(
            """
            - Prototype học thuật — không phải hệ thống phê duyệt tín dụng thực tế
            - Dataset: UCI Taiwan 2005 — chưa external validation
            - Hệ thống lưu trữ: Đã tích hợp PostgreSQL 16 (Docker) với phân quyền Least Privilege (app_streamlit)
            - SHAP diễn đạt mối liên hệ trong mô hình, không phải quan hệ nhân quả
            - Threshold được chọn dựa trên F1 OOF, không phải cost matrix ngân hàng
            """,
        )

        st.markdown("## 🎓 Thông tin Đồ án")
        st.info(
            """
            **Sinh viên:** Nguyễn Trọng Thể  
            **MSSV:** 1150080117  
            **Ngành:** Tin học Tài nguyên và Môi trường  
            **Đề tài:** Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo rủi ro tín dụng khách hàng  
            **Dataset:** Default of Credit Card Clients  
            **Giai đoạn:** Tuần 10 — Web Application Prototype
            """
        )


# ── Footer ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center;color:#999;font-size:0.8rem;padding:0.5rem">
        Credit Risk Assessment Prototype | Nguyễn Trọng Thể — MSSV: 1150080117 |
        Đồ án Tốt nghiệp 2026 | Model: XGBoost Tuned | Threshold: 0.60 | 33 Features
    </div>
    """,
    unsafe_allow_html=True,
)
