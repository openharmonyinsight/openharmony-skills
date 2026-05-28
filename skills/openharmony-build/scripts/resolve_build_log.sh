#!/bin/bash
# Print the primary OpenHarmony build log path for a product.

set -euo pipefail

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

usage() {
    echo "Usage: $0 <product-name> [openharmony-root]" >&2
    echo "Examples:" >&2
    echo "  $0 rk3568 /path/to/OpenHarmony" >&2
    echo "  $0 ohos-sdk /path/to/OpenHarmony" >&2
    echo "  $0 host_product /path/to/OpenHarmony" >&2
    echo "  $0 standard /path/to/OpenHarmony" >&2
}

if [[ $# -lt 1 ]]; then
    usage
    exit 1
fi

PRODUCT="$1"
ROOT_HINT="${2:-$PWD}"

if ! OH_ROOT="$(find_root "$ROOT_HINT")"; then
    echo "OpenHarmony root not found from: $ROOT_HINT" >&2
    exit 1
fi

case "$PRODUCT" in
    host_product)
        echo "$OH_ROOT/out/host/host_product/build.log"
        ;;
    ohos-sdk|sdk)
        echo "$OH_ROOT/out/sdk/build.log"
        ;;
    standard|independent|component|component-independent)
        echo "$OH_ROOT/out/standard/build.log"
        ;;
    *)
        echo "$OH_ROOT/out/$PRODUCT/build.log"
        ;;
esac
