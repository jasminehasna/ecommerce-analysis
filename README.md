# Proyek Analisis Data: Brazilian E-Commerce Public Dataset

## Struktur Folder

- `notebook_final.ipynb`: notebook analisis final
- `dashboard.py`: dashboard Streamlit final
- `main_data.csv`: dataset hasil pembersihan yang dipakai dashboard
- `final url.txt`: file URL dashboard
- `README.md`: dokumentasi proyek
- `requirements.txt`: daftar dependensi

## Pertanyaan Bisnis

1. Berapa persen pelanggan yang masuk ke dalam masing-masing segmen RFM pada transaksi delivered selama periode 15 September 2016 sampai 29 Agustus 2018, dan segmen mana yang paling perlu diprioritaskan untuk strategi retensi pelanggan?
2. Kategori produk apa saja yang masuk 10 besar berdasarkan jumlah order delivered selama periode 15 September 2016 sampai 29 Agustus 2018, dan bagaimana tren jumlah order bulanannya untuk menentukan prioritas stok serta promosi?

## Insight Utama

- Segmen `Potential Loyalists` menjadi segmen terbesar, sehingga aktivasi pelanggan menjadi fokus utama.
- Segmen `Loyal Customers` dan `Champions` perlu dijaga melalui strategi retensi dan loyalty.
- Kategori `bed_bath_table`, `health_beauty`, dan `sports_leisure` menjadi kategori teratas berdasarkan order delivered.

## Cara Menjalankan Dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## URL Dashboard

https://ecommerce-analysis-performance.streamlit.app/
