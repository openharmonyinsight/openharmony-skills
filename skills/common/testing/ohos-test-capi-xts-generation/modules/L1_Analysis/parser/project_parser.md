# 项目解析模块

> 📖 **相关文档**：
> - [头文件解析模块](./unified_api_parser_c.md) - API 信息提取和结构化
> - [测试覆盖率分析](./coverage_analyzer.md) - 测试覆盖情况分析

> **模块信息**
> - 层级：L1_Analysis
> - 优先级：按需加载
> - 适用范围：OpenHarmony CAPI XTS 测试工程结构解析和配置识别
> - 依赖：conventions, L1_Analysis/unified_api_parser_c.md
> - 触发条件：首次分析测试套、需要理解测试套结构时

---

## 一、模块概述

项目解析模块负责解析 OpenHarmony CAPI XTS 测试工程的目录结构、配置文件和构建配置,识别测试套类型、依赖关系和关键文件路径。

### 1.1 核心功能

- **目录结构识别** - 识别测试套的标准目录结构
- **配置文件解析** - 解析 BUILD.gn、CMakeLists.txt、Test.json 等配置文件
- **测试套类型识别** - 识别动态测试套、静态测试套、普通 JS 测试套
- **依赖关系分析** - 分析测试套的依赖项和引用关系
- **文件路径映射** - 建立 API 头文件、测试文件、配置文件的路径映射
- **工程验证** - 验证测试套工程的完整性和正确性

### 1.2 应用场景

1. **测试套初始化** - 新建测试套时验证目录结构
2. **工程迁移** - 迁移测试套时识别需要迁移的文件
3. **配置验证** - 验证配置文件的正确性
4. **依赖分析** - 分析测试套的依赖项,避免遗漏
5. **文档生成** - 为测试套生成结构化文档

---

## 二、目录结构识别

### 2.1 标准测试套结构

识别标准的测试套目录结构:

```bash
# 识别测试套结构
identify_suite_structure() {
    local suite_root=$1

    echo "=== 识别测试套结构: $suite_root ==="

    # 检查标准目录
    local standard_dirs=("entry" "test" "src" "build-profile.json5" "BUILD.gn" "Test.json")
    for dir in "${standard_dirs[@]}"; do
        local path="$suite_root/$dir"
        if [ -d "$path" ]; then
            echo "  ✅ 目录: $dir"
            analyze_directory "$path"
        elif [ -f "$path" ]; then
            echo "  ✅ 文件: $dir"
            analyze_file "$path"
        else
            echo "  ❌ 缺失: $dir"
        fi
    done

    # 检查子目录结构
    check_subdirectory_structure "$suite_root"
}

check_subdirectory_structure() {
    local suite_root=$1

    echo "🔍 检查子目录结构..."

    # 检查 entry 目录
    if [ -d "$suite_root/entry" ]; then
        echo "  📁 entry/ 目录:"
        local entry_dirs=("src/main/cpp" "src/main/ohosTest/ets/test" "build-profile.json5")
        for dir in "${entry_dirs[@]}"; do
            if [ -d "$suite_root/entry/$dir" ]; then
                echo "    ✅ $dir"
            else
                echo "    ❌ 缺失: $dir"
            fi
        done
    fi

    # 检查是否有 types 目录(静态测试套)
    if [ -d "$suite_root/types" ]; then
        echo "  📁 types/ 目录 (静态测试套)"
        local types_dirs=($(ls -1 "$suite_root/types"))
        for dir in "${types_dirs[@]}"; do
            echo "    📦 模块: $dir"
        done
    fi
}
```

### 2.2 目录结构分析

分析目录结构,识别测试套类型:

```bash
# 分析目录结构
analyze_directory() {
    local dir_path=$1

    local dir_name=$(basename "$dir_path")
    echo "  🔍 分析目录: $dir_name"

    # 根据目录内容识别类型
    if [ -f "$dir_path/NapiTest.cpp" ]; then
        echo "    📄 检测到: N-API 封装测试文件"
        echo "    🏷️  类型: N-API 封装测试"
    elif [ -d "$dir_path/ets/test" ]; then
        echo "    📁 检测到: ETS/ArkTS 测试目录"
        echo "    🏷️  类型: ETS 测试"
    elif [ -d "$dir_path/types" ]; then
        echo "    📁 检测到: TypeScript 类型定义目录"
        echo "    🏷️  类型: 静态测试套"
    fi

    # 列出关键文件
    local key_files=("NapiTest.cpp" "CMakeLists.txt" "*.test.ets" "Index.d.ts" "Test.json")
    for file_pattern in "${key_files[@]}"; do
        local files=$(find "$dir_path" -name "$file_pattern" 2>/dev/null)
        if [ -n "$files" ]; then
            echo "    📄 $file_pattern:"
            for file in $files; do
                echo "      - $(basename $file)"
            done
        fi
    done
}
```

---

## 三、配置文件解析

### 3.1 BUILD.gn 解析

解析 BUILD.gn 构建配置文件:

```bash
# 解析 BUILD.gn
parse_build_gn() {
    local build_gn_path=$1

    echo "=== 解析 BUILD.gn: $build_gn_path ==="

    # 检查文件是否存在
    if [ ! -f "$build_gn_path" ]; then
        echo "❌ BUILD.gn 文件不存在"
        return 1
    fi

    # 提取测试套类型
    local suite_type=$(extract_suite_type_from_gn "$build_gn_path")
    echo "🏷️  测试套类型: $suite_type"

    # 提取测试套名称
    local suite_name=$(extract_suite_name_from_gn "$build_gn_path")
    echo "📦 测试套名称: $suite_name"

    # 提取依赖关系
    local deps=$(extract_deps_from_gn "$build_gn_path")
    echo "🔗 依赖项: $deps"

    # 提取配置项
    local configs=$(extract_configs_from_gn "$build_gn_path")
    echo "⚙️  配置项: $configs"
}

# 从 BUILD.gn 提取测试套类型
extract_suite_type_from_gn() {
    local build_gn_path=$1

    # 检查测试套类型
    if grep -q "ohos_js_app_static_suite" "$build_gn_path"; then
        echo "static_js_suite"
    elif grep -q "ohos_js_app_suite" "$build_gn_path"; then
        # 检查是否为动态测试套
        if grep -q "test_hap\s*=\s*true" "$build_gn_path"; then
            echo "dynamic_js_suite"
        else
            echo "dynamic_js_suite"
        fi
    else
        echo "unknown"
    fi
}

# 从 BUILD.gn 提取测试套名称
extract_suite_name_from_gn() {
    local build_gn_path=$1

    # 提取引号内的测试套名称
    grep -E "(ohos_js_app_suite|ohos_js_app_static_suite)\(\"[^\"]+\"\)" "$build_gn_path" | \
        sed 's/.*("\([^"]*\)").*/\1/' | \
        head -1
}

# 从 BUILD.gn 提取依赖项
extract_deps_from_gn() {
    local build_gn_path=$1

    # 提取 deps 列表
    grep -E "deps\s*=\s*\[" "$build_gn_path" -A 20 | \
        grep -E '":\s*"[^"]+"' | \
        sed 's/.*"\([^"]*\)".*/\1/' | \
        tr '\n' ' ' | \
        sed 's/ $//'
}

# 从 BUILD.gn 提取配置项
extract_configs_from_gn() {
    local build_gn_path=$1

    local configs=()

    # 提取常用配置项
    if grep -q "test_hap\s*=\s*true" "$build_gn_path"; then
        configs+=("test_hap=true")
    fi

    echo "${configs[@]}"
}
```

### 3.2 CMakeLists.txt 解析

解析 CMakeLists.txt 构建配置文件:

```bash
# 解析 CMakeLists.txt
parse_cmake_lists() {
    local cmake_path=$1

    echo "=== 解析 CMakeLists.txt: $cmake_path ==="

    # 检查文件是否存在
    if [ ! -f "$cmake_path" ]; then
        echo "❌ CMakeLists.txt 文件不存在"
        return 1
    fi

    # 提取项目名称
    local project_name=$(extract_project_name_from_cmake "$cmake_path")
    echo "📦 项目名称: $project_name"

    # 提取源文件
    local sources=$(extract_sources_from_cmake "$cmake_path")
    echo "📄 源文件数: $(echo "$sources" | wc -w)"

    # 提取库依赖
    local libs=$(extract_libs_from_cmake "$cmake_path")
    echo "🔗 库依赖: $libs"

    # 提取编译选项
    local compile_options=$(extract_compile_options_from_cmake "$cmake_path")
    echo "⚙️  编译选项: $compile_options"
}

# 从 CMakeLists.txt 提取项目名称
extract_project_name_from_cmake() {
    local cmake_path=$1

    grep -i "project" "$cmake_path" | \
        sed 's/.*project(\([^)]*\)).*/\1/' | \
        head -1
}

# 从 CMakeLists.txt 提取源文件
extract_sources_from_cmake() {
    local cmake_path=$1

    grep -i "source_files" "$cmake_path" -A 10 | \
        grep -E '\.cpp|\.c|\.cc' | \
        tr '\n' ' ' | \
        sed 's/ $//'
}

# 从 CMakeLists.txt 提取库依赖
extract_libs_from_cmake() {
    local cmake_path=$1

    grep -i "target_link_libraries" "$cmake_path" -A 20 | \
        grep -E 'lib[a-z_]+\.so' | \
        tr '\n' ' ' | \
        sed 's/ $//'
}

# 从 CMakeLists.txt 提取编译选项
extract_compile_options_from_cmake() {
    local cmake_path=$1

    local options=()

    if grep -qi "c.*11" "$cmake_path"; then
        options+=("C++11")
    fi
    if grep -qi "c.*14" "$cmake_path"; then
        options+=("C++14")
    fi

    echo "${options[@]}"
}
```

### 3.3 Test.json 解析

解析 Test.json 测试配置文件:

```bash
# 解析 Test.json
parse_test_json() {
    local test_json_path=$1

    echo "=== 解析 Test.json: $test_json_path ==="

    # 检查文件是否存在
    if [ ! -f "$test_json_path" ]; then
        echo "❌ Test.json 文件不存在"
        return 1
    fi

    # 提取测试套名称
    local suite_name=$(jq -r '.packageName' "$test_json_path")
    echo "📦 测试套名称: $suite_name"

    # 提取测试类型
    local test_type=$(jq -r '.testType' "$test_json_path")
    echo "🏷️  测试类型: $test_type"

    # 提取设备类型
    local device_type=$(jq -r '.deviceType' "$test_json_path")
    echo "📱 设备类型: $device_type"

    # 提取 API 版本
    local api_version=$(jq -r '.version' "$test_json_path")
    echo "📋 API 版本: $api_version"

    # 提取测试用例列表
    local test_cases=$(jq -r '.testCases[] | "\(.name): \(.type)"' "$test_json_path")
    echo "📝 测试用例:"
    echo "$test_cases" | while read test_case; do
        echo "  - $test_case"
    done
}
```

### 3.4 oh-package.json5 解析

解析 oh-package.json5 依赖配置文件:

```bash
# 解析 oh-package.json5
parse_oh_package() {
    local package_path=$1

    echo "=== 解析 oh-package.json5: $package_path ==="

    # 检查文件是否存在
    if [ ! -f "$package_path" ]; then
        echo "❌ oh-package.json5 文件不存在"
        return 1
    fi

    # 提取包名
    local package_name=$(jq -r '.name' "$package_path")
    echo "📦 包名: $package_name"

    # 提取版本
    local version=$(jq -r '.version' "$package_path")
    echo "🔢 版本: $version"

    # 提取依赖项
    local dependencies=$(jq -r '.dependencies // {} | to_entries[] | "\(.key): \(.value)"' "$package_path")
    echo "🔗 依赖项:"
    echo "$dependencies" | while read dep; do
        echo "  - $dep"
    done

    # 提取 devDependencies
    local dev_deps=$(jq -r '.devDependencies // {} | to_entries[] | "\(.key): \(.value)"' "$package_path")
    echo "🛠️  开发依赖:"
    echo "$dev_deps" | while read dep; do
        echo "  - $dep"
    done
}
```

---

## 四、测试套类型识别

### 4.1 测试套类型判断

根据配置文件和目录结构判断测试套类型:

```bash
# 判断测试套类型
determine_suite_type() {
    local suite_root=$1

    echo "=== 判断测试套类型 ==="

    # 检查 BUILD.gn
    if [ -f "$suite_root/BUILD.gn" ]; then
        local suite_type=$(extract_suite_type_from_gn "$suite_root/BUILD.gn")
        echo "🏷️  根据 BUILD.gn 判断: $suite_type"
    fi

    # 检查目录结构
    if [ -d "$suite_root/types" ]; then
        echo "🏷️  根据 types/ 目录判断: 静态测试套"
        suite_type="static_js_suite"
    fi

    # 检查 CMakeLists.txt
    if [ -f "$suite_root/entry/src/main/cpp/CMakeLists.txt" ]; then
        echo "🏷️  根据 CMakeLists.txt 判断: N-API 封装测试"
        suite_type="native_test_suite"
    fi

    # 输出最终类型
    echo "✅ 测试套类型: ${suite_type:-unknown}"

    # 根据类型输出特征
    print_suite_characteristics "$suite_type"
}

# 输出测试套特征
print_suite_characteristics() {
    local suite_type=$1

    echo "📋 测试套特征:"

    case "$suite_type" in
        "native_test_suite")
            echo "  - 编译目标: ohos_js_app_static_suite() (静态) 或 ohos_js_app_suite() (动态)"
            echo "  - 代码类型: C/C++"
            echo "  - N-API 封装: 是"
            echo "  - ETS 测试: 是"
            ;;
        "static_js_suite")
            echo "  - 编译目标: ohos_js_app_suite()"
            echo "  - 配置项: xts_suitetype=hap_static"
            echo "  - 静态 SDK: 需要同步编译"
            echo "  - 类型定义: types/ 目录"
            ;;
        "dynamic_js_suite")
            echo "  - 编译目标: ohos_js_app_suite()"
            echo "  - 配置项: test_hap=true"
            echo "  - 运行时类型: 动态"
            ;;
        *)
            echo "  - 未知类型"
            ;;
    esac
}
```

### 4.2 测试套特征对比

对比不同测试套的特征:

| 特征 | 静态 JS 测试套 | 动态 JS 测试套 |
|------|--------------|--------------|
| **编译目标** | ohos_js_app_static_suite | ohos_js_app_suite |
| **BUILD.gn** | ohos_js_app_static_suite (testonly=true) | ohos_js_app_suite (test_hap=true, testonly=true) |
| **代码类型** | C/C++ + JS/TS | C/C++ + JS/TS |
| **N-API 封装** | 是 | 是 |
| **静态类型** | 是 | 否 |
| **types/ 目录** | 有 | 有 |
| **编译命令** | ./build.sh suite=XXX xts_suitetype=hap_static | ./build.sh suite=XXX |
| **编译时间** | 较长 | 较短 |

---

## 五、依赖关系分析

### 5.1 依赖项提取

提取测试套的所有依赖项:

```bash
# 提取依赖项
extract_dependencies() {
    local suite_root=$1

    echo "=== 提取依赖项: $suite_root ==="

    # 从 BUILD.gn 提取依赖
    local gn_deps=$(extract_deps_from_gn "$suite_root/BUILD.gn")
    echo "🔗 BUILD.gn 依赖: $gn_deps"

    # 从 oh-package.json5 提取依赖
    local package_deps=$(jq -r '.dependencies // {} | keys[]' "$suite_root/oh-package.json5")
    echo "🔗 oh-package.json5 依赖: $package_deps"

    # 从 CMakeLists.txt 提取库依赖
    local cmake_libs=$(extract_libs_from_cmake "$suite_root/entry/src/main/cpp/CMakeLists.txt")
    echo "🔗 CMakeLists.txt 库依赖: $cmake_libs"

    # 合并所有依赖
    local all_deps=$(echo -e "$gn_deps\n$package_deps\n$cmake_libs" | sort | uniq)
    echo "✅ 所有依赖项:"
    echo "$all_deps" | while read dep; do
        echo "  - $dep"
    done

    # 保存依赖项到文件
    echo "$all_deps" > "test/dependencies/dependencies.txt"
}

# 验证依赖项
verify_dependencies() {
    local deps_file=$1

    echo "=== 验证依赖项 ==="

    # 检查每个依赖项是否存在
    while IFS= read -r dep; do
        if [[ "$dep" == *.so ]]; then
            # 库文件依赖
            if [ -f "$CAPI_LIB/$dep" ]; then
                echo "  ✅ $dep: 存在"
            else
                echo "  ❌ $dep: 缺失"
            fi
        else
            # 模块依赖
            if [ -d "$OH_ROOT/$dep" ]; then
                echo "  ✅ $dep: 存在"
            else
                echo "  ⚠️  $dep: 未验证"
            fi
        fi
    done < "$deps_file"
}
```

### 5.2 依赖关系图

生成依赖关系图:

```bash
# 生成依赖关系图
generate_dependency_graph() {
    local suite_root=$1

    echo "=== 生成依赖关系图 ==="

    local graph_file="test/dependencies/dependency_graph.dot"

    echo "digraph TestSuiteDependencies {" > "$graph_file"
    echo "  rankdir=LR;" >> "$graph_file"
    echo "  node [shape=box];" >> "$graph_file"

    # 添加测试套节点
    local suite_name=$(extract_suite_name_from_gn "$suite_root/BUILD.gn")
    echo "  \"$suite_name\" [style=filled, fillcolor=lightblue];" >> "$graph_file"

    # 添加依赖节点和边
    local deps=$(extract_deps_from_gn "$suite_root/BUILD.gn")
    for dep in $deps; do
        echo "  \"$dep\";" >> "$graph_file"
        echo "  \"$suite_name\" -> \"$dep\";" >> "$graph_file"
    done

    echo "}" >> "$graph_file"

    # 转换为图片 (需要 graphviz)
    if command -v dot &> /dev/null; then
        dot -Tpng "$graph_file" -o "test/dependencies/dependency_graph.png"
        echo "✅ 依赖关系图已生成: test/dependencies/dependency_graph.png"
    else
        echo "⚠️  graphviz 未安装,无法生成图片"
        echo "   DOT 文件: $graph_file"
    fi
}
```

---

## 六、文件路径映射

### 6.1 路径映射表

建立文件路径映射关系:

```bash
# 建立路径映射
build_path_mapping() {
    local suite_root=$1
    local oh_root=$2

    echo "=== 建立路径映射 ==="

    local mapping_file="test/config/path_mapping.json"

    # 创建路径映射对象
    cat > "$mapping_file" << EOF
{
  "suite_root": "$suite_root",
  "oh_root": "$oh_root",
  "api_headers": "$oh_root/interface/sdk_c",
  "capi_libs": "$oh_root/out/rk3568/clang_x64/sysroot/usr/lib",
  "test_cases": "test/xts/acts",
  "output_dir": "out/rk3568/suites/acts/acts/testcases",
  "napi_test_file": "$suite_root/entry/src/main/cpp/NapiTest.cpp",
  "ets_test_dir": "$suite_root/entry/src/main/ohosTest/ets/test",
  "cmake_file": "$suite_root/entry/src/main/cpp/CMakeLists.txt",
  "build_gn_file": "$suite_root/BUILD.gn",
  "test_json_file": "$suite_root/Test.json",
  "oh_package_file": "$suite_root/oh-package.json5",
  "type_defs_dir": "$suite_root/types"
}
EOF

    echo "✅ 路径映射已建立: $mapping_file"

    # 验证路径
    verify_path_mapping "$mapping_file"
}

# 验证路径映射
verify_path_mapping() {
    local mapping_file=$1

    echo "=== 验证路径映射 ==="

    # 读取路径映射
    jq -r 'to_entries[] | "\(.key): \(.value)"' "$mapping_file" | while read -r entry; do
        local key=$(echo "$entry" | cut -d: -f1)
        local path=$(echo "$entry" | cut -d: -f2-)

        # 检查路径是否存在
        if [ -e "$path" ]; then
            echo "  ✅ $key: $path"
        else
            echo "  ⚠️  $key: $path (可能不存在)"
        fi
    done
}
```

### 6.2 路径查询接口

提供路径查询接口:

```bash
# 查询路径
query_path() {
    local mapping_file=$1
    local key=$2

    # 从映射文件查询路径
    local path=$(jq -r ".$key" "$mapping_file")

    if [ "$path" != "null" ]; then
        echo "$path"
    else
        echo "❌ 未找到路径: $key"
        return 1
    fi
}

# 使用示例
local napi_test_path=$(query_path "test/config/path_mapping.json" "napi_test_file")
echo "N-API 测试文件: $napi_test_path"
```

---

## 七、工程验证

### 7.1 完整性检查

检查测试套工程的完整性:

```bash
# 检查工程完整性
verify_suite_integrity() {
    local suite_root=$1

    echo "=== 检查工程完整性: $suite_root ==="

    local is_complete=true

    # 检查必需文件
    local required_files=("BUILD.gn" "Test.json" "oh-package.json5" "entry/build-profile.json5")
    for file in "${required_files[@]}"; do
        if [ ! -f "$suite_root/$file" ]; then
            echo "  ❌ 缺失必需文件: $file"
            is_complete=false
        else
            echo "  ✅ 文件存在: $file"
        fi
    done

    # 检查必需目录
    local required_dirs=("entry/src/main/cpp" "entry/src/main/ohosTest")
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$suite_root/$dir" ]; then
            echo "  ❌ 缺失必需目录: $dir"
            is_complete=false
        else
            echo "  ✅ 目录存在: $dir"
        fi
    done

    # 检查关键测试文件
    if [ ! -f "$suite_root/entry/src/main/cpp/NapiTest.cpp" ]; then
        echo "  ⚠️  缺失 N-API 封装文件"
    fi

    # 输出结果
    if $is_complete; then
        echo "✅ 工程完整性检查通过"
        return 0
    else
        echo "❌ 工程完整性检查失败"
        return 1
    fi
}
```

### 7.2 配置一致性检查

检查各配置文件之间的一致性:

```bash
# 检查配置一致性
verify_config_consistency() {
    local suite_root=$1

    echo "=== 检查配置一致性: $suite_root ==="

    local is_consistent=true

    # 检查测试套名称一致性
    local gn_name=$(extract_suite_name_from_gn "$suite_root/BUILD.gn")
    local json_name=$(jq -r '.packageName' "$suite_root/Test.json")

    if [ "$gn_name" != "$json_name" ]; then
        echo "  ⚠️  测试套名称不一致:"
        echo "    BUILD.gn: $gn_name"
        echo "    Test.json: $json_name"
        is_consistent=false
    fi

    # 检查编译配置一致性
    local test_hap=$(grep -q "test_hap\s*=\s*true" "$suite_root/BUILD.gn" && echo "true" || echo "false")
    local static_type=$(grep -q "ohos_js_app_static_suite" "$suite_root/BUILD.gn" && echo "true" || echo "false")
    local testonly=$(grep -q "testonly.*=.*true" "$suite_root/BUILD.gn" && echo "true" || echo "false")

    if [ "$static_type" == "true" ] && [ "$test_hap" == "true" ]; then
        echo "  ⚠️  编译配置冲突: 静态测试套不应配置 test_hap=true"
        is_consistent=false
    elif [ "$static_type" == "true" ] && [ "$testonly" != "true" ]; then
        echo "  ⚠️  编译配置错误: 静态测试套必须配置 testonly=true"
        is_consistent=false
    elif [ "$static_type" == "false" ] && [ "$test_hap" == "true" ] && [ "$testonly" != "true" ]; then
        echo "  ⚠️  编译配置错误: 动态测试套必须配置 testonly=true"
        is_consistent=false
    fi

    # 检查依赖一致性
    local gn_deps=$(extract_deps_from_gn "$suite_root/BUILD.gn")
    local pkg_deps=$(jq -r '.dependencies // {} | keys[]' "$suite_root/oh-package.json5" | tr '\n' ',')

    # 这里可以添加更复杂的依赖一致性检查

    # 输出结果
    if $is_consistent; then
        echo "✅ 配置一致性检查通过"
        return 0
    else
        echo "❌ 配置一致性检查失败"
        return 1
    fi
}
```

---

## 八、使用示例

### 8.1 完整工程解析流程

```bash
# 完整的工程解析流程
#!/bin/bash

local suite_root="test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsabilitycontextapitest"

# 1. 识别目录结构
identify_suite_structure "$suite_root"

# 2. 解析配置文件
parse_build_gn "$suite_root/BUILD.gn"
parse_cmake_lists "$suite_root/entry/src/main/cpp/CMakeLists.txt"
parse_test_json "$suite_root/Test.json"
parse_oh_package "$suite_root/oh-package.json5"

# 3. 判断测试套类型
determine_suite_type "$suite_root"

# 4. 提取依赖项
extract_dependencies "$suite_root"

# 5. 建立路径映射
build_path_mapping "$suite_root" "$OH_ROOT"

# 6. 验证工程完整性
verify_suite_integrity "$suite_root"

# 7. 验证配置一致性
verify_config_consistency "$suite_root"

# 8. 生成依赖关系图
generate_dependency_graph "$suite_root"
```

### 8.2 批量解析多个测试套

```bash
# 批量解析多个测试套
#!/bin/bash

# 定义测试套列表
local test_suites=(
    "test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsabilitycontextapitest"
    "test/xts/acts/ability/ace_c_arkui_test_api20"
    "test/xts/acts/hilog/hilog/hilogtest"
)

# 批量解析
for suite in "${test_suites[@]}"; do
    echo "========================================"
    echo "解析测试套: $suite"
    echo "========================================"

    # 执行完整解析流程
    identify_suite_structure "$suite"
    determine_suite_type "$suite"
    verify_suite_integrity "$suite"

    echo ""
done
```

---

## 九、常见问题

### Q1: 如何处理自定义目录结构的测试套？

**解决方案**:
- 识别关键文件(如 BUILD.gn、NapiTest.cpp),不依赖标准目录结构
- 支持自定义路径映射配置
- 提供目录结构覆盖配置

### Q2: 如何处理多层嵌套的测试套？

**解决方案**:
- 递归扫描目录,识别嵌套的测试套
- 为每个嵌套测试套创建独立的路径映射
- 支持批量分析嵌套测试套

### Q3: 如何处理配置文件中的变量和条件？

**解决方案**:
- 解析时展开变量(如 `${product_name}`)
- 识别条件编译块,分析所有可能分支
- 提供变量替换接口

---

**版本**: 1.0.0
**创建日期**: 2026-03-18
**更新日期**: 2026-03-18
**兼容性**: OpenHarmony API 10+
