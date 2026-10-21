"""Exercise 3: classical and STL decomposition. Assigned to: Bao Dinh."""
import bootstrap  # noqa: F401

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL, seasonal_decompose

from analysis_utils import (
    COLORS, finish_axes, ljung_box_rows, plot_correlogram, save_csv, save_figure
)
from load_data import load_airpassengers
import matplotlib.pyplot as plt


def _plot_components(components, title, filename, observed_label):
    fig, axes = plt.subplots(4, 1, figsize=(11, 8), sharex=True,
                             constrained_layout=True)
    names = [
        (components.observed, observed_label, COLORS["blue"]),
        (components.trend, "Trend", COLORS["orange"]),
        (components.seasonal, "Seasonal", COLORS["green"]),
        (components.resid, "Residual", COLORS["vermillion"]),
    ]
    for ax, (series, label, color) in zip(axes, names):
        ax.plot(series.index, series, color=color, linewidth=1.25)
        ax.set_ylabel(label)
        finish_axes(ax)
    axes[0].set_title(title)
    axes[-1].set_xlabel("Month")
    save_figure(fig, filename)


def main():
    y = load_airpassengers()
    classical = seasonal_decompose(y, model="multiplicative", period=12)
    _plot_components(classical, "Classical decomposition (multiplicative; period 12)",
                     "b3_classical.png", "Observed")

    log_y = np.log(y)
    stl = STL(log_y, period=12, robust=True).fit()
    fig, axes = plt.subplots(4, 1, figsize=(11, 8), sharex=True,
                             constrained_layout=True)
    components = [
        (log_y, "log(Passengers)", COLORS["blue"]),
        (stl.trend, "Trend (log)", COLORS["orange"]),
        (stl.seasonal, "Seasonal (log)", COLORS["green"]),
        (stl.resid, "Residual (log)", COLORS["vermillion"]),
    ]
    for ax, (series, label, color) in zip(axes, components):
        ax.plot(series.index, series, color=color, linewidth=1.25)
        ax.set_ylabel(label)
        finish_axes(ax)
    axes[0].set_title("STL decomposition of log(AirPassengers), period 12, robust")
    axes[-1].set_xlabel("Month")
    save_figure(fig, "b3_stl.png")

    decomposition = pd.DataFrame({
        "trend": stl.trend,
        "seasonal": stl.seasonal,
        "resid": stl.resid,
    })
    save_csv(decomposition, "decomposition_stl.csv", index_label="Month")

    fig, ax = plt.subplots(figsize=(9, 4.2), constrained_layout=True)
    plot_correlogram(stl.resid, 40, ax,
                     "ACF of STL residuals (log scale)", COLORS["purple"])
    ax.set_xlabel("Lag (months)")
    save_figure(fig, "b3_resid_acf.png")

    residual_variance = np.var(stl.resid, ddof=1)
    trend_strength = max(
        0.0,
        1.0 - residual_variance / np.var(stl.trend + stl.resid, ddof=1),
    )
    seasonal_strength = max(
        0.0,
        1.0 - residual_variance / np.var(stl.seasonal + stl.resid, ddof=1),
    )
    seasonal_cycle = pd.Series(stl.seasonal, index=y.index).groupby(y.index.month).mean()
    peak_month = int(seasonal_cycle.idxmax())
    rows = [
        {"metric": "trend_strength", "value": trend_strength},
        {"metric": "seasonal_strength", "value": seasonal_strength},
        {"metric": "seasonal_peak_month", "value": peak_month},
        {"metric": "residual_variance", "value": residual_variance},
    ]
    lb_rows = ljung_box_rows(pd.Series(stl.resid, index=y.index), "STL residual (log)")
    rows.extend(
        {"metric": f"ljung_box_p_lag_{row['lag']}", "value": row["p_value"]}
        for row in lb_rows
    )
    save_csv(pd.DataFrame(rows), "b3_metrics.csv", index_label="row")
    print("STL strength and residual diagnostics:")
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
