"""Analisis penjualan sebagai contoh penerapan CRISP-DM dan analisis data."""
from pathlib import Path
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "penjualan.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

REQUIRED_COLUMNS = ["tanggal", "produk", "jumlah_terjual", "harga_satuan", "wilayah"]


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Membersihkan kolom wajib, nilai kosong, dan baris duplikat."""
    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)
    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan: {sorted(missing_columns)}")
    cleaned = data.copy()
    cleaned = cleaned.drop_duplicates()
    cleaned["tanggal"] = pd.to_datetime(cleaned["tanggal"], errors="coerce")
    cleaned["jumlah_terjual"] = pd.to_numeric(cleaned["jumlah_terjual"], errors="coerce")
    cleaned["harga_satuan"] = pd.to_numeric(cleaned["harga_satuan"], errors="coerce")
    cleaned = cleaned.dropna(subset=REQUIRED_COLUMNS)
    cleaned = cleaned[(cleaned["jumlah_terjual"] >= 0) & (cleaned["harga_satuan"] >= 0)]
    cleaned["pendapatan"] = cleaned["jumlah_terjual"] * cleaned["harga_satuan"]
    return cleaned.sort_values("tanggal").reset_index(drop=True)


def run_analysis(data_path: Path = DATA_FILE) -> dict:
    raw = pd.read_csv(data_path)
    cleaned = clean_data(raw)

    # Descriptive analytics: ringkasan jumlah dan pendapatan per produk.
    by_product = cleaned.groupby("produk", as_index=False).agg(
        total_terjual=("jumlah_terjual", "sum"),
        total_pendapatan=("pendapatan", "sum"),
        rata_rata_terjual=("jumlah_terjual", "mean"),
    ).sort_values("total_pendapatan", ascending=False)
    by_product.to_csv(OUT / "ringkasan_penjualan.csv", index=False)

    # Diagnostic analytics: membandingkan hasil berdasarkan wilayah.
    by_region = cleaned.groupby("wilayah", as_index=False).agg(
        total_terjual=("jumlah_terjual", "sum"),
        total_pendapatan=("pendapatan", "sum"),
    ).sort_values("total_pendapatan", ascending=False)
    by_region.to_csv(OUT / "analisis_wilayah.csv", index=False)

    # Predictive analytics: prediksi jumlah terjual memakai fitur tanggal dan harga.
    model_data = cleaned.copy()
    model_data["hari_ke"] = (model_data["tanggal"] - model_data["tanggal"].min()).dt.days
    X = model_data[["hari_ke", "harga_satuan"]]
    y = model_data["jumlah_terjual"]
    if len(model_data) < 8:
        raise ValueError("Data terlalu sedikit untuk membagi data latih dan data uji.")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    model = LinearRegression()
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    mae = mean_absolute_error(y_test, predicted)
    prediction_output = X_test.copy()
    prediction_output["aktual"] = y_test.to_numpy()
    prediction_output["prediksi"] = predicted.round(2)
    prediction_output.to_csv(OUT / "prediksi_penjualan.csv", index=False)

    # Prescriptive analytics: rekomendasi awal berdasarkan produk terlaris.
    top_product = by_product.iloc[0]
    recommendation = (
        f"Periksa ketersediaan stok untuk produk '{top_product['produk']}', "
        "karena produk ini menghasilkan pendapatan tertinggi pada data yang dianalisis."
    )
    report = (
        "LAPORAN ANALISIS PENJUALAN\n"
        "=========================\n"
        f"Jumlah baris awal: {len(raw)}\n"
        f"Jumlah baris setelah dibersihkan: {len(cleaned)}\n"
        f"Total pendapatan: Rp{cleaned['pendapatan'].sum():,.0f}\n"
        f"Produk dengan pendapatan tertinggi: {top_product['produk']}\n"
        f"MAE prediksi jumlah terjual: {mae:.2f}\n\n"
        f"Rekomendasi awal: {recommendation}\n\n"
        "Catatan: dataset simulasi; rekomendasi perlu ditinjau manusia."
    )
    (OUT / "laporan_analisis.txt").write_text(report, encoding="utf-8")

    return {
        "raw_rows": len(raw),
        "clean_rows": len(cleaned),
        "total_revenue": float(cleaned["pendapatan"].sum()),
        "top_product": str(top_product["produk"]),
        "mae": float(mae),
        "recommendation": recommendation,
    }


if __name__ == "__main__":
    result = run_analysis()
    print("=== MAKE SENSE OF DATA WITH ANALYSIS AND AI ===")
    print(f"Baris awal                 : {result['raw_rows']}")
    print(f"Baris setelah dibersihkan  : {result['clean_rows']}")
    print(f"Total pendapatan           : Rp{result['total_revenue']:,.0f}")
    print(f"Produk pendapatan tertinggi: {result['top_product']}")
    print(f"MAE prediksi               : {result['mae']:.2f}")
    print(f"Rekomendasi                : {result['recommendation']}")
    print(f"Hasil lengkap tersimpan di : {OUT}")
