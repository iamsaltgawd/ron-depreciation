from pathlib import Path

import numpy as np
import pandas as pd

RATES = Path("data/processed/bnr_rates.parquet")
WEIGHTS = Path("data/processed/weights.parquet")
OUT = Path("data/processed/neer.parquet")


def main():
    weights = pd.read_parquet(WEIGHTS).pivot(index="year", columns="currency", values="weight")
    rates = pd.read_parquet(RATES)[weights.columns]
    rates = rates.loc[str(weights.index.min()):]

    if rates.isna().any().any():
        raise SystemExit("missing basket rates:\n" + rates.isna().sum().to_string())

    log_change = np.log(rates).diff()

    daily_weights = weights.loc[rates.index.year].to_numpy()
    neer_log_change = -(log_change * daily_weights).sum(axis=1)

    neer = 100 * np.exp(neer_log_change.cumsum())
    neer.to_frame("neer").to_parquet(OUT)

    print(f"{len(neer)} days, {neer.index.min():%Y-%m-%d} to {neer.index.max():%Y-%m-%d}")
    print(neer.resample("YE").last().round(2).to_string())


if __name__ == "__main__":
    main()
