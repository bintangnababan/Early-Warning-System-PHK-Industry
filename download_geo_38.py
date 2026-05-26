import urllib.request
import os
import json

os.makedirs('geo', exist_ok=True)

# URL GeoJSON 38 Provinsi terbaru (termasuk pemekaran Papua)
url = "https://raw.githubusercontent.com/denyherianto/indonesia-geojson-topojson-maps-with-38-provinces/refs/heads/main/GeoJSON/indonesia-38-provinces.geojson"
file_path = "geo/indonesia_38.geojson"

print("⏳ Sedang mengunduh peta 38 Provinsi Indonesia...")
try:
    urllib.request.urlretrieve(url, file_path)
    print("✅ Peta berhasil disimpan di:", file_path)
    
    # Mengintip key properties untuk Plotly
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print("\n🔍 CONTOH ISI DATA PROVINSI:")
        print(data['features'][0]['properties'])
except Exception as e:
    print("❌ Gagal mengunduh:", e)
    print("Silakan unduh manual dari: https://github.com/denyherianto/indonesia-geojson-topojson-maps-with-38-provinces")