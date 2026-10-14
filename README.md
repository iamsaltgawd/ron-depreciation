# RON Depreciation Prediction

This project tries to predict short periods in which the Romanian currency loses value. The dataset is built from scratch out of public sources rather than taken from an existing collection.

## Description

Most analyses of RON look only at the EUR/RON rate. That rate is closely managed by the National Bank of Romania, so on its own it says little about how the currency is really doing. Instead, this project measures the overall strength of RON with a trade-weighted nominal effective exchange rate: the value of RON against a basket of foreign currencies, where each currency counts in proportion to its share in Romania's foreign trade. The index is computed in the project and serves as the prediction target.

## Scope

The task is binary classification. For every banking day, the model has to say whether the effective exchange rate of RON will fall by more than a given threshold over the following five banking days. The threshold is chosen so that roughly one day in eight counts as a depreciation episode. The data covers 2015 to the present, which gives around 2800 daily entries with more than 15 features each.

## Data sources

Daily reference exchange rates for about thirty currencies and gold come from the XML archives published by the National Bank of Romania. The weights of the currency basket are computed from Romania's exports and imports by partner country, using data from the National Institute of Statistics, Eurostat and the World Bank. Market context comes from Yahoo Finance (silver, the VIX volatility index, Brent oil and the DAX index), and the ROBOR interbank rate is taken from the National Bank of Romania.

Political and geopolitical context comes from two daily sources: GDELT, which counts news events about Romania and measures their tone, and the Geopolitical Risk Index of Caldara and Iacoviello. Slower macroeconomic indicators such as GDP growth, inflation and the Economic Sentiment Indicator are added from the National Institute of Statistics and Eurostat, each aligned on the day it was published so that the model never sees information before it was available. A small hand-built calendar marks Romanian elections and the policy meetings of the National Bank of Romania and the European Central Bank.

To check that the index is built correctly, it is compared with the official effective exchange rate for Romania published by the Bank for International Settlements.

## Repository

The `etl` folder holds one data collection script per source. Downloaded files go into `data/raw` and are not committed, while the merged dataset lives in `data/processed`. Feature engineering, the construction of the index and the models are in `src`, the analysis is in `notebooks`, and the final report is in `report`.
