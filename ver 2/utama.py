import streamlit as st
import requests

# Set konfigurasi halaman web
st.set_page_config(page_title="Konverter Mata Uang Dunia", page_icon="🌍", layout="centered")

# Judul Aplikasi
st.title("🌍 Konverter Mata Uang Dunia Real-Time")
st.write("Aplikasi web berbasis Python & Streamlit untuk memantau dan mengonversi kurs global.")
st.markdown("---")

# Fungsi untuk mengambil semua mata uang yang tersedia berdasarkan base currency
@st.cache_data(ttl=3600) # Menyimpan cache selama 1 jam agar web lebih cepat & hemat kuota API
def get_exchange_data(base):
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("result") == "success":
            return data["rates"]
    except Exception:
        return None
    return None

# Ambil data awal (menggunakan USD sebagai dasar pencarian daftar mata uang)
initial_rates = get_exchange_data("USD")

if initial_rates:
    # Mengambil daftar kode mata uang untuk pilihan di dropdown (diurutkan abjad)
    list_mata_uang = sorted(list(initial_rates.keys()))
    
    # Membuat Layout Kolom di Streamlit
    col1, col2 = st.columns(2)
    
    with col1:
        # Dropdown Mata Uang Asal (Default: IDR jika ada, jika tidak USD)
        default_from = list_mata_uang.index("IDR") if "IDR" in list_mata_uang else 0
        from_curr = st.selectbox("Dari Mata Uang:", list_mata_uang, index=default_from)
        
    with col2:
        # Dropdown Mata Uang Tujuan (Default: USD jika ada, jika tidak posisi ke-1)
        default_to = list_mata_uang.index("USD") if "USD" in list_mata_uang else 1
        to_curr = st.selectbox("Ke Mata Uang:", list_mata_uang, index=default_to)

    # Input Jumlah Uang
    amount = st.number_input(f"Masukkan Jumlah Uang ({from_curr}):", min_value=0.0, value=100000.0, step=1000.0)

    # Ambil data kurs real-time berdasarkan mata uang asal yang dipilih user
    rates = get_exchange_data(from_curr)
    
    if rates and to_curr in rates:
        kurs_tujuan = rates[to_curr]
        hasil_konversi = amount * kurs_tujuan
        
        # Tampilkan Hasil Konversi dengan Desain Menarik
        st.markdown("### 🎯 Hasil Konversi:")
        
        # Menggunakan st.metric untuk visualisasi angka yang profesional
        st.metric(
            label=f"{amount:,.2f} {from_curr} sama dengan:",
            value=f"{hasil_konversi:,.2f} {to_curr}"
        )
        
        # Informasi Kurs Tambahan
        st.info(f"💡 **Informasi Kurs:** 1 {from_curr} = {kurs_tujuan:,.4f} {to_curr}")
    else:
        st.error("Gagal mengambil data konversi untuk mata uang tersebut.")
else:
    st.error("Gagal terhubung ke server API. Periksa koneksi internet Anda.")

# Footer
st.markdown("---")
st.caption("Data kurs diperbarui secara real-time setiap jam via Open Exchange Rates API.")
