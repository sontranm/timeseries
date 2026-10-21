"""Exercise 4b: detect outliers in the series and STL residuals. Assigned to: Hoang Thang."""
import bootstrap  # noqa: F401

import numpy as np
import pandas as pd

from analysis_utils import COLORS, finish_axes, save_csv, save_figure
from load_data import PROCESSED, load_airpassengers
import matplotlib.pyplot as plt


def _zscore(series: pd.Series) -> pd.Series:
    standard_deviation = series.std(ddof=0)
    if standard_deviation == 0:
        return pd.Series(0.0, index=series.index)
    return (series - series.mean()) / standard_deviation


def _iqr_bounds(series: pd.Series):
    first_quartile = series.quantile(0.25)
    third_quartile = series.quantile(0.75)
    spread = third_quartile - first_quartile
    return first_quartile - 1.5 * spread, third_quartile + 1.5 * spread


def main():
    original = load_airpassengers()
    decomposition = pd.read_csv(
        PROCESSED / "decomposition_stl.csv",
        parse_dates=["Month"],
        index_col="Month",
    )
    residual = decomposition["resid"].astype(float)

    residual_z = _zscore(residual)
    residual_iqr_low, residual_iqr_high = _iqr_bounds(residual)
    residual_z_flag = residual_z.abs() > 3
    residual_iqr_flag = (residual < residual_iqr_low) | (residual > residual_iqr_high)
    residual_consensus = residual_z_flag & residual_iqr_flag

    raw_z = _zscore(original)
    raw_iqr_low, raw_iqr_high = _iqr_bounds(original)
    raw_iqr_flag = (original < raw_iqr_low) | (original > raw_iqr_high)
    rolling_mean = original.rolling(window=12, min_periods=6).mean()
    rolling_std = original.rolling(window=12, min_periods=6).std()
    rolling_flag = (original - rolling_mean).abs() > 3 * rolling_std

    table = pd.DataFrame(
        {
            "Passengers": original,
            "STL_residual_log": residual,
            "residual_z_score": residual_z,
            "residual_z_outlier": residual_z_flag,
            "residual_iqr_outlier": residual_iqr_flag,
            "residual_consensus_outlier": residual_consensus,
            "raw_z_score": raw_z,
            "raw_z_outlier": raw_z.abs() > 3,
            "raw_iqr_outlier": raw_iqr_flag,
            "raw_rolling_mean_12": rolling_mean,
            "raw_rolling_std_12": rolling_std,
            "raw_rolling_3sd_outlier": rolling_flag,
        },
        index=original.index,
    )
    save_csv(table, "b4b_detection.csv", index_label="Month")

    # Synthetic check: add isolated, deliberately large deviations to a copy only.
    synthetic = residual.copy()
    injected_dates = pd.to_datetime(["1952-03-01", "1956-06-01", "1959-10-01"])
    injected_multipliers = [8.0, -8.0, 8.0]
    residual_sd = float(residual.std(ddof=0))
    for date, multiplier in zip(injected_dates, injected_multipliers):
        synthetic.loc[date] += multiplier * residual_sd
    synthetic_z = _zscore(synthetic)
    synthetic_low, synthetic_high = _iqr_bounds(synthetic)
    synthetic_iqr_flag = (synthetic < synthetic_low) | (synthetic > synthetic_high)
    test = pd.DataFrame(
        {
            "injected_residual": synthetic.loc[injected_dates],
            "z_score": synthetic_z.loc[injected_dates],
            "z_detected": synthetic_z.loc[injected_dates].abs() > 3,
            "iqr_detected": synthetic_iqr_flag.loc[injected_dates],
        },
        index=injected_dates,
    )
    test.index.name = "Month"
    save_csv(test, "b4b_synthetic_outlier_test.csv", index_label="Month")
    print("Synthetic outlier injection check:")
    print(test.to_string())

    counts = pd.DataFrame(
        [
            ("STL residual |z| > 3", int(residual_z_flag.sum())),
            ("STL residual IQR", int(residual_iqr_flag.sum())),
            ("STL residual both methods", int(residual_consensus.sum())),
            ("Raw series |z| > 3", int((raw_z.abs() > 3).sum())),
            ("Raw series IQR", int(raw_iqr_flag.sum())),
            ("Raw series rolling 3 SD", int(rolling_flag.sum())),
        ],
        columns=["method", "flagged_points"],
    )
    save_csv(counts, "b4b_method_counts.csv", index_label="row")
    print("\nOutlier counts by method:")
    print(counts.to_string(index=False))

    flagged_dates = residual_consensus[residual_consensus].index
    cleaned = original.copy()
    if len(flagged_dates):
        cleaned.loc[flagged_dates] = cleaned.interpolate(method="linear").loc[flagged_dates]
        print("Consensus outlier candidates interpolated:",
              ", ".join(date.strftime("%Y-%m") for date in flagged_dates))
    else:
        print("No point was flagged by both residual Z-score and residual IQR; "
              "the original series is retained.")
    cleaned.rename("Passengers").to_csv(
        PROCESSED / "airpassengers_clean.csv",
        index_label="Month",
    )

    fig, ax = plt.subplots(figsize=(11, 4.5), constrained_layout=True)
    ax.plot(residual.index, residual, color=COLORS["blue"], linewidth=1.2,
            label="STL residual (log scale)")
    ax.scatter(residual_z_flag[residual_z_flag].index,
               residual.loc[residual_z_flag], marker="s", s=45,
               color=COLORS["orange"], label="Z-score |z| > 3")
    ax.scatter(residual_iqr_flag[residual_iqr_flag].index,
               residual.loc[residual_iqr_flag], marker="^", s=45,
               facecolors="none", edgecolors=COLORS["purple"],
               label="IQR fence")
    if len(flagged_dates):
        ax.scatter(flagged_dates, residual.loc[flagged_dates], marker="o", s=85,
                   color=COLORS["vermillion"], label="Both methods", zorder=4)
    ax.axhline(residual_iqr_low, color=COLORS["purple"], linestyle=":", linewidth=1)
    ax.axhline(residual_iqr_high, color=COLORS["purple"], linestyle=":", linewidth=1)
    ax.set(title="Outlier candidates in robust STL residuals",
           xlabel="Month", ylabel="Residual on log scale")
    ax.legend(ncols=2, frameon=False, fontsize=8)
    finish_axes(ax)
    save_figure(fig, "b4b_outlier.png")

    fig, ax = plt.subplots(figsize=(11, 4.5), constrained_layout=True)
    ax.plot(original.index, original, color=COLORS["gray"], linewidth=1.7,
            label="Original AirPassengers")
    ax.plot(cleaned.index, cleaned, color=COLORS["green"], linewidth=1.1,
            linestyle="--", label="After consensus outlier handling")
    if len(flagged_dates):
        ax.scatter(flagged_dates, original.loc[flagged_dates], color=COLORS["vermillion"],
                   marker="x", s=60, label="Interpolated candidates", zorder=3)
    ax.set(title="AirPassengers before and after outlier handling",
           xlabel="Month", ylabel="Passengers (thousands)")
    ax.legend(frameon=False)
    finish_axes(ax)
    save_figure(fig, "b4b_before_after.png")


if __name__ == "__main__":
    main()
