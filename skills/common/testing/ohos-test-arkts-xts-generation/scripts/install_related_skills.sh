#!/usr/bin/env bash
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_MD="${SKILL_ROOT}/SKILL.md"
SKILLS_DIR="${HOME}/.opencode/skills"
CACHE_DIR="${HOME}/.cache/oh-xts-skills"
PROBE_RESULTS="${SKILL_ROOT}/.probe_results"
PARSE_CACHE="${SKILL_ROOT}/.parse_cache"

# ==================== Parse SKILL.md frontmatter ====================
# Output: one line per skill, fields separated by |
#   name|min_version|required|probe_count
# Probes written to .parse_cache/probes/{name}.txt (one per line)

parse_related_skills() {
  mkdir -p "${PARSE_CACHE}/probes"
  local in_block=0 in_rs=0 cur_name="" cur_mv="" cur_req="false"
  local probe_file="" probe_count=0
  while IFS= read -r line; do
    if [[ "$line" =~ ^---$ ]]; then
      ((in_block++)) || true
      if (( in_block == 2 )); then
        if [[ -n "$cur_name" ]]; then
          echo "${cur_name}|${cur_mv:-}|${cur_req:-false}|${probe_count}"
          cur_name=""
        fi
        break
      fi
      continue
    fi
    (( in_block != 1 )) && continue
    if [[ "$line" =~ ^[[:space:]]*related-skills: ]]; then
      in_rs=1
      continue
    fi
    (( in_rs )) || continue

    # End of related-skills block: non-indented or non-list non-property line
    if [[ ! "$line" =~ ^[[:space:]]+- ]] && [[ ! "$line" =~ ^[[:space:]]+[a-z_] ]]; then
      if [[ -n "$cur_name" ]]; then
        echo "${cur_name}|${cur_mv:-}|${cur_req:-false}|${probe_count}"
        cur_name=""
      fi
      in_rs=0
      continue
    fi

    # New skill entry: - name: xxx
    if [[ "$line" =~ ^[[:space:]]+-[[:space:]]name:[[:space:]]*(.+)$ ]]; then
      if [[ -n "$cur_name" ]]; then
        echo "${cur_name}|${cur_mv:-}|${cur_req:-false}|${probe_count}"
      fi
      cur_name="${BASH_REMATCH[1]}"
      cur_mv=""
      cur_req="false"
      probe_count=0
      probe_file="${PARSE_CACHE}/probes/${cur_name}.txt"
      : > "$probe_file" 2>/dev/null || true
      continue
    fi

    # Property: required
    if [[ "$line" =~ ^[[:space:]]+required:[[:space:]]*(.+)$ ]]; then
      cur_req="${BASH_REMATCH[1]}"
      continue
    fi

    # Property: min_version
    if [[ "$line" =~ min_version: ]]; then
      if [[ "$line" =~ min_version:[[:space:]]*\"?([0-9][0-9a-zA-Z._-]*)\"? ]]; then
        cur_mv="${BASH_REMATCH[1]}"
      fi
      continue
    fi

    # Skip probes: header
    if [[ "$line" =~ ^[[:space:]]+probes: ]]; then
      continue
    fi

    # Probe entry: - "command"
    if [[ "$line" =~ ^[[:space:]]+-[[:space:]]*\"(.+)\"[[:space:]]*$ ]]; then
      if [[ -n "$cur_name" ]]; then
        echo "${BASH_REMATCH[1]}" >> "$probe_file"
        ((probe_count++)) || true
      fi
      continue
    fi
  done < "$SKILL_MD"
  # Last entry (if YAML block didn't end with ---)
  if [[ -n "$cur_name" ]]; then
    echo "${cur_name}|${cur_mv:-}|${cur_req:-false}|${probe_count}"
  fi
}

parse_main_version() {
  local in_block=0
  while IFS= read -r line; do
    if [[ "$line" =~ ^---$ ]]; then
      ((in_block++)) || true
      (( in_block >= 2 )) && break
      continue
    fi
    (( in_block == 1 )) || continue
    if [[ "$line" =~ ^[[:space:]]*version:[[:space:]]*\"?([0-9][0-9a-zA-Z._-]*)\"? ]]; then
      echo "${BASH_REMATCH[1]}"
      return
    fi
  done < "$SKILL_MD"
  echo "unknown"
}

# ==================== Version comparison ====================

version_gte() {
  local v1="$1" v2="$2"
  [[ "$v1" == "$v2" ]] && return 0
  local IFS=.
  local i a1=($v1) a2=($v2)
  for ((i=0; i<${#a1[@]} || i<${#a2[@]}; i++)); do
    local p1="${a1[i]:-0}" p2="${a2[i]:-0}"
    ((10#$p1 > 10#$p2)) && return 0
    ((10#$p1 < 10#$p2)) && return 1
  done
  return 0
}

# ==================== Skill version detection ====================

get_skill_version() {
  local name="$1"
  local dir="${SKILLS_DIR}/${name}"
  if [ -f "${dir}/SKILL.md" ]; then
    local v
    v=$(awk '/^---/{c++;next} c==1 && /^[[:space:]]*version:/{gsub(/["'"'"']/,""); print $2; exit}' "${dir}/SKILL.md" 2>/dev/null || true)
    if [[ -n "$v" && "$v" != "" ]]; then
      echo "$v"
      return
    fi
  fi
  if [ -f "${dir}/.install-source" ]; then
    local commit
    commit=$(grep '^commit=' "${dir}/.install-source" 2>/dev/null | cut -d= -f2 || true)
    [[ -n "$commit" ]] && echo "commit:${commit}" && return
  fi
  echo "unknown"
}

# ==================== Probes ====================

run_probes() {
  local name="$1" probe_count="$2"
  local dir="${SKILLS_DIR}/${name}"
  local probe_file="${PARSE_CACHE}/probes/${name}.txt"
  local pass=0 fail_details=""

  if [[ "$probe_count" -eq 0 ]] || [[ ! -f "$probe_file" ]]; then
    echo "0|0|"
    return
  fi

  while IFS= read -r probe; do
    [[ -z "$probe" ]] && continue
    local cmd="${probe//\{dir\}/${dir}}"
    if eval "$cmd" >/dev/null 2>&1; then
      ((pass++)) || true
    else
      local safe_cmd
      safe_cmd=$(echo "$cmd" | sed 's|.opencode/skills|…/skills|')
      fail_details="${fail_details}    FAIL: ${safe_cmd}"$'\n'
    fi
  done < "$probe_file"

  local total
  total=$(grep -c '.' "$probe_file" 2>/dev/null || echo "$probe_count")
  echo "${pass}|${total}|${fail_details}"
}

# ==================== Colors ====================

BLUE='\033[0;34m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; RED='\033[0;31m'; NC='\033[0m'
log_info()  { printf "${BLUE}[INFO]${NC} %s\n" "$1"; }
log_ok()    { printf "${GREEN}[OK]${NC} %s\n" "$1"; }
log_warn()  { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; }
log_error() { printf "${RED}[ERROR]${NC} %s\n" "$1"; }

# ==================== Remote sources ====================

declare -A SKILL_REMOTE=(
  ["ohos-test-xts-code-quality"]="https://gitcode.com/openharmony-sig/compatibility.git|master|test_suite/resource/skills_XTS/ohos-test-xts-code-quality"
  ["ohos-dev-arkts-static-specification-reference"]="https://gitcode.com/openharmonyinsight/openharmony-skills.git|release|skills/common/development/ohos-dev-arkts-static-specification-reference"
  ["arkts-skill"]="https://gitcode.com/Maxi_241437/arkts-skills.git|main|skills/arkts-skill"
  ["demo-pipeline"]="https://gitcode.com/openharmony-ai-testdesign/oh-test-skills.git|main|ohos-test-design/skills/demo-pipeline"
)

declare -A SKILL_LOCAL_FALLBACK=(
  ["ohos-test-xts-code-quality"]="${HOME}/openharmony-skills_4397/skills/common/testing/ohos-test-xts-code-quality"
  ["ohos-dev-arkts-static-specification-reference"]="${HOME}/openharmony-skills_4397/skills/common/development/ohos-dev-arkts-static-specification-reference"
  ["arkts-skill"]="${HOME}/arkts-skills/skills/arkts-skill"
  ["demo-pipeline"]="${HOME}/oh-test-skills/ohos-test-design/skills/demo-pipeline"
)

# ==================== Install functions ====================

check_installed() {
  [ -f "${SKILLS_DIR}/${1}/SKILL.md" ]
}

resolve_source() {
  local name="$1"
  local local_path="${SKILL_LOCAL_FALLBACK[$name]:-}"
  if [ -n "$local_path" ] && [ -f "${local_path}/SKILL.md" ]; then
    echo "local|${local_path}"
    return 0
  fi
  local remote="${SKILL_REMOTE[$name]:-}"
  if [[ -z "$remote" ]]; then
    log_error "${name}: 无本地源也无远程源配置"
    return 1
  fi
  local repo_url="${remote%%|*}"
  local rest="${remote#*|}"
  local branch="${rest%%|*}"
  local subpath="${rest#*|}"
  local repo_hash
  repo_hash=$(echo -n "${repo_url}" | sha256sum | cut -c1-12)
  local clone_dir="${CACHE_DIR}/${repo_hash}"
  if [ ! -d "${clone_dir}/.git" ]; then
    log_info "克隆 ${repo_url} (branch: ${branch})..."
    mkdir -p "${CACHE_DIR}"
    git clone --depth 1 --branch "${branch}" "${repo_url}" "${clone_dir}" 2>&1 | sed 's/^/  /'
  else
    log_info "更新缓存 ${repo_url}..."
    (cd "${clone_dir}" && git fetch --depth 1 origin "${branch}" 2>&1 && git reset --hard "origin/${branch}" 2>&1) | sed 's/^/  /'
  fi
  local source_path="${clone_dir}/${subpath}"
  if [ ! -f "${source_path}/SKILL.md" ]; then
    log_error "${name}: SKILL.md not found at ${source_path}"
    return 1
  fi
  local commit
  commit=$(cd "${clone_dir}" && git rev-parse --short HEAD)
  echo "remote|${source_path}|${repo_url}|${branch}|${commit}"
}

install_skill() {
  local name="$1" source_type="$2"
  shift 2
  local target="${SKILLS_DIR}/${name}"
  if [[ "$FORCE" == "1" ]] && check_installed "$name"; then
    log_info "强制重新安装 ${name}（覆盖已有）"
    rm -rf "${target}"
  fi
  local source_path="$1"
  log_info "安装 ${name} ← ${source_path}"
  mkdir -p "${target}"
  rsync -a --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' \
    "${source_path}/" "${target}/"
  local manifest="${target}/.install-source"
  if [ "${source_type}" == "local" ]; then
    { echo "source=local"; echo "path=${source_path}"; echo "installed=$(date -Iseconds)"; } > "${manifest}"
  else
    { echo "source=remote"; echo "repo=${2:-}"; echo "branch=${3:-}"; echo "commit=${4:-}"; echo "installed=$(date -Iseconds)"; } > "${manifest}"
  fi
  if check_installed "$name"; then
    log_ok "${name} 安装成功"
    return 0
  else
    log_error "${name} 安装失败（SKILL.md 未找到）"
    return 1
  fi
}

# ==================== Check functions ====================

do_check_probes() {
  local entries
  entries=$(parse_related_skills)
  local ok=0 warn=0 fail=0 missing=0

  echo "# Generated by install_related_skills.sh at $(date -Iseconds)" > "$PROBE_RESULTS"
  echo "# format: name|status|version|probe_pass/probe_total|detail" >> "$PROBE_RESULTS"

  while IFS='|' read -r name min_ver required probe_count; do
    [[ -z "$name" ]] && continue
    local desc=""
    case "$name" in
      ohos-test-xts-code-quality) desc="代码质量深度扫描（Phase 7B 必选）" ;;
      ohos-dev-arkts-static-specification-reference) desc="ArkTS 静态语法规范校验（Phase 7A）" ;;
      arkts-skill) desc="ArkTS 动态语法/API 按需检索（Phase 3/8）" ;;
      demo-pipeline) desc="Demo 被测应用生成（Phase 5A）" ;;
      *) desc="$name" ;;
    esac

    if ! check_installed "$name"; then
      if [[ "$required" == "true" ]]; then
        log_error "✗ ${name} — 未安装（必选，${desc}）"
        echo "${name}|MISSING|-|0/0|required but not installed" >> "$PROBE_RESULTS"
        ((fail++)) || true
      else
        log_warn "✗ ${name} — 未安装（可选，${desc}）"
        echo "${name}|MISSING_OPTIONAL|-|0/0|optional, not installed" >> "$PROBE_RESULTS"
        ((missing++)) || true
      fi
      continue
    fi

    local inst_ver
    inst_ver=$(get_skill_version "$name")

    # Version check
    if [[ -n "$min_ver" && "$min_ver" != "" ]]; then
      if [[ "$inst_ver" == "unknown" || "$inst_ver" == commit:* ]]; then
        : # rely on probes
      elif ! version_gte "$inst_ver" "$min_ver"; then
        log_error "✗ ${name} — 版本过低: ${inst_ver} < ${min_ver}（${desc}）"
        echo "${name}|VERSION_LOW|${inst_ver}|0/0|need >= ${min_ver}" >> "$PROBE_RESULTS"
        ((fail++)) || true
        continue
      fi
    fi

    # Probe check
    if [[ "$probe_count" -gt 0 ]]; then
      local probe_result
      probe_result=$(run_probes "$name" "$probe_count")
      local p_pass="${probe_result%%|*}"
      local rest="${probe_result#*|}"
      local p_total="${rest%%|*}"
      local p_fails="${rest#*|}"

      if [[ "$p_pass" == "$p_total" ]]; then
        if [[ "$inst_ver" == "unknown" || "$inst_ver" == commit:* ]]; then
          log_warn "⚠ ${name} (${inst_ver}) — 探测全通过，版本未知（${desc}）"
          echo "${name}|WARN_VERSION|${inst_ver}|${p_pass}/${p_total}|version unknown but probes pass" >> "$PROBE_RESULTS"
          ((warn++)) || true
        else
          log_ok "✓ ${name} (${inst_ver}) — 探测 ${p_pass}/${p_total} 通过（${desc}）"
          echo "${name}|OK|${inst_ver}|${p_pass}/${p_total}|" >> "$PROBE_RESULTS"
          ((ok++)) || true
        fi
      else
        printf "${RED}[FAIL]${NC} %s (%s) — 探测 %s/%s 通过（%s）\n" "$name" "$inst_ver" "$p_pass" "$p_total" "$desc"
        printf "%b" "$p_fails"
        echo "${name}|FAIL_PROBES|${inst_ver}|${p_pass}/${p_total}|probes failed" >> "$PROBE_RESULTS"
        ((fail++)) || true
      fi
    else
      if [[ "$inst_ver" == "unknown" ]]; then
        log_warn "⚠ ${name} — 已安装，无探测规则，版本未知（${desc}）"
        echo "${name}|WARN_VERSION|${inst_ver}|-/-|no probes, version unknown" >> "$PROBE_RESULTS"
        ((warn++)) || true
      else
        log_ok "✓ ${name} (${inst_ver}) — 已安装，无探测规则（${desc}）"
        echo "${name}|OK|${inst_ver}|-/-|no probes defined" >> "$PROBE_RESULTS"
        ((ok++)) || true
      fi
    fi
  done <<< "$entries"

  echo ""
  printf "检查结果: %d 通过, %d 警告, %d 失败, %d 未安装(可选)\n" "$ok" "$warn" "$fail" "$missing"
  echo ""
  log_info "探测结果已写入: ${PROBE_RESULTS}"

  (( fail > 0 )) && return 1 || return 0
}

# ==================== Main ====================

INSTALL_MODE="missing"
FORCE=0
VERBOSE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)          INSTALL_MODE="all" ;;
    --force)        FORCE=1 ;;
    --check)        INSTALL_MODE="check" ;;
    --check-probes) INSTALL_MODE="check_probes" ;;
    --verbose|-v)   VERBOSE=1 ;;
    --help|-h)
      local main_ver
      main_ver=$(parse_main_version)
      cat <<HELP
Usage: install_related_skills.sh [options]

Options:
  --all            安装全部依赖 skill（包括已安装的）
  --force          强制重新安装（覆盖已有）
  --check          仅检查安装状态，不安装
  --check-probes   检查版本兼容性 + 能力探测（生成 .probe_results）
  --verbose        显示详细信息
  --help           显示帮助

默认行为：仅安装缺失的 skill，安装后自动执行 probes

主 skill 版本: ${main_ver}
HELP
      exit 0
      ;;
    *) log_error "未知选项: $1"; exit 1 ;;
  esac
  shift
done

if [[ "$INSTALL_MODE" == "check_probes" ]]; then
  do_check_probes
  exit $?
fi

if [ ! -d "$SKILLS_DIR" ]; then
  log_info "创建 skill 安装目录: ${SKILLS_DIR}"
  mkdir -p "$SKILLS_DIR"
fi

log_info "Skill 安装目录: ${SKILLS_DIR}"

entries=$(parse_related_skills)

INSTALLED=0 MISSING=0 FAILED=0

while IFS='|' read -r name min_ver required probe_count; do
  [[ -z "$name" ]] && continue

  if check_installed "$name" && [[ "$INSTALL_MODE" != "all" ]] && [[ "$FORCE" != "1" ]]; then
    log_ok "✓ ${name} — 已安装"
    ((INSTALLED++)) || true
    continue
  fi

  if [[ "$INSTALL_MODE" == "check" ]]; then
    log_warn "✗ ${name} — 未安装"
    ((MISSING++)) || true
    continue
  fi

  resolved=$(resolve_source "$name") || {
    log_error "${name}: 无法获取源（本地和远程均失败）"
    ((FAILED++)) || true
    continue
  }

  source_type="${resolved%%|*}"
  rest="${resolved#*|}"

  if [[ "${source_type}" == "local" ]]; then
    source_path="${rest}"
    if install_skill "$name" "local" "${source_path}"; then
      ((INSTALLED++)) || true
    else
      ((FAILED++)) || true
    fi
  else
    source_path="${rest%%|*}"
    rest2="${rest#*|}"
    repo_url="${rest2%%|*}"
    rest3="${rest2#*|}"
    branch="${rest3%%|*}"
    commit="${rest3#*|}"
    if install_skill "$name" "remote" "${source_path}" "${repo_url}" "${branch}" "${commit}"; then
      ((INSTALLED++)) || true
    else
      ((FAILED++)) || true
    fi
  fi
done <<< "$entries"

echo ""

if [[ "$INSTALL_MODE" == "check" ]]; then
  printf "检查结果: %d 已安装, %d 缺失, %d 失败\n" "$INSTALLED" "$MISSING" "$FAILED"
  if (( MISSING > 0 || FAILED > 0 )); then
    echo ""
    log_info "运行以下命令安装缺失的 skill:"
    echo "  bash ${SKILL_ROOT}/scripts/install_related_skills.sh"
    exit 1
  fi
else
  printf "安装结果: %d 已安装, %d 失败\n" "$INSTALLED" "$FAILED"
  if (( INSTALLED > 0 && FAILED == 0 )); then
    echo ""
    log_info "运行兼容性探测..."
    do_check_probes
  fi
fi

(( FAILED > 0 )) && exit 1 || exit 0
