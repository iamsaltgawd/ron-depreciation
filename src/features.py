from pathlib import Path

import numpy as np
import pandas as pd

P = Path("data/processed")
OUT = P / "dataset.parquet"

START, END = "2017-01-01", "2026-11-20"
HORIZON = 5

GDELT_LAG = pd.Timedelta(days=1)
GPR_LAG = pd.Timedelta(days=14)
MACRO_LAGS = {"economic_sentiment": 0, "ro_bond_yield_10y": 10, "ro_de_bond_spread": 10,
              "inflation_yoy": 20, "retail_sales_yoy": 40,
              "industrial_production_yoy": 45, "gdp_growth_qoq": 60}

GPR_NAMES = {"gpr": "geo_risk", "gpr_act": "geo_risk_acts", "gpr_threat": "geo_risk_threats",
             "gpr_ma7": "geo_risk_avg_7d", "gpr_ma30": "geo_risk_avg_30d"}
MACRO_NAMES = {"esi": "economic_sentiment", "yield_ro": "ro_bond_yield_10y",
               "spread": "ro_de_bond_spread", "hicp": "inflation_yoy",
               "retail_yoy": "retail_sales_yoy", "industry_yoy": "industrial_production_yoy",
               "gdp_qoq": "gdp_growth_qoq"}


def to_days(data, days, lag=pd.Timedelta(0)):
    data = data.copy()
    data.index = data.index + lag
    return data.reindex(data.index.union(days)).ffill().reindex(days)


def change(s, n=1):
    return 100 * np.log(s).diff(n)


def main():
    rates = pd.read_parquet(P / "bnr_rates.parquet").loc[:END]
    neer = pd.read_parquet(P / "neer.parquet")["neer"].loc[:END]
    markets = pd.read_parquet(P / "markets.parquet").loc[:END]
    gpr = (pd.read_parquet(P / "gpr.parquet").drop(columns="gpr_event")
           .rename(columns=GPR_NAMES).loc[:END])
    gdelt = pd.read_parquet(P / "gdelt.parquet").loc[:END]
    macro = pd.read_parquet(P / "macro.parquet").rename(columns=MACRO_NAMES)

    days = neer.index
    df = pd.DataFrame(index=days)

    df["neer_change_1d"] = change(neer)
    df["neer_change_yesterday"] = df["neer_change_1d"].shift(1)
    df["neer_change_2days_ago"] = df["neer_change_1d"].shift(2)
    df["neer_change_5d"] = change(neer, 5)
    df["neer_change_21d"] = change(neer, 21)
    df["neer_vs_avg_5d"] = 100 * (neer / neer.rolling(5).mean() - 1)
    df["neer_vs_avg_21d"] = 100 * (neer / neer.rolling(21).mean() - 1)
    df["neer_volatility_21d"] = df["neer_change_1d"].rolling(21).std()

    for cur in ["EUR", "USD", "GBP", "CHF", "HUF", "PLN", "CZK"]:
        df[f"{cur.lower()}_change_1d"] = change(rates[cur]).reindex(days)
    df["gold_change_1d"] = change(rates["XAU"]).reindex(days)

    mk = to_days(markets, days)
    df["vix"] = mk["vix"]
    df["vix_change_5d"] = mk["vix"].diff(5)
    for col in ["brent", "dax", "silver"]:
        df[f"{col}_change_1d"] = change(mk[col])
    gold_usd_oz = rates["XAU"].reindex(days) / rates["USD"].reindex(days) * 31.1035
    df["gold_silver_ratio"] = gold_usd_oz / mk["silver"]

    df = df.join(to_days(gpr, days, GPR_LAG))

    share, tone = gdelt["news_share"], gdelt["news_tone"]
    news = pd.DataFrame({
        "news_volume_vs_90d": share.rolling("7D").mean() / share.rolling("90D", min_periods=60).mean(),
        "news_tone_vs_90d": tone.rolling("7D").mean() - tone.rolling("90D", min_periods=60).mean(),
    })
    df = df.join(to_days(news, days, GDELT_LAG))

    for col, lag in MACRO_LAGS.items():
        df[col] = to_days(macro[col].dropna(), days, pd.Timedelta(days=lag))

    df["day_of_week"] = days.day_of_week

    fwd = 100 * np.log(neer.shift(-HORIZON) / neer)
    df["target_neer_change_5d"] = fwd
    df["target_ron_weakens"] = (fwd < 0).astype(int)

    df = df.loc[START:]
    missing = df.isna().sum()
    print("missing before dropna:\n" + missing[missing > 0].to_string())
    df = df.dropna()
    df.index.name = "date"

    df.to_parquet(OUT)
    df.to_csv(P / "dataset.csv")
    print(f"\n{len(df)} rows x {df.shape[1] - 2} features + 2 targets, "
          f"{df.index.min():%Y-%m-%d} to {df.index.max():%Y-%m-%d}")
    print(f"share of RON weakening: {df['target_ron_weakens'].mean():.3f}")


if __name__ == "__main__":
    main()
