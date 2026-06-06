import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. KONFIGURASI HALAMAN (Dark Aesthetic)
# ==========================================
st.set_page_config(
    page_title="Bioluminescence Simulator",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk membuat UI Streamlit jadi estetik gelap
st.markdown("""
    <style>
    .stApp { background-color: #0d0e15; color: #e2e8f0; }
    h1, h2, h3 { color: #00f2fe; font-family: 'Courier New', Courier, monospace; text-shadow: 0 0 10px rgba(0, 242, 254, 0.5); }
    .stSlider > div > div > div > div { background-color: #00f2fe; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR KONTROL (Parameter Sains)
# ==========================================
st.sidebar.markdown("## 🔬 Parameter Inkubator")
st.sidebar.caption("Atur variabel untuk melihat perubahan dinamika sel/partikel secara real-time.")

jumlah_sel = st.sidebar.slider("Kepadatan Populasi Sel", 50, 300, 150, 10)
jarak_ikatan = st.sidebar.slider("Jarak Ikatan Saraf (Radius)", 50, 200, 120, 10)
kecepatan = st.sidebar.slider("Aktivitas Kinetik", 1, 10, 3, 1)

warna_tema = st.sidebar.selectbox("Gugus Warna Estetik", [
    "Cyan-Blue (Bioluminescence)", 
    "Purple-Pink (Neural Synapse)", 
    "Green-Yellow (Toxic Isotope)"
])

# Logika penerjemahan warna ke kode HEX untuk JavaScript
if warna_tema == "Cyan-Blue (Bioluminescence)":
    particle_color = "#00f2fe"
    line_color = "rgba(0, 242, 254,"
elif warna_tema == "Purple-Pink (Neural Synapse)":
    particle_color = "#d53369"
    line_color = "rgba(213, 51, 105,"
else:
    particle_color = "#a8ff78"
    line_color = "rgba(168, 255, 120,"

# ==========================================
# 3. TAMPILAN DASHBOARD
# ==========================================
st.title("🧬 Neural Web & Population Dynamics")
st.markdown("Sebuah simulasi *Artificial Life* menggunakan jaringan interaksi partikel. Setiap titik merepresentasikan entitas sel yang bergerak secara kinetik dan akan membentuk ikatan kimia/saraf secara otomatis jika berada dalam jarak radius tertentu.")

st.write("---")

# ==========================================
# 4. ENGINE ANIMASI (HTML5 CANVAS + JS)
# ==========================================
# Kodenya panjang dan kompleks di sisi algoritma komputasi visualnya (Bikin temenmu takjub!)
html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ margin: 0; padding: 0; background-color: #05050A; overflow: hidden; display: flex; justify-content: center; align-items: center; border-radius: 15px; box-shadow: 0 0 30px rgba(0,0,0,0.8) inset; }}
        canvas {{ display: block; border-radius: 15px; }}
    </style>
</head>
<body>

<canvas id="neuralCanvas"></canvas>

<script>
    const canvas = document.getElementById('neuralCanvas');
    const ctx = canvas.getContext('2d');
    
    // Setting ukuran canvas
    canvas.width = window.innerWidth - 40;
    canvas.height = 450;

    // Parameter dari Streamlit
    const numParticles = {jumlah_sel};
    const connectionRadius = {jarak_ikatan};
    const speedMultiplier = {kecepatan} * 0.5;
    const pColor = "{particle_color}";
    const lColorBase = "{line_color}";

    // Array penyimpan partikel
    let particlesArray = [];

    // Class cetak biru Partikel (Sel)
    class Particle {{
        constructor() {{
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2.5 + 1;
            this.weight = Math.random() * 1.5 + 0.5;
            this.directionX = (Math.random() * 2 - 1) * speedMultiplier;
            this.directionY = (Math.random() * 2 - 1) * speedMultiplier;
        }}
        
        // Algoritma pergerakan partikel (Hukum Pemantulan Kinetik)
        update() {{
            if (this.x > canvas.width || this.x < 0) {{
                this.directionX = -this.directionX;
            }}
            if (this.y > canvas.height || this.y < 0) {{
                this.directionY = -this.directionY;
            }}
            
            this.x += this.directionX;
            this.y += this.directionY;
            this.draw();
        }}
        
        // Render bentuk sel
        draw() {{
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = pColor;
            ctx.fill();
            ctx.shadowBlur = 10;
            ctx.shadowColor = pColor;
        }}
    }}

    // Inisialisasi awal ekosistem
    function init() {{
        particlesArray = [];
        for (let i = 0; i < numParticles; i++) {{
            particlesArray.push(new Particle());
        }}
    }}

    // Algoritma O(n^2) untuk mendeteksi jarak ikatan antar semua sel
    function connect() {{
        let opacityValue = 1;
        for (let a = 0; a < particlesArray.length; a++) {{
            for (let b = a; b < particlesArray.length; b++) {{
                let distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x)) + 
                               ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
                
                // Jika jarak memenuhi syarat, buat garis ikatan (Sinapsis)
                if (distance < (connectionRadius * connectionRadius)) {{
                    opacityValue = 1 - (distance / (connectionRadius * connectionRadius));
                    ctx.strokeStyle = lColorBase + opacityValue + ')';
                    ctx.lineWidth = 1.5;
                    ctx.beginPath();
                    ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                    ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                    ctx.stroke();
                }}
            }}
        }}
    }}

    // Loop Animasi (60 Frame per Second)
    function animate() {{
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        for (let i = 0; i < particlesArray.length; i++) {{
            particlesArray[i].update();
        }}
        connect();
    }}

    // Jalankan program
    init();
    animate();

    // Responsif jika ukuran browser diubah
    window.addEventListener('resize', function() {{
        canvas.width = window.innerWidth - 40;
        init();
    }});
</script>

</body>
</html>
"""

# Menyematkan Canvas Animasi ke dalam Streamlit
components.html(html_code, height=470)

st.write("---")
col1, col2 = st.columns(2)
with col1:
    st.info("💡 **Konsep Biologi & Informatika:** Animasi di atas menggunakan komputasi matriks jarak *O(n²)*. Setiap kali sel saling mendekat, algoritma akan menciptakan sinapsis (garis ikatan) buatan secara instan.")
with col2:
    st.success("👨‍💻 **Teknologi:** Merender ribuan iterasi kinetik per detik dengan *HTML5 Canvas API* yang sangat ringan tanpa membebani server.")
