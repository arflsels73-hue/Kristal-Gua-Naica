import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

# ==========================================
# 1. KONFIGURASI HALAMAN (Aesthetic Mode)
# ==========================================
st.set_page_config(
    page_title="The Crystal Cave Simulator",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk Dark Aesthetic & Glow
st.markdown("""
    <style>
    .stApp {
        background-color: #05050A;
        color: #E0E0FF;
    }
    .css-1d391kg, .css-1lcbmhc {
        background-color: #0A0A14 !important;
    }
    h1, h2, h3 {
        color: #DDA0DD !important;
        font-family: 'Georgia', serif;
    }
    .metric-box {
        background: linear-gradient(145deg, #121220, #0a0a14);
        border: 1px solid #3b205e;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(138, 43, 226, 0.2);
    }
    .metric-value { font-size: 24px; font-weight: bold; color: #E0B0FF; }
    .metric-label { font-size: 12px; color: #8A8A9E; text-transform: uppercase; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ALGORITMA INFORMATIKA: FRACTAL 3D
# ==========================================
def generate_crystal_fractal(iterations, branches, length, angle_variance, depth=0, current_point=np.array([0.0, 0.0, 0.0]), current_vector=np.array([0.0, 0.0, 1.0]), data=None):
    """
    Fungsi rekursif untuk menghasilkan koordinat titik-titik kristal dalam ruang 3D.
    Menggunakan logika matriks rotasi vektor dan kalkulus geometri.
    """
    if data is None:
        data = {'x': [], 'y': [], 'z': [], 'color': [], 'size': []}
        
    if depth >= iterations:
        return data

    for _ in range(branches):
        # Matriks Rotasi Acak (Trigonometri 3D)
        theta = random.uniform(-angle_variance, angle_variance)
        phi = random.uniform(0, 2 * np.pi)
        
        # Rotasi Vektor
        x_rot = np.sin(theta) * np.cos(phi)
        y_rot = np.sin(theta) * np.sin(phi)
        z_rot = np.cos(theta)
        
        new_vector = current_vector + np.array([x_rot, y_rot, z_rot])
        new_vector = new_vector / np.linalg.norm(new_vector) # Normalisasi Vektor
        
        # Hitung Titik Ujung Kristal (End Point)
        branch_length = length * random.uniform(0.7, 1.3) * (0.85 ** depth)
        end_point = current_point + (new_vector * branch_length)
        
        # Simpan Jalur Garis (dengan nilai None agar Plotly memutus garis)
        data['x'].extend([current_point[0], end_point[0], None])
        data['y'].extend([current_point[1], end_point[1], None])
        data['z'].extend([current_point[2], end_point[2], None])
        
        # Warna dan ketebalan memudar seiring pertumbuhan
        data['color'].extend([depth, depth, None])
        
        # Panggil fungsi ini lagi secara rekursif
        generate_crystal_fractal(
            iterations, 
            branches=random.randint(1, 3) if depth > 0 else branches, 
            length=length, 
            angle_variance=angle_variance, 
            depth=depth+1, 
            current_point=end_point, 
            current_vector=new_vector, 
            data=data
        )
        
    return data

# ==========================================
# 3. SIDEBAR (Parameter Fisika & Kimia)
# ==========================================
st.sidebar.markdown("## ⚙️ Parameter Geologi")
st.sidebar.caption("Atur variabel termodinamika untuk melihat hasil simulasi pertumbuhan.")

suhu_magma = st.sidebar.slider("Suhu Inti Magma (°C)", 100, 1000, 500, 10)
tekanan = st.sidebar.slider("Tekanan Atmosfer Bawah Tanah (atm)", 10, 200, 100, 5)
waktu_geologi = st.sidebar.slider("Siklus Pertumbuhan (Ribu Tahun)", 1, 10, 5, 1)

mineral_type = st.sidebar.selectbox("Jenis Mineral", ["Amethyst (Ungu)", "Quartz (Bening)", "Malachite (Hijau)", "Citrine (Kuning)"])

# Logika Warna Estetik Berdasarkan Mineral
color_scales = {
    "Amethyst (Ungu)": "Purples",
    "Quartz (Bening)": "Greys",
    "Malachite (Hijau)": "Tealgrn",
    "Citrine (Kuning)": "Wistia"
}
selected_colorscale = color_scales[mineral_type]

st.sidebar.markdown("---")
st.sidebar.info("💡 **Konsep Sains:** Kristal tumbuh saat fluida hidrotermal mendingin secara perlahan. Semakin lama waktu geologi, semakin kompleks cabang sel kristalnya.")

# ==========================================
# 4. KONEKSI LOGIKA KE ALGORITMA
# ==========================================
# Suhu mempengaruhi seberapa acak/berantakan arah tumbuhnya (Entropy)
variance = np.interp(suhu_magma, [100, 1000], [0.1, 0.8])
# Tekanan mempengaruhi kepadatan cabang kristal
branching_factor = int(np.interp(tekanan, [10, 200], [2, 5]))
# Waktu mempengaruhi kedalaman iterasi (seberapa panjang kristal tumbuh)
iterasi = waktu_geologi

# Eksekusi Algoritma Generate
with st.spinner("Menginkubasi mineral... Merender matriks 3D..."):
    crystal_data = generate_crystal_fractal(
        iterations=iterasi, 
        branches=branching_factor, 
        length=10.0, 
        angle_variance=variance
    )

# Hitung Total Fraktal untuk Dasbor
total_bonds = len([x for x in crystal_data['x'] if x is not None]) // 2

# ==========================================
# 5. RENDER 3D ESTETIK (PLOTLY)
# ==========================================
fig = go.Figure()

# Menambahkan Jalur Garis (Struktur Inti Kristal)
fig.add_trace(go.Scatter3d(
    x=crystal_data['x'], y=crystal_data['y'], z=crystal_data['z'],
    mode='lines',
    line=dict(
        color=crystal_data['color'],
        colorscale=selected_colorscale,
        width=4,
        reversescale=True
    ),
    hoverinfo='none',
    opacity=0.8
))

# Menambahkan Partikel Ujung Kristal (Efek Glow/Pendar)
# Hanya mengambil titik ujung dari cabang (koordinat yang sebelum None)
end_x = [crystal_data['x'][i-1] for i in range(1, len(crystal_data['x'])) if crystal_data['x'][i] is None]
end_y = [crystal_data['y'][i-1] for i in range(1, len(crystal_data['y'])) if crystal_data['y'][i] is None]
end_z = [crystal_data['z'][i-1] for i in range(1, len(crystal_data['z'])) if crystal_data['z'][i] is None]

fig.add_trace(go.Scatter3d(
    x=end_x, y=end_y, z=end_z,
    mode='markers',
    marker=dict(
        size=5,
        color='white',
        symbol='diamond',
        opacity=0.9,
        line=dict(width=1, color='rgba(255,255,255,0.5)')
    ),
    hoverinfo='none'
))

# Membersihkan Axis agar terlihat seperti Hologram Melayang
fig.update_layout(
    paper_bgcolor='#05050A',
    margin=dict(l=0, r=0, b=0, t=0),
    scene=dict(
        xaxis=dict(visible=False, showgrid=False, zeroline=False),
        yaxis=dict(visible=False, showgrid=False, zeroline=False),
        zaxis=dict(visible=False, showgrid=False, zeroline=False),
        camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.2, y=1.2, z=1.2) # Jarak pandang kamera
        )
    ),
    showlegend=False
)

# ==========================================
# 6. TAMPILAN DASHBOARD UTAMA
# ==========================================
st.title("💎 The Cave of Crystals: 3D Simulator")
st.markdown("Visualisasi komputasional pertumbuhan mineral fraktal dalam ruang $3D$ berdasarkan hukum termodinamika.")

# Deretan Dasbor Estetik
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'<div class="metric-box"><div class="metric-value">{total_bonds:,}</div><div class="metric-label">Ikatan Sel Kristal</div></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-box"><div class="metric-value">{suhu_magma}°C</div><div class="metric-label">Temperatur Magma</div></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-box"><div class="metric-value">{tekanan} atm</div><div class="metric-label">Tekanan Fluida</div></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-box"><div class="metric-value">{variance:.2f} S</div><div class="metric-label">Entropi (Acak)</div></div>', unsafe_allow_html=True)

st.write("") # Spacer

# Render Grafik 3D
st.plotly_chart(fig, use_container_width=True, height=600)

st.caption("Gunakan *mouse* atau jari untuk memutar, memperbesar, dan menggeser hologram kristal $3D$ di atas. Dikembangkan dengan Python & Plotly.")
