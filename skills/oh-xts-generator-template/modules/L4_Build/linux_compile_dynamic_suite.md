# Linux 动态测试套编译流程

> **模块信息**
> - 层级：L4_Build
> - 优先级：按需加载
> - 适用范围：Linux 环境下的动态 XTS 测试套编译
> - 平台：Linux
> - 依赖：L1_Framework, L2_Analysis, L3_Generation
> - 相关：`linux_compile_static_suite.md`（静态测试套编译）

## 一、模块概述

### 1.1 核心功能

- **动态测试套编译** - 完整的动态测试套编译流程指导
- **编译命令** - 单目标、多目标编译命令
- **编译验证** - 编译产物验证方法
- **subagent 执行** - 使用 general subagent 执行编译任务，避免主流程中断
- **监听机制** - 监听编译进程直至完成，确保编译状态正确返回
- **错误处理** - 自动修复语法错误，配置错误需确认后修改

### 1.2 应用场景

1. 编译动态 XTS 测试套（默认编译方式）
2. 配置 BUILD.gn 文件为动态测试套
3. 执行预编译清理
4. 编译测试套并验证

### 1.3 相关模块（按需加载）

| 任务类型 | 加载模块 |
|---------|---------|
| **环境准备** | [linux_compile_env_setup.md](./linux_compile_env_setup.md) |
| **BUILD.gn 配置** | [build_gn_config.md](./build_gn_config.md) |
| **预编译清理** | [linux_prebuild_cleanup.md](./linux_prebuild_cleanup.md) |
| **问题排查** | [linux_compile_troubleshooting.md](./linux_compile_troubleshooting.md) |
| **静态测试套编译** | [linux_compile_static_suite.md](./linux_compile_static_suite.md) |

---

## 二、完整编译工作流

### 2.1 工作流程图

```
┌─────────────────────────────────────────────────────────────┐
│              动态测试套编译流程                        │
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
         │  步骤4：subagent 执行编译      │
         │  （使用 general subagent）     │
         └───────────────────────────────┘
                             │
                             ▼
         ┌───────────────────────────────┐
         │  步骤5：监听编译进程           │
         │  （等待编译完成）              │
         └───────────────────────────────┘
                             │
                             ▼
         ┌───────────────────────────────┐
         │  步骤6：编译结果处理           │
         │  ┌─────────────────────┐     │
         │  │ 编译成功？          │     │
         │  │  ┌───┬──────┐       │     │
         │  │  │Yes│   No │       │     │
         │  │  │   │      │       │     │
         │  │  ▼   ▼      │       │     │
         │  │完成 错误处理│       │     │
         │  └─────┬──────┘       │     │
         └─────────┼──────────────┘     │
                   │                     │
                   ▼                     │
         ┌───────────────────────────────┐
         │  步骤7：错误处理（如有）      │
         │  ├─ 语法错误：自动修复       │
         │  ├─ 配置错误：确认后修改     │
         │  └─ 其他错误：手动排查       │
         └───────────────────────────────┘
                   │
                   ▼
         ┌───────────────────────────────┐
         │  步骤8：验证编译产物          │
         │  （本模块提供）               │
         └───────────────────────────────┘
                   │
                   ▼
         ┌───────────────────────────────┐
         │  步骤9：编译完成               │
         └───────────────────────────────┘
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

**⚠️ 重要提示**：步骤3"预编译清理"必须每次编译前执行，确保编译结果包含所有最新代码。

---

## 三、编译命令说明

### 3.1 命令格式

#### 3.1.1 基本编译命令

**命令格式**：
```bash
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称}
```

**参数说明**：
- `product_name=rk3568` - 产品名称（必选，固定值）
- `system_size=standard` - 系统规格（必选，固定值）
- `suite={测试套名称}` - 测试套名称（必选）

#### 3.1.2 参数说明

| 参数 | 说明 | 是否必选 | 可选值 | 说明 |
|------|------|---------|------|
| `product_name` | 产品名称 | ✅ **必选** | rk3568 | **固定值，不可修改** |
| `system_size` | 系统规格 | ✅ **必选** | standard | **固定值，不可修改** |
| `suite` | 测试套名称 | ✅ 必选 | {测试套名称} | 从 BUILD.gn 中获取 |
| `xts_suitetype` | 测试套类型 | ❌ 可选 | hap_dynamic, hap_static | 默认：hap_dynamic（动态测试套） |

**重要说明**：
- `product_name=rk3568` 和 `system_size=standard` 是必选参数，值固定，不可修改
- `suite` 参数指定要编译的测试套名称（必选）
- **默认编译动态测试套**，无需指定 `xts_suitetype` 参数
- 只有编译静态测试套时才需要添加 `xts_suitetype=hap_static` 参数

### 3.2 编译目标名称

编译目标名称由 `BUILD.gn` 中 `ohos_js_app_suite()` 或 `ohos_js_app_static_suite()` 的第一个参数决定：

```gni
# testfwk/uitest/BUILD.gn（动态测试套）
ohos_js_app_suite("ActsUiTest") {  # ← "ActsUiTest" 就是编译目标名称
  test_hap = true
  testonly = true
  ...
}
```

**编译命令中的 suite 参数值必须与 BUILD.gn 中的名称一致**：
```bash
suite=ActsUiTest  # ✅ 正确：与 BUILD.gn 中的名称一致
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

##### 示例 1：编译测试框架（testfwk）的所有动态测试套

**编译命令**：
```bash
# 编译测试框架的所有动态测试套
cd {OH_ROOT}
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
  ...
}
```

**说明**：
- `suite=testfwk` 会编译 `group("testfwk")` 下所有 deps 依赖的测试套
- 标准系统会编译 8-10 个测试套（取决于产品特性）
- 适用于需要编译测试框架所有测试套的场景

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

# 步骤3：预编译清理（每次编译前强制执行）
# 参考：linux_prebuild_cleanup.md
# ⚠️ 重要：确保清理所有缓存，以便编译结果包含所有最新代码
# 使用统一的 cleanup_group.sh 脚本
cd {OH_ROOT}
./test/xts/acts/cleanup_group.sh {OH_ROOT} testfwk

# 步骤4：执行编译
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest

# 步骤5：验证编译产物
test -f out/rk3568/suites/acts/acts/testcases/ActsUiTest/ActsUiTest.hap && echo "✅ 编译成功" || echo "❌ 编译失败"
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

- **v1.2.0** (2026-02-11): **强化预编译清理的强制执行**
  - **核心更新**：
     * 强化预编译清理步骤的强制性要求
     * 明确清理的目的是确保编译结果包含所有最新代码
  - **快速参考更新**：
     * 在快速参考表格后添加"⚠️ 重要提示"
     * 强调预编译清理必须每次编译前执行
  - **完整示例更新**：
     * 在预编译清理步骤添加"⚠️ 重要"提示
     * 说明清理的目的是确保编译结果包含所有最新代码
  - **优化效果**：
     * 确保动态测试套编译前都执行清理
     * 避免缓存导致编译结果不包含最新代码的问题
     * 提高编译结果的可靠性
  - 版本号升级至 v1.2.0

- **v1.1.0** (2026-02-11): **添加 subagent 执行和错误处理机制**
  - **核心更新**：
    * 新增 subagent 执行编译任务说明
    * 新增编译进程监听机制
    * 新增自动错误处理流程
  - **工作流程图更新**：
    * 添加 subagent 执行步骤
    * 添加监听编译进程步骤
    * 添加编译结果处理步骤
    * 添加自动错误处理步骤
  - **核心功能更新**：
    * 添加 subagent 执行功能
    * 添加监听机制功能
    * 添加错误处理功能
  - 版本号升级至 v1.1.0

- **v1.0.0** (2026-02-10): 从 build_workflow_linux.md 拆分出的动态测试套编译流程文档
  - 专注于动态测试套编译流程
  - 提供完整的编译命令和参数说明
  - 包含编译多个目标的方法
  - 提供编译产物验证方法
