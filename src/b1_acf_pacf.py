"""Bài 1: Phân tích ACF và PACF của chuỗi AirPassengers."""

import matplotlib.pyplot as plt

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, pacf

from load_data import load_airpassengers, FIG


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

plt.figure(figsize=(12, 6))

plt.plot(y.index, y.values)

plt.title("AirPassengers - Monthly Passengers")
plt.xlabel("Time")
plt.ylabel("Passengers (thousands)")

plt.grid(True)
plt.tight_layout()

plt.savefig(FIG / "b1_line.png", dpi=300)

plt.show()

# ==============================
# 3. VE ACF 40 LAGS
# ==============================

fig, ax = plt.subplots(figsize=(12, 6))

plot_acf(y, lags=40, ax=ax)

ax.set_title("ACF - AirPassengers (40 lags)")
ax.set_xlabel("Lag")
ax.set_ylabel("Autocorrelation")

plt.tight_layout()

plt.savefig(FIG / "b1_acf.png", dpi=300)

plt.show()

# ==============================
# 4. VE PACF 40 LAGS
# ==============================

fig, ax = plt.subplots(figsize=(12, 6))

plot_pacf(y, lags=40, method="ywm", ax=ax)

ax.set_title("PACF - AirPassengers (40 lags)")
ax.set_xlabel("Lag")
ax.set_ylabel("Partial Autocorrelation")

plt.tight_layout()

plt.savefig(FIG / "b1_pacf.png", dpi=300)

plt.show()

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