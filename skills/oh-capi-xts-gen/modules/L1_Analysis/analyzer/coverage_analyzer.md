# 测试覆盖率分析模块

> 📖 **相关文档**：
> - [头文件解析模块](./unified_api_parser_c.md) - API 信息提取和结构化
> - [测试生成核心](../L2_Generation/test_generation_c.md) - 基于覆盖率报告生成测试用例

> **模块信息**
> - 层级：L1_Analysis
> - 优先级：按需加载
> - 适用范围：OpenHarmony CAPI XTS 测试覆盖率分析
> - 依赖：conventions, L1_Analysis/unified_api_parser_c.md
> - 触发条件：标准流程（未提供覆盖率报告时）或显式请求覆盖率分析

---

## 一、模块概述

测试覆盖率分析模块负责分析现有测试文件的覆盖情况,识别已覆盖和未覆盖的 API、参数组合和测试场景,为测试用例生成提供精准的目标列表。

### 1.1 核心功能

- **覆盖率扫描** - 扫描现有测试文件,提取测试覆盖的 API 和测试场景
- **API 覆盖分析** - 识别已覆盖和未覆盖的 API
- **参数组合分析** - 分析已覆盖和缺失的参数组合
- **测试场景分析** - 识别 PARAM、ERROR、RETURN、BOUNDARY、MEMORY 等测试类型的覆盖情况
- **覆盖率报告生成** - 生成结构化的覆盖率分析报告
- **增量更新支持** - 支持增量覆盖率分析,只分析新增测试用例

### 1.2 应用场景

1. **标准流程覆盖率分析** - 在未提供覆盖率报告时,自动执行覆盖率分析
2. **覆盖率验证** - 验证测试套的覆盖完整性
3. **缺失测试识别** - 识别需要补充的测试用例
4. **覆盖率趋势分析** - 追踪覆盖率随时间的变化
5. **子系统对比分析** - 对比不同子系统的覆盖率情况

---

## 二、覆盖率扫描

### 2.1 测试文件扫描

扫描目标测试套的所有测试文件,提取以下信息:

```bash
# 扫描测试文件
scan_test_files() {
    local test_suite_dir=$1

    echo "=== 扫描测试文件: $test_suite_dir ==="

    # 扫描 N-API 封装测试文件
    scan_napi_test_files "$test_suite_dir"

    # 扫描 ETS/ArkTS 测试文件
    scan_ets_test_files "$test_suite_dir"

    # 扫描测试设计文档
    scan_test_design_docs "$test_suite_dir"

    echo "✅ 测试文件扫描完成"
}

scan_napi_test_files() {
    local test_suite_dir=$1

    echo "🔍 扫描 N-API 封装测试文件..."

    local napi_test_files=$(find "$test_suite_dir" -name "NapiTest.cpp")
    for napi_file in $napi_test_files; do
        echo "  📄 $napi_file"
        extract_napi_test_info "$napi_file"
    done
}

scan_ets_test_files() {
    local test_suite_dir=$1

    echo "🔍 扫描 ETS/ArkTS 测试文件..."

    local ets_test_files=$(find "$test_suite_dir" -name "*.test.ets")
    for ets_file in $ets_test_files; do
        echo "  📄 $ets_file"
        extract_ets_test_info "$ets_file"
    done
}

scan_test_design_docs() {
    local test_suite_dir=$1

    echo "🔍 扫描测试设计文档..."

    local design_docs=$(find "$test_suite_dir" -name "测试设计*.md" -o -name "*design*.md")
    for design_doc in $design_docs; do
        echo "  📄 $design_doc"
        extract_design_doc_info "$design_doc"
    done
}
```

### 2.2 测试用例信息提取

从测试文件中提取测试用例的详细信息:

```bash
# 提取 N-API 测试用例信息
extract_napi_test_info() {
    local napi_file=$1

    echo "  🔍 提取 N-API 测试信息: $napi_file"

    # 提取函数名
    local function_names=$(grep -E "static napi_value [A-Za-z_]+.*\(" "$napi_file" | sed 's/.*napi_value \([A-Za-z_]*\).*/\1/')
    echo "    📦 函数: $function_names"

    # 提取测试用例编号
    local test_numbers=$(grep -E "@tc\.name:.*SUB_[A-Z0-9_]+" "$napi_file" | sed 's/.*SUB_[A-Z0-9_]*/&/' | sort | uniq)
    echo "    🔢 测试用例数: $(echo "$test_numbers" | wc -l)"

    # 提取测试类型
    local test_types=$(grep -E "@tc\.type:.*(PARAM|ERROR|RETURN|BOUNDARY|MEMORY)" "$napi_file" | sed 's/.*\(PARAM\|ERROR\|RETURN\|BOUNDARY\|MEMORY\).*/\1/' | sort | uniq -c)
    echo "    📊 测试类型: $test_types"
}

# 提取 ETS 测试用例信息
extract_ets_test_info() {
    local ets_file=$1

    echo "  🔍 提取 ETS 测试信息: $ets_file"

    # 提取测试用例名称
    local test_names=$(grep -E "it\(['\"]" "$ets_file" | sed 's/.*it(\(['\"][^'\"]*['\"]).*/\1/')
    echo "    📦 测试用例: $test_names"

    # 提取测试用例编号
    local test_numbers=$(grep -E "@tc\.name:.*SUB_[A-Z0-9_]+" "$ets_file" | sed 's/.*SUB_[A-Z0-9_]*/&/' | sort | uniq)
    echo "    🔢 测试用例数: $(echo "$test_numbers" | wc -l)"
}

# 提取测试设计文档信息
extract_design_doc_info() {
    local design_doc=$1

    echo "  🔍 提取测试设计文档信息: $design_doc"

    # 提取 API 列表
    local apis=$(grep -E "^## [A-Za-z]+ API" "$design_doc" | sed 's/^## //')
    echo "    📦 涉及 API: $apis"

    # 提取测试用例数量
    local test_count=$(grep -E "^### 用例 [0-9]+" "$design_doc" | wc -l)
    echo "    🔢 测试用例数: $test_count"
}
```

---

## 三、覆盖率分析

### 3.1 API 覆盖分析

对比 API 列表和测试覆盖情况:

```bash
# API 覆盖分析
analyze_api_coverage() {
    local api_list_file=$1
    local test_info_file=$2

    echo "=== API 覆盖分析 ==="

    # 读取 API 列表
    local apis=$(cat "$api_list_file" | jq -r '.[] | .function_name')

    # 读取测试覆盖的 API
    local covered_apis=$(jq -r '.covered_apis[]' "$test_info_file" | sort | uniq)

    # 计算覆盖率
    local total_api_count=$(echo "$apis" | wc -l)
    local covered_api_count=$(echo "$covered_apis" | wc -l)
    local coverage_rate=$(echo "scale=2; $covered_api_count * 100 / $total_api_count" | bc)

    echo "📊 API 覆盖率: $coverage_rate% ($covered_api_count/$total_api_count)"

    # 识别未覆盖的 API
    local uncovered_apis=$(comm -23 <(echo "$apis" | sort) <(echo "$covered_apis"))
    if [ -n "$uncovered_apis" ]; then
        echo "⚠️  未覆盖的 API:"
        echo "$uncovered_apis" | while read api; do
            echo "  ❌ $api"
        done
    fi

    # 生成覆盖率报告
    generate_api_coverage_report "$api_list_file" "$test_info_file" "$coverage_rate" "$uncovered_apis"
}

# 生成 API 覆盖率报告
generate_api_coverage_report() {
    local api_list_file=$1
    local test_info_file=$2
    local coverage_rate=$3
    local uncovered_apis=$4

    local report_file="test/coverage/api_coverage_report.md"

    echo "# API 覆盖率报告" > "$report_file"
    echo "" >> "$report_file"
    echo "**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')" >> "$report_file"
    echo "**覆盖率**: $coverage_rate%" >> "$report_file"
    echo "" >> "$report_file"
    echo "## 覆盖详情" >> "$report_file"
    echo "" >> "$report_file"
    echo "| API | 状态 | 测试用例数 |" >> "$report_file"
    echo "|-----|------|------------|" >> "$report_file"

    # 遍历所有 API
    cat "$api_list_file" | jq -c '.' | while read -r api_info; do
        local api_name=$(echo "$api_info" | jq -r '.function_name')
        local test_count=$(jq -r --arg api "$api_name" '.covered_apis | select(. == $api) | length' "$test_info_file")

        if [ "$test_count" -gt 0 ]; then
            echo "| $api_name | ✅ 已覆盖 | $test_count |" >> "$report_file"
        else
            echo "| $api_name | ❌ 未覆盖 | 0 |" >> "$report_file"
        fi
    done

    echo "" >> "$report_file"
    echo "## 未覆盖的 API" >> "$report_file"
    echo "" >> "$report_file"

    if [ -n "$uncovered_apis" ]; then
        echo "$uncovered_apis" | while read api; do
            echo "- $api" >> "$report_file"
        done
    else
        echo "✅ 所有 API 已覆盖" >> "$report_file"
    fi

    echo "✅ API 覆盖率报告已生成: $report_file"
}
```

### 3.2 参数组合覆盖分析

分析每个 API 的参数组合覆盖情况:

```bash
# 参数组合覆盖分析
analyze_param_coverage() {
    local api_list_file=$1
    local test_info_file=$2

    echo "=== 参数组合覆盖分析 ==="

    # 读取 API 列表
    cat "$api_list_file" | jq -c '.' | while read -r api_info; do
        local api_name=$(echo "$api_info" | jq -r '.function_name')
        local params=$(echo "$api_info" | jq -r '.parameters[] | "\(.type):\(.name)"')

        echo "🔍 分析 API: $api_name"

        # 计算可能的参数组合
        local param_count=$(echo "$params" | wc -l)
        local total_combinations=$(echo "2^$param_count" | bc)
        echo "  📊 可能的参数组合: $total_combinations"

        # 提取已覆盖的参数组合
        local covered_combinations=$(jq -r --arg api "$api_name" '.param_combinations | select(.api == $api) | .combination' "$test_info_file" | sort | uniq)
        local covered_count=$(echo "$covered_combinations" | wc -l)

        echo "  ✅ 已覆盖的参数组合: $covered_count"

        # 计算覆盖率
        if [ "$total_combinations" -gt 0 ]; then
            local coverage_rate=$(echo "scale=2; $covered_count * 100 / $total_combinations" | bc)
            echo "  📊 参数覆盖率: $coverage_rate%"
        fi

        # 识别缺失的参数组合
        if [ "$covered_count" -lt "$total_combinations" ]; then
            echo "  ⚠️  缺失的参数组合:"
            # 这里可以进一步分析具体的缺失组合
        fi
    done

    # 生成参数覆盖率报告
    generate_param_coverage_report "$api_list_file" "$test_info_file"
}
```

### 3.3 测试场景覆盖分析

分析不同测试类型(PARAM、ERROR、RETURN、BOUNDARY、MEMORY)的覆盖情况:

```bash
# 测试场景覆盖分析
analyze_test_scenario_coverage() {
    local test_info_file=$1

    echo "=== 测试场景覆盖分析 ==="

    # 定义测试类型
    local test_types=("PARAM" "ERROR" "RETURN" "BOUNDARY" "MEMORY")

    # 分析每个测试类型的覆盖情况
    for test_type in "${test_types[@]}"; do
        echo "🔍 分析测试类型: $test_type"

        # 统计该类型的测试用例数
        local test_count=$(jq -r --arg type "$test_type" '.test_cases[] | select(.type == $type) | length' "$test_info_file")

        echo "  📊 $test_type 测试用例数: $test_count"

        # 分析覆盖的 API
        local covered_apis=$(jq -r --arg type "$test_type" '.test_cases[] | select(.type == $type) | .api' "$test_info_file" | sort | uniq)
        echo "  ✅ 覆盖的 API: $(echo "$covered_apis" | tr '\n' ', ' | sed 's/,$//')"
    done

    # 生成测试场景覆盖率报告
    generate_scenario_coverage_report "$test_info_file"
}

# 生成测试场景覆盖率报告
generate_scenario_coverage_report() {
    local test_info_file=$1

    local report_file="test/coverage/test_scenario_coverage.md"

    echo "# 测试场景覆盖率报告" > "$report_file"
    echo "" >> "$report_file"
    echo "**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')" >> "$report_file"
    echo "" >> "$report_file"

    echo "## 测试类型分布" >> "$report_file"
    echo "" >> "$report_file"
    echo "| 测试类型 | 测试用例数 | 占比 |" >> "$report_file"
    echo "|---------|------------|------|" >> "$report_file"

    local total_tests=$(jq '.test_cases | length' "$test_info_file")

    local test_types=("PARAM" "ERROR" "RETURN" "BOUNDARY" "MEMORY")
    for test_type in "${test_types[@]}"; do
        local test_count=$(jq -r --arg type "$test_type" '.test_cases[] | select(.type == $type) | length' "$test_info_file")
        local percentage=$(echo "scale=2; $test_count * 100 / $total_tests" | bc)

        echo "| $test_type | $test_count | $percentage% |" >> "$report_file"
    done

    echo "" >> "$report_file"
    echo "## 各 API 测试类型覆盖" >> "$report_file"
    echo "" >> "$report_file"

    # 遍历每个 API,列出其测试类型覆盖
    local apis=$(jq -r '.test_cases[].api' "$test_info_file" | sort | uniq)
    for api in $apis; do
        echo "### $api" >> "$report_file"
        echo "" >> "$report_file"
        echo "| 测试类型 | 已覆盖 |" >> "$report_file"
        echo "|---------|--------|" >> "$report_file"

        for test_type in "${test_types[@]}"; do
            local covered=$(jq -r --arg api "$api" --arg type "$test_type" '.test_cases[] | select(.api == $api and .type == $type) | length' "$test_info_file")
            if [ "$covered" -gt 0 ]; then
                echo "| $test_type | ✅ ($covered) |" >> "$report_file"
            else
                echo "| $test_type | ❌ |" >> "$report_file"
            fi
        done

        echo "" >> "$report_file"
    done

    echo "✅ 测试场景覆盖率报告已生成: $report_file"
}
```

---

## 四、覆盖率报告生成

### 4.1 报告格式

生成结构化的覆盖率报告:

```markdown
# 测试覆盖率分析报告

## 基本信息

- **子系统**: BundleManager
- **测试套**: ActsAbilityContextApiTest
- **分析时间**: 2026-03-18 10:30:00
- **API 总数**: 15
- **已覆盖 API**: 12
- **未覆盖 API**: 3
- **总体覆盖率**: 80%

## API 覆盖详情

| API | 测试用例数 | 参数覆盖率 | 测试类型覆盖 | 状态 |
|-----|------------|-----------|-------------|------|
| GetAbilityInfo | 8 | 75% | PARAM, ERROR, RETURN | ✅ 已覆盖 |
| QueryAbilityInfo | 5 | 60% | PARAM, RETURN | ⚠️ 部分覆盖 |
| ContinueAbility | 0 | 0% | - | ❌ 未覆盖 |

## 未覆盖的 API

1. **ContinueAbility**
   - 缺失参数组合: (正常参数)
   - 缺失测试场景: PARAM, ERROR, RETURN, BOUNDARY
   - 优先级: 高

2. **StopAbility**
   - 缺失参数组合: (正常参数)
   - 缺失测试场景: PARAM, ERROR, RETURN
   - 优先级: 高

3. **TerminateAbility**
   - 缺失参数组合: (正常参数)
   - 缺失测试场景: PARAM, ERROR, RETURN, BOUNDARY
   - 优先级: 中

## 测试类型分布

| 测试类型 | 用例数 | 占比 |
|---------|-------|------|
| PARAM | 15 | 45% |
| ERROR | 10 | 30% |
| RETURN | 5 | 15% |
| BOUNDARY | 2 | 6% |
| MEMORY | 1 | 3% |

## 建议

1. **优先补充未覆盖 API 的基础测试** - ContinueAbility, StopAbility, TerminateAbility
2. **提高参数组合覆盖率** - 重点补充 QueryAbilityInfo 的缺失参数组合
3. **增加边界测试用例** - BOUNDARY 类型测试覆盖率较低,需要增加
4. **完善错误处理测试** - 确保每个 API 都有 ERROR 类型测试
```

### 4.2 优先级划分

根据 API 重要性和覆盖情况划分优先级:

```bash
# 划分优先级
classify_priority() {
    local api_name=$1
    local coverage_rate=$2
    local api_importance=$3

    local priority="低"

    # 根据覆盖率和重要性划分优先级
    if [ "$coverage_rate" -eq 0 ]; then
        priority="高"
    elif [ "$api_importance" == "critical" ]; then
        priority="高"
    elif [ "$coverage_rate" -lt 50 ]; then
        priority="中"
    fi

    echo "$api_name: $priority"
}

# 优先级定义
# 高优先级:
#   - 完全未覆盖的 API (覆盖率 0%)
#   - 关键 API (api_importance == "critical")
#
# 中优先级:
#   - 覆盖率低于 50% 的 API
#   - 重要 API (api_importance == "important")
#
# 低优先级:
#   - 覆盖率高于 50% 的 API
#   - 普通 API (api_importance == "normal")
```

---

## 五、增量覆盖率分析

### 5.1 增量扫描

只扫描新增或修改的测试文件:

```bash
# 增量覆盖率分析
incremental_coverage_analysis() {
    local test_suite_dir=$1
    local last_analysis_time=$2

    echo "=== 增量覆盖率分析 ==="
    echo "基准时间: $last_analysis_time"

    # 查找新增或修改的文件
    local modified_files=$(find "$test_suite_dir" -newermt "$last_analysis_time" -name "*.cpp" -o -name "*.ets" -o -name "*.md")

    if [ -n "$modified_files" ]; then
        echo "📝 发现修改的文件: $(echo "$modified_files" | wc -l)"

        # 只扫描修改的文件
        for file in $modified_files; do
            echo "  🔍 扫描: $file"
            extract_test_info "$file"
        done

        # 更新覆盖率信息
        update_coverage_info "$modified_files"
    else
        echo "✅ 未发现新的测试文件"
    fi
}

# 更新覆盖率信息
update_coverage_info() {
    local modified_files=$1

    echo "🔄 更新覆盖率信息..."

    # 读取现有覆盖率数据
    local existing_data=$(cat "test/coverage/coverage_data.json")

    # 合并新数据
    local new_data=$(merge_coverage_data "$existing_data" "$modified_files")

    # 保存更新后的数据
    echo "$new_data" > "test/coverage/coverage_data.json"

    # 更新分析时间戳
    echo "$(date '+%Y-%m-%d %H:%M:%S')" > "test/coverage/last_analysis.txt"

    echo "✅ 覆盖率信息已更新"
}
```

### 5.2 差异对比

对比两次覆盖率分析的差异:

```bash
# 覆盖率差异对比
compare_coverage_diff() {
    local old_report=$1
    local new_report=$2

    echo "=== 覆盖率差异对比 ==="

    # 解析旧报告
    local old_coverage=$(extract_coverage_rate "$old_report")
    local old_uncovered=$(extract_uncovered_apis "$old_report")

    # 解析新报告
    local new_coverage=$(extract_coverage_rate "$new_report")
    local new_uncovered=$(extract_uncovered_apis "$new_report")

    # 计算差异
    local coverage_diff=$(echo "scale=2; $new_coverage - $old_coverage" | bc)

    echo "📊 覆盖率变化: $old_coverage% → $new_coverage% ($coverage_diff%)"

    # 识别新增覆盖的 API
    local newly_covered=$(comm -13 <(echo "$old_uncovered") <(echo "$new_uncovered"))
    if [ -n "$newly_covered" ]; then
        echo "✅ 新增覆盖的 API:"
        echo "$newly_covered" | while read api; do
            echo "  ➕ $api"
        done
    fi

    # 识别仍然未覆盖的 API
    local still_uncovered=$(comm -12 <(echo "$old_uncovered") <(echo "$new_uncovered"))
    if [ -n "$still_uncovered" ]; then
        echo "⚠️  仍未覆盖的 API:"
        echo "$still_uncovered" | while read api; do
            echo "  ➖ $api"
        done
    fi
}
```

---

## 六、使用示例

### 6.1 完整覆盖率分析流程

```bash
# 完整的覆盖率分析流程
#!/bin/bash

# 1. 扫描测试文件
scan_test_files "test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsabilitycontextapitest"

# 2. 读取 API 列表
local api_list_file="test/coverage/api_list.json"

# 3. 分析 API 覆盖率
analyze_api_coverage "$api_list_file" "test/coverage/test_info.json"

# 4. 分析参数组合覆盖率
analyze_param_coverage "$api_list_file" "test/coverage/test_info.json"

# 5. 分析测试场景覆盖率
analyze_test_scenario_coverage "test/coverage/test_info.json"

# 6. 生成综合覆盖率报告
generate_comprehensive_coverage_report "test/coverage/"
```

### 6.2 增量覆盖率分析

```bash
# 增量覆盖率分析
#!/bin/bash

# 读取上次分析时间
local last_analysis_time=$(cat "test/coverage/last_analysis.txt")

# 执行增量分析
incremental_coverage_analysis "test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsabilitycontextapitest" "$last_analysis_time"

# 对比差异
compare_coverage_diff "test/coverage/old_report.md" "test/coverage/new_report.md"
```

### 6.3 子系统对比分析

```bash
# 对比多个子系统的覆盖率
#!/bin/bash

# 定义子系统列表
local subsystems=("bundlemanager" "ability" "hilog")

# 分析每个子系统
for subsystem in "${subsystems[@]}"; do
    echo "=== 分析子系统: $subsystem ==="
    scan_test_files "test/xts/acts/$subsystem"
    generate_comprehensive_coverage_report "test/coverage/$subsystem/"
done

# 生成对比报告
generate_subsystem_comparison_report "test/coverage/"
```

---

## 七、常见问题

### Q1: 如何处理条件编译的测试用例？

**解决方案**:
- 扫描时忽略 `#ifdef` 和 `#ifndef` 包裹的代码
- 分析多个编译配置下的覆盖率
- 分别统计不同配置的覆盖情况

### Q2: 如何处理参数化的测试用例？

**解决方案**:
- 识别参数化测试的模式(如 `@ParameterizedTest`)
- 将每个参数组合视为独立的测试用例
- 统计时考虑参数化测试的覆盖情况

### Q3: 如何提高覆盖率分析的准确性？

**解决方案**:
- 结合静态分析(代码扫描)和动态分析(运行时数据)
- 使用测试框架的覆盖率工具(如 gcov、lcov)
- 定期更新覆盖率数据,保持数据新鲜度

---

**版本**: 1.0.0
**创建日期**: 2026-03-18
**更新日期**: 2026-03-18
**兼容性**: OpenHarmony API 10+
