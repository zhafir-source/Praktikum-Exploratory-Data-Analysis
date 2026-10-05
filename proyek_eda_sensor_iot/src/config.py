"""Konfigurasi path proyek (dipakai oleh semua langkah)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RAW_CSV = ROOT / "data" / "raw" / "dataset_sensor_iot_kelas.csv"
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "outputs"

CSV_STEP4 = PROCESSED / "step4_missing_handled.csv"
CSV_STEP5 = PROCESSED / "step5_cleaned.csv"

PROCESSED.mkdir(parents=True, exist_ok=True)
OUTPUT.mkdir(parents=True, exist_ok=True)


def judul(teks: str) -> None:
    """Cetak judul bagian agar output terminal rapi."""
    print("\n" + "=" * 70)
    print(teks)
    print("=" * 70)
