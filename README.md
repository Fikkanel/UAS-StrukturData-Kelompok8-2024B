# 🚗 Algoritma Dijkstra & Traveling Salesman Problem (TSP) di Jawa Timur

Sebuah aplikasi Python interaktif untuk mencari rute tercepat antar kota di Jawa Timur menggunakan **Algoritma Dijkstra** dan **Brute Force Traveling Salesman Problem (TSP)**. Proyek ini juga menampilkan output dengan animasi dan warna untuk memperjelas visualisasi hasil.

## 📌 Fitur Utama

- 🔍 Cari rute tercepat dari kota asal ke kota tujuan dengan **Dijkstra**
- 🌍 Cari rute optimal mengunjungi semua kota (tanpa kembali) menggunakan **Brute Force TSP**
- 🎨 Tampilan terminal yang menarik menggunakan **Colorama**
- 📋 Menampilkan rincian jarak, rute, dan animasi panah perjalanan
- 🏙️ Dukungan untuk 10 kota di Jawa Timur

## 🏙️ Kota yang Didukung

- Surabaya
- Sidoarjo
- Gresik
- Lamongan
- Mojokerto
- Pasuruan
- Malang
- Probolinggo
- Bangkalan
- Jombang

## 🛠️ Instalasi

1. **Clone repositori:**
   ```bash
   git clone https://github.com/username/nama-repo.git
   cd nama-repo
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Cara Menjalankan
  ```bash
  python gpsfinal2.py
  ```

## Requirements
   ``` bash
   colorama==0.4.6
   networkx==3.3
   matplotlib==3.8.4
   ```

## 📂 Struktur Proyek
  ```bash
├── tsp_dijkstra.py       # File utama
├── README.md             # Dokumentasi proyek
└── requirements.txt      # Daftar dependencies
```

## 🧠 Algoritma yang Digunakan
1. Dijkstra Algorithm untuk pencarian jarak terpendek antar dua titik
2. Brute Force TSP: mencoba semua kemungkinan rute untuk mencari jalur optimal tanpa kembali ke awal
