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
# 2. INJEKSI CSS 
# ========================================================
st.markdown("""
    <style>
        /* Menyembunyikan sidebar bawaan */
        [data-testid="collapsedControl"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }
        
        /* Menghindari tabrakan dengan header atas */
        .block-container { padding-top: 4.5rem !important; }
        
        /* STYLING MENU ADAPTIF (DARK/LIGHT MODE) */
        /* Menghilangkan garis bawah tautan */
        a { text-decoration: none !important; }
        
        /* Membuat kotak pembungkus st.page_link merespons interaksi kursor */
        [data-testid="stPageLink-NavLink"] {
            background-color: transparent;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            transition: background-color 0.3s ease;
        }
        
        /* Saat kursor diarahkan, latar belakang menggunakan warna sekunder dari tema aktif */
        [data-testid="stPageLink-NavLink"]:hover {
            background-color: var(--secondary-background-color) !important;
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