# Proyek EDA - Dataset Sensor IoT Kelas

Modul Ajar KKA - Elemen 2: EDA
**Tahapan: 6 Langkah Menuju Proyek** (NumPy, Pandas, cleaning, analisis).

## Struktur Folder

```
proyek_eda_sensor_iot/
├── .vscode/settings.json          # pengaturan VS Code
├── data/
│   ├── raw/                       # data asli (jangan diubah)
│   │   └── dataset_sensor_iot_kelas.csv
│   └── processed/                 # data hasil tiap langkah
│       ├── step4_missing_handled.csv
│       └── step5_cleaned.csv
├── src/
│   ├── config.py                  # path & helper
│   ├── step1_numpy_array.py       # 1. Operasi dasar NumPy Array
│   ├── step2_series_dataframe.py  # 2. Membuat Series & DataFrame
│   ├── step3_loading_inspection.py# 3. Data Loading & Inspection
│   ├── step4_missing_value.py     # 4. Menangani Missing Value
│   ├── step5_duplikat_tipe_data.py# 5. Menangani Duplikat & Tipe Data
│   └── step6_filter_sort_groupby.py# 6. Filtering, Sorting, Groupby
├── outputs/                       # hasil akhir (CSV ringkasan + grafik)
├── main.py                        # jalankan semua langkah
├── requirements.txt
└── README.md
```

## Cara Menjalankan di VS Code

1. `File > Open Folder` -> pilih folder `proyek_eda_sensor_iot`
2. Buka terminal (`Ctrl + ``) lalu:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows  (Mac/Linux: source .venv/bin/activate)
   pip install -r requirements.txt
   ```
3. Jalankan semua langkah: `python main.py`
   atau satu per satu: `python src/step3_loading_inspection.py`
4. Tiap file memakai penanda `# %%`, jadi bisa dijalankan per sel
   (klik **Run Cell** / `Shift+Enter`) dengan ekstensi Jupyter.

Jalankan berurutan: step 4 membaca data mentah, step 5 membaca hasil step 4, step 6 membaca hasil step 5.

## Masalah Data yang Ditemukan & Solusinya

| Masalah | Langkah | Solusi |
|---|---|---|
| Missing di suhu, kelembapan, status | 4 | median / "Tidak Diketahui" |
| Outlier (suhu 90 C, kelembapan 250 %) | 4 | dijadikan NaN lalu diimputasi |
| Suhu bertipe teks ('27.0C', '26.6 derajat') | 4 | regex ekstrak angka |
| 4 baris duplikat | 5 | `drop_duplicates()` (74 -> 70 baris) |
| 3 format waktu berbeda | 5 | fungsi `parse_waktu` -> datetime |
| 15 variasi nama ruang | 5 | dinormalisasi jadi 5 ruang |
| Status AKTIF/aktif/Aktif | 5 | `str.title()` |
| Analisis | 6 | filter, sort, groupby, pivot, grafik |
