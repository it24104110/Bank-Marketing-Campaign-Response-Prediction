"""Shared validation and evaluation tools (Step 4 - see notebooks/03_validation.ipynb).

Every model is scored with the SAME cross-validation folds and the SAME metrics,
so comparisons between models are fair. The test set is only used once, at the
end, through evaluate_test().
"""
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, average_precision_score, balanced_accuracy_score,
                             confusion_matrix, f1_score, make_scorer, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import StratifiedKFold, cross_validate

from . import config

# Same 5 folds for every model (decision D18)
CV = StratifiedKFold(n_splits=5, shuffle=True, random_state=config.RANDOM_STATE)

# Business metric: share of all subscribers found by calling only the top-ranked 20% of clients
TOP_FRACTION = 0.20

# Main metric used to compare and select models
PRIMARY_METRIC = "pr_auc"


def top_k_capture(y_true, y_score, fraction=TOP_FRACTION):
    """Share of all positives that fall in the top `fraction` of clients ranked by score."""
    y_true = np.asarray(y_true)
    n_top = int(np.ceil(fraction * len(y_true)))
    top_idx = np.argsort(-np.asarray(y_score), kind="stable")[:n_top]
    return y_true[top_idx].sum() / y_true.sum()


def _top_capture_scorer(estimator, X, y):
    return top_k_capture(y, estimator.predict_proba(X)[:, 1])


SCORING = {
    "pr_auc": "average_precision",
    "roc_auc": "roc_auc",
    "precision": make_scorer(precision_score, zero_division=0),
    "recall": make_scorer(recall_score, zero_division=0),
    "f1": make_scorer(f1_score, zero_division=0),
    "balanced_acc": "balanced_accuracy",
    "accuracy": "accuracy",
    "top20_capture": _top_capture_scorer,
}


def evaluate_cv(model, X, y, name, cv=CV, n_jobs=None):
    """Cross-validate a full pipeline and return one row of mean/std scores."""
    scores = cross_validate(model, X, y, cv=cv, scoring=SCORING, n_jobs=n_jobs)
    row = {"model": name}
    for metric in SCORING:
        row[f"{metric}_mean"] = scores[f"test_{metric}"].mean()
        row[f"{metric}_std"] = scores[f"test_{metric}"].std()
    row["fit_time_s"] = scores["fit_time"].mean()
    row["fold_scores"] = {metric: scores[f"test_{metric}"] for metric in SCORING}
    return row


def paired_comparison(rows, baseline, metric=PRIMARY_METRIC):
    """Compare each model with the baseline fold by fold (all models share the same folds)."""
    by_name = {r["model"]: r["fold_scores"][metric] for r in rows}
    base = by_name[baseline]
    out = []
    for name, folds in by_name.items():
        if name == baseline:
            continue
        diff = folds - base
        out.append({"model": name, f"mean_{metric}_diff_vs_baseline": diff.mean(),
                    "std_of_diff": diff.std(), "folds_better": f"{(diff > 0).sum()}/{len(diff)}"})
    return pd.DataFrame(out).set_index("model")


def cv_table(rows, metrics=("pr_auc", "roc_auc", "recall", "precision", "f1",
                            "balanced_acc", "accuracy", "top20_capture")):
    """Format evaluate_cv rows as a readable 'mean ± std' table."""
    df = pd.DataFrame(rows).drop(columns="fold_scores", errors="ignore").set_index("model")
    out = pd.DataFrame(index=df.index)
    for m in metrics:
        out[m] = df[f"{m}_mean"].map("{:.3f}".format) + " ± " + df[f"{m}_std"].map("{:.3f}".format)
    return out


def score_predictions(y_true, y_score, threshold=0.5):
    """All metrics for one set of predicted probabilities (used for test / per-fold evaluation)."""
    y_pred = (np.asarray(y_score) >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "pr_auc": average_precision_score(y_true, y_score),
        "roc_auc": roc_auc_score(y_true, y_score),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "balanced_acc": balanced_accuracy_score(y_true, y_pred),
        "accuracy": accuracy_score(y_true, y_pred),
        "top20_capture": top_k_capture(y_true, y_score),
        "TP": tp, "FP": fp, "FN": fn, "TN": tn,
    }


def evaluate_test(fitted_model, X_test, y_test, threshold=0.5):
    """Final, one-time evaluation of a fitted model on the locked test set."""
    return score_predictions(y_test, fitted_model.predict_proba(X_test)[:, 1], threshold)
