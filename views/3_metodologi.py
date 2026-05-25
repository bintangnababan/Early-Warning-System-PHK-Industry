import streamlit as st
import pandas as pd
from datetime import datetime
from views.data_engine import load_cloud_data, process_advanced_analytics

st.title("Metodologi, Dokumentasi & Referensi Ilmiah")
st.markdown("Analisis komprehensif landasan teoritis makroekonomi dan instrumen pelaporan kebijakan berbasis bukti data.")
st.divider()

tab_teori, tab_interpretasi = st.tabs(["📖 Landasan Teori Makroekonomi", "📄 Laporan Analisis & Kebijakan"])

# --------------------------------------------------------
# TAB 1: LANDASAN TEORI KOMPREHENSIF
# --------------------------------------------------------
with tab_teori:
    st.header("Kerangka Teoritis Analisis Pasar Tenaga Kerja")
    st.markdown("""
    Sistem indikatif ini dibangun di atas sintesis tiga pilar utama ekonomi makro struktural. Pendekatan ini diperlukan untuk 
    memahami transmisi kausalitas antara pertumbuhan ekonomi, stabilitas harga, dan elastisitas penyerapan tenaga kerja 
    di tingkat regional.
    """)
    
    st.markdown("---")
    st.subheader("1. Hukum Okun (Okun's Law) & Dinamika Output-Ketenagakerjaan")
    st.latex(r"\Delta U = \alpha - \beta(g)")
    
    st.markdown(r"""
    **Mekanisme Transmisi dan Koefisien Elastisitas:** Formulasi Arthur Okun (1962) mempostulatkan adanya hubungan empiris negatif antara perubahan tingkat pengangguran ($\Delta U$) 
    dan pertumbuhan ekonomi riil ($g$). Parameter $\alpha$ merepresentasikan tingkat pertumbuhan ekonomi minimum yang diperlukan 
    hanya untuk menjaga agar tingkat pengangguran tetap konstan (mengingat adanya pertumbuhan angkatan kerja baru dan peningkatan produktivitas). 
    Sementara itu, koefisien $\beta$ mengukur elastisitas penyerapan tenaga kerja terhadap setiap persen pertumbuhan output.

    **Kondisi Batas Struktural (Jobless Growth):** Dalam konteks ekonomi regional, hukum ini sering kali mengalami deviasi akibat perubahan struktur ekonomi. Fenomena *Jobless Growth* terjadi ketika pertumbuhan PDRB digerakkan oleh sektor padat modal (seperti industri ekstraktif, keuangan, atau teknologi tinggi) atau 
    melalui intensifikasi modal tanpa perluasan lapangan kerja riil. Dalam kondisi ini, meskipun angka $g$ tinggi, koefisien $\beta$ mengecil 
    sehingga gagal menurunkan angka pengangguran secara signifikan.
    """)
    
    st.markdown("---")
    st.subheader("2. Kurva Phillips (Phillips Curve) & Ekspektasi Inflasi-Pengangguran")
    st.latex(r"\pi = \pi^e - \beta(U - U^n) + v")
    
    st.markdown(r"""
    **Interaksi Jangka Pendek dan Guncangan Sisi Penawaran:** Kurva Phillips modern (dikembangkan dari A.W. Phillips, 1958) menjelaskan tarik-ulur (*trade-off*) jangka pendek antara 
    tingkat inflasi ($\pi$) dan pengangguran ($U$). Dinamika ini dipengaruhi oleh ekspektasi inflasi dari pelaku pasar ($\pi^e$), 
    tingkat pengangguran alamiah ($U^n$), dan guncangan pasokan eksternal ($v$). Ketika pasar tenaga kerja mengetat ($U < U^n$), 
    daya tawar pekerja meningkat, memicu kenaikan upah nominal yang kemudian ditransmisikan oleh produsen ke dalam harga jual produk (inflasi).

    **Ancaman Stagflasi Sektoral:** Jika perekonomian dihantam oleh guncangan pasokan ($v$) yang parah—seperti lonjakan biaya logistik, krisis energi, atau disrupsi 
    rantai pasok global—kurva Phillips akan bergeser secara struktural ke arah kanan atas. Kondisi ini melahirkan *Stagflasi*, di mana 
    inflasi tinggi dan pengangguran tinggi terjadi secara simultan. Dalam kondisi ini, instrumen kebijakan stimulus permintaan konvensional 
    menjadi tidak efektif karena meredakan satu sisi justru akan memperparah sisi lainnya.
    """)
    
    st.markdown("---")
    st.subheader("3. Teori Permintaan Tenaga Kerja Neoklasik & Struktur Beban Upah Riil")
    st.latex(r"L^d = f\left(\frac{W}{P}\right)")
    st.markdown(r"""
    **Produktivitas Marjinal dan Maksimalisasi Keuntungan:** Berdasarkan teori Neoklasik (Borjas, 2014), perusahaan mengoptimalkan keuntungan dengan mempekerjakan tenaga kerja hingga titik 
    di mana Produk Marjinal Tenaga Kerja (*Marginal Product of Labor*) sama dengan upah riil ($W/P$). Di sini, $W$ mewakili upah nominal 
    (termasuk regulasi Upah Minimum Provinsi) dan $P$ mewakili tingkat harga umum (inflasi).

    **Efek Substitusi dan Efek Output Regulasi Upah:** Kenaikan Upah Minimum Provinsi (UMP) yang tidak diimbangi oleh peningkatan produktivitas pekerja atau kenaikan nilai tambah PDRB 
    akan menggelembungkan biaya upah riil. Industri, khususnya sektor manufaktur padat karya, akan merespons fenomena ini melalui dua jalur:
    1. *Efek Substitusi:* Perusahaan mempercepat otomatisasi dengan mengganti tenaga kerja manusia menggunakan modal/mesin.
    2. *Efek Output:* Perusahaan terpaksa menurunkan skala produksi atau merelokasi pabrik ke wilayah dengan biaya input lebih rendah. 
    Kedua efek ini secara akumulatif menurunkan permintaan total tenaga kerja ($L^d$) dan memicu risiko pemutusan hubungan kerja (PHK).
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