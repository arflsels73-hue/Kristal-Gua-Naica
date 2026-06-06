import streamlit as st
import pandas as pd
import requests

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Neo-Earth Terminal", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Gaya Cyberpunk (Latar Belakang Gelap & Teks Neon)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        .stApp {
            background-color: #0B0C10;
        }
        h1 {
            color: #1F2833;
            text-align: center;
            font-family: 'Courier New', monospace;
            color: #00FFCC;
            text-shadow: 0 0 10px #00FFCC;
        }
        .status-bar {
            color: #66FCF1;
            text-align: center;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>[ NEO-EARTH: TACTICAL SEISMIC MAP ]</h1>", unsafe_allow_html=True)

# 3. Fungsi Ambil Data Gempa Real-time
@st.cache_data(ttl=300)
def load_seismic_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.csv"
    try:
        df = pd.read_csv(url)
        
        # Beri warna neon berdasarkan kekuatan gempa (Magnitudo)
        # Gempa kuat = Merah Neon (#FF0055), Gempa sedang = Cyan (#00FFFF)
        df['color'] = df['mag'].apply(lambda x: '#FF0055' if x >= 5.0 else '#00FFFF')
        
        # Mengatur ukuran titik di peta berdasarkan magnitudo (dalam meter)
        df['size'] = df['mag'] * 25000 
        
        return df
    except:
        return pd.DataFrame()

df = load_seismic_data()

if not df.empty:
    st.markdown("<p class='status-bar'>► SYSTEM STATUS: ONLINE // LINKING TO SATELLITE DATA...</p>", unsafe_allow_html=True)
    
    # 4. FITUR UTAMA: Peta Digital Bawaan Streamlit (Bisa di-zoom & digeser)
    st.map(
        df, 
        latitude='latitude', 
        longitude='longitude', 
        color='color', 
        size='size', 
        use_container_width=True
    )
    
    # 5. Panel Informasi / Log Data (Tampilan Tabel Hacker)
    st.markdown("<h3 style='color:#00FFCC; font-family:monospace;'>► REAL-TIME SEISMIC LOGS</h3>", unsafe_allow_html=True)
    
    # Saring kolom yang penting saja agar rapi
    df_display = df[['time', 'mag', 'place', 'depth']].copy()
    df_display.columns = ['WAKTU (UTC)', 'MAGNITUDO', 'LOKASI', 'KEDALAMAN (KM)']
    
    # Tampilkan tabel data interaktif
    st.dataframe(df_display.head(15), use_container_width=True)
    
else:
    st.error("ERROR: Gagal terhubung ke satelit BMKG/USGS. Periksa koneksi internet.")
