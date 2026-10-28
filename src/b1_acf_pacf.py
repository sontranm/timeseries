"""Bài 1: Phân tích ACF và PACF của chuỗi AirPassengers."""

import bootstrap  # noqa: F401

import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import acf, pacf

from analysis_utils import (
    COLORS, add_caption, add_mean_line, annotate_extremes, finish_axes,
    plot_correlogram, save_figure, year_axis
)
from load_data import load_airpassengers


# Đọc dữ liệu AirPassengers
y = load_airpassengers()


# ==============================
# 1. KIỂM TRA DỮ LIỆU
# ==============================

print("===== 5 DONG DAU =====")
print(y.head())

print("\n===== THONG TIN =====")
y.info()

print("\n===== THONG KE MO TA =====")
print(y.describe())

# ==============================
# 2. VE LINE CHART
# ==============================

# Trung binh tung nam (bac thang) va trung binh toan chuoi (net dut)
annual_mean = y.groupby(y.index.year).transform("mean")

fig, ax = plt.subplots(figsize=(11, 4.8), constrained_layout=True)

ax.plot(y.index, y, color=COLORS["blue"], linewidth=1.8,
        label="Monthly passengers")
ax.plot(annual_mean.index, annual_mean, color=COLORS["orange"], linewidth=1.6,
        drawstyle="steps-post", label="Annual mean (one level per year)")
add_mean_line(ax, y, label="Overall mean", unit="k")
annotate_extremes(ax, y, unit="k")

ax.set(title="Monthly AirPassengers (1949–1960): rising trend with yearly peaks",
       xlabel="Year", ylabel="Passengers (thousands)")
ax.legend(frameon=False, fontsize=8, loc="upper left")
year_axis(ax)
finish_axes(ax)
add_caption(fig, "Blue line: number of international airline passengers each month. "
            "Orange steps: average of each year, which rises every year, so the series "
            "has an upward trend. Dashed black line: mean of all 144 months; early years lie "
            "below it and later years above it, so the series is not stationary around one "
            "level. The swings around the steps grow over time, showing multiplicative "
            "seasonality.")

save_figure(fig, "b1_line.png")

# ==============================
# 3. VE ACF 40 LAGS
# ==============================

fig, ax = plt.subplots(figsize=(10, 4.8), constrained_layout=True)

plot_correlogram(y, 40, ax, "AirPassengers ACF (40 lags): slow decay, peaks every 12 months",
                 COLORS["blue"], method="acf", highlight=(12, 24, 36))

ax.set_xlabel("Lag (months)")
add_caption(fig, "Each stem is the correlation between the series and itself shifted by k "
            "months. Stems outside the blue band are statistically significant. The slow "
            "decay from lag 1 indicates trend; the local peaks at lags 12, 24, 36 indicate "
            "annual seasonality.")

save_figure(fig, "b1_acf.png")

# ==============================
# 4. VE PACF 40 LAGS
# ==============================

fig, ax = plt.subplots(figsize=(10, 4.8), constrained_layout=True)

plot_correlogram(y, 40, ax,
                 "AirPassengers PACF (40 lags; Yule–Walker): dominant spike at lag 1",
                 COLORS["orange"], method="pacf", highlight=(1, 13))

ax.set_xlabel("Lag (months)")
add_caption(fig, "PACF measures the direct correlation at lag k after removing the effect "
            "of shorter lags. The large spike at lag 1 means each month depends mainly on the "
            "previous month; the negative spike at lag 13 reflects the annual seasonal pattern.")

save_figure(fig, "b1_pacf.png")

# ==============================
# 5. TINH GIA TRI ACF VA PACF
# ==============================

acf_values = acf(y, nlags=40)

pacf_values = pacf(
    y,
    nlags=40,
    method="ywm"
)


# Cac lag can quan tam
important_lags = [1, 12, 24, 36]


print("\n===== ACF VA PACF TAI CAC LAG QUAN TRONG =====")
print("Lag\tACF\t\tPACF")

for lag in important_lags:
    print(
        f"{lag}\t"
        f"{acf_values[lag]:.4f}\t\t"
        f"{pacf_values[lag]:.4f}"
    )