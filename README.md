# Lab 2 — Time Series Analysis

Chapter 2 practical assignment on describing and checking time series, using
AirPassengers and daily minimum temperatures in Melbourne.

## Objectives

1. Examine ACF/PACF and identify trend and seasonality.
2. Simulate white noise and compare it with a structured series using Ljung–Box.
3. Decompose a series into trend, seasonal, and residual components with
   classical decomposition and STL.
4. Simulate missing values, handle calendar gaps, and examine outliers.
5. Visualize the data with rolling statistics, seasonal plots, a heatmap, and
   monthly boxplots.
6. Summarize the methods, results, limitations, and forecasting implications.

## Data

### AirPassengers

Monthly international airline passenger counts from January 1949 through
December 1960 (144 observations), measured in thousands. The source columns are
Month and Passengers; there are no missing observations. The dataset is cited
in the group assignment as the [Brownlee time-series
dataset](https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv),
from Box & Jenkins, *Time Series Analysis: Forecasting and Control*.

### Daily minimum temperatures

Daily minimum temperature in Melbourne, Australia, during 1981–1990. The source
columns are Date and Temp (°C). The observations do not cover every calendar
day; asfreq("D") reveals the missing dates before interpolation. The dataset is
cited in the group assignment as the [Brownlee daily-min-temperatures
dataset](https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv),
originally from the Australian Bureau of Meteorology.

The source files are kept unchanged in data/raw/. Simulated gaps, imputations,
and outlier handling are written to data/processed/.

## Environment

The pipeline was run with Python 3.11.15, NumPy 2.4.6, pandas 3.0.3, Matplotlib
3.11.0, Seaborn 0.13.2, SciPy 1.17.1, and statsmodels 0.15.0. Python 3.10 or
later is required.

## Install and run

~~~bash
git clone https://github.com/sontranm/timeseries.git
cd timeseries
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/main.py
~~~

On Windows, activate the environment with .venv\Scripts\activate. Individual
exercises can also be run from the repository root:

~~~bash
python src/b1_acf_pacf.py
python src/b4a_missing.py
~~~

The pipeline runs Exercises 1, 2, 3, 4a, 4b, and 5 in order because Exercise 4b
uses the STL residuals produced by Exercise 3. Figures are saved in
docs/lab2/figures/, processed data and intermediate tables in data/processed/,
and the consolidated report and workflow in docs/lab2/.

## Project structure

~~~text
.
├── data/
│   ├── raw/                       # Original, unchanged datasets
│   └── processed/                 # Derived series and analysis tables
├── src/
│   ├── bootstrap.py               # Matplotlib cache configuration
│   ├── load_data.py               # Shared data loaders
│   ├── analysis_utils.py          # Shared statistics and plotting helpers
│   ├── b1_acf_pacf.py
│   ├── b2_white_noise.py
│   ├── b3_decomposition.py
│   ├── b4a_missing.py
│   ├── b4b_outliers.py
│   ├── b5_visualization.py
│   └── main.py                    # Run the full analysis
├── requirements.txt
├── docs/lab2/
│   ├── figures/                   # PNG figures at 150 dpi
│   ├── report.md                  # Consolidated report
│   └── process.md                 # Consolidated workflow
└── team-assignment.md             # Team roles and work plan
~~~

## Contributors

| Contributor | Assignment |
|---|---|
| Lê Quỳnh | Project setup and Exercise 1 — ACF/PACF |
| Phạm Lê Văn Bảo | Exercise 2 — White noise |
| Bao Dinh | Exercise 3 — Decomposition |
| Trần Minh Sơn | Exercise 4a — Missing values |
| Hoàng Thắng | Exercise 4b — Outliers |
| Hoàng Nam | Exercise 5 — Visualization |
| Thành | Exercise 6 — Report and project review |

The consolidated results and workflow are in docs/lab2/.
