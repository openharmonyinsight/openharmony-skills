# Independent Component Build

Use this reference for `hb build <component> -i` and `hb build <component> -t`.

## Command Rules

```bash
command -v hb
hb build <component-name> -i
hb build <component-name> -t
```

If `hb` is missing and the workspace contains `build/hb`:

```bash
python3 -m pip install --user build/hb
export PATH="$HOME/.local/bin:$PATH"
command -v hb
```

Rules:

- Use the OpenHarmony component name, not necessarily the repository name.
- Put `-i` or `-t` after the component name.
- Use `-i` for source validation and `-t` for test validation.
- If both are requested, run `-i` first.
- Use multi-component builds only when the components are known to be adapted or the user asks for combined validation.
- Do not default to `--skip-download`; use it only for local debugging or explicit no-download requests.

## Useful Options

```bash
hb build <component-name> -i --keep-ninja-going
hb build <component-name> -i --build-target <target>
hb build <component-name> -i --gn-args key=value
hb build <component-name> -i --skip-download
```

## Output

Independent build output is usually under:

- `out/standard/src/`
- `out/standard/src/lib.unstripped/`
- `out/standard/test/`
- `out/standard/test/lib.unstripped/`

Check the command exit code and final hb output first, then inspect the relevant `out/standard/` artifacts.

## Diagnosis Patterns

- `OHOS component:(xxx) not found`: verify the component is declared and dependency names match hb/HPM component names.
- `unable to find linux-x64 based @ohos/xxx`: required dependent package is missing or lacks a usable Linux x64 snapshot.
- `unable to find linux-x64 based @openharmony/xxx`: check whether metadata uses `@openharmony/<component>` while the available package is `@ohos/<component>`.
- `part_subsystem.json does not exist`: inspect generated component metadata and independent-build setup.
- Header-not-found or undefined-symbol errors: inspect dependency exposure, `public_deps`, `public_configs`, exported include dirs, required defines, and source inclusion.
- Macro or flag missing only in independent build: use `gn desc` to inspect `defines`, `cflags`, `cflags_cc`, `configs`, `public_configs`, and `all_dependent_configs`.
- Absolute local paths in `BUILD.gn` usually fail because independent builds consume dependencies from packages under `binary/`, not from the full source tree.

If symptoms do not match current sources, check whether `out/standard/` is stale before changing code.
