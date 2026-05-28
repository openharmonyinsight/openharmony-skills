#!/bin/bash
# Helper script to determine if fast-rebuild can be used.
# It is intentionally conservative: --fast-rebuild is only recommended when
# existing output is present and build configuration files show no changes.

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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

CONFIG_PATHS=(
    ':(glob)**/BUILD.gn'
    ':(glob)**/*.gni'
    ':(glob)**/bundle.json'
    ':(glob)**/ohos.build'
    ':(glob)**/build-profile.json5'
    ':(glob)productdefine/**'
    ':(glob)vendor/**'
    ':(glob)build/ohos/**'
    ':(glob)build/subsystem_config.json'
)

list_repo_paths() {
    local root="$1"

    if command -v repo >/dev/null 2>&1 && [[ -d "$root/.repo" ]]; then
        (
            cd "$root"
            repo list -p 2>/dev/null || true
        )
        return
    fi

    if git -C "$root" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        echo "."
    fi
}

collect_config_changes() {
    local root="$1"
    local path repo_dir status
    local seen=" "

    while IFS= read -r path; do
        [[ -n "$path" ]] || continue
        [[ "$seen" == *" $path "* ]] && continue
        seen+="$path "
        repo_dir="$root/$path"
        [[ -d "$repo_dir" ]] || continue

        status=$(git -C "$repo_dir" status --porcelain --untracked-files=all -- "${CONFIG_PATHS[@]}" 2>/dev/null || true)
        if [[ -n "$status" ]]; then
            while IFS= read -r line; do
                [[ -n "$line" ]] || continue
                printf '%s/%s\n' "$path" "$line"
            done <<< "$status"
        fi
    done < <(list_repo_paths "$root")
}

# Default time window in minutes (used as an extra mtime signal only)
TIME_WINDOW=${1:-30}
ROOT_HINT="${2:-$PWD}"
if ! OH_ROOT="$(find_root "$ROOT_HINT")"; then
    echo -e "${RED}Error: OpenHarmony root not found from: $ROOT_HINT${NC}"
    exit 1
fi

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

# Check tracked and untracked build configuration changes first. This is the
# actual gate for --fast-rebuild; mtime checks below are only a fallback signal.
echo -e "${YELLOW}Checking git status for build configuration changes...${NC}"

CONFIG_CHANGES=$(collect_config_changes "$OH_ROOT")

if [[ -n "$CONFIG_CHANGES" ]]; then
    echo -e "${RED}✗ Build configuration changes detected:${NC}"
    echo ""
    echo "$CONFIG_CHANGES" | while IFS= read -r file; do
        echo "  - $file"
    done
    echo ""
    echo "Recommended: Use standard build command (do NOT use --fast-rebuild)"
    echo "  cd $OH_ROOT"
    echo "  ./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache"
    exit 0
fi

if [[ -z "$(list_repo_paths "$OH_ROOT")" ]]; then
    echo -e "${RED}✗ Could not inspect git workspace configuration changes${NC}"
    echo "Recommended: Use standard build command (do NOT use --fast-rebuild)"
    exit 0
fi

echo -e "${GREEN}✓ No build configuration changes found in git status${NC}"
echo ""

# Find recently modified GN files as an additional conservative signal.
echo -e "${YELLOW}Checking for recently modified GN files...${NC}"

RECENT_GN_FILES=$(find "$OH_ROOT" -type f \( -name "BUILD.gn" -o -name "*.gni" \) -mmin -$TIME_WINDOW 2>/dev/null || true)

if [ -z "$RECENT_GN_FILES" ]; then
    echo -e "${GREEN}✓ No GN files modified in the last $TIME_WINDOW minutes${NC}"
    echo ""
    echo -e "${GREEN}✓ Eligible to use --fast-rebuild${NC}"
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
echo "  $0 <minutes> [openharmony-root]"
echo ""
echo "Example: Check last 60 minutes"
echo "  $0 60 /path/to/OpenHarmony"
