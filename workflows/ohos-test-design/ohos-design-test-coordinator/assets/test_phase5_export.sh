#!/usr/bin/env bash
# test_phase5_export.sh — Phase5 xlsx export smoke + openpyxl lifecycle tests.
# Proves: (a) the vendored openpyxl_vendor.zip is self-contained (runs under
# `python3 -S`, no global site-packages); (b) missing vendor -> fail-fast;
# (c) missing output dir -> fail-fast; (d) repeat execution idempotent;
# (e) vendored version == pinned requirements.txt version.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS="$SCRIPT_DIR"
EXPORT_PY="$ASSETS/phase5_export.py"
VENDOR_ZIP="$ASSETS/_vendor/openpyxl_vendor.zip"

pass=0; fail=0
ok()  { printf '[OK] %s\n' "$1";   pass=$((pass+1)); }
bad() { printf '[FAIL] %s\n' "$1" >&2; fail=$((fail+1)); }

PY="${PYTHON:-python3}"
# Use -S to skip site-packages, proving the vendor zip is self-contained.
RUN_ISO() { "$PY" -S "$EXPORT_PY" "$@"; }

cat > "$SCRIPT_DIR/.tp_smoke_tp.md" <<'EOF'
# 测试点设计

## 汇总区

| 测试点ID | 测试场景 | 预期输出概要 | 优先级 | 执行方式 |
|---|---|---|---|---|
| TP-001 | 场景A | 输出X | P0 | 黑盒自动化 |
EOF

cat > "$SCRIPT_DIR/.tp_smoke_tc.md" <<'EOF'
# 测试用例文档

### TC-001-场景A

**测试类型：** 功能测试
**测试技术：** 等价类划分
**执行方式：** 黑盒自动化
**用例级别：** P0
**来源：** spec
**关联测试点：** TP-001
**预置条件：**
- 条件1
**测试步骤：**
| 步骤 | 操作 | 预期结果 |
|---|---|---|
| 1 | 执行A | 返回成功 |
EOF

# 1. isolated full export (vendored openpyxl, no global site-packages)
TMP="$(mktemp -d)"
mkdir -p "$TMP/out"
cp "$EXPORT_PY" "$TMP/out/phase5_export.py"
cp -r "$ASSETS/_vendor" "$TMP/out/_vendor"
cp "$SCRIPT_DIR/.tp_smoke_tc.md" "$TMP/out/test_cases.md"
cp "$SCRIPT_DIR/.tp_smoke_tp.md" "$TMP/out/test_point_design.md"
out=$(cd "$TMP/out" && "$PY" -S phase5_export.py --output . --testpoint test_point_design.md 2>&1)
rc=$?
if [[ "$rc" -eq 0 ]] && echo "$out" | grep -q '"status": "success"'; then
  ok "isolated export succeeds under -S (vendored openpyxl)"
else
  bad "isolated export failed (rc=$rc): $out"
fi
if [[ -f "$TMP/out/test_cases.xlsx" ]] && [[ -s "$TMP/out/test_cases.xlsx" ]]; then
  ok "test_cases.xlsx generated and non-empty"
else
  bad "test_cases.xlsx missing/empty"
fi
if [[ -f "$TMP/out/validation_report.md" ]]; then
  ok "validation_report.md generated"
else
  bad "validation_report.md missing"
fi
"$PY" - "$TMP/out/validation_report.md" <<'PY' && ok "validation report: score>=80 and P0=0" || bad "validation report gate values wrong"
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"\*\*综合\*\*[^\n]*?(\d+)/100", t)
p = re.search(r"P0问题数[：:]\s*(\d+)", t)
assert m and p, "score/p0 not found"
assert int(m.group(1)) >= 80, f"score {m.group(1)} < 80"
assert int(p.group(1)) == 0, f"P0 {p.group(1)} > 0"
PY

# 2. missing vendor zip -> fail-fast
mkdir -p "$TMP/novendor"
cp "$EXPORT_PY" "$TMP/novendor/phase5_export.py"
cp "$SCRIPT_DIR/.tp_smoke_tc.md" "$TMP/novendor/test_cases.md"
out=$(cd "$TMP/novendor" && "$PY" -S phase5_export.py --output . 2>&1)
rc=$?
if [[ "$rc" -ne 0 ]] && echo "$out" | grep -q "openpyxl not importable"; then
  ok "missing vendor zip -> fail-fast error"
else
  bad "missing vendor zip did not fail-fast (rc=$rc): $out"
fi

# 3. missing output dir -> fail-fast
mkdir -p "$TMP/baddir"
cp "$EXPORT_PY" "$TMP/baddir/phase5_export.py"
cp -r "$ASSETS/_vendor" "$TMP/baddir/_vendor"
cp "$SCRIPT_DIR/.tp_smoke_tc.md" "$TMP/baddir/test_cases.md"
out=$(cd "$TMP/baddir" && "$PY" -S phase5_export.py --output nope_dir 2>&1)
rc=$?
if [[ "$rc" -ne 0 ]] && echo "$out" | grep -q "目录不存在\|error"; then
  ok "missing output dir -> fail-fast error"
else
  bad "missing output dir not caught (rc=$rc): $out"
fi

# 4. repeat execution idempotent
out1=$(cd "$TMP/out" && "$PY" -S phase5_export.py --output . --testpoint test_point_design.md 2>&1)
rc1=$?
out2=$(cd "$TMP/out" && "$PY" -S phase5_export.py --output . --testpoint test_point_design.md 2>&1)
rc2=$?
if [[ "$rc1" -eq 0 && "$rc2" -eq 0 ]] && echo "$out2" | grep -q '"status": "success"'; then
  ok "repeat execution idempotent (both succeed)"
else
  bad "repeat execution diverged (rc1=$rc1 rc2=$rc2)"
fi

rm -rf "$TMP"

# 5. vendored version == pinned requirements.txt version
PINNED="$("$PY" - "$ASSETS/requirements.txt" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"openpyxl==([0-9.]+)", t)
print(m.group(1) if m else "")
PY
)"
VENDORED="$("$PY" -S - "$VENDOR_ZIP" <<'PY'
import sys, zipfile
sys.path.insert(0, sys.argv[1])
import openpyxl
print(openpyxl.__version__)
PY
)"
if [[ -n "$PINNED" && "$PINNED" == "$VENDORED" ]]; then
  ok "vendored openpyxl $VENDORED == pinned $PINNED"
else
  bad "version drift: vendored=$VENDORED pinned=$PINNED"
fi

rm -f "$SCRIPT_DIR/.tp_smoke_tp.md" "$SCRIPT_DIR/.tp_smoke_tc.md"

echo "pass=${pass} fail=${fail}"
[[ "$fail" -eq 0 ]]
