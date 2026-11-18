
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Sleman Weather Monitor",
    page_icon="🌤️",
    layout="wide"
)

DB_PATH = Path(__file__).resolve().parent / "sleman_weather.db"


def get_weather_data():
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            waktu_update,
            suhu,
            kelembapan,
            kecepatan_angin,
            kode_cuaca,
            kondisi
        FROM weather_data
        ORDER BY waktu_update DESC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


st.markdown("""
<style>
    .stApp {
        background-color: #F4F7FC;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-header {
        background: linear-gradient(120deg, #17365D, #2563A6);
        padding: 28px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
    }

    .main-header h1 {
        color: white;
        font-size: 30px;
        margin-bottom: 5px;
    }

    .main-header p {
        color: #DCEBFA;
        font-size: 14px;
        margin-bottom: 0;
    }

    .section-header {
        color: #17365D;
        font-size: 21px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 12px;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04);
    }

    [data-testid="stSidebar"] {
        background-color: #EAF1FA;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 1.5rem 1.2rem 1rem 1.2rem;
    }

    .sidebar-brand {
        padding-bottom: 16px;
        border-bottom: 1px solid #D2DCE9;
        margin-bottom: 20px;
    }

    .sidebar-brand h2 {
        font-size: 19px;
        color: #17365D;
        margin: 0;
        font-weight: 700;
    }

    .sidebar-brand p {
        color: #64748B;
        font-size: 12px;
        margin: 5px 0 0 0;
    }

    .sidebar-heading {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        letter-spacing: 1px;
        margin-bottom: 13px;
    }

    .sidebar-item {
        display: flex;
        align-items: flex-start;
        gap: 11px;
        margin-bottom: 17px;
    }

    .sidebar-icon {
        font-size: 17px;
        width: 23px;
        flex-shrink: 0;
        padding-top: 1px;
    }

    .sidebar-info {
        flex: 1;
    }

    .sidebar-info strong {
        display: block;
        color: #17365D;
        font-size: 13px;
        font-weight: 650;
        margin-bottom: 3px;
    }

    .sidebar-info span {
        display: block;
        color: #64748B;
        font-size: 12px;
        line-height: 1.4;
    }

    .sidebar-divider {
        border-top: 1px solid #D2DCE9;
        margin: 18px 0;
    }

    .sidebar-note {
        color: #64748B;
        font-size: 12px;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    [data-testid="stSidebar"] .stButton button {
        width: 100%;
        background-color: #2563A6;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        padding: 9px;
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #17365D;
        color: white;
    }

    div[data-testid="stPlotlyChart"] {
        background-color: white;
        border-radius: 12px;
        padding: 8px;
        border: 1px solid #E2E8F0;
    }

    .footer {
        text-align: center;
        color: #64748B;
        font-size: 12px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>🌤️ Sleman Weather</h2>
        <p>Weather Monitoring System</p>
    </div>

    <div class="sidebar-heading">INFORMASI SISTEM</div>

    <div class="sidebar-item">
        <div class="sidebar-icon">📍</div>
        <div class="sidebar-info">
            <strong>Lokasi</strong>
            <span>Kabupaten Sleman, Yogyakarta</span>
        </div>
    </div>

    <div class="sidebar-item">
        <div class="sidebar-icon">🌐</div>
        <div class="sidebar-info">
            <strong>Sumber Data</strong>
            <span>Open-Meteo API</span>
        </div>
    </div>

    <div class="sidebar-item">
        <div class="sidebar-icon">💾</div>
        <div class="sidebar-info">
            <strong>Database</strong>
            <span>SQLite</span>
        </div>
    </div>

    <div class="sidebar-divider"></div>

    <div class="sidebar-heading">PEMBARUAN DATA</div>

    <div class="sidebar-note">
        🔄 Data diperbarui melalui Telegram Bot.
    </div>
    """, unsafe_allow_html=True)

    if st.button("↻  Refresh Dashboard", use_container_width=True):
        st.rerun()

    st.markdown("""
    <div class="sidebar-divider"></div>
    <div style="text-align:center; color:#94A3B8; font-size:10px;">
        Sleman Weather Monitor<br>
        Python • Streamlit • SQLite
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="main-header">
    <h1>🌤️ Sleman Weather Monitor</h1>
    <p>Dashboard Pemantauan Kondisi Cuaca Kabupaten Sleman</p>
</div>
""", unsafe_allow_html=True)


df = get_weather_data()

if df.empty:
    st.warning(
        "Belum ada data cuaca. Silakan jalankan scraper.py "
        "atau gunakan perintah /cekcuaca melalui Telegram."
    )
    st.stop()

df["waktu_update"] = pd.to_datetime(
    df["waktu_update"],
    errors="coerce"
)

df = df.dropna(subset=["waktu_update"])

if df.empty:
    st.warning("Data waktu cuaca tidak dapat dibaca.")
    st.stop()

df = df.sort_values("waktu_update")
latest = df.iloc[-1]


st.markdown(
    '<div class="section-header">📍 Kondisi Cuaca Terbaru</div>',
    unsafe_allow_html=True
)

st.caption(
    "Waktu data: "
    + latest["waktu_update"].strftime("%d-%m-%Y %H:%M")
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🌡️ Suhu", f"{latest['suhu']} °C")

with col2:
    st.metric("💧 Kelembapan", f"{latest['kelembapan']}%")

with col3:
    st.metric(
        "💨 Kecepatan Angin",
        f"{latest['kecepatan_angin']} km/jam"
    )

with col4:
    st.metric("☁️ Kondisi Cuaca", str(latest["kondisi"]))


st.markdown(
    '<div class="section-header">📊 Grafik Riwayat Cuaca</div>',
    unsafe_allow_html=True
)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    fig_suhu = px.line(
        df,
        x="waktu_update",
        y="suhu",
        markers=True,
        title="🌡️ Perubahan Suhu",
        labels={
            "waktu_update": "Waktu",
            "suhu": "Suhu (°C)"
        }
    )

    fig_suhu.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    fig_suhu.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=55, b=20),
        hovermode="x unified"
    )

    st.plotly_chart(fig_suhu, use_container_width=True)


with col_chart2:
    fig_kelembapan = px.line(
        df,
        x="waktu_update",
        y="kelembapan",
        markers=True,
        title="💧 Perubahan Kelembapan",
        labels={
            "waktu_update": "Waktu",
            "kelembapan": "Kelembapan (%)"
        }
    )

    fig_kelembapan.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    fig_kelembapan.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=55, b=20),
        hovermode="x unified"
    )

    st.plotly_chart(fig_kelembapan, use_container_width=True)


st.markdown(
    '<div class="section-header">📋 Riwayat Data Cuaca</div>',
    unsafe_allow_html=True
)

st.caption(f"Total data tersimpan: {len(df)} data")

riwayat = df.sort_values(
    "waktu_update",
    ascending=False
).copy()

riwayat["waktu_update"] = (
    riwayat["waktu_update"].dt.strftime("%d-%m-%Y %H:%M")
)

riwayat = riwayat.rename(columns={
    "waktu_update": "Waktu",
    "suhu": "Suhu (°C)",
    "kelembapan": "Kelembapan (%)",
    "kecepatan_angin": "Kecepatan Angin (km/jam)",
    "kode_cuaca": "Kode Cuaca",
    "kondisi": "Kondisi"
})

st.dataframe(
    riwayat,
    use_container_width=True,
    hide_index=True
)


st.markdown("""
<div class="footer">
    Sleman Weather Monitor |
    Python • Streamlit • SQLite • Open-Meteo API • Telegram Bot
</div>
""", unsafe_allow_html=True)
