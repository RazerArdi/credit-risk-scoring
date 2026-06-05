# User Manual: Credit Risk Center

## 1. Pendahuluan

Selamat datang di **Credit Risk**. Dokumen ini adalah panduan operasional bagi Analis Kredit, *Customer Service*, dan staf manajerial untuk menggunakan Dasbor Sistem Prediksi Risiko Kredit Terpadu.

Sistem ini didukung oleh algoritma kecerdasan buatan (*Machine Learning*) yang dirancang untuk membantu Anda mengaudit kelayakan kredit nasabah baru secara cepat, akurat, dan transparan.

---

## 2. Cara Mengakses Sistem

Saat ini, sistem berjalan pada lingkungan lokal (*localhost*). Untuk membuka aplikasi:

1. Pastikan komputer Anda terhubung ke *server* lokal perusahaan.
2. Buka *Terminal* atau *Command Prompt*.
3. Arahkan direktori ke *root folder* proyek ini.
4. Jalankan perintah berikut:
```bash

streamlit run dashboard/app.py

```
5. Dasbor akan terbuka secara otomatis di *browser* web default Anda (biasanya di alamat `http://localhost:8501`).

---

## 3. Panduan Antarmuka & Penggunaan

Dasbor dirancang dengan antarmuka satu layar (*Single-Page Application*) agar Anda tidak perlu berpindah-pindah halaman. Ikuti langkah operasional berikut:

### Langkah 1: Memilih Nasabah (Panel Kiri / Sidebar)
* Di sebelah kiri layar, Anda akan melihat kotak **PANEL OPERASIONAL**.
* Gunakan menu *dropdown* **"ID Nasabah (Index)"** untuk memilih nasabah mana yang ingin diaudit dari antrean data.
* Begitu ID dipilih, sistem akan langsung memproses seluruh data profil nasabah tersebut secara *real-time* (kurang dari 1 detik).

### Langkah 2: Membaca Ringkasan Keputusan (Panel Atas)
Setelah nasabah dipilih, lihat tiga indikator utama di bagian atas layar:
* **Status Historis:** Menunjukkan rekam jejak asli nasabah (hanya untuk keperluan evaluasi/pengujian).
* **Probabilitas Risiko:** Angka persentase (0% - 100%) yang menunjukkan seberapa besar kemungkinan nasabah ini akan gagal bayar.
* **KEPUTUSAN:** Rekomendasi final dari sistem.
    * 🟢 **DISETUJUI:** Risiko nasabah dianggap aman (probabilitas gagal bayar di bawah ambang batas toleransi 45%).
    * 🔴 **DITOLAK:** Risiko nasabah dinilai berbahaya (probabilitas gagal bayar 45% atau lebih tinggi).

### Langkah 3: Meninjau Profil Komprehensif (Panel Tengah)
Sistem secara otomatis mengubah angka rumit/bahasa mesin (seperti *Z-Score*) menjadi angka dunia nyata yang mudah Anda pahami. Anda dapat meninjau:
* **Data Demografi:** Usia aktual nasabah dan klasifikasi kelompok produktif.
* **Profil Pinjaman:** Plafon kredit (jumlah uang yang dipinjam) dan Tenor (lama bulan cicilan).
* **Aset & Likuiditas:** Status pekerjaan, saldo rekening harian, dan ketersediaan tabungan.
* **Riwayat Historis:** Rekam jejak kredit di tempat lain dan tujuan penggunaan dana (misal: Modal Usaha vs Konsumtif).

---

## 4. Membaca Radar Transparansi Algoritma (SHAP Force Plot)

Jika nasabah bertanya, *"Mengapa pengajuan kredit saya ditolak?"*, Anda tidak perlu bingung. Geser ke bagian paling bawah layar untuk melihat **Radar Transparansi Algoritma**.

Grafik ini bekerja seperti mesin rontgen (*X-Ray*) yang memperlihatkan isi pikiran algoritma.
* **Arahkan Kursor Anda (Hover):** Letakkan kursor *mouse* Anda di atas area grafik berwarna untuk melihat detail angka secara spesifik.
* **Area Merah (Risiko Tinggi):** Fitur atau data nasabah yang mendorong sistem untuk **MENOLAK** kredit (meningkatkan probabilitas gagal bayar). *Contoh: Saldo rekening minus, atau pernah menunggak kredit sebelumnya.*
* **Area Biru (Risiko Rendah):** Fitur yang mendorong sistem untuk **MENYETUJUI** kredit. *Contoh: Usia sangat matang, atau memiliki pekerjaan tetap di sektor prioritas.*
* **Garis Pertemuan:** Titik di mana warna Merah dan Biru bertemu adalah skor akhir dari probabilitas gagal bayar nasabah tersebut.

---

## 5. Pertanyaan Umum (FAQ) & Batasan Sistem

**T: Apakah saya wajib mengikuti keputusan sistem secara mutlak?**
*J: Tidak. Sistem ini bertindak sebagai asisten (Decision Support System). Jika keputusan sistem adalah "DITOLAK", namun Anda memiliki pertimbangan/data eksternal lain di luar sistem, wewenang final (*override*) tetap berada di tangan Manajer Kredit.*

**T: Mengapa umur atau jumlah pinjaman tampil sedikit berbeda dari KTP nasabah?**
*J: Jika data mentah tidak tersedia di server, sistem akan menggunakan mesin kalkulasi mundur (Reversing Z-Score) untuk memperkirakan nilai riil, sehingga mungkin ada pembulatan angka (toleransi margin error).*

**T: Apa yang harus saya lakukan jika dasbor terhenti / layar putih (*blank*)?**
*J: Hal ini dapat terjadi jika ada gangguan pada jaringan ke server lokal. Silakan segarkan (Refresh / tekan F5) halaman browser Anda. Seluruh data aman dan tidak akan hilang.*

---
**Hak Cipta & Dukungan Teknis**
* Dikembangkan oleh: @Bayu Ardiyansyah
* Kontak Bantuan IT: bayuardi30@outlook.com