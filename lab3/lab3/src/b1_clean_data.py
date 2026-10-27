import pandas as pd

from load_data import PROCESSED, load_aep_raw


def main():
    df = load_aep_raw()
    print("Rows:", len(df), "| Range:", df["Datetime"].min(), "->", df["Datetime"].max())
    print("Missing values:", int(df["AEP_MW"].isna().sum()))

    df = df.sort_values("Datetime").reset_index(drop=True)

    dup = int(df["Datetime"].duplicated().sum())
    print("Duplicate timestamps:", dup)
    df = df.groupby("Datetime", as_index=False)["AEP_MW"].mean()

    series = df.set_index("Datetime")["AEP_MW"].asfreq("h")
    print("Missing hours:", int(series.isna().sum()))
    series = series.interpolate(method="time")

    print("Values <= 0:", int((series <= 0).sum()))
    print(series.describe().round(1))

    series.rename("AEP_MW").reset_index().to_csv(PROCESSED / "b1_aep_clean.csv", index=False)
    print("Saved: data/processed/b1_aep_clean.csv")


if __name__ == "__main__":
    main()
