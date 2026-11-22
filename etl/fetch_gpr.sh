#!/usr/bin/env bash
set -euo pipefail

out=data/raw/gpr
mkdir -p "$out"
curl -fsSL --retry 3 -o "$out/data_gpr_daily_recent.xls" \
  "https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.xls"
