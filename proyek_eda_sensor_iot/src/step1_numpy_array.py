"""
LANGKAH 1 - Operasi Dasar NumPy Array
Konteks: contoh data suhu & kelembapan ruang kelas (sensor IoT).
"""
# %%
import numpy as np
from config import judul

# %% 1. Membuat array
judul("1. Membuat array")
suhu = np.array([29.1, 24.8, 30.3, 26.6, 27.0, 25.0, 29.3, 29.0, 31.6, 26.0])
kelembapan = np.array([55, 64, 45, 62, 59, 65, 65, 45, 70, 63])

print("suhu       :", suhu)
print("kelembapan :", kelembapan)
print("zeros      :", np.zeros(5))
print("ones       :", np.ones(5))
print("arange     :", np.arange(0, 10, 2))
print("linspace   :", np.linspace(0, 1, 5))

# %% 2. Atribut array
judul("2. Atribut array")
print("shape :", suhu.shape)
print("ndim  :", suhu.ndim)
print("size  :", suhu.size)
print("dtype :", suhu.dtype)

# %% 3. Indexing & slicing
judul("3. Indexing & slicing")
print("Elemen pertama   :", suhu[0])
print("Elemen terakhir  :", suhu[-1])
print("3 data pertama   :", suhu[:3])
print("Setiap 2 data    :", suhu[::2])

# %% 4. Operasi aritmatika (vectorized)
judul("4. Operasi aritmatika")
suhu_kalibrasi = suhu - 0.5            # koreksi sensor -0.5 derajat
suhu_fahrenheit = suhu * 9 / 5 + 32    # konversi C -> F
print("Kalibrasi  :", suhu_kalibrasi)
print("Fahrenheit :", np.round(suhu_fahrenheit, 1))
print("Heat index sederhana (suhu + kelembapan/10):", np.round(suhu + kelembapan / 10, 1))

# %% 5. Fungsi statistik
judul("5. Fungsi statistik")
print("Rata-rata :", suhu.mean())
print("Median    :", np.median(suhu))
print("Std dev   :", round(suhu.std(), 3))
print("Min / Max :", suhu.min(), "/", suhu.max())
print("Indeks suhu tertinggi:", suhu.argmax())

# %% 6. Boolean masking (filter)
judul("6. Boolean masking")
mask_panas = suhu > 29
print("Mask panas :", mask_panas)
print("Suhu > 29  :", suhu[mask_panas])
print("Jumlah     :", mask_panas.sum())

# %% 7. Reshape & array 2D
judul("7. Reshape & array 2D")
data_2d = np.column_stack((suhu, kelembapan))   # tiap baris = 1 bacaan
print("Array 2D (10 x 2):\n", data_2d)
print("Rata-rata per kolom (axis=0):", data_2d.mean(axis=0))
print("Rata-rata per baris (axis=1):", data_2d.mean(axis=1))
print("Reshape 5x2 suhu:\n", suhu.reshape(5, 2))

# %% 8. Sorting & nilai hilang
judul("8. Sorting & NaN")
print("Urut naik   :", np.sort(suhu))
print("Urut turun  :", np.sort(suhu)[::-1])
suhu_nan = np.array([29.1, np.nan, 30.3, np.nan, 27.0])
print("Dengan NaN  :", suhu_nan)
print("mean biasa  :", suhu_nan.mean())      # hasil nan
print("nanmean     :", np.nanmean(suhu_nan))  # abaikan nan
print("Ada NaN?    :", np.isnan(suhu_nan))
