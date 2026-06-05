# Business Requirement Document (BRD) & Project Charter

**Project Name:** Credit Risk Center (Predictive Scoring System)
**Document Owner:** Bayu Ardiyansyah (Lead Data Scientist)
**Methodology:** CRISP-DM (Cross-Industry Standard Process for Data Mining)

## 1. Latar Belakang Masalah (Business Context)

Dalam industri perbankan dan pembiayaan finansial, *Non-Performing Loan* (NPL) atau kredit macet merupakan ancaman terbesar terhadap likuiditas dan profitabilitas perusahaan.

Proses *underwriting* (penilaian kelayakan kredit) tradisional yang mengandalkan analisis manusia secara manual memiliki beberapa kelemahan kritis:

1. **Rentan Terhadap Bias Subjektif:** Keputusan dapat dipengaruhi oleh kelelahan analis atau preferensi pribadi yang tidak terstandarisasi.
2. **Skalabilitas Rendah:** Membutuhkan waktu berhari-hari untuk memproses volume pengajuan kredit yang masif.
3. **Ketidakmampuan Menemukan Pola Kompleks:** Otak manusia memiliki keterbatasan dalam mengkalkulasi korelasi persilangan dari puluhan variabel finansial secara bersamaan.

Oleh karena itu, dibutuhkan sebuah Sistem Pendukung Keputusan (*Decision Support System*) berbasis *Machine Learning* yang mampu mengisolasi nasabah berisiko tinggi secara akurat, konsisten, dan komputasional.

---

## 2. Objektif Bisnis (Business Objectives)

> **Kepatuhan Standar:** Dokumen ini merupakan pemenuhan *Fase CRISP-DM: Business Understanding* dan **KUK SKKNI: J.62DMI00.001.1 (Menentukan Objektif Bisnis)**.

Tujuan utama dari inisiatif pengembangan kecerdasan buatan ini adalah:

1. **Mitigasi Risiko Finansial (Menekan NPL):** Mengurangi persentase persetujuan terhadap nasabah yang berpotensi gagal bayar (*False Negatives*) untuk melindungi modal bank.
2. **Menjaga Profitabilitas (Ekuilibrium Portofolio):** Mencegah sistem menolak terlalu banyak nasabah yang sebenarnya berkapasitas bayar (*False Positives*), untuk memastikan target penyaluran kredit dan pendapatan bunga bank tetap tercapai.
3. **Transparansi & Kepatuhan Tata Kelola (Audit OJK):** Memastikan setiap keputusan persetujuan atau penolakan kredit dapat dijelaskan secara logis kepada nasabah dan auditor eksternal, menghilangkan praktik *Black-Box AI*.

---

## 3. Tujuan Teknis Data Science (Technical Objectives)

> **Kepatuhan Standar:** Dokumen ini merupakan pemenuhan *Fase CRISP-DM: Business Understanding* dan **KUK SKKNI: J.62DMI00.002.1 (Menentukan Tujuan Teknis Data Science)**.

Untuk menjawab objektif bisnis di atas, proyek ini menargetkan pencapaian teknis sebagai berikut:

1. **Pemodelan Prediktif Klasifikasi Biner:** Mengembangkan algoritma *Supervised Learning* untuk memprediksi kelas probabilitas: `1` (Bad Risk / Macet) dan `0` (Good Risk / Lancar).
2. **Penanganan Ketidakseimbangan Kelas (Imbalance Handling):** Mengaplikasikan rekayasa matriks secara matematis (seperti *SMOTE*) pada ruang latih untuk mencegah model hanya menebak kelas mayoritas (nasabah lancar).
3. **Optimasi Algoritma Ekuilibrium:** Mengkalibrasi *hyperparameter* pada arsitektur berbasis *Tree* (seperti XGBoost atau *Voting Ensemble*) dengan fungsi objektif (*Objective Function*) yang difokuskan pada optimalisasi metrik *Recall* tanpa menghancurkan skor akurasi agregat.
4. **Implementasi Explainable AI (XAI):** Mengintegrasikan algoritma SHAP (*SHapley Additive exPlanations*) untuk mendekonstruksi kontribusi setiap variabel demografi/finansial terhadap prediksi akhir.

---

## 4. Kriteria Keberhasilan (Success Metrics)

Proyek ini dianggap berhasil dan siap diimplementasikan (*Deployment*) jika memenuhi parameter evaluasi pengujian (*Blind Test*) berikut:

* **Discriminative Power (ROC-AUC):** Mencapai skor minimal **> 0.75**. Menunjukkan probabilitas model lebih dari 75% akurat dalam membedakan distribusi nasabah macet dan lancar.
* **Recall (Sensitivitas Risiko):** Memiliki rasio penangkapan kelas minoritas (nasabah macet) yang stabil, lebih tinggi dari model klasifikasi linier standar.
* **F1-Score Harmonik:** Mencapai titik keseimbangan yang dapat diterima antara *Precision* dan *Recall* pada dataset minoritas.
* **Zero Data Leakage:** Terbuktinya protokol sterilisasi data, di mana set data uji tidak terkontaminasi oleh rekayasa fitur data latih.

---

## 5. Ruang Lingkup dan Batasan (Scope & Limitations)

### 5.1. In-Scope (Termasuk dalam Sistem)

* Analisis data demografi (umur, pekerjaan, perumahan).
* Analisis data historis finansial (riwayat kredit, saldo rekening harian, ketersediaan tabungan).
* Rekomendasi skor akhir berupa "Disetujui" atau "Ditolak".

### 5.2. Out-of-Scope (Di Luar Sistem)

* Model ini tidak mempertimbangkan faktor makroekonomi *real-time* (seperti fluktuasi inflasi bulanan atau suku bunga acuan bank sentral).
* Model difokuskan untuk portofolio *Personal Loan* (Kredit Individu), bukan untuk audit pendanaan *Corporate / Enterprise* berskala masif.