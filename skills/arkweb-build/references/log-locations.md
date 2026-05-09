# ArkWeb Build Log Locations

Guide to the main files used to verify and diagnose ArkWeb builds.

## Primary build log

Always check this file first:

```text
<arkweb-root>/src/out/<product>/build.log
```

Examples:

- `src/out/rk3568/build.log`
- `src/out/rk3568_64/build.log`
- `src/out/musl_64/build.log`
- `src/out/x86_64/build.log`

Quick commands:

```bash
tail -200 <arkweb-root>/src/out/<product>/build.log
grep -ni "error:" <arkweb-root>/src/out/<product>/build.log | tail -20
grep -niE "fatal error|undefined reference|multiple definition|ERROR at|cannot find|No such file|killed|OutOfMemory" <arkweb-root>/src/out/<product>/build.log | tail -20
```

## Rotated build logs

When a new build starts, the previous `build.log` may be renamed to a timestamped file in the same directory:

```text
src/out/<product>/build_YYYYMMDDHHMMSS.log
```

Use these when the current `build.log` was replaced and you still need the previous failure.

## Build arguments

The configured GN arguments live here:

```text
<arkweb-root>/src/out/<product>/args.gn
```

Use this file to confirm which product or build settings are active in the current output directory.

## LFS configuration and package lists

When ArkWeb fails because prebuilts were not fully downloaded, check these files first:

```text
<arkweb-root>/src/.gitattributes
<arkweb-root>/src/ohos_sdk/.gitattributes
<arkweb-root>/src/third_party/ohos_ndk/.gitattributes
<arkweb-root>/src/ohos_sdk/.install
```

How to use them:

- `src/.gitattributes`
  current root-level LFS tracking for release SDK zip packages, LLVM tarball, and `arkweb.profdata`
- `src/ohos_sdk/.gitattributes`
  SDK-local LFS tracking for `rust-toolchain.tar.gz`, `llvm.tar.gz`, and older split archives
- `src/third_party/ohos_ndk/.gitattributes`
  additional LFS-tracked NDK/LLVM binaries; useful as a secondary signal, but `src/ohos_sdk/.install` is usually the first file to trust for current required package names
- `src/ohos_sdk/.install`
  the current package names the install step actually consumes, such as `native-linux-x64-6.1.0.31-Release.zip`, `llvm-linux-x86_64_stripped.tar.gz`, and `rust-toolchain.tar.gz`

## Ninja state

Useful files under the same output directory:

```text
<arkweb-root>/src/out/<product>/.ninja_log
<arkweb-root>/src/out/<product>/obj/
<arkweb-root>/src/out/<product>/gen/
```

These help when the user is resuming an incremental build or when a generated file is missing.

## Resource snapshots

When diagnosing silent build exits in the Ninja phase, store and inspect snapshots here:

```text
<arkweb-root>/src/out/<product>/resource_snapshots/
```

These files are produced by:

```bash
bash <skill-dir>/scripts/capture_resource_snapshot.sh <product> <label> <arkweb-root>
```

Use them to correlate:

- estimated CPU idle ratio
- current load average
- `MemAvailable`
- `SwapFree`
- top CPU and memory consumers

## Typical output artifacts

Common artifacts for native builds are usually placed directly under:

```text
<arkweb-root>/src/out/<product>/
```

Examples:

- `libarkweb_engine.so`
- `libarkweb_render.so`
- `libffmpeg.so`
- `libadapter_ndk_stub.so`

Quick checks:

```bash
find <arkweb-root>/src/out/<product> -maxdepth 1 -type f \( -name "libarkweb*.so" -o -name "libadapter_ndk_stub.so" -o -name "libffmpeg.so" \) | sort
ls -lh <arkweb-root>/src/out/<product>/build.log
```

## Wrapper root vs git root

Build commands run at the wrapper root:

```text
<arkweb-root>/
```

Git status and diff usually belong to the real worktree:

```text
<arkweb-root>/src/
```
