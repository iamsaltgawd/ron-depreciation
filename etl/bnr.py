from pathlib import Path
import xml.etree.ElementTree as ET

import pandas as pd

RAW = Path("data/raw/bnr")
OUT = Path("data/processed/bnr_rates.parquet")


def parse_file(path):
    root = ET.parse(path).getroot()
    rows = []
    for cube in root.iterfind(".//{*}Cube"):
        date = cube.get("date")
        for rate in cube.iterfind("{*}Rate"):
            if rate.text == "-":
                continue
            value = float(rate.text)
            multiplier = int(rate.get("multiplier", 1))
            rows.append((date, rate.get("currency"), value / multiplier))
    return rows


def main():
    rows = []
    for path in sorted(RAW.glob("nbrfxrates*.xml")):
        rows.extend(parse_file(path))

    if not rows:
        raise SystemExit(f"no rates parsed from {RAW}, check the path and XML structure")

    long = pd.DataFrame(rows, columns=["date", "currency", "rate"])
    long["date"] = pd.to_datetime(long["date"])
    wide = long.pivot(index="date", columns="currency", values="rate").sort_index()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wide.to_parquet(OUT)
    print(f"{len(wide)} days, {wide.shape[1]} currencies, "
          f"{wide.index.min():%Y-%m-%d} to {wide.index.max():%Y-%m-%d}")


if __name__ == "__main__":
    main()
