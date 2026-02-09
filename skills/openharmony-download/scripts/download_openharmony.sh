#!/bin/bash
# OpenHarmony Download Script
# Pure execution mode - all parameters passed via command line
# Claude collects information through conversation, then calls this script
# Download runs in foreground with real-time progress output

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print usage
print_usage() {
    cat << EOF
使用方法: $0 -m MIRROR -b BRANCH [-d DIR] [-j JOBS]

必需参数:
  -m, --mirror MIRROR       镜像源 (gitcode|gitee|github)
  -b, --branch BRANCH       分支名 (例如: master, OpenHarmony-5.0.1-Release)

可选参数:
  -d, --dir DIR             下载目录（绝对路径，默认: ~/OpenHarmony/<branch>/）
  -j, --jobs N              并行任务数（默认: CPU核心数/4）
  -h, --help                显示此帮助信息

镜像源说明:
  gitcode   GitCode 镜像（中国用户推荐）
  gitee     Gitee 镜像（中国用户）
  github    GitHub 镜像（国际用户）

常用分支:
  master                    主分支（最新开发代码）
  OpenHarmony-5.1.0-Release 5.1.0 版本
  OpenHarmony-5.0.3-Release 5.0.3 版本
  OpenHarmony-5.0.2-Release 5.0.2 版本
  OpenHarmony-5.0.1-Release 5.0.1 版本
  OpenHarmony-4.1-Release    4.1 版本

示例:
  $0 -m gitcode -b master
  $0 -m github -b OpenHarmony-5.0.1-Release -d /opt/openharmony
  $0 -m gitee -b master -j 32

EOF
}

# Initialize variables
MIRROR=""
BRANCH=""
CUSTOM_DIR=""
DEFAULT_BASE_DIR="$HOME/OpenHarmony"

# Auto-detect optimal jobs based on CPU cores (1/4 of CPU cores)
CPU_CORES=$(nproc 2>/dev/null || echo 4)
if [ -z "$CPU_CORES" ] || [ "$CPU_CORES" -lt 1 ]; then
    CPU_CORES=4
fi
DEFAULT_JOBS=$((CPU_CORES / 4))
if [ "$DEFAULT_JOBS" -lt 1 ]; then
    DEFAULT_JOBS=1
fi
JOBS="$DEFAULT_JOBS"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--mirror)
            MIRROR="$2"
            shift 2
            ;;
        -b|--branch)
            BRANCH="$2"
            shift 2
            ;;
        -j|--jobs)
            JOBS="$2"
            shift 2
            ;;
        -d|--dir)
            CUSTOM_DIR="$2"
            shift 2
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo "错误: 未知参数 $1"
            echo ""
            print_usage
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$MIRROR" ]; then
    echo -e "${RED}错误: 必须指定镜像源 (-m)${NC}"
    echo "支持的镜像源: gitcode, gitee, github"
    echo ""
    print_usage
    exit 1
fi

if [ -z "$BRANCH" ]; then
    echo -e "${RED}错误: 必须指定分支 (-b)${NC}"
    echo "常用分支: master, OpenHarmony-5.1.0-Release, OpenHarmony-5.0.3-Release, etc."
    echo ""
    print_usage
    exit 1
fi

# Validate mirror value
if [[ "$MIRROR" != "gitcode" ]] && [[ "$MIRROR" != "gitee" ]] && [[ "$MIRROR" != "github" ]]; then
    echo -e "${RED}错误: 不支持的镜像源 '$MIRROR'${NC}"
    echo "支持的镜像源: gitcode, gitee, github"
    exit 1
fi

# Mirror URLs
declare -A MIRROR_URLS
MIRROR_URLS[gitcode]="https://gitcode.com/openharmony/manifest.git"
MIRROR_URLS[gitee]="https://gitee.com/openharmony/manifest.git"
MIRROR_URLS[github]="https://github.com/openharmony/manifest.git"

MANIFEST_URL="${MIRROR_URLS[$MIRROR]}"

# Show download configuration
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}OpenHarmony 源码下载${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo "镜像源: $MIRROR ($MANIFEST_URL)"
echo "分支: $BRANCH"
echo "CPU 核心数: $CPU_CORES"
echo "并行任务: $JOBS ${GREEN}(自动计算: CPU核心数/4)${NC}"
echo ""

# Determine download directory
if [ -n "$CUSTOM_DIR" ]; then
    DOWNLOAD_DIR="$CUSTOM_DIR"
    echo -e "${GREEN}使用自定义下载目录: $DOWNLOAD_DIR${NC}"
else
    DOWNLOAD_DIR="$DEFAULT_BASE_DIR/$BRANCH"
    echo -e "${BLUE}使用默认下载目录: $DOWNLOAD_DIR${NC}"
fi

echo ""
echo -e "${BLUE}下载目标目录: ${GREEN}$DOWNLOAD_DIR${NC}"
echo ""

# Create directory if it doesn't exist
if [ ! -d "$DOWNLOAD_DIR" ]; then
    echo -e "${YELLOW}创建下载目录...${NC}"
    mkdir -p "$DOWNLOAD_DIR"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 目录创建成功${NC}"
    else
        echo -e "${RED}✗ 目录创建失败${NC}"
        echo "请检查权限和路径"
        exit 1
    fi
else
    echo -e "${YELLOW}目录已存在${NC}"
fi

# Navigate to download directory
echo -e "${YELLOW}进入下载目录...${NC}"
cd "$DOWNLOAD_DIR"
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ 无法进入目录${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 当前目录: $(pwd)${NC}"
echo ""

# Check if we're in an OpenHarmony directory
if [ -f ".repo/manifest.xml" ]; then
    echo -e "${YELLOW}警告: 检测到已存在的 .repo 目录${NC}"
    echo "当前目录可能已经包含 OpenHarmony 源码"
    echo -e "${YELLOW}将删除旧的 .repo 目录并重新初始化${NC}"
    rm -rf .repo
    echo -e "${GREEN}✓ 已删除旧的 .repo 目录${NC}"
fi

# Step 1: Initialize repo
echo ""
echo -e "${BLUE}步骤 1/4: 初始化 repo${NC}"
echo "----------------------"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v repo &> /dev/null; then
    echo -e "${YELLOW}repo 工具未安装，尝试安装...${NC}"
    mkdir -p ~/bin
    curl https://raw.gitcode.com/gitcode-dev/repo/raw/main/repo-py3 -o ~/bin/repo
    chmod a+x ~/bin/repo
    export PATH=~/bin:$PATH
    pip3 install -i https://repo.huaweicloud.com/repository/pypi/simple requests
    echo -e "${GREEN}✓ repo 工具安装完成${NC}"
fi

echo "初始化 manifest..."
echo "  镜像: $MANIFEST_URL"
echo "  分支: $BRANCH"

if repo init -u "$MANIFEST_URL" -b "$BRANCH" --no-repo-verify; then
    echo -e "${GREEN}✓ repo 初始化成功${NC}"
else
    echo -e "${RED}✗ repo 初始化失败${NC}"
    exit 1
fi

# Step 2: Sync source code
echo ""
echo -e "${BLUE}步骤 2/4: 同步源码${NC}"
echo "------------------------------"
echo -e "${YELLOW}这将需要 15 分钟到数小时，取决于网络速度${NC}"
echo "源码大小: 30-40GB"
echo -e "${GREEN}并行任务: $JOBS (基于 $CPU_CORES CPU 核心)${NC}"
echo ""

# Start repo sync
echo "开始同步（使用 $JOBS 个并行任务）..."
repo sync -c --jobs="$JOBS"
echo $REPO_PID > .download.pid
echo -e "${GREEN}✓ 下载任务已启动 (PID: $REPO_PID)${NC}"
echo ""

# Wait to ensure sync is progressing
sleep 3

# Step 3: Pull LFS files
echo ""
echo -e "${BLUE}步骤 3/4: 拉取 LFS 文件${NC}"
echo "------------------------"
echo "拉取大文件（工具链、二进制依赖等）..."
echo ""

if repo forall -c 'git lfs pull'; then
    echo -e "${GREEN}✓ LFS 文件拉取成功${NC}"
else
    echo -e "${YELLOW}⚠ LFS 文件拉取出现问题${NC}"
    echo "部分仓库可能缺少 git-lfs 依赖"
    echo "您可以稍后手动运行: repo forall -c 'git lfs pull'"
fi

# Step 4: Verification
echo ""
echo -e "${BLUE}步骤 4/4: 验证下载${NC}"
echo "------------------------"
echo "验证下载完整性..."

if [ -f "$SCRIPT_DIR/verify_download.sh" ]; then
    bash "$SCRIPT_DIR/verify_download.sh" || echo -e "${YELLOW}⚠ 验证脚本执行完成，请检查输出${NC}"
else
    echo -e "${YELLOW}⚠ 验证脚本未找到，跳过自动验证${NC}"
fi

# Success message
echo ""
echo -e "${BLUE}======================================${NC}"
echo -e "${GREEN}✓ OpenHarmony 源码下载完成！${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo "下载摘要:"
echo "  镜像源: $MIRROR"
echo "  分支: $BRANCH"
echo "  下载目录: $(pwd)"
echo ""
echo "后续步骤:"
echo "1. 配置编译环境"
echo "2. 全量编译代码: ./build.sh --product-name rk3568 --ccache"
echo "3. 查看文档: cat docs/README.md"
echo ""
