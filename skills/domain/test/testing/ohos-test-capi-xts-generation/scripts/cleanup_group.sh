#!/bin/bash

# Group 编译对象清理脚本
# 用法: ./cleanup_group.sh <OH_ROOT> <子系统名>

OH_ROOT="${1:-/mnt/data/c00810129/oh_0130}"
SUBSYSTEM="${2:-testfwk}"

if [ ! -d "$OH_ROOT/test/xts/acts/$SUBSYSTEM" ]; then
    echo "❌ 子系统目录不存在: $OH_ROOT/test/xts/acts/$SUBSYSTEM"
    exit 1
fi

echo "🧹 开始清理 Group: $SUBSYSTEM"
echo "📂 OH_ROOT: $OH_ROOT"
echo "📁 子系统: $SUBSYSTEM"

# 1. 解析 BUILD.gn 获取所有测试套路径
BUILD_GN_FILE="$OH_ROOT/test/xts/acts/$SUBSYSTEM/BUILD.gn"

if [ ! -f "$BUILD_GN_FILE" ]; then
    echo "❌ BUILD.gn 文件不存在: $BUILD_GN_FILE"
    exit 1
fi

echo "📋 解析 $BUILD_GN_FILE 中的测试套..."

# 提取 deps 中的测试套路径（简化版）
TEST_SUITES=$(grep -A 50 "group(\"$SUBSYSTEM\")" "$BUILD_GN_FILE" | \
              grep 'deps =' -A 30 | \
              grep '"' | \
              sed 's/.*"\([^"]*\)".*/\1/' | \
              grep -v '^$' | \
              cut -d':' -f1 | \
              sort | uniq)

# 过滤掉非目录的依赖
TEST_SUITES=$(echo "$TEST_SUITES" | grep -v "^[[:space:]]*#" | grep -v "^$")

if [ -z "$TEST_SUITES" ]; then
    echo "❌ 未找到测试套目标，请检查 BUILD.gn 文件格式"
    exit 1
fi

echo "🔍 发现以下测试套："
echo "$TEST_SUITES" | nl

# 2. 逐个清理测试套
cd "$OH_ROOT/test/xts/acts/$SUBSYSTEM"

CLEANED_COUNT=0
FAILED_COUNT=0

while IFS= read -r suite; do
    if [ -n "$suite" ] && [ -d "$suite" ]; then
        echo "🗂️  清理测试套: $suite"

        cd "$suite" 2>/dev/null

        if [ $? -eq 0 ]; then
            # 清理缓存目录
            echo "  🗑️  删除 .hvigor, build, entry/build, oh_modules..."
            rm -rf .hvigor build entry/build oh_modules 2>/dev/null

            # 清理配置文件
            echo "  🗑️  删除 oh-package-lock.json5, local.properties..."
            rm -f oh-package-lock.json5 local.properties 2>/dev/null

            echo "  ✅ 清理完成: $suite"
            CLEANED_COUNT=$((CLEANED_COUNT + 1))
        else
            echo "  ❌ 无法进入目录: $suite"
            FAILED_COUNT=$((FAILED_COUNT + 1))
        fi

        cd "$OH_ROOT/test/xts/acts/$SUBSYSTEM" 2>/dev/null
    else
        echo "⚠️  跳过不存在的测试套: $suite"
    fi
done <<< "$TEST_SUITES"

echo ""
echo "📊 清理统计："
echo "  ✅ 成功清理: $CLEANED_COUNT 个测试套"
echo "  ❌ 清理失败: $FAILED_COUNT 个测试套"

# 3. 清理 OH_ROOT 目录下的 out 目录
echo ""
echo "🗂️  清理 OH_ROOT 下的 out 目录..."
cd "$OH_ROOT"
rm -rf out 2>/dev/null

if [ $? -eq 0 ]; then
    echo "  ✅ out 目录已删除"
else
    echo "  ⚠️  out 目录不存在或删除失败"
fi

echo ""
echo "🎉 Group 清理完成！"
