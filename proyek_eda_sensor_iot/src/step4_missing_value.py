"""
LANGKAH 4 - Menangani Missing Value
Input : data/raw/dataset_sensor_iot_kelas.csv
Output: data/processed/step4_missing_handled.csv
"""
# %%
import numpy as np
import pandas as pd
from config import RAW_CSV, CSV_STEP4, judul

pd.set_option("display.width", 200)
df = pd.read_csv(RAW_CSV)

# %% 1. Deteksi missing
judul("1. Deteksi missing value")
missing = df.isna().sum()
persen = (df.isna().mean() * 100).round(2)
print(pd.DataFrame({"jumlah": missing, "persen": persen}))

print("\nBaris yang memiliki missing:")
print(df[df.isna().any(axis=1)])

# %% 2. Ekstrak angka suhu agar bisa dihitung
# Syarat sebelum imputasi: kolom suhu harus numerik.
# '27.0C' dan '26.6 derajat' -> 27.0 dan 26.6
judul("2. Ekstrak angka dari suhu_celsius")
df["suhu_celsius"] = pd.to_numeric(
    df["suhu_celsius"].str.extract(r"(-?\d+\.?\d*)")[0], errors="coerce"
)
print(df["suhu_celsius"].describe())

# %% 3. Deteksi nilai tidak valid (outlier fisik) -> jadikan NaN
judul("3. Nilai tidak masuk akal -> NaN")
SUHU_MIN, SUHU_MAX = 15, 40          # suhu ruang kelas wajar
HUM_MIN, HUM_MAX = 0, 100            # kelembapan relatif 0-100 %

suhu_invalid = ~df["suhu_celsius"].between(SUHU_MIN, SUHU_MAX) & df["suhu_celsius"].notna()
hum_invalid = ~df["kelembapan_persen"].between(HUM_MIN, HUM_MAX) & df["kelembapan_persen"].notna()

print("Suhu tidak valid:\n", df.loc[suhu_invalid, ["id_bacaan", "suhu_celsius"]])
print("Kelembapan tidak valid:\n", df.loc[hum_invalid, ["id_bacaan", "kelembapan_persen"]])

df.loc[suhu_invalid, "suhu_celsius"] = np.nan
df.loc[hum_invalid, "kelembapan_persen"] = np.nan

print("\nMissing setelah outlier dijadikan NaN:\n", df.isna().sum())

# %% 4. Strategi penanganan
# - suhu & kelembapan (numerik)  -> isi dengan MEDIAN (tahan terhadap outlier)
# - status_sensor (kategori)     -> isi 'Tidak Diketahui' (jangan menebak)
judul("4. Imputasi")
median_suhu = df["suhu_celsius"].median()
median_hum = df["kelembapan_persen"].median()
print(f"Median suhu       : {median_suhu}")
print(f"Median kelembapan : {median_hum}")

df["suhu_celsius"] = df["suhu_celsius"].fillna(median_suhu)
df["kelembapan_persen"] = df["kelembapan_persen"].fillna(median_hum)
df["status_sensor"] = df["status_sensor"].fillna("Tidak Diketahui")

# %% 5. Verifikasi & simpan
judul("5. Verifikasi")
print("Sisa missing:\n", df.isna().sum())
assert df.isna().sum().sum() == 0, "Masih ada missing value!"

df.to_csv(CSV_STEP4, index=False)
print(f"\nTersimpan: {CSV_STEP4}")
