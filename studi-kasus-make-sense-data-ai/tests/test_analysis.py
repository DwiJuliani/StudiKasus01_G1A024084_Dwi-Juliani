import unittest
import pandas as pd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analysis import clean_data


class TestCleanData(unittest.TestCase):
    def test_duplicate_and_missing_rows_are_removed(self):
        data = pd.DataFrame([
            {"tanggal":"2026-01-01","produk":"Buku","jumlah_terjual":2,"harga_satuan":10000,"wilayah":"Bengkulu"},
            {"tanggal":"2026-01-01","produk":"Buku","jumlah_terjual":2,"harga_satuan":10000,"wilayah":"Bengkulu"},
            {"tanggal":"2026-01-02","produk":"Pulpen","jumlah_terjual":None,"harga_satuan":4000,"wilayah":"Curup"},
        ])
        cleaned = clean_data(data)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned.iloc[0]["pendapatan"], 20000)


if __name__ == "__main__":
    unittest.main()
