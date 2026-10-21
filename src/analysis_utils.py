"""Shared plotting and statistics helpers. Prepared for the group by Thành."""
import os
from pathlib import Path

_mpl_config = Path(__file__).resolve().parents[1] / ".mplconfig"
_mpl_config.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_mpl_config))

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


def finish_axes(ax):
    ax.grid(True, alpha=0.22, linewidth=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_correlogram(series, lags, ax, title, color, method="acf"):
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
    ax.axhspan(-bound, bound, color="#DCEAF3", alpha=0.8,
               label=f"Approx. 95% band ±{bound:.3f}")
    ax.axhline(0, color="#333333", linewidth=0.8)
    ax.vlines(lag_numbers, 0, coefficients, color=color, linewidth=1.4)
    ax.scatter(lag_numbers, coefficients, color=color, s=20, zorder=3)
    ax.set(title=title, xlabel="Lag", ylabel=ylabel, xlim=(0, lags + 1))
    ax.legend(frameon=False, fontsize=8, loc="best")
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
