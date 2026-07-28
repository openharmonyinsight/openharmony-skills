#!/usr/bin/env bash
# api-reference external data dependency — probe + install instructions.
#
# The API reference data is NOT shipped in this repo (too large / maintained
# upstream / evolves with SDK versions). This script probes the local install
# and prints how to provide it. It does NOT download, does NOT touch the
# network, and does NOT modify the user environment.
#
# Usage:
#   bash reference/api-reference/install.sh             # probe all installed domains
#   bash reference/api-reference/install.sh <domain>     # probe one domain
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
DOMAIN="${1:-}"

echo "api-reference external dependency probe"
echo "install root: $HERE"
echo

if [ -n "$DOMAIN" ]; then
  idx="$HERE/$DOMAIN/index.json"
  if [ -f "$idx" ]; then
    echo "[OK]      $DOMAIN: index.json present -> Demo Pipeline FULL mode for this domain"
  else
    echo "[MISSING] $DOMAIN: index.json not found -> Demo Pipeline DEGRADED mode"
    echo "          (APIs marked '⚠️ 无 API 参考', gate decides; NOT independent-run)"
    echo "          place data at: $HERE/$DOMAIN/index.json (+ referenced API JSON files)"
  fi
  exit 0
fi

echo "installed domains:"
found=0
shopt -s nullglob
for d in "$HERE"/*/; do
  name="$(basename "$d")"
  if [ -f "$d/index.json" ]; then
    echo "  [OK]      $name"
    found=1
  else
    echo "  [partial] $name (no index.json)"
  fi
done
if [ "$found" -eq 0 ]; then
  echo "  (none — Demo Pipeline runs in DEGRADED mode until data is installed; NOT independent-run)"
fi
echo
echo "How to provide api-reference data:"
echo "  1. Obtain the domain's index.json (schema: modules[].files[]{name,type,file}) and referenced API JSON files."
echo "  2. Place them under: $HERE/<domain>/"
echo "  3. Re-run: bash reference/api-reference/install.sh <domain>"
echo "Until installed, Demo Pipeline does NOT claim independent run; it degrades with '⚠️ 无 API 参考' markers."
