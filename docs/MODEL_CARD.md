# Model Card: Credit Risk Scoring (Champion Model)

## 1. Model Details

### 1.1 Basic Information

* **Model Name:** `champion_xgboost.pkl` (Arsitektur Voting Ensemble teroptimasi)
* **Version:** 1.0.0
* **Date of Release:** [Tanggal Deployment Anda, misal: 10 Juni 2026]
* **Developed By:** Bayu Ardiyansyah (Lead Data Scientist)
* **Primary Frameworks:** `scikit-learn`, `xgboost`, `optuna`, `shap`
* **Model Type:** Supervised Machine Learning (Binary Classification)
* **Target Variable:** Gagal Bayar / Non-Performing Loan (`1` = Gagal Bayar/Bad, `0` = Lancar/Good)

### 1.2 Architecture Overview

Arsitektur akhir (Champion Model) merupakan integrasi berjenjang (*pipeline*) yang terdiri dari:

1. **Preprocessor:** Standardisasi fitur numerik menggunakan Z-Score (`StandardScaler`) dan enkoding kategori (`OneHotEncoder`).
2. **Imbalance Mitigation:** Penyeimbangan kelas menggunakan teknik sintetis SMOTE secara eksklusif pada set data latih (*Zero Data Leakage*).
3. **Core Classifier:** Algoritma ekuilibrium terpilih, didukung oleh mesin XGBoost (*Extreme Gradient Boosting*) yang dikalibrasi.
4. **Optimizer:** Pencarian *hyperparameter* menggunakan arsitektur Bayesian (*Optuna*) dengan target metrik *Recall*.

---

## 2. Intended Use & Business Value

### 2.1 Primary Use Case

Model ini dirancang sebagai sistem pakar penunjang keputusan (*Decision Support System*) untuk Analis Kredit dan *Customer Service* di industri perbankan. Model bertugas mengkalkulasi probabilitas kelancaran kredit berdasarkan data demografi, riwayat historis, dan status aset nasabah baru.

### 2.2 Out-of-Scope Uses (Batasan)

* Model **tidak boleh** digunakan secara otonom (tanpa validasi manusia/ *human-in-the-loop*) untuk menolak pengajuan kredit secara final.
* Model ini dikalibrasi pada data pinjaman individu (Personal Loan). Tidak diuji dan tidak direkomendasikan untuk audit pinjaman korporat sekala besar (*Corporate/Commercial Loans*).
* Model tidak mempertimbangkan makroekonomi *real-time* (seperti inflasi atau suku bunga acuan terkini) dalam kalkulasi fiturnya.

### 2.3 Business Impact

Fokus utama arsitektur ini adalah memitigasi risiko kebocoran NPL (*Non-Performing Loan*) melalui penekanan metrik *False Negatives* (nasabah macet yang diprediksi lancar), sekaligus mengamankan volume penyaluran kredit sehat melalui penjagaan metrik *ROC-AUC*.

---

## 3. Data Integrity & Preprocessing

### 3.1 Training & Testing Split

* **Total Data Awal:** 1.000 observasi (700 Lancar, 300 Macet).
* **Data Uji (Test Set / Unseen Data):** 20% (200 observasi - 140 Lancar, 60 Macet).
* **Sterilisasi:** Data uji disegel dan dipisahkan sebelum injeksi SMOTE untuk menjamin pengujian tersimulasi secara murni (mencegah *Data Leakage*).

### 3.2 Feature Engineering

* Tidak ada penghapusan baris data.
* Konversi metrik nilai mata uang ke dalam distribusi seragam (*Z-Score*).
* Fitur utama (*Feature Importance*) yang menggerakkan prediksi model: `checking_account_status`, `duration_months`, `credit_amount`, `credit_history`.

---

## 4. Performance Metrics & Audit

### 4.1 Evaluation on Unseen Data (200 Blind Test)

Berdasarkan pengujian silang terstratifikasi pada matriks *Test Set*, model mencetak rekam jejak performa sebagai berikut:

* **ROC-AUC Score:** 0.77 (Daya pisah agregat / Probabilitas ketepatan deteksi).
* **Recall (Kelas Minoritas):** 0.57 (Berhasil menangkap 34 dari 60 potensi gagal bayar riil).
* **Precision (Kelas Minoritas):** 0.63.
* **F1-Score (Kelas Minoritas):** 0.60 (Keseimbangan harmonik).

### 4.2 Trade-Off Analysis (Kenapa Baseline Ditolak?)

* Model regresi logistik (*Baseline*) mampu mencapai Recall yang lebih tinggi (0.68).
* **Justifikasi Bisnis:** Model *Baseline* ditolak secara teknis karena rasio *False Positives* yang tidak terkontrol (agresivitas menuduh nasabah lancar sebagai nasabah gagal bayar). Hal ini bertentangan dengan *business objective* untuk mempertahankan perputaran modal bank. Champion model dipilih karena menjaga ekuilibrium akurasi operasional (77%).

---

## 5. Explainable AI (XAI) & Compliance

Sistem ini didesain agar tidak beroperasi sebagai mekanisme *Black-Box*.

* **Audit Skala Makro (Global):** Memanfaatkan algoritma *SHAP (SHapley Additive exPlanations)* untuk memetakan dominasi fitur dalam keputusan prediktif (Visual: SHAP Summary/Bar Plot).
* **Audit Skala Mikro (Lokal):** Dasbor operasional menggunakan *SHAP Force Plot* yang membongkar logika mesin per individu secara waktu nyata (*real-time*). Keputusan penolakan kredit dapat dijustifikasi secara matematis per nasabah, memenuhi standar perlindungan konsumen dan audit Otoritas Jasa Keuangan (OJK).

---

## 6. Recommendations & Threshold Calibrations

* **Ambang Batas Default:** Sistem diekspor menggunakan ambang batas kalkulasi `0.45` (45% probabilitas untuk klasifikasi gagal bayar).
* **Threshold Tuning (Kondisi Makro):** Jika kondisi makroekonomi menuntut bank untuk memperketat likuiditas, manajemen disarankan untuk mengkalibrasi ambang batas klasifikasi menjadi `0.40` atau `0.35` untuk meningkatkan mitigasi risiko (Recall), tanpa perlu melakukan pelatihan ulang model (Retraining).