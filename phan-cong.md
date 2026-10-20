# Phân công Bài tập thực hành Chương 2 (Lab 2)

**Nhóm 7 người** · Trưởng nhóm: Trần Minh Sơn · Người viết báo cáo: Thành

---

## 1. Bảng phân công (đã bốc thăm ngẫu nhiên)

6 bạn được xếp vào 6 vai bằng cách **xáo trộn ngẫu nhiên** danh sách (`random.shuffle` trong Python). Thành giữ vai số 7 (viết báo cáo) theo yêu cầu.

| # | Thành viên | Phần việc | File code của bạn trong `src/` |
|---|---|---|---|
| 1 | **Lê Quỳnh** | Dựng khung dự án, viết `README.md`, làm **Bài 1: ACF/PACF** | `load_data.py`, `b1_acf_pacf.py` |
| 2 | **Phạm Lê Văn Bảo** | **Bài 2: White noise** | `b2_white_noise.py` |
| 3 | **Bao Dinh** | **Bài 3: Phân rã chuỗi** | `b3_decomposition.py` |
| 4 | **Trần Minh Sơn** | **Bài 4a: Dữ liệu thiếu** (NaN, ffill, interpolation) | `b4a_missing.py` |
| 5 | **Hoàng Thắng** | **Bài 4b: Outlier** (rolling, Z-score, IQR) | `b4b_outliers.py` |
| 6 | **Hoàng Nam** | **Bài 5: Trực quan hóa** | `b5_visualization.py` |
| 7 | **Thành** | **Bài 6: Báo cáo**: tổng hợp `report.md`, `process.md`, kiểm tra toàn dự án | `main.py` |

**Vì sao Bài 4 được chia cho 2 người:** đề có 6 bài, Bài 6 là báo cáo nên Thành giữ. Còn 6 bạn cho 5 bài, nên tách bài nặng nhất là Bài 4 (gồm 2 việc khác hẳn nhau: xử lý dữ liệu thiếu và phát hiện outlier). Vai số 1 làm thêm phần dựng dự án và README vì Bài 1 cũng bắt đầu bằng bước tải dữ liệu.

---

## 2. Lịch làm việc

Gọi **H** là hạn nộp của cô.

| Mốc | Ai | Việc phải xong |
|---|---|---|
| Ngày đầu tiên | **Lê Quỳnh** | Dựng xong repo, có sẵn dữ liệu trong `data/raw/` và `src/load_data.py`, gửi link cho cả nhóm |
| Ngày đầu tiên | **Thành** | Gửi file phân công này, chốt hạn, gửi phần "Data Introduction" cho Lê Quỳnh |
| Sớm nhất có thể | **Bao Dinh** | Xuất `data/processed/decomposition_stl.csv` (**Hoàng Thắng cần file này để làm Bài 4b**) |
| **H trừ 3 ngày** | 6 bạn | Nộp đủ code, hình, dữ liệu xử lý và 2 file nháp `.md` |
| H trừ 1 ngày | **Thành** | Ghép xong `report.md`, `process.md`, gửi nhóm đọc lại |
| H | **Thành** + **Trần Minh Sơn** | Chạy lại toàn bộ dự án lần cuối, nộp bài |

Trưởng nhóm **Trần Minh Sơn** nhắc tiến độ trong nhóm chat, đặc biệt mốc H trừ 3 ngày.

---

## 3. Cấu trúc dự án (theo yêu cầu của cô)

```
chuong2-timeseries/                 ← 1 repo GitHub (hoặc 1 thư mục Google Drive) chung
├── README.md                       ← Lê Quỳnh viết, Thành duyệt
├── requirements.txt                ← Lê Quỳnh
├── data/
│   ├── raw/                        ← dữ liệu GỐC, KHÔNG ai được sửa
│   │   ├── airline-passengers.csv          (Lê Quỳnh tải về)
│   │   └── daily-min-temperatures.csv      (Lê Quỳnh tải về)
│   └── processed/                  ← dữ liệu SAU xử lý
│       ├── white_noise.csv                 (Phạm Lê Văn Bảo)
│       ├── decomposition_stl.csv           (Bao Dinh)
│       ├── airpassengers_filled.csv        (Trần Minh Sơn)
│       ├── temperatures_filled.csv         (Trần Minh Sơn)
│       └── airpassengers_clean.csv         (Hoàng Thắng)
├── src/                            ← mã nguồn, mỗi file một chức năng
│   ├── load_data.py                (Lê Quỳnh) hàm đọc dữ liệu dùng chung
│   ├── b1_acf_pacf.py              (Lê Quỳnh)
│   ├── b2_white_noise.py           (Phạm Lê Văn Bảo)
│   ├── b3_decomposition.py         (Bao Dinh)
│   ├── b4a_missing.py              (Trần Minh Sơn)
│   ├── b4b_outliers.py             (Hoàng Thắng)
│   ├── b5_visualization.py         (Hoàng Nam)
│   └── main.py                     (Thành) chạy lần lượt tất cả file trên
└── docs/
    └── lab2/
        ├── report.md               ← Thành tổng hợp: nội dung và kết quả
        ├── process.md              ← Thành tổng hợp: quy trình, phương pháp, kết quả trung gian
        ├── figures/                ← tất cả hình của cả nhóm
        └── parts/                  ← bản nháp từng bạn nộp, Thành ghép xong thì xóa
```

### Quy ước bắt buộc cho cả nhóm

1. **Code là file `.py` trong `src/`.** Ai quen Jupyter có thể thử trên notebook, nhưng bản nộp phải là `.py`. Mỗi file phải chạy được độc lập từ thư mục gốc, ví dụ `python src/b1_acf_pacf.py`.
2. **Đọc dữ liệu qua `load_data.py`**, không tự tải lại từ internet:
   `from load_data import load_airpassengers, load_temperatures, PROCESSED, FIG`
3. **Không sửa gì trong `data/raw/`.** Dữ liệu đã biến đổi ghi vào `data/processed/` với đúng tên ở sơ đồ trên.
4. **Hình** lưu vào `docs/lab2/figures/`, định dạng `.png`, `dpi=150`, phải có tiêu đề, tên trục, chú thích. Tên hình bắt đầu bằng mã bài: `b1_acf.png`, `b3_stl.png`, ...
5. Mọi chỗ có ngẫu nhiên đặt `np.random.seed(42)` để chạy lại ra đúng kết quả.
6. **Mỗi bạn (vai 1 đến 6) nộp 2 file Markdown** vào `docs/lab2/parts/`:
   - `bX_report.md`: kết quả và nhận xét, chèn hình bằng `![Mô tả](../figures/b1_acf.png)`, có **con số cụ thể** (ví dụ "ACF tại lag 12 bằng 0,76"), không viết chung chung.
   - `bX_process.md`: các bước đã làm, hàm và thư viện dùng, tham số đã chọn và lý do, kết quả trung gian, lỗi gặp phải và cách sửa.
7. Đầu mỗi file `.py` ghi comment: tên bài, tên người làm, mô tả ngắn file làm gì.

---

## 4. Dữ liệu (đã kiểm tra tải được ngày 19/10/2026)

### AirPassengers (cả nhóm dùng)

| Thuộc tính | Giá trị |
|---|---|
| Nội dung | Số hành khách đi máy bay quốc tế hằng tháng (đơn vị nghìn người) của hãng hàng không Mỹ |
| Nguồn gốc | Sách Box & Jenkins, *Time Series Analysis: Forecasting and Control* |
| Thời gian | 01/1949 đến 12/1960 |
| Tần suất | Tháng |
| Số điểm | 144, không có giá trị thiếu |
| Cột | `Month` (dạng `1949-01`), `Passengers` (số nguyên) |
| Thống kê | Min 104, max 622, trung bình khoảng 280,3, độ lệch chuẩn khoảng 120 |
| Link tải | https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv |

### Daily-Min-Temperatures (chỉ Trần Minh Sơn dùng thêm cho Bài 4a)

| Thuộc tính | Giá trị |
|---|---|
| Nội dung | Nhiệt độ thấp nhất hằng ngày (°C) ở Melbourne, Úc |
| Nguồn gốc | Cục Khí tượng Úc (Australian Bureau of Meteorology) |
| Thời gian | 01/01/1981 đến 31/12/1990 |
| Tần suất | Ngày |
| Số dòng | 3650, cột `Date`, `Temp` |
| Điểm đặc biệt | **Thiếu thật 2 ngày: 1984-12-31 và 1988-12-31** (đã kiểm tra) |
| Link tải | https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv |

### Nội dung `src/load_data.py` (Lê Quỳnh tạo, cả nhóm dùng)

```python
"""Đọc dữ liệu dùng chung cho Lab 2. Người viết: Lê Quỳnh."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIG = ROOT / "docs" / "lab2" / "figures"
PROCESSED.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

def load_airpassengers():
    df = pd.read_csv(RAW / "airline-passengers.csv", parse_dates=["Month"], index_col="Month")
    df.index.freq = "MS"
    return df["Passengers"]

def load_temperatures():
    df = pd.read_csv(RAW / "daily-min-temperatures.csv", parse_dates=["Date"], index_col="Date")
    return df["Temp"]
```

---

## 5. Chi tiết việc của từng người

### 5.1. Lê Quỳnh: Dựng dự án, README.md, Bài 1 (ACF/PACF)

**Phần A. Dựng dự án (làm ngay ngày đầu)**
1. Tạo repo GitHub (hoặc thư mục Drive) đúng sơ đồ mục 3. Thư mục rỗng thêm file `.gitkeep` để Git giữ lại.
2. Tải 2 file CSV ở mục 4 về `data/raw/`.
3. Tạo `src/load_data.py` (copy nội dung mục 4).
4. Tạo `requirements.txt`: `pandas`, `numpy`, `matplotlib`, `seaborn`, `statsmodels`, `scipy`.
5. Mời cả nhóm vào repo, gửi link trong nhóm chat.

**Phần B. README.md** (4 phần cô yêu cầu)
1. **Giới thiệu:** tên Lab 2, Bài tập thực hành chương 2, 6 mục tiêu trong đề.
2. **Data Introduction:** dùng đoạn Thành gửi (nội dung mục 4): nguồn, nội dung, các biến chính, thời gian, tần suất.
3. **Môi trường:** phiên bản Python (`python --version`), danh sách thư viện và phiên bản (`pip freeze`).
4. **Cài đặt và chạy:** `git clone ...`, `pip install -r requirements.txt`, `python src/main.py` hoặc chạy từng file; kết quả nằm ở `docs/lab2/figures/` và `data/processed/`.
5. Thêm bảng cấu trúc thư mục và bảng thành viên (mục 1).

**Phần C. Bài 1** trong `src/b1_acf_pacf.py`
1. In `y.head()`, `y.info()`, `y.describe()`; vẽ line chart nhanh.
2. Vẽ ACF và PACF 40 lags: `plot_acf(y, lags=40)`, `plot_pacf(y, lags=40, method="ywm")` (từ `statsmodels.graphics.tsaplots`).
3. Tính số: `acf(y, nlags=40)`, `pacf(y, nlags=40)`; ghi giá trị lag 1, 12, 24, 36.
4. (Nên làm thêm) Vẽ ACF sau sai phân `y.diff().dropna()` và sai phân mùa `y.diff(12).dropna()`.

**Phải tự tìm hiểu**
- Markdown cơ bản và Git cơ bản (clone, pull, add, commit, push) để hướng dẫn nhóm.
- ACF là gì, PACF là gì, khác nhau thế nào.
- Dải tin cậy 95% trên hình (khoảng ±1,96/√n) nghĩa là gì.
- Cách đọc hình: ACF giảm chậm là dấu hiệu có xu hướng (chuỗi không dừng); đỉnh lặp lại ở lag 12, 24, 36 là mùa vụ theo năm.

**Kết quả phải nộp**
- [ ] Repo đúng cấu trúc, `data/raw/` có 2 file, `src/load_data.py`, `requirements.txt`
- [ ] `README.md` đủ 4 phần
- [ ] `src/b1_acf_pacf.py` chạy được
- [ ] Hình: `b1_line.png`, `b1_acf.png`, `b1_pacf.png` (+ `b1_acf_diff.png` nếu làm)
- [ ] `parts/b1_report.md`: bảng ACF/PACF tại lag 1, 12, 24, 36; trả lời 3 câu của đề, mỗi câu 2 đến 3 dòng: (1) chuỗi có tự tương quan mạnh không, (2) có xu hướng/mùa vụ thể hiện qua ACF/PACF không, (3) lag nào quan trọng nhất
- [ ] `parts/b1_process.md`

---

### 5.2. Phạm Lê Văn Bảo: Bài 2 (White noise)

**Các bước** trong `src/b2_white_noise.py`
1. Sinh 1000 điểm: `np.random.seed(42); wn = np.random.normal(0, 1, 1000)`; lưu ra `data/processed/white_noise.csv`.
2. Vẽ line chart của white noise.
3. Vẽ ACF 40 lags của white noise; đếm số lag vượt dải tin cậy 95%.
4. Kiểm định Ljung-Box (`from statsmodels.stats.diagnostic import acorr_ljungbox`, `lags=[10, 20]`) cho cả white noise và AirPassengers.
5. Vẽ 1 hình 2 ô: ACF của white noise bên trái, ACF của AirPassengers bên phải.

**Phải tự tìm hiểu**
- Định nghĩa white noise: trung bình 0, phương sai không đổi, không tự tương quan.
- Vì sao với 40 lags vẫn có thể có khoảng 2 lag vượt ngưỡng chỉ do ngẫu nhiên (5% × 40 = 2).
- Kiểm định Ljung-Box và cách đọc p-value (p > 0,05 thì không bác bỏ giả thuyết "chuỗi là white noise").

**Kết quả phải nộp**
- [ ] `src/b2_white_noise.py` chạy được
- [ ] `data/processed/white_noise.csv`
- [ ] Hình: `b2_wn_line.png`, `b2_wn_acf.png`, `b2_sosanh_acf.png`
- [ ] `parts/b2_report.md`: số lag vượt ngưỡng của white noise; bảng p-value Ljung-Box của 2 chuỗi; **đúng 5 dòng** mô tả sự khác nhau
- [ ] `parts/b2_process.md`

---

### 5.3. Bao Dinh: Bài 3 (Phân rã chuỗi)

> Hoàng Thắng cần file `decomposition_stl.csv` của bạn, nên làm bước 3 sớm nhất có thể.

**Các bước** trong `src/b3_decomposition.py`
1. Dùng AirPassengers (dữ liệu tháng, chu kỳ 12).
2. Classical: `seasonal_decompose(y, model="multiplicative", period=12)`, vẽ 4 thành phần.
3. STL: `STL(np.log(y), period=12).fit()`, vẽ 4 thành phần; lưu 3 cột `trend`, `seasonal`, `resid` ra `data/processed/decomposition_stl.csv`, **báo Hoàng Thắng ngay**.
4. Vẽ ACF của residual, chạy Ljung-Box.
5. (Nên làm thêm) Tính độ mạnh xu hướng và mùa vụ:
   `F_T = max(0, 1 - Var(R)/Var(T+R))`, `F_S = max(0, 1 - Var(R)/Var(S+R))`.

**Phải tự tìm hiểu**
- 4 thành phần Observed, Trend, Seasonal, Residual.
- Mô hình cộng (additive) và nhân (multiplicative); vì sao AirPassengers nên dùng nhân, hoặc lấy log rồi dùng cộng (biên độ mùa vụ tăng theo thời gian).
- Khác nhau giữa classical và STL (STL linh hoạt hơn, không mất dữ liệu ở 2 đầu chuỗi).

**Kết quả phải nộp**
- [ ] `src/b3_decomposition.py` chạy được
- [ ] `data/processed/decomposition_stl.csv`
- [ ] Hình: `b3_classical.png`, `b3_stl.png`, `b3_resid_acf.png`
- [ ] `parts/b3_report.md`: trả lời 3 câu của đề: (1) xu hướng tăng hay giảm, (2) mùa vụ mạnh hay yếu, đỉnh vào tháng nào, (3) residual có giống white noise không; kèm F_T, F_S, p-value Ljung-Box
- [ ] `parts/b3_process.md`

---

### 5.4. Trần Minh Sơn: Bài 4a (Dữ liệu thiếu)

**Các bước** trong `src/b4a_missing.py`
1. Copy AirPassengers, xóa ngẫu nhiên khoảng 10% giá trị (`np.random.seed(42)`), thêm 1 đoạn thiếu liền 3 tháng.
2. Kiểm tra: `isna().sum()`, in danh sách các mốc bị thiếu.
3. Xử lý 2 cách: `ffill()` và `interpolate(method="linear")`.
4. So với giá trị thật đã xóa, tính MAE của từng cách.
5. Vẽ trên cùng 1 hình: chuỗi gốc, chuỗi có lỗ, 2 chuỗi sau xử lý.
6. Lưu chuỗi xử lý tốt hơn ra `data/processed/airpassengers_filled.csv`.
7. Với dữ liệu nhiệt độ: `load_temperatures().asfreq("D")` để lộ 2 ngày thiếu thật (1984-12-31, 1988-12-31), xử lý bằng interpolation, vẽ đoạn quanh 2 ngày đó, lưu `data/processed/temperatures_filled.csv`.

**Phải tự tìm hiểu**
- Vì sao trong chuỗi thời gian không được xóa dòng bị thiếu tùy tiện (mất tính liên tục về thời gian).
- Ưu nhược điểm của ffill (tạo "bậc thang") và interpolation (mượt hơn nhưng làm mờ đỉnh mùa vụ).
- Hàm `asfreq` trong pandas.

**Kết quả phải nộp**
- [ ] `src/b4a_missing.py` chạy được
- [ ] `data/processed/airpassengers_filled.csv`, `data/processed/temperatures_filled.csv`
- [ ] Hình: `b4a_truoc_sau.png`, `b4a_temp_missing.png`
- [ ] `parts/b4a_report.md`: bảng số giá trị thiếu và MAE của từng cách; 3 đến 4 dòng kết luận nên dùng cách nào, vì sao
- [ ] `parts/b4a_process.md`

---

### 5.5. Hoàng Thắng: Bài 4b (Outlier)

> Bạn dùng file `decomposition_stl.csv` của Bao Dinh. Trong lúc chờ, làm trước bước 1 và 3.

**Các bước** trong `src/b4b_outliers.py`
1. Rolling mean và rolling std (window=12) trên chuỗi gốc; đánh dấu điểm lệch khỏi rolling mean quá 3 lần rolling std.
2. Z-score (|z| > 3) và IQR (ngoài khoảng `[Q1 - 1.5·IQR, Q3 + 1.5·IQR]`), áp lên cột `resid` trong `decomposition_stl.csv`; áp thử lên chuỗi gốc để so sánh.
3. Chèn thử 2 đến 3 outlier giả (ví dụ nhân đôi 1 giá trị) vào bản copy để kiểm tra phương pháp có bắt được không.
4. Nếu dữ liệu thật có outlier: thay bằng giá trị nội suy. Lưu kết quả ra `data/processed/airpassengers_clean.csv` (không có outlier thì lưu nguyên chuỗi và ghi rõ trong báo cáo).
5. Vẽ hình đánh dấu outlier bằng chấm đỏ và hình trước/sau.

**Phải tự tìm hiểu**
- Z-score và IQR, giả định của từng cách.
- Vì sao xu hướng và mùa vụ làm phát hiện outlier sai nếu áp thẳng lên chuỗi gốc (các tháng cuối luôn cao nên dễ bị coi nhầm là outlier).

**Kết quả phải nộp**
- [ ] `src/b4b_outliers.py` chạy được
- [ ] `data/processed/airpassengers_clean.csv`
- [ ] Hình: `b4b_outlier.png`, `b4b_truoc_sau.png`
- [ ] `parts/b4b_report.md`: bảng mốc thời gian, giá trị, phương pháp nào phát hiện; 3 đến 4 dòng kết luận dữ liệu gốc có outlier thật không, phương pháp nào hợp lý hơn
- [ ] `parts/b4b_process.md`

---

### 5.6. Hoàng Nam: Bài 5 (Trực quan hóa)

**Các bước** trong `src/b5_visualization.py`
1. Line chart toàn bộ chuỗi.
2. Rolling mean và rolling std (window=12) vẽ chồng lên chuỗi gốc.
3. Seasonal plot: mỗi năm 1 đường, trục ngang là tháng 1 đến 12.
4. Heatmap tháng × năm: `pivot_table(index=năm, columns=tháng, values="Passengers")` rồi `sns.heatmap(..., annot=True, fmt=".0f")`.
5. (Nên làm thêm) Boxplot theo tháng.

**Phải tự tìm hiểu**
- Rolling window là gì; rolling std tăng dần nói gì về phương sai của chuỗi.
- Cách đọc seasonal plot và heatmap.
- Thư viện `seaborn` (heatmap, boxplot).

**Kết quả phải nộp**
- [ ] `src/b5_visualization.py` chạy được
- [ ] Hình: `b5_line.png`, `b5_rolling.png`, `b5_seasonal.png`, `b5_heatmap.png` (+ `b5_boxplot.png`)
- [ ] `parts/b5_report.md`: 5 đến 7 dòng kết luận: xu hướng chung, tháng cao điểm và thấp điểm, biên độ mùa vụ thay đổi thế nào qua các năm, có điểm bất thường không
- [ ] `parts/b5_process.md`

---

### 5.7. Thành: Bài 6 (Báo cáo), kiểm tra toàn dự án

**Các bước**
1. **Ngày đầu:** gửi file này cho nhóm, chốt hạn H trừ 3 ngày; gửi đoạn Data Introduction (mục 4) cho Lê Quỳnh đưa vào README.
2. Viết `src/main.py` chạy lần lượt `b1` đến `b5` (dùng `runpy.run_path`), **theo thứ tự b1, b2, b3, b4a, b4b, b5** vì b4b cần kết quả của b3.
3. Khi nhận bài từng bạn: chạy thử file `.py` trên máy mình, kiểm tra hình trong `figures/`, dữ liệu trong `processed/`, 2 file trong `parts/` đủ ý theo checklist. Thiếu thì trả lại ngay.
4. Ghép `docs/lab2/report.md` theo 7 mục đề yêu cầu:

| Mục trong report.md | Lấy từ |
|---|---|
| 1. Mô tả dataset | Thành tự viết (mục 4) |
| 2. Kiểm tra ACF/PACF | `b1_report.md` (Lê Quỳnh) |
| 3. Kiểm tra white noise | `b2_report.md` (Phạm Lê Văn Bảo) |
| 4. Phân rã chuỗi | `b3_report.md` (Bao Dinh) |
| 5. Vấn đề chất lượng dữ liệu | `b4a_report.md` (Trần Minh Sơn) + `b4b_report.md` (Hoàng Thắng) |
| 6. Ý nghĩa trực quan hóa | `b5_report.md` (Hoàng Nam) |
| 7. Kết luận: dữ liệu có phù hợp để dự báo không | Thành tự viết |

5. Ghép `docs/lab2/process.md`: mở đầu bằng sơ đồ luồng dữ liệu (`data/raw` → từng file trong `src/` → `data/processed` và `figures/`), sau đó lần lượt `b1_process.md` đến `b5_process.md`, cuối cùng là bảng phân công thành viên (mục 1).
6. Sửa văn phong cho thống nhất, đánh số hình và bảng (Hình 1, Hình 2, ...), sửa đường dẫn ảnh thành `figures/...` vì `report.md` nằm ngay trong `docs/lab2/`.
7. Kiểm tra chéo: các phần không mâu thuẫn (mùa vụ 12 tháng phải khớp ở Bài 1, 3, 5; kết luận outlier của Bài 4b khớp với Bài 5).
8. Xóa `docs/lab2/parts/`. Cùng Trần Minh Sơn clone repo về một máy sạch, làm đúng theo README, chạy `python src/main.py`, xác nhận ra đủ kết quả rồi mới nộp.

**Phải tự tìm hiểu**
- Markdown: tiêu đề, bảng, chèn ảnh bằng đường dẫn tương đối.
- Đọc lướt phần "phải tự tìm hiểu" của cả 6 bạn để hiểu từng bài.
- Thế nào là chuỗi "phù hợp để dự báo": có cấu trúc (xu hướng, mùa vụ, tự tương quan) chứ không phải white noise; đủ dài; ít lỗi.
- Tính dừng và các phép biến đổi trước khi dự báo: log, sai phân, sai phân mùa.

**Gợi ý ý chính cho mục Kết luận** (kiểm lại bằng kết quả thật của nhóm):
AirPassengers phù hợp để dự báo vì có xu hướng tăng và mùa vụ 12 tháng rõ, ACF giảm chậm và có đỉnh ở lag 12, khác hẳn white noise; dữ liệu đầy đủ, không có outlier đáng kể. Tuy nhiên chuỗi không dừng và biên độ mùa vụ tăng theo thời gian, nên cần biến đổi log và lấy sai phân (hoặc dùng mô hình có mùa vụ như SARIMA, Holt-Winters) trước khi dự báo. Hạn chế: chỉ 144 điểm và dữ liệu đã cũ (1949 đến 1960).

**Kết quả cuối**
- [ ] `docs/lab2/report.md` đủ 7 mục, hình hiển thị đúng
- [ ] `docs/lab2/process.md` đủ quy trình của 6 phần
- [ ] `src/main.py` chạy ra toàn bộ kết quả
- [ ] README đã duyệt, làm theo được từ đầu đến cuối

---

> **Các Lab sau:** tạo thêm `docs/lab3/`, `docs/lab4/`, ... cùng cấu trúc. Hết môn thì gộp thành `docs/report.md` chung, mỗi Lab một chương riêng như cô yêu cầu.
