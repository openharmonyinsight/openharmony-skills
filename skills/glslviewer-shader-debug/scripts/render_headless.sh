#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  render_headless.sh [--output DIR] [--size WIDTHxHEIGHT] shader1.frag [shader2.frag ...]

Environment:
  GLSLVIEWER_BIN   Optional explicit glslViewer binary path

Example:
  render_headless.sh --output /tmp/shader-out --size 512x512 ./preview.frag
EOF
}

OUT_DIR=""
SIZE="256x256"
declare -a SHADERS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --output)
            OUT_DIR="$2"
            shift 2
            ;;
        --size)
            SIZE="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        -*)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
        *)
            SHADERS+=("$1")
            shift
            ;;
    esac
done

if [[ ${#SHADERS[@]} -eq 0 ]]; then
    usage >&2
    exit 1
fi

if [[ -z "${GLSLVIEWER_BIN:-}" ]]; then
    GLSLVIEWER_BIN="$(command -v glslViewer || command -v glslviewer || true)"
fi

if [[ -z "${GLSLVIEWER_BIN:-}" ]]; then
    echo "glslViewer binary not found. Set GLSLVIEWER_BIN=/full/path/to/glslViewer and rerun." >&2
    exit 1
fi

if [[ ! -x "$GLSLVIEWER_BIN" ]]; then
    echo "glslViewer binary is not executable: $GLSLVIEWER_BIN" >&2
    exit 1
fi

if [[ ! "$SIZE" =~ ^[0-9]+x[0-9]+$ ]]; then
    echo "Invalid size '$SIZE'. Expected WIDTHxHEIGHT." >&2
    exit 1
fi

WIDTH="${SIZE%x*}"
HEIGHT="${SIZE#*x}"

if [[ -z "$OUT_DIR" ]]; then
    OUT_DIR="$(pwd)/glslviewer-out"
fi

mkdir -p "$OUT_DIR"

render_one() {
    local shader_path="$1"
    local shader_abs
    shader_abs="$(realpath "$shader_path")"
    local shader_name
    shader_name="$(basename "$shader_path")"
    local stem="${shader_name%.*}"
    local frame_dir="$OUT_DIR/$stem.frames"

    rm -rf "$frame_dir"
    mkdir -p "$frame_dir"

    (
        cd "$frame_dir"
        "$GLSLVIEWER_BIN" "$shader_abs" -w "$WIDTH" -h "$HEIGHT" --headless -E sequence,0,0,1
    )

    local first_frame
    first_frame="$(find "$frame_dir" -maxdepth 1 -type f -name '*.png' | sort | head -n 1)"
    if [[ -z "$first_frame" ]]; then
        echo "No PNG produced for $shader_path" >&2
        exit 1
    fi

    cp "$first_frame" "$OUT_DIR/$stem.png"
    echo "Rendered $shader_path -> $OUT_DIR/$stem.png"
}

for shader in "${SHADERS[@]}"; do
    if [[ ! -f "$shader" ]]; then
        echo "Shader not found: $shader" >&2
        exit 1
    fi
    render_one "$shader"
done
