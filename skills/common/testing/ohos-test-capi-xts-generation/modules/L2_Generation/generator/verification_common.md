# 通用校验模块

> **版本**: 1.0.0  
> **创建日期**: 2026-03-24  
> **用途**: 定义测试用例生成后的三重Napi校验和编译前工程结构校验流程

## 概述

本模块定义了 CAPI XTS 测试用例生成的两个关键校验环节：

1. **三重Napi校验** - 在测试代码生成后立即执行，确保 N-API 注册的完整性
2. **编译前工程结构校验** - 在编译前执行，防止因缺少文件或参数错误导致编译失败

---

## 一、三重Napi校验

### 1.1 校验时机

**必须在测试代码生成完成后、提交代码或编译验证前执行**

### 1.2 校验目的

确保 N-API 封装测试的三个关键步骤同步完成，避免编译错误或运行时错误。

### 1.3 校验步骤

| 步骤 | 校验项 | 校验内容 | 失败后果 |
|------|--------|---------|---------|
| **步骤 1** | N-API 函数注册 | 验证所有 N-API 封装函数都在 `Init` 函数的 `napi_property_descriptor` 数组中完成注册 | 编译错误：函数未注册 |
| **步骤 2** | TypeScript 接口声明 | 验证所有 N-API 函数都在 `types/libentry/index.d.ts` 中有对应的 `export const` 声明 | TypeScript 编译错误：找不到函数定义 |
| **步骤 3** | ETS 测试接口使用 | 验证所有 ETS 测试用例中使用的 N-API 接口都有对应的 N-API 实现 | ETS 运行时错误：undefined is not a function |

### 1.4 详细校验方法

#### 步骤 1：N-API 函数注册校验

**校验位置**：`entry/src/main/cpp/NapiTest.cpp` 或 `napi_init.cpp`

**校验规则**：
- 每个 `static napi_value [函数名]` 函数都必须在 `Init` 函数的 `napi_property_descriptor` 数组中注册
- 注册时使用的函数名称必须与 `static napi_value` 定义的函数名称完全一致
- 不能有遗漏注册的函数
- 不能有重复注册的函数

**校验命令**：

```bash
# 提取所有 N-API 封装函数定义
defined_funcs=$(grep -oP 'static napi_value\s+\K[A-Za-z0-9_]+(?=\s*\()' entry/src/main/cpp/NapiTest.cpp | sort | uniq)

# 提取 Init 函数中注册的函数（支持多种注册方式）
registered_funcs=$(grep -A 100 'napi_property_descriptor desc\[\]' entry/src/main/cpp/NapiTest.cpp | grep -oP '(DECLARE_NAPI_PROPERTY\s*\(\s*"[^"]+"|"[^"]+"\s*,\s*nullptr\s*,\s*[A-Za-z0-9_]+)' | grep -oP '[A-Za-z0-9_]+$' | sort | uniq)

# 对比两个列表
echo "=== 定义但未注册的函数 ==="
comm -23 <(echo "$defined_funcs") <(echo "$registered_funcs")

echo "=== 注册但未定义的函数 ==="
comm -13 <(echo "$defined_funcs") <(echo "$registered_funcs")
```

**正确示例**：

```cpp
// 函数定义
static napi_value MyNewFunction_napi(napi_env env, napi_callback_info info)
{
    // 函数实现
}

// Init 函数中注册
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        DECLARE_NAPI_FUNCTION("myNewFunction", MyNewFunction_napi),  // ✅ 已注册
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
```

#### 步骤 2：TypeScript 接口声明校验

**校验位置**：`entry/src/main/cpp/types/libentry/index.d.ts`

**校验规则**：
- 每个 N-API 函数都必须在 `index.d.ts` 中有对应的 `export const` 声明
- 函数签名必须匹配：参数类型和返回类型必须与 C++ 实现一致
- 函数名称必须完全一致（区分大小写）
- 不能有遗漏声明的函数
- 不能有多余的声明（未使用的函数声明）

**校验命令**：

```bash
# 提取 Init 函数中注册的函数名称（JS 侧使用的名称）
js_names=$(grep -A 100 'napi_property_descriptor desc\[\]' entry/src/main/cpp/NapiTest.cpp | grep -oP 'DECLARE_NAPI_PROPERTY\s*\(\s*"\K[^"]+' | sort | uniq)

# 提取 index.d.ts 中声明的函数名称
declared_names=$(grep 'export const' entry/src/main/cpp/types/libentry/index.d.ts | grep -oP 'export const\s+\K[A-Za-z0-9_]+' | sort | uniq)

# 对比两个列表
echo "=== 注册但未声明的函数 ==="
comm -23 <(echo "$js_names") <(echo "$declared_names")

echo "=== 声明但未注册的函数 ==="
comm -13 <(echo "$js_names") <(echo "$declared_names")
```

**正确示例**：

```typescript
// types/libentry/index.d.ts
export const myNewFunction: (param: string) => number;
export const otherFunction: () => number;
```

#### 步骤 3：ETS 测试接口使用校验

**校验位置**：`entry/src/ohosTest/ets/test/*.test.ets`

**校验规则**：
- 所有 ETS 测试用例中使用的 `testNapi.xxx` 接口都必须在 `index.d.ts` 中有对应的声明
- 所有 `index.d.ts` 中声明的函数都必须有对应的 N-API 实现
- 不能在 ETS 中使用未声明的接口

**校验命令**：

```bash
# 提取所有 ETS 测试文件中使用的 N-API 接口
used_interfaces=$(grep -h 'testNapi\.' entry/src/ohosTest/ets/test/*.test.ets | grep -oP 'testNapi\.\K[A-Za-z0-9_]+' | sort | uniq)

# 提取 index.d.ts 中声明的函数名称
declared_interfaces=$(grep 'export const' entry/src/main/cpp/types/libentry/index.d.ts | grep -oP 'export const\s+\K[A-Za-z0-9_]+' | sort | uniq)

# 对比使用的接口是否都有声明
echo "=== 使用但未声明的接口 ==="
comm -23 <(echo "$used_interfaces") <(echo "$declared_interfaces")
```

**正确示例**：

```typescript
// ETS 测试文件
import testNapi from 'libentry.so';

it('TestMyFunction', () => {
    let result = testNapi.myNewFunction("test");  // ✅ myNewFunction 已声明
});
```

### 1.5 自动化校验脚本

```bash
#!/bin/bash
# 三重Napi校验脚本
# 用法：./verify_napi_triple.sh <测试套路径>

SUITE_PATH="${1:-.}"
ERRORS=0

echo "========================================="
echo "三重Napi校验"
echo "========================================="
echo "测试套路径: ${SUITE_PATH}"
echo ""

# 步骤 1：N-API 函数注册校验
echo "【步骤 1：N-API 函数注册校验】"
cpp_file="${SUITE_PATH}/entry/src/main/cpp/NapiTest.cpp"
if [ ! -f "$cpp_file" ]; then
    cpp_file="${SUITE_PATH}/entry/src/main/cpp/napi_init.cpp"
fi

if [ -f "$cpp_file" ]; then
    defined_funcs=$(grep -oP 'static napi_value\s+\K[A-Za-z0-9_]+(?=\s*\()' "$cpp_file" | sort | uniq)
    registered_funcs=$(grep -A 100 'napi_property_descriptor desc\[\]' "$cpp_file" | grep -oP '(DECLARE_NAPI_PROPERTY\s*\(\s*"[^"]+"|"[^"]+"\s*,\s*nullptr\s*,\s*[A-Za-z0-9_]+)' | grep -oP '[A-Za-z0-9_]+$' | sort | uniq)
    
    missing=$(comm -23 <(echo "$defined_funcs") <(echo "$registered_funcs"))
    if [ -n "$missing" ]; then
        echo "❌ 定义但未注册的函数："
        echo "$missing"
        ERRORS=$((ERRORS + 1))
    else
        echo "✅ 所有函数都已注册"
    fi
else
    echo "❌ 找不到 NapiTest.cpp 或 napi_init.cpp"
    ERRORS=$((ERRORS + 1))
fi

# 步骤 2：TypeScript 接口声明校验
echo ""
echo "【步骤 2：TypeScript 接口声明校验】"
ts_file="${SUITE_PATH}/entry/src/main/cpp/types/libentry/index.d.ts"
if [ -f "$ts_file" ]; then
    js_names=$(grep -A 100 'napi_property_descriptor desc\[\]' "$cpp_file" 2>/dev/null | grep -oP 'DECLARE_NAPI_PROPERTY\s*\(\s*"\K[^"]+' | sort | uniq)
    declared_names=$(grep 'export const' "$ts_file" | grep -oP 'export const\s+\K[A-Za-z0-9_]+' | sort | uniq)
    
    missing=$(comm -23 <(echo "$js_names") <(echo "$declared_names"))
    if [ -n "$missing" ]; then
        echo "❌ 注册但未声明的函数："
        echo "$missing"
        ERRORS=$((ERRORS + 1))
    else
        echo "✅ 所有函数都已声明"
    fi
else
    echo "❌ 找不到 index.d.ts"
    ERRORS=$((ERRORS + 1))
fi

# 步骤 3：ETS 测试接口使用校验
echo ""
echo "【步骤 3：ETS 测试接口使用校验】"
test_dir="${SUITE_PATH}/entry/src/ohosTest/ets/test"
if [ -d "$test_dir" ]; then
    used_interfaces=$(grep -h 'testNapi\.' "$test_dir"/*.test.ets 2>/dev/null | grep -oP 'testNapi\.\K[A-Za-z0-9_]+' | sort | uniq)
    declared_interfaces=$(grep 'export const' "$ts_file" 2>/dev/null | grep -oP 'export const\s+\K[A-Za-z0-9_]+' | sort | uniq)
    
    missing=$(comm -23 <(echo "$used_interfaces") <(echo "$declared_interfaces"))
    if [ -n "$missing" ]; then
        echo "❌ 使用但未声明的接口："
        echo "$missing"
        ERRORS=$((ERRORS + 1))
    else
        echo "✅ 所有接口都已声明"
    fi
else
    echo "❌ 找不到测试目录"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "========================================="
if [ $ERRORS -eq 0 ]; then
    echo "✅ 三重校验通过！"
    exit 0
else
    echo "❌ 发现 $ERRORS 个错误"
    exit 1
fi
```

---

## 二、编译前工程结构校验

### 2.1 校验时机

**必须在编译前执行，在清理历史编译产物之后**

### 2.2 校验目的

1. 验证工程结构完整性，防止因缺少文件导致编译报错
2. 检查配置文件参数正确性，防止因参数缺失或错误导致编译问题
3. 确保严格遵循模板工程结构

### 2.3 校验内容

#### 2.3.1 必需目录检查

| 序号 | 目录/文件 | 说明 |
|------|----------|------|
| 1 | AppScope/ | 应用级配置 |
| 2 | AppScope/app.json5 | 应用配置文件 |
| 3 | AppScope/resources/base/ | 基础资源 |
| 4 | BUILD.gn | 测试套编译配置 |
| 5 | Test.json | Hypium 测试配置 |
| 6 | build-profile.json5 | 项目构建配置 |
| 7 | oh-package.json5 | 项目包配置 |
| 8 | hvigorfile.ts | Hvigor 构建脚本 |
| 9 | hvigor/hvigor-config.json5 | Hvigor 配置 |
| 10 | signature/ | 签名目录 |
| 11 | signature/openharmony.p7b | 签名文件 |
| 12 | entry/ | 入口模块 |
| 13 | entry/build-profile.json5 | 模块构建配置 |
| 14 | entry/oh-package.json5 | 模块包配置 |
| 15 | entry/hvigorfile.ts | 模块 Hvigor 脚本 |
| 16 | entry/src/main/ | 主模块源码 |
| 17 | entry/src/main/cpp/ | C++ 代码目录 |
| 18 | entry/src/main/cpp/NapiTest.cpp | N-API 封装实现 |
| 19 | entry/src/main/cpp/CMakeLists.txt | CMake 配置 |
| 20 | entry/src/main/cpp/types/libentry/ | 类型定义目录 |
| 21 | entry/src/main/cpp/types/libentry/index.d.ts | TypeScript 类型声明 |
| 22 | entry/src/main/cpp/types/libentry/oh-package.json5 | 类型包配置 |
| 23 | entry/src/main/ets/ | ETS 代码目录 |
| 24 | entry/src/main/ets/entryability/ | Ability 目录 |
| 25 | entry/src/main/ets/entryability/EntryAbility.ts | Ability 实现（注意后缀 .ts） |
| 26 | entry/src/main/ets/pages/ | 页面目录 |
| 27 | entry/src/main/ets/pages/Index.ets | 主页面 |
| 28 | entry/src/main/module.json5 | 模块配置 |
| 29 | entry/src/main/syscap.json | 系统能力配置 |
| 30 | entry/src/main/resources/ | 资源目录 |
| 31 | entry/src/ohosTest/ | 测试模块 |
| 32 | entry/src/ohosTest/ets/test/ | 测试用例目录 |
| 33 | entry/src/ohosTest/ets/test/List.test.ets | 测试套注册文件 |
| 34 | entry/src/ohosTest/ets/testability/ | 测试 Ability 目录 |
| 35 | entry/src/ohosTest/ets/testability/TestAbility.ets | 测试 Ability 实现 |
| 36 | entry/src/ohosTest/ets/testrunner/OpenHarmonyTestRunner.ts | 测试运行器 |
| 37 | entry/src/ohosTest/module.json5 | 测试模块配置 |
| 38 | entry/src/ohosTest/syscap.json | 测试系统能力配置 |

#### 2.3.2 配置文件参数检查

**BUILD.gn 检查**：
- ✅ 包含 `ohos_app_assist_suite` 模板
- ✅ 包含 `ohos_js_app_suite` 模板
- ✅ `hap_name` 正确设置
- ✅ `subsystem_name` 正确设置
- ✅ `part_name` 正确设置
- ✅ `certificate_profile` 指向正确的签名文件

**Test.json 检查**：
- ✅ `driver.type` 为 "OHJSUnitTest"
- ✅ `driver.bundle-name` 与 AppScope 一致
- ✅ `driver.module-name` 正确设置
- ✅ `kits[].test-file-name` 与 `hap_name` 对应

**hap 包名对应检查**：
- ✅ BUILD.gn 中的 `hap_name` 与 Test.json 中的 `test-file-name` 对应

**上层 BUILD.gn 注册检查**：
- ✅ 上层目录的 `group()` deps 中包含当前测试套的编译依赖

**syscap.json 检查**：
- ✅ 包含必要的系统能力声明

#### 2.3.3 TypeScript 与 C++ 一致性检查

- ✅ `index.d.ts` 中的函数声明与 C++ 注册的函数数量一致
- ✅ 函数名称完全匹配

### 2.4 自动化校验脚本

```bash
#!/bin/bash
# 编译前工程结构校验脚本
# 用法：./verify_project_structure.sh <测试套路径>

SUITE_PATH="${1:-.}"
ERRORS=0
WARNINGS=0

echo "========================================="
echo "编译前工程结构校验"
echo "========================================="
echo "测试套路径: ${SUITE_PATH}"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_file() {
    local file="$1"
    local desc="$2"
    local required="$3"
    
    if [ -f "${SUITE_PATH}/${file}" ]; then
        echo -e "${GREEN}✅${NC} $desc"
    else
        if [ "$required" = "required" ]; then
            echo -e "${RED}❌${NC} $desc (缺失)"
            ERRORS=$((ERRORS + 1))
        else
            echo -e "${YELLOW}⚠️${NC} $desc (可选，缺失)"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
}

check_dir() {
    local dir="$1"
    local desc="$2"
    local required="$3"
    
    if [ -d "${SUITE_PATH}/${dir}" ]; then
        echo -e "${GREEN}✅${NC} $desc"
    else
        if [ "$required" = "required" ]; then
            echo -e "${RED}❌${NC} $desc (缺失)"
            ERRORS=$((ERRORS + 1))
        else
            echo -e "${YELLOW}⚠️${NC} $desc (可选，缺失)"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
}

echo "【顶层配置检查】"
check_file "BUILD.gn" "BUILD.gn 文件" "required"
check_file "Test.json" "Test.json 文件" "required"
check_file "build-profile.json5" "build-profile.json5 文件" "required"
check_file "oh-package.json5" "oh-package.json5 文件" "required"
check_file "hvigorfile.ts" "hvigorfile.ts 文件" "required"
check_dir "signature/" "signature/ 目录" "required"
check_file "signature/openharmony.p7b" "签名文件" "required"

echo ""
echo "【AppScope 检查】"
check_dir "AppScope/" "AppScope/ 目录" "required"
check_file "AppScope/app.json5" "AppScope/app.json5 文件" "required"
check_dir "AppScope/resources/base/" "AppScope/resources/base/ 目录" "required"

echo ""
echo "【entry 模块检查】"
check_file "entry/build-profile.json5" "entry/build-profile.json5 文件" "required"
check_file "entry/oh-package.json5" "entry/oh-package.json5 文件" "required"
check_file "entry/hvigorfile.ts" "entry/hvigorfile.ts 文件" "required"

echo ""
echo "【C++ 代码检查】"
check_dir "entry/src/main/cpp/" "entry/src/main/cpp/ 目录" "required"
check_file "entry/src/main/cpp/NapiTest.cpp" "NapiTest.cpp 文件" "required"
check_file "entry/src/main/cpp/CMakeLists.txt" "CMakeLists.txt 文件" "required"
check_file "entry/src/main/cpp/types/libentry/index.d.ts" "index.d.ts 文件" "required"
check_file "entry/src/main/cpp/types/libentry/oh-package.json5" "types oh-package.json5 文件" "required"

echo ""
echo "【ETS 代码检查】"
check_dir "entry/src/main/ets/entryability/" "entry/src/main/ets/entryability/ 目录" "required"
check_file "entry/src/main/ets/entryability/EntryAbility.ts" "EntryAbility.ts 文件（注意后缀 .ts）" "required"
check_file "entry/src/main/ets/pages/Index.ets" "Index.ets 文件" "required"
check_file "entry/src/main/module.json5" "module.json5 文件" "required"
check_file "entry/src/main/syscap.json" "syscap.json 文件" "required"

echo ""
echo "【测试模块检查】"
check_dir "entry/src/ohosTest/ets/test/" "测试用例目录" "required"
check_file "entry/src/ohosTest/ets/test/List.test.ets" "List.test.ets 文件" "required"
check_file "entry/src/ohosTest/ets/testability/TestAbility.ets" "TestAbility.ets 文件" "required"
check_file "entry/src/ohosTest/ets/testrunner/OpenHarmonyTestRunner.ts" "OpenHarmonyTestRunner.ts 文件" "required"
check_file "entry/src/ohosTest/module.json5" "测试模块 module.json5 文件" "required"
check_file "entry/src/ohosTest/syscap.json" "测试模块 syscap.json 文件" "required"

echo ""
echo "【配置文件参数检查】"

# BUILD.gn 模板检查
if grep -q "ohos_app_assist_suite" "${SUITE_PATH}/BUILD.gn" 2>/dev/null; then
    echo -e "${GREEN}✅${NC} BUILD.gn 包含 ohos_app_assist_suite 模板"
else
    echo -e "${RED}❌${NC} BUILD.gn 缺少 ohos_app_assist_suite 模板"
    ERRORS=$((ERRORS + 1))
fi

if grep -q "ohos_js_app_suite" "${SUITE_PATH}/BUILD.gn" 2>/dev/null; then
    echo -e "${GREEN}✅${NC} BUILD.gn 包含 ohos_js_app_suite 模板"
else
    echo -e "${RED}❌${NC} BUILD.gn 缺少 ohos_js_app_suite 模板"
    ERRORS=$((ERRORS + 1))
fi

# hap 包名对应检查
hap_name=$(grep "hap_name" "${SUITE_PATH}/BUILD.gn" 2>/dev/null | grep -oP '"[^"]+"' | head -1 | tr -d '"')
test_file=$(grep "test-file-name" "${SUITE_PATH}/Test.json" 2>/dev/null | grep -oP '"[^"]+\.hap"' | head -1 | sed 's/\.hap"//' | tr -d '"')

if [ -n "$hap_name" ] && [ -n "$test_file" ]; then
    if [ "$hap_name" = "$test_file" ]; then
        echo -e "${GREEN}✅${NC} hap 包名对应正确 (BUILD.gn: $hap_name, Test.json: $test_file)"
    else
        echo -e "${RED}❌${NC} hap 包名不对应 (BUILD.gn: $hap_name, Test.json: $test_file)"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${YELLOW}⚠️${NC} 无法验证 hap 包名对应关系"
    WARNINGS=$((WARNINGS + 1))
fi

# 上层 BUILD.gn 注册检查
parent_dir=$(dirname "${SUITE_PATH}")
suite_dir_name=$(basename "${SUITE_PATH}")
suite_name=$(grep "ohos_js_app_suite" "${SUITE_PATH}/BUILD.gn" 2>/dev/null | grep -oP '"[^"]+"' | head -1 | tr -d '"')

if [ -n "$suite_name" ] && [ -f "${parent_dir}/BUILD.gn" ]; then
    if grep -q "${suite_dir_name}:${suite_name}" "${parent_dir}/BUILD.gn" 2>/dev/null; then
        echo -e "${GREEN}✅${NC} 上层 BUILD.gn 已注册测试套"
    else
        echo -e "${RED}❌${NC} 上层 BUILD.gn 未注册测试套 (${suite_dir_name}:${suite_name})"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${YELLOW}⚠️${NC} 无法验证上层 BUILD.gn 注册"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "========================================="
echo "校验结果统计"
echo "========================================="
echo "错误数: $ERRORS"
echo "警告数: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ 工程结构校验通过！${NC}"
    exit 0
else
    echo -e "${RED}❌ 发现 $ERRORS 个错误，请修复后再编译${NC}"
    exit 1
fi
```

---

## 三、集成到工作流

### 3.1 在测试代码生成后执行三重Napi校验

```bash
# 在生成测试用例后执行
bash verify_napi_triple.sh /path/to/test_suite

# 如果校验失败，输出错误并停止
```

### 3.2 在编译前执行工程结构校验

```bash
# 在清理历史编译产物后、编译前执行
bash verify_project_structure.sh /path/to/test_suite

# 如果校验失败，输出错误并停止编译
```

### 3.3 完整工作流集成

```
1. 生成测试代码
2. ⭐ 执行三重Napi校验 ←── 必需步骤
3. 修复校验发现的问题（如有）
4. 清理历史编译产物
5. ⭐ 执行工程结构校验 ←── 必需步骤
6. 修复校验发现的问题（如有）
7. 执行编译
```

---

## 四、模板工程要求

### 4.1 严格遵循模板

生成新工程时，必须严格按照 `template_project/capi_test_template/` 目录结构生成，不得：

- ❌ 缺少任何必需文件
- ❌ 添加无效参数
- ❌ 修改文件路径或命名
- ❌ 省略可选但推荐的文件

### 4.2 模板文件清单

详见 `test_suite_structure_checklist.md` 中的完整性检查清单。

---

**版本**: 1.0.0
**创建日期**: 2026-03-24
**更新日期**: 2026-03-24
