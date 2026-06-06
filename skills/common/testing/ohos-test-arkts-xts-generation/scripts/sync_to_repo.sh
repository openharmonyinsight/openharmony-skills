#!/bin/bash
# sync_to_repo.sh - 将工作目录的内容同步回 Git 发布仓库
#
# 用法:
#   ./sync_to_repo.sh              # 同步并查看差异（不提交）
#   ./sync_to_repo.sh --commit     # 同步 + 提交
#   ./sync_to_repo.sh --push       # 同步 + 提交 + 推送
#   ./sync_to_repo.sh --dry-run    # 仅预览，不同步文件
#
# 同步源 → 目标:
#   agents/ohos-arkts-xts-agent/   → repo/ohos-arkts-xts-agent/
#   ~/oh-test-knowledge/           → repo/knowledge/
#   skills/{3个skill}/             → repo/skills/{3个skill}/

set -euo pipefail

# ==================== 路径配置 ====================
AGENT_SRC="$HOME/.opencode/agents/ohos-arkts-xts-agent"
KNOWLEDGE_SRC="$HOME/oh-test-knowledge"
SKILLS_SRC="$HOME/.opencode/skills"
REPO_DIR="/tmp/ohos-test-xts-generation-agent"

SKILLS_LIST=("arkts-static-spec" "check-test-code-quality" "demo-pipeline")

# ==================== 参数解析 ====================
ACTION="sync"
DRY_RUN=false
SYNC_AGENT=true
SYNC_KNOWLEDGE=false
SYNC_SKILLS=false
COMMIT_MSG=""

for arg in "$@"; do
    case "$arg" in
        --commit)   ACTION="commit" ;;
        --push)     ACTION="push" ;;
        --dry-run)  DRY_RUN=true ;;
        --all)      SYNC_KNOWLEDGE=true; SYNC_SKILLS=true ;;
        --knowledge) SYNC_KNOWLEDGE=true ;;
        --skills)   SYNC_SKILLS=true ;;
        --msg=*)    COMMIT_MSG="${arg#--msg=}" ;;
        --help|-h)
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  --commit       同步后自动 git commit"
            echo "  --push         同步后自动 git commit && git push"
            echo "  --dry-run      仅预览差异，不同步文件"
            echo "  --all          同步 agent + knowledge + skills"
            echo "  --knowledge    同步知识库"
            echo "  --skills       同步依赖的 skills"
            echo "  --msg=MSG      指定提交信息"
            echo "  -h, --help     显示帮助"
            exit 0
            ;;
        *)
            echo "未知参数: $arg"
            exit 1
            ;;
    esac
done

# ==================== 颜色 ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ==================== 工具函数 ====================
log_info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_err()   { echo -e "${RED}[ERROR]${NC} $1"; }

check_dir() {
    if [ ! -d "$1" ]; then
        log_err "目录不存在: $1"
        return 1
    fi
}

# rsync 排除运行时文件
RSYNC_EXCLUDES=(
    --exclude='.git'
    --exclude='.coverage_data'
    --exclude='.task_summary'
    --exclude='.oh-xts-config.json'
    --exclude='__pycache__'
    --exclude='*.pyc'
    --exclude='*.log'
    --exclude='EVALUATION_REPORT.md'
    --exclude='.git'
    --exclude='node_modules'
    --exclude='.venv'
    --exclude='venv'
)

rsync_sync() {
    local src="$1"
    local dst="$2"
    local label="$3"

    if [ ! -d "$src" ]; then
        log_warn "$label 源目录不存在，跳过: $src"
        return 0
    fi

    if [ ! -d "$dst" ]; then
        log_warn "$label 目标目录不存在，跳过: $dst"
        return 0
    fi

    local rsync_args=(-av --delete "${RSYNC_EXCLUDES[@]}")

    if $DRY_RUN; then
        rsync_args+=(--dry-run)
    fi

    log_info "同步 $label ..."
    rsync "${rsync_args[@]}" "$src" "$dst/" 2>&1 | grep -E '^(sending|deleting|sent|total)' || true
    log_ok "$label 同步完成"
}

# ==================== 前置检查 ====================
check_dir "$REPO_DIR" || exit 1
check_dir "$AGENT_SRC" || exit 1

cd "$REPO_DIR"

log_info "Repo 目录: $REPO_DIR"
log_info "Agent 源:  $AGENT_SRC"
log_info "知识库源:  $KNOWLEDGE_SRC"
log_info "Skills 源: $SKILLS_SRC"
echo ""

# ==================== 1. 同步 Agent ====================
if $SYNC_AGENT; then
    rsync_sync "$AGENT_SRC/" "$REPO_DIR/ohos-arkts-xts-agent" "Agent"
fi

# ==================== 2. 同步 Knowledge ====================
if $SYNC_KNOWLEDGE; then
    rsync_sync "$KNOWLEDGE_SRC/" "$REPO_DIR/knowledge" "Knowledge"
fi

# ==================== 3. 同步 Skills ====================
if $SYNC_SKILLS; then
    for skill in "${SKILLS_LIST[@]}"; do
        rsync_sync "$SKILLS_SRC/$skill/" "$REPO_DIR/skills/$skill" "Skill/$skill"
    done
fi

# ==================== 4. 显示差异 ====================
echo ""
log_info "===== Git Diff 概览 ====="

if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
    if [ -z "$(git ls-files --others --exclude-standard)" ]; then
        log_ok "无差异，工作目录与 repo 完全一致"
        exit 0
    fi
fi

echo ""
git diff --stat 2>/dev/null || true
git diff --cached --stat 2>/dev/null || true

untracked=$(git ls-files --others --exclude-standard 2>/dev/null)
if [ -n "$untracked" ]; then
    echo ""
    log_info "新增文件:"
    echo "$untracked" | sed 's/^/  + /'
fi

if [ "$ACTION" = "sync" ] || $DRY_RUN; then
    echo ""
    if $DRY_RUN; then
        log_info "预览模式（--dry-run），未执行任何操作"
    else
        log_info "文件已同步到 repo，但未提交。使用 --commit 或 --push 提交。"
    fi
    exit 0
fi

# ==================== 5. 提交 ====================
echo ""
git add -A

if [ -z "$(git diff --cached --name-only)" ]; then
    log_ok "无变更需要提交"
    exit 0
fi

changed_files=$(git diff --cached --name-only)
changed_count=$(echo "$changed_files" | wc -l)

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="sync: update from working directory ($changed_count files)"
fi

log_info "提交 $changed_count 个文件: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"
log_ok "提交成功"

# ==================== 6. 推送 ====================
if [ "$ACTION" = "push" ]; then
    log_info "推送到远端 ..."
    git push origin "$(git branch --show-current)"
    log_ok "推送完成"
fi

echo ""
log_ok "完成!"
