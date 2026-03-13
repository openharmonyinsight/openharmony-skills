#!/bin/bash

echo "正在构建 GitCode MCP Server..."

# 设置版本号
VERSION="1.0.0"

# 设置构建目录
BUILD_DIR="./bin"
mkdir -p $BUILD_DIR

# 编译MCP服务器
echo "编译MCP服务器..."
go build -o $BUILD_DIR/gitcode-mcp main.go
if [ $? -ne 0 ]; then
    echo "编译失败: gitcode-mcp"
    exit 1
fi

# 复制配置文件示例
cp .env.example $BUILD_DIR/.env.example
cp mcp.json $BUILD_DIR/mcp.json

echo "编译完成！构建结果保存在 $BUILD_DIR 目录中。"
echo "可执行文件:"
echo "  - $BUILD_DIR/gitcode-mcp: MCP服务器"
echo ""
echo "使用说明:"
echo "  STDIO模式: ./gitcode-mcp"
echo "  SSE模式: MCP_TRANSPORT=sse ./gitcode-mcp" 