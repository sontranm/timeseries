# Bài 5: Trực quan hóa - Hoàng Nam.
# Đọc AirPassengers, vẽ 5 hình và in số liệu hỗ trợ nhận xét.
"""Chạy từ thư mục gốc: python src/b5_visualization.py"""
import matplotlib

matplotlib.use("Agg")  # Lưu hình trực tiếp, chạy được cả khi không mở cửa sổ.
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from load_data import FIG, load_airpassengers

WINDOW = 12
DPI = 150
UNIT = "Số hành khách (nghìn người)"
BLUE = "#2166AC"
ORANGE = "#D97706"
GREEN = "#19836B"


def validate(y):
    """Bảo đảm đang vẽ đúng bộ dữ liệu tháng của đề."""
    expected = pd.date_range("1949-01-01", "1960-12-01", freq="MS")
    if len(y) != 144 or not y.index.equals(expected):
        raise ValueError("AirPassengers phải có đủ 144 tháng từ 01/1949 đến 12/1960.")
    if y.isna().any() or not np.isfinite(y.to_numpy()).all() or (y <= 0).any():
        raise ValueError("Dữ liệu phải là số hữu hạn, dương và không thiếu.")


def save(fig, name):
    fig.savefig(FIG / name, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def time_axis(ax):
    ax.set_xlabel("Thời gian (năm)")
    ax.set_ylabel(UNIT)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.margins(x=0.01)


def plot_all(y):
    sns.set_theme(style="whitegrid", context="notebook", font="DejaVu Sans")
    plt.rcParams.update({
        "axes.titlesize": 16, "axes.titleweight": "bold",
        "axes.labelsize": 11, "figure.dpi": DPI,
        "axes.spines.top": False, "axes.spines.right": False,
    })
    frame = y.rename("Passengers").to_frame()
    frame["year"] = frame.index.year
    frame["month"] = frame.index.month
    mean = y.rolling(window=WINDOW, min_periods=WINDOW).mean()
    std = y.rolling(window=WINDOW, min_periods=WINDOW).std(ddof=1)

    fig, ax = plt.subplots(figsize=(12, 5), layout="constrained")
    ax.plot(y.index, y, color=BLUE, linewidth=1.8, label="Chuỗi gốc")
    ax.scatter([y.idxmin(), y.idxmax()], [y.min(), y.max()], color=ORANGE, zorder=4)
    ax.annotate("Thấp nhất: 104 (11/1949)", (y.idxmin(), y.min()),
                xytext=(18, 35), textcoords="offset points", fontsize=10,
                arrowprops={"arrowstyle": "->", "color": ORANGE})
    ax.annotate("Cao nhất: 622 (07/1960)", (y.idxmax(), y.max()),
                xytext=(-170, -35), textcoords="offset points", fontsize=10,
                arrowprops={"arrowstyle": "->", "color": ORANGE})
    time_axis(ax)
    ax.set_title("AirPassengers · Số hành khách theo tháng, 1949–1960", loc="left")
    ax.legend(loc="upper left")
    save(fig, "b5_line.png")

    fig, ax = plt.subplots(figsize=(12, 5.5), layout="constrained")
    ax.plot(y.index, y, color=BLUE, alpha=0.6, linewidth=1.3, label="Chuỗi gốc")
    ax.plot(mean.index, mean, color=ORANGE, linewidth=2.5, label="Trung bình trượt 12 tháng")
    ax.plot(std.index, std, color=GREEN, linewidth=2.2, linestyle="--",
            label="Độ lệch chuẩn trượt 12 tháng (ddof=1)")
    time_axis(ax)
    ax.set_ylim(bottom=0)
    ax.set_title("Mức hành khách và độ biến động qua cửa sổ 12 tháng", loc="left")
    ax.legend(loc="upper left")
    fig.supxlabel("Cửa sổ gồm tháng hiện tại và 11 tháng trước; 11 tháng đầu chưa đủ dữ liệu.",
                  fontsize=10, color="#555555")
    save(fig, "b5_rolling.png")

    fig, ax = plt.subplots(figsize=(12, 6), layout="constrained")
    years = sorted(frame["year"].unique())
    colors = sns.color_palette("viridis", n_colors=len(years))
    for year, color in zip(years, colors):
        group = frame[frame["year"] == year]
        ax.plot(group["month"], group["Passengers"], color=color,
                marker="o", markersize=4, linewidth=1.6, label=str(year))
    ax.set(title="Mùa vụ theo năm · Đỉnh thường rơi vào tháng 7–8",
           xlabel="Tháng trong năm", ylabel=UNIT, xticks=range(1, 13))
    ax.legend(title="Năm", bbox_to_anchor=(1.02, 1), loc="upper left", ncol=2)
    save(fig, "b5_seasonal.png")

    pivot = frame.pivot_table(index="year", columns="month", values="Passengers")
    fig, ax = plt.subplots(figsize=(12, 8), layout="constrained")
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5,
                linecolor="white", cbar_kws={"label": UNIT}, ax=ax)
    ax.set(title="AirPassengers · Bản đồ nhiệt tháng × năm",
           xlabel="Tháng trong năm", ylabel="Năm")
    ax.tick_params(axis="y", rotation=0)
    save(fig, "b5_heatmap.png")

    fig, ax = plt.subplots(figsize=(12, 5.5), layout="constrained")
    sns.boxplot(data=frame, x="month", y="Passengers", color="#88BDD5", ax=ax,
                width=0.6, whis=1.5)
    ax.set(title="Phân bố số hành khách theo từng tháng",
           xlabel="Tháng trong năm", ylabel=UNIT)
    fig.supxlabel("Mỗi hộp gồm 12 năm; độ phân tán chứa cả ảnh hưởng của xu hướng tăng.",
                  fontsize=10, color="#555555")
    save(fig, "b5_boxplot.png")
    return frame, mean, std


def summarize(frame, mean, std):
    """Số liệu được tính lại khi chạy, không lấy nhận xét ước lượng từ hình."""
    annual = frame.groupby("year")["Passengers"].agg(["mean", "min", "max"])
    annual["range"] = annual["max"] - annual["min"]
    monthly = frame.groupby("month")["Passengers"].mean()
    print("AIRPASSENGERS: 144 months, 1949-01 to 1960-12; unit: thousand passengers.")
    print("\nAnnual statistics:\n" + annual.round(2).to_string())
    print("\nMean by calendar month:\n" + monthly.round(2).to_string())
    print(f"\nRolling mean: {mean.dropna().iloc[0]:.4f} -> {mean.iloc[-1]:.4f}")
    print(f"Rolling std (ddof=1): {std.dropna().iloc[0]:.4f} -> {std.iloc[-1]:.4f}")
    print(f"Rolling std decreases in {int((std.dropna().diff() < 0).sum())} monthly steps.")
    print("\nFive PNG figures saved to docs/lab2/figures/.")


def main():
    y = load_airpassengers()
    validate(y)
    frame, mean, std = plot_all(y)
    summarize(frame, mean, std)


if __name__ == "__main__":
    main()
