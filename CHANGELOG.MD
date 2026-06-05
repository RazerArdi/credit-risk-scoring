# Changelog

All notable changes to the **Credit Risk Command Center** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-10 (Production Release)

### Added
- **Streamlit Dashboard (`app.py`)**: Fully integrated UI for Credit Analysts to perform real-time credit scoring.
- **Explainable AI Module**: Embedded SHAP Force Plots natively within the web application.
- **Dynamic Reversing Protocol**: Internal algorithms to convert machine-scaled Z-Scores back into human-readable integers (Age, Credit Amount, Duration).
- **Comprehensive Documentation**: Added `README.md`, `BUSINESS_REQUIREMENT.md`, `SYSTEM_ARCHITECTURE.md`, `MODEL_CARD.md`, and `USER_MANUAL.md` to fulfill BNSP SKKNI compliance.

### Fixed
- **Critical XGBoost & SHAP Compatibility Bug**: Implemented Monkey Patching within `app.py` to intercept and clean the `[5E-1]` string bug from XGBoost's `save_config`, preventing SHAP from crashing during real-time rendering.
- Bypassed static `matplotlib` rendering in favor of native Javascript rendering for faster dashboard load times.

---

## [0.3.0] - 2026-06-08 (Explainability & Audit Phase)

### Added
- **Notebook 04 (`04_model_interpretability_xai.ipynb`)**: Dedicated workflow for algorithmic transparency.
- SHAP Summary Plots generated to audit macro-level feature importance across the entire dataset.
- SHAP Waterfall Plots generated to justify individual rejection decisions (e.g., Audit on Customer #3).
- **Business Logic Defense**: Documented the trade-off analysis defending the selection of the Voting Ensemble over high-recall baseline models to protect bank profitability.

---

## [0.2.0] - 2026-06-05 (Modeling & Optimization Phase)

### Added
- **Notebook 03 (`03_modeling_and_evaluation.ipynb`)**: Core predictive engine development.
- Implemented Bayesian Hyperparameter Optimization utilizing the `Optuna` framework.
- Built a Voting Ensemble architecture driven by `XGBoost`.
- Model export functionality: Serialized the champion model into `champion_xgboost.pkl`.

### Changed
- Defined the optimization objective function strictly to maximize the `Recall` of the minority class (Bad Risk).

---

## [0.1.1] - 2026-06-03 (Data Sterilization & Engineering)

### Added
- **Notebook 02 (`02_data_preparation_and_smote.ipynb`)**: Feature engineering and balancing pipeline.
- Implemented `StandardScaler` for continuous financial variables.
- Implemented `OneHotEncoder` for categorical demography variables.
- **Zero Leakage Protocol**: Successfully isolated 20% of the data as a blind test set (`X_test_encoded.pkl`).

### Changed
- Mitigated the 70:30 class imbalance by applying **SMOTE** exclusively on the training matrix.

---

## [0.1.0] - 2026-06-01 (Initialization & Business Understanding)

### Added
- Initialized Git repository structure.
- **Notebook 01 (`01_business_understanding_and_eda.ipynb`)**: Initial Exploratory Data Analysis (EDA).
- Plotted class distributions, bivariate analyses, and outlier topologies using `seaborn`.
- Exported primary SQL extraction queries (`extract_credit_data.sql`).
- Created initial `DATA_DICTIONARY.md` to define raw tabular columns from the German Credit dataset.