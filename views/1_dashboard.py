import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from views.data_engine import load_cloud_data, process_advanced_analytics

st.title("Dashboard Utama: Kondisi Makro Ketenagakerjaan")
st.markdown("Memantau tingkat tekanan pasar kerja tingkat nasional dan mengevaluasi kerentanan wilayah secara spesifik.")
st.divider()

# ========================================================
# 1. PERSIAPAN & PEMROSESAN DATA
# ========================================================
with st.spinner("Memproses korpus data dan mengekstraksi indeks..."):
    raw_df = load_cloud_data()
    master_df = process_advanced_analytics(raw_df)

tahun_terkini = int(master_df['Tahun'].max())

# Solusi aman: Gunakan copy() dan isi nilai NaN dengan 0 agar grafik/peta tidak crash
df_tahun_ini = master_df[master_df['Tahun'] == tahun_terkini].copy()
df_tahun_ini['TPT'] = df_tahun_ini['TPT'].fillna(0)
df_tahun_ini['LSI'] = df_tahun_ini['LSI'].fillna(0)

# ========================================================
# 2. LANDASAN TEORI UMUM
# ========================================================
with st.expander("📖 Landasan Teori: Misery Index & Objektivitas PCA"):
    st.markdown("""
    **Teori Indeks Kesengsaraan (Misery Index):** Dikonseptualisasikan oleh Arthur Okun pada era 1970-an, teori ini mengasumsikan bahwa tingginya tingkat pengangguran dan inflasi secara bersamaan akan menciptakan beban sosial-ekonomi yang masif. Proyek ini memodifikasi indeks tersebut menjadi *Labor Stress Index* (LSI).

    **Pembobotan Matematis (Principal Component Analysis):** Alih-alih menggunakan bobot persentase subjektif yang rentan terhadap bias peneliti, sistem ini menerapkan algoritma PCA (Jolliffe, 2002). PCA mereduksi dimensi data dan mengekstrak matriks variansi terbesar dari indikator makro, menghasilkan skor yang digerakkan oleh bukti historis (*Data-Driven*).
    """)

tab_nasional, tab_provinsi = st.tabs(["📈 Analisis Agregat Nasional", "🔍 Deep-Dive Regional (Threshold)"])

# ========================================================
# 3. TAB 1: ANALISIS AGREGAT NASIONAL + GEO-SPATIAL MAP
# ========================================================
with tab_nasional:
    st.subheader(f"Peta Sebaran Tekanan Labor Nasional Tahun {tahun_terkini}")
    
    # 3A. GEOSPATIAL CHOROPLETH MAP (PETA 38 PROVINSI ASLI)
    import json
    
    # 1. Memuat file GeoJSON 38 Provinsi
    try:
        # Pastikan nama filenya sesuai dengan yang Anda simpan
        with open('geo/indonesia_38.geojson', 'r', encoding='utf-8') as f:
            geojson_indo = json.load(f)
    except FileNotFoundError:
        st.error("File GeoJSON 38 Provinsi tidak ditemukan. Pastikan path file benar.")
        geojson_indo = None

    if geojson_indo:
        # 2. Render Peta Koroplet secara presisi
        fig_map = px.choropleth_mapbox(
            df_tahun_ini,
            geojson=geojson_indo,
            locations='Provinsi', # Ini adalah nama kolom di DataFrame Python kita
            featureidkey='properties.PROVINSI', # PERBAIKAN: Menggunakan KUNCI KAPITAL sesuai JSON Anda
            color='LSI',
            color_continuous_scale='Reds',
            range_color=[0, 100],
            mapbox_style="carto-darkmatter", # Tema gelap elegan
            zoom=3.8,
            center={"lat": -2.0, "lon": 118.0},
            opacity=0.7,
            labels={'LSI': 'Skor LSI', 'Provinsi': 'Wilayah'},
            hover_data={'Pertumbuhan_PDRB': ':.2f}%', 'TPT': ':.2f}%'}
        )
        
        fig_map.update_layout(
            height=500,
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0")
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
    st.divider()

    # 3B. KOMPONEN ANALISIS SPASIAL OTOMATIS
    st.subheader("Analisis Klaster Spasial Regional (Spillover Clustering)")
    st.markdown("Mengevaluasi pemusatan risiko ketenagakerjaan berdasarkan rata-rata wilayah kepulauan geografis.")
    
    df_spasial = df_tahun_ini.groupby('Pulau').agg({
        'LSI': 'mean',
        'TPT': 'mean',
        'Provinsi': 'count'
    }).reset_index().sort_values(by='LSI', ascending=False)
    
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        fig_spatial_bar = px.bar(
            df_spasial, x='LSI', y='Pulau', orientation='h',
            color='LSI', color_continuous_scale='Blues',
            labels={'LSI': 'Rata-rata Skor LSI', 'Pulau': 'Klaster Pulau'}
        )
        fig_spatial_bar.update_layout(
            coloraxis_showscale=False, height=280,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig_spatial_bar, use_container_width=True)
        
    with col_s2:
        st.markdown("**Metrik Ringkasan Pulau**")
        st.dataframe(
            df_spasial.style.format({'LSI': '{:.2f}', 'TPT': '{:.2f}%'}),
            hide_index=True, use_container_width=True
        )
        
    # Narasi Spasial Otomatis
    pulau_tertinggi = df_spasial.iloc[0]['Pulau']
    lsi_tertinggi = df_spasial.iloc[0]['LSI']
    st.info(f"""
    **Catatan Analisis Geografis:** Berdasarkan pemetaan spasial periode data tahun {tahun_terkini}, konsentrasi tekanan pasar kerja 
    tertinggi terdeteksi berada di **Klaster Kepulauan {pulau_tertinggi}** dengan rata-rata skor LSI sebesar **{lsi_tertinggi:.2f}**. 
    Kondisi ini merekomendasikan koordinasi lintas wilayah provinsi dalam satu regional untuk mengantisipasi efek rembetan pengangguran friksional.
    """)
    
    st.divider()
    
    # 3C. PERINGKAT LIGA UTAMA EKONOMI MATANG
    st.subheader("Evaluasi Peringkat Kerentanan Wilayah")
    df_matang = df_tahun_ini[df_tahun_ini['Maturitas_Wilayah'] == "Ekonomi Matang"]
    df_berkembang = df_tahun_ini[df_tahun_ini['Maturitas_Wilayah'] == "Ekonomi Berkembang/Baru"]
    
    col_kiri, col_kanan = st.columns([2, 1])
    with col_kiri:
        st.markdown("**Liga Utama: Top 5 Kerentanan Wilayah Ekonomi Matang**")
        df_top5_matang = df_matang.sort_values(by='LSI', ascending=False).head(5)
        
        fig_bar = px.bar(
            df_top5_matang, x='LSI', y='Provinsi', orientation='h',
            labels={'LSI': 'Skor Indeks (PCA)', 'Provinsi': 'Wilayah'},
            color='LSI', color_continuous_scale='Reds'
        )
        fig_bar.update_layout(
            yaxis={'categoryorder': 'total ascending'}, 
            coloraxis_showscale=False, height=280,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
        )
        
    with col_kanan:
        st.markdown("**Detail Indikator**")
        st.dataframe(
            df_top5_matang[['Provinsi', 'LSI', 'TPT']].style.format({'LSI': '{:.2f}', 'TPT': '{:.2f}%'}),
            hide_index=True, use_container_width=True
        )
        
    st.divider()
    
    st.markdown("**Grup Pantauan Khusus: Kerentanan Wilayah Pemekaran / Otonomi Baru**")
    if df_berkembang.empty:
        st.info("Tidak ada wilayah otonomi baru yang terdeteksi pada periode tahun ini.")
    else:
        st.dataframe(
            df_berkembang[['Provinsi', 'LSI', 'TPT', 'Inflasi_Nasional']].sort_values(by='LSI', ascending=False).style.format({
                'LSI': '{:.2f}', 'TPT': '{:.2f}%', 'Inflasi_Nasional': '{:.2f}%'
            }),
            hide_index=True, use_container_width=True
        )

# ========================================================
# 4. TAB 2: DEEP-DIVE REGIONAL & PENYESUAIAN TIPOLOGI SPASIAL
# ========================================================
with tab_provinsi:
    
   # 4A. LANDASAN TEORI HETEROGENITAS REGIONAL
    with st.expander("📖 Landasan Teori: Heterogenitas Spasial & Resiliensi Regional (2024-2025)"):
        # PERBAIKAN: Menggunakan r""" (tanpa 'f') agar Python tidak membaca {ij} di dalam LaTeX sebagai variabel
        st.markdown(r"""
        **Asimetri Resiliensi Pasar Kerja (Martin et al., 2024):** Literatur ekonomi regional pasca-pandemi membuktikan bahwa tidak ada standar tunggal untuk kerentanan makro. Elastisitas tenaga kerja sangat bergantung pada basis ekonomi wilayah (*Core-Periphery Asymmetries*). Wilayah aglomerasi manufaktur merespons guncangan secara berbeda dibandingkan wilayah pengekspor komoditas.

        **Model Autoregresi Spasial / Spatial Autoregressive Model (Anselin & Rey, 2023):**
        Risiko pengangguran di suatu provinsi ($i$) tidak berdiri sendiri, melainkan dipengaruhi oleh efek rambatan (*Spillover Effect*) dari provinsi tetangganya ($j$). Hal ini dirumuskan dalam model SAR:
        """)
        st.latex(r"LSI_{i,t} = \rho \sum_{j \neq i} W_{ij} LSI_{j,t} + X_{i,t}\beta + \epsilon_i")
        st.markdown(r"""
        Di mana $\rho$ adalah parameter lag spasial yang mengukur kekuatan penularan krisis antar-wilayah, $W_{ij}$ adalah matriks pembobot spasial (jarak geografis/ekonomi), dan $X_{i,t}$ adalah variabel makro internal daerah tersebut.
        
        **Klasifikasi Penyesuaian Tipologi (ADB Regional Report, 2025):**
        * **Pusat Aglomerasi (Jawa & Sumatera):** Sensitivitas tinggi terhadap disrupsi rantai pasok global dan kebijakan suku bunga.
        * **Pusat Komoditas (Kalimantan, Sulawesi, Maluku-Papua):** Sensitivitas tinggi terhadap fluktuasi harga komoditas global (*Commodity Supercycle*). Permintaan tenaga kerja cenderung inelastis.
        * **Pusat Jasa & Pariwisata (Bali-Nusra):** Volatilitas ekstrem terhadap guncangan eksternal (mobilitas manusia), namun memiliki pemulihan (*rebound*) paling cepat.
        """)

    list_matang = sorted(master_df[master_df['Maturitas_Wilayah'] == "Ekonomi Matang"]['Provinsi'].unique())
    list_berkembang = sorted(master_df[master_df['Maturitas_Wilayah'] == "Ekonomi Berkembang/Baru"]['Provinsi'].unique())
    
    col_filter1, col_filter2 = st.columns([2, 1])
    with col_filter1:
        pilihan_wilayah = st.selectbox(
            "Pilih Wilayah Provinsi untuk Evaluasi Sinyal Dini:",
            options=list_matang + list_berkembang
        )
    
    df_wil = master_df[master_df['Provinsi'] == pilihan_wilayah].sort_values('Tahun')
    data_terakhir = df_wil.iloc[-1]
    pulau_wilayah = data_terakhir['Pulau']
    
    # 4B. VISUALISASI TREN HISTORIS
    fig_line = go.Figure()
    # Menambahkan Background Area Indikator Warna
    fig_line.add_shape(type="rect", x0=df_wil['Tahun'].min(), y0=70, x1=df_wil['Tahun'].max(), y1=100, fillcolor="rgba(231, 76, 60, 0.2)", line_width=0)
    fig_line.add_shape(type="rect", x0=df_wil['Tahun'].min(), y0=40, x1=df_wil['Tahun'].max(), y1=70, fillcolor="rgba(241, 196, 15, 0.2)", line_width=0)
    fig_line.add_shape(type="rect", x0=df_wil['Tahun'].min(), y0=0, x1=df_wil['Tahun'].max(), y1=40, fillcolor="rgba(46, 204, 113, 0.2)", line_width=0)
    
    # Menghapus setting color hitam agar auto-adapt ke Dark Mode
    fig_line.add_trace(go.Scatter(x=df_wil['Tahun'], y=df_wil['LSI'], mode='lines+markers', line=dict(width=3), name="Skor LSI"))
    fig_line.update_layout(
        title=f"Tren Historis Labor Stress Index: {pilihan_wilayah} ({df_wil['Maturitas_Wilayah'].iloc[-1]})",
        yaxis=dict(range=[0, 100], showgrid=True, gridcolor="rgba(255,255,255,0.05)"), 
        xaxis=dict(tickmode='linear', dtick=1, showgrid=False),
        margin=dict(t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0")
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    # 4C. PENYESUAIAN NARASI SPASIAL BERDASARKAN PULAU
    st.markdown("### Narasi Diagnostik dan Evaluasi Kebijakan Daerah (Adjusted Spatial Typology)")
    skor_lsi = data_terakhir['LSI']
    
    # Logika Penyesuaian Karakteristik Regional
    if pulau_wilayah in ['Jawa', 'Sumatera']:
        karakteristik = "Pusat Aglomerasi Manufaktur & Jasa"
        risiko_spasial = "Rentan terhadap guncangan rantai pasok global dan efek rambatan (spillover) ketenagakerjaan dari provinsi tetangga yang tinggi akibat integrasi infrastruktur ekonomi."
        fokus_kebijakan = "Stimulus likuiditas untuk industri padat karya dan optimalisasi jejaring bursa kerja antar-daerah."
    elif pulau_wilayah in ['Kalimantan', 'Sulawesi', 'Maluku-Papua']:
        karakteristik = "Pusat Ekonomi Ekstraktif & Komoditas"
        risiko_spasial = "Rentan terhadap volatilitas harga komoditas global. Ketidaksesuaian kompetensi (mismatch) antara sektor ekstraktif padat modal dengan angkatan kerja lokal mendominasi struktur pengangguran."
        fokus_kebijakan = "Hilirisasi padat karya turunan komoditas dan program reskilling transisi energi hijau."
    elif pulau_wilayah == 'Bali-Nusra':
        karakteristik = "Pusat Pariwisata & Jasa Layanan Eksternal"
        risiko_spasial = "Memiliki elastisitas ekstrem terhadap mobilitas manusia dan daya beli makro. Guncangan inflasi langsung menekan marjin sektor perhotelan dan pariwisata."
        fokus_kebijakan = "Diversifikasi pendorong ekonomi lokal dan jaring pengaman sosial adaptif bagi pekerja sektor informal/harian."
    else:
        karakteristik = "Struktur Ekonomi Transisional"
        risiko_spasial = "Dinamika pasar kerja dipengaruhi oleh kombinasi volatilitas sektoral lokal."
        fokus_kebijakan = "Peningkatan kapasitas fiskal daerah untuk investasi infrastruktur padat karya."

    # Penentuan Status LSI Dasar
    if skor_lsi >= 70:
        status, warna_box = "Kritis (Zona Merah)", "error"
        saran_status = f"Diperlukan intervensi darurat (Emergency Action). Prioritas utama pada: {fokus_kebijakan}"
    elif skor_lsi >= 40:
        status, warna_box = "Waspada (Zona Kuning)", "warning"
        saran_status = f"Fase ekuilibrium rentan. Pengawasan parameter makro ketat dengan mitigasi struktural: {fokus_kebijakan}"
    else:
        status, warna_box = "Aman (Zona Hijau)", "success"
        saran_status = f"Struktur pasar kerja dinilai tangguh. Kebijakan diarahkan pada pemeliharaan iklim investasi dan keberlanjutan: {karakteristik.lower()}."

    # Render Narasi Gabungan (LSI + Spasial) menggunakan rf"""
    teks_interpretasi = rf"""
    Berdasarkan pemodelan PCA yang telah **disesuaikan dengan tipologi spasial wilayah**, Provinsi **{pilihan_wilayah}** diklasifikasikan sebagai **{karakteristik}**. 
    
    Saat ini wilayah berada pada status **{status}** dengan skor indeks kerentanan sebesar **{skor_lsi:.2f}**. 
    Keseimbangan pasar tenaga kerja dipengaruhi oleh tingkat pengangguran terbuka daerah sebesar **{data_terakhir['TPT']:.2f}%** dengan pertumbuhan ekonomi regional sebesar **{data_terakhir['Pertumbuhan_PDRB']:.2f}%**.
    
    * **Karakteristik Kerentanan Spasial:** {risiko_spasial}
    * **Rekomendasi Respons Sistem:** {saran_status}
    """
    
    if warna_box == "error": st.error(teks_interpretasi)
    elif warna_box == "warning": st.warning(teks_interpretasi)
    else: st.success(teks_interpretasi)