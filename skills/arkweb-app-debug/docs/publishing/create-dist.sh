#!/bin/bash
# ArkWeb Debug Tool - Distribution Script
# 版本: 1.0

set -e

VERSION="1.0"
DIST_DIR="dist"
SOURCE_DIR="arkweb-app-debug-skill"

echo "📦 ArkWeb Debug Tool v${VERSION} - 创建发布包"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "项目根目录: $PROJECT_ROOT"
echo ""

# 清理旧的发布目录
rm -rf ${PROJECT_ROOT}/${DIST_DIR}
mkdir -p ${PROJECT_ROOT}/${DIST_DIR}

# 方式1: 创建 tar.gz 压缩包
echo "📦 创建 tar.gz 压缩包..."
cd ${PROJECT_ROOT}
tar -czf ${DIST_DIR}/arkweb-app-debug-skill-${VERSION}.tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    --exclude='dist' \
    --exclude='*.egg-info' \
    --exclude='.pytest_cache' \
    --exclude='.python-version' \
    ${SOURCE_DIR}/

echo "   ✅ ${DIST_DIR}/arkweb-app-debug-skill-${VERSION}.tar.gz"

# 方式2: 创建 zip 压缩包
echo "📦 创建 zip 压缩包..."
zip -rq ${DIST_DIR}/arkweb-app-debug-skill-${VERSION}.zip \
    ${SOURCE_DIR} \
    -x '*__pycache__*' \
    -x '*.pyc' \
    -x '.git*' \
    -x '.DS_Store' \
    -x 'dist/*' \
    -x '*.egg-info/*' \
    -x '.pytest_cache/*' \
    -x '.python-version'

echo "   ✅ ${DIST_DIR}/arkweb-app-debug-skill-${VERSION}.zip"

# 计算文件大小和哈希
echo ""
echo "📊 发布包信息:"
cd ${DIST_DIR}
for file in *.tar.gz *.zip; do
    if [ -f "$file" ]; then
        SIZE=$(du -h "$file" | cut -f1)
        HASH=$(shasum -a 256 "$file" | cut -d' ' -f1)
        echo ""
        echo "   📄 ${file}"
        echo "   大小: ${SIZE}"
        echo "   SHA256: ${HASH}"
    fi
done
cd ${PROJECT_ROOT}

echo ""
echo "✅ 发布包创建完成！"
echo ""
echo "📋 分发方式:"
echo ""
echo "   方式1 - tar.gz:"
echo "   用户执行:"
echo "   $ tar -xzf ${DIST_DIR}/arkweb-app-debug-skill-${VERSION}.tar.gz"
echo "   $ cd arkweb-app-debug-skill"
echo "   $ ./arkweb-app-debug start  # 直接运行，无需安装！"
echo ""
echo "   方式2 - zip:"
echo "   用户执行:"
echo "   $ unzip ${DIST_DIR}/arkweb-app-debug-skill-${VERSION}.zip"
echo "   $ cd arkweb-app-debug-skill"
echo "   $ ./arkweb-app-debug start  # 直接运行，无需安装！"
echo ""
echo "详细使用说明请查看: README.md"
echo ""
