"""Exercise 1: ACF/PACF analysis of AirPassengers. Assigned to: Le Quynh."""
import bootstrap  # noqa: F401

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf

from analysis_utils import COLORS, finish_axes, plot_correlogram, save_csv, save_figure
from load_data import load_airpassengers
import matplotlib.pyplot as plt


def main():
    y = load_airpassengers()
    print("=== AirPassengers: descriptive statistics ===")
    print(y.head().to_string())
    print(y.describe().round(2).to_string())
    print(f"Observations: {y.size}; missing: {int(y.isna().sum())}")

    fig, ax = plt.subplots(figsize=(11, 4.5), constrained_layout=True)
    ax.plot(y.index, y, color=COLORS["blue"], linewidth=1.8)
    ax.set(title="Monthly AirPassengers (1949–1960)",
           xlabel="Month", ylabel="Passengers (thousands)")
    finish_axes(ax)
    save_figure(fig, "b1_line.png")

    fig, ax = plt.subplots(figsize=(10, 4.5), constrained_layout=True)
    plot_correlogram(y, 40, ax, "AirPassengers ACF (40 lags)",
                     COLORS["blue"], method="acf")
    ax.set_xlabel("Lag (months)")
    save_figure(fig, "b1_acf.png")

    fig, ax = plt.subplots(figsize=(10, 4.5), constrained_layout=True)
    plot_correlogram(y, 40, ax,
                     "AirPassengers PACF (40 lags; Yule–Walker method)",
                     COLORS["orange"], method="pacf")
    ax.set_xlabel("Lag (months)")
    save_figure(fig, "b1_pacf.png")

    acf_values = acf(y, nlags=40, fft=True)
    pacf_values = pacf(y, nlags=40, method="ywm")
    result = pd.DataFrame({
        "lag": np.arange(41),
        "acf": acf_values,
        "pacf_ywm": pacf_values,
    })
    save_csv(result, "b1_acf_pacf_values.csv", index_label="row")
    print("\nACF/PACF at the requested lags:")
    print(result.loc[result["lag"].isin([1, 12, 24, 36])].round(4).to_string(index=False))

    first_difference = y.diff().dropna()
    seasonal_difference = y.diff(12).dropna()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)
    plot_correlogram(first_difference, 40, axes[0],
                     "ACF after first differencing", COLORS["green"])
    plot_correlogram(seasonal_difference, 40, axes[1],
                     "ACF after seasonal differencing (lag 12)", COLORS["purple"])
    for ax in axes:
        ax.set_xlabel("Lag (months)")
    save_figure(fig, "b1_acf_differenced.png")


if __name__ == "__main__":
    main()
