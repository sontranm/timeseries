"""Shared helpers: features, split, metrics, plotting."""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from load_data import FIG

TEST_FRACTION = 0.2


def make_lag_features(series: pd.Series, p: int = 24) -> pd.DataFrame:
    """Return a frame with target 'y' and lag_1..lag_p (lag_k = value k hours ago)."""
    data = {"y": series}
    for k in range(1, p + 1):
        data[f"lag_{k}"] = series.shift(k)
    return pd.DataFrame(data).dropna()


def add_rolling_features(frame: pd.DataFrame, series: pd.Series, window: int = 24) -> pd.DataFrame:
    """Rolling mean/std computed on shifted data, so the current value is never used."""
    past = series.shift(1)
    out = frame.copy()
    out[f"roll_mean_{window}"] = past.rolling(window).mean()
    out[f"roll_std_{window}"] = past.rolling(window).std()
    return out.dropna()


def add_calendar_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["hour"] = out.index.hour
    out["dayofweek"] = out.index.dayofweek
    out["month"] = out.index.month
    return out


def split_xy(frame: pd.DataFrame):
    """Chronological split. Never shuffle a time series."""
    X, y = frame.drop(columns="y"), frame["y"]
    cut = int(len(frame) * (1 - TEST_FRACTION))
    return X.iloc[:cut], X.iloc[cut:], y.iloc[:cut], y.iloc[cut:]


def metrics(y_true, y_pred) -> dict:
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    return {
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "RMSE": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "MAPE_%": float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100),
    }


def save_fig(fig, name: str):
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=150)
    print("Saved figure:", FIG / name)
