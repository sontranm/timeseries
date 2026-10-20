from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

def load_a10():
    df = pd.read_csv(RAW / "a10.csv", parse_dates=["date"], index_col="date")
    return df["value"].asfreq("MS")

def load_airpassengers():
    df = pd.read_csv(RAW / "airlinepassengers.csv", parse_dates=["Month"], index_col="Month")
    return df["Passengers"].asfreq("MS")