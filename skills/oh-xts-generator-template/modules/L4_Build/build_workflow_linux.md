# Linux 编译工作流

> **模块信息**
> - 层级：L4_Build
> - 优先级：按需加载
> - 适用范围：Linux 环境下的 XTS 测试工程编译
> - 平台：Linux
> - 依赖：L1_Framework, L2_Analysis, L3_Generation
> - 相关：`build_workflow_windows.md`（Windows 编译方案）

> **⚠️ 重要提示（Linux 环境）**
>
> **在 Linux 环境下编译 XTS 测试工程，必须使用 `./test/xts/acts/build.sh` 脚本进行编译。**
>
> - ✅ **正确方式**：使用 `./test/xts/acts/build.sh` 脚本
> - ❌ **错误方式**：不要使用 `hvigorw` 命令
>
> **原因**：
> 1. `./test/xts/acts/build.sh` 是 XTS 测试工程的官方编译脚本
> 2. `./test/xts/acts/build.sh` 会正确处理依赖关系和测试套结构
> 3. `hvigorw` 是 Windows/DevEco Studio 的编译工具，不适用于 Linux 环境
> 4. 使用 `hvigorw` 可能导致编译失败或生成的 HAP 包不正确
>
> **编译命令示例**：
> ```bash
> # 正确：使用 ./test/xts/acts/build.sh
> ./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest
>
> # 错误：不要使用 hvigorw（Linux 环境下不适用）
> # hvigorw assembleHap  # ❌ 不要在 Linux 环境下使用
> ```

---

## 一、模块概述

Linux 编译工作流模块提供在 Linux 环境下 OpenHarmony XTS 测试工程的完整编译指导。

### 1.1 核心功能

- **编译工作流导航** - 指导动态和静态测试套编译流程
- **编译命令** - 单目标、多目标编译命令
- **编译验证** - 编译产物验证方法
- **subagent 执行** - 使用 general subagent 执行编译任务，避免主流程中断
- **监听机制** - 监听编译进程直至完成，确保编译状态正确返回
- **错误处理** - 自动修复语法错误，配置错误需确认后修改

### 1.2 应用场景

1. 准备 Linux 编译环境
2. 确认 BUILD.gn 中的编译目标
3. 执行预编译清理
4. 选择编译类型（动态或静态）
5. 使用 subagent 执行编译任务
6. 监听编译进程直至完成
7. 处理编译错误（自动修复语法错误，配置错误需确认）
8. 验证编译产物

### 1.3 相关模块（按需加载）

| 任务类型 | 加载模块 |
|---------|---------|
| **环境准备** | [linux_compile_env_setup.md](./linux_compile_env_setup.md) |

| **预编译清理** | [linux_prebuild_cleanup.md](./linux_prebuild_cleanup.md) |
| **问题排查** | [linux_compile_troubleshooting.md](./linux_compile_troubleshooting.md) |
| **动态测试套编译** | [linux_compile_dynamic_suite.md](./linux_compile_dynamic_suite.md) |
| **静态测试套编译** | [linux_compile_static_suite.md](./linux_compile_static_suite.md) |

### 1.4 编译方式说明（重要）

**Linux 环境下的唯一正确编译方式**：

| 环境 | 编译工具 | 编译命令 | 说明 |
|------|---------|---------|------|
| **Linux** | `build.sh` | `./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称}` | ✅ **必须使用** |
| **Windows** | `hvigorw.bat` | `hvigorw.bat assembleHap ...` | Windows 专用 |

**Linux 环境下不要使用的方式**：
- ❌ 不要使用 `hvigorw` 命令
- ❌ 不要使用 DevEco Studio 的编译功能（Windows 专用）
- ❌ 不要尝试直接调用 GN 或 Ninja 命令

**为什么 Linux 必须使用 build.sh**：
1. `build.sh` 封装了完整的编译流程
2. 正确处理 OpenHarmony 的构建系统（GN + Ninja）
3. 自动配置环境变量和工具链
4. 支持测试套的特定编译需求
5. 与 XTS 测试框架完全兼容

---

## 二、编译类型选择

### 2.1 动态测试套 vs 静态测试套

| 特性 | 动态测试套 | 静态测试套 |
|------|-----------|-----------|
| **BUILD.gn 中的编译目标** | `ohos_js_app_suite()` | `ohos_js_app_static_suite()` |
| **test_hap 标志** | `test_hap = true` | **不设置** test_hap |
| **编译参数** | 默认（不指定 xts_suitetype） | **必须指定** `xts_suitetype=hap_static` |
| **SDK 编译** | 使用系统现有 SDK | **同步编译**静态 SDK |
| **适用场景** | 普通测试套 | 需要 arkTS 静态语法的测试套 |
| **HAP 包** | 动态 HAP | 静态 HAP |

### 2.2 如何选择编译类型

#### 选择动态测试套编译

**适用情况**：
- 普通的 XTS 测试套
- 不需要 arkTS 静态语法特性
- 大多数现有测试套

**编译命令**：
```bash
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称}
```

**详细文档**：[linux_compile_dynamic_suite.md](./linux_compile_dynamic_suite.md)

#### 选择静态测试套编译

**适用情况**：
- 需要 arkTS 静态语法的测试套（如 API 23+）
- 使用了静态语言特性的测试代码
- 明确标注为静态测试套

**编译命令**：
```bash
# 首次编译前清理 SDK 缓存
cd {OH_ROOT}
rm -rf prebuilts/ohos-sdk/linux

# 编译静态测试套
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard xts_suitetype=hap_static suite={测试套名称}
```

**详细文档**：[linux_compile_static_suite.md](./linux_compile_static_suite.md)

### 2.3 工作流程图

```
┌─────────────────────────────────────────────────────────────┐
│              Linux 编译工作流（主入口）                   │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
          ┌───────────────────────────────┐
          │  步骤1：环境准备（首次必需）  │
          │  模块：linux_compile_env_setup │
          └───────────────────────────────┘
                             │
                             ▼
          ┌───────────────────────────────┐
           │  步骤2：确认 BUILD.gn 编译目标  │
          └───────────────────────────────┘
                             │
                             ▼
          ┌───────────────────────────────┐
          │  步骤3：预编译清理（每次必需）  │
          │  模块：linux_prebuild_cleanup  │
          └───────────────────────────────┘
                             │
                             ▼
          ┌───────────────────────────────┐
          │  步骤4：选择编译类型           │
          │  ┌───────────────┐          │
          │  │ 动态测试套？ │          │
          │  └───────┬───────┘          │
          │          │                    │
          │         Yes│No                │
          │          │                   │
          │     ┌────▼─────┐            │
          │     │ 步骤5a：    │ 步骤5b：   │
          │     │ 动态编译    │ 静态编译   │
          │     │ └─────────────┘            │
          │     └──────────────┬─────────────┘  │
          │                    │              │
          │                    ▼              │
          │     ┌───────────────────────────────┐  │
          │     │  步骤5c：subagent 执行编译   │  │
          │     │  （使用 general subagent）   │  │
          │     └───────────────────────────────┘  │
          │                    │              │
          │                    ▼              │
          │     ┌───────────────────────────────┐  │
          │     │  步骤5d：监听编译进程         │  │
          │     │  （等待编译完成）             │  │
          │     └───────────────────────────────┘  │
          │                    │              │
          │                    ▼              │
          │     ┌───────────────────────────────┐  │
          │     │  步骤6：编译结果处理         │  │
          │     │  ┌─────────────────────┐   │  │
          │     │  │ 编译成功？          │   │  │
          │     │  │  ┌───┬──────┐       │   │  │
          │     │  │  │Yes│   No │       │   │  │
          │     │  │  │   │      │       │   │  │
          │     │  │  ▼   ▼      │       │   │  │
          │     │  │完成 错误处理│       │   │  │
          │     │  └─────┬──────┘       │   │  │
          │     └─────────┼──────────────┘   │  │
          │               │                  │  │
          │               ▼                  │  │
          │     ┌───────────────────────────────┐  │
          │     │  步骤7：错误处理（如有）     │  │
          │     │  ├─ 语法错误：自动修复      │  │
          │     │  ├─ 配置错误：确认后修改    │  │
          │     │  └─ 其他错误：手动排查      │  │
          │     └───────────────────────────────┘  │
          └──────────────────┬─────────────────────┘
                             │
                             ▼
                    编译成功？
                     │      │
                    Yes     No
                     │      │
                     │      └──────────► 步骤8：问题排查
                     │                   模块：linux_compile_troubleshooting
                     │
                     ▼
               编译完成
```

---

## 三、快速参考

### 3.1 编译类型对照表

| 编译类型 | 详细文档 | 编译命令 | 特殊要求 |
|---------|---------|---------|---------|
| **动态测试套** | [linux_compile_dynamic_suite.md](./linux_compile_dynamic_suite.md) | `./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称}` | 无特殊要求 |
| **静态测试套** | [linux_compile_static_suite.md](./linux_compile_static_suite.md) | `./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称} xts_suitetype=hap_static` | 1. 清理 SDK 缓存<br>2. 添加 hap_static 参数 |

### 3.2 参考路径

| 类型 | 路径 |
|------|------|
| 编译脚本 | `./test/xts/acts/build.sh` |
| 模板文件 | `./test/xts/tools/build/suite.gni` |
| 测试框架 | `./test/xts/acts/` |
| 编译输出 | `out/{product_name}/suites/acts/acts/testcases/` |

---

## 三、编译命令说明

### 3.1 编译命令执行规范（重要）

> **⚠️ 编译命令执行要求**
>
> - ✅ **执行位置**：必须在 **OH_ROOT 目录**下执行编译命令
> - ✅ **必选参数**：`product_name=rk3568 system_size=standard` 为必选参数，不可修改或省略
> - ✅ **默认编译类型**：动态测试套（无需指定 `xts_suitetype` 参数）
> - ✅ **subagent 执行**：必须使用 general subagent 执行编译任务，避免主流程中断
> - ✅ **监听机制**：必须监听编译进程直至完成，确保编译状态正确返回
> - ❌ **禁止操作**：不要在测试套目录下执行编译命令
> - ❌ **禁止操作**：不要修改 `product_name` 和 `system_size` 参数值
> - ❌ **禁止操作**：不要在主流程直接执行编译命令，必须通过 subagent

> **📌 subagent 执行规范（v1.16.0+）**
>
> - **执行方式**：使用 general subagent 执行编译任务
> - **监听机制**：持续监听编译进程，直至完成
> - **错误处理**：
>   - **语法错误**：自动分析错误日志，修复语法问题并重试编译
>   - **配置错误**：检测到工程配置问题时，暂停编译，向用户确认后才修改
> - **返回结果**：subagent 必须返回详细的编译结果和错误信息

### 3.2 单目标编译

#### 3.2.1 标准编译命令

```bash
# 在 OH_ROOT 目录下执行
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称}
```

**完整示例**：
```bash
# 示例 1：编译动态测试套（默认，无需指定 xts_suitetype）
cd /mnt/data/c00810129/oh_0130
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest

# 示例 2：编译静态测试套（需要添加 xts_suitetype=hap_static）
cd /mnt/data/c00810129/oh_0130
./test/xts/acts/build.sh product_name=rk3568 system_size=standard xts_suitetype=hap_static suite=ActsUiStaticTest
```

**如何区分动态和静态测试套**：

动态测试套使用 `ohos_js_app_suite`：
```gni
# testfwk/uitest_errorcode/BUILD.gn（动态测试套）
ohos_js_app_suite("ActsUiTestErrorCodeTest") {
  test_hap = true
  testonly = true
  ...
}
```

静态测试套使用 `ohos_js_app_static_suite`：
```gni
# xts/ActsCanIUseStatic/BUILD.gn（静态测试套）
ohos_js_app_static_suite("ActsCanIUseStaticTest") {
  ...
}
```

#### 3.2.2 参数说明

| 参数 | 说明 | 是否必选 | 可选值 | 说明 |
|------|------|---------|--------|------|
| `product_name` | 产品名称 | ✅ **必选** | rk3568 | **固定值，不可修改** |
| `system_size` | 系统规格 | ✅ **必选** | standard | **固定值，不可修改** |
| `suite` | 测试套名称 | ✅ 必选 | {测试套名称} | 从 BUILD.gn 中获取 |
| `xts_suitetype` | 测试套类型 | ❌ 可选 | hap_static | **默认不指定（动态测试套）** |

**重要说明**：
- `product_name=rk3568` 和 `system_size=standard` 是必选参数，值固定，不可修改
- `suite` 参数指定要编译的测试套名称（必选）
- **默认编译动态测试套**，无需指定 `xts_suitetype` 参数
- 只有编译静态测试套时才需要添加 `xts_suitetype=hap_static` 参数

#### 3.2.3 编译目标名称

编译目标名称由 `BUILD.gn` 中 `ohos_js_app_suite()` 的第一个参数决定：

```gni
# testfwk/uitest_errorcode/BUILD.gn
ohos_js_app_suite("ActsUiTestErrorCodeTest") {  # ← "ActsUiTestErrorCodeTest" 就是编译目标名称
  test_hap = true
  testonly = true
  ...
}
```

**编译命令中的 suite 参数值必须与 BUILD.gn 中的名称一致**：
```bash
suite=ActsUiTestErrorCodeTest  # ✅ 正确：与 BUILD.gn 中的名称一致
```

### 3.3 编译多个目标

#### 3.3.1 编译限制

**重要限制**：`build.sh` 命令的 `suite` 参数**不支持指定多个编译目标**。

```bash
# ❌ 错误：不支持一次编译多个 suite
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest,ActsArkUITest

# ❌ 错误：不支持多次指定 suite 参数
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest suite=ActsArkUITest
```

#### 3.3.2 替代方案：编译 group（按 BUILD.gn 中的目标）

**重要说明**：虽然 `suite` 参数不支持指定多个具体的测试套，但可以**按照 BUILD.gn 中的 group 目标**来编译多个相关测试套。每个子系统的 BUILD.gn 文件中定义了 `group()`，可以一次性编译该 group 下的所有依赖测试套。

**查找 group 名称的方法**：

1. 查看子系统的 BUILD.gn 文件
2. 找到 `group("子系统名")` 的定义
3. 使用该 group 名称作为 `suite` 参数值

##### 示例 1：编译测试框架（testfwk）的所有测试套

**编译命令**：
```bash
# 编译测试框架的所有测试套
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=testfwk
```

**配置依据**：
```bash
# BUILD.gn 文件位置
/test/xts/acts/testfwk/BUILD.gn

# 关键配置（第17行）
group("testfwk") {
  testonly = true
  if (ace_engine_feature_wearable) {
    deps = [
      "uitest:ActsUiTest",
      "uitestScene:ActsUiTestScene",
      "uitestStatic:ActsUiStaticTest",
    ]
  } else {
    deps = [
      "perftest:ActsPerfTestTest",
      "perftestStatic:ActsPerfTestTestStaticTest",
      "perftestScene:ActsPerfTestScene",
      "uitest:ActsUiTest",
      "uitestScene:ActsUiTestScene",
      "uitestStatic:ActsUiStaticTest",
      "uitest_errorcode:ActsUiTestErrorCodeTest",
      "uitest_errorcode_static:ActsUiTestErrorCodeStaticTest",
      "uitestQuarantine:ActsUiTestQuarantineTest",
      "uitest_quarantine_static:ActsUiTestQuarStaticTest",
    ]
  }
  if (arkxtest_product_feature == "pc") {
    deps += [
      "uitestScene:ActsUiTestScene",
      "uitest_pc:ActsUiPCTest",
      "uitest_pc_static:ActsUiPCStaticTest",
    ]
  }
}
```

**说明**：
- `suite=testfwk` 会编译 `group("testfwk")` 下所有 deps 依赖的测试套
- 标准系统会编译 8-10 个测试套（取决于产品特性）
- 适用于需要编译测试框架所有测试套的场景

##### 示例 2：编译 ArkUI 子系统的所有测试套

**编译命令**：
```bash
# 编译 ArkUI 子系统的所有测试套
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=arkui
```

**配置依据**：
```bash
# BUILD.gn 文件位置
/test/xts/acts/arkui/BUILD.gn

# 关键配置（第15行）
group("arkui") {
  testonly = true
  if (ace_engine_feature_wearable) {
    deps = [
      "ace_c_accessibility_api_16:ActsAceCapiInspector16Test",
      "ace_c_arkui_test:ActsAceCArkUITest",
      "ace_c_arkui_test_api13:ActsAceCArkUI13Test",
      # ... 更多测试套
    ]
  } else {
    deps = [
      "ace_c_accessibility_api_16:ActsAceCapiInspector16Test",
      "ace_c_arkui_test:ActsAceCArkUITest",
      "ace_c_arkui_test_api13:ActsAceCArkUI13Test",
      # ... 更多测试套（30+ 个测试套）
    ]
  }
}
```

**说明**：
- `suite=arkui` 会编译 `group("arkui")` 下所有 deps 依赖的测试套
- ArkUI 子系统包含 30+ 个测试套
- 适用于需要编译 ArkUI 所有测试套的场景

##### 通用规则总结

| 子系统 | group 名称 | 编译命令 | BUILD.gn 位置 | 编译的测试套数量 |
|--------|-----------|---------|--------------|----------------|
| **测试框架** | `testfwk` | `suite=testfwk` | `/test/xts/acts/testfwk/BUILD.gn` | 8-10 个 |
| **ArkUI** | `arkui` | `suite=arkui` | `/test/xts/acts/arkui/BUILD.gn` | 30+ 个 |
| **multimedia** | `multimedia` | `suite=multimedia` | `/test/xts/acts/multimedia/BUILD.gn` | 根据其定义 |
| **其他子系统** | 见对应 BUILD.gn | `suite={子系统名}` | `/test/xts/acts/{子系统}/BUILD.gn` | 根据其定义 |

**使用建议**：
1. **编译单个测试套**：使用 `suite=测试套名称`（如 `suite=ActsUiTest`）
2. **编译子系统所有测试套**：使用 `suite=子系统名`（如 `suite=arkui`）
3. **查找可用 group**：查看对应子系统的 BUILD.gn 文件，找到 `group()` 定义

### 3.4 编译输出位置

```
out/{product_name}/suites/acts/acts/testcases/
├── .....hap
├── ActsArkUITest.hap
└── ActsUiTest.hap
```

---

## 四、编译输出管理

### 4.1 编译产物验证

#### 4.1.1 检查编译状态

```bash
# 查看编译日志
tail -f out/rk3568/suites/acts/acts/build.log

# 检查编译错误
grep -i "error" out/rk3568/suites/acts/acts/build.log
```

#### 4.1.2 验证输出文件

```bash
# 检查 HAP 包是否存在
test -f out/rk3568/suites/acts/acts/testcases/ActsUiTest/ActsUiTest.hap && echo "✅ HAP 存在" || echo "❌ HAP 不存在"

# 查看 HAP 包大小
du -sh out/rk3568/suites/acts/acts/testcases/
```

### 4.2 编译错误处理（v1.16.0+）

#### 4.2.1 错误类型识别

**subagent 执行编译时，需识别以下错误类型**：

| 错误类型 | 处理策略 | 说明 |
|---------|---------|------|
| **语法错误** | **自动修复** | 分析错误日志，定位语法问题，修改代码后重试 |
| **配置错误** | **确认后修改** | 检测到证书等配置问题，暂停并向用户确认 |
| **依赖错误** | **手动排查** | 依赖缺失或路径错误，需手动检查和修复 |
| **环境错误** | **手动排查** | Node.js 版本、磁盘空间等环境问题，需手动修复 |

#### 4.2.2 语法错误自动修复流程

```
编译失败
    │
    ▼
分析错误日志
    │
    ├─ 定位错误位置（文件、行号）
    ├─ 识别错误类型（语法、类型、导入等）
    └─ 提取错误上下文
    │
    ▼
生成修复方案
    │
    ├─ 语法错误：修正语法
    ├─ 类型错误：添加类型注解
    ├─ 导入错误：添加缺失的导入
    └─ API 错误：修正 API 调用
    │
    ▼
应用修复
    │
    ├─ 修改源代码文件
    └─ 保存修改
    │
    ▼
重新编译
    │
    ├─ 执行编译命令
    └─ 监听编译状态
    │
    ▼
编译成功？
    │
    ├─ Yes → 输出成功结果
    └─ No → 重复上述流程（最多重试 3 次）
```

#### 4.2.3 配置错误确认流程

```
检测到配置错误
    │
    ▼
识别配置类型
    │
    ├─ BUILD.gn 目标识别问题
    ├─ 证书文件问题
    ├─ 环境变量问题
    └─ 工程路径问题
    │
    ▼
向用户确认
    │
    ├─ 说明配置问题
    ├─ 说明修改方案
    ├─ 说明影响范围
    └─ 询问是否同意修改
    │
    ▼
用户确认？
    │
    ├─ Yes → 应用修改并重新编译
    └─ No → 暂停编译，等待用户手动处理
```

#### 4.2.4 错误处理示例

**示例 1：语法错误自动修复**

```
错误日志：
ERROR in entry/src/ohosTest/ets/test/Component.onClick.test.ets:45:15
TS1005: ')' expected.

分析结果：
- 错误位置：Component.onClick.test.ets:45:15
- 错误类型：语法错误（缺少右括号）
- 错误代码：onClick(() => { console.log('test' }  // 缺少 )

修复方案：
在第 45 行末尾添加右括号

修复后代码：
onClick(() => { console.log('test') })  // 已修复

重新编译：
✅ 编译成功
```

**示例 2：配置错误确认**

```
错误日志：
ERROR: certificate not found: ./signature/test.p7b

分析结果：
- 错误类型：配置错误（证书文件缺失）
- 配置位置：BUILD.gn 中的 certificate_profile
- 影响范围：测试套编译

向用户确认：
❓ 检测到证书文件缺失
   - 缺失文件：./signature/test.p7b
   - 修改方案：复制默认证书文件
   - 影响范围：测试套编译
   - 是否同意修改？

用户确认：
✅ 同意修改

应用修改：
cp ./signature/default.p7b ./signature/test.p7b

重新编译：
✅ 编译成功
```

---

## 五、参考示例

### 5.1 完整编译示例

```bash
# 步骤1：准备编译环境（首次必需）
# 参考：linux_compile_env_setup.md

# 步骤2：确认 BUILD.gn 中的编译目标（首次必需）

# 步骤3：预编译清理（每次编译前必需）
# 参考：linux_prebuild_cleanup.md
# 使用统一的 ~/.opencode/skills/oh-xts-generator-template/scripts/cleanup_group.sh 脚本
~/.opencode/skills/oh-xts-generator-template/scripts/cleanup_group.sh {OH_ROOT} testfwk

# 步骤4：执行编译
cd /mnt/data/c00810129/oh_0130
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTestErrorCodeTest

# 步骤5：验证编译产物
test -f out/rk3568/suites/acts/acts/testcases/ActsUiTestErrorCodeTest/ActsUiTestErrorCodeTest.hap && echo "✅ 编译成功" || echo "❌ 编译失败"
```

### 5.2 参考路径

| 类型 | 路径 |
|------|------|
| 编译脚本 | `./test/xts/acts/build.sh` |
| 模板文件 | `./test/xts/tools/build/suite.gni` |
| 测试框架 | `./test/xts/acts/` |
| 编译输出 | `out/{product_name}/suites/acts/acts/testcases/` |

---