/*
===============================================================================
ARTEFAK EKSTRAKSI DATA WAREHOUSE - CREDIT RISK SCORING
===============================================================================
Pemenuhan SKKNI   : J.62DMI00.007.1 (Menentukan Objek Data)
Target Eksekusi   : RDBMS PostgreSQL / Google BigQuery
Modul             : Risk & Compliance Analytics

Deskripsi:
Kueri ini dirancang untuk mengekstraksi dan mendenormalisasi entitas data
nasabah dari tiga tabel relasional utama: Profil Demografi, Riwayat Finansial,
dan Aplikasi Pinjaman (Origination). Luaran dari kueri ini menghasilkan
satu flat-table (20 fitur + 1 label target) yang siap diekspor
menjadi format .csv untuk diinjeksi ke dalam pipeline Machine Learning.

Teknik: Common Table Expressions (CTE) & Inner Joins
===============================================================================
*/

WITH CustomerDemographics AS (
    -- Mengekstraksi profil demografi dan status sosial ekonomi nasabah
    SELECT 
        customer_id,
        personal_status_and_sex AS status_sex,
        age_in_years AS age,
        housing,
        job,
        number_of_people_liable_to_provide_maintenance AS dependants,
        telephone,
        foreign_worker
    FROM 
        core_banking.dim_customers
),

FinancialHistory AS (
    -- Mengekstraksi riwayat kepatuhan dan status likuiditas aset
    SELECT 
        customer_id,
        status_of_existing_checking_account AS checking_status,
        credit_history,
        savings_account_and_bonds AS savings_status,
        present_employment_since AS employment_duration
    FROM 
        core_banking.fact_account_history
),

LoanOrigination AS (
    -- Mengekstraksi detail pengajuan kredit saat ini beserta label risiko historis
    SELECT 
        loan_id,
        customer_id,
        duration_in_month AS duration,
        purpose,
        credit_amount,
        installment_rate_in_percentage_of_disposable_income AS installment_rate,
        present_residence_since AS residence_duration,
        property,
        other_installment_plans,
        number_of_existing_credits_at_this_bank AS existing_credits,
        target_risk_label -- 1 = Good Credit, 2 = Bad Credit (Default)
    FROM 
        loan_origination.fact_applications
    WHERE 
        application_status = 'CLOSED' -- Hanya mengambil data historis yang sudah selesai
)

-- Integrasi Data Mart (Denormalisasi Final)
SELECT 
    fh.checking_status,
    lo.duration,
    fh.credit_history,
    lo.purpose,
    lo.credit_amount,
    fh.savings_status,
    fh.employment_duration,
    lo.installment_rate,
    cd.status_sex,
    -- Fitur 'other_debtors_guarantors' diasumsikan menempel pada tabel origination
    lo.other_installment_plans,
    lo.residence_duration,
    lo.property,
    cd.age,
    lo.other_installment_plans,
    cd.housing,
    lo.existing_credits,
    cd.job,
    cd.dependants,
    cd.telephone,
    cd.foreign_worker,
    lo.target_risk_label AS credit_risk
FROM 
    CustomerDemographics cd
INNER JOIN 
    FinancialHistory fh ON cd.customer_id = fh.customer_id
INNER JOIN 
    LoanOrigination lo ON cd.customer_id = lo.customer_id;