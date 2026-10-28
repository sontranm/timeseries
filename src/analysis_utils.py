"""Shared plotting and statistics helpers. Prepared for the group by Thành."""
import os
from pathlib import Path

_mpl_config = Path(__file__).resolve().parents[1] / ".mplconfig"
_mpl_config.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_mpl_config))

import textwrap

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf, pacf

from load_data import FIG, PROCESSED


COLORS = {
    "blue": "#0072B2",
    "orange": "#E69F00",
    "green": "#009E73",
    "vermillion": "#D55E00",
    "purple": "#CC79A7",
    "sky": "#56B4E9",
    "gray": "#666666",
}
MEAN_COLOR = "#222222"


def finish_axes(ax):
    ax.grid(True, alpha=0.22, linewidth=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def year_axis(ax):
    """Label a date axis with one tick per calendar year."""
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


def add_mean_line(ax, series, label="Mean", unit="", fmt=".1f", color=MEAN_COLOR):
    """Draw the sample mean as a dashed line, in the legend and at the right edge."""
    mean = float(pd.Series(series).mean())
    ax.axhline(mean, color=color, linestyle="--", linewidth=1.3, zorder=2.5,
               label=f"{label} = {mean:{fmt}}{unit}")
    ax.annotate(f"{label} {mean:{fmt}}", xy=(1.0, mean),
                xycoords=("axes fraction", "data"), xytext=(4, 0),
                textcoords="offset points", va="center", ha="left",
                fontsize=8, color=color, fontweight="bold")
    return mean


def annotate_extremes(ax, series, unit="", fmt=".0f", date_fmt="%b %Y"):
    """Mark and label the maximum and minimum observations."""
    series = pd.Series(series).dropna()
    for position, name, offset, align in (
        (series.idxmax(), "Max", (-12, 6), "right"),
        (series.idxmin(), "Min", (12, -4), "left"),
    ):
        value = series.loc[position]
        ax.scatter([position], [value], color=COLORS["vermillion"], s=32, zorder=4)
        when = position.strftime(date_fmt) if hasattr(position, "strftime") else position
        ax.annotate(f"{name}: {value:{fmt}}{unit} ({when})", xy=(position, value),
                    xytext=offset, textcoords="offset points", ha=align,
                    fontsize=8, color=COLORS["vermillion"])


def add_caption(fig, text):
    """Add a plain-language guide under the figure: what is shown and how to read it."""
    width = int(fig.get_figwidth() * 15)
    fig.text(0.01, -0.01, textwrap.fill(text, width), ha="left", va="top",
             fontsize=8.8, color="#333333", style="italic")


def plot_correlogram(series, lags, ax, title, color, method="acf", highlight=()):
    """Plot ACF/PACF coefficients with a zero-centred ±1.96/sqrt(n) reference band."""
    values = pd.Series(series).dropna().to_numpy(dtype=float)
    if method == "acf":
        coefficients = acf(values, nlags=lags, fft=True)[1:]
        ylabel = "Autocorrelation"
    elif method == "pacf":
        coefficients = pacf(values, nlags=lags, method="ywm")[1:]
        ylabel = "Partial autocorrelation"
    else:
        raise ValueError("method must be 'acf' or 'pacf'")
    lag_numbers = np.arange(1, lags + 1)
    bound = 1.96 / np.sqrt(len(values))
    outside = int(np.sum(np.abs(coefficients) > bound))
    ax.axhspan(-bound, bound, color="#DCEAF3", alpha=0.8,
               label=f"95% band ±{bound:.3f} (inside = not significant)")
    ax.axhline(0, color=MEAN_COLOR, linewidth=1.0, linestyle="--",
               label="0 = no correlation (expected for white noise)")
    ax.vlines(lag_numbers, 0, coefficients, color=color, linewidth=1.4)
    ax.scatter(lag_numbers, coefficients, color=color, s=20, zorder=3,
               label=f"Coefficient ({outside}/{lags} lags outside band)")
    for lag in highlight:
        if 1 <= lag <= lags:
            value = coefficients[lag - 1]
            ax.axvline(lag, color=COLORS["gray"], linewidth=0.8, linestyle=":", zorder=1)
            ax.annotate(f"lag {lag}\n{value:.2f}", xy=(lag, value),
                        xytext=(0, 8 if value >= 0 else -22), textcoords="offset points",
                        ha="center", fontsize=8, color=MEAN_COLOR)
    low = min(coefficients.min(), -bound)
    high = max(coefficients.max(), bound)
    span = high - low
    # Headroom above the stems keeps the legend and lag labels off the data.
    ax.set(title=title, xlabel="Lag", ylabel=ylabel, xlim=(0, lags + 1),
           ylim=(low - 0.15 * span, high + 0.45 * span))
    ax.set_yticks([tick for tick in ax.get_yticks() if -1 <= tick <= 1])
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    finish_axes(ax)
    return coefficients


def save_figure(fig, filename: str) -> Path:
    path = FIG / filename
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def save_csv(frame: pd.DataFrame, filename: str, index_label: str | None = None) -> Path:
    path = PROCESSED / filename
    frame.to_csv(path, index_label=index_label)
    return path


def ljung_box_rows(series: pd.Series, label: str, lags=(10, 20)) -> list[dict]:
    result = acorr_ljungbox(series.dropna(), lags=list(lags), return_df=True)
    return [
        {
            "series": label,
            "lag": int(lag),
            "lb_stat": float(row["lb_stat"]),
            "p_value": float(row["lb_pvalue"]),
        }
        for lag, row in result.iterrows()
    ]
