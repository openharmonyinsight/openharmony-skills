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

**脚本位置**：`scripts/verify_napi_triple.sh`

```bash
bash scripts/verify_napi_triple.sh <测试套路径>
```

校验内容：
- 步骤 1：N-API 函数注册校验（C++ 定义 vs desc[] 注册）
- 步骤 2：TypeScript 接口声明校验（desc[] 注册 vs index.d.ts 声明）
- 步骤 3：ETS 测试接口使用校验（testNapi.xxx 调用 vs index.d.ts 声明）

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

**脚本位置**：`scripts/check_test_suite_structure.sh`

```bash
bash scripts/check_test_suite_structure.sh <测试套路径>
```

校验内容：
- 顶层配置文件检查（BUILD.gn、Test.json、签名文件等）
- AppScope 目录检查
- entry 模块检查（C++ 代码、ETS 代码、module.json5、syscap.json）
- 测试模块检查（List.test.ets、TestAbility、TestRunner）
- BUILD.gn 模板检查（ohos_app_assist_suite、ohos_js_app_suite）
- hap 包名对应检查（BUILD.gn hap_name vs Test.json test-file-name）
- 上层 BUILD.gn 注册检查

### 2.5 文件优先级分层

**一级必需文件（缺失会导致编译失败）**（10 个）：
- `BUILD.gn`、`Test.json`、`build-profile.json5`、`oh-package.json5`、`hvigorfile.ts`、`hvigor/hvigor-config.json5`
- `AppScope/app.json5`、`AppScope/resources/base/element/string.json`
- `signature/openharmony.p7b`
- `.gitignore`

**二级必需文件（缺失会导致编译或运行时错误）**（14 个）：
- `entry/build-profile.json5`、`entry/oh-package.json5`、`entry/hvigorfile.ts`
- `entry/src/main/cpp/NapiTest.cpp`、`entry/src/main/cpp/CMakeLists.txt`
- `entry/src/main/cpp/types/libentry/index.d.ts`、`entry/src/main/cpp/types/libentry/oh-package.json5`
- `entry/src/main/ets/entryability/EntryAbility.ts`（⚠️ 后缀是 .ts 不是 .ets）
- `entry/src/main/ets/pages/Index.ets`、`entry/src/main/module.json5`、`entry/src/main/syscap.json`
- 资源文件：`color.json`、`string.json`、`main_pages.json`、`icon.png`

**三级必需文件（缺失会导致测试无法运行）**（11 个）：
- `entry/src/ohosTest/ets/test/List.test.ets`（⭐ 测试套注册文件）
- `entry/src/ohosTest/ets/test/*.test.ets`（实际测试用例）
- `entry/src/ohosTest/ets/testability/TestAbility.ets`、`pages/Index.ets`
- `entry/src/ohosTest/ets/testrunner/OpenHarmonyTestRunner.ts`
- `entry/src/ohosTest/module.json5`、`entry/src/ohosTest/syscap.json`
- 测试资源文件：`color.json`、`string.json`、`test_pages.json`、`icon.png`

### 2.6 常见错误速查

| 错误 | 错误示例 | 正确做法 |
|------|---------|---------|
| EntryAbility 后缀错误 | `EntryAbility.ets` | `EntryAbility.ts` |
| 签名文件名错误 | `openharmony_sx.p7b` | `openharmony.p7b` |
| 缺少 syscap.json | — | `entry/src/main/syscap.json` 和 `entry/src/ohosTest/syscap.json` 都必需 |
| 缺少 List.test.ets | — | `entry/src/ohosTest/ets/test/List.test.ets` 是测试套注册文件，必须存在 |

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

## 二、N-API 封装生成失败回退策略

### 2.1 失败场景分类

| 失败类型 | 检测方法 | 严重程度 | 常见原因 |
|---------|---------|---------|---------|
| **注册缺失** | C++ 函数定义已存在但未在 desc[] 中注册 | 🔴 Critical | 复制模板时忘记修改 desc[] |
| **声明缺失** | desc[] 中已注册但 index.d.ts 中无声明 | 🔴 Critical | TypeScript 声明生成逻辑错误 |
| **调用未定义** | ETS 中调用了不存在的 testNapi 函数 | 🟡 Medium | 测试用例与 N-API 封装不同步 |
| **签名不匹配** | C++ 参数数量与 TypeScript 不一致 | 🟡 Medium | 参数提取错误 |
| **类型不匹配** | napi_value 与 TypeScript 类型转换失败 | 🟡 Medium | 类型映射规则错误 |

### 2.2 回退决策树

```
N-API 封装生成失败
  ↓
检查失败类型
  ↓
┌─────────────────────────────────────────────────────────────────┐
│ 失败类型 1: 注册缺失                                      │
│                                                             │
│ 症状: C++ 有 static napi_value 定义，但 desc[] 中无对应项  │
│                                                             │
│ 专家判断: 模板复制时忘记更新注册数组                         │
│                                                             │
│ 修复策略:                                                    │
│ 1. 手动添加: DECLARE_NAPI_PROPERTY("funcName", funcName)     │
│ 2. 或: 自动修复脚本                                          │
│    bash scripts/auto_fix_napi_triple.sh {target_path}           │
│                                                             │
│ 预防措施:                                                    │
│ - 每次生成后立即运行 verify_napi_triple.sh                   │
│ - 在 desc[] 数组上方添加 TODO 注释                              │
│                                                             │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│ 失败类型 2: 声明缺失 (index.d.ts)                         │
│                                                             │
│ 症状: desc[] 中已注册，但 index.d.ts 中无 export const       │
│                                                             │
│ 专家判断: TypeScript 声明生成逻辑被条件编译跳过                 │
│                                                             │
│ 修复策略:                                                    │
│ 1. 检查 NapiTest.cpp 中的条件编译宏                         │
│    #ifdef OHOS_ENABLE_CAMERA                                  │
│    static napi_value OH_Camera_Start_napi(...)                │
│    #endif                                                   │
│                                                             │
│ 2. 同步更新 index.d.ts:                                      │
│    export const OH_Camera_Start: ( ... ) => number;            │
│                                                             │
│ 预防措施:                                                    │
│ - 生成时同时生成 C++ 和 TypeScript，不要分步                  │
│ - 在 TypeScript 生成代码中添加检查:                             │
│   // Ensure all desc[] entries have corresponding declaration   │
│                                                             │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│ 失败类型 3: 签名不匹配                                    │
│                                                             │
│ 症状: C++ 参数数量 ≠ TypeScript 参数数量                      │
│                                                             │
│ 专家判断: 参数提取逻辑遇到以下情况之一:                         │
│ - 指针参数被错误解析 (e.g., Camera ** vs Camera *)           │
│ - 函数指针参数被跳过                                         │
│ - 变参函数被错误处理                                         │
│                                                             │
│ 修复策略:                                                    │
│ 1. 对比原始 .h 文件中的函数签名                               │
│ 2. 手动修正 NapiTest.cpp 参数列表                              │
│ 3. 同步修正 index.d.ts 类型签名                               │
│                                                             │
│ 专家经验:                                                    │
│ - 指针参数总是需要 napi_get_value_uint32 之类的提取            │
│ - 函数指针参数需要特殊处理（参考 test_patterns_napi_ets_advance.md）│
│                                                             │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│ 失败类型 4: 复杂类型无法映射                                 │
│                                                             │
│ 症状: C++ 中的结构体/枚举无法直接映射到 TypeScript          │
│                                                             │
│ 专家判断: 遇到以下情况:                                      │
│ - 前向声明的结构体 (typedef struct Camera Camera;)           │
│ - 匿名枚举                                                  │
│ - 宏定义的类型别名                                           │
│                                                             │
│ 修复策略:                                                    │
│ 1. 前向声明结构体: 使用 OpaqueHandle 类型                    │
│    export type OpaqueHandle = number;                          │
│                                                             │
│ 2. 匿名枚举: 生成命名枚举                                  │
│    export enum CameraStatus {                                  │
│      Unknown = 0,                                            │
│      Active = 1,                                             │
│      // ... extracted from header comments or usage            │
│    }                                                        │
│                                                             │
│ 3. 宏定义类型: 展开 macro 并记录映射关系                      │
│                                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 自动修复脚本

使用 `scripts/auto_fix_napi_triple.sh` 自动修复常见问题：

```bash
# 用法
bash scripts/auto_fix_napi_triple.sh /path/to/test/suite

# 修复内容
1. 自动添加缺失的 N-API 函数注册
2. 自动添加缺失的 TypeScript 声明
3. 验证修复结果
```

### 2.4 人工修复检查清单

当自动修复失败时，使用此清单进行人工修复：

```markdown
## N-API 失败人工修复检查清单

- [ ] **注册完整性检查**
  - [ ] 每个 static napi_value 函数都在 desc[] 中有对应的 DECLARE_NAPI_PROPERTY
  - [ ] desc[] 数组以 `};` 正确结束
  - [ ] Init 函数调用了 `napi_define_properties`

- [ ] **TypeScript 声明检查**
  - [ ] 每个 export const 名称与 desc[] 中的注册名称一致
  - [ ] 参数类型与 C++ 参数类型匹配
  - [ ] 返回类型正确（通常是 `Promise<void>` 或 `number`）

- [ ] **ETS 测试检查**
  - [ ] 所有 testNapi.xxx 调用都有对应的 TypeScript 声明
  - [ ] 异步函数使用了 `await testNapi.xxx()`
  - [ ] 错误处理使用了 try-catch 并验证错误码

- [ ] **条件编译同步**
  - [ ] #ifdef 块在 C++ 和 TypeScript 中保持一致
  - [ ] 被跳过的函数没有生成测试用例

- [ ] **复杂类型处理**
  - [ ] 指针参数正确使用 napi_get_value_uint32 等提取函数
  - [ ] 函数指针参数参考 test_patterns_napi_ets_advance.md
  - [ ] 结构体参数正确转换为 TypeScript 对象
```

### 2.5 失败记录与学习

每次修复失败后，记录到失败知识库：

```json
{
  "failure_id": "NAPI-FAIL-001",
  "timestamp": "2026-05-12T10:30:00Z",
  "failure_type": "registration_missing",
  "function_name": "OH_Camera_SetPreviewCallback",
  "root_cause": "Function pointer parameter caused parameter extraction to skip function entirely",
  "resolution": "Manually added registration and updated parameter extraction logic",
  "prevention": "Update parameter extraction to handle function pointers correctly"
}
```

这些记录用于持续改进参数提取逻辑，减少未来失败。

---

## 四、模板工程要求

### 4.1 严格遵循模板

生成新工程时，必须严格按照 `template_project/capi_test_template/` 目录结构生成，不得：

- ❌ 缺少任何必需文件
- ❌ 添加无效参数
- ❌ 修改文件路径或命名
- ❌ 省略可选但推荐的文件

### 4.2 模板文件清单

详见本文档 2.5 节「文件优先级分层」中的完整性检查清单。

---

**版本**: 1.0.0
**创建日期**: 2026-03-24
**更新日期**: 2026-03-24
