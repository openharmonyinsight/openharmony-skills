# Tooling Guidance

Load this file when validation, cleanup, formatting, strict checks, or CI-readiness checks are requested.

## Intent

Use project tooling to cover format and machine-checkable convention rules without making normal code generation heavy. Keep human review focused on the OpenHarmony rules that tools do not reliably enforce.

## Packaged tooling

This skill bundles:

- `../scripts/oh_cpp_guard.py`
- `../scripts/.clang-format`
- `../scripts/.clang-tidy`

The guard script uses the bundled clang-format and clang-tidy configuration so the skill remains portable after packaging.

For OpenHarmony repositories, prefer the LLVM tools under the source tree's `prebuilts/clang/ohos/<host>/.../bin/` directory. The OpenHarmony clang already carries the correct libc++ setup. Do not add synthetic libc++ or resource-dir arguments when using the OpenHarmony prebuilt tool.

The guard script discovers the OpenHarmony root in this order:

1. `--ohos-root <path>`
2. `OHOS_ROOT`, `OHOS_BASE`, or `OPENHARMONY_ROOT`
3. upward search from the current directory and checked paths for `prebuilts/clang`

It then prefers `clang-format` and `clang-tidy` from the current host's `prebuilts/clang/ohos/<host>/**/bin/` before falling back to `PATH`. It does not choose tools from a different host tag because that can fail with `exec format error`.

If the script must fall back to a non-OpenHarmony `clang-tidy`, it adds OpenHarmony libc++ include directories as a best-effort fallback. The primary fallback path is `prebuilts/clang/ohos/<host>/llvm_ndk/include/libcxx-ohos/include/c++/v1`. Prefer a real OpenHarmony prebuilt `clang-tidy` whenever available.

## Validation flow

### Default after generation

Do not run bundled tooling by default. First do a lightweight self-check against `rules.md` for file layout, naming, include guards, public API comments, copy or move semantics, inheritance, macros, templates, ownership, and lambda captures.

### Requested validation or cleanup

When the user asks for validation, cleanup, formatting, or tool checks, run formatting checks only and scope them to changed files:

```bash
python3 <skill-path>/scripts/oh_cpp_guard.py --format-only <changed-files>
```

Apply formatting fixes in place only when the user asks for cleanup or formatting changes:

```bash
python3 <skill-path>/scripts/oh_cpp_guard.py --format-only --fix-format <changed-files>
```

### Strict validation

Run clang-tidy only when the user explicitly asks for strict validation, clang-tidy, full checks, or CI readiness. Prefer changed `.cpp` files and pass a compile database when the repository provides one:

```bash
python3 <skill-path>/scripts/oh_cpp_guard.py --tidy-only path/to/file.cpp
```

#### Compile database for OpenHarmony

OpenHarmony clang-tidy is most reliable with a compile database. The compile database is only meaningful after the target has been built or at least after GN has generated the build graph. If only the GN phase has run, some generated headers may still be missing, so clang-tidy can still fail on code that has not completed a build.

Generate the compile database from the OpenHarmony source root with the prebuilt ninja:

```bash
prebuilts/build-tools/linux-x86/bin/ninja \
  -C out/rk3568 \
  -w dupbuild=warn \
  -t compdb cc cxx > out/compile_commands.json
```

Use the host prebuilt ninja when it exists, such as `prebuilts/build-tools/linux-x86/bin/ninja`. Do not use `prebuilts/build-tools/ohos/bin/ninja` from a non-OHOS host; it may be an ARM/OHOS binary and fail with `exec format error`. If no host prebuilt ninja is present, the guard falls back to `ninja` from `PATH`.

Then run clang-tidy from the OpenHarmony root and point the guard at the directory containing `compile_commands.json`:

```bash
python3 <skill-path>/scripts/oh_cpp_guard.py \
  --ohos-root /path/to/openharmony \
  --compile-db /path/to/openharmony/out \
  --tidy-only path/to/file.cpp
```

The guard script can generate the compile database explicitly when requested:

```bash
python3 <skill-path>/scripts/oh_cpp_guard.py \
  --ohos-root /path/to/openharmony \
  --build-dir out/rk3568 \
  --generate-compile-db \
  --tidy-only path/to/file.cpp
```

Do not generate the compile database by default during normal validation; it can be expensive, may produce a multi-GB `compile_commands.json`, and may expose missing generated-header problems if the build has not completed.

If the command is not run from inside the OpenHarmony checkout, pass the root explicitly:

```bash
python3 <skill-path>/scripts/oh_cpp_guard.py --ohos-root /path/to/openharmony --tidy-only path/to/file.cpp
```

If a repository requires a specific tool binary, override discovery explicitly:

```bash
python3 <skill-path>/scripts/oh_cpp_guard.py \
  --clang-tidy /path/to/prebuilts/clang/ohos/linux-x86_64/llvm/bin/clang-tidy \
  --tidy-only path/to/file.cpp
```

Use `--no-fallback-cxx-includes` only when a fallback system `clang-tidy` already has the complete C++ include setup or the auto-added OpenHarmony libc++ paths conflict with project-local configuration.

Run the full guard only for explicit full-check requests:

```bash
python3 <skill-path>/scripts/oh_cpp_guard.py <changed-files>
```

Avoid scanning the whole repository unless the user asks for a repo-wide check.

## What tooling covers well

- line width, indentation, brace style, spacing
- many naming rules through `readability-identifier-naming`
- `using namespace` checks
- `nullptr` and `override`
- C-style casts
- broad macro usage detection

## What still needs human judgment

- file naming and class-to-file matching
- copyright headers
- public API comment quality
- header ownership and improper `extern` usage
- include placement inside `extern "C"`
- whether forward declarations should be replaced with includes
- anonymous namespace placement
- deleted copy or move semantics and polymorphic design
- whether templates are justified at all
- OpenHarmony ownership style choices
- lambda capture lifetime risks

## Evaluation tie-in

When this skill itself is being benchmarked, treat tooling output as supplemental evidence. The benchmark should still grade whether the response or generated code reflects OpenHarmony-specific judgment. See [evaluation-framework.md](evaluation-framework.md).
