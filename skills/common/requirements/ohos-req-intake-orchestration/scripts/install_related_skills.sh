#!/usr/bin/env bash
set -euo pipefail

# install_related_skills.sh — Requirements Intake Bundle 依赖安装与预检
# 用法:
#   --check          仅检查，不安装（默认）
#   --install        从 source 目录复制缺失 skill 到 target 目录
#   --check-probes   检查 + 运行一致性探针
#
# 环境变量:
#   OHOS_REQ_SKILLS_DIR         目标 requirements skills 目录，默认 scripts/../..
#   OHOS_REQ_SKILLS_SOURCE_DIR  安装源 requirements skills 目录，默认同 target

MODE="${1:---check}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
SKILLS_DIR="${OHOS_REQ_SKILLS_DIR:-$DEFAULT_SKILLS_DIR}"
SOURCE_DIR="${OHOS_REQ_SKILLS_SOURCE_DIR:-$DEFAULT_SKILLS_DIR}"

REQUIRED_SKILLS=(
  "ohos-req-requirement-intake:0.4.0:true"
  "ohos-req-feasibility-analysis:0.4.0:true"
  "ohos-req-arch-decision:0.4.0:true"
  "ohos-req-feature-proposal-baseline:0.4.0:true"
  "ohos-req-value-decision:0.4.0:true"
  "ohos-req-value-ppt-gen:0.2.0:false"
)

ORCHESTRATOR="ohos-req-intake-orchestration"
TOTAL=$(( ${#REQUIRED_SKILLS[@]} + 1 ))

version_ge() {
  local found="$1" required="$2"
  IFS=. read -r f1 f2 f3 <<< "$found"
  IFS=. read -r r1 r2 r3 <<< "$required"
  f1="${f1:-0}"; f2="${f2:-0}"; f3="${f3:-0}"
  r1="${r1:-0}"; r2="${r2:-0}"; r3="${r3:-0}"
  if (( f1 != r1 )); then (( f1 > r1 )); return; fi
  if (( f2 != r2 )); then (( f2 > r2 )); return; fi
  (( f3 >= r3 ))
}

install_missing() {
  local name="$1"
  local src="$SOURCE_DIR/$name"
  local dst="$SKILLS_DIR/$name"
  if [[ -d "$dst" ]]; then
    return 0
  fi
  if [[ ! -d "$src" ]]; then
    return 1
  fi
  mkdir -p "$SKILLS_DIR"
  cp -R "$src" "$dst"
}

case "$MODE" in
  --check|--install|--check-probes) ;;
  *)
    echo "Usage: $0 [--check|--install|--check-probes]" >&2
    exit 2
    ;;
esac

if [[ "$MODE" == "--install" ]]; then
  for entry in "${REQUIRED_SKILLS[@]}"; do
    name="${entry%%:*}"
    install_missing "$name" || true
  done
  install_missing "$ORCHESTRATOR" || true
fi

INSTALLED=0
MISSING=()
VERSION_MISMATCH=()

for entry in "${REQUIRED_SKILLS[@]}"; do
  name="${entry%%:*}"
  rest="${entry#*:}"
  min_version="${rest%%:*}"
  required="${rest##*:}"

  skill_file="$SKILLS_DIR/$name/SKILL.md"
  if [[ ! -f "$skill_file" ]]; then
    if [[ "$required" == "true" ]]; then
      MISSING+=("$name")
    fi
    continue
  fi

  fm_name="$(grep -m1 '^name:' "$skill_file" | sed 's/^name:[[:space:]]*//')"
  if [[ "$fm_name" != "$name" ]]; then
    echo "WARN: directory name '$name' != frontmatter name '$fm_name'"
  fi

  fm_version="$(grep -m1 'version:' "$skill_file" | sed 's/.*version:[[:space:]]*//')"
  if [[ -n "$min_version" && -n "$fm_version" ]] && ! version_ge "$fm_version" "$min_version"; then
    VERSION_MISMATCH+=("$name (found=$fm_version, required>=$min_version)")
  fi

  INSTALLED=$((INSTALLED + 1))
done

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
  echo "Restore missing skills from skills/common/requirements in the same repository branch, or run --install with OHOS_REQ_SKILLS_SOURCE_DIR."
  exit 1
fi

if [[ "$version_mismatch_count" -gt 0 ]]; then
  echo "Result: NOT READY (version mismatch)"
  exit 1
fi

if [[ "$MODE" == "--check-probes" ]]; then
  echo "Probe: related skill consistency"
  bash "$SKILLS_DIR/$ORCHESTRATOR/scripts/check_related_skills_consistency.sh"
fi

echo "Result: READY"
exit 0
