# Quy trình Bài 5: Trực quan hóa

## 1. Dữ liệu đầu vào

- Dùng `data/raw/airline-passengers.csv`, hai cột `Month` và `Passengers`.
- Dữ liệu lấy từ [kho jbrownlee/Datasets](https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv), ngày 20/10/2026.
- Đọc dữ liệu qua `from load_data import FIG, load_airpassengers`. Hàm đọc chuyển `Month` thành DatetimeIndex, tần suất đầu tháng `MS`, trả về Series `Passengers`.
- Phân tích trực tiếp chuỗi gốc để quan sát xu hướng, mùa vụ và mức biến động theo thời gian.

Luồng xử lý:

```text
data/raw/airline-passengers.csv
             ↓ load_airpassengers()
      kiểm tra dữ liệu tháng
             ↓
      src/b5_visualization.py
             ├── 5 hình PNG → docs/lab2/figures/
             └── bảng thống kê → màn hình chạy → nhận xét b5_report.md
```

Các thống kê trượt và bảng tổng hợp được tính trên bản dữ liệu trong bộ nhớ; file CSV gốc được giữ nguyên.

## 2. Kiểm tra dữ liệu

Hàm `validate()` kiểm tra đủ 144 mốc từ 01/1949 đến 12/1960, đúng thứ tự tháng, không thiếu tháng, không có giá trị NaN/vô hạn hoặc không dương. Việc so với dãy tháng kỳ vọng cũng loại trường hợp tháng trùng hoặc thứ tự sai.

Kết quả kiểm tra đầu vào: 144 dòng, 0 giá trị thiếu; nhỏ nhất 104 ở 11/1949, lớn nhất 622 ở 07/1960. Tất cả hình dùng đơn vị **nghìn hành khách**.

## 3. Thư viện, hàm và tham số

| Công việc | Hàm / thư viện | Tham số và lý do |
|---|---|---|
| Đọc CSV | `pandas.read_csv` trong `load_data.py` | `parse_dates=["Month"]`, `index_col="Month"` để có trục thời gian |
| Chuỗi gốc | `matplotlib.axes.Axes.plot` | Vẽ toàn bộ 144 tháng, đánh dấu cực trị để dễ đối chiếu |
| Trung bình trượt | `y.rolling(...).mean()` | `window=12`, `min_periods=12`: một năm dữ liệu tháng |
| Độ lệch chuẩn trượt | `y.rolling(...).std(ddof=1)` | Dùng độ lệch chuẩn mẫu, cùng cửa sổ với trung bình |
| Seasonal plot | Tách `index.year`, `index.month`, dùng `plot` | 12 đường ứng với 12 năm, mỗi đường 12 tháng; màu và chú thích phân biệt năm |
| Heatmap | `pivot_table`, `seaborn.heatmap` | `index="year"`, `columns="month"`, `values="Passengers"`, `annot=True`, `fmt=".0f"` |
| Boxplot | `seaborn.boxplot` | Theo tháng; `whis=1.5`, mỗi nhóm có 12 giá trị |
| Thống kê đối chiếu | `groupby`, `agg`, `mean` | Trung bình năm/tháng, min/max, khoảng đỉnh–đáy |
| Xuất hình | `fig.savefig`, `plt.close` | PNG, `dpi=150`, `bbox_inches="tight"` để không cắt nhãn |

Rolling window tại tháng t chứa tháng t và 11 tháng trước đó, không lấy tháng tương lai. Với `min_periods=12`, 11 giá trị đầu của hai đường rolling là NaN do chưa đủ cửa sổ; không phải dữ liệu gốc bị thiếu, không điền thêm giá trị.

Rolling mean giúp nhìn xu hướng tổng quát. Rolling std đo mức phân tán trong cửa sổ, chịu cả ảnh hưởng của mùa vụ và xu hướng; không phải độ lệch chuẩn của residual sau phân rã. Cửa sổ 12 phù hợp chu kỳ một năm của dữ liệu tháng.

Code dùng backend `Agg` để ghi hình khi chạy tự động; font `DejaVu Sans` hỗ trợ chữ tiếng Việt. Không có bước sinh ngẫu nhiên nên không cần đặt seed.

## 4. Kết quả trung gian

Đơn vị trong các bảng dưới đây: nghìn hành khách.

| Năm | Trung bình tháng | Min | Max | Max − Min |
|---|---:|---:|---:|---:|
| 1949 | 126,67 | 104 | 148 | 44 |
| 1950 | 139,67 | 114 | 170 | 56 |
| 1951 | 170,17 | 145 | 199 | 54 |
| 1952 | 197,00 | 171 | 242 | 71 |
| 1953 | 225,00 | 180 | 272 | 92 |
| 1954 | 238,92 | 188 | 302 | 114 |
| 1955 | 284,00 | 233 | 364 | 131 |
| 1956 | 328,25 | 271 | 413 | 142 |
| 1957 | 368,42 | 301 | 467 | 166 |
| 1958 | 381,00 | 310 | 505 | 195 |
| 1959 | 428,33 | 342 | 559 | 217 |
| 1960 | 476,17 | 390 | 622 | 232 |

Khoảng max − min được dùng làm mô tả dao động trong năm, không phải ước lượng riêng thành phần mùa vụ đã tách khỏi xu hướng.

| Tháng | Trung bình qua 12 năm |
|---|---:|
| 1 | 241,75 |
| 2 | 235,00 |
| 3 | 270,17 |
| 4 | 267,08 |
| 5 | 271,83 |
| 6 | 311,67 |
| 7 | 351,33 |
| 8 | 351,08 |
| 9 | 302,42 |
| 10 | 266,58 |
| 11 | 232,83 |
| 12 | 261,83 |

- Cửa sổ đầu tiên (01–12/1949): mean = 126,6667; std mẫu = 13,7201.
- Cửa sổ cuối (01–12/1960): mean = 476,1667; std mẫu = 77,7371.
- Có 133 cửa sổ đầy đủ. Rolling std giảm ở 75 trong 132 lần chuyển cửa sổ; vì vậy chỉ kết luận độ biến động nhìn chung cao hơn về cuối, không nói tăng liên tục.
- Ma trận heatmap có 12 hàng × 12 cột, không thiếu ô.

## 5. Cách đọc và giới hạn

- Line chart: đọc mức tăng dài hạn và các đỉnh lặp lại.
- Seasonal plot: so vị trí đỉnh/đáy trên cùng trục tháng, đồng thời so mức các đường năm.
- Heatmap: màu đậm thể hiện số hành khách cao; đọc dọc cột để so cùng tháng qua các năm, đọc ngang hàng để so các tháng trong năm.
- Boxplot: hộp biểu diễn Q1–Q3, đường trong hộp là trung vị; râu tới giá trị quan sát xa nhất còn trong ngưỡng 1,5 IQR. Điểm ngoài râu nếu có chỉ là dấu hiệu để kiểm tra thêm.
- Việc gộp nhiều năm vào boxplot chứa ảnh hưởng xu hướng; để xác định outlier cần đánh giá sai lệch sau khi xét xu hướng và mùa vụ.

## 6. Vấn đề gặp trong quá trình chạy và cách xử lý

- Môi trường ban đầu thiếu thư viện vẽ biểu đồ: cài bổ sung `matplotlib` và `seaborn`.
- Giữ 11 giá trị rolling đầu tiên ở dạng NaN vì chưa đủ cửa sổ 12 tháng; đường rolling bắt đầu từ tháng 12/1949.
- Dùng font `DejaVu Sans` và bố cục tự động để hiển thị đầy đủ nhãn tiếng Việt, chú thích và thang màu.
- Chương trình tạo đủ năm hình và các bảng thống kê, không phát sinh lỗi xử lý dữ liệu.

## 7. Kiểm tra đầu ra

Chạy từ thư mục gốc:

```bash
python src/b5_visualization.py
```

Đã chạy thành công và kiểm tra trực quan đủ năm hình: chữ tiếng Việt, tiêu đề, nhãn trục, chú thích/thang màu và các giá trị heatmap hiển thị rõ. Các bảng số trong báo cáo lấy từ kết quả thống kê của lần chạy.

Các giá trị trung bình và độ lệch chuẩn ở cửa sổ đầu, cửa sổ cuối được đối chiếu bằng phép tính độc lập. Ma trận heatmap có đủ 144 ô, các hình PNG được lưu ở độ phân giải 150 dpi và đường dẫn ảnh trong báo cáo trỏ đúng tới file kết quả.
