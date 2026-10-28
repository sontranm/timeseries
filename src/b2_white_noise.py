"""Exercise 2: white-noise simulation and Ljung–Box test. Assigned to: Pham Le Van Bao."""
import bootstrap  # noqa: F401

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

from analysis_utils import (
    COLORS, add_caption, add_mean_line, finish_axes, ljung_box_rows, plot_correlogram,
    save_csv, save_figure
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

    sd = float(white_noise.std())
    fig, ax = plt.subplots(figsize=(11, 4.6), constrained_layout=True)
    ax.axhspan(-1.96 * sd, 1.96 * sd, color="#DCEAF3", alpha=0.6,
               label=f"Mean ± 1.96 SD (≈95% of values; SD = {sd:.2f})")
    ax.plot(white_noise.index, white_noise, color=COLORS["blue"], linewidth=0.7,
            label="Simulated value ε_t ~ N(0, 1)")
    ax.axhline(0, color=COLORS["green"], linewidth=1.0, linestyle=":",
               label="Theoretical mean = 0")
    add_mean_line(ax, white_noise, label="Sample mean", fmt=".3f")
    ax.set(title="Simulated Gaussian white noise (n = 1,000; seed = 42): constant mean and spread",
           xlabel="Sample index (t)", ylabel="Value")
    ax.legend(frameon=False, fontsize=8, ncols=2, loc="upper left")
    ax.set_ylim(white_noise.min() - 0.5, white_noise.max() + 1.6)
    finish_axes(ax)
    add_caption(fig, "Each point is an independent draw from a normal distribution with mean 0 "
                "and SD 1. The sample mean (dashed) stays on the theoretical mean 0 and the "
                "spread stays inside the same band throughout: no trend, no seasonality, no "
                "pattern. This is the benchmark for a series with no predictable structure.")
    save_figure(fig, "b2_white_noise_line.png")

    fig, ax = plt.subplots(figsize=(9, 4.6), constrained_layout=True)
    plot_correlogram(white_noise, 40, ax,
                     "White-noise ACF (40 lags): almost all lags inside the band",
                     COLORS["blue"])
    add_caption(fig, "For white noise the true autocorrelation is 0 at every lag. About 5% of "
                "lags (≈2 of 40) may exceed the 95% band by chance alone.")
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
    fig.suptitle("ACF comparison: random series vs. structured series", fontweight="bold")
    add_caption(fig, "Left: white-noise coefficients scatter around 0 inside the band (no memory). "
                "Right: AirPassengers coefficients are large, positive and decay slowly with "
                "peaks every 12 lags, so the series has trend and seasonality.")
    save_figure(fig, "b2_acf_comparison.png")

    rows = ljung_box_rows(white_noise, "White noise (n=1000)")
    rows.extend(ljung_box_rows(passengers, "AirPassengers (n=144)"))
    table = pd.DataFrame(rows)
    save_csv(table, "b2_ljung_box.csv", index_label="row")
    print("\nLjung–Box test:")
    print(table.round(5).to_string(index=False))


if __name__ == "__main__":
    main()
