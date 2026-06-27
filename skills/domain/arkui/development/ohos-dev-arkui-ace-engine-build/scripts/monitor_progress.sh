#!/bin/bash
# Monitor an ongoing ace_engine build by tailing build_console.log for ninja progress.
# Usage: monitor_progress.sh [--interval <seconds>] [--root <path>] [--product <name>]
#
# Exit conditions:
#   - build_console.log contains "build  successful" or "build success" → success (exit 0)
#   - build_console.log contains "FAILED:" or "build failed" and log stops growing → failure (exit 1)
#   - Ctrl+C → manual stop
#
# Phases tracked:
#   1. Pre-build: ohpm init, GN generation, prebuild_and_preload
#   2. Ninja: [OHOS INFO] [NINJA] [current/total] with progress bar
#   3. Post-build: [OHOS INFO] [POSTBUILD] ccache summary, deps_guard checks

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

INTERVAL=1
OH_ROOT=""
PRODUCT_NAME="rk3568"
CHECK_ONLY=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --interval) INTERVAL="$2"; shift 2 ;;
        --root)     OH_ROOT="$2";  shift 2 ;;
        --product)  PRODUCT_NAME="$2"; shift 2 ;;
        --check)    CHECK_ONLY=true; shift ;;
        *)          echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

if [[ -z "$OH_ROOT" ]]; then
    dir="$(pwd)"
    while [[ ! -f "$dir/.gn" ]]; do
        dir="$(dirname "$dir")"
        if [[ "$dir" == "/" ]]; then
            echo -e "${RED}Error: OpenHarmony root not found (no .gn file)${NC}" >&2
            exit 1
        fi
    done
    OH_ROOT="$dir"
fi

if [[ "$PRODUCT_NAME" == "ohos-sdk" ]]; then
    BUILD_LOG="$OH_ROOT/out/sdk/build_console.log"
elif [[ "$PRODUCT_NAME" == "host_product" ]]; then
    BUILD_LOG="$OH_ROOT/out/host/host_product/build_console.log"
else
    BUILD_LOG="$OH_ROOT/out/$PRODUCT_NAME/build_console.log"
fi

# --check mode: test whether a build is active, then exit
#   exit 0 = build active (log exists, growing, no completion marker, PID alive)
#   exit 1 = no active build (log missing, stale, already finished, or PID dead)
if [[ "$CHECK_ONLY" == true ]]; then
    if [[ ! -f "$BUILD_LOG" ]]; then
        echo "no_log"
        exit 1
    fi

    # Extract PID from first line (BUILD_PID=<pid>)
    BUILD_PID=$(head -1 "$BUILD_LOG" 2>/dev/null | grep -oP '^BUILD_PID=\K\d+' || echo "")

    # If PID exists, verify process is alive
    if [[ -n "$BUILD_PID" ]]; then
        if ! kill -0 "$BUILD_PID" 2>/dev/null; then
            echo "killed"
            exit 1
        fi
    fi

    if grep -q 'build  successful\|build success' "$BUILD_LOG" 2>/dev/null; then
        echo "completed"
        exit 1
    fi
    if grep -q 'FAILED:\|build failed' "$BUILD_LOG" 2>/dev/null; then
        echo "failed"
        exit 1
    fi
    # If PID is alive, build is active (even if log temporarily not growing)
    if [[ -n "$BUILD_PID" ]] && kill -0 "$BUILD_PID" 2>/dev/null; then
        echo "active"
        exit 0
    fi

    # No PID recorded — fallback to log growth detection
    S1=$(stat -c '%s' "$BUILD_LOG" 2>/dev/null || stat -f '%z' "$BUILD_LOG" 2>/dev/null || echo 0)
    sleep 2
    S2=$(stat -c '%s' "$BUILD_LOG" 2>/dev/null || stat -f '%z' "$BUILD_LOG" 2>/dev/null || echo 0)
    if [[ "$S1" != "$S2" ]]; then
        echo "active"
        exit 0
    else
        echo "stale"
        exit 1
    fi
fi

echo -e "${CYAN}=== Build Progress Monitor ===${NC}"
echo "Log:      $BUILD_LOG"
echo "Interval: ${INTERVAL}s"
echo "Press Ctrl+C to stop monitoring."
echo ""

if [[ ! -f "$BUILD_LOG" ]]; then
    echo -e "${YELLOW}Waiting for build_console.log to appear...${NC}"
    while [[ ! -f "$BUILD_LOG" ]]; do
        sleep 2
    done
fi

# Extract PID from first line (BUILD_PID=<pid>)
BUILD_PID=$(head -1 "$BUILD_LOG" 2>/dev/null | grep -oP '^BUILD_PID=\K\d+' || echo "")
if [[ -n "$BUILD_PID" ]]; then
    echo -e "${CYAN}Build PID: ${BUILD_PID}${NC}"
fi

LAST_LINE=""
START_TIME=$SECONDS

print_progress() {
    local ELAPSED=$(( SECONDS - START_TIME ))
    local MINS=$(( ELAPSED / 60 ))
    local SECS=$(( ELAPSED % 60 ))
    local TIME_TAG="${CYAN}[+${MINS}m${SECS}s]${NC}"

    # Ninja progress: [OHOS INFO] [NINJA] [current/total] ...
    local NINJA_LINE=$(grep -oP '\[NINJA\] \[\d+/\d+\]' "$BUILD_LOG" 2>/dev/null | tail -1 || true)
    local OUTPUT=""

    if [[ -n "$NINJA_LINE" ]]; then
        local CURRENT=$(echo "$NINJA_LINE" | grep -oP '(?<=\[)\d+(?=/)' || true)
        local TOTAL=$(echo "$NINJA_LINE" | grep -oP '(?<=/)\d+(?=\])' || true)
        if [[ -n "$TOTAL" && "$TOTAL" -gt 0 ]]; then
            local PCT=$(( CURRENT * 100 / TOTAL ))
            local BAR_LEN=30
            local FILLED=$(( PCT * BAR_LEN / 100 ))
            local EMPTY=$(( BAR_LEN - FILLED ))
            local BAR=$(printf '%0.s#' $(seq 1 $FILLED 2>/dev/null) 2>/dev/null || true)
            local SPACE=$(printf '%0.s-' $(seq 1 $EMPTY 2>/dev/null) 2>/dev/null || true)
            OUTPUT="${TIME_TAG} [NINJA] [${CURRENT}/${TOTAL}] ${GREEN}[${BAR}${SPACE}]${NC} ${PCT}%"
        else
            OUTPUT="${TIME_TAG} ${NINJA_LINE}"
        fi
        LAST_LINE="[${CURRENT}/${TOTAL}]"
    else
        # Check for post-build or pre-build phases
        local POSTBUILD=$(grep -c '\[POSTBUILD\]' "$BUILD_LOG" 2>/dev/null || true)
        if [[ "$POSTBUILD" -gt 0 ]]; then
            local PB_LINE=$(grep '\[POSTBUILD\]' "$BUILD_LOG" 2>/dev/null | tail -1 | sed 's/.*\[POSTBUILD\] //' | head -c 60 || true)
            OUTPUT="${TIME_TAG} ${YELLOW}[POSTBUILD]${NC} ${PB_LINE}"
        else
            # Pre-ninja: GN, prebuild, ohpm, etc.
            local PHASE=$(tail -5 "$BUILD_LOG" 2>/dev/null | grep -oP '\[OHOS INFO\].*' | tail -1 || true)
            PHASE=$(echo "$PHASE" | sed 's/\x1b\[[0-9;]*m//g' | head -c 80)
            if [[ -n "$PHASE" ]]; then
                OUTPUT="${TIME_TAG} ${YELLOW}${PHASE}${NC}"
            else
                OUTPUT="${TIME_TAG} ${YELLOW}Build initializing...${NC}"
            fi
        fi
    fi

    printf "\r\033[K"
    printf '%b' "${OUTPUT}"
}

check_done() {
    # Check if build process is still alive (if PID was recorded)
    if [[ -n "$BUILD_PID" ]]; then
        if ! kill -0 "$BUILD_PID" 2>/dev/null; then
            # Process is dead — check if build completed successfully or crashed
            if grep -q 'build  successful\|build success' "$BUILD_LOG" 2>/dev/null; then
                local COST=$(grep -oP 'Cost Time:\s*\K\S+' "$BUILD_LOG" 2>/dev/null || true)
                printf "\r\033[K"
                if [[ -n "$COST" ]]; then
                    echo -e "${GREEN}=====build successful=====${NC} (${LAST_LINE}, cost ${COST})"
                else
                    echo -e "${GREEN}=====build successful=====${NC} (${LAST_LINE})"
                fi
                exit 0
            else
                printf "\r\033[K"
                echo -e "${RED}=====build process killed=====${NC} (PID $BUILD_PID no longer exists)"
                echo ""
                grep -iE '(error:|FAILED:)' "$BUILD_LOG" 2>/dev/null | tail -20 || true
                exit 1
            fi
        fi
    fi

    # Success: log contains "build  successful" or "<product> build success"
    if grep -q 'build  successful\|build success' "$BUILD_LOG" 2>/dev/null; then
        local COST=$(grep -oP 'Cost Time:\s*\K\S+' "$BUILD_LOG" 2>/dev/null || true)
        printf "\r\033[K"
        if [[ -n "$COST" ]]; then
            echo -e "${GREEN}=====build successful=====${NC} (${LAST_LINE}, cost ${COST})"
        else
            echo -e "${GREEN}=====build successful=====${NC} (${LAST_LINE})"
        fi
        exit 0
    fi
    # Failure: log contains "FAILED:" or "build failed" and log stopped growing
    if grep -q 'FAILED:\|build failed' "$BUILD_LOG" 2>/dev/null; then
        local S1=$(stat -c '%s' "$BUILD_LOG" 2>/dev/null || stat -f '%z' "$BUILD_LOG" 2>/dev/null || echo 0)
        sleep 3
        local S2=$(stat -c '%s' "$BUILD_LOG" 2>/dev/null || stat -f '%z' "$BUILD_LOG" 2>/dev/null || echo 0)
        if [[ "$S1" == "$S2" ]]; then
            printf "\r\033[K"
            echo -e "${RED}=====build failed=====${NC}"
            echo ""
            grep -iE '(error:|FAILED:)' "$BUILD_LOG" 2>/dev/null | tail -20 || true
            exit 1
        fi
    fi
}

print_progress
check_done

while true; do
    sleep "$INTERVAL"
    print_progress
    check_done
done
