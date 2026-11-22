#!/usr/bin/env bash
set -euo pipefail

out=data/raw/ecb
mkdir -p "$out"
curl -fsSL --retry 3 -o "$out/neer_ron.csv" \
  "https://data-api.ecb.europa.eu/service/data/EXR/D.E03.RON.EN00.A?format=csvdata&startPeriod=2014-01-01"
