#!/usr/bin/env bash
# Common functions for CTS development scripts
# All other scripts source this file for root detection and build dir detection.

detect_root_dir() {
    if [[ -n "${ARK_ROOT_DIR:-}" ]]; then
        ROOT_DIR="$ARK_ROOT_DIR"
        return 0
    fi

    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[1]:-$0}")" && pwd)"

    local search_start
    search_start="$(pwd)"

    local dir="$search_start"
    while [[ "$dir" != "/" ]]; do
        if [[ -d "$dir/runtime_core" && -d "$dir/ets_frontend" ]]; then
            ROOT_DIR="$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done

    dir="$script_dir"
    while [[ "$dir" != "/" ]]; do
        if [[ -d "$dir/runtime_core" && -d "$dir/ets_frontend" ]]; then
            ROOT_DIR="$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done

    echo "ERROR: Cannot find project root (directory containing both runtime_core/ and ets_frontend/)." >&2
    echo "Please either:" >&2
    echo "  1. Set ARK_ROOT_DIR environment variable to the project root path" >&2
    echo "  2. Run the script from within the project tree" >&2
    echo "  3. cd to the project root before running" >&2
    exit 1
}

_prompt_build_dir() {
    local static_core="$1"
    echo "" >&2
    echo "WARNING: Cannot auto-detect build directory under: $static_core" >&2
    echo "  Searched: build_release/bin, out/bin — neither found." >&2
    echo "" >&2
    echo "Available directories under $static_core:" >&2
    local found=0
    for d in "$static_core"/*/; do
        if [[ -d "$d" ]]; then
            echo "  $(basename "$d")/" >&2
            found=1
        fi
    done
    if [[ "$found" -eq 0 ]]; then
        echo "  (none)" >&2
    fi
    echo "" >&2
    echo "Please specify the build directory name (e.g. out, build_release, cmake-build-debug):" >&2
    read -r BUILD_DIR_NAME
    if [[ -z "$BUILD_DIR_NAME" ]]; then
        echo "ERROR: No build directory specified. Aborting." >&2
        exit 1
    fi
    if [[ ! -d "$static_core/$BUILD_DIR_NAME" ]]; then
        echo "ERROR: Directory $static_core/$BUILD_DIR_NAME does not exist. Aborting." >&2
        exit 1
    fi
    echo "Using build directory: $static_core/$BUILD_DIR_NAME" >&2
}

detect_build_dir() {
    local static_core="$1"
    if [[ -n "${ARK_BUILD_DIR:-}" ]]; then
        BUILD_DIR="${ARK_BUILD_DIR}"
        BUILD_DIR_NAME="$(basename "$BUILD_DIR")"
    elif [[ -d "$static_core/build_release/bin" ]]; then
        BUILD_DIR="$static_core/build_release"
        BUILD_DIR_NAME="build_release"
    elif [[ -d "$static_core/out/bin" ]]; then
        BUILD_DIR="$static_core/out"
        BUILD_DIR_NAME="out"
    else
        _prompt_build_dir "$static_core"
        BUILD_DIR="$static_core/$BUILD_DIR_NAME"
    fi
}

detect_build_dir_name() {
    local static_core="$1"
    detect_build_dir "$static_core"
}

init_common() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[1]:-$0}")" && pwd)"
    detect_root_dir
    STATIC_CORE="$ROOT_DIR/runtime_core/static_core"
}
