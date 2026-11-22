import json
from pathlib import Path

import pandas as pd

RAW = Path("data/raw/markets")
OUT = Path("data/processed/markets.parquet")
NAMES = {"VIX": "vix", "BZ": "brent", "GDAXI": "dax", "SI": "silver"}


def parse_file(path):
    result = json.loads(path.read_text())["chart"]["result"][0]
    tz = result["meta"]["exchangeTimezoneName"]
    dates = (pd.to_datetime(result["timestamp"], unit="s", utc=True)
             .tz_convert(tz).normalize().tz_localize(None))
    close = result["indicators"]["quote"][0]["close"]
    series = pd.Series(close, index=dates, dtype=float).dropna()
    return series[~series.index.duplicated(keep="last")]


def main():
    markets = pd.DataFrame({col: parse_file(RAW / f"{name}.json") for name, col in NAMES.items()})
    markets.index.name = "date"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    markets.to_parquet(OUT)
    print(f"{len(markets)} days, {markets.index.min():%Y-%m-%d} to {markets.index.max():%Y-%m-%d}")
    print(markets.notna().sum().to_string())
    print(markets.tail(3).round(2).to_string())


if __name__ == "__main__":
    main()
