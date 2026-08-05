#!/usr/bin/env bash
set -euo pipefail

# install_related_skills.sh — Requirements Intake Bundle 依赖安装与预检
# 用法:
#   --check    仅检查，不安装（默认）
#   --install  兼容旧入口；当前仅提示缺失依赖
#   --check-probes  检查 + 能力探针

MODE="${1:---check}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"  # skills/common/requirements/

# 依赖清单（与 frontmatter related-skills 保持一致，CI 校验两者相等）
REQUIRED_SKILLS=(
  "ohos-req-requirement-intake:0.1.0:true"
  "ohos-req-feasibility-analysis:0.1.0:true"
  "ohos-req-arch-decision:0.1.0:true"
  "ohos-req-feature-proposal-baseline:0.1.0:true"
  "ohos-req-value-decision:0.1.0:true"
  "ohos-req-value-ppt-gen:0.1.0:false"
)

ORCHESTRATOR="ohos-req-intake-orchestration"
TOTAL=$(( ${#REQUIRED_SKILLS[@]} + 1 ))  # 依赖 + 编排器自身
INSTALLED=0
MISSING=()
VERSION_MISMATCH=()

for entry in "${REQUIRED_SKILLS[@]}"; do
  name="${entry%%:*}"
  rest="${entry#*:}"
  min_version="${rest%%:*}"
  required="${rest##*:}"

  skill_dir="$SKILLS_DIR/$name"
  skill_file="$skill_dir/SKILL.md"

  if [[ ! -f "$skill_file" ]]; then
    if [[ "$required" == "true" ]]; then
      MISSING+=("$name")
    fi
    continue
  fi

  # 校验目录名与 frontmatter name 一致
  fm_name=$(grep -m1 '^name:' "$skill_file" | sed 's/^name:[[:space:]]*//')
  if [[ "$fm_name" != "$name" ]]; then
    echo "WARN: directory name '$name' != frontmatter name '$fm_name'"
  fi

  # 校验版本
  fm_version=$(grep -m1 'version:' "$skill_file" | sed 's/.*version:[[:space:]]*//')
  if [[ -n "$min_version" && -n "$fm_version" ]]; then
    if [[ "$fm_version" < "$min_version" ]]; then
      VERSION_MISMATCH+=("$name (found=$fm_version, required>=$min_version)")
    fi
  fi

  INSTALLED=$((INSTALLED + 1))
done

# 编排器自身
if [[ -f "$SKILLS_DIR/$ORCHESTRATOR/SKILL.md" ]]; then
  INSTALLED=$((INSTALLED + 1))
fi

echo "Bundle: ohos-requirements-intake"
echo "Installed: $INSTALLED/$TOTAL"

missing_count=0
for m in "${MISSING[@]:-}"; do
  [[ -z "$m" ]] && continue
  echo "  MISSING (required): $m"
  missing_count=$((missing_count + 1))
done
echo "Required missing: $missing_count"

version_mismatch_count=0
for v in "${VERSION_MISMATCH[@]:-}"; do
  [[ -z "$v" ]] && continue
  echo "  VERSION: $v"
  version_mismatch_count=$((version_mismatch_count + 1))
done
echo "Version mismatch: $version_mismatch_count"

if [[ "$missing_count" -gt 0 ]]; then
  echo "Result: NOT READY"
  echo ""
  echo "Restore missing skills from skills/common/requirements in the same repository branch."
  exit 1
fi

if [[ "$version_mismatch_count" -gt 0 ]]; then
  echo "Result: NOT READY (version mismatch)"
  exit 1
fi

echo "Result: READY"
exit 0
