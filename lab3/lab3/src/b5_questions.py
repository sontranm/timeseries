import bootstrap  # noqa: F401

import warnings

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from xgboost import XGBRegressor

from load_data import PROCESSED, load_aep_clean
from utils import make_lag_features, metrics, save_fig, split_xy

warnings.filterwarnings("ignore")


def xgb():
    return XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=6,
                        subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1)


def q1_linear_vs_xgb(series, p=24):
    Xtr, Xte, ytr, yte = split_xy(make_lag_features(series, p))
    rows = []
    for name, model in [("Linear Regression", LinearRegression()), ("XGBoost", xgb())]:
        model.fit(Xtr, ytr)
        rows.append({"model": name, **metrics(yte, model.predict(Xte))})
    return pd.DataFrame(rows)


def q2_vary_p(series, ps=(1, 3, 6, 12, 24, 48, 72, 168)):
    rows = []
    for p in ps:
        Xtr, Xte, ytr, yte = split_xy(make_lag_features(series, p))
        m = xgb().fit(Xtr, ytr)
        rows.append({"p": p, **metrics(yte, m.predict(Xte))})
    return pd.DataFrame(rows)


def q3_arima_vs_xgb(series, p=24, train_hours=24 * 90, test_hours=24 * 14):
    """ARIMA is slow on 100k+ points, so compare on a recent window.
    Both models give ONE-STEP-AHEAD forecasts on the same test hours."""
    window = series.iloc[-(train_hours + test_hours):]
    train, test = window.iloc[:train_hours], window.iloc[train_hours:]

    arima = ARIMA(train, order=(p, 0, 1)).fit()
    arima_pred = arima.apply(window).predict(start=test.index[0], end=test.index[-1])

    frame = make_lag_features(series, p)
    Xtr = frame.loc[:train.index[-1]].drop(columns="y")
    ytr = frame.loc[:train.index[-1], "y"]
    Xte = frame.loc[test.index[0]:test.index[-1]].drop(columns="y")
    m = xgb().fit(Xtr, ytr)
    xgb_pred = pd.Series(m.predict(Xte), index=Xte.index)

    rows = [
        {"model": f"ARIMA({p},0,1)", **metrics(test, arima_pred.loc[test.index])},
        {"model": "XGBoost", **metrics(test.loc[Xte.index], xgb_pred)},
    ]
    return pd.DataFrame(rows)


def main():
    series = load_aep_clean()

    print("\n== Q1: Linear Regression vs XGBoost ==")
    q1 = q1_linear_vs_xgb(series)
    print(q1.round(3).to_string(index=False))

    print("\n== Q2: effect of lag order p ==")
    q2 = q2_vary_p(series)
    print(q2.round(3).to_string(index=False))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(q2["p"], q2["MAE"], marker="o")
    ax.set_xscale("log")
    ax.set_xlabel("Number of lags p")
    ax.set_ylabel("MAE (MW)")
    ax.set_title("MAE vs number of lags")
    save_fig(fig, "b5_vary_p.png")

    print("\n== Q3: ARIMA vs XGBoost (recent window) ==")
    q3 = q3_arima_vs_xgb(series)
    print(q3.round(3).to_string(index=False))

    q1.to_csv(PROCESSED / "b5_q1.csv", index=False)
    q2.to_csv(PROCESSED / "b5_q2.csv", index=False)
    q3.to_csv(PROCESSED / "b5_q3.csv", index=False)


if __name__ == "__main__":
    main()
