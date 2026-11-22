from pathlib import Path

import pandas as pd

RAW = Path("data/raw/macro")
OUT = Path("data/processed/macro.parquet")


def read_series(name, freq):
    df = pd.read_csv(RAW / f"{name}.csv", usecols=["geo", "TIME_PERIOD", "OBS_VALUE"])
    df.index = pd.PeriodIndex(df["TIME_PERIOD"], freq=freq).to_timestamp(how="end").normalize()
    df.index.name = "date"
    return df


def main():
    monthly = {name: read_series(name, "M")["OBS_VALUE"]
               for name in ["hicp", "esi", "industry", "retail"]}
    gdp = read_series("gdp", "Q")["OBS_VALUE"]
    yields = read_series("yields", "M").pivot(columns="geo", values="OBS_VALUE")

    macro = pd.DataFrame({
        "hicp": monthly["hicp"],
        "esi": monthly["esi"],
        "industry_yoy": monthly["industry"].pct_change(12) * 100,
        "retail_yoy": monthly["retail"].pct_change(12) * 100,
        "gdp_qoq": gdp,
        "yield_ro": yields["RO"],
        "yield_de": yields["DE"],
    })
    macro["spread"] = macro["yield_ro"] - macro["yield_de"]
    macro = macro.loc["2014":]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    macro.to_parquet(OUT)
    print(f"{len(macro)} months, {macro.index.min():%Y-%m} to {macro.index.max():%Y-%m}")
    print(macro.notna().sum().to_string())
    print(macro.tail(4).round(2).to_string())


if __name__ == "__main__":
    main()
