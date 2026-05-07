#!/bin/bash
# 三重Napi校验脚本
# 用法：./verify_napi_triple.sh <测试套路径>
# 功能：验证 N-API 封装测试的三个关键步骤是否同步完成
#       步骤4：参数类型一致性校验（新增）

set -e
ERRORS=0

SUITE_PATH="${1:-}"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "三重Napi校验 + 类型一致性检查"
echo "========================================="
echo "测试套路径: ${SUITE_PATH}"
echo ""

cpp_file="${SUITE_PATH}/entry/src/main/cpp/NapiTest.cpp"
if [ ! -f "$cpp_file" ]; then
    cpp_file="${SUITE_PATH}/entry/src/main/cpp/napi_init.cpp"
fi

ts_file="${SUITE_PATH}/entry/src/main/cpp/types/libentry/index.d.ts"
test_dir="${SUITE_PATH}/entry/src/ohosTest/ets/test"

echo "【步骤 1：N-API 函数注册校验】"
if [ -f "$cpp_file" ]; then
    defined_funcs=$(grep -oP 'static napi_value\s+\K[A-Za-z0-9_]+(?=\s*\()' "$cpp_file" 2>/dev/null | grep -vE '^(Init|RegisterModule|napi_module_register)$' | sort | uniq || true)
    registered_funcs=$(grep -A 200 'napi_property_descriptor desc\[\]' "$cpp_file" 2>/dev/null | grep -oP '(DECLARE_NAPI_PROPERTY\s*\(\s*"[^"]+"|"[^"]+"\s*,\s*nullptr\s*,\s*[A-Za-z0-9_]+)' | grep -oP '[A-Za-z0-9_]+$' | sort | uniq || true)
    if [ -z "$registered_funcs" ]; then
        registered_funcs=$(grep -A 200 'napi_property_descriptor desc\[\]' "$cpp_file" 2>/dev/null | grep -oP '"\K[A-Za-z0-9_]+(?="\s*,\s*nullptr)' | sort | uniq || true)
    fi
    
    if [ -n "$defined_funcs" ]; then
        missing=$(comm -23 <(echo "$defined_funcs") <(echo "$registered_funcs") 2>/dev/null || true)
        if [ -n "$missing" ]; then
            echo -e "${RED}❌ 定义但未注册的函数：${NC}"
            echo "$missing"
            ERRORS=$((ERRORS + 1))
        else
            def_count=$(echo "$defined_funcs" | wc -l)
            echo -e "${GREEN}✅ 所有函数都已注册 (共 ${def_count} 个)${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ 未找到 N-API 函数定义${NC}"
    fi
else
    echo -e "${RED}❌ 找不到 NapiTest.cpp 或 napi_init.cpp${NC}"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "【步骤 2：TypeScript 接口声明校验】"
if [ -f "$ts_file" ] && [ -f "$cpp_file" ]; then
    js_names=$(grep -A 200 'napi_property_descriptor desc\[\]' "$cpp_file" 2>/dev/null | grep -oP 'DECLARE_NAPI_PROPERTY\s*\(\s*"\K[^"]+' | sort | uniq || true)
    if [ -z "$js_names" ]; then
        js_names=$(grep -A 200 'napi_property_descriptor desc\[\]' "$cpp_file" 2>/dev/null | grep -oP '"\K[A-Za-z0-9_]+(?="\s*,\s*nullptr)' | sort | uniq || true)
    fi
    declared_names=$(grep 'export const' "$ts_file" 2>/dev/null | grep -oP 'export const\s+\K[A-Za-z0-9_]+' | sort | uniq || true)
    
    if [ -n "$js_names" ]; then
        missing=$(comm -23 <(echo "$js_names") <(echo "$declared_names") 2>/dev/null || true)
        if [ -n "$missing" ]; then
            echo -e "${RED}❌ 注册但未声明的函数：${NC}"
            echo "$missing"
            ERRORS=$((ERRORS + 1))
        else
            js_count=$(echo "$js_names" | wc -l)
            echo -e "${GREEN}✅ 所有函数都已声明 (共 ${js_count} 个)${NC}"
        fi
    fi
else
    echo -e "${RED}❌ 找不到 index.d.ts${NC}"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "【步骤 3：ETS 测试接口使用校验】"
if [ -d "$test_dir" ]; then
    if ls "$test_dir"/*.test.ets 1>/dev/null 2>&1; then
        used_interfaces=$(grep -h 'testNapi\.' "$test_dir"/*.test.ets 2>/dev/null | grep -v '^\s*//' | grep -oP 'testNapi\.\K[A-Za-z0-9_]+' | sort | uniq || true)
        declared_interfaces=$(grep 'export const' "$ts_file" 2>/dev/null | grep -oP 'export const\s+\K[A-Za-z0-9_]+' | sort | uniq || true)
        
        if [ -n "$used_interfaces" ]; then
            missing=$(comm -23 <(echo "$used_interfaces") <(echo "$declared_interfaces") 2>/dev/null || true)
            if [ -n "$missing" ]; then
                echo -e "${RED}❌ 使用但未声明的接口：${NC}"
                echo "$missing"
                ERRORS=$((ERRORS + 1))
            else
                used_count=$(echo "$used_interfaces" | wc -l)
                echo -e "${GREEN}✅ 所有接口都已声明 (共使用 ${used_count} 个)${NC}"
            fi
        else
            echo -e "${YELLOW}⚠️ 未找到 N-API 接口调用${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ 未找到测试文件${NC}"
    fi
else
    echo -e "${RED}❌ 找不到测试目录${NC}"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "【步骤 4：参数类型一致性校验】"

cpp_count=0
ts_count=0
ets_count=0

check_type_consistency() {
    if [ ! -f "$cpp_file" ] || [ ! -f "$ts_file" ]; then
        echo -e "${YELLOW}⚠️ 缺少 C++ 或 TS 文件，跳过类型一致性检查${NC}"
        return
    fi

    if [ ! -d "$test_dir" ]; then
        echo -e "${YELLOW}⚠️ 缺少 ETS 测试目录，部分检查跳过${NC}"
    fi

    local type_issues=0

    # 提取 Init 中注册的 JS 函数名（用于与 TS/ETS 对比）
    local js_func_names
    js_func_names=$(grep -A 200 'napi_property_descriptor desc\[\]' "$cpp_file" 2>/dev/null | grep -oP 'DECLARE_NAPI_(FUNCTION|PROPERTY)\s*\(\s*"\K[^"]+' | sort | uniq || true)
    if [ -z "$js_func_names" ]; then
        js_func_names=$(grep -A 200 'napi_property_descriptor desc\[\]' "$cpp_file" 2>/dev/null | grep -oP '"\K[A-Za-z0-9_]+(?="\s*,\s*nullptr)' | sort | uniq || true)
    fi

    while IFS= read -r js_name; do
        [ -z "$js_name" ] && continue
        cpp_count=$((cpp_count + 1))

        local ts_decl_line
        ts_decl_line=$(grep -E "export (const|function) ${js_name}\b" "$ts_file" 2>/dev/null | head -1)

        if [ -z "$ts_decl_line" ]; then
            echo -e "${RED}  ISSUE [${js_name}]: Init 注册了但 TS index.d.ts 中缺少声明${NC}"
            type_issues=$((type_issues + 1))
            continue
        fi
        ts_count=$((ts_count + 1))

        # 检查 TS 声明中的参数类型是否包含 nullable 标记（? 修饰符或 | null）
        local ts_param_part
        ts_param_part=$(echo "$ts_decl_line" | grep -oP '\(.*?\)' | head -1)
        local ts_has_nullable=0
        if echo "$ts_param_part" | grep -qiE '\?|null|undefined'; then
            ts_has_nullable=1
        fi
        # 也检查返回类型是否标记了 nullable
        local ts_return_part
        ts_return_part=$(echo "$ts_decl_line" | grep -oP '=>\s*\K.*' | sed 's/;$//')
        if echo "$ts_return_part" | grep -qiE '\|.*null|null.*\||\?'; then
            ts_has_nullable=1
        fi

        # 检查 ETS 中是否有调用此函数
        local ets_calls=""
        local ets_passes_null=0
        if [ -d "$test_dir" ] && ls "$test_dir"/*.test.ets 1>/dev/null 2>&1; then
            ets_calls=$(grep -h "testNapi\.${js_name}" "$test_dir"/*.test.ets 2>/dev/null || true)
            if [ -n "$ets_calls" ]; then
                ets_count=$((ets_count + 1))
                if echo "$ets_calls" | grep -qiE 'null|undefined'; then
                    ets_passes_null=1
                fi
            fi
        fi

        # 关键校验：ETS 传了 null/undefined 但 TS 声明没标记 nullable
        if [ "$ets_passes_null" -eq 1 ] && [ "$ts_has_nullable" -eq 0 ]; then
            echo -e "${RED}  ISSUE [${js_name}]: ETS 测试传了 null/undefined，但 TS 声明 '${ts_decl_line}' 未标记 nullable${NC}"
            type_issues=$((type_issues + 1))
        fi

        # TS 声明标记了 nullable 但 ETS 测试没有 null 用例（警告级别）
        if [ "$ts_has_nullable" -eq 1 ] && [ "$ets_passes_null" -eq 0 ] && [ -n "$ets_calls" ]; then
            echo -e "${YELLOW}  WARN [${js_name}]: TS 声明含 nullable，但 ETS 测试未覆盖 null 场景${NC}"
        fi

        # 参数数量一致性
        if [ -n "$ts_param_part" ] && [ -n "$ets_calls" ]; then
            local param_count_ts
            param_count_ts=$(echo "$ts_param_part" | tr ',' '\n' | grep -c '[a-zA-Z]' || echo "0")
            local ets_call_args
            ets_call_args=$(echo "$ets_calls" | grep -oP "testNapi\.${js_name}\K\(.*?\)" | head -1)
            if [ -n "$ets_call_args" ]; then
                local param_count_ets
                param_count_ets=$(echo "$ets_call_args" | tr ',' '\n' | grep -c '[a-zA-Z0-9]' || echo "0")
                if [ "$param_count_ts" != "$param_count_ets" ]; then
                    echo -e "${RED}  ISSUE [${js_name}]: 参数数量不一致 TS=${param_count_ts} ETS=${param_count_ets}${NC}"
                    type_issues=$((type_issues + 1))
                fi
            fi
        fi
    done < <(echo "$js_func_names")

    echo ""
    echo "  检查统计: JS 注册 ${cpp_count} 个, TS 声明 ${ts_count} 个, ETS 调用 ${ets_count} 个"

    if [ "$type_issues" -eq 0 ]; then
        echo -e "${GREEN}✅ 类型一致性检查通过${NC}"
    else
        echo -e "${RED}❌ 发现 ${type_issues} 个类型一致性问题${NC}"
        ERRORS=$((ERRORS + 1))
    fi
}

check_type_consistency

echo ""
echo "=== 类型一致性校验统计 ==="
echo "检查的函数数量: C++ ${cpp_count}, TS ${ts_count}, ETS ${ets_count}"

echo ""
echo "========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ 全部校验通过！${NC}"
    exit 0
else
    echo -e "${RED}❌ 发现 $ERRORS 个错误${NC}"
    exit 1
fi
