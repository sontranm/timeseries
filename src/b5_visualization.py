"""Exercise 5: visualize trend and seasonality. Assigned to: Hoang Nam."""
import bootstrap  # noqa: F401

import pandas as pd

from analysis_utils import COLORS, finish_axes, save_figure
from load_data import load_airpassengers
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    passengers = load_airpassengers()
    frame = passengers.rename("Passengers").to_frame()
    frame["Year"] = frame.index.year
    frame["Month"] = frame.index.month

    fig, ax = plt.subplots(figsize=(11, 4.5), constrained_layout=True)
    ax.plot(passengers.index, passengers, color=COLORS["blue"], linewidth=1.7)
    ax.set(title="AirPassengers: monthly observations, 1949–1960",
           xlabel="Month", ylabel="Passengers (thousands)")
    finish_axes(ax)
    save_figure(fig, "b5_line.png")

    rolling_mean = passengers.rolling(window=12, min_periods=12).mean()
    rolling_std = passengers.rolling(window=12, min_periods=12).std()
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                             constrained_layout=True)
    axes[0].plot(passengers.index, passengers, color=COLORS["blue"], alpha=0.65,
                 linewidth=1.0, label="Observed")
    axes[0].plot(rolling_mean.index, rolling_mean, color=COLORS["vermillion"],
                 linewidth=2, label="12-month rolling mean")
    axes[0].set_ylabel("Passengers (thousands)")
    axes[0].legend(frameon=False)
    axes[1].plot(rolling_std.index, rolling_std, color=COLORS["green"], linewidth=1.8)
    axes[1].set_ylabel("Rolling SD (thousands)")
    axes[1].set_xlabel("Month")
    axes[1].set_title("12-month rolling standard deviation")
    for ax in axes:
        finish_axes(ax)
    save_figure(fig, "b5_rolling.png")

    seasonal = frame.pivot(index="Month", columns="Year", values="Passengers")
    fig, ax = plt.subplots(figsize=(10.5, 5.5), constrained_layout=True)
    palette = plt.colormaps["tab20"].resampled(len(seasonal.columns))
    for i, year in enumerate(seasonal.columns):
        ax.plot(seasonal.index, seasonal[year], marker="o", markersize=3.5,
                linewidth=1.3, color=palette(i), label=str(year))
    ax.set(title="Seasonal plot: each line is one calendar year",
           xlabel="Month", ylabel="Passengers (thousands)",
           xticks=range(1, 13))
    ax.legend(title="Year", ncols=3, frameon=False, fontsize=8)
    finish_axes(ax)
    save_figure(fig, "b5_seasonal.png")

    fig, ax = plt.subplots(figsize=(10.5, 5.5), constrained_layout=True)
    sns.heatmap(
        seasonal,
        ax=ax,
        cmap="YlGnBu",
        annot=True,
        fmt=".0f",
        linewidths=0.35,
        linecolor="white",
        cbar_kws={"label": "Passengers (thousands)"},
    )
    ax.set(title="Monthly passenger counts by year",
           xlabel="Year", ylabel="Month")
    save_figure(fig, "b5_heatmap.png")

    monthly = [passengers[passengers.index.month == month].to_numpy()
               for month in range(1, 13)]
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    box = ax.boxplot(
        monthly,
        tick_labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        patch_artist=True,
        medianprops={"color": "#222222", "linewidth": 1.4},
        flierprops={"marker": "o", "markersize": 3, "alpha": 0.55},
    )
    for patch in box["boxes"]:
        patch.set_facecolor("#56B4E9")
        patch.set_alpha(0.65)
    ax.set(title="AirPassengers distribution by calendar month",
           xlabel="Month", ylabel="Passengers (thousands)")
    finish_axes(ax)
    save_figure(fig, "b5_boxplot.png")

    monthly_median = frame.groupby(frame["Month"], sort=True)["Passengers"].median()
    print("Lowest monthly median:", int(monthly_median.idxmin()),
          "highest monthly median:", int(monthly_median.idxmax()))
    print("Annual means:")
    print(frame.groupby("Year")["Passengers"].mean().round(1).to_string())


if __name__ == "__main__":
    main()
