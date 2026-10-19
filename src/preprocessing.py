"""Shared preprocessing for all models (Step 3 - see notebooks/02_preprocessing.ipynb).

Two kinds of preprocessing are kept strictly apart:

1. clean_rows(): deterministic row-level fixes that learn nothing from the data
   (drop duplicates, drop leakage column, flags, merges, capping). Safe to apply
   before the train/test split.
2. build_preprocessor(): a scikit-learn ColumnTransformer whose steps are FITTED
   (one-hot categories, scaling). It must only ever be fitted on training data,
   inside a Pipeline together with the model, so no test information leaks.
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from . import config

# ---- Row-level cleaning settings (decisions D3, D8, D9, D10, D13, D14) -------
CAMPAIGN_CAP = 10
EDUCATION_MERGE = {"illiterate": "basic.4y"}

# ---- Age bins for the linear model (captures the U-shaped effect, insight E12)
AGE_BINS = [16, 25, 30, 40, 50, 60, 70, 120]
AGE_LABELS = ["17-25", "26-30", "31-40", "41-50", "51-60", "61-70", "71+"]

# ---- Feature lists -----------------------------------------------------------
CAT_FEATURES = ["job", "marital", "education", "default", "housing", "loan",
                "contact", "month", "day_of_week", "poutcome"]
NUM_FEATURES = ["age", "campaign", "previous", "contacted_before"]
ECON_FEATURES = list(config.ECONOMIC_FEATURES)
# Linear model keeps one of the three highly collinear indicators (decision D11)
ECON_FEATURES_LINEAR = ["euribor3m", "cons.price.idx", "cons.conf.idx"]

# Features removed by feature selection (decision D15, verified in 02_preprocessing)
DROPPED_FEATURES = ["housing", "loan"]


def clean_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the deterministic row-level cleaning steps and return a new DataFrame."""
    out = df.drop_duplicates().reset_index(drop=True)                       # D8
    out = out.drop(columns=config.LEAKAGE_FEATURES)                         # D3
    out["contacted_before"] = (out["previous"] > 0).astype(int)             # D10
    out = out.drop(columns=["pdays"])                                       # D10
    out["default"] = np.where(out["default"] == "no", "no", "not_no")       # D13
    out["education"] = out["education"].replace(EDUCATION_MERGE)            # D14
    out["campaign"] = out["campaign"].clip(upper=CAMPAIGN_CAP)              # D9
    out[config.TARGET] = (out[config.TARGET] == config.POSITIVE_CLASS).astype(int)
    return out


def bin_age(X: pd.DataFrame) -> pd.DataFrame:
    """Replace numeric age with an age-group label (used by the linear pipeline only)."""
    return X.assign(age=pd.cut(X["age"], bins=AGE_BINS, labels=AGE_LABELS).astype(str))


def feature_lists(kind: str, drop=None):
    """Return (categorical, numeric) feature lists for a pipeline kind ('linear' or 'tree')."""
    drop = set(DROPPED_FEATURES if drop is None else drop)
    if kind == "linear":
        cats = [c for c in CAT_FEATURES if c not in drop]
        nums = [c for c in NUM_FEATURES if c != "age"] + ECON_FEATURES_LINEAR
    elif kind == "tree":
        cats = [c for c in CAT_FEATURES if c not in drop]
        nums = NUM_FEATURES + ECON_FEATURES
    else:
        raise ValueError("kind must be 'linear' or 'tree'")
    return cats, [c for c in nums if c not in drop]


def _one_hot():
    return OneHotEncoder(handle_unknown="ignore", sparse_output=False)


def build_preprocessor(kind: str, drop=None) -> ColumnTransformer:
    """Build the (unfitted) ColumnTransformer for a model family.

    linear: one-hot categoricals + age groups, standard-scaled numerics,
            reduced economic indicators (Logistic Regression).
    tree:   one-hot categoricals, raw numerics, all economic indicators
            (Decision Tree, Random Forest, XGBoost - no scaling needed).
    `drop` overrides DROPPED_FEATURES (used for the feature-selection check).
    """
    cats, nums = feature_lists(kind, drop)
    if kind == "linear":
        age_pipe = Pipeline([
            ("bin", FunctionTransformer(bin_age, feature_names_out="one-to-one")),
            ("onehot", _one_hot()),
        ])
        transformers = [
            ("cat", _one_hot(), cats),
            ("age", age_pipe, ["age"]),
            ("num", StandardScaler(), nums),
        ]
    else:
        transformers = [
            ("cat", _one_hot(), cats),
            ("num", "passthrough", nums),
        ]
    return ColumnTransformer(transformers, remainder="drop", verbose_feature_names_out=False)


MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def reconstruct_year(month: pd.Series) -> pd.Series:
    """Approximate year of each row from the date-ordered month column (analysis only, never a feature).

    Rows are ordered by date (May 2008 - Nov 2010), so a new year starts whenever the month number goes back.
    """
    month_num = month.map({m: i for i, m in enumerate(MONTHS, start=1)})
    return 2008 + (month_num.diff() < 0).cumsum()


def recreate_split_with_positions():
    """Re-run the deterministic cleaning + seeded split, keeping each row's original (date-order) index.

    Returns clean, X_train, X_test, y_train, y_test - identical rows to train.csv / test.csv.
    """
    from sklearn.model_selection import train_test_split
    clean = clean_rows(pd.read_csv(config.RAW_FILE, sep=config.CSV_SEPARATOR))
    X, y = clean.drop(columns=config.TARGET), clean[config.TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, stratify=y, random_state=config.RANDOM_STATE)
    return clean, X_train, X_test, y_train, y_test


def load_split():
    """Load the saved train/test files and return X_train, X_test, y_train, y_test."""
    train = pd.read_csv(config.TRAIN_FILE)
    test = pd.read_csv(config.TEST_FILE)
    return (train.drop(columns=config.TARGET), test.drop(columns=config.TARGET),
            train[config.TARGET], test[config.TARGET])
