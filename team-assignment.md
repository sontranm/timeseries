# Lab 2 Team Assignment Plan

**Seven-member team** · Team leader: Trần Minh Sơn · Report writer: Thành

## 1. Role assignment

Six roles were assigned by randomly shuffling the member list in Python with
`random.shuffle`. Thành took role 7 (report writing) as requested.

| # | Member | Assignment | Source files |
|---:|---|---|---|
| 1 | Lê Quỳnh | Project setup, README, Exercise 1 — ACF/PACF | `load_data.py`, `b1_acf_pacf.py` |
| 2 | Phạm Lê Văn Bảo | Exercise 2 — White noise | `b2_white_noise.py` |
| 3 | Bao Dinh | Exercise 3 — Time-series decomposition | `b3_decomposition.py` |
| 4 | Trần Minh Sơn | Exercise 4a — Missing values (NaN, forward fill, interpolation) | `b4a_missing.py` |
| 5 | Hoàng Thắng | Exercise 4b — Outliers (rolling threshold, Z-score, IQR) | `b4b_outliers.py` |
| 6 | Hoàng Nam | Exercise 5 — Visualization | `b5_visualization.py` |
| 7 | Thành | Exercise 6 — Report and project review | `main.py` |

Exercise 4 was split between two people because it contains two distinct tasks:
handling missing values and detecting outliers. Since the assignment has six
exercises and Exercise 6 is the report, the remaining five analysis exercises
were shared among six people. Role 1 also handles setup and the README because
Exercise 1 begins with loading the data.

## 2. Schedule

Let **H** be the instructor's submission deadline.

| Milestone | Owner | Deliverable |
|---|---|---|
| First day | Lê Quỳnh | Set up the repository, place the source data in `data/raw/`, create `src/load_data.py`, and share the repository with the team. |
| First day | Thành | Share this assignment plan, confirm the internal deadline, and send the Data Introduction text to Lê Quỳnh. |
| As early as possible | Bao Dinh | Export `data/processed/decomposition_stl.csv`; Hoàng Thắng needs it for Exercise 4b. |
| H − 3 days | All six exercise owners | Submit code, figures, processed data, and draft Markdown notes. |
| H − 1 day | Thành | Finish `report.md` and `process.md`, then ask the team to review them. |
| H | Thành and Trần Minh Sơn | Run the complete project one last time and submit it. |

Team leader Trần Minh Sơn tracks progress in the group chat, especially at
the H − 3 day milestone.

## 3. Project structure

The project is kept in one shared GitHub repository or Google Drive folder.

~~~text
timeseries/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                       # Original source data; do not edit
│   └── processed/                 # Derived series and analysis tables
├── src/                           # One focused Python script per exercise
│   ├── load_data.py
│   ├── b1_acf_pacf.py
│   ├── b2_white_noise.py
│   ├── b3_decomposition.py
│   ├── b4a_missing.py
│   ├── b4b_outliers.py
│   ├── b5_visualization.py
│   └── main.py
└── docs/lab2/
    ├── report.md
    ├── process.md
    └── figures/
~~~

### Team conventions

1. Submit Python source files in `src/`. Notebooks may be used for exploration,
   but the submitted `.py` files must run independently from the repository
   root, for example: `python src/b1_acf_pacf.py`.
2. Load data through `load_data.py`; do not download a second copy from the
   internet. Shared imports include `load_airpassengers`, `load_temperatures`,
   `PROCESSED`, and `FIG`.
3. Keep `data/raw/` unchanged. Write transformed data to `data/processed/`.
4. Save figures as PNG files in `docs/lab2/figures/` at 150 dpi. Each figure
   should have a title, labeled axes, and a legend when needed. Prefix filenames
   with the exercise identifier, such as `b1_acf.png` or `b3_stl.png`.
5. Set `np.random.seed(42)` wherever randomness is used so results can be
   reproduced.
6. At the start of each `.py` file, document the exercise, contributor, and
   purpose of the file.
7. During drafting, each exercise owner supplies a report note and a process
   note. The report note should include figures, specific numeric results, and
   interpretation; the process note should record steps, functions, libraries,
   parameter choices, intermediate results, and fixes for problems encountered.

## 4. Data

### AirPassengers

| Property | Description |
|---|---|
| Contents | Monthly international airline passenger counts, in thousands |
| Source | Box and Jenkins, *Time Series Analysis: Forecasting and Control* |
| Period | January 1949–December 1960 |
| Frequency | Monthly |
| Observations | 144, with no missing values |
| Columns | `Month` (for example, `1949-01`) and integer `Passengers` |
| Summary | Minimum 104, maximum 622, mean about 280.3, standard deviation about 120 |
| Download | [AirPassengers CSV](https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv) |

### Daily minimum temperatures

Trần Minh Sơn also uses this dataset in Exercise 4a.

| Property | Description |
|---|---|
| Contents | Daily minimum temperature in Melbourne, Australia, in °C |
| Source | Australian Bureau of Meteorology |
| Period | January 1, 1981–December 31, 1990 |
| Frequency | Daily |
| Rows and columns | 3,650 source rows; `Date` and `Temp` |
| Data gaps | Two missing calendar dates: 1984-12-31 and 1988-12-31 |
| Download | [Daily minimum temperatures CSV](https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv) |

The shared loader in `src/load_data.py` reads both local source files and
creates the processed-data and figure directories when needed. AirPassengers
is indexed at monthly-start frequency; temperatures are indexed by date.

## 5. Individual assignments

### 5.1. Lê Quỳnh — Project setup, README, and Exercise 1

**Project setup**

1. Create the shared repository with the structure in Section 3.
2. Download both CSV files to `data/raw/` and create the shared loader.
3. Create `requirements.txt` with pandas, NumPy, Matplotlib, Seaborn,
   statsmodels, and SciPy.
4. Invite the team and share the repository link.

**README**

Include the lab introduction and six objectives, data sources and variables,
the Python and library versions, installation and run instructions, the
project tree, and the contributor table.

**Exercise 1: ACF/PACF**

1. Print the first observations and descriptive statistics; draw the series.
2. Plot ACF and PACF through lag 40, using the Yule–Walker method for PACF.
3. Report ACF and PACF at lags 1, 12, 24, and 36.
4. Also plot the ACF after first differencing and seasonal differencing at lag
   12.

Understand the definitions of ACF and PACF, the approximate 95% band
`±1.96/√n`, and how slow ACF decay and repeated peaks at lags 12, 24, and 36
indicate trend and annual seasonality.

**Deliverables:** runnable `b1_acf_pacf.py`; `b1_line.png`, `b1_acf.png`,
`b1_pacf.png`, and `b1_acf_differenced.png`; a report note with the requested
lag values and short answers about autocorrelation, trend/seasonality, and the
most important lag; and a process note.

### 5.2. Phạm Lê Văn Bảo — Exercise 2: White noise

1. Generate 1,000 standard normal values with seed 42 and save
   `data/processed/white_noise.csv`.
2. Plot the simulated series and its ACF through lag 40; count lags outside the
   approximate 95% band.
3. Run the Ljung–Box test at lags 10 and 20 for white noise and AirPassengers.
4. Plot both ACFs side by side.

Understand white noise (zero mean, constant variance, and no autocorrelation),
why some of 40 ACF coefficients can exceed the band by chance, and how to
interpret Ljung–Box p-values. At the 5% level, p > 0.05 means the null of no
autocorrelation is not rejected.

**Deliverables:** runnable `b2_white_noise.py`; the processed CSV;
`b2_white_noise_line.png`, `b2_white_noise_acf.png`, and
`b2_acf_comparison.png`; a report note with the exceedance count, p-value table,
and a five-line comparison; and a process note.

### 5.3. Bao Dinh — Exercise 3: Time-series decomposition

Hoàng Thắng needs `decomposition_stl.csv` for Exercise 4b, so complete and
share that output early.

1. Use AirPassengers with a seasonal period of 12.
2. Apply multiplicative classical decomposition and plot all four components.
3. Apply STL to `log(y)` with period 12, plot its components, and save the trend,
   seasonal, and residual columns to `data/processed/decomposition_stl.csv`.
4. Plot the residual ACF and run the Ljung–Box test.
5. Also calculate trend and seasonal strength using
   `FT = max(0, 1 − Var(R)/Var(T + R))` and
   `FS = max(0, 1 − Var(R)/Var(S + R))`.

Understand observed, trend, seasonal, and residual components; additive and
multiplicative models; and the differences between classical decomposition
and STL.

**Deliverables:** runnable `b3_decomposition.py`; the STL CSV;
`b3_classical.png`, `b3_stl.png`, and `b3_resid_acf.png`; a report note on trend,
seasonality and its peak month, residual behavior, strength measures, and
Ljung–Box p-values; and a process note.

### 5.4. Trần Minh Sơn — Exercise 4a: Missing values

1. Copy AirPassengers, mask about 10% of its values with seed 42, and add one
   consecutive three-month gap.
2. Count and list the missing timestamps.
3. Impute using forward fill and linear interpolation; calculate each method's
   MAE against the hidden true values.
4. Plot the reference series, gaps, and both imputed series together; save the
   better-performing result as `data/processed/airpassengers_filled.csv`.
5. Reindex the temperature series to daily frequency, reveal the two real gaps,
   interpolate them, plot the surrounding dates, and save
   `data/processed/temperatures_filled.csv`.

Understand why dropping missing rows breaks time continuity, the trade-offs
between forward fill and interpolation, and how pandas `asfreq` reveals missing
calendar dates.

**Deliverables:** runnable `b4a_missing.py`; both processed CSVs;
`b4a_missing_imputation.png` and `b4a_temperature_gaps.png`; a report note with
missing counts, MAE values, and a short recommendation; and a process note.

### 5.5. Hoàng Thắng — Exercise 4b: Outliers

Use Bao Dinh's `decomposition_stl.csv`. While waiting for it, start the work on
the original series and the synthetic check.

1. On the original series, calculate a 12-month rolling mean and standard
   deviation; flag values more than three standard deviations from the rolling
   mean.
2. Apply Z-score (absolute z > 3) and IQR fences to STL residuals, and try the
   same methods on the original series for comparison.
3. Add two or three deliberately large outliers to a copy of the residuals and
   check whether the methods detect them.
4. Interpolate any consensus candidates and save the cleaned series to
   `data/processed/airpassengers_clean.csv`. If no candidates are found, keep
   the original series and state that in the report.
5. Plot the flagged points and show the series before and after handling.

Understand the assumptions behind Z-score and IQR and why trend and seasonality
can cause false flags when outlier detection is applied directly to the raw
series.

**Deliverables:** runnable `b4b_outliers.py`; the cleaned CSV;
`b4b_outlier.png` and `b4b_before_after.png`; a report note listing dates,
values, methods, and whether the candidates seem plausible; and a process note.

### 5.6. Hoàng Nam — Exercise 5: Visualization

1. Plot the full series.
2. Overlay 12-month rolling mean and standard deviation.
3. Create a seasonal plot with one line per year and months 1–12 on the
   horizontal axis.
4. Create an annotated month-by-year heatmap.
5. Also create a boxplot by calendar month.

Understand rolling windows, what a rising rolling standard deviation says about
variation, how to read the seasonal plot and heatmap, and the Seaborn heatmap
and plotting functions.

**Deliverables:** runnable `b5_visualization.py`;
`b5_line.png`, `b5_rolling.png`, `b5_seasonal.png`, `b5_heatmap.png`, and
`b5_boxplot.png`; a report note on the overall trend, peak and low months,
seasonal amplitude over time, and unusual points; and a process note.

### 5.7. Thành — Exercise 6: Report and project review

1. Share the assignment plan and confirm the internal deadline; send the Data
   Introduction to Lê Quỳnh for the README.
2. Create `src/main.py` to run exercises 1 through 5 in order: b1, b2, b3, b4a,
   b4b, and b5. Exercise 4b depends on the decomposition output from Exercise 3.
3. Review each contribution for runnable code, figures, processed data, and
   clear report and process notes. Return incomplete work for correction.
4. Consolidate `docs/lab2/report.md` with seven sections: dataset description,
   ACF/PACF, white-noise check, decomposition, data quality, visualization
   findings, and a conclusion about forecasting implications.
5. Consolidate `docs/lab2/process.md` with the data flow, methods and
   intermediate results, and contributor roles.
6. Make the language and figure references consistent; number figures and
   tables when appropriate.
7. Cross-check that the 12-month seasonality, outlier interpretation, and
   conclusions agree across sections.
8. Run the full project from a clean environment according to the README before
   submission.

The conclusion should explain that AirPassengers has structure (trend,
seasonality, and autocorrelation) that can be explored with forecasting
methods. It is non-stationary and its seasonal amplitude grows, so a log
transform, differencing, or a seasonal model may be considered. State the
limitations: 144 historical observations from 1949–1960, and no fitted model
or holdout evaluation in this lab.

**Final checklist:** `report.md` has all seven sections and working figure
links; `process.md` explains the workflow; `src/main.py` regenerates the
outputs; and the README provides reproducible setup and run instructions.

> For later labs, create a parallel `docs/lab3/`, `docs/lab4/`, and so on. The
> course report can combine them into separate lab chapters if requested.
