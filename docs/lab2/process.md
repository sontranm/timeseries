# Lab 2 Workflow

## Data flow

~~~text
data/raw/
  ├── airline-passengers.csv ──> load_data.py ──> Exercises 1, 2, 3, 4a, 4b, 5
  └── daily-min-temperatures.csv ──> load_data.py ──> Exercise 4a

Exercises 1–5 ──> data/processed/ (derived series and analysis tables)
             ├──> docs/lab2/figures/ (PNG figures at 150 dpi)
             └──> docs/lab2/report.md and process.md
~~~

The source files in data/raw/ remain unchanged. Scripts resolve paths relative
to the repository, so they can be run from the project root. Exercise 4b follows
Exercise 3 because it reads decomposition_stl.csv.

## Environment and execution

The results were generated with Python 3.11.15, NumPy 2.4.6, pandas 3.0.3,
Matplotlib 3.11.0, Seaborn 0.13.2, SciPy 1.17.1, and statsmodels 0.15.0.

Create an environment and run the pipeline:

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/main.py
~~~

The pipeline runs Exercises 1, 2, 3, 4a, 4b, and 5 in order. Random generation
uses seed 42 for the white-noise sample and simulated missing values. ACF/PACF,
Ljung–Box, STL metrics, MAE, and outlier-detection tables are saved in
data/processed/ for comparison with the report.

## Methods by exercise

1. **ACF/PACF:** inspect AirPassengers and calculate 40 lags; estimate PACF with
   Yule–Walker; plot ACF after ordinary and seasonal differencing.
2. **White noise:** generate 1,000 N(0, 1) values; count ACF coefficients outside
   1.96/√n; run Ljung–Box at lags 10 and 20 for white noise and AirPassengers.
3. **Decomposition:** apply multiplicative seasonal_decompose with period 12;
   run robust STL on log values with period 12; calculate trend/seasonal
   strength and check residual autocorrelation.
4. **Missing values:** mask 12 random months and one consecutive three-month
   block; compare forward fill with linear interpolation using MAE; reveal the
   two missing temperature dates with daily asfreq and interpolate them.
5. **Outliers:** apply Z-score, IQR, and a 12-month rolling threshold; compare
   the original series with STL residuals; check three injected deviations on a
   copy; interpolate residual candidates flagged by both Z-score and IQR.
6. **Visualization:** produce a line chart, rolling mean/SD, yearly seasonal
   plot, month-by-year heatmap, and monthly boxplot.

## Group assignments

| Contributor | Assignment |
|---|---|
| Lê Quỳnh | Project setup and Exercise 1 — ACF/PACF |
| Phạm Lê Văn Bảo | Exercise 2 — White noise |
| Bao Dinh | Exercise 3 — Decomposition |
| Trần Minh Sơn | Exercise 4a — Missing values |
| Hoàng Thắng | Exercise 4b — Outliers |
| Hoàng Nam | Exercise 5 — Visualization |
| Thành | Exercise 6 — Consolidated report |

## Review notes

Report values were calculated from the source CSV files and tables in
data/processed/. Interpolated temperatures are estimates, not measurements.
Outlier thresholds produce candidates; this project uses agreement between
Z-score and IQR on the residuals for the cleaning step. Forecast accuracy was
not evaluated out of sample.
