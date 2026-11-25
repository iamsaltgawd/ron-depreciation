from pathlib import Path

import pandas as pd

RAW = Path("data/raw/gdelt")
OUT = Path("data/processed/gdelt.parquet")


def read_timeline(name):
    df = pd.read_csv(RAW / f"{name}.csv", encoding="utf-8-sig", parse_dates=["Date"])
    df = df.pivot(index="Date", columns="Series", values="Value")
    return df.iloc[:-1]


def main():
    vol = read_timeline("timelinevolraw")
    tone = read_timeline("timelinetone")

    gdelt = pd.DataFrame({
        "news_share": vol["Article Count"] / vol["Total Monitored Articles"] * 10_000,
        "news_tone": tone["Average Tone"],
    }).dropna()
    gdelt.index.name = "date"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    gdelt.to_parquet(OUT)

    all_days = pd.date_range(gdelt.index.min(), gdelt.index.max())
    print(f"{len(gdelt)} days, {gdelt.index.min():%Y-%m-%d} to {gdelt.index.max():%Y-%m-%d}, "
          f"{len(all_days) - len(gdelt)} calendar days missing")
    print(gdelt.resample("YE").mean().round(2).to_string())


if __name__ == "__main__":
    main()
