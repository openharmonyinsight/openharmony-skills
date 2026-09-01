#!/usr/bin/env bash
set -euo pipefail

# check_related_skills_consistency.sh — Requirements Intake Bundle 引用一致性校验
# 校验：
#   A. 编排器 frontmatter metadata.related-skills
#   B. install_related_skills.sh REQUIRED_SKILLS
#   C. 全部幸存 SKILL.md/reference(s) 中的 ohos-* skill 引用
#   D. requirements bundle 中不得残留 ODK 已废弃的归档根、扁平路径或 link 命令
# 任一悬空引用、三方清单漂移、旧别名或旧 ODK 路径残留即失败。

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORCH_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$(cd "$ORCH_DIR/.." && pwd)"
ORCH_SKILL="$ORCH_DIR/SKILL.md"
INSTALL_SH="$SCRIPT_DIR/install_related_skills.sh"

[[ -f "$ORCH_SKILL" ]] || { echo "FATAL: $ORCH_SKILL not found" >&2; exit 2; }
[[ -f "$INSTALL_SH" ]] || { echo "FATAL: $INSTALL_SH not found" >&2; exit 2; }

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -name 'ohos-req-*' \
  -exec basename {} \; | sort -u > "$tmp/registered.txt"

awk '/^---$/{c++; next} c==1{print}' "$ORCH_SKILL" \
  | awk '/^[[:space:]]*- name:/{sub(/^[[:space:]]*- name:[[:space:]]*/,""); sub(/[[:space:]]*$/,""); print}' \
  | sort -u > "$tmp/declared.txt"

grep -oE '"ohos-req-[a-z0-9-]+:' "$INSTALL_SH" \
  | sed 's/^"//; s/:$//' \
  | sort -u > "$tmp/install.txt"

{
  find "$SKILLS_DIR" -path '*/evals/*' -prune -o -path '*/examples/*' -prune -o \
    \( -name 'SKILL.md' -o -path '*/reference/*.md' -o -path '*/references/*.md' -o -path '*/reference/*.json' -o -path '*/references/*.json' \) \
    -type f -print0 \
  | xargs -0 grep -hoE 'ohos-[a-z0-9-]+' || true
} | sort -u > "$tmp/references_raw.txt"

grep -E '^ohos-req-[a-z0-9-]+$' "$tmp/references_raw.txt" \
  | grep -v -x 'ohos-req-xxx' \
  | sort -u > "$tmp/references_req.txt" || true

grep -E '^ohos-[a-z0-9-]+$' "$tmp/references_raw.txt" \
  | grep -v -E '^(ohos-requirements-intake|ohos-delivery-kit|ohos-req-|ohos-req-xxx)$' \
  | sort -u > "$tmp/references_all.txt" || true

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
echo "declared=$(wc -l < "$tmp/declared.txt" | tr -d ' ') install=$(wc -l < "$tmp/install.txt" | tr -d ' ') registered=$(wc -l < "$tmp/registered.txt" | tr -d ' ') referenced=$(wc -l < "$tmp/references_req.txt" | tr -d ' ')"
cmp_sets "declared vs install-array" "$tmp/declared.txt" "$tmp/install.txt"

if [[ -s "$tmp/references_all.txt" ]]; then
  while IFS= read -r ref; do
    if ! grep -qx "$ref" "$tmp/registered.txt"; then
      rc=1
      echo "UNRESOLVED reference: $ref"
    fi
  done < "$tmp/references_all.txt"
fi

while IFS= read -r declared; do
  if ! grep -qx "$declared" "$tmp/registered.txt"; then
    rc=1
    echo "UNREGISTERED declared skill: $declared"
  fi
done < "$tmp/declared.txt"

legacy_odk_root=".codespec""/changes"
legacy_link_command="odk-link""-issue"
for token in "$legacy_odk_root" "$legacy_link_command"; do
  stale_matches="$(
    grep -RFn --include='*.md' --exclude-dir=evals --exclude-dir=examples \
      -- "$token" "$SKILLS_DIR" || true
  )"
  if [[ -n "$stale_matches" ]]; then
    rc=1
    echo "STALE ODK archive token: $token"
    echo "$stale_matches"
  fi
done

review_handoff="$SKILLS_DIR/../development/ohos-dev-gitcode-pr-review/references/reviewing-skill-prs.md"
flat_matches="$(python3 - "$SKILLS_DIR" "$review_handoff" <<'PY'
import pathlib
import re
import sys

roots = [pathlib.Path(raw) for raw in sys.argv[1:] if pathlib.Path(raw).exists()]
patterns = (
    re.compile(
        r"codespec/changes/(?:<req-id>|\{req-id\}|\$\{req_id\})-"
        r"(?:<english-slug>|\{english-slug\}|\$\{slug\})"
    ),
    re.compile(
        r"codespec/changes/draft-(?:<yyyymmdd>|\{yyyymmdd\}|\$\{yyyymmdd\})-"
        r"(?:<english-slug>|\{english-slug\}|\$\{slug\})"
    ),
    re.compile(
        r"codespec/changes/draft-[0-9]{8}-[a-z0-9]+(?:-[a-z0-9]+)*/"
        r"(?=$|[\s`'\"\)\]\}.,;:])"
    ),
    # Concrete formal examples conventionally use an uppercase/numeric req-id
    # followed by a lowercase English slug in the old single archive layer.
    re.compile(
        r"codespec/changes/(?:[A-Z0-9][A-Z0-9-]*[A-Z0-9]|[0-9]+)-"
        r"[a-z0-9]+(?:-[a-z0-9]+)*/(?=$|[\s`'\"\)\]\}.,;:])"
    ),
    # A proposal immediately below changes/ has only the old 0.8 archive layer;
    # ODK 0.9 always has <repo-name>/<req-id-or-draft>/proposal.md.
    re.compile(r"codespec/changes/[^/\s`]+/proposal\.md"),
)

for root in roots:
    files = [root] if root.is_file() else root.rglob("*.md")
    for path in files:
        if any(part in {"evals", "examples"} for part in path.parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as error:
            print(f"SCAN ERROR {path}: {error}")
            raise SystemExit(2)
        for number, line in enumerate(lines, 1):
            if any(pattern.search(line) for pattern in patterns):
                print(f"{path}:{number}:{line}")
PY
)" || {
  rc=1
  echo "ODK archive path semantic scan failed"
}
if [[ -n "$flat_matches" ]]; then
  rc=1
  while IFS= read -r match; do
    echo "STALE ODK 0.8 flat archive path: $match"
  done <<< "$flat_matches"
fi

if [[ "$rc" -eq 0 ]]; then
  echo "Result: CONSISTENT"
else
  echo "Result: INCONSISTENT — 修正 related-skills、install 数组、目录名、SKILL/reference 引用或旧 ODK 归档 token"
fi
exit "$rc"
