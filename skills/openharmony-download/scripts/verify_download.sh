#!/bin/bash
# OpenHarmony Download Verification Script
# This script verifies the completeness of OpenHarmony source code download

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}OpenHarmony 下载验证${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Counter
ISSUES=0
CHECKS=0

# Function to check directory
check_dir() {
    CHECKS=$((CHECKS + 1))
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 (缺失)"
        ISSUES=$((ISSUES + 1))
        return 1
    fi
}

# Function to check file
check_file() {
    CHECKS=$((CHECKS + 1))
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 (缺失)"
        ISSUES=$((ISSUES + 1))
        return 1
    fi
}

# Check if we're in OpenHarmony root
if [ ! -f ".repo/manifest.xml" ]; then
    echo -e "${RED}错误: 未找到 .repo/manifest.xml${NC}"
    echo "请确保在 OpenHarmony 根目录运行此脚本"
    exit 1
fi

echo "1. 检查顶层目录结构"
echo "--------------------"
check_dir "applications"
check_dir "base"
check_dir "build"
check_dir "docs"
check_dir "foundation"
check_dir "domains"
check_dir "drivers"
check_dir "kernel"
check_dir "prebuilts"
check_dir "test"
check_dir "third_party"
check_dir "vendor"
echo ""

echo "2. 检查 foundation 子系统"
echo "-------------------------"
check_dir "foundation/ability"
check_dir "foundation/arkui"
check_dir "foundation/appexecfwk"
check_dir "foundation/bundlemanager"
check_dir "foundation/communication"
check_dir "foundation/distributedhardware"
check_dir "foundation/graphic"
check_dir "foundation/multimedia"
check_dir "foundation/resourceschedule"
check_dir "foundation/security"
check_dir "foundation/startup"
echo ""

echo "3. 检查 ACE Engine"
echo "-------------------"
if check_dir "foundation/arkui/ace_engine"; then
    echo "  ACE Engine 子目录:"
    if [ -d "foundation/arkui/ace_engine/frameworks" ]; then
        echo -e "    ${GREEN}✓${NC} frameworks/"
    fi
    if [ -d "foundation/arkui/ace_engine/interfaces" ]; then
        echo -e "    ${GREEN}✓${NC} interfaces/"
    fi
    if [ -d "foundation/arkui/ace_engine/test" ]; then
        echo -e "    ${GREEN}✓${NC} test/"
    fi
fi
echo ""

echo "4. 检查关键文件"
echo "---------------"
check_file "build.py"
check_file ".repo/manifest.xml"
check_file ".repo/project.list"
echo ""

echo "5. 检查 repo 状态"
echo "-----------------"
if command -v repo &> /dev/null; then
    echo "repo 信息:"
    repo info | head -n 10
    echo ""

    echo "检查仓库状态..."
    UNCLEAN=$(repo status | grep -c "project.*status" || true)
    if [ "$UNCLEAN" -eq 0 ]; then
        echo -e "${GREEN}✓ 所有仓库状态干净${NC}"
    else
        echo -e "${YELLOW}⚠ $UNCLEAN 个仓库未清理${NC}"
        echo "运行 'repo status' 查看详情"
    fi
else
    echo -e "${YELLOW}⚠ repo 命令不可用${NC}"
fi
echo ""

echo "6. 检查磁盘空间"
echo "----------------"
DISK_USAGE=$(du -sh . 2>/dev/null | cut -f1)
echo "源码大小: $DISK_USAGE"

AVAILABLE=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
echo "可用空间: ${AVAILABLE}GB"

if [ "$AVAILABLE" -lt 20 ]; then
    echo -e "${YELLOW}⚠ 可用空间不足 20GB，编译可能失败${NC}"
    ISSUES=$((ISSUES + 1))
fi
echo ""

echo "7. 检查部分仓库完整性"
echo "----------------------"
if [ -f ".repo/project.list" ]; then
    TOTAL_REPOS=$(wc -l < .repo/project.list)
    echo "manifest 中定义的仓库总数: $TOTAL_REPOS"

    # Count actual repo directories
    REPO_COUNT=$(find . -type d -name ".git" | wc -l)
    echo "实际克隆的仓库数: $REPO_COUNT"

    if [ "$REPO_COUNT" -lt "$TOTAL_REPOS" ]; then
        echo -e "${YELLOW}⚠ 仓库数量不匹配，下载可能不完整${NC}"
        echo "建议运行: repo sync -c"
        ISSUES=$((ISSUES + 1))
    else
        echo -e "${GREEN}✓ 仓库数量匹配${NC}"
    fi
fi
echo ""

# Summary
echo -e "${BLUE}======================================${NC}"
echo "验证摘要"
echo -e "${BLUE}======================================${NC}"
echo "总检查项: $CHECKS"
echo -e "发现问题: ${RED}$ISSUES${NC}"
echo ""

if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✓ 验证通过！OpenHarmony 源码完整。${NC}"
    echo ""
    echo "后续步骤:"
    echo "1. 配置编译环境"
    echo "2. 编译代码: ./build.sh --product-name rk3568 --build-target ohos"
    echo "3. 阅读 docs/ 目录中的文档"
    exit 0
else
    echo -e "${RED}✗ 验证失败，发现 $ISSUES 个问题${NC}"
    echo ""
    echo "建议:"
    echo "1. 运行 'repo sync -c' 同步缺失的仓库"
    echo "2. 运行 'repo forall -c \"git lfs pull\"' 拉取 LFS 文件"
    echo "3. 检查网络连接"
    echo "4. 查看详细状态: repo status"
    exit 1
fi
