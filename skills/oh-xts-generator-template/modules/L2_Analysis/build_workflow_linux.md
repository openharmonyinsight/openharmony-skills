# Linux 编译工作流

> **模块信息**
> - 层级：L2_Analysis
> - 优先级：按需加载
> - 适用范围：Linux 环境下的 XTS 测试工程编译
> - 平台：Linux
> - 依赖：L1_Framework
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
> 2. `./test/xts/acts/build.sh` 会正确处理 BUILD.gn 配置、依赖关系和测试套结构
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

- **编译工作流** - 完整的编译流程指导
- **编译命令** - 单目标、多目标编译命令
- **编译验证** - 编译产物验证方法

### 1.2 应用场景

1. 准备 Linux 编译环境
2. 配置 BUILD.gn 文件
3. 执行预编译清理
4. 编译测试套
5. 验证编译产物
6. 排查编译问题

### 1.3 相关模块（按需加载）

| 任务类型 | 加载模块 |
|---------|---------|
| **环境准备** | [linux_compile_env_setup.md](./linux_compile_env_setup.md) |
| **BUILD.gn 配置** | [build_gn_config.md](./build_gn_config.md) |
| **预编译清理** | [linux_prebuild_cleanup.md](./linux_prebuild_cleanup.md) |
| **问题排查** | [linux_compile_troubleshooting.md](./linux_compile_troubleshooting.md) |

### 1.4 编译方式说明（重要）

**Linux 环境下的唯一正确编译方式**：

| 环境 | 编译工具 | 编译命令 | 说明 |
|------|---------|---------|------|
| **Linux** | `build.sh` | `./test/xts/acts/build.sh ...` | ✅ **必须使用** |
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

## 二、完整编译工作流

### 2.1 工作流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    Linux 编译工作流                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────┐
        │  步骤1：环境准备（首次必需）    │
        │  模块：linux_compile_env_setup │
        └───────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────┐
        │  步骤2：配置 BUILD.gn          │
        │  模块：build_gn_config         │
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
        │  步骤4：执行编译命令           │
        │  （本模块提供）                │
        └───────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────┐
        │  步骤5：验证编译产物           │
        │  （本模块提供）                │
        └───────────────────────────────┘
                            │
                            ▼
                   编译成功？
                    │      │
                   Yes     No
                    │      │
                    │      └──────────► 步骤6：问题排查
                    │                   模块：linux_compile_troubleshooting
                    │
                    ▼
              编译完成
```

### 2.2 快速参考

| 步骤 | 操作 | 命令/文档 |
|------|------|----------|
| 1. 环境准备 | 安装 Node.js、npm 等 | 参考 [linux_compile_env_setup.md](./linux_compile_env_setup.md) |
| 2. 配置 BUILD.gn | 创建/修改 BUILD.gn | 参考 [build_gn_config.md](./build_gn_config.md) |
| 3. 预编译清理 | 清理缓存 | 参考 [linux_prebuild_cleanup.md](./linux_prebuild_cleanup.md) |
| 4. 执行编译 | 运行 build.sh | `./test/xts/acts/build.sh ...` （见第三章） |
| 5. 验证产物 | 检查 HAP 包 | `test -f out/.../testcases/.../*.hap` |
| 6. 问题排查 | 解决编译错误 | 参考 [linux_compile_troubleshooting.md](./linux_compile_troubleshooting.md) |

---

## 三、编译命令说明

### 3.1 编译命令规范（重要）

> **⚠️ 编译命令执行要求**
>
> - ✅ **执行位置**：必须在 **OH_ROOT 目录**下执行编译命令
> - ✅ **必选参数**：`product_name=rk3568 system_size=standard` 为必选参数，不可修改或省略
> - ✅ **默认编译类型**：动态测试套（无需指定 `xts_suitetype` 参数）
> - ❌ **禁止操作**：不要在测试套目录下执行编译命令
> - ❌ **禁止操作**：不要修改 `product_name` 和 `system_size` 参数值

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
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsCanIUseStaticTest xts_suitetype=hap_static
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

#### 3.3.2 替代方案：编译 group（按 BUILD.gn 配置）

**重要说明**：虽然 `suite` 参数不支持指定多个具体的测试套，但可以**按照 BUILD.gn 中的 group 配置**来编译多个相关目标。每个子系统的 BUILD.gn 文件中定义了 `group()`，可以一次性编译该 group 下的所有依赖测试套。

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
| **multimedia** | `multimedia` | `suite=multimedia` | `/test/xts/acts/multimedia/BUILD.gn` | 根据配置 |
| **其他子系统** | 见对应 BUILD.gn | `suite={子系统名}` | `/test/xts/acts/{子系统}/BUILD.gn` | 根据配置 |

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

---

## 五、参考示例

### 5.1 完整编译示例

```bash
# 步骤1：准备编译环境（首次必需）
# 参考：linux_compile_env_setup.md

# 步骤2：配置 BUILD.gn（首次必需）
# 参考：build_gn_config.md

# 步骤3：预编译清理（每次编译前必需）
# 参考：linux_prebuild_cleanup.md
cd /mnt/data/c00810129/oh_0130/test/xts/acts/testfwk/uitest_errorcode
rm -rf .hvigor build entry/build oh_modules
rm -f oh-package-lock.json5 local.properties
cd /mnt/data/c00810129/oh_0130
rm -rf out

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

## 六、版本历史

- **v2.0.0** (2026-02-06): 大规模重构，模块化拆分
  - **拆分出 4 个独立模块**：
    - `linux_compile_env_setup.md` - 编译环境准备
    - `linux_prebuild_cleanup.md` - 预编译清理
    - `build_gn_config.md` - BUILD.gn 配置
    - `linux_compile_troubleshooting.md` - 编译问题排查
  - **简化主文件**：专注于核心编译工作流
  - **新增工作流程图**：可视化展示编译流程
  - **优化章节结构**：更清晰的组织方式
  - **文件大小**：从 716 行减少到约 350 行（减少 51%）
- **v1.2.0** (2026-02-06): 将编译环境准备内容拆分为独立模块 `linux_compile_env_setup.md`
  - 创建 `linux_compile_env_setup.md` 文件
  - 从原文档中删除第二章"编译环境准备"
  - 更新章节编号
  - 添加对新模块的引用和加载说明
- **v1.1.2** (2026-02-06): 明确编译命令规范和参数要求
  - 强调必须在 OH_ROOT 目录下执行编译命令
  - 明确 `product_name=rk3568 system_size=standard` 为必选参数
  - 说明默认编译动态测试套
  - 重新组织"编译命令说明"，增加参数详细说明表格
- **v1.1.1** (2026-02-06): 明确区分两种 build 目录的处理规则
- **v1.1.0** (2026-02-05): 添加第四章"预编译清理（强制执行）"
- **v1.0.0** (2025-01-31): 初始版本
