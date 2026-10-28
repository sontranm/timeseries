"""Exercise 4a: simulate and handle missing values. Assigned to: Tran Minh Son."""
import bootstrap  # noqa: F401

import numpy as np
import pandas as pd

from analysis_utils import (
    COLORS, add_caption, add_mean_line, finish_axes, save_csv, save_figure, year_axis
)
from load_data import PROCESSED, load_airpassengers, load_temperatures
import matplotlib.pyplot as plt


def _mae(filled: pd.Series, original: pd.Series, index) -> float:
    return float((filled.loc[index] - original.loc[index]).abs().mean())


def main():
    np.random.seed(42)
    original = load_airpassengers()
    block = original.loc["1955-06-01":"1955-08-01"].index
    candidates = original.index[1:-1].difference(block)
    random_index = pd.DatetimeIndex(
        np.random.choice(candidates, size=12, replace=False)
    ).sort_values()
    missing_index = block.union(random_index).sort_values()

    holed = original.copy()
    holed.loc[missing_index] = np.nan
    forward_filled = holed.ffill()
    interpolated = holed.interpolate(method="linear")
    metrics = pd.DataFrame(
        {
            "ffill_MAE": [
                _mae(forward_filled, original, missing_index),
                _mae(forward_filled, original, random_index),
                _mae(forward_filled, original, block),
            ],
            "linear_interpolation_MAE": [
                _mae(interpolated, original, missing_index),
                _mae(interpolated, original, random_index),
                _mae(interpolated, original, block),
            ],
        },
        index=["all_15_missing", "12_random_missing", "3_consecutive_missing"],
    )
    metrics.to_csv(PROCESSED / "b4a_mae.csv", index_label="evaluation_group")
    print("AirPassengers missing count:", int(holed.isna().sum()))
    print("Missing months:", ", ".join(date.strftime("%Y-%m") for date in missing_index))
    print("MAE by imputation method:")
    print(metrics.round(2).to_string())

    fig, ax = plt.subplots(figsize=(12, 5.4), constrained_layout=True)
    for i, date in enumerate(missing_index):
        ax.axvspan(date - pd.Timedelta(days=15), date + pd.Timedelta(days=15),
                   color="#F3E3C3", alpha=0.7, zorder=0,
                   label="Simulated missing month" if i == 0 else None)
    ax.plot(original.index, original, color="#B7C0C8", linewidth=1.5,
            linestyle="--", label="Original values (reference)")
    ax.plot(holed.index, holed, color=COLORS["blue"], linewidth=1.2,
            marker=".", markersize=3, label="Observed series with gaps")
    ax.scatter(missing_index, forward_filled.loc[missing_index], color=COLORS["orange"],
               marker="s", s=36, label="Forward fill at missing months", zorder=3)
    ax.scatter(missing_index, interpolated.loc[missing_index], color=COLORS["green"],
               marker="^", s=38, label="Linear interpolation at missing months", zorder=3)
    add_mean_line(ax, original, label="Mean", unit="k")
    ffill_mae = metrics.loc["all_15_missing", "ffill_MAE"]
    linear_mae = metrics.loc["all_15_missing", "linear_interpolation_MAE"]
    ax.set(title="AirPassengers: 15 simulated missing values filled by two methods "
                 f"(MAE: forward fill {ffill_mae:.1f}k, linear {linear_mae:.1f}k)",
           xlabel="Year", ylabel="Passengers (thousands)")
    ax.legend(ncols=3, frameon=False, fontsize=8, loc="upper left")
    year_axis(ax)
    finish_axes(ax)
    add_caption(fig, "Shaded columns mark the 15 months deleted on purpose (12 random + 3 in a "
                "row, Jun–Aug 1955). Grey dashed line: the true values. Orange squares repeat "
                "the last known value (forward fill); green triangles draw a straight line "
                "between neighbours (linear interpolation). The closer a marker is to the grey "
                "line, the better the estimate. MAE = mean absolute error over the 15 months.")
    save_figure(fig, "b4a_missing_imputation.png")

    temperatures = load_temperatures()
    daily = temperatures.asfreq("D")
    missing_days = daily.index[daily.isna()]
    temperature_filled = daily.interpolate(method="linear")
    temperature_filled.rename("Temp").to_csv(
        PROCESSED / "temperatures_filled.csv", index_label="Date"
    )
    best_method = (
        "linear_interpolation"
        if metrics.loc["all_15_missing", "linear_interpolation_MAE"]
        <= metrics.loc["all_15_missing", "ffill_MAE"]
        else "ffill"
    )
    best_series = interpolated if best_method == "linear_interpolation" else forward_filled
    best_series.rename("Passengers").to_csv(
        PROCESSED / "airpassengers_filled.csv", index_label="Month"
    )

    print(f"Daily temperature observations: {int(temperatures.notna().sum())}")
    print(f"Calendar days after asfreq('D'): {len(daily)}")
    print("Missing dates revealed by daily frequency:",
          ", ".join(date.strftime("%Y-%m-%d") for date in missing_days))
    for date in missing_days:
        print(f"Linear estimate for {date:%Y-%m-%d}: "
              f"{temperature_filled.loc[date]:.2f} °C")
    print(f"Saved best AirPassengers fill ({best_method}) and temperature fill.")

    fig, axes = plt.subplots(1, max(1, len(missing_days)), figsize=(12, 4.5),
                             squeeze=False, constrained_layout=True)
    for ax, date in zip(axes[0], missing_days):
        window_start = date - pd.Timedelta(days=15)
        window_end = date + pd.Timedelta(days=15)
        window = daily.loc[window_start:window_end]
        ax.plot(window, color=COLORS["blue"],
                marker=".", linewidth=1, label="Observed daily minimum")
        ax.axvline(date, color=COLORS["vermillion"], linewidth=0.8, linestyle=":")
        ax.scatter([date], [temperature_filled.loc[date]], color=COLORS["vermillion"],
                   marker="^", s=70, zorder=3, label="Linear estimate for the missing day")
        add_mean_line(ax, window, label="31-day mean", unit=" °C")
        ax.set(title=f"Missing day {date:%Y-%m-%d}: estimate "
                     f"{temperature_filled.loc[date]:.2f} °C",
               xlabel="Date", ylabel="Minimum temperature (°C)")
        ax.tick_params(axis="x", rotation=35)
        low, high = ax.get_ylim()
        ax.set_ylim(low, high + 0.3 * (high - low))
        ax.legend(frameon=False, fontsize=8, ncols=2, loc="upper left")
        finish_axes(ax)
    fig.suptitle("Melbourne daily minimum temperature: the two dates absent from the file "
                 "(±15 days shown)", fontweight="bold")
    add_caption(fig, "After reindexing to one row per calendar day, these two dates had no value. "
                "Blue: observed temperatures in the surrounding month; the gap is at the dotted "
                "line. Red triangle: value estimated by joining the day before and the day after "
                "with a straight line. Dashed line: mean of the window, for comparison.")
    save_figure(fig, "b4a_temperature_gaps.png")


if __name__ == "__main__":
    main()
