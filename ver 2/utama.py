import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. Konfigurasi Halaman (Harus selalu di paling atas)
st.set_page_config(
    page_title="Neo-Earth: Geological Pulse", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    page_icon="🌍"
)

# 2. Injeksi Custom CSS (Vibe Cyberpunk & Menyembunyikan Menu Streamlit)
st.markdown("""
    <style>
        /* Menyembunyikan header, footer, dan menu bawaan Streamlit */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Mengubah latar belakang utama menjadi hitam pekat */
        .stApp {
            background-color: #050505;
        }
        
        /* Kustomisasi Teks dengan efek Neon */
        h1 {
            color: #00FFFF;
            text-align: center;
            font-family: 'Courier New', Courier, monospace;
            text-shadow: 0 0 5px #00FFFF, 0 0 15px #00FFFF;
            margin-bottom: 0px;
        }
        .subtitle {
            color: #FF00FF;
            text-align: center;
            font-family: 'Courier New', Courier, monospace;
            text-shadow: 0 0 5px #FF00FF;
            margin-top: -10px;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>NEO-EARTH: 3D GLOBAL GEOLOGICAL PULSE</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Live Seismic Activity // Otorisasi: Diterima</p>", unsafe_allow_html=True)

# 3. Fungsi Menarik Data Geospasial Real-time (USGS Earthquake Data)
@st.cache_data(ttl=600) # Data di-cache dan diperbarui setiap 10 menit
def fetch_live_earthquake_data():
    # Menarik data gempa bumi > M 2.5 dalam 24 jam terakhir
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari satelit: {e}")
        return pd.DataFrame()

df_quake = fetch_live_earthquake_data()

if not df_quake.empty:
    # 4. Membangun Proyeksi Bola Bumi 3D
    fig = go.Figure()

    # Lapisan A: Efek Partikel Pendaran (Glow/Halo effect)
    # Kita menggunakan marker yang lebih besar namun transparan
    fig.add_trace(go.Scattergeo(
        lon = df_quake['longitude'],
        lat = df_quake['latitude'],
        hoverinfo = 'skip',
        marker = dict(
            size = df_quake['mag'] ** 2.5, # Perhitungan matematis eksponensial untuk radius pendaran
            color = df_quake['mag'],
            # Gradasi warna neon yang transparan
            colorscale = [[0, 'rgba(0, 255, 255, 0.2)'], [0.5, 'rgba(255, 215, 0, 0.2)'], [1, 'rgba(255, 0, 255, 0.2)']],
        ),
        showlegend = False
    ))

    # Lapisan B: Titik Gempa Inti (Core Seismic Point)
    fig.add_trace(go.Scattergeo(
        lon = df_quake['longitude'],
        lat = df_quake['latitude'],
        text = df_quake['place'] + '<br>Magnitude: ' + df_quake['mag'].astype(str) + ' SR<br>Kedalaman: ' + df_quake['depth'].astype(str) + ' km',
        marker = dict(
            size = df_quake['mag'] ** 1.8, # Ukuran inti lebih kecil
            color = df_quake['mag'],
            colorscale = [[0, '#00FFFF'], [0.5, '#FFD700'], [1, '#FF00FF']], # Cyan -> Gold -> Magenta
            showscale = True,
            colorbar_title = "Magnitude",
            colorbar = dict(tickfont=dict(color='#00FFFF'), titlefont=dict(color='#00FFFF')),
            line = dict(width=1, color='rgba(255, 255, 255, 0.9)')
        ),
        name = 'Titik Episentrum'
    ))

    # 5. Pengaturan Environment (Lighting & Tekstur Bola Bumi)
    fig.update_geos(
        projection_type="orthographic", # Mengubah peta 2D menjadi Bola Bumi 3D
        showcoastlines=True,
        coastlinecolor="#00FFFF",       # Garis pantai bercahaya Cyan
        coastlinewidth=0.5,
        showland=True,
        landcolor="#0A0A0A",            # Daratan hitam gelap
        showocean=True,
        oceancolor="#020202",           # Lautan hitam pekat
        showlakes=False,
        showcountries=True,
        countrycolor="#1A1A1A",         # Batas negara remang-remang
        framecolor="#050505",
        bgcolor="#050505",              # Menghilangkan background kotak bawaan Plotly
        resolution=50                   # Resolusi render menengah untuk performa
    )

    # 6. Finalisasi Tata Letak & Kamera
    fig.update_layout(
        paper_bgcolor="#050505",
        plot_bgcolor="#050505",
        margin=dict(t=10, b=10, l=0, r=0),
        geo=dict(
            center=dict(lon=113.92, lat=-0.78), # Posisi kamera awal menghadap wilayah Indonesia
            projection_scale=1.1 # Default Zoom-in
        )
    )

    # Menampilkan ke Streamlit dengan ukuran penuh
    st.plotly_chart(fig, use_container_width=True)

    # Footer/Data Statistik sederhana di bawah bola bumi
    st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<p style='color: #00FFFF; text-align: center;'>Total Terdeteksi: <b>{len(df_quake)} Gempa</b></p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='color: #FFD700; text-align: center;'>Magnitudo Maks: <b>{df_quake['mag'].max()} SR</b></p>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p style='color: #FF00FF; text-align: center;'>Sumber Data: <b>USGS API (Real-time)</b></p>", unsafe_allow_html=True)

else:
    st.warning("Menunggu koneksi ke satelit USGS...")
