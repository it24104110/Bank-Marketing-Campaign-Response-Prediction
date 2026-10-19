"""Shared project settings for IT3091 Group 2026-DS-02 (Bank Marketing).

Every notebook imports from here so all members use the same paths,
random seed, and dataset definition.
"""
from pathlib import Path

# ---- Paths -----------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
FIGURES = PROJECT_ROOT / "figures"
DOCS = PROJECT_ROOT / "docs"
MODELS_DIR = PROJECT_ROOT / "models"
RESULTS_DIR = PROJECT_ROOT / "results"

RAW_FILE = DATA_RAW / "bank-additional-full.csv"
CLEAN_FILE = DATA_PROCESSED / "bank_clean.csv"
TRAIN_FILE = DATA_PROCESSED / "train.csv"
TEST_FILE = DATA_PROCESSED / "test.csv"
TEST_SIZE = 0.20
CSV_SEPARATOR = ";"

# SHA-256 of the original UCI file (see docs/dataset_fingerprint.md)
RAW_FILE_SHA256 = "74adfc578bf77a7ff4bb1ba4a9f8709d9e3c6907342959c2c8416847e0afb4d8"
EXPECTED_SHAPE = (41188, 21)

# ---- Reproducibility -------------------------------------------------------
RANDOM_STATE = 42

# ---- Target ----------------------------------------------------------------
TARGET = "y"
POSITIVE_CLASS = "yes"

# ---- Known leakage feature (decision D3, to be verified in preprocessing) ---
LEAKAGE_FEATURES = ["duration"]

# ---- Feature groups (from bank-additional-names.txt) -----------------------
CLIENT_FEATURES = ["age", "job", "marital", "education", "default", "housing", "loan"]
CONTACT_FEATURES = ["contact", "month", "day_of_week", "duration"]
CAMPAIGN_FEATURES = ["campaign", "pdays", "previous", "poutcome"]
ECONOMIC_FEATURES = ["emp.var.rate", "cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed"]

MISSING_TOKEN = "unknown"   # categorical missing values are coded as "unknown"
PDAYS_NOT_CONTACTED = 999   # sentinel: client not previously contacted
