# Common ArkWeb Build Errors

Reference for recurring ArkWeb build failures and how to investigate them.

## Compilation errors

### Header file not found

Typical log fragments:

```text
fatal error: 'foo/bar.h' file not found
```

Checks:

- confirm the header exists where the code expects it
- inspect the target's `BUILD.gn` for the required dependency or include path
- verify the failure is in the current patch scope before changing unrelated targets
- because this is a Ninja compile failure, after fixing it, `cd <arkweb-root>/src/out/<product>` and rerun the failed compiler command shown after the first `FAILED:` line before rerunning the full build

## Linker errors

### Undefined reference

Typical log fragments:

```text
undefined reference to 'symbol_name'
```

Common causes:

- missing dependency in `BUILD.gn`
- source file not included in the producing target
- signature or namespace mismatch
- generated file not produced because an earlier step failed

Useful checks:

```bash
grep -R "symbol_name" --include="*.h" --include="*.cc" --include="*.cpp" <arkweb-root>/src
grep -n "undefined reference" <arkweb-root>/src/out/<product>/build.log
```

Because this is a Ninja link failure, after fixing it, `cd <arkweb-root>/src/out/<product>` and rerun the failed linker command shown after the first `FAILED:` line before rerunning the full build.

## GN configuration errors

### Missing target or bad dependency

Typical log fragments:

```text
ERROR at //path/to/BUILD.gn:line:col: Unable to load
ninja: error: unknown target: target_name
```

Checks:

- confirm the target name exists
- confirm the dependency path is correct
- inspect `src/out/<product>/args.gn` to make sure the current output directory matches the intended product
- do not use single-command compiler/linker verification for GN generation or Ninja target graph failures

## Failure stage classification

Use `scripts/analyze_build_error.sh` to classify the failed stage before choosing the rerun strategy:

- `pre-gn/sdk-lfs`: SDK install, archive extraction, Git LFS pointer, missing package, or `gzip`/`tar`/`unzip` errors before GN or Ninja
- `gn-generation`: `ERROR at //...`, `Unable to load`, or bad GN evaluation
- `ninja-graph-or-target`: `ninja: error: unknown target`, missing `build.ninja`, or Ninja graph loading failure
- `ninja-compile-link`: compiler or linker failure after Ninja starts, such as `FAILED:`, `fatal error:`, `undefined reference`, `multiple definition`, `ld.lld: error`, or `clang++: error`
- `resource-or-terminated`: explicit `killed` or `OutOfMemory`
- `resource-or-terminated-suspected`: Ninja-looking progress at the log tail with no `FAILED:`, GN error, or Ninja target error. Inspect the latest resource snapshot before changing code.

Only `ninja-compile-link` should use the single failed command as a quick post-fix check, and that command must run from `<arkweb-root>/src/out/<product>`. After it succeeds, switch back to `<arkweb-root>` for the full `build_arkweb.sh` command, or to `<arkweb-root>/src` only for the same direct Ninja target set. Other stages should rerun the configured build command or target set after the stage-specific fix.

## Tooling or generated-file failures

### Missing generated file or stale output

Typical log fragments:

```text
No such file or directory
cannot find
```

Checks:

- read the first earlier error, not only the final missing-file message
- confirm the producer step completed before the failing compile step
- verify whether rerunning the same incremental build is enough before considering any stronger action
- if the failing path is under `src/ohos_sdk/`, do not patch toolchain files or install scripts there directly; check LFS assets, producer steps, and in-project dependencies first

## Resource failures

### Killed or out-of-memory

Typical log fragments:

```text
killed
OutOfMemory
```

Checks:

- confirm whether the process was terminated by the kernel or job limits
- consider lowering `-j` only if the user allows changing parallelism
- do not clean the tree as a first response

### Build stops with no visible error and the process is gone

Typical symptoms:

- the build was running normally in the Ninja phase
- no clear compiler or linker error appears in `build.log`
- the process disappears or returns unexpectedly
- the last visible output may just stop mid-progress

Most likely cause:

- CPU or memory pressure, often effectively an OOM or heavy resource contention event

Required workflow:

- record a resource snapshot for the Ninja phase. If using `build_arkweb.sh`, do it immediately before launching the build. If using direct Ninja, do it immediately before the `ninja` command:

```bash
bash <skill-dir>/scripts/capture_resource_snapshot.sh rk3568_64 before-ninja <arkweb-root>
```

- if the build later stops silently, inspect the latest snapshot file under:

```text
<arkweb-root>/src/out/<product>/resource_snapshots/
```

- treat high CPU saturation together with low `MemAvailable` or low `SwapFree` as a strong signal that parallelism is too high

Suggested mitigation:

- rerun with `-j 32`
- if the machine is still unstable, rerun with `-j 16`
- prefer reducing parallelism before attempting unrelated code changes

## Missing Git LFS assets

### Prebuilt archives or binaries were not fully pulled

This is a common ArkWeb failure mode when checkout completed but `repo forall -c 'git lfs pull'` was skipped or did not finish successfully.

Typical log fragments:

```text
Package native-linux-x64-6.1.0.31-Release.zip not found, need to reinstall...
ERROR: Failed to extract llvm tarball
gzip: stdin: not in gzip format
tar: This does not look like a tar archive
End-of-central-directory signature not found
unzip: cannot find or open ...
```

Why this happens:

- some ArkWeb prebuilts are tracked by Git LFS instead of normal git blobs
- the checkout may contain the file path but only as an LFS pointer file
- `src/ohos_sdk/.install` then tries to unzip or untar that placeholder as if it were a real archive
- the correct fix is usually to restore project-local assets, not to edit files under `src/ohos_sdk/` or change server state outside the current project

Primary config locations to inspect:

- `<arkweb-root>/src/.gitattributes`
  root-level LFS tracking for current `ohos_sdk/*.zip`, `ohos_sdk/llvm-linux-x86_64_stripped.tar.gz`, and `build/pgo/ohos/arkweb.profdata`
- `<arkweb-root>/src/ohos_sdk/.gitattributes`
  LFS tracking for SDK-local archives such as `rust-toolchain.tar.gz` and older split SDK tarballs
- `<arkweb-root>/src/third_party/ohos_ndk/.gitattributes`
  LFS tracking for a set of NDK/LLVM binaries; treat this as a secondary clue unless the failing build step explicitly references that toolchain payload
- `<arkweb-root>/src/ohos_sdk/.install`
  the authoritative list of archive filenames that the SDK install step is currently trying to unzip or untar

Checks:

- run `bash <skill-dir>/scripts/check_lfs_artifacts.sh <arkweb-root>`; it treats packages from `src/ohos_sdk/.install` as current-build required and reports other `.gitattributes` LFS entries as informational
- prioritize the packages named in `src/ohos_sdk/.install` before treating `third_party/ohos_ndk` payloads as the primary root cause
- inspect whether the failing file exists but starts with the Git LFS pointer header:

```text
version https://git-lfs.github.com/spec/v1
```

- check current LFS-tracked ArkWeb prebuilts:

```bash
git -C <arkweb-root>/src lfs ls-files | rg 'ohos_sdk|third_party/ohos_ndk|build/pgo/ohos/arkweb.profdata'
```

Typical fix commands:

```bash
cd <arkweb-root>
repo forall -c 'git lfs pull'
```

Or for the current repo only:

```bash
git -C <arkweb-root>/src lfs pull
```

## Build-script failures

### `build_arkweb.sh` exits before Ninja finishes

Checks:

- inspect the actual exit code
- inspect `src/out/<product>/build.log`
- confirm whether the failure happened in GN generation, a prebuild script, or the Ninja phase
- only switch to direct Ninja if the output directory is already configured and you are resuming the same incremental build
