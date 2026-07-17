#!/bin/bash

# dict位置验证脚本
# 用途：验证dict文件是否在正确位置，检测cd命令错误使用
# 支持：--clean 参数自动清理错误位置的dict

set -e

LOG_DIR=""
AUTO_CLEAN=false

# 解析参数
for arg in "$@"; do
    case $arg in
        --clean)
            AUTO_CLEAN=true
            shift
            ;;
        *)
            if [ -z "$LOG_DIR" ]; then
                LOG_DIR="$arg"
            fi
            ;;
    esac
done

OUTPUT_DIR="${LOG_DIR}_parsed"

if [ -z "$LOG_DIR" ]; then
    echo "用法: $0 <日志目录> [--clean]"
    echo "示例: $0 /path/to/hilog_FMR0123417000740"
    echo "      $0 /path/to/hilog_FMR0123417000740 --clean"
    echo ""
    echo "参数说明:"
    echo "  --clean    自动清理错误位置的dict目录"
    exit 1
fi

if [ ! -d "$LOG_DIR" ]; then
    echo "错误：日志目录不存在: $LOG_DIR"
    exit 1
fi

echo "=== 验证dict文件位置 ==="
echo ""

# 1. 检查技能目录下是否有dict文件（检查根目录）
SKILL_DICT_DIR="$HOME/.opencode/skills/ohos-issue-xts-log-analysis/dict"

if [ -d "$SKILL_DICT_DIR" ]; then
    DICT_SIZE=$(du -sh "$SKILL_DICT_DIR" 2>/dev/null | awk '{print $1}')
    echo "❌ 错误：检测到技能目录下有dict文件"
    echo "位置: $SKILL_DICT_DIR ($DICT_SIZE)"
    echo "原因：执行hilogtool时使用了cd命令（错误做法）"
    echo ""
    
    if [ "$AUTO_CLEAN" = true ]; then
        echo "自动清理中..."
        rm -rf "$SKILL_DICT_DIR"
        if [ $? -eq 0 ]; then
            echo "✅ 已清理技能目录下的dict文件"
        else
            echo "❌ 清理失败，请手动清理："
            echo "   rm -rf $SKILL_DICT_DIR"
        fi
    else
        echo "清理命令："
        echo "  rm -rf $SKILL_DICT_DIR"
        echo ""
        echo "或使用自动清理："
        echo "  $0 $LOG_DIR --clean"
    fi
    echo ""
else
    echo "✅ 技能目录下无dict文件（正确）"
fi

# 2. 检查输出目录是否存在
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "ℹ️  输出目录不存在: $OUTPUT_DIR"
    echo "   可能尚未解密"
    exit 0
fi

# 3. 检查输出目录下的dict位置
EXPECTED_DICT="$OUTPUT_DIR/dict"

if [ -d "$EXPECTED_DICT" ]; then
    DICT_SIZE=$(du -sh "$EXPECTED_DICT" 2>/dev/null | awk '{print $1}')
    echo "✅ dict文件位置正确: $EXPECTED_DICT ($DICT_SIZE)"
else
    echo "ℹ️  输出目录下无dict文件（可能已清理）"
fi

# 4. 检查解密状态文件
STATE_FILE="$OUTPUT_DIR/.decrypt_state.json"

if [ -f "$STATE_FILE" ]; then
    echo "✅ 解密状态文件存在: $STATE_FILE"
    echo ""
    echo "状态信息："
    python3 -c "
import json
with open('$STATE_FILE', 'r') as f:
    state = json.load(f)
    print(f\"  解密时间: {state.get('decrypted_time', 'N/A')}\")
    print(f\"  成功文件: {state.get('success_files', 0)}/{state.get('total_files', 0)}\")
    print(f\"  并行解密: {'是' if state.get('parallel', False) else '否'}\")
" 2>/dev/null || echo "  （状态文件读取失败）"
else
    echo "ℹ️  解密状态文件不存在"
fi

echo ""
echo "=== 验证完成 ==="