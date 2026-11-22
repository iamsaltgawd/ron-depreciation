from pathlib import Path

import pandas as pd

RAW = Path("data/raw/trade/comext_ro.csv")
OUT = Path("data/processed/weights.parquet")

EURO_AREA = ["AT", "BE", "CY", "DE", "EE", "ES", "FI", "FR", "GR", "HR", "IE",
             "IT", "LT", "LU", "LV", "MT", "NL", "PT", "SI", "SK", "BG"]

CURRENCY = {country: "EUR" for country in EURO_AREA} | {
    "HU": "HUF", "PL": "PLN", "TR": "TRY", "CN": "CNY", "CZ": "CZK", "GB": "GBP",
    "US": "USD", "MD": "MDL", "UA": "UAH", "CH": "CHF", "XS": "RSD", "RU": "RUB",
}


def main():
    trade = pd.read_csv(RAW, usecols=["partner", "TIME_PERIOD", "OBS_VALUE"])
    trade = trade.rename(columns={"TIME_PERIOD": "trade_year", "OBS_VALUE": "value"})

    trade["currency"] = trade["partner"].map(CURRENCY)
    basket = trade.dropna(subset=["currency"])

    totals = basket.groupby(["trade_year", "currency"])["value"].sum()
    weights = totals / totals.groupby(level="trade_year").transform("sum")

    weights = weights.rename("weight").reset_index()
    weights["year"] = weights["trade_year"] + 1
    weights = weights[["year", "currency", "weight"]]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    weights.to_parquet(OUT, index=False)
    print(weights.pivot(index="year", columns="currency", values="weight").round(3).to_string())


if __name__ == "__main__":
    main()
