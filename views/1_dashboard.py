import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from views.data_engine import load_cloud_data, process_advanced_analytics

st.title("Dashboard Utama: Kondisi Makro Ketenagakerjaan")
st.markdown("Memantau tingkat tekanan pasar kerja tingkat nasional dan mengevaluasi kerentanan wilayah secara spesifik.")
st.divider()

with st.spinner("Memproses korpus data dan mengekstraksi indeks..."):
    raw_df = load_cloud_data()
    master_df = process_advanced_analytics(raw_df)

tahun_terkini = int(master_df['Tahun'].max())

df_tahun_ini = master_df[master_df['Tahun'] == tahun_terkini].copy()
df_tahun_ini['TPT'] = df_tahun_ini['TPT'].fillna(0)
df_tahun_ini['LSI'] = df_tahun_ini['LSI'].fillna(0)

with st.expander("📖 Landasan Teori: Misery Index & Objektivitas PCA"):
    st.markdown("""
    **Teori Indeks Kesengsaraan (Misery Index):** Dikonseptualisasikan oleh Arthur Okun pada era 1970-an, teori ini mengasumsikan bahwa tingginya tingkat pengangguran dan inflasi secara bersamaan akan menciptakan beban sosial-ekonomi yang masif. Proyek ini memodifikasi indeks tersebut menjadi *Labor Stress Index* (LSI).

    **Pembobotan Matematis (Principal Component Analysis):** Alih-alih menggunakan bobot persentase subjektif yang rentan terhadap bias peneliti, sistem ini menerapkan algoritma PCA (Jolliffe, 2002). PCA mereduksi dimensi data dan mengekstrak matriks variansi terbesar dari indikator makro, menghasilkan skor yang digerakkan oleh bukti historis (*Data-Driven*).
    """)

tab_nasional, tab_provinsi = st.tabs(["📈 Analisis Agregat Nasional", "🔍 Deep-Dive Regional (Threshold)"])

# --------------------------------------------------------
# TAB 1: ANALISIS AGREGAT NASIONAL + GEO-SPATIAL MAP
# --------------------------------------------------------
with tab_nasional:
    st.subheader(f"Peta Sebaran Tekanan Labor Nasional Tahun {tahun_terkini}")
    
    # 1. GEOSPATIAL BUBBLE MAP
    # Ukuran lingkaran = TPT (Tingkat Pengangguran), Warna = LSI (Labor Stress Index)
    fig_map = px.scatter_geo(
        df_tahun_ini,
        lat='Latitude',
        lon='Longitude',
        color='LSI',
        size='TPT',
        hover_name='Provinsi',
        hover_data={'Pertumbuhan_PDRB': ':.2f}%', 'TPT': ':.2f}%', 'LSI': ':.2f'},
        color_continuous_scale='Reds',
        range_color=[0, 100],
        labels={'LSI': 'Skor LSI', 'TPT': 'Tingkat Pengangguran'},
    )
    
    # Mengunci fokus visual khusus ke area Kepulauan Indonesia
    fig_map.update_geos(
        scope='asia',
        lonaxis_range=[95, 141], # Batas barat-timur Indonesia
        lataxis_range=[-11, 6],   # Batas selatan-utara Indonesia
        showland=True, landcolor="var(--default-background-color)",
        showocean=True, oceancolor="rgba(135, 206, 250, 0.2)"
    )
    fig_map.update_layout(height=450, margin={"r":0,"t":30,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.divider()

    # 2. KOMPONEN ANALISIS SPASIAL OTOMATIS
    st.subheader("Analisis Klaster Spasial Regional (Spillover Clustering)")
    st.markdown("Mengevaluasi pemusatan risiko ketenagakerjaan berdasarkan rata-rata wilayah kepulauan geografis.")
    
    # Menghitung rata-rata LSI per pulau besar
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
        fig_spatial_bar.update_layout(coloraxis_showscale=False, height=280)
        st.plotly_chart(fig_spatial_bar, use_container_width=True)
        
    with col_s2:
        st.markdown("**Metrik Ringkasan Pulau**")
        st.dataframe(
            df_spasial.style.format({'LSI': '{:.2f}', 'TPT': '{:.2f}%'}),
            hide_index=True, use_container_width=True
        )
        
    # Narasi Spasial Otomatis (Objektif)
    pulau_tertinggi = df_spasial.iloc[0]['Pulau']
    lsi_tertinggi = df_spasial.iloc[0]['LSI']
    st.info(f"""
    **Catatan Analisis Geografis:** Berdasarkan pemetaan spasial periode data tahun {tahun_terkini}, konsentrasi tekanan pasar kerja 
    tertinggi terdeteksi berada di **Klaster Kepulauan {pulau_tertinggi}** dengan rata-rata skor LSI sebesar **{lsi_tertinggi:.2f}**. 
    Kondisi ini merekomendasikan koordinasi lintas wilayah provinsi dalam satu regional untuk mengantisipasi efek rembetan pengangguran friksional.
    """)
    
    st.divider()
    
    # 3. PERINGKAT LIGA UTAMA EKONOMI MATANG
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
        fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False, height=280)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_kanan:
        st.markdown("**Detail Indikator Liga Utama**")
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

# --------------------------------------------------------
# TAB 2: DEEP-DIVE REGIONAL & INTERPRETASI
# --------------------------------------------------------
with tab_provinsi:
    list_matang = sorted(master_df[master_df['Maturitas_Wilayah'] == "Ekonomi Matang"]['Provinsi'].unique())
    list_berkembang = sorted(master_df[master_df['Maturitas_Wilayah'] == "Ekonomi Berkembang/Baru"]['Provinsi'].unique())
    
    pilihan_wilayah = st.selectbox(
        "Pilih Wilayah Provinsi untuk Evaluasi Sinyal Dini:",
        options=list_matang + list_berkembang
    )
    
    df_wil = master_df[master_df['Provinsi'] == pilihan_wilayah].sort_values('Tahun')
    
    fig_line = go.Figure()
    fig_line.add_shape(type="rect", x0=df_wil['Tahun'].min(), y0=70, x1=df_wil['Tahun'].max(), y1=100, fillcolor="rgba(231, 76, 60, 0.2)", line_width=0)
    fig_line.add_shape(type="rect", x0=df_wil['Tahun'].min(), y0=40, x1=df_wil['Tahun'].max(), y1=70, fillcolor="rgba(241, 196, 15, 0.2)", line_width=0)
    fig_line.add_shape(type="rect", x0=df_wil['Tahun'].min(), y0=0, x1=df_wil['Tahun'].max(), y1=40, fillcolor="rgba(46, 204, 113, 0.2)", line_width=0)
    
    fig_line.add_trace(go.Scatter(x=df_wil['Tahun'], y=df_wil['LSI'], mode='lines+markers', line=dict(width=3)))
    fig_line.update_layout(
        title=f"Tren Historis Labor Stress Index: {pilihan_wilayah} ({df_wil['Maturitas_Wilayah'].iloc[-1]})",
        yaxis=dict(range=[0, 100]), 
        xaxis=dict(tickmode='linear', dtick=1)
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("### Narasi Diagnostik dan Evaluasi Kebijakan Daerah")
    data_terakhir = df_wil.iloc[-1]
    skor_lsi = data_terakhir['LSI']
    
    if skor_lsi >= 70:
        status, warna_box, saran = "Kritis (Zona Merah)", "error", "Diperlukan intervensi kebijakan darurat berupa stimulus penciptaan lapangan kerja padat karya dan evaluasi penyesuaian UMP."
    elif skor_lsi >= 40:
        status, warna_box, saran = "Waspada (Zona Kuning)", "warning", "Diperlukan pengawasan parameter makro secara ketat serta penyiapan program jaring pengaman sosial."
    else:
        status, warna_box, saran = "Aman (Zona Hijau)", "success", "Struktur pasar kerja dinilai tangguh. Kebijakan diarahkan pada pemeliharaan iklim investasi."

    teks_interpretasi = f"""
    Berdasarkan pemodelan objektif PCA pada periode data terakhir, Provinsi **{pilihan_wilayah}** berada pada **{status}** dengan skor indeks sebesar **{skor_lsi:.2f}**. 
    Keseimbangan pasar tenaga kerja dipengaruhi oleh tingkat pengangguran terbuka (TPT) daerah sebesar **{data_terakhir['TPT']:.2f}%**, didukung pertumbuhan ekonomi regional sebesar **{data_terakhir['Pertumbuhan_PDRB']:.2f}%**.
    
    **Rekomendasi Respons Sistem:** {saran}
    """
    
    if warna_box == "error": st.error(teks_interpretasi)
    elif warna_box == "warning": st.warning(teks_interpretasi)
    else: st.success(teks_interpretasi)