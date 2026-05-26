import streamlit as st

# ========================================================
# 1. KONFIGURASI HALAMAN UTAMA
# ========================================================
st.set_page_config(
    page_title="Macro Labor Stress EWS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================================
# 2. INJEKSI CSS (COMMAND CENTER & BACKGROUND IMAGE)
# ========================================================
st.markdown("""
    <style>
        /* 1. Menyembunyikan elemen bawaan yang mengganggu */
        [data-testid="collapsedControl"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }
        
        /* 2. Memasang Gambar Latar Belakang (Cyber/Tech Map) di seluruh aplikasi */
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        
        /* 3. Membuat efek kaca gelap (Dark Glassmorphism) pada kontainer utama */
        .block-container { 
            padding-top: 4.5rem !important; 
            background-color: rgba(10, 14, 23, 0.85); /* Hitam transparan agar teks tetap terbaca */
            border-radius: 15px;
            box-shadow: 0 8px 32px 0 rgba(0, 210, 255, 0.15); /* Bayangan Cyan Neon */
            backdrop-filter: blur(8px); /* Efek blur pada gambar latar */
            margin-top: 2rem;
            margin-bottom: 2rem;
            padding-bottom: 4rem;
        }
        
        /* 4. Modifikasi Tombol Navigasi Atas (Neon Hover Effect) */
        a { text-decoration: none !important; }
        [data-testid="stPageLink-NavLink"] {
            background-color: rgba(21, 27, 38, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease-in-out;
        }
        [data-testid="stPageLink-NavLink"]:hover {
            background-color: rgba(0, 210, 255, 0.15) !important;
            border: 1px solid #00d2ff;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.4); /* Neon Glow */
            transform: translateY(-2px);
        }
        
        /* 5. Mengubah warna garis pembatas (divider) menjadi Cyan redup */
        hr {
            border-color: rgba(0, 210, 255, 0.2) !important;
        }
    </style>
""", unsafe_allow_html=True)

# ========================================================
# 3. PENDAFTARAN HALAMAN (HARUS DILAKUKAN LEBIH DULU)
# ========================================================
halaman_dashboard = st.Page("views/1_dashboard.py", title="Dashboard Utama")
halaman_simulasi = st.Page("views/2_simulasi.py", title="Simulasi Kebijakan")
halaman_metodologi = st.Page("views/3_metodologi.py", title="Metodologi & Laporan")

# Mendaftarkan navigasi secara tersembunyi
pg = st.navigation([halaman_dashboard, halaman_simulasi, halaman_metodologi], position="hidden")

# ========================================================
# 4. MEMBANGUN MENU NAVIGASI HORIZONTAL (TOP BAR)
# ========================================================
col1, col2, col3, col_kosong = st.columns([1.5, 1.8, 1.8, 5])

# Sekarang st.page_link memanggil variabel halaman yang sudah didaftarkan di Langkah 3
with col1:
    st.page_link(halaman_dashboard, label="Dashboard Utama", icon="📊")
with col2:
    st.page_link(halaman_simulasi, label="Simulasi Kebijakan", icon="🔬")
with col3:
    st.page_link(halaman_metodologi, label="Metodologi & Laporan", icon="📚")

st.divider()

# ========================================================
# 5. EKSEKUSI KONTEN HALAMAN
# ========================================================
pg.run()