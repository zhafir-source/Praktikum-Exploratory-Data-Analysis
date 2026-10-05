"""
LANGKAH 5 - Menangani Duplikat & Tipe Data
Input : data/processed/step4_missing_handled.csv
Output: data/processed/step5_cleaned.csv
"""
# %%
import re
import pandas as pd
from config import CSV_STEP4, CSV_STEP5, judul

pd.set_option("display.width", 200)
df = pd.read_csv(CSV_STEP4)

# %% 1. Duplikat
judul("1. Deteksi & hapus duplikat")
print("Jumlah baris awal :", len(df))
print("Duplikat penuh    :", df.duplicated().sum())
print(df[df.duplicated(keep=False)].sort_values("id_bacaan"))

df = df.drop_duplicates().reset_index(drop=True)
print("\nJumlah baris akhir:", len(df))
print("ID bacaan masih duplikat?", df["id_bacaan"].duplicated().any())

# %% 2. Tipe data awal
judul("2. Tipe data sebelum diperbaiki")
print(df.dtypes)

# %% 3. Seragamkan format waktu -> datetime
BULAN = {
    "januari": 1, "februari": 2, "maret": 3, "april": 4, "mei": 5, "juni": 6,
    "juli": 7, "agustus": 8, "september": 9, "oktober": 10, "november": 11, "desember": 12,
}


def parse_waktu(teks):
    """Ubah 3 format waktu berbeda menjadi pd.Timestamp."""
    t = str(teks).strip().lower()

    # '4 agustus 2026 jam 13:00'
    m = re.match(r"(\d{1,2})\s+([a-z]+)\s+(\d{4})\s+jam\s+(\d{1,2})[:.](\d{2})", t)
    if m:
        d, bln, y, h, mnt = m.groups()
        return pd.Timestamp(int(y), BULAN[bln], int(d), int(h), int(mnt))

    # '2026-08-08 7:00'
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})\s+(\d{1,2})[:.](\d{2})", t)
    if m:
        y, bln, d, h, mnt = m.groups()
        return pd.Timestamp(int(y), int(bln), int(d), int(h), int(mnt))

    # '05/08/2026 15.00'  (dd/mm/yyyy)
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})\s+(\d{1,2})[:.](\d{2})", t)
    if m:
        d, bln, y, h, mnt = m.groups()
        return pd.Timestamp(int(y), int(bln), int(d), int(h), int(mnt))

    return pd.NaT


judul("3. Waktu -> datetime")
df["waktu"] = df["waktu"].apply(parse_waktu)
print("Waktu gagal diparse:", df["waktu"].isna().sum())
print(df["waktu"].head())

# Kolom turunan untuk analisis
df["tanggal"] = df["waktu"].dt.date
df["jam"] = df["waktu"].dt.hour
df["hari"] = df["waktu"].dt.day_name()

# %% 4. Seragamkan nama ruang
judul("4. Standarisasi nama ruang")
print("Sebelum:", df["ruang"].nunique(), "variasi")


def normalisasi_ruang(teks):
    t = str(teks).lower().replace("-", " ").replace("kelas", "").strip()
    t = re.sub(r"\s+", " ", t)
    if "lab" in t:                                   # 'lab komputer 1'
        return t.title()                             # -> 'Lab Komputer 1'
    return t.upper()                                 # 'xi rpl 3' -> 'XI RPL 3'


df["ruang"] = df["ruang"].apply(normalisasi_ruang)
print("Sesudah:", df["ruang"].nunique(), "ruang ->", sorted(df["ruang"].unique()))

# %% 5. Seragamkan status sensor
judul("5. Standarisasi status_sensor")
df["status_sensor"] = df["status_sensor"].str.strip().str.title()
print(df["status_sensor"].value_counts())

# %% 6. Konversi tipe data
judul("6. Konversi tipe data")
df["id_bacaan"] = df["id_bacaan"].astype("string")
df["ruang"] = df["ruang"].astype("category")
df["status_sensor"] = df["status_sensor"].astype("category")
df["suhu_celsius"] = df["suhu_celsius"].astype("float64")
df["kelembapan_persen"] = df["kelembapan_persen"].astype("float64")
df["jam"] = df["jam"].astype("int8")

print(df.dtypes)
print("\nMemori:", round(df.memory_usage(deep=True).sum() / 1024, 1), "KB")

# %% 7. Simpan
judul("7. Simpan data bersih")
df = df.sort_values("waktu").reset_index(drop=True)
df.to_csv(CSV_STEP5, index=False)
print(df.head(10))
print(f"\nTersimpan: {CSV_STEP5}  | shape = {df.shape}")
