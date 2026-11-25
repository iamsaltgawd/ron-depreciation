#!/usr/bin/env bash
set -euo pipefail

out=data/raw/gdelt
mkdir -p "$out"
base="https://api.gdeltproject.org/api/v2/doc/doc"
range="startdatetime=20170101000000&enddatetime=$(date -u +%Y%m%d)000000"

for mode in timelinevolraw timelinetone; do
    file="$out/$mode.csv"
    if [[ -s $file ]]; then
        echo "skipping $mode (already downloaded)"
        continue
    fi
    echo "fetching $mode"
    curl -fsSL --retry 3 --retry-delay 60 -A "Mozilla/5.0" -o "$file.tmp" \
      "$base?query=romania&mode=$mode&format=csv&$range"
    mv "$file.tmp" "$file"
    sleep 30
done
