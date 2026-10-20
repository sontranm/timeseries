"""Bài 4a: Xử lý dữ liệu thiếu (NaN, ffill, interpolation).
Người làm: Trần Minh Sơn.
Mô tả: tạo lỗ giả trên AirPassengers rồi so sánh ffill với nội suy tuyến tính
bằng MAE; sau đó xử lý 2 ngày thiếu thật trong chuỗi nhiệt độ Melbourne.
Chạy từ thư mục gốc: python src/b4a_missing.py
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from load_data import load_airpassengers, load_temperatures, PROCESSED, FIG

np.random.seed(42)

original = load_airpassengers().astype(float)

block = original.index[(original.index >= "1955-06-01") & (original.index <= "1955-08-01")]
candidates = original.index[1:-1].difference(block)  
random_idx = np.random.choice(candidates, size=12, replace=False)
missing_idx = block.union(pd.DatetimeIndex(random_idx)).sort_values()

holed = original.copy()
holed.loc[missing_idx] = np.nan

print("=== AirPassengers ===")
print("Số giá trị thiếu:", holed.isna().sum(), f"({holed.isna().mean():.1%})")
print("Các mốc bị thiếu:", [d.strftime("%Y-%m") for d in missing_idx])

ffilled = holed.ffill()
interp = holed.interpolate(method="linear")

def mae(filled, idx):
    return (filled.loc[idx] - original.loc[idx]).abs().mean()


rand_idx = pd.DatetimeIndex(random_idx).sort_values()
results = pd.DataFrame({
    "ffill": [mae(ffilled, missing_idx), mae(ffilled, rand_idx), mae(ffilled, block)],
    "interpolate": [mae(interp, missing_idx), mae(interp, rand_idx), mae(interp, block)],
}, index=["Tất cả (15 điểm)", "12 điểm ngẫu nhiên", "Đoạn liền 3 tháng"])
print("\nMAE so với giá trị thật:")
print(results.round(2))

fig, ax = plt.subplots(figsize=(13, 6))
ax.plot(original, color="lightgray", linewidth=3, label="Chuỗi gốc")
ax.plot(holed, color="black", marker="o", markersize=3, linewidth=1, label="Chuỗi có lỗ (NaN)")
ax.plot(ffilled.loc[missing_idx], "s", color="tab:orange", markersize=6, label="Sau ffill")
ax.plot(interp.loc[missing_idx], "^", color="tab:green", markersize=6, label="Sau interpolate (linear)")
ax.set_title("AirPassengers: dữ liệu thiếu và 2 cách xử lý")
ax.set_xlabel("Tháng")
ax.set_ylabel("Số hành khách (nghìn)")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / "b4a_truoc_sau.png", dpi=150)
plt.close()

best_name = "interpolate" if results.loc["Tất cả (15 điểm)", "interpolate"] <= results.loc["Tất cả (15 điểm)", "ffill"] else "ffill"
best = interp if best_name == "interpolate" else ffilled
best.rename("Passengers").to_csv(PROCESSED / "airpassengers_filled.csv", index_label="Month")
print(f"\nCách tốt hơn: {best_name} -> đã lưu data/processed/airpassengers_filled.csv")


temp_raw = load_temperatures()
temp = temp_raw.asfreq("D")  
temp_missing = temp[temp.isna()].index
print("\n=== Nhiệt độ Melbourne ===")
print("Số dòng gốc:", len(temp_raw), "| sau asfreq('D'):", len(temp))
print("Các ngày thiếu thật:", [d.strftime("%Y-%m-%d") for d in temp_missing])

temp_filled = temp.interpolate(method="linear")
temp_filled.rename("Temp").to_csv(PROCESSED / "temperatures_filled.csv", index_label="Date")

fig, axes = plt.subplots(1, len(temp_missing), figsize=(13, 5))
axes = np.atleast_1d(axes)
for ax, day in zip(axes, temp_missing):
    lo, hi = day - pd.Timedelta(days=15), day + pd.Timedelta(days=15)
    ax.plot(temp.loc[lo:hi], marker="o", markersize=4, color="black", label="Dữ liệu gốc")
    ax.plot(temp_filled.loc[[day]], "^", color="tab:green", markersize=10, label="Giá trị nội suy")
    ax.axvline(day, color="red", linestyle="--", alpha=0.5)
    ax.set_title(f"Quanh ngày thiếu {day:%Y-%m-%d}")
    ax.set_xlabel("Ngày")
    ax.set_ylabel("Nhiệt độ thấp nhất (°C)")
    ax.tick_params(axis="x", rotation=30)
    ax.legend()
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / "b4a_temp_missing.png", dpi=150)
plt.close()
for d in temp_missing:
    print(f"Giá trị nội suy {d:%Y-%m-%d}: {temp_filled.loc[d]:.2f} °C")
