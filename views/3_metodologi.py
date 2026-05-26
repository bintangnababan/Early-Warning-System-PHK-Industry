import streamlit as st
import pandas as pd
from datetime import datetime
from views.data_engine import load_cloud_data, process_advanced_analytics

st.title("Metodologi, Dokumentasi & Referensi Ilmiah")
st.markdown("Analisis komprehensif landasan teoritis makroekonomi dan instrumen pelaporan kebijakan berbasis bukti data.")
st.divider()

tab_teori, tab_interpretasi = st.tabs(["📖 Landasan Teori Makroekonomi", "📄 Laporan Analisis & Kebijakan"])

# --------------------------------------------------------
# TAB 1: LANDASAN TEORI & PERHITUNGAN MANUAL (STATE-OF-THE-ART)
# --------------------------------------------------------
with tab_teori:
    st.header("Kerangka Teoritis & Pemodelan EWS")
    st.markdown("""
    Sistem peringatan dini (EWS) ini tidak hanya bersandar pada teori klasik, tetapi telah dikalibrasi menggunakan 
    temuan empiris makroekonomi, ekonometrika spasial, dan *Machine Learning* dalam lima tahun terakhir (2021-2026).
    """)
    
    st.markdown("---")
    # ==========================================
    # 1. HUKUM OKUN
    # ==========================================
    st.subheader("1. Hukum Okun & Asimetri Jobless Growth")
    st.latex(r"\Delta U = \alpha - \beta(g)")
    st.markdown(rf"""
    **Dinamika Asimetris (2024-2025):** Formulasi klasik Okun (1962) mengasumsikan korelasi linier antara pertumbuhan ($g$) dan perubahan pengangguran ($\Delta U$). Namun, riset empiris lintas-negara pasca-pandemi (Pitoňáková et al., 2025; Akkoyunlu, 2024) membuktikan bahwa koefisien $\beta$ kini bersifat sangat asimetris. 
    
    **Kondisi Batas Struktural:** Elastisitas penyerapan tenaga kerja terbukti melemah secara drastis selama fase ekspansi/pemulihan dibandingkan dengan fase resesi. Fenomena ini memvalidasi kerentanan *Jobless Growth*, di mana PDRB yang didorong oleh intensifikasi modal di sektor tertentu gagal menurunkan tingkat pengangguran secara agregat.
    """)
    with st.expander("🧮 Bedah Perhitungan Manual: Simulasi Hukum Okun"):
        st.markdown(r"""
        **Skenario:**
        Sebuah provinsi memiliki tingkat pengangguran awal $U_{t-1} = 6.0\%$. Parameter historis menunjukkan pertumbuhan ekonomi minimum untuk menahan pengangguran ($\alpha$) adalah $2.5\%$, dan koefisien serapan tenaga kerja ($\beta$) adalah $0.4$. Tahun ini, provinsi tersebut mencetak pertumbuhan PDRB ($g$) sebesar $4.0\%$.

        **Langkah Perhitungan:**
        1. Menghitung delta pengangguran: 
           $\Delta U = \alpha - \beta(g)$
           $\Delta U = 2.5 - 0.4(4.0)$
           $\Delta U = 2.5 - 1.6 = +0.9\%$
        2. Pengangguran aktual tahun ini:
           $U_t = U_{t-1} + \Delta U$
           $U_t = 6.0\% + 0.9\% = 6.9\%$

        *Kesimpulan Analitik:* Meskipun ekonomi tumbuh positif (4.0%), angkanya tidak cukup tinggi untuk menyerap angkatan kerja baru dan menutupi efisiensi industri, sehingga pengangguran justru **naik** menjadi 6.9%.
        """)
    
    st.markdown("---")
    # ==========================================
    # 2. KURVA PHILLIPS
    # ==========================================
    st.subheader("2. Kurva Phillips Non-Linier & Guncangan Pasokan")
    st.latex(r"\pi = \pi^e - \beta(U - U^n) + v")
    st.markdown(rf"""
    **Transisi ke Model Non-Linier:** Literatur makroekonomi termutakhir (Benigno & Eggertsson, 2023; Mercan et al., 2024) merevisi model Kurva Phillips klasik menjadi sangat non-linier (*steep nonlinear Phillips curve*) akibat gesekan pasar kerja yang baru. 
    
    **Ancaman Stagflasi Sektoral:** Tingkat inflasi ($\pi$) saat ini jauh lebih sensitif terhadap pengetatan pasar dan guncangan rantai pasok eksternal ($v$). Ketika pasar kerja menyempit, daya tawar pekerja memicu kenaikan upah nominal yang langsung ditransmisikan ke harga jual produk. 
    """)
    with st.expander("🧮 Bedah Perhitungan Manual: Simulasi Kurva Phillips"):
        st.markdown(r"""
        **Skenario:**
        Ekspektasi inflasi masyarakat ($\pi^e$) adalah $3.0\%$. Tingkat pengangguran alamiah ($U^n$) adalah $5.0\%$. Pengangguran aktual ($U$) turun menjadi $4.0\%$ (pasar kerja ketat). Sensitivitas upah terhadap inflasi ($\beta$) adalah $0.5$. Tiba-tiba terjadi guncangan harga energi global ($v$) sebesar $2.0\%$.

        **Langkah Perhitungan:**
        1. Hitung dorongan dari pasar kerja (Demand-pull):
           $-\beta(U - U^n) = -0.5(4.0 - 5.0) = -0.5(-1.0) = +0.5\%$
        2. Hitung inflasi total ($\pi$):
           $\pi = \pi^e + \text{Dorongan Pasar} + v$
           $\pi = 3.0\% + 0.5\% + 2.0\%$
           $\pi = 5.5\%$

        *Kesimpulan Analitik:* Inflasi melonjak hingga 5.5%. Guncangan eksternal ($v$) memperburuk inflasi yang sudah mulai memanas akibat pengetatan pasar kerja ($U < U^n$).
        """)
    
    st.markdown("---")
    # ==========================================
    # 3. TEORI NEOKLASIK
    # ==========================================
    st.subheader("3. Teori Neoklasik, Otomatisasi & Substitusi Tenaga Kerja")
    st.latex(r"L^d = f\left(\frac{W}{P}\right)")
    st.markdown(rf"""
    **Beban Upah Riil dan Otomatisasi:** Studi termutakhir oleh National Bureau of Economic Research (Acemoglu et al., 2024) dan evaluasi sektoral IMF (2025) membuktikan bahwa kenaikan Upah Minimum Provinsi (UMP) yang melebihi produktivitas marjinal tidak hanya menyebabkan PHK jangka pendek, tetapi memicu *Efek Substitusi* permanen. 
    
    Industri merespons biaya upah riil ($W/P$) yang tinggi dengan mempercepat investasi pada otomatisasi, yang secara struktural memangkas kapasitas penyerapan tenaga kerja manusia di masa depan.
    """)
    with st.expander("🧮 Bedah Perhitungan Manual: Evaluasi Upah Riil"):
        st.markdown(r"""
        **Skenario Beban Industri:**
        Tahun lalu, UMP Nominal ($W$) adalah Rp3.000.000 dan Indeks Harga Konsumen ($P$) adalah $100$.
        Tahun ini, pemerintah menaikkan UMP menjadi Rp3.300.000 (naik 10%), tetapi inflasi menaikkan IHK ($P$) menjadi $105$ (naik 5%). Kapasitas PDRB stagnan.

        **Langkah Perhitungan:**
        1. Upah Riil Tahun Lalu ($RUpah_{t-1}$):
           $\frac{W}{P} = \frac{3.000.000}{100} = 30.000$ (Satuan Daya Beli)
        2. Upah Riil Tahun Ini ($RUpah_t$):
           $\frac{W}{P} = \frac{3.300.000}{105} = 31.428$ (Satuan Daya Beli)

        *Kesimpulan Analitik:* Meskipun tergerus inflasi, beban upah riil yang harus dibayar perusahaan tetap naik sekitar $4.7\%$. Tanpa adanya kenaikan produktivitas pekerja, marjin keuntungan menurun, memaksa rasionalisasi karyawan ($L^d$ turun).
        """)

    st.markdown("---")
    # ==========================================
    # 4. MACHINE LEARNING (PCA & K-MEANS)
    # ==========================================
    st.subheader("4. Metodologi EWS Berbasis Unsupervised Machine Learning")
    st.markdown(rf"""
    **Evolusi Analitik Data:** Mengadopsi pergeseran paradigma metodologi pemantauan risiko sistemik (Macroeconomic Early Warning Systems, 2025), sistem ini meninggalkan pembobotan linier statis.
    
    **Ekstraksi Risiko (PCA & K-Means):** Algoritma *Principal Component Analysis* (PCA) digunakan untuk mengekstrak variansi krisis secara *data-driven*. Selanjutnya, *Spatial Clustering* (K-Means) diterapkan untuk memetakan kedekatan Euclidean antar-provinsi guna mendeteksi efek rambatan spasial (*Spatial Spillover Effect*).
    """)
    with st.expander("🧮 Bedah Perhitungan Manual: Logika Ekstraksi PCA (LSI)"):
        st.markdown(r"""
        Mesin ini mengubah dua variabel (Pengangguran dan Inflasi) menjadi satu Skor Risiko Utama (Labor Stress Index / LSI).

        **Langkah Algoritma PCA (Simplified):**
        1. **Standarisasi (Z-Score):** Menyamakan satuan persentase menjadi skala seragam.
           $Z = \frac{X - \mu}{\sigma}$
        2. **Matriks Kovarians:** Mengukur seberapa kuat pengangguran dan inflasi bergerak bersamaan di daerah tersebut (mendeteksi gejala Stagflasi).
        3. **Ekstraksi Nilai Eigen (Eigenvalues):** Mencari garis tren (*Principal Component*) yang merepresentasikan pola stres terbesar dari data.
        4. **Skoring Akhir (Min-Max Scaling):** Komponen utama tersebut kemudian diskalakan ke rentang 0 hingga 100.
           $LSI = \frac{PC_{aktual} - PC_{min}}{PC_{max} - PC_{min}} \times 100$

        Hasilnya: Skor $LSI = 85$ tidak lagi berarti "bobot inflasi 50% dan pengangguran 50%", melainkan representasi matematis objektif bahwa wilayah tersebut berada pada puncaknya kurva volatilitas risiko krisis.
        """)

# --------------------------------------------------------
# TAB 2: LAPORAN ANALISIS & KEBIJAKAN (INTEGRASI TEORI)
# --------------------------------------------------------
with tab_interpretasi:
    st.header("Laporan Analisis Kebijakan Makro Regional")
    st.markdown("Evaluasi kondisi ketenagakerjaan daerah dan opsi respons strategis berdasarkan integrasi pemodelan teoritis.")
    
    with st.spinner("Sinkronisasi pangkalan data makro..."):
        raw_df = load_cloud_data()
        master_df = process_advanced_analytics(raw_df)
        
    tahun_terkini = int(master_df['Tahun'].max())
    list_provinsi = sorted(master_df['Provinsi'].unique())
    
    pilihan_prov = st.selectbox("Pilih Wilayah Sasaran Analisis:", list_provinsi)
    df_prov = master_df[(master_df['Provinsi'] == pilihan_prov) & (master_df['Tahun'] == tahun_terkini)]
    
    if not df_prov.empty:
        df_prov = df_prov.iloc[0]
        
        # ====================================================
        # LOGIKA DIAGNOSIS BERDASARKAN TEORI KOMPREHENSIF
        # ====================================================
        
        # 1. Konteks Skor LSI
        if df_prov['LSI'] >= 70:
            status_ews = "Tinggi / Zona Merah"
            narasi_lsi = rf"""
            Kondisi pasar tenaga kerja menunjukkan indikasi tekanan struktural yang signifikan. Akumulasi parameter inflasi dan pengangguran 
            berada pada level kritis, menandakan adanya ketidakseimbangan akut antara kapasitas penyerapan sektor formal dan laju pertumbuhan 
            angkatan kerja baru. Sinyal ini merekomendasikan perlunya evaluasi darurat terhadap instrumen jaring pengaman sosial ekonomi daerah.
            """
        elif df_prov['LSI'] >= 40:
            status_ews = "Menengah / Zona Kuning"
            narasi_lsi = rf"""
            Kondisi pasar tenaga kerja berada dalam fase ekuilibrium yang rentan. Meskipun belum memasuki tahap kritis, terdapat riak volatilitas 
            pada indikator makro yang berpotensi menggerus stabilitas penyerapan tenaga kerja jika tidak disertai mitigasi preventif. Pengawasan 
            berkelanjutan terhadap pergerakan harga kebutuhan pokok dan tingkat friksi pasar kerja sangat disarankan.
            """
        else:
            status_ews = "Rendah / Zona Hijau"
            narasi_lsi = rf"""
            Indikator ketenagakerjaan menunjukkan tingkat resiliensi yang memadai pada periode ini. Struktur pasar kerja dinilai relatif tangguh, 
            di mana kapasitas pertumbuhan ekonomi lokal masih mampu mengompensasi pergerakan laju pengangguran dan inflasi dalam batas toleransi alamiah.
            """

        # 2. Integrasi Hukum Okun
        if df_prov['Pertumbuhan_PDRB'] > 3.0 and df_prov['TPT'] > 5.0:
            status_okun = "Penyimpangan Struktural (Jobless Growth)"
            # PERBAIKAN: Menggunakan awalan rf"" agar $\beta$ tidak dibaca sebagai spasi mundur
            narasi_okun = rf"""
            Meskipun perekonomian daerah mencatatkan pertumbuhan output positif sebesar **{df_prov['Pertumbuhan_PDRB']:.2f}%**, Tingkat Pengangguran 
            Terbuka tetap tertahan tinggi di angka **{df_prov['TPT']:.2f}%**. Secara teoritis, terjadi penurunan koefisien elastisitas penyerapan ($\beta$) 
            pada Hukum Okun. Kondisi ini mengindikasikan bahwa ekspansi ekonomi didominasi oleh sektor padat modal atau peningkatan produktivitas 
            internal industri tanpa dibarengi dengan perluasan kesempatan kerja riil secara agregat.
            """
        elif df_prov['Pertumbuhan_PDRB'] <= 0:
            status_okun = "Kontraksi Output Agregat"
            narasi_okun = rf"""
            Tercatat stagnasi atau kontraksi output ekonomi daerah sebesar **{df_prov['Pertumbuhan_PDRB']:.2f}%**. Sesuai dengan aksioma Hukum Okun, 
            penurunan output riil ini mentransmisikan tekanan langsung berupa penurunan kapasitas produksi, yang secara linier menekan penyerapan 
            tenaga kerja dan berpotensi meningkatkan angka pengangguran terbuka sebesar **{df_prov['TPT']:.2f}%**.
            """
        else:
            status_okun = "Normal-Proporsional"
            narasi_okun = rf"""
            Pertumbuhan PDRB tercatat stabil pada level **{df_prov['Pertumbuhan_PDRB']:.2f}%** beriringan dengan Tingkat Pengangguran Terbuka (TPT) 
            sebesar **{df_prov['TPT']:.2f}%**. Dinamika ini merefleksikan berjalannya kerangka kerja Hukum Okun secara konvensional, di mana ekspansi 
            skala ekonomi daerah berjalan selaras dengan kapasitas penyerapan angkatan kerja regional.
            """

        # 3. Integrasi Kurva Phillips & Teori Neoklasik
        if df_prov['Inflasi_Nasional'] > 5.0 and df_prov['TPT'] > 5.0:
            status_phillips = "Gejala Stagflasi Regional"
            narasi_upah = rf"""
            Interaksi antara inflasi nasional sebesar **{df_prov['Inflasi_Nasional']:.2f}%** dan tingkat pengangguran **{df_prov['TPT']:.2f}%** mengindikasikan gejala guncangan sisi penawaran (*Supply-Shock*) jangka pendek pada sistem Kurva Phillips. Kondisi ini diperberat oleh 
            beban regulasi upah minimum, di mana rasio UMP terhadap PDRB mencapai **{df_prov['Rasio_UMP_PDRB']:.2f}%**. Angka rasio yang tinggi ini 
            menandakan beban kompensasi tenaga kerja formal yang semakin mendekati batas atas produktivitas marginal modal, sehingga mempersempit 
            ruang likuiditas industri padat karya untuk mempertahankan jumlah pekerja.
            """
        else:
            status_phillips = "Ekuilibrium Moneter-Labor Terjaga"
            narasi_upah = rf"""
            Tingkat inflasi nasional terekam sebesar **{df_prov['Inflasi_Nasional']:.2f}%** dengan proporsi rasio UMP terhadap PDRB daerah berada di level 
            **{df_prov['Rasio_UMP_PDRB']:.2f}%**. Berdasarkan teori permintaan tenaga kerja Neoklasik, struktur upah riil pada periode ini dinilai masih 
            berada dalam batas ekuilibrium yang wajar, di mana biaya input tenaga kerja formal belum menciptakan disinsentif ekstrem yang memicu otomatisasi 
            atau pemangkasan skala produksi massal oleh pelaku usaha.
            """

        # ====================================================
        # TAMPILAN ARTIKEL DOKUMEN RESMI (NATIVE WEB GRAPHIC)
        # ====================================================
        st.markdown("---")
        st.markdown(f"## Analisis Komprehensif Kondisi Makroekonomi Ketenagakerjaan")
        st.markdown(f"**Wilayah Evaluasi:** {pilihan_prov} | **Periode Data:** Tahun {tahun_terkini}")
        st.markdown(f"**Klasifikasi Maturitas Struktur Data:** *{df_prov['Maturitas_Wilayah']}*")
        st.markdown("---")
        
        # Bagian I
        st.markdown("### I. Diagnosis Evaluasi Risiko Ketenagakerjaan (Labor Stress Index)")
        st.markdown(f"- **Tingkat Indikasi Tekanan:** `{status_ews}`")
        st.markdown(f"- **Skor Indeks Objektif PCA:** `{df_prov['LSI']:.2f}` / `100.00`")
        st.write(narasi_lsi)
        
        # Bagian II
        st.markdown("### II. Evaluasi Parameter Riil & Transmisi Teori Ekonometrika")
        
        st.markdown("**1. Analisis Elastisitas Output (Kerangka Kerja Hukum Okun):**")
        st.caption(f"Kategori Struktur: {status_okun}")
        st.write(narasi_okun)
        
        st.markdown("**2. Analisis Struktur Harga dan Kompensasi Upah (Kerangka Kurva Phillips & Neoklasik):**")
        st.caption(f"Kategori Tren: {status_phillips}")
        st.write(narasi_upah)
        
        # Matriks Data
        st.markdown("**3. Ringkasan Parameter Deskriptif:**")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Pertumbuhan PDRB", f"{df_prov['Pertumbuhan_PDRB']:.2f}%")
        col_m2.metric("Pengangguran (TPT)", f"{df_prov['TPT']:.2f}%")
        col_m3.metric("Inflasi Nasional", f"{df_prov['Inflasi_Nasional']:.2f}%")
        col_m4.metric("Rasio UMP/PDRB", f"{df_prov['Rasio_UMP_PDRB']:.2f}%")
        
        # Bagian III
        st.markdown("### III. Pertimbangan Respons Kebijakan Strategis (Policy Considerations)")
        if df_prov['LSI'] >= 70:
            st.markdown("""
            * **Jangka Pendek:** Implementasi program subsidi upah bersyarat bagi industri manufaktur padat karya guna menahan gelombang PHK, serta penundaan pengenalan beban retribusi atau regulasi fiskal baru di tingkat daerah.
            * **Jangka Menengah:** Restrukturisasi skema investasi daerah dengan memberikan insentif khusus bagi pemodal yang berfokus pada penciptaan lapangan kerja skala masif (*labor-intensive sectors*).
            """)
        elif df_prov['LSI'] >= 40:
            st.markdown("""
            * **Jangka Pendek:** Optimalisasi peran bursa kerja lokal (*job-matching platform*) untuk menekan angka pengangguran friksional, disertai operasi pasar intervensi harga untuk menjaga stabilitas daya beli upah riil pekerja.
            * **Jangka Menengah:** Peningkatan alokasi anggaran pelatihan ulang keterampilan (*reskilling/upskilling*) yang disesuaikan dengan kebutuhan transformasi digital industri lokal.
            """)
        else:
            st.markdown("""
            * **Jangka Pendek:** Mempertahankan regulasi iklim usaha yang kondusif guna menjamin kepastian investasi, serta memfasilitasi integrasi rantai pasok antara industri skala besar dan UMKM daerah.
            * **Jangka Menengah:** Mendorong hilirisasi komoditas unggulan daerah guna menciptakan nilai tambah ekonomi yang berkelanjutan di sektor formal.
            """)
            
        st.markdown("---")
        
        # ====================================================
        # COMPILING DATA TEKS KHUSUS UNTUK FILE TXT
        # ====================================================
        teks_ekspor = f"""DOKUMEN INTERPRETASI MAKRO & LAPORAN KEBIJAKAN KETENAGAKERJAAN
========================================================================
DAERAH EVALUASI : {pilihan_prov}
PERIODE ANALISIS : TAHUN {tahun_terkini}
KLASIFIKASI DATA : {df_prov['Maturitas_Wilayah'].upper()}
========================================================================

I. DIAGNOSIS UTAMA & STATUS PERINGATAN INDIKATIF (LSI)
------------------------------------------------------------------------
- Skor Labor Stress Index (LSI) : {df_prov['LSI']:.2f} / 100.00
- Status Risiko                 : {status_ews}

Interpretasi Kondisi:
{narasi_lsi.strip()}

II. EVALUASI PARAMETER RIIL & TRANSMISI TEORI EKONOMETRIKA
------------------------------------------------------------------------
1. Analisis Elastisitas Output (Hukum Okun):
   * Kategori Struktur : {status_okun}
   * Diagnosis Detail  : {narasi_okun.strip().replace('**', '')}

2. Analisis Struktur Harga dan Kompensasi Upah (Kurva Phillips & Neoklasik):
   * Kategori Tren     : {status_phillips}
   * Diagnosis Detail  : {narasi_upah.strip().replace('**', '')}

3. Nilai Indikator Aktual:
   * Pertumbuhan PDRB  : {df_prov['Pertumbuhan_PDRB']:.2f}%
   * Pengangguran (TPT): {df_prov['TPT']:.2f}%
   * Inflasi Nasional  : {df_prov['Inflasi_Nasional']:.2f}%
   * Rasio UMP/PDRB    : {df_prov['Rasio_UMP_PDRB']:.2f}%

III. CATATAN PERTIMBANGAN KEBIJAKAN STRATEGIS
------------------------------------------------------------------------
Rekomendasi diarahkan pada penguatan mitigasi risiko pasar kerja lokal 
melalui harmonisasi regulasi upah riil yang disesuaikan dengan nilai 
tambah ekonomi riil regional demi menjaga keberlangsungan penyerapan 
tenaga kerja formal.

------------------------------------------------------------------------
Dokumen ini disusun sebagai ringkasan interpretasi indikatif berbasis 
bukti data makroekonomi regional.
========================================================================
"""

        # Meletakkan tombol unduhan dokumen formal
        c_space, c_btn = st.columns([3, 1])
        with c_btn:
            st.download_button(
                label="📥 Ekspor Ringkasan Teori-Data (TXT)",
                data=teks_ekspor,
                file_name=f"Laporan_Interpretasi_{pilihan_prov.replace(' ', '_')}_{tahun_terkini}.txt",
                mime="text/plain",
                use_container_width=True
            )
    else:
        st.error("Data indikator makroekonomi daerah tidak ditemukan untuk periode saat ini.")