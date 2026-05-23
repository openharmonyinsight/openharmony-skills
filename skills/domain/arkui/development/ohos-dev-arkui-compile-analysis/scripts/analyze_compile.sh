#!/bin/bash
#
# 编译效率分析脚本
# 功能：分析单个文件的编译时间、资源开销和头文件依赖
#
# ⚠️ 重要要求：
#   1. 编译命令必须在 out/{product} 目录下执行
#   2. 分析结果必须基于实际运行结果，不能推测
#   3. 头文件依赖必须通过 parse_ii.py 解析 .ii 文件
#
# 使用方法:
#   ./analyze_compile.sh <源文件路径> [产品名称] [选项]
#
# 示例:
#   ./analyze_compile.sh frameworks/core/event/touch_event.cpp
#   ./analyze_compile.sh frameworks/core/event/touch_event.cpp rk3568
#   ./analyze_compile.sh frameworks/core/event/touch_event.cpp rk3568 --save-script
#
# 选项:
#   --save-script    保存增强编译脚本到 out/{product}/compile_single_file_{name}.sh
#                    可用于后续重复执行独立的性能测试

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 查找 OpenHarmony 根目录
find_oh_root() {
    local dir="$(pwd)"
    while [[ ! -f "$dir/.gn" ]]; do
        dir="$(dirname "$dir")"
        if [[ "$dir" == "/" ]]; then
            echo "错误: 找不到 OpenHarmony 根目录（无 .gn 文件）" >&2
            return 1
        fi
    done
    echo "$dir"
}

# 查找 ace_engine 目录
find_ace_engine_root() {
    local oh_root="$1"
    if [[ -d "$oh_root/foundation/arkui/ace_engine" ]]; then
        echo "$oh_root/foundation/arkui/ace_engine"
    else
        echo "错误: 找不到 ace_engine 目录" >&2
        return 1
    fi
}

# 检查参数
if [[ $# -lt 1 ]]; then
    echo "用法: $0 <源文件路径> [产品名称] [选项]"
    echo ""
    echo "示例:"
    echo "  $0 frameworks/core/event/touch_event.cpp"
    echo "  $0 frameworks/core/event/touch_event.cpp rk3568"
    echo "  $0 frameworks/core/event/touch_event.cpp rk3568 --save-script"
    echo ""
    echo "选项:"
    echo "  --save-script    保存增强编译脚本到 out/{product}/compile_single_file_{name}.sh"
    exit 1
fi

SOURCE_FILE="$1"
PRODUCT_NAME="${2:-rk3568}"
SAVE_SCRIPT=""
if [[ "$3" == "--save-script" ]] || [[ "$2" == "--save-script" ]]; then
    SAVE_SCRIPT="--save-enhanced"
fi

# 查找目录
OH_ROOT=$(find_oh_root)
ACE_ENGINE_ROOT=$(find_ace_engine_root "$OH_ROOT")

echo "========================================"
echo "编译效率分析工具"
echo "========================================"
echo ""
echo "OpenHarmony 根目录: $OH_ROOT"
echo "ACE Engine 根目录: $ACE_ENGINE_ROOT"
echo "源文件: $SOURCE_FILE"
echo "产品名称: $PRODUCT_NAME"
echo ""

# 切换到 ace_engine 目录以获取编译命令
cd "$ACE_ENGINE_ROOT"

# 步骤 1: 生成增强编译脚本（--save-enhanced 直接写文件，避免从 stdout 解析多行命令）
echo "========================================"
echo "步骤 1: 生成增强编译脚本"
echo "========================================"
echo ""

SOURCE_BASENAME=$(basename "$SOURCE_FILE" | sed 's/\.cpp$//;s/\.cc$//;s/\.cxx$//;s/\.c$//')
ENHANCED_SCRIPT="$OH_ROOT/out/$PRODUCT_NAME/compile_single_file_${SOURCE_BASENAME}.sh"

python3 "$SCRIPT_DIR/get_compile_command.py" "$SOURCE_FILE" "$OH_ROOT/out/$PRODUCT_NAME" --save-enhanced 2>&1

if [[ $? -ne 0 ]] || [[ ! -f "$ENHANCED_SCRIPT" ]]; then
    echo "错误: 无法生成增强编译脚本"
    exit 1
fi

echo ""
echo "✓ 增强编译脚本已生成: $ENHANCED_SCRIPT"
echo ""

# 如果用户指定了 --save-script，提示后续可复用
if [[ -n "$SAVE_SCRIPT" ]]; then
    echo "  后续可独立使用该脚本进行重复编译测试:"
    echo "    cd $OH_ROOT/out/$PRODUCT_NAME"
    echo "    bash compile_single_file_${SOURCE_BASENAME}.sh"
    echo ""
fi

# 步骤 2: 执行增强编译脚本
echo "========================================"
echo "步骤 2: 在 out/$PRODUCT_NAME 目录执行编译并收集性能数据"
echo "========================================"
echo ""

cd "$OH_ROOT/out/$PRODUCT_NAME"
bash "$ENHANCED_SCRIPT"
EXIT_CODE=$?

if [[ $EXIT_CODE -ne 0 ]]; then
    echo "========================================"
    echo "❌ 错误: 编译失败 (退出码: $EXIT_CODE)"
    echo "========================================"
    exit 1
fi

echo "----------------------------------------"
echo ""

# 步骤 3: 查找生成的 .ii 文件
echo "========================================"
echo "步骤 3: 查找预编译文件 (.ii)"
echo "========================================"
echo ""

# 在 obj 目录查找 .ii 文件
II_FILE=$(find obj -name "${SOURCE_BASENAME}.ii" 2>/dev/null | head -1)

if [[ -z "$II_FILE" ]]; then
    echo "❌ 错误: 找不到生成的 .ii 文件"
    echo "查找的文件名: ${SOURCE_BASENAME}.ii"
    echo "查找目录: $(pwd)/obj"
    echo ""
    echo "可能的原因:"
    echo "  1. 编译命令未使用 -save-temps 选项"
    echo "  2. .ii 文件生成失败"
    echo "  3. 文件名不匹配"
    exit 1
fi

echo "✓ 找到预编译文件: $II_FILE"
echo ""

# 步骤 4: 使用 parse_ii.py 解析头文件依赖
echo "========================================"
echo "步骤 4: 使用 parse_ii.py 解析头文件依赖"
echo "========================================"
echo ""
echo "⚠️  正在解析 .ii 文件，请稍候..."
echo ""

DEP_OUTPUT="$OH_ROOT/out/$PRODUCT_NAME/${SOURCE_BASENAME}_dependency_tree.txt"
python3 "$SCRIPT_DIR/parse_ii.py" "$II_FILE" --output "$DEP_OUTPUT"

if [[ $? -ne 0 ]]; then
    echo ""
    echo "❌ 错误: 解析 .ii 文件失败"
    exit 1
fi

echo ""
echo "========================================"
echo "✓ 分析完成！"
echo "========================================"
echo ""
echo "实际运行结果:"
echo "  - 编译时间: 见上方编译输出中的 '编译时间:'"
echo "  - 峰值内存: 见上方编译输出中的 '峰值内存:'"
echo "  - 头文件依赖树: 见上方 parse_ii.py 输出"
echo ""
echo "文件位置:"
echo "  - 预编译文件: $II_FILE"
echo "  - 目标文件: $(dirname $II_FILE)/${SOURCE_BASENAME}.o"
echo ""
echo "⚠️  提示: 所有数据均来自实际编译运行，无推测内容"
echo ""
