# Vendored openpyxl runtime dependency for Phase5 xlsx export

`openpyxl_vendor.zip` bundles `openpyxl` (MIT) and its required runtime dependency
`et_xmlfile` (MIT) as a single importable zip. `phase5_export.py` inserts it onto
`sys.path` before `import openpyxl`, so Phase5 export:

- does NOT rely on the user's global Python environment,
- does NOT modify the user's environment at runtime (read-only zip import),
- works fully offline (no `pip`/network needed at runtime),
- is uninstalled with the plugin automatically (this file ships under the
  skill's `assets/` dir, which the platform install scripts copy as part of
  `skills/` and remove via the owned-files manifest).

## Regenerating the vendor zip

The pinned source of truth is `../requirements.txt` (`openpyxl==3.1.5`).

```bash
python -m pip download --no-deps --no-binary :none: -d /tmp/wheels openpyxl==3.1.5
python -m pip download --no-deps -d /tmp/wheels et_xmlfile
# Or, from an existing install, zip the two packages from site-packages:
python -c "import openpyxl, et_xmlfile, os; print(os.path.dirname(openpyxl.__file__)); print(os.path.dirname(et_xmlfile.__file__))"
zip openpyxl_vendor.zip openpyxl et_xmlfile   # both at top level of the zip
```

The zip must contain `openpyxl/` and `et_xmlfile/` at its top level so that
`sys.path.insert(0, "<this_dir>/openpyxl_vendor.zip")` makes both importable.

## Health check

```bash
python -S -c "import sys; sys.path.insert(0,'openpyxl_vendor.zip'); import openpyxl; print(openpyxl.__version__)"
```

`-S` skips `site` (no global site-packages), proving the zip is self-contained.

## Version pin

Bump the version in `../requirements.txt` and regenerate the zip. The Phase5
export smoke test (`test_phase5_export.sh`) asserts the vendored version equals
the pinned version to detect drift.
