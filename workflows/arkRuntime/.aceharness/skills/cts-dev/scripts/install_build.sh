#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"
init_common
detect_build_dir_name "$STATIC_CORE"

cd "$STATIC_CORE/tools"
ln -sf ../../../ets_frontend/ets2panda es2panda
cd ..
./scripts/install-third-party --force-clone
cmake -B "$BUILD_DIR_NAME" -DCMAKE_CXX_FLAGS="-DES2PANDA_STRICT" -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain/host_clang_default.cmake -GNinja .
cmake --build "$BUILD_DIR_NAME"
