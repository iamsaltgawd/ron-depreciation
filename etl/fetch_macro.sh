#!/usr/bin/env bash
set -euo pipefail

out=data/raw/macro
mkdir -p "$out"
base="https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"

declare -A series=(
    [hicp]="prc_hicp_minr/M.RCH_A.TOTAL.RO"
    [esi]="ei_bssi_m_r2/M.BS-ESI-I.SA.RO"
    [industry]="sts_inpr_m/M.PRD.B-D.SCA.I21.RO"
    [retail]="sts_trtu_m/M.VOL_SLS.G47.SCA.I21.RO"
    [gdp]="namq_10_gdp/Q.CLV_PCH_PRE.SCA.B1GQ.RO"
    [yields]="irt_lt_mcby_m/M.MCBY.RO+DE"
)

for name in "${!series[@]}"; do
    echo "fetching $name"
    curl -fsSL --retry 3 -o "$out/$name.csv" \
      "$base/${series[$name]}?format=SDMX-CSV&startPeriod=2013-01"
    sleep 1
done
