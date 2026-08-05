#!/usr/bin/env bash
set -euo pipefail

# check_related_skills_consistency.sh — Requirements Intake Bundle 三方一致性校验
# 校验下列三集合两两相等，任一漂移即判失败（防止重命名/新增时遗漏同步）：
#   A. 编排器 SKILL.md 正文引用的 ohos-req-* 集合（spawn / 调用点）
#   B. 编排器 frontmatter metadata.related-skills 声明集合
#   C. install_related_skills.sh 中 REQUIRED_SKILLS 数组
# 用法: bash check_related_skills_consistency.sh
# 退出码: 0 一致 / 1 不一致 / 2 文件缺失

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORCH_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ORCH_SKILL="$ORCH_DIR/SKILL.md"
INSTALL_SH="$SCRIPT_DIR/install_related_skills.sh"

[ -f "$ORCH_SKILL" ] || { echo "FATAL: $ORCH_SKILL not found" >&2; exit 2; }
[ -f "$INSTALL_SH" ] || { echo "FATAL: $INSTALL_SH not found" >&2; exit 2; }

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# A: 正文引用集合（第二个 --- 之后的 ohos-req-* 记号，排除编排器自身）
awk '/^---$/{c++; next} c>=2{print}' "$ORCH_SKILL" \
  | grep -oE 'ohos-req-[a-z0-9-]+' \
  | grep -v -x 'ohos-req-intake-orchestration' \
  | sort -u > "$tmp/body.txt"

# B: frontmatter related-skills 声明集合（两个 --- 之间的 "- name:" 行）
awk '/^---$/{c++; next} c==1{print}' "$ORCH_SKILL" \
  | awk '/^[[:space:]]*- name:/{sub(/^[[:space:]]*- name:[[:space:]]*/,""); sub(/[[:space:]]*$/,""); print}' \
  | sort -u > "$tmp/declared.txt"

# C: install_related_skills.sh REQUIRED_SKILLS 数组中的 name（带 ":version:required" 的条目，排除 ORCHESTRATOR 自身变量）
grep -oE '"ohos-req-[a-z0-9-]+:' "$INSTALL_SH" \
  | sed 's/^"//; s/:$//' \
  | sort -u > "$tmp/install.txt"

rc=0
cmp_sets() {
  local label="$1" a="$2" b="$3"
  if diff -q "$a" "$b" >/dev/null; then
    echo "OK   [$label] ($(wc -l < "$a" | tr -d ' ') skills)"
  else
    rc=1
    echo "MISMATCH [$label]"
    echo "  only in $(basename "$a"): $(comm -23 "$a" "$b" | tr '\n' ' ')"
    echo "  only in $(basename "$b"): $(comm -13 "$a" "$b" | tr '\n' ' ')"
  fi
}

echo "Bundle: ohos-requirements-intake"
echo "body=$(wc -l < "$tmp/body.txt" | tr -d ' ') declared=$(wc -l < "$tmp/declared.txt" | tr -d ' ') install=$(wc -l < "$tmp/install.txt" | tr -d ' ')"
cmp_sets "body vs declared"            "$tmp/body.txt"     "$tmp/declared.txt"
cmp_sets "declared vs install-array"   "$tmp/declared.txt" "$tmp/install.txt"

if [ "$rc" -eq 0 ]; then
  echo "Result: CONSISTENT"
else
  echo "Result: INCONSISTENT — 三处名称需保持同步："
  echo "  1) SKILL.md frontmatter metadata.related-skills"
  echo "  2) 编排器正文 spawn/调用点的 ohos-req-* 引用"
  echo "  3) install_related_skills.sh REQUIRED_SKILLS 数组"
fi
exit "$rc"
