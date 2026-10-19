# EDA Insight Log – Group 2026-DS-02

Each insight records the evidence and how it affects the prediction task. Source: `notebooks/01_eda.ipynb`.

| ID | Insight | Evidence | Implication for the task | Action (step) |
|---|---|---|---|---|
| E1 | Target is imbalanced: 11.27% yes (7.9 : 1) | fig01; §4 | Accuracy is misleading ("always no" = 88.7%) | Use PR-AUC, recall/F1, ROC-AUC; stratify; handle imbalance (Steps 3–5) |
| E2 | One row = one client contact record; no client ID; rows date-ordered 2008–2010 | §3 | Repeat clients cannot be detected | Report as limitation |
| E3 | 12 exact duplicates, 0 label conflicts | §3 | Duplicates could land in both train and test | Remove before split (D8) |
| E4 | 26% of rows contain `"unknown"`; `default` 20.9% unknown with 5.2% vs 12.9% yes-rate | §8.1 | "unknown" is informative, not random | Keep as category (D7) |
| E5 | `default = yes` only 3 rows | §8.1, §8.3 | Level too rare to learn | Merge level (Step 3) |
| E6 | `housing` and `loan` unknown on the same 990 rows | §8.1 | Shared missingness | Note; no separate fix |
| E7 | `pdays = 999` in 96.3%; 4,110 rows have 999 but `previous > 0` | §8.2 | Raw `pdays` is unreliable as a number | Contacted-before flag (D10) |
| E8 | IQR outliers in age/campaign/previous are real and predictive (age 70+: 47% yes) | fig03; §5 | Removing them deletes signal | Keep all; cap campaign for LR (D9) |
| E9 | `poutcome = success` gives 65.1% yes (Cramér's V 0.32, strongest) | fig05; §7.2 | Prior success is a key predictor and profile | Keep; highlight in profiles |
| E10 | Economic indicators are the strongest numeric predictors (AUC 0.72–0.75); lower rates → more yes | fig06; §7.3 | Important inputs | Keep (handle collinearity, E13) |
| E11 | Month: Mar/Sep/Oct/Dec at 44–51% but only 2,016 rows; May 6.4% with 13,769 rows | fig05; §7.1 | Strong but partly a time proxy | Keep; interpret with care (E14) |
| E12 | Age is U-shaped (17–25: 21%, 41–50: 8%, 61+: 43–48%); linear AUC only 0.51 | fig07; §7.4 | Non-linear effect, which LR misses | Age bins for LR; trees handle it |
| E13 | Severe multicollinearity: VIF euribor3m 64, emp.var.rate 33, nr.employed 32 | fig08; §9 | Unstable LR coefficients | Reduce/regularise for LR (D11) |
| E14 | Strong time drift: yes-rate 4.8% (2008) → 19.5% (2009) → 52.1% (2010) as volume falls | fig09; §10 | Random split may be optimistic; generalisation risk | Validation design (D12); limitation |
| E15 | Contact fatigue: 13.0% at 1 call → 3.6% at 10+ | fig07; §7.4 | Diminishing returns of repeated calls | Recommendation input; cap campaign |
| E16 | Cellular 14.7% vs telephone 5.2%; students 31.4%, retired 25.2% | fig05; §7.1 | Channel and job are useful profile features | Keep; profiles |
| E17 | `housing` (p=0.058), `loan` (p=0.58), `day_of_week` (V 0.025) weak or no signal | §7.2 | Low predictive value | Feature-selection candidates (Step 3) |
| E18 | `duration` AUC 0.818 > any pre-call feature; shortest decile 0.02% yes vs longest 46% | fig10; §11 | Confirms post-call leakage | Exclude from realistic model (D3) |
| E19 | `campaign` counts calls in this campaign incl. the last one | Data dictionary | Only partly known before contact | Decide and justify in Step 3 |
