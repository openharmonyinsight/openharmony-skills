#!/bin/bash

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # 无颜色

# 解析命令行参数
DRY_RUN=false
for arg in "$@"; do
  case $arg in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
  esac
done

echo -e "${GREEN}开始安装 GitCode MCP Server...${NC}"

# 设置版本号和安装目录
VERSION="1.0.0"
INSTALL_DIR="/usr/local/bin"
CONFIG_DIR="$HOME/.gitcode_mcp"

# 首先构建项目
echo -e "${YELLOW}正在构建项目...${NC}"
go build -o gitcode-mcp

# 检查编译结果
if [ $? -ne 0 ]; then
    echo -e "${RED}编译失败，安装终止${NC}"
    exit 1
fi

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[模拟模式] 将执行以下操作：${NC}"
    echo -e "- 创建配置目录: $CONFIG_DIR"
    echo -e "- 复制配置文件到: $CONFIG_DIR"
    echo -e "- 安装可执行文件到: $INSTALL_DIR/gitcode-mcp"
    echo -e "${GREEN}模拟安装完成。未进行实际更改。${NC}"
    exit 0
fi

# 检查权限
mkdir -p "$CONFIG_DIR"

# 将配置文件复制到配置目录
echo -e "${YELLOW}正在复制配置文件...${NC}"
cp .env.example "$CONFIG_DIR/.env"
cp -r docs "$CONFIG_DIR/"
cp mcp.json "$CONFIG_DIR/"

# 替换配置文件中的令牌占位符
echo -e "${YELLOW}请输入您的GitCode访问令牌 (如果没有可以按Enter跳过)：${NC}"
read token
if [ ! -z "$token" ]; then
    # 对于macOS使用sed -i ''
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/<您的GitCode访问令牌>/$token/g" "$CONFIG_DIR/.env"
    else
        # 对于Linux使用sed -i
        sed -i "s/<您的GitCode访问令牌>/$token/g" "$CONFIG_DIR/.env"
    fi
    echo -e "${GREEN}已更新GitCode令牌${NC}"
fi

# 复制可执行文件到系统路径需要sudo权限
echo -e "${YELLOW}正在将可执行文件复制到 $INSTALL_DIR (可能需要管理员权限)${NC}"
sudo cp gitcode-mcp "$INSTALL_DIR/"
if [ $? -ne 0 ]; then
    echo -e "${RED}无法复制文件到 $INSTALL_DIR，请检查权限${NC}"
    echo -e "${YELLOW}尝试安装到用户目录...${NC}"
    
    USER_BIN="$HOME/bin"
    mkdir -p "$USER_BIN"
    cp gitcode-mcp "$USER_BIN/"
    
    # 检查PATH中是否包含用户bin目录
    if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
        echo -e "${YELLOW}请将 $USER_BIN 添加到您的PATH环境变量中：${NC}"
        
        # 检测用户shell类型
        if [[ "$SHELL" == */zsh ]]; then
            echo -e "echo 'export PATH=\"\$PATH:$USER_BIN\"' >> ~/.zshrc"
            echo -e "source ~/.zshrc"
        elif [[ "$SHELL" == */bash ]]; then
            echo -e "echo 'export PATH=\"\$PATH:$USER_BIN\"' >> ~/.bashrc"
            echo -e "source ~/.bashrc"
        else
            echo -e "请将 $USER_BIN 添加到您的PATH环境变量中"
        fi
    fi
    
    echo -e "${GREEN}已安装到 $USER_BIN/gitcode-mcp${NC}"
else
    # 设置可执行权限
    sudo chmod +x "$INSTALL_DIR/gitcode-mcp"
    echo -e "${GREEN}已成功安装到 $INSTALL_DIR/gitcode-mcp${NC}"
fi

echo -e "${GREEN}GitCode MCP Server 安装完成！${NC}"
echo -e "${YELLOW}配置文件位置: $CONFIG_DIR${NC}"
echo -e "${YELLOW}使用方法:${NC}"
echo -e "  STDIO模式: gitcode-mcp"
echo -e "  配置文件: 编辑 $CONFIG_DIR/.env 设置您的GitCode令牌"
echo -e "  平台配置文件: 位于 $CONFIG_DIR/docs/ 目录下"
echo -e ""
echo -e "${GREEN}感谢使用 GitCode MCP Server！${NC}" 