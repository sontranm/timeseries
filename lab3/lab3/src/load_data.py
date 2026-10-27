from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIG = ROOT / "docs" / "figures"

for directory in (PROCESSED, FIG):
    directory.mkdir(parents=True, exist_ok=True)


def load_aep_raw() -> pd.DataFrame:
    """Load AEP_hourly.csv exactly as downloaded."""
    path = RAW / "AEP_hourly.csv"
    if not path.is_file():
        raise FileNotFoundError(f"Not found: {path}. Put AEP_hourly.csv in data/raw/.")
    return pd.read_csv(path, parse_dates=["Datetime"])


def load_aep_clean() -> pd.Series:
    """Load the cleaned hourly series produced by b1_clean_data.py."""
    path = PROCESSED / "b1_aep_clean.csv"
    if not path.is_file():
        raise FileNotFoundError("Run b1_clean_data.py first.")
    frame = pd.read_csv(path, parse_dates=["Datetime"], index_col="Datetime")
    return frame["AEP_MW"].asfreq("h")
