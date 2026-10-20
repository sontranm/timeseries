"""Đọc dữ liệu dùng chung cho Lab 2."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIG = ROOT / "docs" / "lab2" / "figures"
PROCESSED.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)


def load_airpassengers():
    path = RAW / "airline-passengers.csv"
    if not path.exists():  
        path = RAW / "airlinepassengers.csv"
    df = pd.read_csv(path, parse_dates=["Month"], index_col="Month")
    df.index.freq = "MS"
    return df["Passengers"]


def load_temperatures():
    df = pd.read_csv(RAW / "daily-min-temperatures.csv",
                     parse_dates=["Date"], index_col="Date")
    return df["Temp"]


def load_a10():
    df = pd.read_csv(RAW / "a10.csv", parse_dates=["date"], index_col="date")
    return df["value"].asfreq("MS")
