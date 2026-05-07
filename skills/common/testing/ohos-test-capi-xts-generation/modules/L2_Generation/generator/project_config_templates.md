# 工程配置模板指南

> **工程配置模板** - CAPI 测试套的完整工程配置指南，包含 Test.json、oh-package.json5、BUILD.gn 和测试套结构

> 📖 **相关文档**：
> - **[测试用例生成模块](./test_generation_c.md)** - 测试用例生成策略和规范 ⭐
> - **[N-API 和 ETS 公共模式](./test_patterns_napi_ets.md)** - N-API 封装和 ETS 测试的公共模式
> - **[N-API 和 ETS 高级模式](./test_patterns_napi_ets_advance.md)** - N-API 封装和 ETS 测试的高级模式
> - **[测试套结构检查清单](./test_suite_structure_checklist.md)** - 文件结构完整性检查 ⭐

## 概述

**配置文件层次**：
| 层级 | 文件 | 作用 |
|------|------|------|
| **模块级** | `types/[库名]/oh-package.json5` | 定义动态链接库的元信息和类型定义 |
| **项目级** | `entry/oh-package.json5` | 管理项目依赖和类型定义引用 |
| **工程级** | `oh-package.json5` (根目录) | 全局配置（依赖覆盖、依赖重写） |
| **测试配置** | `Test.json` | 测试套的运行配置 |
| **构建配置** | `hvigor/hvigor-config.json5` | Hvigor 构建系统配置 |

---

## Test.json 配置

### 1. 基础配置

```json
{
    "description": "Configuration for Tests",
    "driver": {
        "type": "OHJSUnitTest",
        "test-timeout": "180000",
        "shell-timeout": "180000",
        "bundle-name": "[包名]",
        "module-name": "[模块名]"
    },
    "kits": [
        {
            "test-file-name": [
                "[HAP文件名].hap"
            ],
            "type": "AppInstallKit",
            "cleanup-apps": true
        }
    ]
}
```

### 2. 完整配置

```json
{
    "description": "Configuration for N-API CAPI Test Suite",
    "driver": {
        "type": "OHJSUnitTest",
        "test-timeout": "300000",
        "shell-timeout": "300000",
        "bundle-name": "com.ohos.test.napi",
        "module-name": "entry",
        "test-timeout-unit": "ms",
        "shell-timeout-unit": "ms",
        "case-timeout": "60000"
    },
    "kits": [
        {
            "test-file-name": [
                "ActsNapiTest.hap"
            ],
            "type": "AppInstallKit",
            "cleanup-apps": true,
            "hap-install-mode": "force"
        },
        {
            "test-file-name": [
                "TestResource1.hap"
            ],
            "type": "AppInstallKit",
            "cleanup-apps": false
        }
    ],
    "policies": {
        "access-locations": [
            "internal://app/"
        ]
    },
    "dump-config": {
        "case-dump": true,
        "system-dump": true
    }
}
```

### 3. 配置项说明

| 配置项 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| `description` | String | 是 | 测试套的描述信息 |
| `driver.type` | String | 是 | 测试框架类型（OHJSUnitTest） |
| `driver.test-timeout` | Number | 否 | 单个测试超时时间（ms） |
| `driver.shell-timeout` | Number | 否 | Shell 命令超时时间（ms） |
| `driver.bundle-name` | String | 是 | 测试包名（如 com.ohos.test.napi） |
| `driver.module-name` | String | 是 | 模块名（如 entry） |
| `kits` | Array | 是 | 测试套件配置列表 |
| `kits[].test-file-name` | Array | 是 | 要测试的 HAP 文件列表 |
| `kits[].type` | String | 是 | 套件类型（AppInstallKit） |
| `kits[].cleanup-apps` | Boolean | 否 | 测试后是否清理应用 |
| `policies` | Object | 否 | 测试策略配置 |
| `dump-config` | Object | 否 | Dump 配置 |

---

## oh-package.json5 配置规范

### 1. 模块级配置文件

**位置**: `src/main/cpp/types/[库名]/oh-package.json5` — 定义动态链接库的元信息和类型定义

**配置示例**:
```json5
{
  "name": "libentry.so",
  "types": "./index.d.ts",
  "version": "",
  "description": "N-API wrapper library for CAPI testing"
}
```

**字段说明**:
| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | String | 是 | 库的唯一标识符（如 "libentry.so"） |
| `types` | String | 是 | 类型定义文件路径（指向 "./index.d.ts"） |
| `version` | String | 否 | 版本号（构建时自动填充） |
| `description` | String | 否 | 库描述信息 |

### 2. 项目级配置文件

**位置**: `entry/oh-package.json5` — 管理项目依赖关系和类型定义引用

**配置示例**:
```json5
{
  "license": "",
  "devDependencies": {
    "@types/libentry.so": "file:./src/main/cpp/types/libentry"
  },
  "author": "",
  "name": "entry",
  "description": "CAPI test suite entry",
  "main": "",
  "version": "1.0.0",
  "dependencies": {}
}
```

**字段说明**:
| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | String | 是 | 项目名称（如 "entry"） |
| `version` | String | 否 | 项目版本号 |
| `devDependencies` | Object | 否 | 开发依赖配置，引用类型定义文件 |
| `dependencies` | Object | 否 | 生产依赖 |
| `license` | String | 否 | 开源许可证 |
| `author` | String | 否 | 作者信息 |
| `description` | String | 否 | 项目描述 |

### 3. 工程级配置文件

**位置**: 项目根目录 `oh-package.json5` — 全局配置（overrides、overrideDependencyMap、parameterFile）

**配置示例**:
```json5
{
  "overrides": {
    "@types/libentry.so": "file:./test/xts/acts/overrides/libentry"
  },
  "overrideDependencyMap": {
    "@types/libentry.so": "file:./test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsbmsgetabilityresourcendkenterprisetest/entry/src/main/cpp/types/libentry"
  },
  "parameterFile": "./parameters.json"
}
```

**字段说明**:
| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `overrides` | Object | 否 | 依赖覆盖配置 |
| `overrideDependencyMap` | Object | 否 | 依赖关系重写配置 |
| `parameterFile` | String | 否 | 参数化配置文件路径 |

### 4. 配置文件查找和使用

查找优先级：**工程级 > 项目级 > 模块级**（工程级覆盖项目级，项目级引用模块级）。项目级通过 `devDependencies` 引用模块级配置的库。

---

## 测试套目录结构

> 📋 **完整目录结构详见**：[测试套结构检查清单](./test_suite_structure_checklist.md)

### ETS 测试文件路径规范（⭐ 重要）

**⚠️ 硬性规范**：
- ETS 测试文件**必须**位于 `entry/src/ohosTest/ets/test/` 目录
- **不是** `entry/src/main/ets/test/` 或其他位置
- 这是 XTS 测试套的标准规范，违反会导致编译失败

**标准目录结构**：
```
entry/
└── src/
    └── ohosTest/              # 测试模块根目录
        └── ets/
            └── test/          # ⭐ ETS 测试文件标准位置
                ├── List.test.ets        # 测试套注册文件
                ├── [测试套名].test.ets  # 主测试文件
                └── [其他测试].test.ets  # 其他测试文件（可选）
```

**常见错误**：`entry/src/main/ets/test/`（在 main 下）、`entry/src/ets/test/`（缺 ohosTest）、`ets/test/`（直接根目录）均为错误位置。正确位置：`entry/src/ohosTest/ets/test/`。

### BUILD.gn 双层级更新（⭐ 关键）

> ⚠️ **两个层级的 BUILD.gn 都需要同步更新**，否则编译失败：
> - 测试套目录 BUILD.gn：定义测试套类型（`ohos_js_app_suite`）
> - 上层目录 BUILD.gn：在 `group()` 的 deps 中添加测试套依赖
>
> 完整配置示例见下方 [BUILD.gn 配置](#buildgn-配置) 章节

### 测试套参考示例

| 测试套 | 参考路径 | 特点 |
|--------|----------|------|
| BundleManager | `{OH_ROOT}/test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsbmsgetabilityresourcendkenterprisetest` | 标准单库 N-API 封装，配置文件层次完整 |
| ArkUI | `{OH_ROOT}/test/xts/acts/arkui/ace_c_arkui_test_api20` | 多库封装（libnativefunc.so、libnativerender.so），每个库独立模块级配置 |

---

## TypeScript 类型定义

### index.d.ts 示例

**位置**: `src/main/cpp/types/libentry/index.d.ts` — 为 N-API 模块提供 TypeScript 类型定义

**示例**:
```typescript
export const [函数名]_NormalTest: (param1: string, param2: number) => number;
export const [函数名]_ErrorCodeTest: (param1: string) => void;
export const [函数名]_EnumTest: (param1: number) => number;
export const [函数名]_BoolTest: (param1: boolean) => boolean;
export const [函数名]_ParamValidationTest: (param1: string) => void;
```

**同步规则**：
1. 每添加一个 N-API 封装函数，需要在 `napi_property_descriptor` 数组中注册
2. 每注册一个函数，需要在 `index.d.ts` 中添加对应的类型定义
3. 函数签名必须与 C++ 实现一致（参数类型、返回类型）
4. 三者必须同步：C++ 注册 + TS 声明 + ETS 调用

### TypeScript 声明完整性验证

> 📋 **TypeScript 声明完整性验证方法详见**：[通用校验模块 - 三重Napi校验](./verification_common.md#一三重napi校验)
>
> 或使用自动化脚本：`./scripts/verify_napi_triple.sh <测试套路径>`

---

## BUILD.gn 配置

### 1. 测试套目录 BUILD.gn

```cpp
import("//test/xts/tools/build/suite.gni")

ohos_app_assist_suite("ActsAbilityContextApiMain") {
  testonly = true
  certificate_profile = "./signature/openharmony_sx.p7b"
  hap_name = "ActsAbilityContextApiMain"
  part_name = "ability_runtime"
  subsystem_name = "ability"
}

ohos_js_app_suite("ActsAbilityContextApiTest") {
  test_hap = true
  testonly = true
  certificate_profile = "./signature/openharmony_sx.p7b"
  hap_name = "ActsAbilityContextApiTest"
  part_name = "ability_runtime"
  subsystem_name = "ability"
  deps = [ ":ActsAbilityContextApiMain" ]
}
```

**⚠️ 配置说明**：

| 配置项 | 必需 | 说明 |
|--------|------|------|
| `test_hap` | **是** | 设置为 true，表示测试时需要安装 HAP |
| `testonly` | **是** | 设置为 true，表示仅用于测试 |
| `certificate_profile` | **是** | 签名文件路径，通常为 `./signature/openharmony_sx.p7b` |
| `hap_name` | **是** | HAP 文件名称 |
| `part_name` | **是** | 所属部件名称 |
| `subsystem_name` | **是** | 所属子系统名称 |
| `deps` | **是** | 依赖辅助 HAP（ohos_app_assist_suite 的名称） |

**重要规则**：
1. **必须同时定义两个模板**：`ohos_app_assist_suite` 和 `ohos_js_app_suite`
2. `ohos_js_app_suite` 的 deps 必须引用 `ohos_app_assist_suite`
3. 两个模板的名称应保持一致，辅助 HAP 添加 `_Main` 或 `_Assist` 后缀
4. **不要使用** `ohos_js_app_static_suite`（已淘汰）

### 2. 上层目录 BUILD.gn（⭐ 关键步骤）

> ⚠️ **重要**：两个层级的 BUILD.gn 都需要更新！

**格式**：在 group() 的 deps 中添加新测试套的编译依赖

```cpp
# [abilitycapitest]/BUILD.gn
group("abilitycapitest") {
  testonly = true
  if (is_standard_system) {
    deps = [
      "actscapistartselfuiabilitytest:ActsCapiStartSelfUiAbilityTest",
      "actsabilitycontextapitest:ActsAbilityContextApiTest",  # ⭐ 新增测试套
    ]
  }
}
```

### 3. 静态和动态测试套区别

| 类型 | 配置 | 说明 |
|------|------|------|
| **静态测试套** | `ohos_js_app_static_suite` | 测试用例在编译时打包到 HAP 中，运行时无需重新编译 |
| **动态测试套** | `ohos_js_app_suite` + `test_hap = true` | 测试用例在运行时动态加载到设备，需要先安装 HAP |

---

## Hvigor 配置

### 1. hvigor-config.json5 配置

**位置**: `hvigor/hvigor-config.json5` — 配置 Hvigor 构建系统的版本和依赖

**配置示例**（⚠️ 实际文件需包含 Apache License 2.0 版权声明头部）:
```json5
{
  "modelVersion": "6.0.0",
  "dependencies": {
  }
}
```

**字段说明**:
| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `modelVersion` | String | 是 | Hvigor 配置模型版本（如 "6.0.0"） |
| `dependencies` | Object | 否 | 自定义依赖配置 |

**⚠️ 注意事项**：
- 必须包含 Apache License 2.0 版权声明
- `modelVersion` 通常为 "6.0.0"
- 对于标准测试套，`dependencies` 通常为空对象

### 2. hvigorfile.ts 配置

**位置**: `[测试套根目录]/hvigorfile.ts` 和 `entry/hvigorfile.ts` — 定义 Hvigor 构建任务

**根目录和 entry 目录的 hvigorfile.ts 配置相同**:
```typescript
import { hapTasks } from '@ohos/hypium'

export default {
  system: "harmonyos",
  compilerOptions: {
    sourceMaps: true
  },
  rules: [
    ...hapTasks()
  ]
}
```

**⚠️ 注意事项**：
- 测试套使用 `@ohos/hypium` 插件（不是 `@ohos/hvigor-ohos-plugin`）
- `system` 必须为 `"harmonyos"`，`rules` 必须展开 `hapTasks()`
- 两个 hvigorfile.ts（根目录和 entry）内容通常相同

---

## 配置最佳实践

### 1. 配置文件命名规范

| 配置类型 | 文件名 | 位置 |
|---------|--------|------|
| 测试套配置 | `Test.json` | 测试套根目录 |
| 模块配置 | `oh-package.json5` | `types/[库名]/` 目录 |
| 项目配置 | `oh-package.json5` | 测试套根目录 |
| 工程配置 | `oh-package.json5` | 工程根目录 |

### 2. 配置同步规则

**三步同步检查清单**（遗漏任一步都会导致编译失败）：
1. ✅ 在 `napi_property_descriptor` 数组中添加函数注册（遗漏→编译错误：函数未注册）
2. ✅ 在 `types/libentry/index.d.ts` 中添加 `export const` 声明（遗漏→TS编译错误）
3. ✅ 在上层目录的 `BUILD.gn` 的 `group()` deps 中添加测试套依赖（遗漏→找不到测试套）

### 3. 版本号管理

- 模块级 `version` 由构建系统自动填充；项目级 `version` 由开发者维护；建议保持一致

---

## 快速参考

| 类别 | 关键配置 |
|------|----------|
| **Test.json** | 标准超时 180000ms，长测试 300000ms，性能测试 600000ms |
| **oh-package.json5** | 库名 `libentry.so`，类型 `./index.d.ts`，依赖 `@types/libentry.so: file:./...` |
| **BUILD.gn** | 类型 `ohos_js_app_suite` + `test_hap=true` + `testonly=true`，需同时定义 `ohos_app_assist_suite` |
| **Hvigor** | modelVersion `6.0.0`，system `"harmonyos"`，插件 `@ohos/hypium` |
| **ETS 路径** | ✅ `entry/src/ohosTest/ets/test/` ❌ `entry/src/main/ets/test/` |

---

## ⭐ 必需文件清单

> **重要**：生成测试套时，必须确保以下所有文件都已创建。缺少任一文件都会导致编译失败。

### 1. 根目录必需文件

| 序号 | 文件路径 | 说明 | 来源 |
|------|----------|------|------|
| 1 | `BUILD.gn` | 测试套编译配置 | 从模板生成 |
| 2 | `Test.json` | Hypium 测试配置 | 从模板生成 |
| 3 | `oh-package.json5` | 工程级包配置 | 从模板生成 |
| 4 | `build-profile.json5` | 工程级构建配置 | 从模板生成，**必须包含SDK版本** |
| 5 | `hvigorfile.ts` | Hvigor 构建脚本（根） | 从模板生成 |
| 6 | `hvigor/hvigor-config.json5` | Hvigor 配置 | 从模板生成 |
| 7 | `AppScope/app.json5` | 应用配置 | 从模板生成 |
| 8 | `.gitignore` | Git 忽略配置 | 从模板生成（可选） |

### 2. entry 目录必需文件

| 序号 | 文件路径 | 说明 | 来源 |
|------|----------|------|------|
| 9 | `entry/oh-package.json5` | 项目级包配置 | 从模板生成 |
| 10 | `entry/build-profile.json5` | 项目级构建配置 | 从模板生成 |
| 11 | `entry/hvigorfile.ts` | Hvigor 构建脚本（entry） | 从模板生成 |
| 12 | `entry/src/main/module.json5` | 主模块配置 | 从模板生成 |
| 13 | `entry/src/main/syscap.json` | 系统能力配置 | 从模板生成 |
| 14 | `entry/src/main/cpp/NapiTest.cpp` | N-API 封装实现 | 根据API生成 |
| 15 | `entry/src/main/cpp/CMakeLists.txt` | CMake 构建配置 | 从模板生成 |
| 16 | `entry/src/main/cpp/types/libentry/index.d.ts` | TypeScript 类型定义 | 根据N-API函数生成 |
| 17 | `entry/src/main/cpp/types/libentry/oh-package.json5` | 模块级包配置 | 从模板生成 |
| 18 | `entry/src/main/ets/entryability/EntryAbility.ts` | 入口 Ability | 从模板生成（注意后缀为.ts） |
| 19 | `entry/src/main/ets/pages/Index.ets` | 主页面 | 从模板生成 |
| 20 | `entry/src/ohosTest/module.json5` | 测试模块配置 | 从模板生成 |
| 21 | `entry/src/ohosTest/syscap.json` | 测试系统能力 | 从模板生成 |
| 22 | `entry/src/ohosTest/ets/test/List.test.ets` | 测试套注册 | 从模板生成 |
| 23 | `entry/src/ohosTest/ets/testability/TestAbility.ets` | 测试 Ability | 从模板生成 |
| 24 | `entry/src/ohosTest/ets/testrunner/OpenHarmonyTestRunner.ts` | 测试运行器 | 从模板生成 |

### 3. 签名文件（⭐ 关键）

| 序号 | 文件路径 | 说明 | 来源 |
|------|----------|------|------|
| 25 | `signature/openharmony_sx.p7b` | 签名文件 | **从参考测试套复制** |

**⚠️ 签名文件获取方式**：
```bash
# 从同领域参考测试套复制签名文件
cp {OH_ROOT}/test/xts/acts/{子系统}/{参考测试套}/signature/openharmony_sx.p7b {新测试套}/signature/
```

### 4. 资源文件

| 序号 | 文件路径 | 说明 |
|------|----------|------|
| 26 | `AppScope/resources/base/element/string.json` | 应用字符串资源 |
| 27 | `AppScope/resources/base/media/app_icon.png` | 应用图标 |
| 28 | `entry/src/main/resources/base/element/color.json` | 颜色资源 |
| 29 | `entry/src/main/resources/base/element/string.json` | 字符串资源 |
| 30 | `entry/src/main/resources/base/profile/main_pages.json` | 页面配置 |
| 31 | `entry/src/main/resources/base/media/icon.png` | 模块图标 |
| 32 | `entry/src/ohosTest/resources/base/element/color.json` | 测试颜色资源 |
| 33 | `entry/src/ohosTest/resources/base/element/string.json` | 测试字符串资源 |
| 34 | `entry/src/ohosTest/resources/base/profile/test_pages.json` | 测试页面配置 |
| 35 | `entry/src/ohosTest/resources/base/media/icon.png` | 测试图标 |

---

## ⭐ build-profile.json5 SDK 版本配置

> **⚠️ 重要**：`build-profile.json5` 必须包含 SDK 版本配置，否则 hvigor 检查会失败。

### 配置模板

```json5
{
  "app": {
    "products": [
      {
        "name": "default",
        "signingConfig": "default",
        "compileSdkVersion": 24,
        "compatibleSdkVersion": 20,
        "targetSdkVersion": 20,
        "runtimeOS": "OpenHarmony"
      }
    ],
    "signingConfigs": []
  },
  "modules": [
    {
      "name": "entry",
      "srcPath": "./entry",
      "targets": [
        {
          "name": "default",
          "applyToProducts": [
            "default"
          ]
        }
      ]
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `compileSdkVersion` | Number | **是** | 编译 SDK 版本（如 24） |
| `compatibleSdkVersion` | Number | **是** | 兼容 SDK 版本（如 20） |
| `targetSdkVersion` | Number | **是** | 目标 SDK 版本（如 20） |
| `runtimeOS` | String | **是** | 运行时操作系统（"OpenHarmony"） |

### 获取参考配置

```bash
# 从参考测试套读取 SDK 配置
cat {OH_ROOT}/test/xts/acts/{子系统}/{参考测试套}/build-profile.json5
```

---

## ⭐ 工程结构同步校验

> 📋 **工程结构三步同步校验（目录完整性 + 配置一致性 + BUILD.gn 同步）详见**：
> - [通用校验模块 - 编译前工程结构校验](./verification_common.md#二编译前工程结构校验)
> - [测试套结构检查清单](./test_suite_structure_checklist.md)

---

**版本**: 1.2.0
**创建日期**: 2026-03-19
**更新日期**: 2026-03-28
**兼容性**: OpenHarmony API 10+

**更新日志**:
- v1.2.0 (2026-03-28): 精简文档，验证脚本和校验流程移至 verification_common.md，测试套示例精简为参考表格
- v1.1.0 (2026-03-24): 添加必需文件清单、工程结构三步同步校验、SDK版本配置规范
- v1.0.0 (2026-03-19): 初始版本
