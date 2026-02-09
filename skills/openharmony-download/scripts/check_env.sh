#!/bin/bash
# OpenHarmony Environment Check - Individual Check Script
# Usage: check_env.sh <check_type>
# Returns: 0 (success) or 1 (failed)

CHECK_TYPE="$1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_git() {
    if command -v git &> /dev/null; then
        version=$(git --version 2>&1)
        echo -e "${GREEN}✓${NC} git 已安装"
        echo "版本: $version"
        return 0
    else
        echo -e "${RED}✗${NC} git 未安装"
        return 1
    fi
}

check_git_lfs() {
    if command -v git-lfs &> /dev/null; then
        version=$(git-lfs version 2>&1 | head -n 1)
        echo -e "${GREEN}✓${NC} git-lfs 已安装"
        echo "版本: $version"
        return 0
    else
        echo -e "${RED}✗${NC} git-lfs 未安装"
        return 1
    fi
}

check_python3() {
    if command -v python3 &> /dev/null; then
        version=$(python3 --version 2>&1)
        echo -e "${GREEN}✓${NC} python3 已安装"
        echo "版本: $version"
        return 0
    else
        echo -e "${RED}✗${NC} python3 未安装"
        return 1
    fi
}

check_curl() {
    if command -v curl &> /dev/null; then
        version=$(curl --version 2>&1 | head -n 1)
        echo -e "${GREEN}✓${NC} curl 已安装"
        echo "版本: $version"
        return 0
    else
        echo -e "${RED}✗${NC} curl 未安装"
        return 1
    fi
}

check_repo() {
    if command -v repo &> /dev/null; then
        version=$(repo --version 2>&1 | head -n 1)
        echo -e "${GREEN}✓${NC} repo 工具已安装"
        echo "版本: $version"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} repo 工具未安装"
        echo "建议安装方法:"
        echo "  mkdir -p ~/bin"
        echo "  https://raw.gitcode.com/gitcode-dev/repo/raw/main/repo-py3 -o ~/bin/repo"
        echo "  chmod a+x ~/bin/repo"
        echo "  export PATH=~/bin:\$PATH"
        echo "  pip3 install -i https://repo.huaweicloud.com/repository/pypi/simple requests"
        return 1
    fi
}

check_git_config() {
    MISSING=0

    if git config --global user.name &> /dev/null; then
        echo -e "${GREEN}✓${NC} Git 用户名已配置"
        echo "  $(git config --global user.name)"
    else
        echo -e "${RED}✗${NC} Git 用户名未配置"
        echo "  运行: git config --global user.name \"Your Name\""
        MISSING=1
    fi

    if git config --global user.email &> /dev/null; then
        echo -e "${GREEN}✓${NC} Git 邮箱已配置"
        echo "  $(git config --global user.email)"
    else
        echo -e "${RED}✗${NC} Git 邮箱未配置"
        echo "  运行: git config --global user.email \"your-email@example.com\""
        MISSING=1
    fi

    return $MISSING
}

check_disk_space() {
    available=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
    echo -e "${GREEN}✓${NC} 磁盘空间检查"
    echo "可用空间: ${available}GB"

    if [ "$available" -lt 40 ]; then
        echo -e "${RED}  警告: 可用空间不足 40GB，下载可能失败${NC}"
        return 1
    elif [ "$available" -lt 80 ]; then
        echo -e "${YELLOW}  注意: 建议至少 80GB 可用空间${NC}"
        return 0
    else
        echo -e "${GREEN}  磁盘空间充足${NC}"
        return 0
    fi
}

# Main
case "$CHECK_TYPE" in
    git)
        check_git
        ;;
    git-lfs)
        check_git_lfs
        ;;
    python3)
        check_python3
        ;;
    curl)
        check_curl
        ;;
    repo)
        check_repo
        ;;
    git-config)
        check_git_config
        ;;
    disk-space)
        check_disk_space
        ;;
    all)
        FAILED=0
        check_git || FAILED=1
        check_git_lfs || FAILED=1
        check_python3 || FAILED=1
        check_curl || FAILED=1
        check_repo || FAILED=1
        check_git_config || FAILED=1
        check_disk_space || FAILED=1

        if [ $FAILED -eq 0 ]; then
            echo ""
            echo -e "${GREEN}所有环境检查通过！${NC}"
            exit 0
        else
            echo ""
            echo -e "${RED}部分环境检查未通过，请先解决上述问题${NC}"
            exit 1
        fi
        ;;
    *)
        echo "用法: $0 <check_type>"
        echo ""
        echo "支持的检查类型:"
        echo "  git         - 检查 git"
        echo "  git-lfs     - 检查 git-lfs"
        echo "  python3     - 检查 python3"
        echo "  curl        - 检查 curl"
        echo "  repo        - 检查 repo 工具"
        echo "  git-config  - 检查 git 配置"
        echo "  disk-space  - 检查磁盘空间"
        echo "  all         - 执行所有检查"
        exit 1
        ;;
esac
