#!/usr/bin/env bash
# test_phase_pipeline.sh — automated tests for the 5 phase2/phase4 business
# scripts + minimum end-to-end pipeline (phase2→phase4→phase5).
#
# Covers the reviewer's concern: 5 new Python business scripts (~4,965 lines)
# had zero automated tests, and no test exercised the minimum end-to-end
# behavior of the test-design pipeline.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS="$SCRIPT_DIR"
PY="${PYTHON:-python3}"

pass=0; fail=0
ok()  { printf '[OK] %s\n' "$1";   pass=$((pass+1)); }
bad() { printf '[FAIL] %s\n' "$1" >&2; fail=$((fail+1)); }

# ── fixture: requirement_analysis.md ──
REQ="# 需求分析报告

## 1. 主单元 [US-001]

- 输入：用户名、密码
- 输出：登录成功/失败

## 2. 边界条件

- 用户名长度 1-20
- 密码长度 6-20

## 3. 等价类

- 有效用户名：长度1-20的字母数字
- 无效用户名：空、超长、特殊字符

## 4. 业务规则

- BR-001：连续3次失败锁定账户

## 5. 因子

| 因子 | 水平1 | 水平2 |
|---|---|---|
| 用户名 | 有效 | 无效 |
| 密码 | 正确 | 错误 |
"

# ── fixture: phase2 batch file (8-col TP table) ──
BATCH2="## 测试点列表

| 测试点ID | 测试场景 | 输入条件 | 预期输出概要 | 测试类型 | 优先级 | 执行方式 | 来源 |
|---|---|---|---|---|---|---|---|
| TP-US01-001 | 有效登录 | 正确用户名密码 | 登录成功 | 功能测试 | P0 | 黑盒自动化 | spec |
| TP-US01-002 | 无效密码 | 正确用户名错误密码 | 登录失败 | 功能测试 | P0 | 黑盒自动化 | spec |
"

# ── fixture: phase4 batch file (TC sections) ──
BATCH4="### TC-temp-001-有效登录

**测试类型：** 功能测试
**测试技术：** 等价类划分
**执行方式：** 黑盒自动化
**用例级别：** P0
**来源：** spec
**关联测试点：** TP-US01-001
**预置条件：**
- 系统正常运行
**测试步骤：**
| 步骤 | 操作 | 预期结果 |
|---|---|---|
| 1 | 输入正确用户名密码 | 登录成功 |

### TC-temp-002-无效密码

**测试类型：** 功能测试
**测试技术：** 等价类划分
**执行方式：** 黑盒自动化
**用例级别：** P0
**来源：** spec
**关联测试点：** TP-US01-002
**预置条件：**
- 系统正常运行
**测试步骤：**
| 步骤 | 操作 | 预期结果 |
|---|---|---|
| 1 | 输入正确用户名错误密码 | 登录失败 |
"

# ── work dir ──
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

printf '%s' "$REQ" > "$WORK/requirement_analysis.md"
mkdir -p "$WORK/batches_phase2"
printf '%s' "$BATCH2" > "$WORK/batches_phase2/batch_US01.md"
mkdir -p "$WORK/batches_phase4"
printf '%s' "$BATCH4" > "$WORK/batches_phase4/batch_001.md"

# ═══════════════════════════════════════════════════════════════════
# 1. phase2_testing_technology.py --technique generate_all
# ═══════════════════════════════════════════════════════════════════
out=$("$PY" "$ASSETS/phase2_testing_technology.py" \
  --technique generate_all \
  --requirement "$WORK/requirement_analysis.md" \
  --output "$WORK/testing_technology.json" 2>&1)
rc=$?
if [[ "$rc" -eq 0 ]] && [[ -f "$WORK/testing_technology.json" ]]; then
  ok "phase2_testing_technology generate_all produces JSON"
else
  bad "phase2_testing_technology generate_all failed (rc=$rc): $out"
fi
if "$PY" -c "import json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); assert d.get('status')=='success'; assert 'techniques' in d" "$WORK/testing_technology.json" 2>/dev/null; then
  ok "phase2_testing_technology JSON has status+techniques"
else
  bad "phase2_testing_technology JSON structure wrong"
fi

# ═══════════════════════════════════════════════════════════════════
# 2. phase2_testpoint_utils.py --action merge_batch_mds
# ═══════════════════════════════════════════════════════════════════
out=$("$PY" "$ASSETS/phase2_testpoint_utils.py" \
  --action merge_batch_mds \
  --batch-dir "$WORK/batches_phase2" \
  --requirement "$WORK/requirement_analysis.md" \
  --output "$WORK/test_point_design.md" 2>&1)
rc=$?
if [[ "$rc" -eq 0 ]] && [[ -f "$WORK/test_point_design.md" ]]; then
  ok "phase2_testpoint_utils merge_batch_mds produces test_point_design.md"
else
  bad "phase2_testpoint_utils merge_batch_mds failed (rc=$rc): $out"
fi
if [[ -f "$WORK/test_point_design.md" ]] && grep -q "TP-US01-001" "$WORK/test_point_design.md" 2>/dev/null; then
  ok "merged test_point_design.md contains TP-US01-001"
else
  bad "merged test_point_design.md missing TP-US01-001"
fi

# ═══════════════════════════════════════════════════════════════════
# 3. phase2_testpoint_utils.py --action coverage_check
# ═══════════════════════════════════════════════════════════════════
out=$("$PY" "$ASSETS/phase2_testpoint_utils.py" \
  --action coverage_check \
  --testpoint "$WORK/test_point_design.md" \
  --requirement "$WORK/requirement_analysis.md" \
  --output "$WORK/coverage_result.json" 2>&1)
rc=$?
if [[ "$rc" -eq 0 ]] && [[ -f "$WORK/coverage_result.json" ]]; then
  ok "phase2_testpoint_utils coverage_check produces JSON"
else
  bad "phase2_testpoint_utils coverage_check failed (rc=$rc): $out"
fi

# ═══════════════════════════════════════════════════════════════════
# 4. phase2_adversary.py
# ═══════════════════════════════════════════════════════════════════
out=$("$PY" "$ASSETS/phase2_adversary.py" \
  --testpoint "$WORK/test_point_design.md" \
  --requirement "$WORK/requirement_analysis.md" \
  --output "$WORK/phase2_adversary.json" 2>&1)
rc=$?
if [[ "$rc" -eq 0 ]] && [[ -f "$WORK/phase2_adversary.json" ]]; then
  ok "phase2_adversary produces JSON"
else
  bad "phase2_adversary failed (rc=$rc): $out"
fi
if [[ -f "$WORK/phase2_adversary.json" ]] && "$PY" -c "import json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); assert 'status' in d" "$WORK/phase2_adversary.json" 2>/dev/null; then
  ok "phase2_adversary JSON has status"
else
  bad "phase2_adversary JSON missing status"
fi

# ═══════════════════════════════════════════════════════════════════
# 5. phase4_testcase_utils.py --action merge_batch_mds
# ═══════════════════════════════════════════════════════════════════
out=$("$PY" "$ASSETS/phase4_testcase_utils.py" \
  --action merge_batch_mds \
  --batch-dir "$WORK/batches_phase4" \
  --testpoint "$WORK/test_point_design.md" \
  --output "$WORK/test_cases.md" 2>&1)
rc=$?
if [[ "$rc" -eq 0 ]] && [[ -f "$WORK/test_cases.md" ]]; then
  ok "phase4_testcase_utils merge_batch_mds produces test_cases.md"
else
  bad "phase4_testcase_utils merge_batch_mds failed (rc=$rc): $out"
fi
if [[ -f "$WORK/test_cases.md" ]] && grep -q "TC-001" "$WORK/test_cases.md" 2>/dev/null; then
  ok "merged test_cases.md contains renumbered TC-001"
else
  bad "merged test_cases.md missing TC-001"
fi

# ═══════════════════════════════════════════════════════════════════
# 6. phase4_adversary.py
# ═══════════════════════════════════════════════════════════════════
out=$("$PY" "$ASSETS/phase4_adversary.py" \
  --testcases "$WORK/test_cases.md" \
  --testpoint "$WORK/test_point_design.md" \
  --output "$WORK/phase4_adversary.json" 2>&1)
rc=$?
if [[ "$rc" -eq 0 ]] && [[ -f "$WORK/phase4_adversary.json" ]]; then
  ok "phase4_adversary produces JSON"
else
  bad "phase4_adversary failed (rc=$rc): $out"
fi
if [[ -f "$WORK/phase4_adversary.json" ]] && "$PY" -c "import json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); assert 'status' in d" "$WORK/phase4_adversary.json" 2>/dev/null; then
  ok "phase4_adversary JSON has status"
else
  bad "phase4_adversary JSON missing status"
fi

# ═══════════════════════════════════════════════════════════════════
# 7. phase4_testcase_utils.py --action coverage_check
# ═══════════════════════════════════════════════════════════════════
out=$("$PY" "$ASSETS/phase4_testcase_utils.py" \
  --action coverage_check \
  --md "$WORK/test_cases.md" \
  --testpoint "$WORK/test_point_design.md" \
  --output "$WORK/phase4_coverage.json" 2>&1)
rc=$?
if [[ "$rc" -eq 0 ]] && [[ -f "$WORK/phase4_coverage.json" ]]; then
  ok "phase4_testcase_utils coverage_check produces JSON"
else
  bad "phase4_testcase_utils coverage_check failed (rc=$rc): $out"
fi

# ═══════════════════════════════════════════════════════════════════
# 8. END-TO-END: phase5_export.py consumes merged test_cases.md
#    + test_point_design.md → test_cases.xlsx + validation_report.md
# ═══════════════════════════════════════════════════════════════════
# phase5 needs the vendored openpyxl; copy _vendor into the work dir.
cp -r "$ASSETS/_vendor" "$WORK/_vendor"
cp "$ASSETS/phase5_export.py" "$WORK/phase5_export.py"

out=$("$PY" -S "$WORK/phase5_export.py" \
  --output "$WORK" \
  --testpoint "$WORK/test_point_design.md" 2>&1)
rc=$?
if [[ "$rc" -eq 0 ]] && echo "$out" | grep -q '"status": "success"'; then
  ok "e2e phase5_export succeeds on pipeline output"
else
  bad "e2e phase5_export failed (rc=$rc): $out"
fi
if [[ -f "$WORK/test_cases.xlsx" ]] && [[ -s "$WORK/test_cases.xlsx" ]]; then
  ok "e2e test_cases.xlsx generated and non-empty"
else
  bad "e2e test_cases.xlsx missing/empty"
fi
if [[ -f "$WORK/validation_report.md" ]]; then
  ok "e2e validation_report.md generated"
else
  bad "e2e validation_report.md missing"
fi
# Verify the e2e validation report passes the Level D gate (score>=80, P0=0).
"$PY" - "$WORK/validation_report.md" <<'PY' && ok "e2e report: score>=80 and P0=0" || bad "e2e report gate values wrong"
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"\*\*综合\*\*[^\n]*?(\d+)/100", t)
p = re.search(r"P0问题数[：:]\s*(\d+)", t)
assert m and p, "score/p0 not found in e2e report"
assert int(m.group(1)) >= 80, f"e2e score {m.group(1)} < 80"
assert int(p.group(1)) == 0, f"e2e P0 {p.group(1)} > 0"
PY

# ═══════════════════════════════════════════════════════════════════
# 9. NEGATIVE: allpairspy unavailable → pairwise=skipped degradation
#    Blocks allpairspy import via sys.modules to reliably simulate its
#    absence regardless of whether it is installed on the test machine.
#    Fixture has 正交判定：非正交 + 组合真值表 to trigger the pairwise path.
# ═══════════════════════════════════════════════════════════════════
REQ_ORTH="# 需求分析报告

## 1. 主单元 [US-002]

- 输入：浏览器、网络
- 输出：适配结果

正交判定：非正交

#### 组合真值表

| COND-001 | COND-002 |
|---|---|
| Chrome | WiFi |
| Firefox | 5G |
| Chrome | 5G |
| Firefox | WiFi |

## 2. 全局规格表

| COND-001 | 浏览器 |
|---|---|
| COND-002 | 网络 |
"

printf '%s' "$REQ_ORTH" > "$WORK/req_nonorth.md"

cat > "$WORK/_block_allpairspy.py" <<'PYEOF'
import sys, runpy
sys.modules['allpairspy'] = None  # force ImportError on 'import allpairspy'
real_script = sys.argv.pop(1)    # extract real script path from argv
runpy.run_path(real_script, run_name='__main__')
PYEOF

out=$("$PY" "$WORK/_block_allpairspy.py" "$ASSETS/phase2_testing_technology.py" \
  --technique generate_all \
  --requirement "$WORK/req_nonorth.md" \
  --output "$WORK/testing_technology_nopair.json" 2>&1)
rc=$?
if [[ "$rc" -eq 0 ]] && [[ -f "$WORK/testing_technology_nopair.json" ]]; then
  ok "phase2 generate_all succeeds even without allpairspy (degraded)"
else
  bad "phase2 generate_all failed without allpairspy (rc=$rc): $out"
fi
if [[ -f "$WORK/testing_technology_nopair.json" ]] && "$PY" -c "
import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
fc = d.get('techniques', {}).get('factor_combination', {})
found = any(v.get('coverage') == 'pairwise=skipped' for v in fc.values() if isinstance(v, dict))
assert found, 'no pairwise=skipped found; degradation was silent'
" "$WORK/testing_technology_nopair.json" 2>/dev/null; then
  ok "pairwise=skipped degradation written to result when allpairspy absent"
else
  bad "pairwise degradation not recorded (silent)"
fi
if echo "$out" | grep -q '\[WARN\] allpairspy not found'; then
  ok "startup probe warns about missing allpairspy on stderr"
else
  bad "startup probe did not warn about missing allpairspy"
fi

echo ""
echo "pass=${pass} fail=${fail}"
[[ "$fail" -eq 0 ]]
