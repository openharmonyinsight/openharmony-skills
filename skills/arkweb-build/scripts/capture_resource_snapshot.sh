#!/usr/bin/env bash

set -euo pipefail

find_arkweb_root() {
  local dir="${1:-$PWD}"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/build_arkweb.sh" && -f "$dir/src/arkweb/build/build.sh" ]]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}

read_cpu_totals() {
  local line user nice system idle iowait irq softirq steal guest guest_nice
  read -r line user nice system idle iowait irq softirq steal guest guest_nice < /proc/stat
  local total=$((user + nice + system + idle + iowait + irq + softirq + steal))
  local idle_all=$((idle + iowait))
  printf '%s %s\n' "$total" "$idle_all"
}

usage() {
  echo "Usage: $0 [product] [label] [arkweb-root-or-subdir]" >&2
  echo "       $0 [product] [arkweb-root-or-subdir]" >&2
  echo "Example: $0 rk3568_64 before-build /path/to/arkweb" >&2
  echo "Example: $0 rk3568_64 /path/to/arkweb" >&2
}

PRODUCT="${1:-rk3568_64}"
LABEL="${2:-snapshot}"
ROOT_HINT="${3:-$PWD}"

if [[ $# -eq 2 && "$2" == /* ]]; then
  LABEL="snapshot"
  ROOT_HINT="$2"
fi

if [[ "$PRODUCT" == /* || "$PRODUCT" == *"/"* || ! "$PRODUCT" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "Invalid product: $PRODUCT" >&2
  echo "The first argument is the product name, for example rk3568_64; it is not the ArkWeb root path." >&2
  usage
  exit 2
fi

if ! ARKWEB_ROOT="$(find_arkweb_root "$ROOT_HINT")"; then
  echo "ArkWeb root not found from: $ROOT_HINT" >&2
  usage
  exit 1
fi

OUT_DIR="$ARKWEB_ROOT/src/out/$PRODUCT"
SNAPSHOT_DIR="$OUT_DIR/resource_snapshots"
mkdir -p "$SNAPSHOT_DIR"

timestamp="$(date +%Y%m%d%H%M%S)"
safe_label="${LABEL// /_}"
safe_label="${safe_label//\//_}"
safe_label="${safe_label//[^A-Za-z0-9._-]/_}"
SNAPSHOT_FILE="$SNAPSHOT_DIR/${timestamp}_${safe_label}.log"

read -r total1 idle1 < <(read_cpu_totals)
sleep 1
read -r total2 idle2 < <(read_cpu_totals)

total_delta=$((total2 - total1))
idle_delta=$((idle2 - idle1))
busy_pct=0
idle_pct=0
if (( total_delta > 0 )); then
  idle_pct=$((100 * idle_delta / total_delta))
  busy_pct=$((100 - idle_pct))
fi

mem_total_kb="$(awk '/MemTotal:/ {print $2}' /proc/meminfo)"
mem_available_kb="$(awk '/MemAvailable:/ {print $2}' /proc/meminfo)"
swap_total_kb="$(awk '/SwapTotal:/ {print $2}' /proc/meminfo)"
swap_free_kb="$(awk '/SwapFree:/ {print $2}' /proc/meminfo)"
nproc_value="$(nproc 2>/dev/null || getconf _NPROCESSORS_ONLN 2>/dev/null || echo unknown)"
load_avg="$(cat /proc/loadavg)"

{
  echo "timestamp=$(date -Iseconds)"
  echo "label=$LABEL"
  echo "arkweb_root=$ARKWEB_ROOT"
  echo "product=$PRODUCT"
  echo "snapshot_file=$SNAPSHOT_FILE"
  echo "nproc=$nproc_value"
  echo "cpu_busy_percent_estimate=$busy_pct"
  echo "cpu_idle_percent_estimate=$idle_pct"
  echo "loadavg=$load_avg"
  echo "mem_total_kb=$mem_total_kb"
  echo "mem_available_kb=$mem_available_kb"
  echo "swap_total_kb=$swap_total_kb"
  echo "swap_free_kb=$swap_free_kb"
  echo
  echo "== free -h =="
  free -h
  echo
  echo "== top cpu consumers =="
  ps -eo pid,ppid,comm,%cpu,%mem --sort=-%cpu | head -n 15
  echo
  echo "== top memory consumers =="
  ps -eo pid,ppid,comm,%cpu,%mem --sort=-%mem | head -n 15
} > "$SNAPSHOT_FILE"

echo "Resource snapshot written to: $SNAPSHOT_FILE"
