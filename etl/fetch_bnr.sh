#!/usr/bin/env bash
set -euo pipefail

out=data/raw/bnr
mkdir -p "$out"
current=$(date +%Y)

for year in $(seq 2005 "$current"); do
    file="$out/nbrfxrates$year.xml"
    if [[ -f $file && $year -ne $current ]]; then
        continue
    fi
    echo "fetching $year"
    curl -fsSL --retry 3 -o "$file" \
        "https://curs.bnr.ro/files/xml/years/nbrfxrates$year.xml"
    sleep 1
done
