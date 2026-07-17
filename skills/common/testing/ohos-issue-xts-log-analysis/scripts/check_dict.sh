#!/bin/bash

# dict文件检测脚本
# 用途：自动检测hilog目录中的dict文件，并验证是否可用

set -e

LOG_DIR="$1"

if [ -z "$LOG_DIR" ]; then
    echo "用法: $0 <hilog日志目录>"
    echo "示例: $0 /path/to/hilog_FMR0123417000740"
    exit 1
fi

if [ ! -d "$LOG_DIR" ]; then
    echo "错误：目录不存在: $LOG_DIR"
    exit 1
fi

echo "=== 检查hilog日志目录: $LOG_DIR ==="
echo ""

# 1. 检查hilog文件
hilog_count=$(find "$LOG_DIR" -name "hilog.*.gz" -type f 2>/dev/null | wc -l)
echo "1. hilog文件数量: $hilog_count"
if [ "$hilog_count" -eq 0 ]; then
    echo "   ⚠️  未找到hilog.*.gz文件"
    exit 0
else
    echo "   ✅ 找到 $hilog_count 个hilog文件"
fi
echo ""

# 2. 检查dict文件
echo "2. 检查dict文件..."
dict_files=$(find "$LOG_DIR" -maxdepth 1 \( -name "hilog_dict.*.zip" -o -name "dict.zip" \) -type f 2>/dev/null)

if [ -z "$dict_files" ]; then
    echo "   ❌ 未找到dict文件"
    echo "   可能的原因："
    echo "   - dict文件在其他目录"
    echo "   - dict文件未包含在日志包中"
    echo ""
    echo "   建议："
    echo "   - 检查同批次其他测试目录"
    echo "   - 联系测试环境负责人获取dict文件"
    exit 1
fi

dict_count=$(echo "$dict_files" | wc -l)
echo "   ✅ 找到 $dict_count 个dict文件："
echo "$dict_files" | while read -r dict_file; do
    file_size=$(ls -lh "$dict_file" | awk '{print $5}')
    file_name=$(basename "$dict_file")
    echo "   - $file_name ($file_size)"
done
echo ""

# 3. 检查dict时间戳（如果有多个）
if [ "$dict_count" -gt 1 ]; then
    echo "3. ⚠️  检测到多个dict文件，建议使用时间戳最近的："
    ls -lt "$LOG_DIR"/hilog_dict.*.zip "$LOG_DIR"/dict.zip 2>/dev/null | head -5
    echo ""
fi

# 4. 说明dict时间戳的作用
echo "4. dict文件说明..."
echo "   ℹ️  dict时间戳与hilog时间戳不需要匹配"
echo "   - dict文件是密钥字典，与日志时间无关"
echo "   - 即使时间戳不同，也可以正常解密"
echo "   - 例如：dict时间20260626，hilog时间20260630，可以正常解密"
echo ""

# 5. 输出推荐的解密命令
first_dict=$(echo "$dict_files" | head -1)
output_dir="${LOG_DIR}_parsed"

echo "5. 推荐的解密命令："
echo ""
echo "   # 创建输出目录"
echo "   mkdir -p \"$output_dir\""
echo ""
echo "   # 执行解密（Linux环境）"
echo "   DISPLAY= wine64 /path/to/hilogtool.exe parse \\"
echo "       -i \"$LOG_DIR\" \\"
echo "       -o \"$output_dir\" \\"
echo "       -d \"$first_dict\""
echo ""
echo "   # 或使用变量"
echo "   dict_file=\"$first_dict\""
echo "   DISPLAY= wine64 hilogtool.exe parse -i \"$LOG_DIR\" -o \"$output_dir\" -d \"\$dict_file\""
echo ""

echo "=== 检查完成 ==="