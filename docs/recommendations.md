# Recommendations, Limitations and Stakeholder Value – Group 2026-DS-02

**Stakeholder:** the bank's marketing / campaign managers and call-centre team.
**Decision:** which clients to call first in a term-deposit campaign, and which client characteristics are linked to subscribing.
All figures are from the hold-out test set (8,236 clients, 928 subscribers) unless stated otherwise.

---

## 1. Stakeholder value

| | Call everyone (current practice) | **Model: call top 20% (main)** | Model: Max F1 (alternative) |
|---|---|---|---|
| Calls | 8,236 | **1,651 (−80%)** | 1,125 (−86%) |
| Subscribers reached | 928 | **622 (67%)** | 536 (58%) |
| Conversion per call | 11.3% | **37.7% (3.3×)** | 47.6% (4.2×) |
| Wasted calls | 7,308 | **1,029 (−86%)** | 589 (−92%) |

The bank can reach **two thirds of its subscribers with one fifth of the calls**. That frees about 6,600 calls of call-centre time
per 8,000 clients, and spares thousands of uninterested clients an unwanted call.

---

## 2. Recommendations

| # | Recommendation | Evidence |
|---|---|---|
| **R1** | **Rank every campaign list with the model and call the top 20% first** (main rule). Extend down the list only if capacity remains. | Top 20% → 67% of subscribers, 3.3× conversion (07 §5); gains curve flattens after ~15–20% (05 §4) |
| **R2** | When staff is short or calls are expensive, use the **Max F1 rule** (score ≥ 0.638): fewer calls, higher hit rate. | 1,125 calls, 47.6% conversion (07 §5) |
| **R3** | **Prioritise clients who said yes to a previous campaign**, and keep complete contact-history records. | 65–77% subscribe (06 §5); `poutcome` = strongest client signal (odds × 2.04); ranking weakest in 2008 when history was missing (0.59 vs 0.79) |
| **R4** | **Prefer mobile numbers**; de-prioritise landline-only clients under 58 and try to obtain their mobile numbers. | Cellular 14.7% vs telephone 5.2% (EDA); landline < 58: 4.8% yes, largest low group (06 §5) |
| **R5** | **Cap calls at about 4 per client per campaign.** | Yes-rate 13.0% at 1 call → 3.6% at 10+ (EDA); SHAP clearly negative from 5 calls (06 §3) |
| **R6** | **Plan campaign intensity around economic conditions**, and review the mass-calling strategy in May. | Low Euribor / employment → far higher response (55% of model importance); May had the most calls (13,769) and the lowest rate (6.4%) |
| **R7** | **Retrain the model before each campaign (at least quarterly)** and monitor conversion of the called list; retrain early if it drops below ~25% or the economy moves outside past ranges. | Forward-in-time validation ROC-AUC ≈ 0.55 vs 0.80 (03 §6); yes-rate moved from 4.8% → 52% across 2008–2010 |
| **R8** | **Keep humans in the loop and monitor fairness:** review call lists, track selection/outcomes by age and marital group, and apply extra care (call caps, clear product information) for older clients. | 61+ selected at 95–99% even without `age` as an input (proxies) (06 §7, 07 §5) |
| **R9** | **Improve the data:** add a stable client ID, record contact history consistently, and capture account balance / product holdings. | No client ID; `pdays` inconsistent in 4,110 rows; 26% of rows contain "unknown" |
| **R10** | Use the **marketing profiles** (`docs/marketing_profiles.md`) to design messages and offers for high-response groups (previous subscribers, retired, students, mobile clients). | Secondary lens (06) |

---

## 3. Limitations

| # | Limitation | Impact | Mitigation |
|---|---|---|---|
| L1 | **Time drift:** results depend on economic conditions; past → future validation is much weaker (ROC-AUC ≈ 0.55) | Real-world performance in a new period may be lower than the test estimate | Frequent retraining, monitoring (R7) |
| L2 | **Random split:** the test set comes from the same 2008–2010 period as training | Test score (PR-AUC 0.496) is likely optimistic for future campaigns | Reported alongside within-year (0.59–0.79) and forward-in-time results |
| L3 | **Old, single-source data:** one Portuguese bank, 2008–2010 financial crisis | May not transfer to other banks, countries or today's interest rates | Retrain on the bank's own recent data before use |
| L4 | **Economic features dominate** (~55% of importance) | Model partly predicts *when* rather than *who*; within a single campaign, ranking relies on fewer signals | Profiles based on history/channel are more transferable (R3, R4) |
| L5 | **Performance ceiling** without call duration: PR-AUC ≈ 0.50 | About 1/3 of subscribers are not in the top 20% | Extend the list when capacity allows (R1) |
| L6 | **Scores are not calibrated probabilities** (class weights) | A score of 0.6 does not mean a 60% chance | Use the model for ranking; calibrate if probabilities are needed |
| L7 | **No client ID; 26% "unknown" values; inconsistent `pdays`** | Repeat clients and some histories cannot be tracked | Data improvements (R9) |
| L8 | **`campaign` is only partly known before a campaign starts** | First-call scores use campaign = 1 | Re-score before each call attempt |
| L9 | **Random Forest overfits the training data** (train–CV gap 25.5%) | Did not hurt test performance, but a sign of memorisation | Monitor; XGBoost fallback (gap 14%) |
| L10 | **Proxies for sensitive attributes** | Removing `age` does not change who is selected | Group monitoring and human oversight (R8) |

---

## 4. Risks and responsible-AI considerations
- **Fairness:** older clients are selected far more often. This reflects their real response, but it creates a risk of
  **over-contacting potentially vulnerable customers** and of mis-selling. Mitigate with call caps, clear product information and monitoring.
- **Privacy:** only data the bank already holds is used; `age` and `marital` removed (data minimisation); no new personal data is collected.
- **Automation risk:** the model must **support** call planning, not decide eligibility for products. Every list is reviewed by a person.
- **Feedback loop:** if only top-scored clients are ever called, the model stops learning about other groups. Keep a small random
  sample (e.g. 5%) of lower-ranked clients in each campaign to keep the training data representative.
- **Transparency:** SHAP reasons can be shown for each recommended call (07 §7), so staff can see *why* a client is prioritised.
