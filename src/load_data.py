"""Shared Lab 2 data loaders. Prepared for the group by Le Quynh."""
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIG = ROOT / "docs" / "lab2" / "figures"

for directory in (PROCESSED, FIG):
    directory.mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path, **kwargs) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(
            f"Data file not found: {path}. Keep source datasets in data/raw/."
        )
    return pd.read_csv(path, **kwargs)


def load_airpassengers() -> pd.Series:
    """Load monthly AirPassengers; the index is the first day of each month."""
    frame = _read_csv(
        RAW / "airline-passengers.csv",
        parse_dates=["Month"],
        index_col="Month",
    ).sort_index()
    if frame.index.has_duplicates:
        raise ValueError("AirPassengers contains duplicate months.")
    series = frame["Passengers"].astype(float).asfreq("MS")
    series.name = "Passengers"
    return series


def load_temperatures() -> pd.Series:
    """Load the original Melbourne daily minimum-temperature observations."""
    frame = _read_csv(
        RAW / "daily-min-temperatures.csv",
        parse_dates=["Date"],
        index_col="Date",
    ).sort_index()
    if frame.index.has_duplicates:
        raise ValueError("Daily minimum temperatures contains duplicate dates.")
    series = frame["Temp"].astype(float)
    series.name = "Temp"
    return series
