"""
LANGKAH 2 - Membuat Series & DataFrame
"""
# %%
import numpy as np
import pandas as pd
from config import judul

# %% 1. Series
judul("1. Pandas Series")
suhu = pd.Series([29.1, 24.8, 30.3, 26.6], name="suhu_celsius")
print(suhu)

suhu_ruang = pd.Series(
    [29.1, 24.8, 30.3],
    index=["Lab Komputer 1", "XI RPL 1", "XI RPL 2"],
    name="suhu_celsius",
)
print("\nSeries dengan index custom:\n", suhu_ruang)
print("\nAkses label   :", suhu_ruang["XI RPL 1"])
print("Akses posisi  :", suhu_ruang.iloc[0])
print("Rata-rata     :", suhu_ruang.mean())
print("Suhu > 26     :\n", suhu_ruang[suhu_ruang > 26])
print("Dari NumPy    :\n", pd.Series(np.array([1, 2, 3])))

# %% 2. DataFrame dari dictionary
judul("2. DataFrame dari dictionary")
data = {
    "id_bacaan": ["SNS0001", "SNS0002", "SNS0003", "SNS0004", "SNS0005"],
    "ruang": ["Lab Komputer 1", "Lab Komputer 2", "XI RPL 1", "XI RPL 2", "XI RPL 3"],
    "suhu_celsius": [29.3, 30.0, 31.2, 30.0, 29.5],
    "kelembapan_persen": [65, 49, 58, 70, 68],
    "status_sensor": ["Aktif", "Aktif", "Nonaktif", "Nonaktif", "Aktif"],
}
df = pd.DataFrame(data)
print(df)

# %% 3. DataFrame dari list of list & NumPy
judul("3. DataFrame dari list of list / NumPy")
df_list = pd.DataFrame(
    [["SNS0001", 29.3], ["SNS0002", 30.0], ["SNS0003", 31.2]],
    columns=["id_bacaan", "suhu_celsius"],
)
print(df_list)
df_np = pd.DataFrame(np.random.default_rng(42).normal(28, 2, (3, 2)).round(1),
                     columns=["suhu", "kelembapan"])
print(df_np)

# %% 4. Atribut DataFrame
judul("4. Atribut DataFrame")
print("shape   :", df.shape)
print("columns :", list(df.columns))
print("index   :", df.index)
print("dtypes  :\n", df.dtypes)

# %% 5. Akses data (kolom, loc, iloc)
judul("5. Akses data")
print("Satu kolom (Series):\n", df["ruang"])
print("\nDua kolom:\n", df[["id_bacaan", "suhu_celsius"]])
print("\nloc  baris 0-2, kolom tertentu:\n", df.loc[0:2, ["ruang", "suhu_celsius"]])
print("\niloc baris 1, semua kolom:\n", df.iloc[1])
print("\niloc 2 baris x 2 kolom:\n", df.iloc[:2, :2])

# %% 6. Menambah, mengubah, menghapus kolom
judul("6. Manipulasi kolom")
df["suhu_fahrenheit"] = (df["suhu_celsius"] * 9 / 5 + 32).round(1)
df["kategori_suhu"] = np.where(df["suhu_celsius"] >= 30, "Panas", "Normal")
print(df)

df = df.rename(columns={"kelembapan_persen": "kelembapan"})
df = df.drop(columns=["suhu_fahrenheit"])
print("\nSetelah rename & drop:\n", df)

# %% 7. Menjadikan id_bacaan sebagai index
judul("7. set_index")
df_idx = df.set_index("id_bacaan")
print(df_idx)
print("\nAmbil SNS0003:\n", df_idx.loc["SNS0003"])
