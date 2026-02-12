#!/bin/bash
# Find recent build errors in OpenHarmony build logs
# Useful for quick error checking during active development

set -e

# OpenHarmony root directory
# Script is at: .../ace_engine/.claude/skills/openharmony-build/scripts/
# Need to go up 7 levels to reach OpenHarmony root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OH_ROOT="$(cd "$SCRIPT_DIR/../../../../../../.." && pwd)"

# Default product if none specified
PRODUCT="${1:-rk3568}"
BUILD_LOG="$OH_ROOT/out/$PRODUCT/build.log"

if [ ! -f "$BUILD_LOG" ]; then
    echo "Build log not found: $BUILD_LOG"
    echo ""
    echo "Usage: $0 [product-name]"
    echo "Example: $0 rk3568"
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
