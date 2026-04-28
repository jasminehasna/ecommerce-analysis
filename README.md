# Proyek Analisis Data: Brazilian E-Commerce Public Dataset

## Struktur Folder

- `notebook_final.ipynb`: notebook analisis final
- `dashboard.py`: dashboard Streamlit final
- `main_data.csv`: dataset hasil pembersihan yang dipakai dashboard
- `final url.txt`: file URL dashboard
- `README.md`: dokumentasi proyek
- `requirements.txt`: daftar dependensi

## Pertanyaan Bisnis

1. Bagaimana distribusi segmen pelanggan berdasarkan analisis RFM, dan segmen mana yang paling mendominasi?
2. Kategori produk apa yang paling banyak dibeli dan bagaimana tren penjualan bulanannya?

## Insight Utama

- Segmen `Lost` dan `Potential Loyalists` mendominasi komposisi pelanggan, sehingga retensi dan aktivasi ulang menjadi fokus utama.
- Pelanggan `Champions` memiliki nilai belanja tertinggi dan layak diprioritaskan untuk strategi loyalty.
- Beberapa kategori produk konsisten mendominasi order, sementara tren bulanan menunjukkan periode permintaan yang berubah sepanjang waktu.

## Cara Menjalankan Dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```
