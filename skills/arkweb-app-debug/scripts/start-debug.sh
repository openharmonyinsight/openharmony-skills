#!/bin/bash
#
# ArkWeb App Debug Tool - Quick Start Script
# 自动使用 ohos-app-build-debug 检测到的环境启动调试
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}ArkWeb App Debug Tool - Quick Start${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# 查找 ohos-app-build-debug
OHOS_SKILL="${HOME}/.claude/skills/ohos-app-build-debug"

if [ ! -d "$OHOS_SKILL" ]; then
    echo -e "${RED}❌ ohos-app-build-debug skill not found${NC}"
    echo -e "${YELLOW}Please install ohos-app-build-debug skill first:${NC}"
    echo "  https://gitcode.com/openharmony/openharmony-skills"
    exit 1
fi

echo -e "${GREEN}✓ Found ohos-app-build-debug skill${NC}"

# 检查 DevEco Studio 环境
echo -e "${BLUE}🔍 Checking DevEco Studio environment...${NC}"

ENV_OUTPUT=$("$OHOS_SKILL/ohos-app-build-debug" env 2>&1)

if echo "$ENV_OUTPUT" | grep -q "未检测到 DevEco Studio"; then
    echo -e "${RED}❌ DevEco Studio not detected${NC}"
    echo -e "${YELLOW}Please install DevEco Studio first:${NC}"
    echo "  https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download"
    exit 1
fi

echo -e "${GREEN}✓ DevEco Studio detected${NC}"

# 提取环境变量
echo -e "${BLUE}🔧 Setting up environment...${NC}"

# 解析环境检测结果获取工具路径
TOOLCHAINS=$(echo "$ENV_OUTPUT" | grep "toolchains:" | awk '{print $NF}')
HDC_PATH=$(echo "$ENV_OUTPUT" | grep "hdc:" | awk '{print $NF}')
HVIGORW_PATH=$(echo "$ENV_OUTPUT" | grep "hvigorw:" | awk '{print $NF}')

if [ -n "$TOOLCHAINS" ]; then
    export PATH="$TOOLCHAINS:$PATH"
    echo -e "${GREEN}  ✓ Toolchains: $TOOLCHAINS${NC}"
fi

if [ -n "$HDC_PATH" ]; then
    HDC_DIR=$(dirname "$HDC_PATH")
    export PATH="$HDC_DIR:$PATH"
    echo -e "${GREEN}  ✓ HDC: $HDC_DIR${NC}"
fi

if [ -n "$HVIGORW_PATH" ]; then
    HVIGORW_DIR=$(dirname "$HVIGORW_PATH")
    export PATH="$HVIGORW_DIR:$PATH"
    echo -e "${GREEN}  ✓ Hvigorw: $HVIGORW_DIR${NC}"
fi

export HDC_SERVER_PORT=7035

echo ""

# 检查设备连接
echo -e "${BLUE}📱 Checking device connection...${NC}"

DEVICE_COUNT=$(hdc list targets 2>/dev/null | wc -l | tr -d ' ')

if [ "$DEVICE_COUNT" -eq 0 ] || [ "$DEVICE_COUNT" -eq 1 ]; then
    echo -e "${YELLOW}⚠ No device found${NC}"
    echo -e "${YELLOW}Please check:${NC}"
    echo "  1. Device is connected via USB"
    echo "  2. USB debugging is enabled"
    echo "  3. Device is authorized"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    DEVICE_ID=$(hdc list targets | head -1)
    echo -e "${GREEN}✓ Device found: $DEVICE_ID${NC}"
fi

echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 启动调试
echo -e "${BLUE}🚀 Starting DevTools debugging session...${NC}"
echo ""

cd "$SCRIPT_DIR"
./arkweb-app-debug start "$@"
