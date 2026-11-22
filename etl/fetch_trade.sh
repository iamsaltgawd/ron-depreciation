#!/usr/bin/env bash
set -euo pipefail

out=data/raw/trade
mkdir -p "$out"

curl -fsSL --retry 3 -o "$out/comext_ro.csv" \
  "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/A.RO..TOTAL.1+2.VALUE_IN_EUROS?format=SDMX-CSV&startPeriod=2013"
