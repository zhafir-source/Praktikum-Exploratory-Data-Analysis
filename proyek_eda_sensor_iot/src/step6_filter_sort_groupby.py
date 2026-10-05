"""
LANGKAH 6 - Filtering, Sorting, Groupby
Input : data/processed/step5_cleaned.csv
Output: outputs/*.csv dan outputs/*.png
"""
# %%
import pandas as pd
import matplotlib
matplotlib.use("Agg")           # simpan gambar tanpa membuka jendela
import matplotlib.pyplot as plt
from config import CSV_STEP5, OUTPUT, judul

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

df = pd.read_csv(CSV_STEP5, parse_dates=["waktu"])
df["ruang"] = df["ruang"].astype("category")
df["status_sensor"] = df["status_sensor"].astype("category")
print("Data siap:", df.shape)

# %% ===================== FILTERING =====================
judul("FILTERING")

print("1) Suhu >= 30 (ruang panas):")
panas = df[df["suhu_celsius"] >= 30]
print(panas[["id_bacaan", "ruang", "suhu_celsius"]].head(), "\n-> total", len(panas))

print("\n2) Hanya Lab Komputer (str.contains):")
lab = df[df["ruang"].str.contains("Lab")]
print("-> total", len(lab))

print("\n3) Sensor Aktif DAN suhu >= 30 (operator &):")
aktif_panas = df[(df["status_sensor"] == "Aktif") & (df["suhu_celsius"] >= 30)]
print(aktif_panas[["id_bacaan", "ruang", "suhu_celsius", "status_sensor"]])

print("\n4) isin - ruang XI RPL 1 atau XI RPL 2:")
print(df[df["ruang"].isin(["XI RPL 1", "XI RPL 2"])].shape)

print("\n5) between - kelembapan 50 s/d 60:")
print(df[df["kelembapan_persen"].between(50, 60)].shape)

print("\n6) query - jam pagi (07:00) & kelembapan > 60:")
print(df.query("jam == 7 and kelembapan_persen > 60")[["id_bacaan", "ruang", "waktu"]])

# %% ===================== SORTING =====================
judul("SORTING")

print("1) 5 suhu tertinggi:")
print(df.sort_values("suhu_celsius", ascending=False)
        [["id_bacaan", "ruang", "waktu", "suhu_celsius"]].head())

print("\n2) 5 suhu terendah:")
print(df.sort_values("suhu_celsius")[["id_bacaan", "ruang", "suhu_celsius"]].head())

print("\n3) Urut ruang (A-Z) lalu suhu (tinggi -> rendah):")
print(df.sort_values(["ruang", "suhu_celsius"], ascending=[True, False])
        [["ruang", "suhu_celsius"]].head(8))

print("\n4) nlargest 3 kelembapan:")
print(df.nlargest(3, "kelembapan_persen")[["id_bacaan", "ruang", "kelembapan_persen"]])

# %% ===================== GROUPBY =====================
judul("GROUPBY")

print("1) Rata-rata suhu per ruang:")
rata_ruang = df.groupby("ruang", observed=True)["suhu_celsius"].mean().round(2)
print(rata_ruang.sort_values(ascending=False))

print("\n2) Agregasi banyak fungsi per ruang:")
ringkasan_ruang = (
    df.groupby("ruang", observed=True)
      .agg(jumlah_data=("id_bacaan", "count"),
           suhu_rata2=("suhu_celsius", "mean"),
           suhu_min=("suhu_celsius", "min"),
           suhu_max=("suhu_celsius", "max"),
           kelembapan_rata2=("kelembapan_persen", "mean"))
      .round(2)
)
print(ringkasan_ruang)

print("\n3) Rata-rata suhu per jam:")
per_jam = df.groupby("jam")["suhu_celsius"].mean().round(2)
print(per_jam)

print("\n4) Jumlah bacaan per status sensor:")
print(df.groupby("status_sensor", observed=True).size())

print("\n5) Rata-rata suhu per tanggal:")
per_tanggal = df.groupby(df["waktu"].dt.date)["suhu_celsius"].mean().round(2)
print(per_tanggal)

print("\n6) Pivot table: rata-rata suhu ruang x jam:")
pivot = df.pivot_table(index="ruang", columns="jam", values="suhu_celsius",
                       aggfunc="mean", observed=True).round(1)
print(pivot)

print("\n7) Crosstab ruang x status sensor:")
print(pd.crosstab(df["ruang"], df["status_sensor"]))

# %% ===================== INSIGHT =====================
judul("INSIGHT")
ruang_terpanas = rata_ruang.idxmax()
jam_terpanas = per_jam.idxmax()
persen_aktif = (df["status_sensor"] == "Aktif").mean() * 100
print(f"- Ruang dengan suhu rata-rata tertinggi : {ruang_terpanas} ({rata_ruang.max()} C)")
print(f"- Jam dengan suhu rata-rata tertinggi   : {jam_terpanas}:00 ({per_jam.max()} C)")
print(f"- Persentase bacaan dari sensor Aktif   : {persen_aktif:.1f}%")
print(f"- Bacaan dengan suhu >= 30 C            : {len(panas)} dari {len(df)}")

# %% ===================== SIMPAN HASIL =====================
judul("SIMPAN HASIL")
ringkasan_ruang.to_csv(OUTPUT / "ringkasan_per_ruang.csv")
per_jam.to_csv(OUTPUT / "suhu_per_jam.csv")
pivot.to_csv(OUTPUT / "pivot_ruang_jam.csv")

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
rata_ruang.sort_values().plot.barh(ax=ax[0], color="#14a89b")
ax[0].set_title("Rata-rata suhu per ruang")
ax[0].set_xlabel("Suhu (C)")
per_jam.plot(ax=ax[1], marker="o", color="#e4572e")
ax[1].set_title("Rata-rata suhu per jam")
ax[1].set_xlabel("Jam")
ax[1].set_ylabel("Suhu (C)")
plt.tight_layout()
plt.savefig(OUTPUT / "grafik_suhu.png", dpi=150)
print("Tersimpan di folder outputs/:")
for f in sorted(OUTPUT.iterdir()):
    print(" -", f.name)
