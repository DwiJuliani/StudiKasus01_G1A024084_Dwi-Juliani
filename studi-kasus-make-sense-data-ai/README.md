# Studi Kasus: Make Sense of Data with Analysis and AI

## 1. Latar belakang
Sebuah toko ingin memahami hasil penjualan agar dapat menentukan produk yang perlu diprioritaskan dan memperkirakan kebutuhan stok. Data transaksi masih perlu diperiksa karena dapat mengandung nilai kosong dan baris duplikat. Proyek ini menerapkan gagasan dalam materi **Make Sense of Data with Analysis and AI**: mengubah data mentah menjadi informasi, insight, dan rekomendasi keputusan.

## 2. Tujuan
- Membersihkan data kosong dan data duplikat.
- Menghitung pendapatan dari jumlah terjual dikali harga satuan.
- Membuat ringkasan penjualan per produk dan wilayah.
- Membuat perkiraan sederhana penjualan harian.
- Menghasilkan rekomendasi awal berdasarkan data.

## 3. Hubungan dengan materi
- **Business Understanding:** memahami kebutuhan toko untuk mengetahui produk dan wilayah penjualan yang perlu diperhatikan.
- **Data Understanding:** memeriksa struktur dan isi `data/penjualan.csv`.
- **Data Preparation:** menangani nilai kosong, menghapus duplikasi, dan membuat kolom pendapatan.
- **Modeling:** menggunakan model regresi linear sederhana untuk memperkirakan jumlah penjualan.
- **Evaluation:** mengukur hasil prediksi dengan MAE pada data uji.
- **Deployment:** menyimpan ringkasan dan hasil prediksi ke folder `outputs/`.

Empat jenis analisis juga diterapkan:
- **Descriptive:** total pendapatan dan jumlah produk terjual.
- **Diagnostic:** membandingkan hasil penjualan berdasarkan produk dan wilayah.
- **Predictive:** memperkirakan penjualan untuk data uji menggunakan regresi linear.
- **Prescriptive:** memberi saran stok awal berdasarkan produk dengan penjualan tertinggi.

## 4. Struktur proyek
```text
studi-kasus-make-sense-data-ai/
├── data/
│   └── penjualan.csv
├── src/
│   └── analysis.py
├── tests/
│   └── test_analysis.py
├── outputs/                 # hasil otomatis saat program dijalankan
├── requirements.txt
├── README.md
└── .gitignore
```

## 5. Cara menjalankan
Pastikan Python 3.10 atau lebih baru telah terpasang.

```bash
pip install -r requirements.txt
python src/analysis.py
```
Di Windows, jika perlu gunakan `py src/analysis.py`.

Untuk menjalankan tes:
```bash
python -m unittest discover -s tests
```

## 6. Hasil keluaran
Setelah dijalankan, folder `outputs/` akan berisi:
- `ringkasan_penjualan.csv`: ringkasan per produk.
- `analisis_wilayah.csv`: ringkasan per wilayah.
- `prediksi_penjualan.csv`: nilai aktual dan prediksi pada data uji.
- `laporan_analisis.txt`: ringkasan temuan, MAE, dan rekomendasi.

## 7. Catatan
Data transaksi dalam proyek ini adalah data simulasi untuk pembelajaran, bukan data toko sungguhan. Prediksi regresi linear hanya contoh penerapan dan tidak menjamin penjualan mendatang. Keputusan stok sebaiknya mempertimbangkan faktor lain seperti musim, ketersediaan pemasok, promosi, dan perubahan permintaan. AI membantu analisis, tetapi hasilnya tetap perlu diperiksa manusia.
