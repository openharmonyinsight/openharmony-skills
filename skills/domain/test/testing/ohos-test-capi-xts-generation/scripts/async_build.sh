#!/bin/bash

# ==============================================================================
# OpenHarmony CAPI XTS 异步编译脚本
# 方案 A：轻量级后台编译 + 日志轮询
# ==============================================================================
# 
# 使用方法:
#   ./async_build.sh <OH_ROOT> <测试套名称> [产品名称] [动作]
#
# 参数:
#   OH_ROOT     - OpenHarmony 工程根目录（必需）
#   测试套名称   - 要编译的测试套名称（必需）
#   产品名称     - 默认 rk3568（可选）
#   动作         - start|status|stop|tail|wait（可选，默认 start）
#
# 动作说明:
#   start  - 启动异步编译（默认）
#   status - 检查编译状态
#   stop   - 停止编译进程
#   tail   - 实时查看编译日志
#   wait   - 等待编译完成并返回结果
#
# 示例:
#   # 启动异步编译
#   ./async_build.sh /path/to/openharmony ActsCameraManagerCapiTest
#
#   # 检查编译状态
#   ./async_build.sh /path/to/openharmony ActsCameraManagerCapiTest rk3568 status
#
#   # 等待编译完成
#   ./async_build.sh /path/to/openharmony ActsCameraManagerCapiTest rk3568 wait
#
#   # 实时查看日志
#   ./async_build.sh /path/to/openharmony ActsCameraManagerCapiTest rk3568 tail
#
# ==============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 参数解析
OH_ROOT="${1:-}"
SUITE_NAME="${2:-}"
PRODUCT_NAME="${3:-rk3568}"
ACTION="${4:-start}"

# 日志和 PID 文件路径
LOG_DIR="/tmp/oh_capi_build"
LOG_FILE="${LOG_DIR}/${SUITE_NAME}.log"
PID_FILE="${LOG_DIR}/${SUITE_NAME}.pid"
STATUS_FILE="${LOG_DIR}/${SUITE_NAME}.status"
ERROR_FILE="${LOG_DIR}/${SUITE_NAME}.error"

# 使用说明
usage() {
    echo -e "${CYAN}OpenHarmony CAPI XTS 异步编译脚本${NC}"
    echo ""
    echo "使用方法:"
    echo "  $0 <OH_ROOT> <测试套名称> [产品名称] [动作]"
    echo ""
    echo "动作:"
    echo "  start  - 启动异步编译（默认）"
    echo "  status - 检查编译状态"
    echo "  stop   - 停止编译进程"
    echo "  tail   - 实时查看编译日志"
    echo "  wait   - 等待编译完成并返回结果"
    echo "  logs   - 查看完整日志"
    echo "  errors - 查看错误日志"
    echo ""
    echo "示例:"
    echo "  # 启动异步编译"
    echo "  $0 /path/to/openharmony ActsCameraManagerCapiTest"
    echo ""
    echo "  # 检查编译状态"
    echo "  $0 /path/to/openharmony ActsCameraManagerCapiTest rk3568 status"
    echo ""
    echo "  # 等待编译完成"
    echo "  $0 /path/to/openharmony ActsCameraManagerCapiTest rk3568 wait"
    exit 1
}

# 验证参数
validate_params() {
    if [ -z "$OH_ROOT" ] || [ -z "$SUITE_NAME" ]; then
        usage
    fi
    
    if [[ ! "$SUITE_NAME" =~ ^[A-Za-z0-9_.-]+$ ]]; then
        echo -e "${RED}❌ 错误: 测试套名称包含非法字符: $SUITE_NAME${NC}"
        exit 1
    fi
    
    if [[ ! "$PRODUCT_NAME" =~ ^[A-Za-z0-9_.-]+$ ]]; then
        echo -e "${RED}❌ 错误: 产品名称包含非法字符: $PRODUCT_NAME${NC}"
        exit 1
    fi
    
    if [ ! -d "$OH_ROOT" ]; then
        echo -e "${RED}❌ 错误: OH_ROOT 目录不存在: $OH_ROOT${NC}"
        exit 1
    fi
    
    if [ ! -f "$OH_ROOT/test/xts/acts/build.sh" ]; then
        echo -e "${RED}❌ 错误: 编译脚本不存在: $OH_ROOT/test/xts/acts/build.sh${NC}"
        exit 1
    fi
}

# 创建日志目录
create_log_dir() {
    mkdir -p "$LOG_DIR"
}

# 启动异步编译
start_build() {
    echo -e "${BLUE}=== 启动异步编译 ===${NC}"
    echo "OH_ROOT: $OH_ROOT"
    echo "测试套: $SUITE_NAME"
    echo "产品: $PRODUCT_NAME"
    
    # 检查是否已有编译进程
    if [ -f "$PID_FILE" ]; then
        local existing_pid=$(cat "$PID_FILE")
        if kill -0 "$existing_pid" 2>/dev/null; then
            echo -e "${YELLOW}⚠️  已有编译进程在运行 (PID: $existing_pid)${NC}"
            echo "使用 '$0 $OH_ROOT $SUITE_NAME $PRODUCT_NAME status' 查看状态"
            exit 0
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    create_log_dir
    
    # 清空日志文件
    > "$LOG_FILE"
    > "$ERROR_FILE"
    
    # 启动后台编译
    echo -e "${GREEN}🚀 启动后台编译进程...${NC}"
    
    export _BUILD_OH_ROOT="$OH_ROOT"
    export _BUILD_SUITE_NAME="$SUITE_NAME"
    export _BUILD_PRODUCT_NAME="$PRODUCT_NAME"
    export _BUILD_LOG_FILE="$LOG_FILE"
    export _BUILD_STATUS_FILE="$STATUS_FILE"
    export _BUILD_ERROR_FILE="$ERROR_FILE"

    cd "$OH_ROOT"
    nohup bash -c '
        set -o pipefail
        
        echo "[BUILD] start_time: $(date "+%Y-%m-%d %H:%M:%S")" > "$_BUILD_STATUS_FILE"
        echo "[BUILD] suite_name: $_BUILD_SUITE_NAME" >> "$_BUILD_STATUS_FILE"
        echo "[BUILD] status: RUNNING" >> "$_BUILD_STATUS_FILE"
        
        cd "$_BUILD_OH_ROOT"
        ./test/xts/acts/build.sh product_name="$_BUILD_PRODUCT_NAME" system_size=standard suite="$_BUILD_SUITE_NAME" 2>&1 | tee -a "$_BUILD_LOG_FILE"
        exit_code=${PIPESTATUS[0]}
        
        echo "[BUILD] end_time: $(date "+%Y-%m-%d %H:%M:%S")" >> "$_BUILD_STATUS_FILE"
        if [ $exit_code -eq 0 ]; then
            echo "[BUILD] status: SUCCESS" >> "$_BUILD_STATUS_FILE"
            echo "[BUILD] exit_code: 0" >> "$_BUILD_STATUS_FILE"
        else
            echo "[BUILD] status: FAILED" >> "$_BUILD_STATUS_FILE"
            echo "[BUILD] exit_code: $exit_code" >> "$_BUILD_STATUS_FILE"
            
            grep -i "error\|failed\|fatal" "$_BUILD_LOG_FILE" > "$_BUILD_ERROR_FILE" 2>/dev/null || true
        fi
    ' > /dev/null 2>&1 &
    
    local pid=$!
    echo $pid > "$PID_FILE"
    
    echo -e "${GREEN}✅ 编译进程已启动 (PID: $pid)${NC}"
    echo ""
    echo "使用以下命令管理编译:"
    echo "  查看状态: $0 $OH_ROOT $SUITE_NAME $PRODUCT_NAME status"
    echo "  实时日志: $0 $OH_ROOT $SUITE_NAME $PRODUCT_NAME tail"
    echo "  等待完成: $0 $OH_ROOT $SUITE_NAME $PRODUCT_NAME wait"
    echo "  停止编译: $0 $OH_ROOT $SUITE_NAME $PRODUCT_NAME stop"
}

# 检查编译状态
check_status() {
    echo -e "${BLUE}=== 编译状态检查 ===${NC}"
    echo "测试套: $SUITE_NAME"
    
    # 检查 PID 文件
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${YELLOW}⚠️  未找到编译进程${NC}"
        if [ -f "$STATUS_FILE" ]; then
            echo ""
            cat "$STATUS_FILE"
        fi
        return 1
    fi
    
    local pid=$(cat "$PID_FILE")
    
    # 检查进程是否在运行
    if kill -0 "$pid" 2>/dev/null; then
        echo -e "${CYAN}🔄 编译进行中... (PID: $pid)${NC}"
        
        # 显示进度信息
        if [ -f "$LOG_FILE" ]; then
            local line_count=$(wc -l < "$LOG_FILE")
            local file_size=$(stat -c%s "$LOG_FILE" 2>/dev/null || echo "0")
            echo ""
            echo "日志行数: $line_count"
            echo "日志大小: $file_size bytes"
            echo ""
            echo "最近的日志输出:"
            echo "----------------------------------------"
            tail -n 5 "$LOG_FILE"
            echo "----------------------------------------"
        fi
    else
        echo -e "${GREEN}✅ 编译已完成${NC}"
        
        # 显示最终状态
        if [ -f "$STATUS_FILE" ]; then
            echo ""
            cat "$STATUS_FILE"
        fi
        
        # 如果有错误，显示错误信息
        if [ -f "$ERROR_FILE" ] && [ -s "$ERROR_FILE" ]; then
            echo ""
            echo -e "${RED}❌ 发现错误:${NC}"
            cat "$ERROR_FILE"
        fi
    fi
}

# 停止编译
stop_build() {
    echo -e "${YELLOW}=== 停止编译 ===${NC}"
    
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${YELLOW}⚠️  未找到编译进程${NC}"
        return 0
    fi
    
    local pid=$(cat "$PID_FILE")
    
    if kill -0 "$pid" 2>/dev/null; then
        echo "正在停止进程 $pid ..."
        kill "$pid" 2>/dev/null || true
        sleep 2
        
        # 强制杀死
        if kill -0 "$pid" 2>/dev/null; then
            kill -9 "$pid" 2>/dev/null || true
        fi
        
        echo -e "${GREEN}✅ 编译进程已停止${NC}"
        
        # 更新状态
        echo "[BUILD] status: STOPPED" >> "$STATUS_FILE"
    else
        echo -e "${YELLOW}⚠️  进程已不存在${NC}"
    fi
    
    rm -f "$PID_FILE"
}

# 实时查看日志
tail_logs() {
    echo -e "${BLUE}=== 实时编译日志 ===${NC}"
    echo "测试套: $SUITE_NAME"
    echo "按 Ctrl+C 退出"
    echo "----------------------------------------"
    
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo -e "${YELLOW}⚠️  日志文件不存在${NC}"
        echo "等待编译启动..."
        while [ ! -f "$LOG_FILE" ]; do
            sleep 1
        done
        tail -f "$LOG_FILE"
    fi
}

# 等待编译完成
wait_build() {
    echo -e "${BLUE}=== 等待编译完成 ===${NC}"
    echo "测试套: $SUITE_NAME"
    
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${YELLOW}⚠️  未找到编译进程${NC}"
        
        # 检查是否有完成状态
        if [ -f "$STATUS_FILE" ] && grep -q "SUCCESS\|FAILED" "$STATUS_FILE"; then
            echo ""
            cat "$STATUS_FILE"
            return 0
        fi
        
        return 1
    fi
    
    local pid=$(cat "$PID_FILE")
    local dots=0
    local spinner=('⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏')
    local spin_idx=0
    
    echo -n "等待编译完成 "
    
    while kill -0 "$pid" 2>/dev/null; do
        printf "\r${spinner[$spin_idx]} 等待中"
        spin_idx=$(( (spin_idx + 1) % 10 ))
        sleep 0.5
    done
    
    echo -e "\r✅ 编译已完成    "
    
    # 显示最终状态
    if [ -f "$STATUS_FILE" ]; then
        echo ""
        cat "$STATUS_FILE"
    fi
    
    # 检查编译结果
    if grep -q "SUCCESS" "$STATUS_FILE" 2>/dev/null; then
        echo -e "${GREEN}✅ 编译成功!${NC}"
        return 0
    elif grep -q "FAILED" "$STATUS_FILE" 2>/dev/null; then
        echo -e "${RED}❌ 编译失败${NC}"
        
        # 显示错误信息
        if [ -f "$ERROR_FILE" ] && [ -s "$ERROR_FILE" ]; then
            echo ""
            echo -e "${RED}错误信息:${NC}"
            cat "$ERROR_FILE"
        fi
        
        return 1
    fi
}

# 查看完整日志
view_logs() {
    echo -e "${BLUE}=== 完整编译日志 ===${NC}"
    
    if [ -f "$LOG_FILE" ]; then
        cat "$LOG_FILE"
    else
        echo -e "${YELLOW}⚠️  日志文件不存在${NC}"
    fi
}

# 查看错误日志
view_errors() {
    echo -e "${RED}=== 错误日志 ===${NC}"
    
    if [ -f "$ERROR_FILE" ] && [ -s "$ERROR_FILE" ]; then
        cat "$ERROR_FILE"
    else
        echo -e "${GREEN}✅ 未发现错误${NC}"
    fi
}

# 主函数
main() {
    validate_params
    
    case "$ACTION" in
        start)
            start_build
            ;;
        status)
            check_status
            ;;
        stop)
            stop_build
            ;;
        tail)
            tail_logs
            ;;
        wait)
            wait_build
            ;;
        logs)
            view_logs
            ;;
        errors)
            view_errors
            ;;
        *)
            echo -e "${RED}❌ 未知动作: $ACTION${NC}"
            usage
            ;;
    esac
}

main
