import streamlit as st
import pandas as pd
import numpy as np
from supabase import create_client, Client
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler

@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

@st.cache_data(ttl=3600)
def load_cloud_data():
    try:
        supabase = init_supabase()
        response = supabase.table("macro_labor_data").select("*").execute()
        
        if not response.data:
            st.error("Kesalahan: Tabel database ditemukan tetapi tidak berisi data.")
            st.stop()
            
        df = pd.DataFrame(response.data)
        df.rename(columns={
            'provinsi': 'Provinsi', 'tahun': 'Tahun', 'pdrb': 'PDRB',
            'ump': 'UMP', 'tpt': 'TPT', 'inflasi_nasional': 'Inflasi_Nasional'
        }, inplace=True)
        
        return df.sort_values(by=['Provinsi', 'Tahun']).reset_index(drop=True)
    except Exception as e:
        st.error(f"Gagal mengambil data dari Supabase: {e}")
        st.stop()

@st.cache_data
def process_advanced_analytics(df):
    # Dictionary pemetaan Pulau Besar untuk Analisis Spasial
    peta_pulau = {
        'Aceh': 'Sumatera', 'Sumatera Utara': 'Sumatera', 'Sumatera Barat': 'Sumatera', 'Riau': 'Sumatera', 
        'Jambi': 'Sumatera', 'Sumatera Selatan': 'Sumatera', 'Bengkulu': 'Sumatera', 'Lampung': 'Sumatera', 
        'Kep. Bangka Belitung': 'Sumatera', 'Kep. Riau': 'Sumatera',
        'DKI Jakarta': 'Jawa', 'Jawa Barat': 'Jawa', 'Jawa Tengah': 'Jawa', 'DI Yogyakarta': 'Jawa', 
        'Jawa Timur': 'Jawa', 'Banten': 'Jawa',
        'Bali': 'Bali-Nusra', 'Nusa Tenggara Barat': 'Bali-Nusra', 'Nusa Tenggara Timur': 'Bali-Nusra',
        'Kalimantan Barat': 'Kalimantan', 'Kalimantan Tengah': 'Kalimantan', 'Kalimantan Selatan': 'Kalimantan', 
        'Kalimantan Timur': 'Kalimantan', 'Kalimantan Utara': 'Kalimantan',
        'Sulawesi Utara': 'Sulawesi', 'Sulawesi Tengah': 'Sulawesi', 'Sulawesi Selatan': 'Sulawesi', 
        'Sulawesi Tenggara': 'Sulawesi', 'Gorontalo': 'Sulawesi', 'Sulawesi Barat': 'Sulawesi',
        'Maluku': 'Maluku-Papua', 'Maluku Utara': 'Maluku-Papua', 'Papua': 'Maluku-Papua', 
        'Papua Barat': 'Maluku-Papua', 'Papua Selatan': 'Maluku-Papua', 'Papua Tengah': 'Maluku-Papua', 
        'Papua Pegunungan': 'Maluku-Papua', 'Papua Barat Daya': 'Maluku-Papua'
    }

    # Dictionary Titik Koordinat Kasar Tengah Provinsi untuk Geolocation Map
    peta_koordinat = {
        'Aceh': [4.69, 96.74], 'Sumatera Utara': [2.11, 99.13], 'Sumatera Barat': [-0.73, 100.8], 'Riau': [0.29, 101.7],
        'Jambi': [-1.61, 102.77], 'Sumatera Selatan': [-3.31, 103.91], 'Bengkulu': [-3.79, 102.26], 'Lampung': [-4.55, 105.4],
        'Kep. Bangka Belitung': [-2.74, 106.44], 'Kep. Riau': [3.91, 108.24],
        'DKI Jakarta': [-6.20, 106.84], 'Jawa Barat': [-6.91, 107.61], 'Jawa Tengah': [-7.15, 110.14], 'DI Yogyakarta': [-7.87, 110.42],
        'Jawa Timur': [-7.53, 112.23], 'Banten': [-6.44, 106.06], 'Bali': [-8.40, 115.18], 'Nusa Tenggara Barat': [-8.65, 117.36],
        'Nusa Tenggara Timur': [-8.65, 121.07], 'Kalimantan Barat': [-0.27, 111.47], 'Kalimantan Tengah': [-1.68, 113.38],
        'Kalimantan Selatan': [-3.09, 115.28], 'Kalimantan Timur': [1.08, 116.29], 'Kalimantan Utara': [3.13, 116.24],
        'Sulawesi Utara': [0.62, 123.97], 'Sulawesi Tengah': [-1.43, 121.44], 'Sulawesi Selatan': [-3.66, 119.97],
        'Sulawesi Tenggara': [-4.14, 122.17], 'Gorontalo': [0.69, 122.45], 'Sulawesi Barat': [-2.84, 119.33],
        'Maluku': [-3.23, 130.14], 'Maluku Utara': [0.63, 127.55], 'Papua': [-4.26, 138.08], 'Papua Barat': [-1.33, 132.9],
        'Papua Selatan': [-7.50, 139.00], 'Papua Tengah': [-4.00, 136.00], 'Papua Pegunungan': [-4.10, 139.30], 'Papua Barat Daya': [-1.10, 131.50]
    }

    hitung_tahun_asli = df.dropna(subset=['TPT', 'PDRB']).groupby('Provinsi')['Tahun'].nunique().to_dict()
    analyzed_dfs = []
    
    for provinsi, group in df.groupby('Provinsi'):
        group = group.copy().sort_values('Tahun')
        
        # SUNTIK DATA SPASIAL
        group['Pulau'] = peta_pulau.get(provinsi, 'Luar Pulau')
        koor = peta_koordinat.get(provinsi, [0.0, 0.0])
        group['Latitude'] = koor[0]
        group['Longitude'] = koor[1]
        
        jumlah_tahun = hitung_tahun_asli.get(provinsi, 0)
        group['Maturitas_Wilayah'] = "Ekonomi Matang" if jumlah_tahun >= 8 else "Ekonomi Berkembang/Baru"
        
        group['Pertumbuhan_PDRB'] = group['PDRB'].pct_change(fill_method=None) * 100
        group['Covid_Shock'] = group['Tahun'].apply(lambda x: 1 if x in [2020, 2021] else 0)
        
        features = group[['TPT', 'Inflasi_Nasional']].ffill().bfill().fillna(0)
        
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        pca = PCA(n_components=1)
        principal_component = pca.fit_transform(scaled_features)
        
        std_pca = np.std(principal_component)
        std_tpt = np.std(features['TPT'])
        
        if std_pca == 0 or std_tpt == 0:
            korelasi = 1
        else:
            korelasi = np.corrcoef(principal_component.flatten(), features['TPT'])[0, 1]
            
        if korelasi < 0:
            principal_component = principal_component * -1
            
        min_max_scaler = MinMaxScaler(feature_range=(0, 100))
        group['LSI'] = min_max_scaler.fit_transform(principal_component)
        group['Rasio_UMP_PDRB'] = (group['UMP'] / group['PDRB']) * 100
        
        analyzed_dfs.append(group)
        
    return pd.concat(analyzed_dfs).reset_index(drop=True)