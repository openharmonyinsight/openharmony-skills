#!/bin/bash
# Check if fast-rebuild can be used
# Verifies no GN files (BUILD.gn, *.gni) have pending or unregenerated changes

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Find OpenHarmony root dynamically via .gn file
# Search from PWD upward (not from script location — script may be outside the source tree)
find_oh_root() {
    local start_dir="$1"
    local dir="$start_dir"
    while [[ ! -f "$dir/.gn" ]]; do
        dir="$(dirname "$dir")"
        if [[ "$dir" == "/" ]]; then
            echo "Error: OpenHarmony root not found (no .gn file) from: $start_dir" >&2
            return 1
        fi
    done
    echo "$dir"
}

# Support --root <path> to explicitly specify OpenHarmony root
OH_ROOT=""
PRODUCT_NAME=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --root)
            OH_ROOT="$2"; shift 2 ;;
        --product)
            PRODUCT_NAME="$2"; shift 2 ;;
        *)
            break ;;
    esac
done

# Default: search upward from current working directory
if [[ -z "$OH_ROOT" ]]; then
    OH_ROOT="$(find_oh_root "$(pwd)")"
fi

# Default product name
PRODUCT_NAME="${PRODUCT_NAME:-rk3568}"

# Helper: recommend standard build
recommend_standard_build() {
    local reason="$1"
    echo -e "${YELLOW}Reason: $reason${NC}"
    echo ""
    echo -e "${YELLOW}Do NOT use --fast-rebuild${NC}"
    echo ""
    echo "Recommended: Use standard build command"
    echo "  ./build.sh --export-para PYCACHE_ENABLE:true --product-name $PRODUCT_NAME --ccache"
}

# Helper: recommend fast rebuild
recommend_fast_build() {
    echo -e "${GREEN}Safe to use --fast-rebuild${NC}"
    echo ""
    echo "Recommended fast rebuild command:"
    echo "  ./build.sh --export-para PYCACHE_ENABLE:true --product-name $PRODUCT_NAME --ccache --fast-rebuild"
    echo ""
    echo "Or for specific component:"
    echo "  ./build.sh --export-para PYCACHE_ENABLE:true --product-name $PRODUCT_NAME --build-target ace_engine --ccache --fast-rebuild"
}

echo -e "${GREEN}ACE Engine Fast Rebuild Checker${NC}"
echo "OpenHarmony Root: $OH_ROOT"
echo "Product: $PRODUCT_NAME"
echo ""

# Check if build output exists
if [[ "$PRODUCT_NAME" == "ohos-sdk" ]]; then
    BUILD_OUT="$OH_ROOT/out/sdk"
elif [[ "$PRODUCT_NAME" == "host_product" ]]; then
    BUILD_OUT="$OH_ROOT/out/host/host_product"
else
    BUILD_OUT="$OH_ROOT/out/$PRODUCT_NAME"
fi
if [ ! -d "$BUILD_OUT" ]; then
    echo -e "${RED}No build output found at $BUILD_OUT${NC}"
    echo "This appears to be a first-time build."
    echo "Recommended: Use standard build command"
    echo "  ./build.sh --export-para PYCACHE_ENABLE:true --product-name $PRODUCT_NAME --ccache"
    exit 0
fi

# --- Check 1: git working tree has uncommitted GN changes ---
echo -e "${YELLOW}[1/3] Checking git working tree for GN changes...${NC}"

GIT_GN_CHANGES=""
if git -C "$OH_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    GIT_GN_CHANGES=$(git -C "$OH_ROOT" status --porcelain -- '**/BUILD.gn' '*.gni' 2>/dev/null || true)
fi

if [ -n "$GIT_GN_CHANGES" ]; then
    echo -e "${RED}Found uncommitted GN file changes:${NC}"
    echo ""
    echo "$GIT_GN_CHANGES" | while IFS= read -r line; do
        echo "  - $line"
    done
    echo ""
    recommend_standard_build "GN files have uncommitted changes that may not have been regenerated into ninja"
    exit 0
fi
echo -e "${GREEN}  No uncommitted GN changes${NC}"

# --- Check 2: GN files newer than ninja build output ---
echo -e "${YELLOW}[2/3] Comparing GN vs ninja timestamps...${NC}"

# Exclude generated/output dirs — these GN files are build artifacts, not source inputs
FIND_EXCLUDE=(-path "$OH_ROOT/out" -prune -o -path "$OH_ROOT/out/*" -prune -o -path "*/node_modules/*" -prune -o -path "*/.git/*" -prune -o)

# Find the most recently modified ninja file in build output
NINJA_STAMP=""
NINJA_FILE=$(find "$BUILD_OUT" -maxdepth 2 -name "build.ninja" -type f 2>/dev/null | head -1 || true)
if [ -n "$NINJA_FILE" ] && [ -f "$NINJA_FILE" ]; then
    NINJA_STAMP=$(stat -c '%Y' "$NINJA_FILE" 2>/dev/null || stat -f '%m' "$NINJA_FILE" 2>/dev/null || true)
fi

if [ -n "$NINJA_STAMP" ]; then
    # Find source GN files modified AFTER the ninja file was generated (exclude out/, node_modules/)
    NEWER_GN_FILES=$(find "$OH_ROOT" "${FIND_EXCLUDE[@]}" -type f \( -name "BUILD.gn" -o -name "*.gni" \) -newer "$NINJA_FILE" -print 2>/dev/null | head -20 || true)
    if [ -n "$NEWER_GN_FILES" ]; then
        echo -e "${RED}Found source GN files newer than build.ninja (${NINJA_FILE#$OH_ROOT/}):${NC}"
        echo ""
        echo "$NEWER_GN_FILES" | while IFS= read -r file; do
            echo "  - ${file#$OH_ROOT/}"
        done
        echo ""
        recommend_standard_build "Source GN files modified after last ninja generation — need gn gen before fast rebuild"
        exit 0
    fi
    echo -e "${GREEN}  All source GN files older than build.ninja${NC}"
else
    echo -e "${YELLOW}  Could not determine ninja timestamp, skipping this check${NC}"
fi

# --- Check 3: recently modified GN files (time window) ---
TIME_WINDOW=${1:-30}
echo -e "${YELLOW}[3/3] Checking for GN files modified in last $TIME_WINDOW minutes...${NC}"

RECENT_GN_FILES=$(find "$OH_ROOT" "${FIND_EXCLUDE[@]}" -type f \( -name "BUILD.gn" -o -name "*.gni" \) -mmin -$TIME_WINDOW -print 2>/dev/null || true)

if [ -n "$RECENT_GN_FILES" ]; then
    echo -e "${RED}Found recently modified GN files:${NC}"
    echo ""
    echo "$RECENT_GN_FILES" | while IFS= read -r file; do
        echo "  - ${file#$OH_ROOT/}"
    done
    echo ""
    recommend_standard_build "GN files modified within the last $TIME_WINDOW minutes"
    exit 0
fi
echo -e "${GREEN}  No GN files modified in the last $TIME_WINDOW minutes${NC}"

# All checks passed
echo ""
echo -e "${GREEN}All checks passed.${NC}"
echo ""
recommend_fast_build

echo ""
echo "Usage: $0 [--root <path>] [--product <name>] [minutes]"
echo "  --root      OpenHarmony root directory (auto-detected from PWD)"
echo "  --product   Product name (default: rk3568)"
echo "  minutes     Time window for recent modification check (default: 30)"
