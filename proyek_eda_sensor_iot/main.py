"""Jalankan seluruh 6 langkah secara berurutan: python main.py"""
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).parent / "src"
LANGKAH = [
    "step1_numpy_array.py",
    "step2_series_dataframe.py",
    "step3_loading_inspection.py",
    "step4_missing_value.py",
    "step5_duplikat_tipe_data.py",
    "step6_filter_sort_groupby.py",
]

for nama in LANGKAH:
    print(f"\n\n##### MENJALANKAN {nama} #####")
    hasil = subprocess.run([sys.executable, str(SRC / nama)], cwd=SRC)
    if hasil.returncode != 0:
        sys.exit(f"Gagal di {nama}")

print("\n\nSelesai. Hasil ada di data/processed/ dan outputs/")
