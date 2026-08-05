#!/usr/bin/env bash
set -euo pipefail

# test_related_skills_consistency.sh — Requirements Intake Bundle 一致性/完整性场景
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

# --- 场景1：完整环境 → install --check 7/7 READY + consistency CONSISTENT ---
sbx="$(setup_sandbox)"
out="$(bash "$(sbx_install "$sbx")" --check || true)"
echo "$out" | grep -q 'Installed: 7/7' && echo "$out" | grep -q 'Result: READY' \
  && ok "S1 完整环境预检 7/7 READY" || { bad "S1 期望 7/7 READY"; echo "$out"; }
cout="$(bash "$(sbx_check "$sbx")" || true)"
echo "$cout" | grep -q 'Result: CONSISTENT' \
  && ok "S1 三方一致性 CONSISTENT" || { bad "S1 期望 CONSISTENT"; echo "$cout"; }

# --- 场景2：删除一个必选依赖 → install --check NOT READY + Required missing 1 ---
rm -rf "$sbx/skills/common/requirements/ohos-req-feature-proposal-baseline"
out="$(bash "$(sbx_install "$sbx")" --check || true)"
echo "$out" | grep -q 'Required missing: 1' && echo "$out" | grep -q 'Result: NOT READY' \
  && ok "S2 缺失依赖预检失败 (missing 1)" || { bad "S2 期望 missing 1 NOT READY"; echo "$out"; }

# --- 场景3：依赖版本过低 → install --check NOT READY (version mismatch) ---
awk '{if (!done && $0=="  version: 0.3.0") {print "  version: 0.0.1"; done=1} else {print}}' \
  "$sbx/skills/common/requirements/ohos-req-arch-decision/SKILL.md" > "$sbx/arch.new" \
  && mv "$sbx/arch.new" "$sbx/skills/common/requirements/ohos-req-arch-decision/SKILL.md"
out="$(bash "$(sbx_install "$sbx")" --check || true)"
echo "$out" | grep -q 'Version mismatch: 1' && echo "$out" | grep -q 'NOT READY' \
  && ok "S3 版本过低预检失败 (version mismatch 1)" || { bad "S3 期望 version mismatch"; echo "$out"; }

# --- 场景4：编排器正文引用清单外 skill → consistency INCONSISTENT ---
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

# --- 场景6：非编排器 reference 中引用旧别名 → consistency INCONSISTENT ---
sbx4="$(setup_sandbox)"
printf '\n历史别名 `ohos-feature` 不应再出现。\n' >> "$sbx4/skills/common/requirements/ohos-req-requirement-intake/reference/requirement-fields.md"
cout="$(bash "$(sbx_check "$sbx4")" || true)"
echo "$cout" | grep -q 'UNRESOLVED reference: ohos-feature' && echo "$cout" | grep -q 'Result: INCONSISTENT' \
  && ok "S6 reference 中旧别名被检出" || { bad "S6 期望旧别名 INCONSISTENT"; echo "$cout"; }

# --- 场景7：--install 支持 source/target 环境变量覆盖 ---
sbx5="$(setup_sandbox)"
target="$sbx5/target"
mkdir -p "$target"
cp -R "$sbx5/skills/common/requirements/ohos-req-intake-orchestration" "$target/"
out="$(OHOS_REQ_SKILLS_DIR="$target" OHOS_REQ_SKILLS_SOURCE_DIR="$sbx5/skills/common/requirements" bash "$target/ohos-req-intake-orchestration/scripts/install_related_skills.sh" --install || true)"
echo "$out" | grep -q 'Installed: 7/7' && echo "$out" | grep -q 'Result: READY' && [[ -d "$target/ohos-req-feature-proposal-baseline" ]] \
  && ok "S7 --install 复制缺失依赖并 READY" || { bad "S7 期望 install READY"; echo "$out"; }

# --- 场景8：数值 semver 比较不把 0.10.0 误判为小于 0.3.0 ---
sbx6="$(setup_sandbox)"
awk '{if (!done && $0=="  version: 0.3.0") {print "  version: 0.10.0"; done=1} else {print}}' \
  "$sbx6/skills/common/requirements/ohos-req-feature-proposal-baseline/SKILL.md" > "$sbx6/feature.new" \
  && mv "$sbx6/feature.new" "$sbx6/skills/common/requirements/ohos-req-feature-proposal-baseline/SKILL.md"
out="$(bash "$(sbx_install "$sbx6")" --check || true)"
echo "$out" | grep -q 'Version mismatch: 0' && echo "$out" | grep -q 'Result: READY' \
  && ok "S8 semver 0.10.0 >= 0.3.0" || { bad "S8 期望 semver READY"; echo "$out"; }

echo ""
echo "Summary: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
