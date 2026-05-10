# ArkWeb Build Commands Reference

Reference commands for building ArkWeb with `build_arkweb.sh`.

## Build entry

Main entry point:

```bash
./build_arkweb.sh [product] -t <target> [options]
```

Run this command from the ArkWeb wrapper root, not from `src/`.

## Products

Common product values:

| Product | CPU | Output directory |
| --- | --- | --- |
| `rk3568` | arm | `src/out/rk3568/` |
| `rk3568_64` | arm64 | `src/out/rk3568_64/` |
| `musl_64` | arm64 musl | `src/out/musl_64/` |
| `x86_64` | x64 | `src/out/x86_64/` |

Default product in most local trees:

```bash
rk3568_64
```

## Targets

Common `-t` values:

| Target | Meaning |
| --- | --- |
| `n` | native targets, the most common default |
| `b` | BrowserShell |
| `w` | NWeb WebView |
| `m` | NWebEx napi module |
| `M` | NWebEx npm package |
| `p` | HMP plus NWeb WebView |

Less common test-oriented target aliases that exist in the build script:

| Target | Meaning |
| --- | --- |
| `coreut` | core unit tests |
| `allut` | broader unit-test target set |
| `smokeut` | smoke unit tests |

## Common options

| Option | Meaning |
| --- | --- |
| `-A` or `-artifact` | use prebuilt NDK style artifact mode |
| `-j N` | override Ninja parallelism |
| `-r` | release build |
| `-asan` | enable AddressSanitizer |
| `-hwasan` | enable HWASan |
| `-fuzzer` | build fuzzer targets and enable ASan |
| `-G <gn_args>` | append extra GN args |

## Pre-build check

Before compiling, first check whether the current output directory already has a `build.log`:

```bash
if [[ -f <arkweb-root>/src/out/rk3568_64/build.log ]]; then
  echo "This tree has been built before for rk3568_64"
else
  echo "Likely first build for rk3568_64"
fi
```

If `build.log` is missing, the first build can easily take about 2 to 3 hours.

## Default commands

Standard default WebView build:

```bash
cd <arkweb-root>
./build_arkweb.sh rk3568_64 -t w -A
```

Standard native incremental build:

```bash
cd <arkweb-root>
./build_arkweb.sh rk3568_64 -t n -A
```

BrowserShell build:

```bash
cd <arkweb-root>
./build_arkweb.sh rk3568_64 -t b -A
```

WebView build:

```bash
cd <arkweb-root>
./build_arkweb.sh rk3568_64 -t w -A
```

Release native build:

```bash
cd <arkweb-root>
./build_arkweb.sh rk3568_64 -t n -A -r
```

ASan build:

```bash
cd <arkweb-root>
./build_arkweb.sh rk3568_64 -t n -A -asan
```

## Direct Ninja continuation

Use direct Ninja only when the output directory is already configured and the user is continuing the same incremental build.

For a Ninja compile or link failure, after applying a fix, first `cd <arkweb-root>/src/out/<product>` and rerun the exact compiler or linker command printed after the first `FAILED:` line in `build.log` when it is available. Treat that only as a fast local check. After it succeeds, record a fresh resource snapshot, then switch directories before broader verification: `cd <arkweb-root>` for the full `build_arkweb.sh` command, or `cd <arkweb-root>/src` only for the same direct Ninja target set below.

Do not use the single failed command path for GN generation, SDK/LFS setup, or Ninja target graph errors.

Examples:

```bash
cd <arkweb-root>/src
third_party/depot_tools/ninja -C out/rk3568_64 ohos_nweb_hap
```

```bash
cd <arkweb-root>/src
third_party/depot_tools/ninja -C out/rk3568_64 adapter_ndk_stub libarkweb_engine libarkweb_render arkweb_crashpad_handler libffmpeg
```

For a default WebView build, the direct Ninja continuation target is usually:

```text
ohos_nweb_hap
```

For the default native target set, the build script usually drives these targets:

```text
adapter_ndk_stub libarkweb_engine libarkweb_render arkweb_crashpad_handler libffmpeg
```

Do not replace the normal `build_arkweb.sh` flow with direct Ninja unless there is a clear reason, such as resuming a failed incremental build after `args.gn` already exists. Always continue with the same target set that the previous `build_arkweb.sh` invocation was building.
