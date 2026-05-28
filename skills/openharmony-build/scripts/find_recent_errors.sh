#!/bin/bash
# Find recent build errors in OpenHarmony build logs
# Useful for quick error checking during active development

set -e

find_root() {
    local dir="${1:-$PWD}"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/.gn" && -f "$dir/build.sh" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

build_log_path() {
    local product="$1"
    local root="$2"
    if [[ "$product" == "host_product" ]]; then
        echo "$root/out/host/host_product/build.log"
    elif [[ "$product" == "ohos-sdk" || "$product" == "sdk" ]]; then
        echo "$root/out/sdk/build.log"
    elif [[ "$product" == "standard" || "$product" == "independent" || "$product" == "component" || "$product" == "component-independent" ]]; then
        echo "$root/out/standard/build.log"
    else
        echo "$root/out/$product/build.log"
    fi
}

# Default product if none specified
PRODUCT="${1:-rk3568}"
ROOT_HINT="${2:-$PWD}"
if ! OH_ROOT="$(find_root "$ROOT_HINT")"; then
    echo "OpenHarmony root not found from: $ROOT_HINT"
    exit 1
fi
BUILD_LOG="$(build_log_path "$PRODUCT" "$OH_ROOT")"

if [ ! -f "$BUILD_LOG" ]; then
    echo "Build log not found: $BUILD_LOG"
    echo ""
    echo "Usage: $0 [product-name] [openharmony-root]"
    echo "Example: $0 rk3568 /path/to/OpenHarmony"
    echo "Example: $0 standard /path/to/OpenHarmony    # independent component build"
    exit 1
fi

echo "Searching for recent errors in: $BUILD_LOG"
echo ""

# Show last 20 lines with "error:"
echo "=== Recent error lines (last 20) ==="
grep -i "error:" "$BUILD_LOG" 2>/dev/null | tail -20
echo ""

# Show last 10 fatal errors
echo "=== Recent fatal errors (last 10) ==="
grep -i "fatal" "$BUILD_LOG" 2>/dev/null | tail -10
echo ""

# Show FAILED sections
echo "=== FAILED sections (last 5) ==="
grep -B 2 "FAILED:" "$BUILD_LOG" 2>/dev/null | tail -20
