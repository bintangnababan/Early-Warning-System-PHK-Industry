import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from views.data_engine import load_cloud_data, process_advanced_analytics

st.title("Simulasi Kebijakan EWS & Machine Learning")
st.markdown("Menguji ketahanan pasar tenaga kerja menggunakan model Regresi Ekonometrika Data Panel dan Klastering Spasial.")
st.divider()

# Memuat Data dari Engine Utama
with st.spinner("Memuat model Machine Learning..."):
    raw_df = load_cloud_data()
    master_df = process_advanced_analytics(raw_df)

tahun_terkini = int(master_df['Tahun'].max())

tab_klaster, tab_regresi = st.tabs(["🧩 Klastering Tipologi Wilayah", "⚙️ Simulasi Kausalitas Kebijakan"])

# --------------------------------------------------------
# TAB 1: K-MEANS CLUSTERING (UNSUPERVISED LEARNING)
# --------------------------------------------------------
with tab_klaster:
    st.subheader(f"Peta Tipologi Ekonomi Regional Tahun {tahun_terkini}")
    with st.expander("📖 Landasan Teori: Pengelompokan Regional (Spatial Clustering)"):
        st.markdown("""
        **Unsupervised Machine Learning (K-Means)** Setiap daerah merespons kebijakan nasional secara asimetris. Algoritma *K-Means* digunakan untuk menghindari "Kebijakan Sapu Jagat" (*One-Size-Fits-All Policy*). Mesin secara mandiri mencari pola kedekatan Euclidean (*Euclidean Distance*) dari struktur pertumbuhan, inflasi, dan pengangguran setiap provinsi, lalu mengelompokkannya ke dalam tiga tipologi maturitas (MacQueen, 1967).
        """)
    st.markdown("Algoritma *K-Means* mengelompokkan wilayah berdasarkan kemiripan struktur makroekonominya (Pertumbuhan PDRB, TPT, dan Rasio Upah).")
    
    # Menyiapkan data tahun terakhir
    df_cluster = master_df[master_df['Tahun'] == tahun_terkini].copy()
    
    # Memilih fitur untuk clustering dan membuang NaN
    fitur_cluster = ['Pertumbuhan_PDRB', 'TPT', 'Rasio_UMP_PDRB']
    df_cluster = df_cluster.dropna(subset=fitur_cluster)
    
    if not df_cluster.empty:
        # Standarisasi Data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_cluster[fitur_cluster])
        
        # Menjalankan K-Means (K=3)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df_cluster['Klaster'] = kmeans.fit_predict(X_scaled)
        
        # Memberikan label klaster secara dinamis berdasarkan rata-rata TPT
        rata_tpt_klaster = df_cluster.groupby('Klaster')['TPT'].mean().sort_values()
        
        # Klaster dengan TPT terendah = Tangguh, Tengah = Berkembang, Tertinggi = Rentan
        label_map = {
            rata_tpt_klaster.index[0]: "Klaster 1: Tangguh & Berdaya Serap",
            rata_tpt_klaster.index[1]: "Klaster 2: Transisi & Berkembang",
            rata_tpt_klaster.index[2]: "Klaster 3: Rentan & Tekanan Tinggi"
        }
        df_cluster['Nama_Klaster'] = df_cluster['Klaster'].map(label_map)
        
        # Visualisasi 2D Scatter Plot dengan penanda klaster
        fig_cluster = px.scatter(
            df_cluster, 
            x='Pertumbuhan_PDRB', 
            y='TPT', 
            color='Nama_Klaster',
            hover_name='Provinsi',
            size='LSI',
            labels={'Pertumbuhan_PDRB': 'Pertumbuhan PDRB (%)', 'TPT': 'Tingkat Pengangguran (%)'},
            title="Sebaran Klaster Tipologi Pasar Kerja"
        )
        fig_cluster.update_layout(height=500)
        st.plotly_chart(fig_cluster, use_container_width=True)
        
        st.markdown("**Deskripsi Operasional Klaster:** Wilayah di Klaster 3 memerlukan intervensi prioritas karena memiliki karakteristik kombinasi pertumbuhan ekonomi yang gagal menekan angka pengangguran.")
    else:
        st.warning("Data tidak cukup untuk melakukan clustering pada tahun ini.")

# --------------------------------------------------------
# TAB 2: REGRESI & MESIN WHAT-IF (SUPERVISED LEARNING)
# --------------------------------------------------------
with tab_regresi:
    st.subheader("Mesin Simulasi Guncangan Makroekonomi (What-If Analysis)")
    with st.expander("📖 Mekanisme Transmisi Kausalitas (Ekonometrika)"):
        st.markdown(r"""
        Prediksi perubahan pengangguran pada mesin ini dikalkulasi menggunakan koefisien $\beta$ dari Regresi Data Panel, yang bersandar pada tiga literatur utama:
        
        * **Hukum Okun (Okun, 1962):** $\Delta U = \alpha - \beta(g)$  
            Mengukur seberapa besar pertumbuhan ekonomi ($g$) mampu menyerap tenaga kerja dan menurunkan pengangguran ($\Delta U$).
        * **Kurva Phillips (Phillips, 1958):** $\pi = \pi^e - \beta(U - U^n) + v$  
            Mengukur sensitivitas *trade-off* jangka pendek antara inflasi ($\pi$) dan pengangguran ($U$).
        * **Teori Permintaan Tenaga Kerja Neoklasik (Borjas, 2014):** $L^d = f\left(\frac{W}{P}\right)$  
            Menjelaskan bahwa keputusan industri untuk mempertahankan pekerja ($L^d$) berbanding terbalik dengan beban rasio upah riil terhadap kapasitas (PDRB).
        """)
    st.markdown("Mengukur probabilitas lonjakan pengangguran menggunakan koefisien elastisitas dari Regresi Data Panel historis.")
    
    # 1. Melatih Model Regresi Global (Semua Tahun & Provinsi)
    df_regresi = master_df.dropna(subset=['TPT', 'Pertumbuhan_PDRB', 'Inflasi_Nasional', 'Rasio_UMP_PDRB']).copy()
    
    X = df_regresi[['Pertumbuhan_PDRB', 'Inflasi_Nasional', 'Rasio_UMP_PDRB']]
    y = df_regresi['TPT']
    
    model = LinearRegression()
    model.fit(X, y)
    
    koef_pdrb = model.coef_[0]
    koef_inflasi = model.coef_[1]
    
    # 2. Antarmuka Simulasi
    col_sim1, col_sim2 = st.columns([1, 2])
    
    with col_sim1:
        st.markdown("#### Parameter Kebijakan")
        prov_simulasi = st.selectbox("Pilih Wilayah Target:", sorted(df_regresi['Provinsi'].unique()))
        
        # Ambil data baseline provinsi tersebut dari tahun terakhir
        baseline_prov = df_regresi[(df_regresi['Provinsi'] == prov_simulasi) & (df_regresi['Tahun'] == tahun_terkini)].iloc[0]
        
        tpt_awal = baseline_prov['TPT']
        pdrb_awal = baseline_prov['Pertumbuhan_PDRB']
        inflasi_awal = baseline_prov['Inflasi_Nasional']
        
        st.markdown(f"**Baseline Saat Ini ({tahun_terkini}):**")
        st.markdown(f"- Pertumbuhan Ekonomi: **{pdrb_awal:.2f}%**")
        st.markdown(f"- Tingkat Inflasi: **{inflasi_awal:.2f}%**")
        st.markdown(f"- Pengangguran (TPT): **{tpt_awal:.2f}%**")
        st.divider()
        
        skenario_pdrb = st.slider("Simulasi Target Pertumbuhan Ekonomi (%)", min_value=-5.0, max_value=15.0, value=float(pdrb_awal), step=0.5)
        skenario_inflasi = st.slider("Simulasi Guncangan Inflasi (%)", min_value=0.0, max_value=15.0, value=float(inflasi_awal), step=0.5)
        
    with col_sim2:
        st.markdown("#### Hasil Proyeksi Sistem EWS")
        
        # Kalkulasi Delta (Perubahan)
        delta_pdrb = skenario_pdrb - pdrb_awal
        delta_inflasi = skenario_inflasi - inflasi_awal
        
        # Prediksi Dampak Berdasarkan Koefisien Regresi
        # Rumus: TPT_Baru = TPT_Awal + (Koef_PDRB * Delta_PDRB) + (Koef_Inflasi * Delta_Inflasi)
        dampak_pdrb = delta_pdrb * koef_pdrb
        dampak_inflasi = delta_inflasi * koef_inflasi
        prediksi_tpt = tpt_awal + dampak_pdrb + dampak_inflasi
        
        # Menghindari TPT bernilai negatif secara tidak logis
        if prediksi_tpt < 0: prediksi_tpt = 0.0
        
        selisih_tpt = prediksi_tpt - tpt_awal
        
        st.metric(
            label=f"Proyeksi TPT Provinsi {prov_simulasi}", 
            value=f"{prediksi_tpt:.2f}%", 
            delta=f"{selisih_tpt:.2f}% Poin",
            delta_color="inverse" # Merah jika pengangguran naik, Hijau jika turun
        )
        
        st.markdown("**Interpretasi Ekonometrika (Hukum Okun & Kurva Phillips):**")
        if selisih_tpt > 0.5:
            st.error(f"Peringatan: Skenario ini memicu pelemahan pasar tenaga kerja. Penyesuaian kebijakan akan meningkatkan pengangguran terbuka sebesar {selisih_tpt:.2f} poin persentase.")
        elif selisih_tpt < -0.5:
            st.success(f"Skenario Optimal: Kebijakan ini efektif menstimulasi penyerapan tenaga kerja, memangkas angka pengangguran sebesar {abs(selisih_tpt):.2f} poin persentase.")
        else:
            st.info("Skenario Netral: Perubahan kebijakan makro tidak memberikan dampak volatilitas yang signifikan terhadap struktur ketenagakerjaan daerah.")