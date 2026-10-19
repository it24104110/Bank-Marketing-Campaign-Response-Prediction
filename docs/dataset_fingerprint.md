# Dataset Fingerprint

| Item | Value |
|---|---|
| Dataset | Bank Marketing (with social/economic context) |
| Source | UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/222/bank+marketing |
| File used | `bank-additional-full.csv` (from `bank-additional.zip` inside the UCI download) |
| Project location | `data/raw/bank-additional-full.csv` |
| Shape | 41,188 rows × 21 columns (20 inputs + target `y`) |
| Separator | `;` |
| Time span | May 2008 – November 2010 (rows ordered by date) |
| Target balance | `yes` = 4,640 (11.27%), `no` = 36,548 (88.73%) |
| SHA-256 | `74adfc578bf77a7ff4bb1ba4a9f8709d9e3c6907342959c2c8416847e0afb4d8` |
| Documentation | `data/raw/bank-additional-names.txt` (SHA-256 `10045462a4c026f858dffa159370c4270510230c1fc63c6c91ca51bba4b3df26`) |
| Date obtained | 2026-10-07 |

## Citation
S. Moro, P. Cortez and P. Rita. *A Data-Driven Approach to Predict the Success of Bank Telemarketing.*
Decision Support Systems, 62:22–31, 2014. https://doi.org/10.1016/j.dss.2014.03.001

## How to verify
Run `notebooks/00_setup_and_data_loading.ipynb`; it recomputes the hash and checks it against `src/config.py`.
Or in a terminal: `certutil -hashfile data\raw\bank-additional-full.csv SHA256` (Windows) / `sha256sum data/raw/bank-additional-full.csv`.

## Files in the UCI download that are NOT used
| File | Reason |
|---|---|
| `bank-additional.csv` | Random 10% sample of the full file; intended only for slow algorithms. |
| `bank-full.csv` | Older version without the 5 economic indicators. |
| `bank.csv` | 10% sample of the older version. |
| `.Rhistory`, `.DS_Store`, `__MACOSX/` | macOS/R system files from the authors' zip; contain no data. |
