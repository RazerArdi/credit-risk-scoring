"""
Modul Deployment Dasbor Eksekutif: Credit Audit Center.

Skrip ini merender antarmuka pengguna berbasis Streamlit untuk memfasilitasi
audit kelayakan kredit tingkat individu. Modul ini mengintegrasikan Champion Model
(XGBoost) untuk kalkulasi probabilitas gagal bayar dan pustaka SHAP (Explainable AI)
guna mendekonstruksi logika keputusan algoritma secara waktu nyata.
Dilengkapi dengan mesin konversi otomatis untuk membalikkan nilai Z-Score ke angka riil.

Cara menjalankan:
    conda activate base
    streamlit run dashboard/app.py
"""

import os
import pickle
import warnings

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import shap
import streamlit as st

warnings.filterwarnings("ignore")


def build_shap_waterfall(explanation, max_display: int = 10) -> go.Figure:
    """
    Membangun Plotly Waterfall chart dari objek shap.Explanation.

    Menampilkan top-N fitur berdasarkan nilai absolut SHAP terbesar,
    diurutkan dari yang paling berpengaruh di bagian atas.

    Args:
        explanation: Objek shap.Explanation untuk satu observasi.
        max_display: Jumlah maksimum fitur yang ditampilkan.

    Returns:
        fig: Objek plotly.graph_objects.Figure siap render.
    """
    shap_vals = explanation.values
    feat_names = list(explanation.feature_names)
    base_val = float(explanation.base_values)

    order = np.argsort(np.abs(shap_vals))[::-1][:max_display]
    order = order[::-1]

    top_names = [feat_names[i] for i in order]
    top_vals = [float(shap_vals[i]) for i in order]

    bar_colors = ["#ff4d6d" if v > 0 else "#00c49a" for v in top_vals]
    text_labels = [f"+{v:.3f}" if v > 0 else f"{v:.3f}" for v in top_vals]

    all_names = [f"E[f(X)] = {base_val:.3f}"] + top_names
    all_vals = [base_val] + top_vals
    all_text = [f"{base_val:.3f}"] + text_labels
    measures = ["absolute"] + ["relative"] * len(top_vals)

    fig = go.Figure(
        go.Waterfall(
            name="SHAP",
            orientation="h",
            measure=measures,
            y=all_names,
            x=all_vals,
            text=all_text,
            textposition="outside",
            connector={"line": {"color": "#2d3748", "width": 1, "dash": "dot"}},
            increasing={"marker": {"color": "#ff4d6d"}},
            decreasing={"marker": {"color": "#00c49a"}},
            totals={"marker": {"color": "#4a5568"}},
            textfont={"color": "#e2e8f0", "size": 11},
        )
    )

    fig.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#e2e8f0", family="'JetBrains Mono', 'Courier New', monospace"),
        height=420,
        margin=dict(l=20, r=60, t=40, b=20),
        title=dict(
            text="Kontribusi Fitur terhadap Keputusan (SHAP Waterfall)",
            font=dict(size=14, color="#a0aec0"),
            x=0,
        ),
        xaxis=dict(
            gridcolor="#1e2533",
            zerolinecolor="#4a5568",
            zerolinewidth=1.5,
            tickfont=dict(size=10),
            title=dict(
                text="SHAP Value (dampak terhadap output model)",
                font=dict(size=11),
            ),
        ),
        yaxis=dict(gridcolor="#1e2533", tickfont=dict(size=10)),
        hoverlabel=dict(bgcolor="#1a202c", font_size=12),
    )

    fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="#718096")
    return fig


def _render_profile_card(title: str, rows: list[tuple]) -> str:
    """
    Merakit string HTML untuk sebuah kartu profil nasabah.

    Setiap baris direpresentasikan sebagai tuple (tag_class, tag_label, value_html).
    Fungsi ini memastikan semua tag div terbuka dan tertutup dengan benar.

    Args:
        title: Judul bagian kartu (ditampilkan di header kartu).
        rows: Daftar tuple (tag_css_class, label_tag, nilai_html).

    Returns:
        String HTML lengkap untuk satu kartu profil.
    """
    rows_html = ""
    for tag_class, tag_label, value_html in rows:
        rows_html += (
            f'<div class="profile-card__row">'
            f'<span class="tag {tag_class}">{tag_label}</span>'
            f'{value_html}'
            f"</div>"
        )

    return (
        f'<div class="profile-card">'
        f'<div class="profile-card__title">{title}</div>'
        f"{rows_html}"
        f"</div>"
    )


def main():
    """
    Fungsi utama untuk merakit dan merender seluruh komponen dasbor Streamlit.

    Menerapkan kalkulasi balik matematis untuk menyajikan data yang dipahami
    oleh pengguna awam. Urutan render: header → load aset → sidebar →
    scorecard → profil nasabah → SHAP waterfall.
    """
    st.set_page_config(
        page_title="Credit Audit Center",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CSS_PATH = os.path.join(BASE_DIR, "dashboard", "assets", "custom.css")

    try:
        with open(CSS_PATH) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    st.markdown(
        """
        <div class="cr-header">
            <div class="cr-header__badge">LIVE AUDIT</div>
            <h1 class="cr-header__title">CREDIT AUDIT CENTER</h1>
            <p class="cr-header__sub">Audit Kelayakan Kredit Terpadu · Berbasis Explainable AI</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    @st.cache_resource
    def load_assets():
        """Memuat model XGBoost dan dataset uji dari direktori yang telah ditentukan."""
        model_path = os.path.join(BASE_DIR, "models", "champion_xgboost.pkl")
        x_test_encoded_path = os.path.join(
            BASE_DIR, "data", "processed", "X_test_encoded.pkl"
        )
        y_test_path = os.path.join(BASE_DIR, "data", "processed", "y_test.pkl")
        x_test_raw_path = os.path.join(
            BASE_DIR, "data", "processed", "X_test_raw.pkl"
        )

        with open(model_path, "rb") as f:
            loaded_model = pickle.load(f)

        data_x_encoded = pd.read_pickle(x_test_encoded_path)
        data_y = pd.read_pickle(y_test_path)
        data_x_encoded.columns = data_x_encoded.columns.str.replace(
            r"[<,>\[\]]", "_", regex=True
        )

        data_x_raw = (
            pd.read_pickle(x_test_raw_path)
            if os.path.exists(x_test_raw_path)
            else None
        )
        return loaded_model, data_x_encoded, data_x_raw, data_y

    try:
        model, X_test_encoded, X_test_raw, y_test = load_assets()
    except Exception as e:
        st.error(f"Gagal memuat model atau data. Detail: {e}")
        st.stop()

    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### ⚙ PANEL OPERASIONAL")
        st.markdown("Pilih ID Nasabah dari antrean data uji untuk diaudit:")
        selected_id = st.selectbox(
            "ID Nasabah (Index):", X_test_encoded.index.tolist()
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.divider()
        st.caption("© 2026 Credit Audit AI · Arsitektur BNSP Data Scientist")

    customer_encoded = X_test_encoded.loc[[selected_id]]
    actual_label = y_test.loc[selected_id]
    prob_val = model.predict_proba(customer_encoded)[0][1]
    THRESHOLD = 0.45
    prediction = "DITOLAK" if prob_val >= THRESHOLD else "DISETUJUI"

    st.markdown(
        '<div class="section-title">Scorecard Risiko</div>', unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        status_hist = "MACET" if actual_label == 1 else "LANCAR"
        color_hist = "#ff4d6d" if actual_label == 1 else "#00c49a"
        st.markdown(
            f'<div class="scorecard">'
            f'<div class="scorecard__label">Status Historis</div>'
            f'<div class="scorecard__value" style="color:{color_hist}">{status_hist}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    with col2:
        risk_color = "#ff4d6d" if prob_val >= THRESHOLD else "#00c49a"
        st.markdown(
            f'<div class="scorecard">'
            f'<div class="scorecard__label">Probabilitas Risiko</div>'
            f'<div class="scorecard__value" style="color:{risk_color}">{prob_val * 100:.2f}%</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    with col3:
        dec_color = "#ff4d6d" if prediction == "DITOLAK" else "#00c49a"
        dec_icon = "✕" if prediction == "DITOLAK" else "✓"
        st.markdown(
            f'<div class="scorecard scorecard--decision" style="border-left-color:{dec_color}">'
            f'<div class="scorecard__label">Keputusan Sistem</div>'
            f'<div class="scorecard__value" style="color:{dec_color}">{dec_icon} {prediction}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown(
        '<div class="section-title">Profil Komprehensif Nasabah (KYC & Finansial)</div>',
        unsafe_allow_html=True,
    )

    if X_test_raw is not None:
        raw = X_test_raw.loc[[selected_id]]
        age_riil = int(raw["age_years"].values[0])
        duration_riil = int(raw["duration_months"].values[0])
        amount_riil = int(raw["credit_amount"].values[0])
        installment_riil = int(raw["installment_rate"].values[0])
        age_z = float(customer_encoded["age_years"].values[0])
        duration_z = float(customer_encoded["duration_months"].values[0])
        amount_z = float(customer_encoded["credit_amount"].values[0])
    else:
        age_z = float(customer_encoded["age_years"].values[0])
        duration_z = float(customer_encoded["duration_months"].values[0])
        amount_z = float(customer_encoded["credit_amount"].values[0])
        installment_riil = 0
        age_riil = int(round(35.54 + age_z * 11.38))
        duration_riil = int(round(20.90 + duration_z * 12.06))
        amount_riil = int(round(3271.26 + amount_z * 2822.74))

    if age_riil < 25:
        age_segment = "Awal Karir (18–24 Th)"
    elif age_riil <= 40:
        age_segment = "Produktif (25–40 Th)"
    elif age_riil <= 60:
        age_segment = "Matang (41–60 Th)"
    else:
        age_segment = "Pensiun (>60 Th)"

    def _flag(col: str) -> bool:
        """Mengembalikan True jika kolom one-hot tertentu bernilai 1 untuk nasabah terpilih."""
        return (
            col in customer_encoded.columns
            and customer_encoded[col].values[0] == 1
        )

    is_skilled = _flag("job_skilled employee/official")
    is_minus = _flag("checking_account_status__ 0 DM")
    is_business = _flag("purpose_business")
    low_savings = _flag("savings_account_status__ 100 DM")
    bad_history = _flag("credit_history_critical account/other credits")

    pc1, pc2, pc3, pc4 = st.columns(4)

    with pc1:
        card_html = _render_profile_card(
            "Data Demografi",
            [
                ("tag--neutral", "Usia Aktual", f"<strong>{age_riil} Tahun</strong>"),
                ("tag--muted", "Z-Score", f'<span class="mono">{age_z:.2f}</span>'),
                ("tag--neutral", "Segmen", f"<strong>{age_segment}</strong>"),
            ],
        )
        st.markdown(card_html, unsafe_allow_html=True)

    with pc2:
        rows_pinjaman = [
            ("tag--neutral", "Plafon", f"<strong>{amount_riil:,} DM</strong>"),
            ("tag--muted", "Z-Score", f'<span class="mono">{amount_z:.2f}</span>'),
            ("tag--neutral", "Tenor", f"<strong>{duration_riil} Bulan</strong>"),
        ]
        if installment_riil > 0:
            rows_pinjaman.append(
                ("tag--neutral", "Cicilan", f"<strong>{installment_riil}%</strong>")
            )
        card_html = _render_profile_card("Profil Pinjaman", rows_pinjaman)
        st.markdown(card_html, unsafe_allow_html=True)

    with pc3:
        job_text = "Tenaga Ahli" if is_skilled else "Sektor Lain"
        rk_class = "tag--danger" if is_minus else "tag--success"
        rk_text = "Defisit (<0 DM)" if is_minus else "Stabil (≥0 DM)"
        sav_class = "tag--danger" if low_savings else "tag--success"
        sav_text = "Rendah (<100 DM)" if low_savings else "Cukup / Tinggi"
        card_html = _render_profile_card(
            "Aset & Likuiditas",
            [
                ("tag--neutral", "Pekerjaan", f"<strong>{job_text}</strong>"),
                (rk_class, "Rek. Harian", f"<strong>{rk_text}</strong>"),
                (sav_class, "Tabungan", f"<strong>{sav_text}</strong>"),
            ],
        )
        st.markdown(card_html, unsafe_allow_html=True)

    with pc4:
        hist_class = "tag--danger" if bad_history else "tag--success"
        hist_text = "Kritis / Berisiko" if bad_history else "Lancar"
        purp_text = "Modal Usaha" if is_business else "Konsumtif"
        card_html = _render_profile_card(
            "Riwayat Historis",
            [
                (hist_class, "Kredit Lain", f"<strong>{hist_text}</strong>"),
                ("tag--neutral", "Tujuan", f"<strong>{purp_text}</strong>"),
            ],
        )
        st.markdown(card_html, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        '<div class="section-title">Radar Transparansi Algoritma · SHAP Waterfall</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="section-sub">Dekomposisi kontribusi setiap fitur terhadap keputusan akhir secara waktu nyata.</p>',
        unsafe_allow_html=True,
    )

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(customer_encoded)

    explanation = shap.Explanation(
        values=shap_values[0],
        base_values=explainer.expected_value,
        data=customer_encoded.iloc[0],
        feature_names=X_test_encoded.columns.tolist(),
    )

    fig = build_shap_waterfall(explanation, max_display=10)
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()