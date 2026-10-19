# Preprocessing / Feature Log – Group 2026-DS-02

Source: `notebooks/02_preprocessing.ipynb` · Code: `src/preprocessing.py`

| # | Issue (EDA ref) | Options considered | Action taken | Justification | Effect / evidence | Stage |
|---|---|---|---|---|---|---|
| P1 | 12 exact duplicates (E3) | keep; remove | Removed | Avoid identical rows in train and test | 41,188 → 41,176 rows; yes-rate unchanged | Row-level |
| P2 | `duration` post-call leakage (E18) | keep; drop; benchmark only | Dropped (benchmark in modelling) | Not known before the call | 20 columns remain | Row-level |
| P3 | `pdays = 999` placeholder, inconsistent (E7) | raw; NaN + impute; flag | `contacted_before` = previous > 0; `pdays` dropped | 96% placeholder; flag consistent with `poutcome` | Exact match with `poutcome`; yes 8.83% vs 26.65% | Row-level |
| P4 | `default = yes` only 3 rows (E5) | keep; drop rows; merge | Merged → `no` / `not_no` | Too rare to learn | 32,577 / 8,599 | Row-level |
| P5 | `education = illiterate` only 18 rows | keep; merge | Merged into `basic.4y` | Too rare; closest level | 7 levels | Row-level |
| P6 | `education` encoding | ordinal; one-hot | One-hot | Yes-rate not ordered by level; "unknown" has no order | – | Fitted |
| P7 | `"unknown"` in 26% of rows (E4) | delete; impute; own category | Kept as own category | Informative (default unknown: 5.2% vs 12.9%) | No rows lost | – |
| P8 | Outliers age/campaign/previous (E8) | remove; cap; keep | Kept all; `campaign` capped at 10 | Real and predictive; cap protects LR | 869 rows capped (yes 3.11%) | Row-level |
| P9 | `campaign` only partly known pre-call (E19) | drop; keep | Kept | Known at each new call attempt | – | – |
| P10 | Hold-out split | random; time-based | Stratified random 80/20, seed 42 (time check in Step 4) | Decisions below must use train only | Train 32,940 / test 8,236, both 11.27% yes | Split |
| P11 | Weak features (E17) | keep; drop | Dropped `housing`, `loan`; kept `day_of_week` | Not significant on train; no CV loss when dropped; day_of_week removal hurt both models | PR-AUC LR 0.4365→0.4368, RF 0.4641→0.4646 | Selection (train) |
| P12 | Multicollinearity (E13) | keep all; drop; regularise | Linear: keep `euribor3m`, drop `emp.var.rate`, `nr.employed`; trees keep all | VIF > 30 makes LR coefficients unstable | Max VIF 64.6 → 4.7 | Selection (train) |
| P13 | Non-linear age (E12) | raw; bins | Linear: 7 age groups (one-hot); trees: raw age | LR cannot learn a U-shape from one linear term | – | Fitted |
| P14 | Categorical encoding | label; ordinal; one-hot | One-hot, `handle_unknown="ignore"` | Nominal categories; safe for unseen levels | Linear 58 / tree 54 columns | Fitted |
| P15 | Scaling | none; standard; min-max | StandardScaler for LR only | LR is scale-sensitive; trees are not | Mean 0 / std 1 on train | Fitted |
| P16 | Class imbalance 7.88 : 1 (E1) | none; undersample; SMOTE; class weights; threshold | Class weights (main); SMOTE compared; threshold tuned later | No synthetic data, no leakage risk | Weights 0.563 / 4.438; `scale_pos_weight` 7.88 | In model pipeline |
