# Final Report Outline – Group 2026-DS-02

Each section lists **what to write**, **where the evidence is**, and the **rubric criterion (marks)** it earns.
Copy tables and figures from the referenced files; all numbers are already final.

| # | Section | Content | Evidence (file / figure) | Rubric (marks) |
|---|---|---|---|---|
| 1 | Introduction & business problem | Bank, telemarketing, 11% success, need to prioritise calls; stakeholder; decision need | `docs/problem_framing_canvas.md` | Framing (5) |
| 2 | Problem framing canvas | Canvas table: lenses, unit of analysis, target/output, allowed inputs, success criteria | `problem_framing_canvas.md` | Framing (5) |
| 3 | Workflow | 10-step workflow diagram + how notebooks map to it | Initial report §4; README structure | Workflow & decision log (10) |
| 4 | Data understanding | Dataset, version choice (D1), row meaning, data dictionary, target imbalance | `data_dictionary.csv`, `dataset_fingerprint.md`, fig01 | EDA (10) |
| 5 | EDA insights | Key insights E1–E19 with figures; "unknown", pdays, outliers, U-shaped age, time drift, duration leakage | `eda_insight_log.md`, `eda_findings.txt`, fig02–fig10 | EDA (10) |
| 6 | Preprocessing & features | Two kinds of preprocessing (row-level vs fitted); each decision with justification; split before selection; VIF fix; two pipelines; imbalance strategy | `preprocessing_log.md`, `preprocessing_findings.txt` | Preprocessing (15) |
| 7 | Validation design | Stratified 5-fold CV, PR-AUC primary + top-20% business metric; dummy floor; duration benchmark; forward-in-time check | `validation_findings.txt`, fig11 | Evaluation (20) |
| 8 | Models & comparison | Baseline LR + DT, RF, XGBoost: why each, tuning, CV comparison, paired fold comparison, overfitting, SMOTE rejected | `model_comparison.md`, `modelling_findings.txt`, fig12–fig13 | Models (20) |
| 9 | Test evaluation | Test vs CV, bootstrap CIs, ROC/PR/gains, thresholds from OOF, business translation, per-year | `evaluation_findings.txt`, fig14–fig16 | Evaluation (20) |
| 10 | Marketing profiles (secondary lens) | Drivers, direction of effects, segments, top-10% profile | `marketing_profiles.md`, `interpretation_findings.txt`, fig17–fig21 | Recommendation (10) / Framing |
| 11 | Responsible AI | Group outcomes, age/marital removal, proxy finding, controls | `interpretation_findings.txt` §6, `model_card.md` | Evaluation (20) / Recommendation (10) |
| 12 | Final model & recommendations | Selection matrix, final config, operating rules, stakeholder value, R1–R10 | `07_final_model.ipynb`, `recommendations.md`, `model_card.md` | Recommendation (10) |
| 13 | Limitations | L1–L10 with mitigations | `recommendations.md` §3 | Recommendation (10) |
| 14 | Decision log | Table D1–D29 (appendix if long) | `decision_log.md` | Workflow & decision log (10) |
| 15 | Reproducibility & AI use | How to run, versions, fingerprint, seed; AI-use declaration | `README.md`, `ai_use_declaration.md` | Reproducibility (10) |
| 16 | References | Moro et al. (2014); scikit-learn; XGBoost; SHAP (Lundberg & Lee, 2017); UCI repository | – | – |

## Key numbers to quote (consistent everywhere)
- Data: 41,188 rows → 41,176 after duplicates; 11.27% yes; train 32,940 / test 8,236.
- Test PR-AUC: LR 0.446 · DT 0.465 · **RF 0.496** · XGB 0.484 · random 0.116.
- RF − XGB = +0.011 [0.003, 0.019]; RF − LR = +0.049 [0.033, 0.066].
- Final model (no age/marital): PR-AUC 0.496, ROC-AUC 0.814, top-20% capture 67.0%.
- Capacity 20%: 1,651 calls → 622 subscribers (67.0%), conversion 37.7% (3.3×). Max F1: 1,125 calls → 536 (57.8%), 47.6% (4.2×).
- Duration leakage: would inflate PR-AUC by +0.15–0.19.
- Time drift: forward-in-time ROC-AUC ≈ 0.52–0.55; within-year 0.59 (2008) / 0.79 (2009) / 0.75 (2010).
- Economic indicators ≈ 55% of RF SHAP importance.
