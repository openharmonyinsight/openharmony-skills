#!/usr/bin/env bash
set -euo pipefail

# test_related_skills_consistency.sh — Phase 0 Intake Bundle 一致性/完整性 5 场景
# 覆盖 sunfei2021 #4 要求的 5 个 CI 测试场景。全部在沙箱副本中执行，不污染源树。
# 用法: bash test_related_skills_consistency.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORCH_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$(cd "$ORCH_DIR/.." && pwd)"   # skills/common/requirements

pass=0; fail=0
ok(){ echo "PASS: $1"; pass=$((pass+1)); }
bad(){ echo "FAIL: $1"; fail=$((fail+1)); }

setup_sandbox() {
  local sbx; sbx="$(mktemp -d)"
  mkdir -p "$sbx/skills/common/requirements"
  cp -r "$SKILLS_DIR/." "$sbx/skills/common/requirements/"
  echo "$sbx"
}
sbx_install(){ echo "$1/skills/common/requirements/ohos-req-intake-orchestration/scripts/install_related_skills.sh"; }
sbx_check(){   echo "$1/skills/common/requirements/ohos-req-intake-orchestration/scripts/check_related_skills_consistency.sh"; }
sbx_orch(){    echo "$1/skills/common/requirements/ohos-req-intake-orchestration/SKILL.md"; }

# --- 场景1：完整环境 → install --check 10/10 READY + consistency CONSISTENT ---
sbx="$(setup_sandbox)"
out="$(bash "$(sbx_install "$sbx")" --check || true)"
echo "$out" | grep -q 'Installed: 10/10' && echo "$out" | grep -q 'Result: READY' \
  && ok "S1 完整环境预检 10/10 READY" || { bad "S1 期望 10/10 READY"; echo "$out"; }
cout="$(bash "$(sbx_check "$sbx")" || true)"
echo "$cout" | grep -q 'Result: CONSISTENT' \
  && ok "S1 三方一致性 CONSISTENT" || { bad "S1 期望 CONSISTENT"; echo "$cout"; }

# --- 场景2：删除一个必选依赖 → install --check NOT READY + Required missing 1 ---
rm -rf "$sbx/skills/common/requirements/ohos-req-review-gate"
out="$(bash "$(sbx_install "$sbx")" --check || true)"
echo "$out" | grep -q 'Required missing: 1' && echo "$out" | grep -q 'Result: NOT READY' \
  && ok "S2 缺失依赖预检失败 (missing 1)" || { bad "S2 期望 missing 1 NOT READY"; echo "$out"; }

# --- 场景3：依赖版本过低 → install --check NOT READY (version mismatch) ---
sed -i 's/^  version: 0.1.0/  version: 0.0.1/' "$sbx/skills/common/requirements/ohos-req-arch-decision/SKILL.md"
out="$(bash "$(sbx_install "$sbx")" --check || true)"
echo "$out" | grep -q 'Version mismatch: 1' && echo "$out" | grep -q 'NOT READY' \
  && ok "S3 版本过低预检失败 (version mismatch 1)" || { bad "S3 期望 version mismatch"; echo "$out"; }

# --- 场景4：正文引用清单外 skill → consistency INCONSISTENT ---
sbx2="$(setup_sandbox)"
printf '\n调用 `ohos-req-foo-bar` 作为占位引用。\n' >> "$(sbx_orch "$sbx2")"
cout="$(bash "$(sbx_check "$sbx2")" || true)"
echo "$cout" | grep -q 'Result: INCONSISTENT' \
  && ok "S4 正文引用清单外 skill 被检出" || { bad "S4 期望 INCONSISTENT"; echo "$cout"; }

# --- 场景5：frontmatter 声明清单外 skill → consistency INCONSISTENT ---
sbx3="$(setup_sandbox)"
awk '{print} /  related-skills:/{print "    - name: ohos-req-foo-bar"}' "$(sbx_orch "$sbx3")" > "$sbx3/orch.new" \
  && mv "$sbx3/orch.new" "$(sbx_orch "$sbx3")"
cout="$(bash "$(sbx_check "$sbx3")" || true)"
echo "$cout" | grep -q 'Result: INCONSISTENT' \
  && ok "S5 清单声明清单外 skill 被检出" || { bad "S5 期望 INCONSISTENT"; echo "$cout"; }

echo ""
echo "Summary: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
