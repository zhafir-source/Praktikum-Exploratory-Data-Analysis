"""
LANGKAH 3 - Data Loading & Inspection
Memuat dataset sensor IoT dan memeriksa kualitas data (belum dibersihkan).
"""
# %%
import pandas as pd
from config import RAW_CSV, judul

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

# %% 1. Loading
judul("1. Loading data")
df = pd.read_csv(RAW_CSV)
print("File:", RAW_CSV.name)

# %% 2. Inspeksi awal
judul("2. Inspeksi awal")
print("Shape   :", df.shape, "(baris, kolom)")
print("\n5 baris pertama:\n", df.head())
print("\n5 baris terakhir:\n", df.tail())
print("\nSampel acak:\n", df.sample(5, random_state=1))

# %% 3. Struktur & tipe data
judul("3. Struktur & tipe data")
df.info()
print("\nTipe data:\n", df.dtypes)

# %% 4. Statistik deskriptif
judul("4. Statistik deskriptif")
print(df.describe(include="all").T)

# %% 5. Nilai unik tiap kolom
judul("5. Jumlah nilai unik")
print(df.nunique())

# %% 6. Cek variasi penulisan kategori
judul("6. Variasi penulisan (kategori tidak konsisten)")
print("Ruang:\n", df["ruang"].value_counts())
print("\nStatus sensor:\n", df["status_sensor"].value_counts(dropna=False))

# %% 7. Format waktu & suhu yang berantakan
judul("7. Contoh format tidak seragam")
print("Waktu :", df["waktu"].sample(6, random_state=3).tolist())
print("Suhu  :", df.loc[df["suhu_celsius"].str.contains("[a-zA-Z]", na=False),
                        "suhu_celsius"].head(6).tolist())

# %% 8. Missing & duplikat (ringkas)
judul("8. Missing value & duplikat")
print("Missing per kolom:\n", df.isna().sum())
print("\nBaris duplikat penuh :", df.duplicated().sum())
print("ID bacaan duplikat   :", df["id_bacaan"].duplicated().sum())

# %% 9. Temuan masalah
judul("9. CATATAN TEMUAN MASALAH DATA")
temuan = [
    "Kolom waktu memiliki 3 format berbeda (ISO, dd/mm/yyyy, teks 'Agustus ... jam')",
    "Kolom suhu_celsius bertipe teks karena ada satuan ('27.0C', '26.6 derajat')",
    "Nama ruang tidak konsisten (XI-RPL-3, kelas xi rpl 3, Kelas XI RPL 3, ...)",
    "Status sensor tidak konsisten huruf besar/kecil (AKTIF, aktif, Aktif)",
    "Ada missing value di suhu, kelembapan, dan status_sensor",
    "Ada outlier tidak masuk akal (suhu 90 C, kelembapan 250 %)",
    "Ada baris duplikat",
]
for i, t in enumerate(temuan, 1):
    print(f"{i}. {t}")
