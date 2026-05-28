#!/bin/bash
# Build OpenHarmony test targets listed in unittest_targets.txt.

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
    echo "Usage: $0 [product-name] [openharmony-root] [target-list-file]"
    echo "Example: $0 rk3568 /path/to/OpenHarmony"
    echo "Example: $0 rk3568 /path/to/OpenHarmony foundation/arkui/ace_engine/unittest_targets.txt"
}

PRODUCT="${1:-rk3568}"
ROOT_HINT="${2:-$PWD}"
LIST_HINT="${3:-}"

if ! OH_ROOT="$(find_root "$ROOT_HINT")"; then
    echo "OpenHarmony root not found from: $ROOT_HINT" >&2
    exit 1
fi

if [[ -n "$LIST_HINT" ]]; then
    if [[ "$LIST_HINT" = /* ]]; then
        TARGET_LIST="$LIST_HINT"
    else
        TARGET_LIST="$OH_ROOT/$LIST_HINT"
    fi
elif [[ -f "$OH_ROOT/foundation/arkui/ace_engine/unittest_targets.txt" ]]; then
    TARGET_LIST="$OH_ROOT/foundation/arkui/ace_engine/unittest_targets.txt"
elif [[ -f "$OH_ROOT/unittest_targets.txt" ]]; then
    TARGET_LIST="$OH_ROOT/unittest_targets.txt"
else
    echo "unittest_targets.txt not found." >&2
    echo "Checked:" >&2
    echo "  $OH_ROOT/foundation/arkui/ace_engine/unittest_targets.txt" >&2
    echo "  $OH_ROOT/unittest_targets.txt" >&2
    exit 1
fi

if [[ ! -f "$TARGET_LIST" ]]; then
    echo "Target list not found: $TARGET_LIST" >&2
    exit 1
fi

echo "OpenHarmony root: $OH_ROOT"
echo "Product: $PRODUCT"
echo "Target list: $TARGET_LIST"

cd "$OH_ROOT"

build_count=0
while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    target="${raw_line%%#*}"
    target="${target#"${target%%[![:space:]]*}"}"
    target="${target%"${target##*[![:space:]]}"}"
    [[ -z "$target" ]] && continue

    build_count=$((build_count + 1))
    echo ""
    echo "[$build_count] Building target: $target"
    ./build.sh --export-para PYCACHE_ENABLE:true --product-name "$PRODUCT" --build-target="$target" --ccache
done < "$TARGET_LIST"

if [[ "$build_count" -eq 0 ]]; then
    echo "No build targets found in: $TARGET_LIST" >&2
    exit 1
fi

echo ""
echo "Built $build_count target(s) successfully."
