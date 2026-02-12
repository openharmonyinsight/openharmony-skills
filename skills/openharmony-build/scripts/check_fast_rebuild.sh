#!/bin/bash
# Helper script to determine if fast-rebuild can be used
# Checks if any GN files (BUILD.gn, *.gni) have been modified recently

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Find OpenHarmony root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OH_ROOT="$(cd "$SCRIPT_DIR/../../../../../../.." && pwd)"

# Default time window in minutes (check for changes in last N minutes)
TIME_WINDOW=${1:-30}

echo -e "${GREEN}OpenHarmony Fast Rebuild Checker${NC}"
echo "OpenHarmony Root: $OH_ROOT"
echo "Time window: last $TIME_WINDOW minutes"
echo ""

# Check if build output exists
if [ ! -d "$OH_ROOT/out" ]; then
    echo -e "${RED}✗ No build output found${NC}"
    echo "This appears to be a first-time build."
    echo "Recommended: Use standard build command"
    echo "  ./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache"
    exit 0
fi

# Find recently modified GN files
echo -e "${YELLOW}Checking for recently modified GN files...${NC}"

RECENT_GN_FILES=$(find "$OH_ROOT" -type f \( -name "BUILD.gn" -o -name "*.gni" \) -mmin -$TIME_WINDOW 2>/dev/null || true)

if [ -z "$RECENT_GN_FILES" ]; then
    echo -e "${GREEN}✓ No GN files modified in the last $TIME_WINDOW minutes${NC}"
    echo ""
    echo -e "${GREEN}✓ Safe to use --fast-rebuild${NC}"
    echo ""
    echo "Recommended fast rebuild command:"
    echo "  cd $OH_ROOT"
    echo "  ./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache --fast-rebuild"
    echo ""
    echo "Or for specific component:"
    echo "  ./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache --fast-rebuild"
else
    echo -e "${RED}✗ Found recently modified GN files:${NC}"
    echo ""
    echo "$RECENT_GN_FILES" | while IFS= read -r file; do
        echo "  - ${file#$OH_ROOT/}"
    done
    echo ""
    echo -e "${YELLOW}⚠ GN files have been modified${NC}"
    echo ""
    echo "Recommended: Use standard build command (do NOT use --fast-rebuild)"
    echo "  cd $OH_ROOT"
    echo "  ./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache"
fi

echo ""
echo "To check a different time window:"
echo "  $0 <minutes>"
echo ""
echo "Example: Check last 60 minutes"
echo "  $0 60"
