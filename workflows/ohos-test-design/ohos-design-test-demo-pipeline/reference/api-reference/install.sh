#!/usr/bin/env bash
# api-reference external data dependency — probe + integrity validation.
#
# The API reference data is NOT shipped in this repo (too large / maintained
# upstream / evolves with SDK versions). This script probes the local install,
# validates index.json schema and every referenced API JSON file, and reports
# FULL / DEGRADED per domain. It does NOT download, does NOT touch the network,
# and does NOT modify the user environment.
#
# A domain is reported FULL only after ALL of:
#   - index.json exists and is valid JSON
#   - schema: { "modules": [{ "files": [{ "name","type","file" }] }] }
#   - every referenced `file` resolves under the domain dir (no absolute / parent
#     traversal / backslash) and is itself valid JSON
#   - (optional) if a file entry declares a `checksum` (sha256 hex), the file
#     content must match; a mismatch forces DEGRADED
# Optional index.json root fields (absent = no check, backward compatible):
#   - `sdk_version`: reported in the FULL line (documents SDK provenance)
#   - `source`:      reported in the FULL line (documents data-source URL/repo)
# Otherwise the domain stays DEGRADED; the Demo Pipeline must NOT claim
# independent run on a degraded domain.
#
# Usage:
#   bash reference/api-reference/install.sh             # probe + validate all domains
#   bash reference/api-reference/install.sh <domain>     # probe + validate one domain
# Exit: 0 always (informational probe); status is reported on stdout.

set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
DOMAIN="${1:-}"

probe_domain() {
  local domain="$1"
  local idx="$HERE/$domain/index.json"
  if [[ ! -f "$idx" ]]; then
    echo "[DEGRADED] $domain: index.json not found -> Demo Pipeline DEGRADED mode"
    return 1
  fi
  "${PYTHON:-python3}" - "$idx" "$HERE/$domain" "$domain" <<'PY' || return 1
import hashlib, json, os, sys
idx, root, domain = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    data = json.load(open(idx, encoding="utf-8"))
except Exception as e:
    print(f"[DEGRADED] {domain}: index.json not valid JSON: {e}")
    sys.exit(1)
modules = data.get("modules") if isinstance(data, dict) else None
if not isinstance(modules, list) or not modules:
    print(f"[DEGRADED] {domain}: index.json schema invalid (modules missing/empty)")
    sys.exit(1)
# Optional metadata fields (absent = no check, backward compatible).
sdk_version = data.get("sdk_version") if isinstance(data, dict) else None
source_url = data.get("source") if isinstance(data, dict) else None
errors = []
total_files = 0
checksum_verified = 0
for mi, mod in enumerate(modules):
    files = mod.get("files") if isinstance(mod, dict) else None
    if not isinstance(files, list):
        errors.append(f"modules[{mi}].files not a list")
        continue
    for fi, entry in enumerate(files):
        if not isinstance(entry, dict):
            errors.append(f"modules[{mi}].files[{fi}] not an object")
            continue
        name = entry.get("name")
        fname = entry.get("file")
        if not name or not fname:
            errors.append(f"modules[{mi}].files[{fi}] missing name/file")
            continue
        if not isinstance(fname, str):
            errors.append(f"{name}: file field not a string")
            continue
        norm = fname.replace("\\", "/")
        if os.path.isabs(fname) or "\\" in fname or ".." in norm.split("/"):
            errors.append(f"{name}: unsafe file path '{fname}' (directory traversal denied)")
            continue
        target = os.path.join(root, fname)
        if not os.path.isfile(target):
            errors.append(f"{name}: referenced file missing: {fname}")
            continue
        try:
            with open(target, encoding="utf-8") as fh:
                json.load(fh)
        except Exception as e:
            errors.append(f"{name}: {fname} not valid JSON: {e}")
            continue
        # Optional sha256 checksum verification (only if index.json declares one).
        expected = entry.get("checksum")
        if expected is not None:
            if not isinstance(expected, str):
                errors.append(f"{name}: checksum field not a string")
                continue
            h = hashlib.sha256()
            with open(target, "rb") as fh:
                for chunk in iter(lambda: fh.read(65536), b""):
                    h.update(chunk)
            actual = h.hexdigest()
            if actual.lower() != expected.lower():
                errors.append(f"{name}: checksum mismatch (expected {expected[:12]}…, got {actual[:12]}…)")
                continue
            checksum_verified += 1
        total_files += 1
if errors:
    print(f"[DEGRADED] {domain}: integrity check failed ({len(errors)} issue(s)):")
    for e in errors[:20]:
        print(f"    - {e}")
    sys.exit(1)
meta_parts = [f"index.json + {total_files} referenced API file(s) validated"]
if checksum_verified:
    meta_parts.append(f"{checksum_verified} checksum(s) verified")
if sdk_version:
    meta_parts.append(f"sdk_version={sdk_version}")
if source_url:
    meta_parts.append(f"source={source_url}")
print(f"[FULL] {domain}: {', '.join(meta_parts)}")
PY
}

echo "api-reference external dependency probe (integrity validation)"
echo "install root: $HERE"
echo

if [[ -n "$DOMAIN" ]]; then
  probe_domain "$DOMAIN"
  echo
  echo "Re-run without args to probe all domains."
  exit 0
fi

found=0
full=0
shopt -s nullglob
for d in "$HERE"/*/; do
  name="$(basename "$d")"
  found=1
  if probe_domain "$name"; then
    full=$((full + 1))
  fi
done
if [[ "$found" -eq 0 ]]; then
  echo "  (none — Demo Pipeline runs in DEGRADED mode until data is installed; NOT independent-run)"
fi
echo
echo "Summary: $full domain(s) FULL"
echo "How to provide api-reference data:"
echo "  1. Obtain the domain's index.json and referenced API JSON files."
echo "     index.json schema: { \"sdk_version\": \"<optional>\", \"source\": \"<optional URL/repo>\","
echo "       \"modules\": [{ \"files\": [{ \"name\",\"type\",\"file\",\"checksum\": \"<optional sha256 hex>\" }] }] }"
echo "  2. Place them under: $HERE/<domain>/"
echo "  3. Re-run: bash reference/api-reference/install.sh <domain>"
echo "A domain is FULL only after this script reports [FULL]; a stale/broken install stays DEGRADED."
exit 0
