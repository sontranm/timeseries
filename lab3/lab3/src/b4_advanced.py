import bootstrap  # noqa: F401

import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBRegressor

from load_data import PROCESSED, load_aep_clean
from utils import (add_calendar_features, add_rolling_features, make_lag_features,
                   metrics, save_fig, split_xy)

P = 24


def new_xgb(**kw):
    params = dict(n_estimators=300, learning_rate=0.05, max_depth=6,
                  subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1)
    params.update(kw)
    return XGBRegressor(**params)


def ex1_rolling(series):
    """Ex 1: add rolling mean/std (+ calendar) and compare with the lag-only baseline."""
    base = make_lag_features(series, P)
    rich = add_calendar_features(add_rolling_features(base, series, 24))
    rows = []
    for name, frame in [("lags only", base), ("lags + rolling + calendar", rich)]:
        Xtr, Xte, ytr, yte = split_xy(frame)
        m = new_xgb().fit(Xtr, ytr)
        rows.append({"model": name, **metrics(yte, m.predict(Xte))})
    return pd.DataFrame(rows)


def ex2_multistep(series, horizons=(1, 6, 12, 24)):
    """Ex 2: direct multi-step forecasting, one model per horizon h (predict y[t+h])."""
    base = make_lag_features(series, P)
    rows = []
    for h in horizons:
        frame = base.copy()
        frame["y"] = base["y"].shift(-(h - 1))  # target h-1 steps ahead of the usual one
        frame = frame.dropna()
        Xtr, Xte, ytr, yte = split_xy(frame)
        m = new_xgb().fit(Xtr, ytr)
        rows.append({"horizon_h": h, **metrics(yte, m.predict(Xte))})
    return pd.DataFrame(rows)


def ex3_tuning(series):
    """Ex 3: small grid search with TimeSeriesSplit (training part only)."""
    frame = make_lag_features(series, P)
    Xtr, Xte, ytr, yte = split_xy(frame)
    grid = {"max_depth": [4, 6], "learning_rate": [0.05, 0.1], "n_estimators": [200, 400]}
    tscv = TimeSeriesSplit(n_splits=3)
    results = []
    for values in itertools.product(*grid.values()):
        params = dict(zip(grid.keys(), values))
        maes = []
        for tr, va in tscv.split(Xtr):
            m = new_xgb(**params).fit(Xtr.iloc[tr], ytr.iloc[tr])
            maes.append(metrics(ytr.iloc[va], m.predict(Xtr.iloc[va]))["MAE"])
        results.append({**params, "cv_MAE": float(np.mean(maes))})
    table = pd.DataFrame(results).sort_values("cv_MAE")
    best = {k: table.iloc[0][k] for k in grid}
    best = {k: (int(v) if k != "learning_rate" else float(v)) for k, v in best.items()}
    final = new_xgb(**best).fit(Xtr, ytr)
    test = metrics(yte, final.predict(Xte))
    return table, best, test


def ex4_random_forest(series):
    """Ex 4: compare XGBoost with Random Forest on the same split."""
    frame = make_lag_features(series, P)
    Xtr, Xte, ytr, yte = split_xy(frame)
    rows = []
    xgb = new_xgb().fit(Xtr, ytr)
    rows.append({"model": "XGBoost", **metrics(yte, xgb.predict(Xte))})
    rf = RandomForestRegressor(n_estimators=100, max_depth=14, min_samples_leaf=5,
                               max_features=0.5, max_samples=0.5,
                               random_state=42, n_jobs=-1).fit(Xtr, ytr)
    rows.append({"model": "Random Forest", **metrics(yte, rf.predict(Xte))})
    return pd.DataFrame(rows)


def main():
    series = load_aep_clean()
    out = {}

    print("\n== Ex 1: rolling mean/std ==")
    out["ex1"] = ex1_rolling(series)
    print(out["ex1"].round(3).to_string(index=False))

    print("\n== Ex 2: multi-step ==")
    out["ex2"] = ex2_multistep(series)
    print(out["ex2"].round(3).to_string(index=False))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(out["ex2"]["horizon_h"], out["ex2"]["MAE"], marker="o")
    ax.set_xlabel("Forecast horizon (hours)")
    ax.set_ylabel("MAE (MW)")
    ax.set_title("Error grows with horizon")
    save_fig(fig, "b4_multistep_mae.png")

    print("\n== Ex 3: TimeSeriesSplit tuning ==")
    table, best, test = ex3_tuning(series)
    print(table.round(3).to_string(index=False))
    print("Best:", best, "| Test:", {k: round(v, 3) for k, v in test.items()})
    out["ex3"] = table

    print("\n== Ex 4: XGBoost vs Random Forest ==")
    out["ex4"] = ex4_random_forest(series)
    print(out["ex4"].round(3).to_string(index=False))

    for name, df in out.items():
        df.to_csv(PROCESSED / f"b4_{name}.csv", index=False)


if __name__ == "__main__":
    main()
