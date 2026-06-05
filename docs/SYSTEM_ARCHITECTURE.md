# System Architecture: Credit Risk Command Center

## 1. Executive Overview

Dokumen ini menguraikan arsitektur sistem *end-to-end* untuk ekosistem **Credit Risk Scoring**. Sistem ini dirancang untuk memproses data mentah nasabah, mengaplikasikan transformasi matematis, mengeksekusi prediksi risiko gagal bayar (*Non-Performing Loan*) menggunakan *Champion Model*, dan menyajikan hasilnya ke dalam antarmuka interaktif yang dilengkapi dengan kapabilitas *Explainable AI (XAI)*.

Arsitektur ini mematuhi metodologi **CRISP-DM** dan prinsip operasional **MLOps** (*Machine Learning Operations*) dasar.

---

## 2. High-Level Architecture Flow

Alur data direpresentasikan dalam topologi spasial berikut:

```text
[Data Mentah (CSV)] 
       │
       ▼
[Fase Pra-Pemrosesan] ──► (Sterilisasi Uji: Zero Leakage) ──► [Data Uji (Pickle)]
       │
       ▼
(Z-Score & Enkoding) ──► (Injeksi SMOTE) ──► [Matriks Latih Seimbang]
                                                   │
                                                   ▼
                                         [Pelatihan Mesin]
                                         (Optuna + XGBoost / Ensemble)
                                                   │
                                                   ▼
[Antarmuka End-User] ◄── (Integrasi Web) ◄── [Ekspor Model (Pickle)]
       │
       ▼
[Modul XAI (SHAP)] ──► (Interpretasi Keputusan Real-Time)

```

---

## 3. Komponen Pipeline (Pipeline Components)

Sistem ini dipecah menjadi 4 lapisan utama (*Layers*):

### 3.1. Data Storage & Preprocessing Layer

Lapisan ini bertugas mengubah data tabular mentah menjadi matriks numerik yang dapat diproses oleh mesin komputasi.

* **Standardisasi Skala:** Menggunakan `StandardScaler` untuk memitigasi distorsi magnitudo finansial (misal: besaran kredit dalam ribuan DM tidak akan mendominasi umur yang hanya puluhan tahun).
* **Enkoding Fitur:** Representasi kategori teks diubah menjadi vektor biner melalui `OneHotEncoder` / `pd.get_dummies`.
* **Protokol Zero Data Leakage:** Matriks dipisah menjadi Data Latih (80%) dan Data Uji (20%) *sebelum* penanganan ketidakseimbangan kelas.
* **Penyeimbangan Kelas (Oversampling):** Menggunakan **SMOTE** secara eksklusif pada Data Latih untuk mencapai ekuilibrium (rasio 50:50 antara nasabah lancar dan macet).
* **Artefak Output:** `X_test_encoded.pkl`, `y_test.pkl`, `X_test_raw.pkl`.

### 3.2. Machine Learning Layer (Core Engine)

Lapisan ini adalah otak pengambilan keputusan prediktif.

* **Arsitektur Model:** Menggunakan pendekatan kombinasi (*Voting Ensemble*) dengan **XGBoost** sebagai tulang punggung utama.
* **Sistem Optimasi:** Kalibrasi *hyperparameter* dilakukan menggunakan arsitektur Bayesian (*Optuna*) dengan fungsi objektif yang difokuskan pada pemaksimalan nilai *Recall* kelas minoritas.
* **Artefak Output:** `champion_xgboost.pkl`.

### 3.3. Interpretability Layer (XAI Module)

Modul ini bertugas mendekonstruksi *Black-Box* untuk memenuhi standar kepatuhan tata kelola (OJK).

* **Mesin Dekonstruksi:** Menggunakan *SHapley Additive exPlanations (SHAP)* `TreeExplainer`.
* **Kalkulasi Real-Time:** Menghitung bobot persentase dari setiap fitur demografi dan finansial yang memengaruhi keputusan prediksi secara waktu nyata.
* **Kompatibilitas:** Memuat implementasi *Monkey Patching* pada fungsi konfigurasi internal XGBoost guna mengatasi konflik *parsing* memori saat integrasi dengan pustaka SHAP.

### 3.4. Application & Deployment Layer

Lapisan presentasi bagi pengguna akhir (*Analis Kredit / Eksekutif*).

* **Framework Web:** *Streamlit* digunakan sebagai fondasi antarmuka karena efisiensi respons dan skalabilitas eksekusi model *backend*.
* **Reversing Data:** Sistem memiliki fungsi *internal routing* untuk mengembalikan nilai *Z-Score* menjadi nilai riil (usia, tenor, plafon kredit) agar dapat dibaca secara logis oleh manusia.
* **Visualisasi JS:** Merender *SHAP Force Plot* menggunakan skrip Javascript interaktif untuk meminimalisir beban *rendering* gambar statis (*bypass matplotlib*).

---

## 4. Technology Stack

* **Bahasa Pemrograman:** Python 3.10+
* **Manipulasi Matriks/Data:** `pandas`, `numpy`
* **Machine Learning Framework:** `scikit-learn`, `xgboost`, `imbalanced-learn`
* **Hyperparameter Optimizer:** `optuna`
* **Algoritma Audit (XAI):** `shap`
* **Deployment/UI Framework:** `streamlit`
* **Serialisasi Objek:** `pickle`

---

## 5. Security & Data Integrity

1. **Isolasi Memori Uji:** Model divalidasi silang menggunakan *Stratified 5-Fold CV* yang memblokir infiltrasi data target ke dalam data latih.
2. **Offline-First:** Dasbor operasional dirancang untuk membaca artefak `pickle` secara lokal tanpa memerlukan panggilan API (*Application Programming Interface*) ke pihak ketiga, menjaga privasi data demografi nasabah (*PII - Personally Identifiable Information*).