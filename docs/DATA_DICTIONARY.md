# KAMUS DATA (DATA DICTIONARY)
**Dataset:** Statlog (German Credit Data)
**Deskripsi:** Pemetaan 20 atribut prediktor (13 kualitatif, 7 numerik) yang digunakan untuk pemodelan risiko kredit.

| No | Atribut Asli (UCI) | Nama Kolom Sistem (Python) | Tipe Data | Deskripsi & Pemetaan Kode (Mapping) |
|:---|:---|:---|:---|:---|
| 1 | Status of existing checking account | `checking_account_status` | Kualitatif | **A11:** < 0 DM <br> **A12:** 0 <= ... < 200 DM <br> **A13:** >= 200 DM / salary assignments <br> **A14:** no checking account |
| 2 | Duration in month | `duration_months` | Numerik | Durasi pinjaman dalam hitungan bulan. |
| 3 | Credit history | `credit_history` | Kualitatif | **A30:** no credits taken/all paid duly <br> **A31:** all credits at bank paid duly <br> **A32:** existing credits paid duly till now <br> **A33:** delay in paying off in the past <br> **A34:** critical account/other credits |
| 4 | Purpose | `purpose` | Kualitatif | **A40:** car (new) <br> **A41:** car (used) <br> **A42:** furniture/equipment <br> **A43:** radio/television <br> **A44:** domestic appliances <br> **A45:** repairs <br> **A46:** education <br> **A47:** vacation <br> **A48:** retraining <br> **A49:** business <br> **A410:** others |
| 5 | Credit amount | `credit_amount` | Numerik | Total nominal kredit yang diajukan (dalam DM). |
| 6 | Savings account/bonds | `savings_account_status` | Kualitatif | **A61:** < 100 DM <br> **A62:** 100 <= ... < 500 DM <br> **A63:** 500 <= ... < 1000 DM <br> **A64:** >= 1000 DM <br> **A65:** unknown/ no savings account |
| 7 | Present employment since | `employment_duration` | Kualitatif | **A71:** unemployed <br> **A72:** < 1 year <br> **A73:** 1 <= ... < 4 years <br> **A74:** 4 <= ... < 7 years <br> **A75:** >= 7 years |
| 8 | Installment rate | `installment_rate` | Numerik | Persentase cicilan terhadap pendapatan (*disposable income*). |
| 9 | Personal status and sex | `personal_status_sex` | Kualitatif | **A91:** male : divorced/separated <br> **A92:** female : divorced/separated/married <br> **A93:** male : single <br> **A94:** male : married/widowed <br> **A95:** female : single |
| 10 | Other debtors / guarantors | `other_debtors_guarantors` | Kualitatif | **A101:** none <br> **A102:** co-applicant <br> **A103:** guarantor |
| 11 | Present residence since | `present_residence_since` | Numerik | Lama menetap di tempat tinggal saat ini (tahun). |
| 12 | Property | `property` | Kualitatif | **A121:** real estate <br> **A122:** building society savings / life insurance <br> **A123:** car or other <br> **A124:** unknown / no property |
| 13 | Age in years | `age_years` | Numerik | Usia pemohon kredit (tahun). |
| 14 | Other installment plans | `other_installment_plans` | Kualitatif | **A141:** bank <br> **A142:** stores <br> **A143:** none |
| 15 | Housing | `housing` | Kualitatif | **A151:** rent <br> **A152:** own <br> **A153:** for free |
| 16 | Number of existing credits | `existing_credits` | Numerik | Jumlah kredit yang sedang berjalan di bank ini. |
| 17 | Job | `job` | Kualitatif | **A171:** unemployed/ unskilled - non-resident <br> **A172:** unskilled - resident <br> **A173:** skilled employee / official <br> **A174:** management/ self-employed / officer |
| 18 | Number of people liable | `dependents` | Numerik | Jumlah tanggungan keluarga. |
| 19 | Telephone | `telephone` | Kualitatif | **A191:** none <br> **A192:** yes, registered under customer's name |
| 20 | Foreign worker | `foreign_worker` | Kualitatif | **A201:** yes <br> **A202:** no |