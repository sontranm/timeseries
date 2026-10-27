import bootstrap  # noqa: F401

import matplotlib.pyplot as plt
import pandas as pd
from xgboost import XGBRegressor

from load_data import PROCESSED, load_aep_clean
from utils import make_lag_features, metrics, save_fig, split_xy

P = 24  # number of lags


def main():
    series = load_aep_clean()

    frame = make_lag_features(series, P)                      # step 2
    X_train, X_test, y_train, y_test = split_xy(frame)        # steps 3-4
    print(f"Train: {len(X_train)} rows | Test: {len(X_test)} rows")
    print("Train ends:", X_train.index[-1], "| Test starts:", X_test.index[0])

    model = XGBRegressor(                                      # step 5
        n_estimators=300, learning_rate=0.05, max_depth=6,
        subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1,
    )
    model.fit(X_train, y_train)

    pred = pd.Series(model.predict(X_test), index=X_test.index)  # step 6
    result = metrics(y_test, pred)
    print({k: round(v, 3) for k, v in result.items()})
    pd.DataFrame([result]).to_csv(PROCESSED / "b3_metrics.csv", index=False)

    fig, ax = plt.subplots(figsize=(11, 4))
    last = slice(-24 * 14, None)
    ax.plot(y_test.iloc[last], label="Actual")
    ax.plot(pred.iloc[last], label="XGBoost", alpha=0.8)
    ax.set_title("Actual vs predicted (last 14 days of test)")
    ax.set_ylabel("MW")
    ax.legend()
    save_fig(fig, "b3_actual_vs_pred.png")

    imp = pd.Series(model.feature_importances_, index=X_train.columns).sort_values()  # step 7
    fig, ax = plt.subplots(figsize=(7, 6))
    imp.tail(15).plot.barh(ax=ax)
    ax.set_title("Top 15 feature importances")
    save_fig(fig, "b3_feature_importance.png")
    print(imp.sort_values(ascending=False).head(5).round(3))


if __name__ == "__main__":
    main()
