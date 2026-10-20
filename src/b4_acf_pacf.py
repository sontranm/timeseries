from pathlib import Path
 
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, pacf, adfuller
 
from load_data import load_a10
 
FIG = Path(__file__).resolve().parents[1] / "docs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
 
LAGS = 40
 
series = load_a10()
log_diff = np.log(series).diff().dropna()
 
stat, pvalue, _, _, crit, _ = adfuller(log_diff)
print(f"ADF statistic: {stat:.4f}")
print(f"p-value: {pvalue:.4f}")
print("Critical values:", crit)
print("Kết luận:", "DỪNG" if pvalue < 0.05 else "KHÔNG DỪNG")
 
n = len(log_diff)
bound = 1.96 / np.sqrt(n)
acf_vals = acf(log_diff, nlags=LAGS)
pacf_vals = pacf(log_diff, nlags=LAGS, method="ywm")
print(f"\nNgưỡng tin cậy 95%: ±{bound:.3f}")
print("ACF vượt ngưỡng ở lag:", [k for k in range(1, LAGS + 1) if abs(acf_vals[k]) > bound])
print("PACF vượt ngưỡng ở lag:", [k for k in range(1, LAGS + 1) if abs(pacf_vals[k]) > bound])

fig, axes = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(log_diff, lags=LAGS, ax=axes[0], title="ACF (log + sai phân bậc 1)")
plot_pacf(log_diff, lags=LAGS, ax=axes[1], method="ywm",
          title="PACF (log + sai phân bậc 1)")
for ax in axes:
    ax.set_xlabel("Lag")
plt.tight_layout()
plt.savefig(FIG / "b4_acf_pacf.png", dpi=150)
plt.show()