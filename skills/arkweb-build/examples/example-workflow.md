# ArkWeb Build Examples

## Example 1: Default WebView build with first-build check

```bash
find_arkweb_root() {
  local dir="${1:-$PWD}"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/build_arkweb.sh" && -f "$dir/src/arkweb/build/build.sh" ]]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}

ARKWEB_ROOT="$(find_arkweb_root)"
if [[ -f "$ARKWEB_ROOT/src/out/rk3568_64/build.log" ]]; then
  echo "Incremental build path"
else
  echo "First build path: expect about 2 to 3 hours"
fi

cd "$ARKWEB_ROOT"
./build_arkweb.sh rk3568_64 -t w -A
```

## Example 2: Standard native build

```bash
ARKWEB_ROOT="$(find_arkweb_root)"
cd "$ARKWEB_ROOT"
bash <skill-dir>/scripts/capture_resource_snapshot.sh rk3568_64 before-build-ninja "$ARKWEB_ROOT"
./build_arkweb.sh rk3568_64 -t n -A
```

## Example 3: Continue the same incremental build with Ninja

Use this only after the output directory already exists and the build is clearly continuing the same configuration.

```bash
ARKWEB_ROOT="$(find_arkweb_root)"
cd "$ARKWEB_ROOT/src"
bash <skill-dir>/scripts/capture_resource_snapshot.sh rk3568_64 before-direct-ninja "$ARKWEB_ROOT"
third_party/depot_tools/ninja -C out/rk3568_64 ohos_nweb_hap
```

Or for the default native target set:

```bash
ARKWEB_ROOT="$(find_arkweb_root)"
cd "$ARKWEB_ROOT/src"
bash <skill-dir>/scripts/capture_resource_snapshot.sh rk3568_64 before-direct-ninja "$ARKWEB_ROOT"
third_party/depot_tools/ninja -C out/rk3568_64 adapter_ndk_stub libarkweb_engine libarkweb_render arkweb_crashpad_handler libffmpeg
```

## Example 4: Diagnose a failed build

```bash
ARKWEB_ROOT="$(find_arkweb_root)"
bash <skill-dir>/scripts/show_relevant_changes.sh "$ARKWEB_ROOT"
tail -200 "$ARKWEB_ROOT/src/out/rk3568_64/build.log"
bash <skill-dir>/scripts/analyze_build_error.sh rk3568_64 "$ARKWEB_ROOT"
```

## Example 5: Check whether Git LFS prebuilts are missing

```bash
ARKWEB_ROOT="$(find_arkweb_root)"
bash <skill-dir>/scripts/check_lfs_artifacts.sh "$ARKWEB_ROOT"
```

## Example 6: Resource snapshot before Ninja and lower parallelism after a silent stop

```bash
ARKWEB_ROOT="$(find_arkweb_root)"
bash <skill-dir>/scripts/capture_resource_snapshot.sh rk3568_64 before-ninja "$ARKWEB_ROOT"

cd "$ARKWEB_ROOT"
./build_arkweb.sh rk3568_64 -t w -A -j 32
```

If the machine still stops silently in the Ninja phase, try:

```bash
cd "$ARKWEB_ROOT"
./build_arkweb.sh rk3568_64 -t w -A -j 16
```
