#!/usr/bin/env bash
# test-api-reference-install.sh — validate install.sh integrity checks.
# Covers: empty install / valid domain (FULL) / missing index (DEGRADED) /
# malformed JSON index / referenced file missing / directory traversal path /
# repeat (idempotent probe).
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../../../.." && pwd)"
INSTALL_SH="$SCRIPT_DIR/install.sh"

pass=0; fail=0
ok()  { printf '[OK] %s\n' "$1";   pass=$((pass+1)); }
bad() { printf '[FAIL] %s\n' "$1" >&2; fail=$((fail+1)); }

# install.sh resolves domains relative to its own dir; stage a throwaway
# api-reference root by copying install.sh into a temp tree.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/api-reference"
cp "$INSTALL_SH" "$TMP/api-reference/install.sh"
chmod +x "$TMP/api-reference/install.sh"
RUN() { bash "$TMP/api-reference/install.sh" "$@"; }

# 1. empty install -> no domain
out=$(RUN 2>&1); rc=$?
[[ "$rc" -eq 0 ]] && ok "empty install exits 0" || bad "empty install exit $rc"
echo "$out" | grep -q "none — Demo Pipeline runs in DEGRADED mode" \
  && ok "empty install reports DEGRADED" || bad "empty install missing DEGRADED line"

# 2. valid domain -> FULL
mkdir -p "$TMP/api-reference/ArkUI"
printf '{"name":"alpha"}' > "$TMP/api-reference/ArkUI/alpha.json"
printf '{"name":"beta"}'  > "$TMP/api-reference/ArkUI/beta.json"
cat > "$TMP/api-reference/ArkUI/index.json" <<EOF
{"modules":[{"files":[{"name":"alpha","type":"class","file":"alpha.json"},
                      {"name":"beta","type":"class","file":"beta.json"}]}]}
EOF
out=$(RUN ArkUI 2>&1)
echo "$out" | grep -q "\[FULL\] ArkUI" && ok "valid domain reports FULL" \
  || { bad "valid domain not FULL: $out"; }

# 3. missing index -> DEGRADED
mkdir -p "$TMP/api-reference/NoIndex"
out=$(RUN NoIndex 2>&1)
echo "$out" | grep -q "\[DEGRADED\] NoIndex: index.json not found" \
  && ok "missing index reports DEGRADED" || bad "missing index not reported"

# 4. malformed JSON index -> DEGRADED
mkdir -p "$TMP/api-reference/BadJson"
printf 'not json{' > "$TMP/api-reference/BadJson/index.json"
out=$(RUN BadJson 2>&1)
echo "$out" | grep -q "\[DEGRADED\] BadJson: index.json not valid JSON" \
  && ok "malformed JSON index reports DEGRADED" || bad "malformed index not reported: $out"

# 5. referenced file missing -> DEGRADED
mkdir -p "$TMP/api-reference/MissingFile"
cat > "$TMP/api-reference/MissingFile/index.json" <<EOF
{"modules":[{"files":[{"name":"alpha","type":"class","file":"alpha.json"}]}]}
EOF
out=$(RUN MissingFile 2>&1)
echo "$out" | grep -q "\[DEGRADED\] MissingFile: integrity check failed" \
  && ok "missing referenced file reports DEGRADED" || bad "missing ref not reported: $out"
echo "$out" | grep -q "referenced file missing: alpha.json" \
  && ok "missing referenced file names the file" || bad "missing ref not named"

# 6. directory traversal path -> DEGRADED
mkdir -p "$TMP/api-reference/Traversal"
printf '{"name":"x"}' > "$TMP/api-reference/Traversal/x.json"
cat > "$TMP/api-reference/Traversal/index.json" <<EOF
{"modules":[{"files":[{"name":"x","type":"class","file":"../../etc/passwd"}]}]}
EOF
out=$(RUN Traversal 2>&1)
echo "$out" | grep -q "\[DEGRADED\] Traversal: integrity check failed" \
  && ok "traversal path reports DEGRADED" || bad "traversal not reported: $out"
echo "$out" | grep -q "unsafe file path" \
  && ok "traversal path named unsafe" || bad "traversal not named unsafe"

# 7. corrupted referenced JSON -> DEGRADED
mkdir -p "$TMP/api-reference/BadRef"
printf 'oops not json' > "$TMP/api-reference/BadRef/alpha.json"
cat > "$TMP/api-reference/BadRef/index.json" <<EOF
{"modules":[{"files":[{"name":"alpha","type":"class","file":"alpha.json"}]}]}
EOF
out=$(RUN BadRef 2>&1)
echo "$out" | grep -q "not valid JSON" \
  && ok "corrupted referenced JSON reported" || bad "corrupted ref not reported: $out"

# 8. repeat probe is idempotent (no state mutated)
out1=$(RUN ArkUI 2>&1)
out2=$(RUN ArkUI 2>&1)
[[ "$out1" == "$out2" ]] && ok "repeat probe idempotent" \
  || bad "repeat probe diverged"

# 9. all-domains probe summarizes
out=$(RUN 2>&1)
echo "$out" | grep -q "Summary:" && ok "all-domains probe summarizes" \
  || bad "all-domains probe no summary"

# 10. checksum present and correct -> FULL with "checksum(s) verified"
mkdir -p "$TMP/api-reference/Checksum"
printf '{"name":"x"}' > "$TMP/api-reference/Checksum/x.json"
CHK="$(sha256sum "$TMP/api-reference/Checksum/x.json" | cut -d' ' -f1)"
cat > "$TMP/api-reference/Checksum/index.json" <<EOF
{"sdk_version":"6.0","source":"https://example.com/api-ref",
 "modules":[{"files":[{"name":"x","type":"class","file":"x.json","checksum":"$CHK"}]}]}
EOF
out=$(RUN Checksum 2>&1)
echo "$out" | grep -q "\[FULL\] Checksum" && ok "checksum correct reports FULL" \
  || bad "checksum correct not FULL: $out"
echo "$out" | grep -q "checksum(s) verified" && ok "checksum verified count reported" \
  || bad "checksum verified not reported: $out"
echo "$out" | grep -q "sdk_version=6.0" && ok "sdk_version reported" \
  || bad "sdk_version not reported: $out"
echo "$out" | grep -q "source=https://example.com" && ok "source URL reported" \
  || bad "source not reported: $out"

# 11. checksum present but wrong -> DEGRADED
mkdir -p "$TMP/api-reference/BadChecksum"
printf '{"name":"x"}' > "$TMP/api-reference/BadChecksum/x.json"
cat > "$TMP/api-reference/BadChecksum/index.json" <<EOF
{"modules":[{"files":[{"name":"x","type":"class","file":"x.json","checksum":"0000000000000000000000000000000000000000000000000000000000000000"}]}]}
EOF
out=$(RUN BadChecksum 2>&1)
echo "$out" | grep -q "\[DEGRADED\] BadChecksum: integrity check failed" \
  && ok "checksum mismatch reports DEGRADED" || bad "checksum mismatch not reported: $out"
echo "$out" | grep -q "checksum mismatch" \
  && ok "checksum mismatch named" || bad "checksum mismatch not named: $out"

# 12. no checksum field (backward compatible) -> still FULL
mkdir -p "$TMP/api-reference/NoChecksum"
printf '{"name":"x"}' > "$TMP/api-reference/NoChecksum/x.json"
cat > "$TMP/api-reference/NoChecksum/index.json" <<EOF
{"modules":[{"files":[{"name":"x","type":"class","file":"x.json"}]}]}
EOF
out=$(RUN NoChecksum 2>&1)
echo "$out" | grep -q "\[FULL\] NoChecksum" \
  && ok "absent checksum still FULL (backward compatible)" \
  || bad "absent checksum broke FULL: $out"

echo "pass=${pass} fail=${fail}"
[[ "$fail" -eq 0 ]]
