# Marketing Profiles – Secondary Lens (Group 2026-DS-02)

Evidence combines EDA (`01_eda`), model interpretation (`06_interpretation`: SHAP, permutation importance, LR odds ratios) and
rule-based segments **trained on the training set and validated on the test set**. Overall yes-rate: 11.3%.

## High-response profiles

| Profile | Evidence | Test yes-rate | Lift |
|---|---|---|---|
| **Previous campaign success, contacted more than once before** | Segment S1 (client features) | 72.0% | 6.4× |
| **Previous campaign success, first call in this campaign** | Segment S2 | 65.9% | 5.9× |
| **Previous success during a low-employment period** (nr.employed ≤ 5,013) | Segment S1 (all features) | 76.7% | 6.8× |
| **Mobile-phone clients aged over 60** (no previous success) | Segment S4 | 41.2% | 3.7× |
| **Any client reached by mobile in a low-employment period** | Segment S3 (all features) | 41.8% | 3.7× |
| Students and retired clients | EDA 31.4% / 25.2%; top-10% over-representation 5.8× / 4.4×; SHAP positive | – | 2.2–2.8× |

## Low-response profiles

| Profile | Evidence | Test yes-rate | Lift |
|---|---|---|---|
| **Landline clients under 58 without previous success** (largest low group, 2,897 test clients) | Segment S7 (client features) | 4.8% | 0.43× |
| Clients called in "normal economy" periods (high employment, normal confidence) | Segments S7–S8 (all features), 81% of test clients | 3.5–6.5% | 0.3–0.6× |
| Clients already called 5+ times in the same campaign | EDA (≤ 7.5%); SHAP negative from 5 calls | – | < 0.7× |
| Clients whose default status is not confirmed "no" | EDA 5.2%; SHAP and LR negative | – | 0.46× |
| Previous campaign failure (in normal periods) | Segment S6 (all features) | 9.2% | 0.82× |

## Key drivers (direction)
| Driver | Effect |
|---|---|
| Low Euribor / low employment (economic context) | Strongly ↑ (55% of RF importance) |
| Previous campaign success | Strongly ↑ (LR odds × 2.04) |
| Mobile vs landline | ↑ mobile, ↓ landline |
| Month | Mar/Sep/Oct/Dec ↑, May ↓ (odds × 0.50) |
| Age | U-shape: under 30 and over 60 ↑, 35–55 ↓ |
| Number of calls this campaign | 5+ calls ↓ |

## Caution
- Much of the "month" and "economy" effect reflects **when** campaigns ran (2008–2010 financial crisis), not stable customer traits.
  Profiles based on contact history and channel are more transferable to future campaigns.
- Over-60 clients are selected very often; see the responsible-AI section (`docs/interpretation_findings.txt` §6) before acting on this profile.
