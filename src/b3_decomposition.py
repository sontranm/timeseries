"""Exercise 3: classical and STL decomposition. Assigned to: Bao Dinh."""
import bootstrap  # noqa: F401

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL, seasonal_decompose

from analysis_utils import (
    COLORS, add_caption, add_mean_line, finish_axes, ljung_box_rows, plot_correlogram,
    save_csv, save_figure, year_axis
)
from load_data import load_airpassengers
import matplotlib.pyplot as plt


def _plot_panels(panels, title, filename, caption):
    """Stack one panel per component, each with its own mean line and short description."""
    fig, axes = plt.subplots(len(panels), 1, figsize=(11, 9), sharex=True,
                             constrained_layout=True)
    for ax, (series, label, description, color, fmt) in zip(axes, panels):
        ax.plot(series.index, series, color=color, linewidth=1.25)
        mean = add_mean_line(ax, series, fmt=fmt)
        ax.set_ylabel(label)
        ax.set_title(f"{description}   (dashed = mean {mean:{fmt}})", loc="left",
                     fontsize=9, color=color)
        finish_axes(ax)
    fig.suptitle(title, fontweight="bold")
    axes[-1].set_xlabel("Year")
    year_axis(axes[-1])
    add_caption(fig, caption)
    save_figure(fig, filename)


def main():
    y = load_airpassengers()
    classical = seasonal_decompose(y, model="multiplicative", period=12)
    _plot_panels(
        [
            (classical.observed, "Observed (thousands)",
             "Observed = Trend × Seasonal × Residual", COLORS["blue"], ".1f"),
            (classical.trend, "Trend (thousands)",
             "Trend: 12-month centred moving average", COLORS["orange"], ".1f"),
            (classical.seasonal, "Seasonal (factor)",
             "Seasonal factor: >1 busier than usual, <1 quieter", COLORS["green"], ".3f"),
            (classical.resid, "Residual (factor)",
             "Residual factor: what trend and season do not explain", COLORS["vermillion"],
             ".3f"),
        ],
        "Classical decomposition of AirPassengers (multiplicative; period 12)",
        "b3_classical.png",
        "The series is split into three multiplied parts. Trend rises steadily from about 120k "
        "to 480k. The seasonal factor repeats the same pattern every year around its mean of "
        "1.0 (summer above 1, winter below 1). Residual factors fluctuate closely around 1.0, so "
        "most structure is captured by trend and seasonality. The trend and residual are "
        "missing for the first and last 6 months because of the centred moving average.",
    )

    log_y = np.log(y)
    stl = STL(log_y, period=12, robust=True).fit()
    _plot_panels(
        [
            (log_y, "log(Passengers)",
             "log(Observed) = Trend + Seasonal + Residual", COLORS["blue"], ".2f"),
            (stl.trend, "Trend (log)", "Trend: long-run level", COLORS["orange"], ".2f"),
            (stl.seasonal, "Seasonal (log)",
             "Seasonal: repeating yearly pattern (>0 above trend)", COLORS["green"], ".3f"),
            (stl.resid, "Residual (log)",
             "Residual: irregular part left over", COLORS["vermillion"], ".3f"),
        ],
        "STL decomposition of log(AirPassengers) (period 12, robust)",
        "b3_stl.png",
        "Taking logs turns multiplicative seasonality into additive, so the three parts are "
        "added. Trend increases smoothly over all 12 years. The seasonal part oscillates around "
        "its mean of about 0 with the same shape every year (peaks in July–August). Residuals "
        "stay near 0 except a few spikes in 1951–1954 that are candidates for outliers.",
    )

    decomposition = pd.DataFrame({
        "trend": stl.trend,
        "seasonal": stl.seasonal,
        "resid": stl.resid,
    })
    save_csv(decomposition, "decomposition_stl.csv", index_label="Month")

    fig, ax = plt.subplots(figsize=(9, 4.2), constrained_layout=True)
    plot_correlogram(stl.resid, 40, ax,
                     "ACF of STL residuals (log scale)", COLORS["purple"],
                     highlight=(12, 24))
    ax.set_xlabel("Lag (months)")
    add_caption(fig, "If decomposition captured all structure, residuals would behave like "
                "white noise and every stem would sit inside the band. Stems outside the band "
                "show correlation that trend and seasonality did not explain.")
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
