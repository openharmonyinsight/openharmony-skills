#!/bin/bash

# ==============================================================================
# OpenHarmony XTS 异步编译脚本
# 基于 nohup 后台编译 + 文件状态轮询
# ==============================================================================
#
# 使用方法:
#   ./async_build.sh <OH_ROOT> <测试套名称> [产品名称] [动作] [额外参数...]
#
# 参数:
#   OH_ROOT       - OpenHarmony 工程根目录（必需）
#   测试套名称     - 要编译的测试套名称（必需）
#   产品名称       - 默认 rk3568（可选）
#   动作           - start|status|stop|tail|wait|logs|errors（可选，默认 start）
#   额外参数       - 传递给 build.sh 的额外参数，如 xts_suitetype=hap_static
#
# 动作说明:
#   start  - 启动异步编译（默认）
#   status - 检查编译状态
#   stop   - 停止编译进程
#   tail   - 实时查看编译日志
#   wait   - 等待编译完成并返回结果
#   logs   - 查看完整日志
#   errors - 查看错误日志
#
# 示例:
#   # 启动异步编译（动态测试套）
#   ./async_build.sh /path/to/openharmony ActsUiTest
#
#   # 启动异步编译（静态测试套）
#   ./async_build.sh /path/to/openharmony ActsUiStaticTest rk3568 start xts_suitetype=hap_static
#
#   # 检查编译状态
#   ./async_build.sh /path/to/openharmony ActsUiTest rk3568 status
#
#   # 等待编译完成
#   ./async_build.sh /path/to/openharmony ActsUiTest rk3568 wait
#
#   # 查看错误日志
#   ./async_build.sh /path/to/openharmony ActsUiTest rk3568 errors
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
shift 4 2>/dev/null || true
EXTRA_PARAMS="$@"

# 日志和 PID 文件路径
LOG_DIR="/tmp/oh_xts_build"
LOG_FILE="${LOG_DIR}/${SUITE_NAME}.log"
PID_FILE="${LOG_DIR}/${SUITE_NAME}.pid"
STATUS_FILE="${LOG_DIR}/${SUITE_NAME}.status"
ERROR_FILE="${LOG_DIR}/${SUITE_NAME}.error"

# 使用说明
usage() {
    echo -e "${CYAN}OpenHarmony XTS 异步编译脚本${NC}"
    echo ""
    echo "使用方法:"
    echo "  $0 <OH_ROOT> <测试套名称> [产品名称] [动作] [额外参数...]"
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
    echo "  # 动态测试套"
    echo "  $0 /path/to/openharmony ActsUiTest"
    echo ""
    echo "  # 静态测试套"
    echo "  $0 /path/to/openharmony ActsUiStaticTest rk3568 start xts_suitetype=hap_static"
    echo ""
    echo "  # 查看状态"
    echo "  $0 /path/to/openharmony ActsUiTest rk3568 status"
    exit 1
}

# 验证参数
validate_params() {
    if [ -z "$OH_ROOT" ] || [ -z "$SUITE_NAME" ]; then
        usage
    fi
    
    if [ ! -d "$OH_ROOT" ]; then
        echo -e "${RED}❌ OH_ROOT 目录不存在: $OH_ROOT${NC}"
        exit 1
    fi
    
    if [ ! -f "$OH_ROOT/test/xts/acts/build.sh" ]; then
        echo -e "${RED}❌ 编译脚本不存在: $OH_ROOT/test/xts/acts/build.sh${NC}"
        exit 1
    fi

    resolve_suite_name
}

resolve_suite_name() {
    if [[ "$SUITE_NAME" == Acts* ]]; then
        return 0
    fi

    local acts_dir="$OH_ROOT/test/xts/acts"
    if [ ! -d "$acts_dir" ]; then
        return 0
    fi

    local found_gn
    found_gn=$(find "$acts_dir" -path "*${SUITE_NAME}" -name "BUILD.gn" 2>/dev/null | head -1)
    if [ -z "$found_gn" ]; then
        return 0
    fi

    local target_name
    target_name=$(grep -oP 'ohos_js_app_suite\("\K[^"]+' "$found_gn" 2>/dev/null | head -1)
    if [ -z "$target_name" ]; then
        return 0
    fi

    echo -e "${YELLOW}ℹ️  SUITE_NAME 解析: '$SUITE_NAME' -> '$target_name'${NC}"
    echo -e "${YELLOW}   BUILD.gn: $found_gn${NC}"

    SUITE_NAME="$target_name"
    LOG_FILE="${LOG_DIR}/${SUITE_NAME}.log"
    PID_FILE="${LOG_DIR}/${SUITE_NAME}.pid"
    STATUS_FILE="${LOG_DIR}/${SUITE_NAME}.status"
    ERROR_FILE="${LOG_DIR}/${SUITE_NAME}.error"
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
    if [ -n "$EXTRA_PARAMS" ]; then
        echo "额外参数: $EXTRA_PARAMS"
    fi
    
    # 检查是否已有编译进程
    if [ -f "$PID_FILE" ]; then
        local existing_pid=$(cat "$PID_FILE")
        if kill -0 "$existing_pid" 2>/dev/null; then
            echo -e "${YELLOW}⚠️  已有编译进程在运行 (PID: $existing_pid)${NC}"
            echo "使用 '$0 $OH_ROOT $SUITE_NAME $PRODUCT_NAME status' 查看状态"
            return 0
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    create_log_dir
    
    # 清空日志文件
    > "$LOG_FILE"
    > "$ERROR_FILE"
    
    echo -e "${GREEN}🚀 启动后台编译进程...${NC}"
    
    # 构建额外参数
    local build_extra=""
    if [ -n "$EXTRA_PARAMS" ]; then
        build_extra=" $EXTRA_PARAMS"
    fi
    
    cd "$OH_ROOT"
    nohup bash -c "
        set -o pipefail
        
        echo '[BUILD] 开始时间: '\$(date '+%Y-%m-%d %H:%M:%S') > '$STATUS_FILE'
        echo '[BUILD] 测试套: $SUITE_NAME' >> '$STATUS_FILE'
        echo '[BUILD] 状态: RUNNING' >> '$STATUS_FILE'
        
        cd '$OH_ROOT'
        ./test/xts/acts/build.sh product_name=$PRODUCT_NAME system_size=standard suite=$SUITE_NAME${build_extra} 2>&1 | tee -a '$LOG_FILE'
        exit_code=\${PIPESTATUS[0]}
        
        echo '[BUILD] 结束时间: '\$(date '+%Y-%m-%d %H:%M:%S') >> '$STATUS_FILE'
        if [ \$exit_code -eq 0 ]; then
            echo '[BUILD] 状态: SUCCESS' >> '$STATUS_FILE'
            echo '[BUILD] 退出码: 0' >> '$STATUS_FILE'
        else
            echo '[BUILD] 状态: FAILED' >> '$STATUS_FILE'
            echo '[BUILD] 退出码: '\$exit_code >> '$STATUS_FILE'
            grep -i 'error\|failed\|fatal' '$LOG_FILE' > '$ERROR_FILE' 2>/dev/null || true
        fi
    " > /dev/null 2>&1 &
    
    echo $! > "$PID_FILE"
    local pid=$(cat "$PID_FILE")
    echo -e "${GREEN}✅ 编译进程已启动 (PID: $pid)${NC}"
    echo "日志文件: $LOG_FILE"
    echo ""
    echo "使用以下命令管理编译:"
    echo "  查看状态: $0 $OH_ROOT $SUITE_NAME $PRODUCT_NAME status"
    echo "  实时日志: $0 $OH_ROOT $SUITE_NAME $PRODUCT_NAME tail"
    echo "  等待完成: $0 $OH_ROOT $SUITE_NAME $PRODUCT_NAME wait"
    echo "  查看错误: $0 $OH_ROOT $SUITE_NAME $PRODUCT_NAME errors"
}

# 检查编译状态
check_status() {
    if [ ! -f "$STATUS_FILE" ]; then
        echo -e "${YELLOW}⚠️  未找到编译状态文件，编译可能未启动${NC}"
        return 1
    fi
    
    echo -e "${BLUE}=== 编译状态 ===${NC}"
    cat "$STATUS_FILE"
    echo ""
    
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "${YELLOW}⏳ 编译进程运行中 (PID: $pid)${NC}"
        else
            echo -e "${GREEN}📦 编译进程已结束${NC}"
        fi
    fi
}

# 停止编译
stop_build() {
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${YELLOW}⚠️  未找到编译进程${NC}"
        return 0
    fi
    
    local pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
        echo -e "${YELLOW}⏹️  停止编译进程 (PID: $pid)...${NC}"
        kill -TERM "$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null || true
        rm -f "$PID_FILE"
        
        # 更新状态文件
        if [ -f "$STATUS_FILE" ]; then
            echo "[BUILD] 结束时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$STATUS_FILE"
            echo "[BUILD] 状态: STOPPED" >> "$STATUS_FILE"
        fi
        
        echo -e "${GREEN}✅ 编译进程已停止${NC}"
    else
        rm -f "$PID_FILE"
        echo -e "${YELLOW}⚠️  编译进程已结束${NC}"
    fi
}

# 实时查看日志
tail_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${YELLOW}⚠️  日志文件不存在${NC}"
        return 1
    fi
    
    echo -e "${BLUE}=== 实时日志 (Ctrl+C 退出) ===${NC}"
    tail -f "$LOG_FILE"
}

# 等待编译完成
wait_build() {
    echo -e "${BLUE}=== 等待编译完成 ===${NC}"
    
    local spinner_chars=('⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏')
    local i=0
    
    while true; do
        if [ -f "$STATUS_FILE" ]; then
            local final_status=$(grep '\[BUILD\] 状态:' "$STATUS_FILE" | tail -1 | sed 's/.*状态: //')
            
            if [ "$final_status" = "SUCCESS" ]; then
                echo -e "\n${GREEN}✅ 编译成功!${NC}"
                grep '\[BUILD\]' "$STATUS_FILE"
                return 0
            elif [ "$final_status" = "FAILED" ]; then
                echo -e "\n${RED}❌ 编译失败!${NC}"
                grep '\[BUILD\]' "$STATUS_FILE"
                echo ""
                if [ -f "$ERROR_FILE" ] && [ -s "$ERROR_FILE" ]; then
                    echo -e "${RED}错误摘要:${NC}"
                    head -20 "$ERROR_FILE"
                fi
                return 1
            elif [ "$final_status" = "STOPPED" ]; then
                echo -e "\n${YELLOW}⏹️  编译已停止${NC}"
                return 1
            fi
        fi
        
        printf "\r${spinner_chars[$((i % 10))]} 编译中..."
        i=$((i + 1))
        sleep 2
    done
}

# 查看完整日志
view_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${YELLOW}⚠️  日志文件不存在${NC}"
        return 1
    fi
    cat "$LOG_FILE"
}

# 查看错误日志
view_errors() {
    if [ ! -f "$ERROR_FILE" ] || [ ! -s "$ERROR_FILE" ]; then
        echo -e "${GREEN}✅ 未发现错误${NC}"
        return 0
    fi
    echo -e "${RED}=== 错误日志 ===${NC}"
    cat "$ERROR_FILE"
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
