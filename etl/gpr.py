from pathlib import Path

import pandas as pd

RAW = Path("data/raw/gpr/data_gpr_daily_recent.xls")
OUT = Path("data/processed/gpr.parquet")

COLUMNS = {
    "GPRD": "gpr",
    "GPRD_ACT": "gpr_act",
    "GPRD_THREAT": "gpr_threat",
    "GPRD_MA7": "gpr_ma7",
    "GPRD_MA30": "gpr_ma30",
    "event": "gpr_event",
}


def main():
    gpr = pd.read_excel(RAW, engine="calamine", usecols=["date", *COLUMNS])
    gpr["date"] = pd.to_datetime(gpr["date"])
    gpr = gpr.rename(columns=COLUMNS).set_index("date").sort_index()
    gpr = gpr.loc["2014":]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    gpr.to_parquet(OUT)
    print(f"{len(gpr)} days, {gpr.index.min():%Y-%m-%d} to {gpr.index.max():%Y-%m-%d}")
    print(gpr.drop(columns="gpr_event").describe().round(1).to_string())
    print(gpr["gpr_event"].dropna().tail(5).to_string())


if __name__ == "__main__":
    main()
