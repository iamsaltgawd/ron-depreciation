#!/usr/bin/env bash
set -euo pipefail

out=data/raw/markets
mkdir -p "$out"

start=$(date -d 2014-01-01 +%s)
end=$(date +%s)

for ticker in %5EVIX BZ%3DF %5EGDAXI SI%3DF; do
    name=$(printf '%s' "$ticker" | sed 's/%5E//; s/%3DF//')
    echo "fetching $name"
    curl -fsSL --retry 3 -A "Mozilla/5.0" -o "$out/$name.json" \
      "https://query1.finance.yahoo.com/v8/finance/chart/$ticker?period1=$start&period2=$end&interval=1d"
    sleep 1
done
