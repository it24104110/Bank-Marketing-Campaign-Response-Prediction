# Model / Method Comparison – Group 2026-DS-02

Source: `notebooks/04_modelling.ipynb` · Training set, stratified 5-fold CV (same folds for all models), mean ± std · threshold 0.5 for recall/precision/F1/accuracy.

## Cross-validated performance

| Model | Role | PR-AUC (primary) | ROC-AUC | Recall | Precision | F1 | Balanced acc. | Accuracy | Top-20% capture |
|---|---|---|---|---|---|---|---|---|---|
| Dummy: always no | floor | 0.113 ± 0.000 | 0.500 | 0.000 | 0.000 | 0.000 | 0.500 | 0.887 | 0.189 |
| Dummy: random guess | floor | 0.113 ± 0.001 | 0.502 | 0.114 | 0.115 | 0.115 | 0.502 | 0.802 | 0.199 |
| Logistic Regression | **baseline** | 0.438 ± 0.012 | 0.787 | 0.634 | 0.328 | 0.432 | 0.735 | 0.812 | 0.620 |
| Decision Tree | alternative 1 | 0.443 ± 0.016 | 0.783 | 0.652 | 0.315 | 0.425 | 0.736 | 0.800 | 0.625 |
| Random Forest | alternative 2 | **0.470 ± 0.018** | **0.801** | 0.603 | **0.411** | **0.489** | 0.747 | **0.858** | **0.643** |
| XGBoost | alternative 3 | 0.467 ± 0.017 | 0.800 | 0.631 | 0.372 | 0.468 | **0.748** | 0.838 | 0.642 |

## Comparison beyond accuracy

| Model | Gain vs baseline (PR-AUC) | Folds better | Train–CV gap | SMOTE effect | Fit time / fold | Size | Interpretability |
|---|---|---|---|---|---|---|---|
| Logistic Regression | – | – | 0.5% | +0.000 | 0.7 s | 7 KB | High (coefficients) |
| Decision Tree | +0.006 ± 0.008 | 3/5 | 7.9% | −0.062 | 0.6 s | 45 KB | High (rules) |
| Random Forest | **+0.033 ± 0.009** | **5/5** | 25.5% | −0.027 | 12.9 s | 21 MB | Medium (importance, SHAP) |
| XGBoost | **+0.030 ± 0.006** | **5/5** | 14.0% | −0.019 | 5.0 s | 1.5 MB | Medium (importance, SHAP) |

## Best hyperparameters

| Model | Search | Best setting |
|---|---|---|
| Logistic Regression | Grid, 6 | `C = 0.01`, class_weight = balanced |
| Decision Tree | Grid, 80 | entropy, max_depth = None, min_samples_leaf = 100, balanced |
| Random Forest | Random, 20 | 300 trees, max_depth = 12, min_samples_leaf = 10, max_features = 0.3, balanced |
| XGBoost | Random, 25 | 600 rounds, learning_rate = 0.01, max_depth = 5, min_child_weight = 5, subsample = 0.7, colsample = 1.0, gamma = 0, λ = 1, scale_pos_weight = 7.88 |

## Interpretation
- Random Forest and XGBoost consistently beat the baseline in all folds; their difference from each other (0.003) is far below fold variation, so they are **tied**.
- The Decision Tree does not reliably beat the baseline; its value is interpretability (readable rules for the profile analysis).
- Class weights outperform SMOTE for every model; SMOTE is rejected.
- **Shortlist:** Random Forest and XGBoost. The final choice uses test results, threshold trade-off, per-year robustness and interpretability (Steps 6–8).
