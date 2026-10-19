# Model Card – Term-Deposit Campaign Response Model

**Group 2026-DS-02 · IT3091 Machine Learning · Version 1.0 (2026-10-10)**
Files: `models/final_model.joblib`, `results/final_model_config.json` · Built in `notebooks/07_final_model.ipynb`

## Purpose
| | |
|---|---|
| **Intended use** | Rank the bank's clients **before** a term-deposit telephone campaign, so the call centre contacts the most likely subscribers first. |
| **Users** | Marketing / campaign managers planning call lists; call-centre supervisors. |
| **Decision supported** | Who to call first, and how many calls to plan. |
| **Not intended for** | Credit or eligibility decisions; automatically excluding clients from products; any use outside telemarketing prioritisation; fully automated decisions without human review. |

## Model
| | |
|---|---|
| Algorithm | Random Forest (scikit-learn Pipeline: one-hot encoding + classifier) |
| Hyperparameters | 300 trees, max_depth 12, min_samples_leaf 10, max_features 0.3, class_weight = balanced |
| Selected because | Best test PR-AUC (0.496, significantly above XGBoost and the LR baseline), best gains, best within-year ranking in every year |
| Fallback | XGBoost (PR-AUC 0.484; faster, 1.5 MB vs 21 MB) |
| Output | Score 0–1 per client; **use as a ranking**. Scores are not calibrated probabilities (class weights shift them upwards). |

## Inputs (15)
- **Client:** job, education, default (no / not_no)
- **Contact plan:** contact (cellular/telephone), month, day_of_week, campaign (calls so far, capped at 10)
- **History:** previous, poutcome, contacted_before
- **Economic context:** emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed

**Excluded:** `duration` (only known after the call, so leakage) · `housing`, `loan` (no signal) · `age`, `marital` (data minimisation; no performance cost) · raw `pdays` (placeholder; replaced by `contacted_before`).

## Data
UCI Bank Marketing, `bank-additional-full.csv` (Moro, Cortez & Rita, 2014). Portuguese bank, May 2008 – Nov 2010, 41,188 rows
(41,176 after removing duplicates), 11.3% subscribed. SHA-256 `74adfc57…afb4d8`. Train/test split: stratified 80/20, seed 42.
The deployed model is refitted on all 41,176 rows.

## Performance (hold-out test set, 8,236 clients, 928 subscribers; model trained on training set only)
| Metric | Value | Reference |
|---|---|---|
| PR-AUC | **0.496** | random 0.113; LR baseline 0.446 |
| ROC-AUC | 0.814 | random 0.5 |
| Top-20% capture | 67.0% of subscribers | random 20% |
| Within-year ROC-AUC | 2008: 0.592 · 2009: 0.788 · 2010: 0.745 | see limitations |

## Operating rules
| Rule | How | Test result |
|---|---|---|
| **Capacity 20% (main)** | Call the top 20% of the ranked list | 1,651 calls → 622 subscribers (67.0%), conversion 37.7% (3.3× calling everyone), wasted calls 7,308 → 1,029 |
| **Max F1 (alternative)** | Call clients with score ≥ 0.638 | 1,125 calls → 536 subscribers (57.8%), conversion 47.6% (4.2×) |

## Fairness and responsible-AI findings
- At the main rule, clients aged **61+ are selected at 95–99%**, 41–50-year-olds at 14%; singles 26.8% vs married 17.6%.
  These gaps track real response differences (61+: 41–55% subscribe), and precision is similar across groups (29–56%).
- **Age is not an input, but proxies remain** (73% of 61+ clients are "retired"; they were mostly contacted in the low-rate period),
  so removing the column did not change who is selected.
- Controls required: monitor selection and outcomes by group each campaign; cap calls per client; extra care with older
  (potentially vulnerable) clients when selling financial products; human review of the call list.

## Limitations
1. **Time drift:** performance depends on economic conditions; trained-on-past → future validation gave ROC-AUC ≈ 0.55. Weak ranking when little contact history exists (2008: 0.59).
2. Data is from one Portuguese bank in 2008–2010 (financial crisis), so it may not reflect today's conditions.
3. About 55% of the model's importance comes from economic indicators, which describe *when* a campaign runs rather than *who* the client is.
4. No client ID, so repeat clients cannot be tracked; 26% of rows contain "unknown" values.
5. Even at its best, about one third of subscribers fall outside the top-20% list.

## Maintenance
Retrain before **each campaign (at least quarterly)** on the most recent data; track conversion of the called list vs the expected
37.7%; retrain immediately if conversion of the top-20% falls below ~25% or economic indicators move outside the training range.
