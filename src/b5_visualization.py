"""Exercise 5: visualize trend and seasonality. Assigned to: Hoang Nam."""
import bootstrap  # noqa: F401

import pandas as pd

from analysis_utils import (
    COLORS, MEAN_COLOR, add_caption, add_mean_line, annotate_extremes, finish_axes,
    save_figure, year_axis
)
from load_data import load_airpassengers
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    passengers = load_airpassengers()
    frame = passengers.rename("Passengers").to_frame()
    frame["Year"] = frame.index.year
    frame["Month"] = frame.index.month

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, ax = plt.subplots(figsize=(11, 4.8), constrained_layout=True)
    ax.plot(passengers.index, passengers, color=COLORS["blue"], linewidth=1.7,
            label="Monthly passengers")
    add_mean_line(ax, passengers, label="Overall mean", unit="k")
    annotate_extremes(ax, passengers, unit="k")
    ax.set(title="AirPassengers: monthly observations, 1949–1960",
           xlabel="Year", ylabel="Passengers (thousands)")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    year_axis(ax)
    finish_axes(ax)
    add_caption(fig, "The line climbs from about 100k to over 600k (trend) and has a peak every "
                "summer (seasonality). Before about 1955 almost every month is below the overall "
                "mean (dashed); afterwards almost every month is above it, so a single mean does "
                "not describe the series well.")
    save_figure(fig, "b5_line.png")

    rolling_mean = passengers.rolling(window=12, min_periods=12).mean()
    rolling_std = passengers.rolling(window=12, min_periods=12).std()
    fig, axes = plt.subplots(2, 1, figsize=(11, 7.5), sharex=True,
                             constrained_layout=True)
    axes[0].plot(passengers.index, passengers, color=COLORS["blue"], alpha=0.65,
                 linewidth=1.0, label="Observed")
    axes[0].plot(rolling_mean.index, rolling_mean, color=COLORS["vermillion"],
                 linewidth=2, label="12-month rolling mean (local level)")
    add_mean_line(axes[0], passengers, label="Overall mean", unit="k")
    axes[0].set_ylabel("Passengers (thousands)")
    axes[0].set_title("Observed series and 12-month rolling mean")
    axes[0].legend(frameon=False, fontsize=8, loc="upper left")
    axes[1].plot(rolling_std.index, rolling_std, color=COLORS["green"], linewidth=1.8,
                 label="12-month rolling SD (local spread)")
    add_mean_line(axes[1], rolling_std.dropna(), label="Mean SD", unit="k")
    axes[1].set_ylabel("Rolling SD (thousands)")
    axes[1].set_xlabel("Year")
    axes[1].set_title("12-month rolling standard deviation")
    axes[1].legend(frameon=False, fontsize=8, loc="upper left")
    year_axis(axes[1])
    for ax in axes:
        finish_axes(ax)
    fig.suptitle("Rolling statistics: both the level and the spread change over time",
                 fontweight="bold")
    add_caption(fig, "Top: the rolling mean averages the last 12 months, removing the seasonal "
                "swings; it rises steadily and crosses the overall mean, so the mean is not "
                "constant. Bottom: the rolling SD also increases over time (from below to above "
                "its average), so the variance is not constant either. Both indicate a "
                "non-stationary series; a log transform and differencing are needed before "
                "ARIMA-type modelling. The first 11 months are empty because a full 12-month "
                "window is required.")
    save_figure(fig, "b5_rolling.png")

    seasonal = frame.pivot(index="Month", columns="Year", values="Passengers")
    fig, ax = plt.subplots(figsize=(11, 6), constrained_layout=True)
    palette = plt.colormaps["viridis"].resampled(len(seasonal.columns))
    for i, year in enumerate(seasonal.columns):
        ax.plot(seasonal.index, seasonal[year], marker="o", markersize=3,
                linewidth=1.1, alpha=0.8, color=palette(i), label=str(year))
    monthly_mean = seasonal.mean(axis=1)
    ax.plot(monthly_mean.index, monthly_mean, color=MEAN_COLOR, linewidth=2.6,
            marker="D", markersize=5, label="Mean of 12 years")
    add_mean_line(ax, passengers, label="Overall mean", unit="k")
    ax.set(title="Seasonal plot: each line is one calendar year, black = monthly mean",
           xlabel="Month", ylabel="Passengers (thousands)", xticks=range(1, 13))
    ax.set_xticklabels(month_names)
    ax.legend(title="Year (dark → light = early → late)", ncols=3, frameon=False,
              fontsize=8, loc="upper left")
    finish_axes(ax)
    add_caption(fig, "Every year follows the same shape: low in Jan–Feb and Nov, rising through "
                "spring and peaking in July–August. Later years (lighter colours) sit higher, "
                "showing the trend, and their summer peaks are taller, showing that the seasonal "
                "swing grows with the level.")
    save_figure(fig, "b5_seasonal.png")

    with_means = seasonal.copy()
    with_means["Month mean"] = seasonal.mean(axis=1)
    with_means.loc["Year mean"] = with_means.mean(axis=0)
    with_means.index = month_names + ["Year mean"]
    fig, ax = plt.subplots(figsize=(12, 6.5), constrained_layout=True)
    sns.heatmap(
        with_means,
        ax=ax,
        cmap="YlGnBu",
        annot=True,
        fmt=".0f",
        linewidths=0.35,
        linecolor="white",
        cbar_kws={"label": "Passengers (thousands)"},
    )
    ax.axhline(12, color=MEAN_COLOR, linewidth=2.5)
    ax.axvline(len(seasonal.columns), color=MEAN_COLOR, linewidth=2.5)
    ax.set(title="Monthly passenger counts by year, with year and month means",
           xlabel="Year", ylabel="Month")
    ax.tick_params(axis="y", rotation=0)
    add_caption(fig, "Each cell is the passenger count for one month of one year; darker = more "
                "passengers. Bottom row: mean of each year (rises every year = trend). Right "
                "column: mean of each month across 12 years (highest in Jul–Aug = seasonality). "
                "Colour darkens from left to right and is darkest in the middle rows.")
    save_figure(fig, "b5_heatmap.png")

    monthly = [passengers[passengers.index.month == month].to_numpy()
               for month in range(1, 13)]
    fig, ax = plt.subplots(figsize=(10.5, 5.4), constrained_layout=True)
    box = ax.boxplot(
        monthly,
        tick_labels=month_names,
        patch_artist=True,
        showmeans=True,
        meanprops={"marker": "D", "markerfacecolor": COLORS["vermillion"],
                   "markeredgecolor": "white", "markersize": 6},
        medianprops={"color": "#222222", "linewidth": 1.4},
        flierprops={"marker": "o", "markersize": 3, "alpha": 0.55},
    )
    for patch in box["boxes"]:
        patch.set_facecolor("#56B4E9")
        patch.set_alpha(0.65)
    add_mean_line(ax, passengers, label="Overall mean", unit="k")
    ax.legend(
        [box["boxes"][0], box["medians"][0], box["means"][0], ax.get_lines()[-1]],
        ["Middle 50% of the 12 years (Q1–Q3)", "Median", "Month mean",
         f"Overall mean = {passengers.mean():.1f}k"],
        frameon=False, fontsize=8, loc="upper left",
    )
    ax.set(title="AirPassengers distribution by calendar month (12 values per box)",
           xlabel="Month", ylabel="Passengers (thousands)")
    finish_axes(ax)
    add_caption(fig, "Each box summarises the 12 values of one calendar month (1949–1960). Box = "
                "middle 50%, black bar = median, red diamond = mean, whiskers = range without "
                "outliers. July and August have the highest centre and lie well above the overall "
                "mean; November and January–February are lowest. Tall boxes reflect the upward "
                "trend across years.")
    save_figure(fig, "b5_boxplot.png")

    monthly_median = frame.groupby(frame["Month"], sort=True)["Passengers"].median()
    print("Lowest monthly median:", int(monthly_median.idxmin()),
          "highest monthly median:", int(monthly_median.idxmax()))
    print("Annual means:")
    print(frame.groupby("Year")["Passengers"].mean().round(1).to_string())


if __name__ == "__main__":
    main()
