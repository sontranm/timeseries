"""Exercise 2: white-noise simulation and Ljung–Box test. Assigned to: Pham Le Van Bao."""
import bootstrap  # noqa: F401

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

from analysis_utils import (
    COLORS, finish_axes, ljung_box_rows, plot_correlogram, save_csv, save_figure
)
from load_data import PROCESSED, load_airpassengers
import matplotlib.pyplot as plt


def main():
    np.random.seed(42)
    white_noise = pd.Series(
        np.random.normal(loc=0.0, scale=1.0, size=1000),
        index=pd.RangeIndex(1, 1001, name="Sample"),
        name="WhiteNoise",
    )
    white_noise.to_csv(PROCESSED / "white_noise.csv", index_label="Sample")
    passengers = load_airpassengers()

    fig, ax = plt.subplots(figsize=(11, 4.2), constrained_layout=True)
    ax.plot(white_noise.index, white_noise, color=COLORS["blue"], linewidth=0.8)
    ax.axhline(0, color=COLORS["gray"], linewidth=0.8)
    ax.set(title="Simulated Gaussian white noise (n = 1,000; seed = 42)",
           xlabel="Sample index", ylabel="Value")
    finish_axes(ax)
    save_figure(fig, "b2_white_noise_line.png")

    fig, ax = plt.subplots(figsize=(9, 4.2), constrained_layout=True)
    plot_correlogram(white_noise, 40, ax,
                     "White-noise ACF (40 lags)", COLORS["blue"])
    save_figure(fig, "b2_white_noise_acf.png")

    wn_acf = acf(white_noise, nlags=40, fft=True)
    bound = 1.96 / np.sqrt(white_noise.size)
    exceed_count = int(np.sum(np.abs(wn_acf[1:]) > bound))
    print(f"White-noise ACF exceeds ±{bound:.4f} at {exceed_count}/40 lags.")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4), constrained_layout=True)
    plot_correlogram(white_noise, 40, axes[0], "White noise (n = 1,000)",
                     COLORS["blue"])
    plot_correlogram(passengers, 40, axes[1], "AirPassengers (n = 144)",
                     COLORS["orange"])
    for ax in axes:
        ax.set_xlabel("Lag")
    save_figure(fig, "b2_acf_comparison.png")

    rows = ljung_box_rows(white_noise, "White noise (n=1000)")
    rows.extend(ljung_box_rows(passengers, "AirPassengers (n=144)"))
    table = pd.DataFrame(rows)
    save_csv(table, "b2_ljung_box.csv", index_label="row")
    print("\nLjung–Box test:")
    print(table.round(5).to_string(index=False))


if __name__ == "__main__":
    main()
