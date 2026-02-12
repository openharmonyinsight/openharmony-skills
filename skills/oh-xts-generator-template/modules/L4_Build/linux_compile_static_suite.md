# Linux 静态测试套编译流程

> **模块信息**
> - 层级：L4_Build
> - 优先级：按需加载
> - 适用范围：Linux 环境下的静态 XTS 测试套编译
> - 平台：Linux
> - 依赖：L1_Framework, L2_Analysis, L3_Generation
> - 相关：`linux_compile_dynamic_suite.md`（动态测试套编译）

> **⚠️ 重要提示（静态测试套编译）**
>
> **在编译静态测试套时，需要特别注意以下四点：**
>
> 1. **版本校验** - 每次编译静态测试套前，必须校验 hvigor 工具版本（详见第二章）
> 2. **强制清理** - **每次编译前必须执行预编译清理**，确保包含所有最新代码（详见第三章）
> 3. **添加 hap_static 参数** - 编译时必须指定 `xts_suitetype=hap_static` 参数
> 4. **BUILD.gn 配置** - 使用 `ohos_js_app_static_suite()` 而非 `ohos_js_app_suite()`

## 一、模块概述

### 1.1 核心功能

- **静态测试套编译** - 完整的静态测试套编译流程指导
- **编译命令** - 单目标、多目标编译命令
- **编译验证** - 编译产物验证方法
- **静态 SDK 同步编译** - 说明静态 SDK 的编译机制
- **subagent 执行** - 使用 general subagent 执行编译任务，避免主流程中断
- **监听机制** - 监听编译进程直至完成，确保编译状态正确返回
- **错误处理** - 自动修复语法错误，配置错误需确认后修改

### 1.2 应用场景

1. 编译静态 XTS 测试套（需要 arkTS 静态语法）
2. 配置 BUILD.gn 文件为静态测试套
3. 每次编译前校验 hvigor 工具版本
4. 按需清理 SDK 缓存和替换 hvigor 编译工具
5. 编译测试套并验证

### 1.3 相关模块（按需加载）

| 任务类型 | 加载模块 |
|---------|---------|
| **环境准备** | [linux_compile_env_setup.md](./linux_compile_env_setup.md) |
| **BUILD.gn 配置** | [build_gn_config.md](./build_gn_config.md) |
| **预编译清理** | [linux_prebuild_cleanup.md](./linux_prebuild_cleanup.md) |
| **问题排查** | [linux_compile_troubleshooting.md](./linux_compile_troubleshooting.md) |
| **动态测试套编译** | [linux_compile_dynamic_suite.md](./linux_compile_dynamic_suite.md) |

---

## 二、完整编译工作流

### 2.1 工作流程图

```
┌─────────────────────────────────────────────────────────────┐
│              静态测试套编译流程                        │
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
           │  步骤2：hvigor 版本校验       │
           │  （每次编译静态套前必需）      │
           │  ┌─────────────────────┐      │
           │  │ 版本匹配？          │      │
           │  │  ┌───┬──────┐       │      │
           │  │  │Yes│   No │       │      │
           │  │  │   │      │       │      │
           │  │  ▼   ▼      │       │      │
           │  │跳过 替换     │       │      │
           │  └─────┬──────┘       │      │
           └────────┼──────────────┘      │
                    │                     │
                    ▼                     │
           ┌───────────────────────────────┐
           │  步骤2.5：替换 hvigor 工具    │
           │  （仅在需要时执行）           │
           │  ├─ 清理 SDK 缓存            │
           │  ├─ 清理旧工具                │
           │  ├─ 下载新工具                │
           │  └─ 移动到预置目录            │
           └───────────────────────────────┘
                               │
                               ▼
           ┌───────────────────────────────┐
           │  步骤3：配置 BUILD.gn          │
           │  模块：build_gn_config         │
           └───────────────────────────────┘
                              │
                               ▼
           ┌───────────────────────────────┐
           │  步骤4：预编译清理（每次必需）  │
           │  模块：linux_prebuild_cleanup  │
           │  ├─ 清理测试套缓存            │
           │  ├─ 清理 out 目录              │
           │  └─ 确保包含最新代码          │
           └───────────────────────────────┘
                               │
                               ▼
           ┌───────────────────────────────┐
           │  步骤5：subagent 执行编译      │
           │  （使用 general subagent）     │
           └───────────────────────────────┘
                               │
                               ▼
           ┌───────────────────────────────┐
           │  步骤6：监听编译进程           │
           │  （等待编译完成）              │
           └───────────────────────────────┘
                               │
                               ▼
           ┌───────────────────────────────┐
           │  步骤7：编译结果处理           │
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
           │  步骤8：错误处理（如有）      │
           │  ├─ 语法错误：自动修复       │
           │  ├─ 配置错误：确认后修改     │
           │  ├─ SDK 错误：清理并重编译   │
           │  └─ 其他错误：手动排查       │
           └───────────────────────────────┘
                     │
                     ▼
           ┌───────────────────────────────┐
           │  步骤9：验证编译产物          │
           │  （本模块提供）               │
           └───────────────────────────────┘
                     │
                     ▼
           ┌───────────────────────────────┐
           │  步骤10：编译完成             │
           └───────────────────────────────┘
```

### 2.2 快速参考

 | 步骤 | 操作 | 命令/文档 | 注意事项 |
|------|------|----------|---------|
| 1. 环境准备 | 安装 Node.js、npm 等 | 参考 [linux_compile_env_setup.md](./linux_compile_env_setup.md) | 首次必需 |
| 2. 版本校验 | 检查 hvigor 版本 | 见第四章详细说明 | **每次编译静态套前必需** |
| 2.5. 替换 hvigor | 清理、下载、移动工具 | 见第四章详细说明 | **仅在需要时执行** |
| 3. 配置 BUILD.gn | 创建/修改 BUILD.gn | 参考 [build_gn_config.md](./build_gn_config.md) | 使用 `ohos_js_app_static_suite()` |
| 4. 预编译清理 | 清理缓存 | 参考 [linux_prebuild_cleanup.md](./linux_prebuild_cleanup.md) | **每次编译前强制执行**，确保包含最新代码 |
| 5. 执行编译 | 运行 build.sh | `./test/xts/acts/build.sh ... xts_suitetype=hap_static` | **必须添加 hap_static 参数** |
| 6. 验证产物 | 检查 HAP 包 | `test -f out/.../testcases/.../*.hap` | 验证编译产物 |
| 7. 问题排查 | 解决编译错误 | 参考 [linux_compile_troubleshooting.md](./linux_compile_troubleshooting.md) | 查看编译日志 |

---

## 三、编译命令说明

### 3.1 命令格式

#### 3.1.1 基本编译命令

**命令格式**：
```bash
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称} xts_suitetype=hap_static
```

**参数说明**：
- `product_name=rk3568` - 产品名称（必选，固定值）
- `system_size=standard` - 系统规格（必选，固定值）
- `suite={测试套名称}` - 测试套名称（必选）
- `xts_suitetype=hap_static` - 测试套类型（**静态测试套必选**）

#### 3.1.2 参数说明

| 参数 | 说明 | 是否必选 | 可选值 | 说明 |
|------|------|---------|------|
| `product_name` | 产品名称 | ✅ **必选** | rk3568 | **固定值，不可修改** |
| `system_size` | 系统规格 | ✅ **必选** | standard | **固定值，不可修改** |
| `suite` | 测试套名称 | ✅ 必选 | {测试套名称} | 从 BUILD.gn 中获取 |
| `xts_suitetype` | 测试套类型 | ❌ 可选 | hap_dynamic, hap_static | **编译静态测试套时必须指定 hap_static** |

**重要说明**：
- `product_name=rk3568` 和 `system_size=standard` 是必选参数，值固定，不可修改
- `suite` 参数指定要编译的测试套名称（必选）
- **编译静态测试套时必须指定** `xts_suitetype=hap_static` 参数
- 不指定 `xts_suitetype` 时默认编译动态测试套

### 3.2 编译目标名称

编译目标名称由 `BUILD.gn` 中 `ohos_js_app_static_suite()` 的第一个参数决定：

```gni
# testfwk/uitestStatic/BUILD.gn（静态测试套）
ohos_js_app_static_suite("ActsUiStaticTest") {  # ← "ActsUiStaticTest" 就是编译目标名称
  #   test_hap = true
  testonly = true
  certificate_profile = "./signature/openharmony_sx.p7b"
  hap_name = "ActsUiStaticTest"
  part_name = "arkxtest"
  subsystem_name = "testfwk"
}
```

**关键区别**：
- 动态测试套：使用 `ohos_js_app_suite()` 并设置 `test_hap = true`
- 静态测试套：使用 `ohos_js_app_static_suite()`，**不设置** `test_hap = true`

**编译命令中的 suite 参数值必须与 BUILD.gn 中的名称一致**：
```bash
suite=ActsUiStaticTest  # ✅ 正确：与 BUILD.gn 中的名称一致
```

### 3.3 编译多个目标

#### 3.3.1 编译限制

**重要限制**：`build.sh` 命令的 `suite` 参数**不支持指定多个编译目标**。

```bash
# ❌ 错误：不支持一次编译多个 suite
./test/xts/acts/build.sh product_name=rk3568 system_size=standard xts_suitetype=hap_static suite=ActsUiStaticTest,ActsArkUIStaticTest

# ❌ 错误：不支持多次指定 suite 参数
./test/xts/acts/build.sh product_name=rk3568 system_size=standard xts_suitetype=hap_static suite=ActsUiStaticTest suite=ActsArkUIStaticTest
```

#### 3.3.2 替代方案：编译 group（按 BUILD.gn 配置）

**重要说明**：虽然 `suite` 参数不支持指定多个具体的测试套，但可以**按照 BUILD.gn 中的 group 配置**来编译多个相关目标。每个子系统的 BUILD.gn 文件中定义了 `group()`，可以一次性编译该 group 下的所有依赖测试套。

**查找 group 名称的方法**：

1. 查看子系统的 BUILD.gn 文件
2. 找到 `group("子系统名")` 的定义
3. 使用该 group 名称作为 `suite` 参数值

##### 示例：编译测试框架（testfwk）的所有静态测试套

**编译命令**：
```bash
# 编译测试框架的所有静态测试套
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard xts_suitetype=hap_static suite=testfwk
```

**配置依据**：
```bash
# BUILD.gn 文件位置
/test/xts/acts/testfwk/BUILD.gn

# 关键配置（第17行）
group("testfwk") {
  testonly = true
  deps = [
    "uitest:ActsUiTest",
    "uitestScene:ActsUiTestScene",
    "uitestStatic:ActsUiStaticTest",
    "uitest_errorcode:ActsUiTestErrorCodeTest",
    "uitest_errorcode_static:ActsUiTestErrorCodeStaticTest",
    "uitestQuarantine:ActsUiTestQuarantineTest",
    "uitest_quarantine_static:ActsUiTestQuarStaticTest",
  ]
  ...
}
```

**说明**：
- `suite=testfwk` 会编译 `group("testfwk")` 下所有 deps 依赖的测试套
- 编译静态测试套时会自动识别哪些是静态测试套
- 适用于需要编译测试框架所有测试套的场景

### 3.4 编译输出位置

```
out/{product_name}/suites/acts/acts/testcases/
├── .....hap
├── ActsUiStaticTest.hap
└── ActsArkUIStaticTest.hap
```

---

## 四、hvigor 工具版本校验和替换流程（静态测试套编译必需）

### 4.1 版本校验逻辑（每次编译静态套前）

**为什么需要版本校验**：
- 避免重复下载和替换已经存在的静态编译工具
- 提高编译流程效率
- 减少不必要的网络请求和磁盘操作

**静态工具版本标识**：
- 版本号：`"6.0.0-arkts1.2-ohosTest-25072102"`
- 位置：`prebuilts/command-line-tools/hvigor/hvigor/package.json`

#### 4.1.1 版本校验步骤

```bash
# 步骤1：检查工具是否存在
if [ -f ./prebuilts/command-line-tools/hvigor/hvigor/package.json ]; then
    # 步骤2：读取工具版本
    TOOL_VERSION=$(cat ./prebuilts/command-line-tools/hvigor/hvigor/package.json | grep '"version"' | cut -d'"' -f4)
    echo "当前 hvigor 版本: $TOOL_VERSION"

    # 步骤3：判断版本是否匹配
    if [ "$TOOL_VERSION" = "6.0.0-arkts1.2-ohosTest-25072102" ]; then
        echo "✅ 版本匹配，无需替换"
        NEED_REPLACE=false
    else
        echo "⚠️  版本不匹配，需要替换"
        NEED_REPLACE=true
    fi
else
    echo "❌ 工具不存在，需要下载"
    NEED_REPLACE=true
fi

# 步骤4：根据判断结果执行操作
if [ "$NEED_REPLACE" = true ]; then
    # 执行替换流程（见4.2节）
    echo "开始替换 hvigor 工具..."
else
    echo "跳过替换，直接编译"
fi
```

#### 4.1.2 快速校验命令

```bash
# 一键校验版本
cd {OH_ROOT}
VERSION=$(cat ./prebuilts/command-line-tools/hvigor/hvigor/package.json 2>/dev/null | grep '"version"' | cut -d'"' -f4)
if [ "$VERSION" = "6.0.0-arkts1.2-ohosTest-25072102" ]; then
    echo "✅ 静态工具已安装，无需替换"
else
    echo "⚠️  需要替换静态工具"
fi
```

#### 4.1.3 决策流程图

```
开始编译静态测试套
        │
        ▼
   检查工具是否存在？
        │
   ┌────┴────┐
   │         │
  No        Yes
   │         │
   ▼         ▼
需要下载   读取版本号
   │         │
   ▼         ▼
执行替换   版本匹配？
           │
      ┌────┴────┐
      │         │
    Yes        No
      │         │
      ▼         ▼
   跳过替换  执行替换
      │         │
      └────┬────┘
           │
           ▼
      开始编译
```

### 4.2 hvigor 工具替换流程（仅在需要时执行）

#### 4.2.1 为什么要替换 hvigor 工具

**背景说明**：
- `prebuilts` 目录中默认配置的是编译动态测试套的编译工具
- 静态测试套需要使用专用的静态编译工具
- 当版本校验不匹配时，需要替换为静态编译专用的 hvigor 工具

**工具来源**：
- 仓库地址：`https://gitee.com/laoji-fuli/hvigor0702.git`
- 分支：`debug2`
- 工具名称：`command-line-tools`

#### 4.2.2 替换步骤

**执行位置**：必须在 `{OH_ROOT}` 目录下执行以下命令

#### 4.2.1 步骤1：清理旧工具

```bash
# 清理旧的 command-line-tools
cd {OH_ROOT}
rm -rf ./prebuilts/command-line-tools
echo "✅ 旧工具清理完成"
```

#### 4.2.2 步骤2：下载新工具

```bash
# 下载静态编译专用的 hvigor 工具
git clone https://gitee.com/laoji-fuli/hvigor0702.git -b debug2 command-line-tools
echo "✅ 新工具下载完成"
```

**下载说明**：
- 使用 `-b debug2` 参数指定分支
- 将工具下载到临时目录 `command-line-tools`

#### 4.2.3 步骤3：移动到预置目录

```bash
# 移动到 prebuilts 目录
mv -f command-line-tools ./prebuilts/
echo "✅ 工具移动完成"
```

### 4.3 完整准备流程（带版本校验）

```bash
# 静态测试套编译前的完整准备流程
cd {OH_ROOT}

# 步骤1：版本校验（每次编译静态套前）
if [ -f ./prebuilts/command-line-tools/hvigor/hvigor/package.json ]; then
    TOOL_VERSION=$(cat ./prebuilts/command-line-tools/hvigor/hvigor/package.json | grep '"version"' | cut -d'"' -f4)
    echo "当前 hvigor 版本: $TOOL_VERSION"
    if [ "$TOOL_VERSION" = "6.0.0-arkts1.2-ohosTest-25072102" ]; then
        echo "✅ 版本匹配，无需替换"
        NEED_REPLACE=false
    else
        echo "⚠️  版本不匹配，需要替换"
        NEED_REPLACE=true
    fi
else
    echo "❌ 工具不存在，需要下载"
    NEED_REPLACE=true
fi

# 步骤2：根据校验结果执行操作
if [ "$NEED_REPLACE" = true ]; then
    echo "开始替换 hvigor 工具..."
    # 步骤2.1：清理 SDK 缓存
    rm -rf prebuilts/ohos-sdk/linux
    echo "✅ SDK 缓存清理完成"
    
    # 步骤2.2：清理旧工具
    rm -rf ./prebuilts/command-line-tools
    
    # 步骤2.3：下载新工具
    git clone https://gitee.com/laoji-fuli/hvigor0702.git -b debug2 command-line-tools
    
    # 步骤2.4：移动到预置目录
    mv -f command-line-tools ./prebuilts/
    echo "✅ hvigor 工具替换完成"
else
    echo "跳过替换，直接编译"
fi

# 步骤3：配置 BUILD.gn（首次必需）
# 参考：build_gn_config.md

# 步骤4：预编译清理（每次编译前必需）
# 参考：linux_prebuild_cleanup.md

# 步骤5：执行编译
./test/xts/acts/build.sh product_name=rk3568 system_size=standard xts_suitetype=hap_static suite={测试套名称}
```

### 4.4 验证工具版本

```bash
# 检查工具版本
VERSION=$(cat {OH_ROOT}/prebuilts/command-line-tools/hvigor/hvigor/package.json | grep '"version"' | cut -d'"' -f4)
echo "当前 hvigor 版本: $VERSION"

# 验证是否为静态工具版本
if [ "$VERSION" = "6.0.0-arkts1.2-ohosTest-25072102" ]; then
    echo "✅ 静态工具版本正确"
else
    echo "❌ 版本不正确，需要替换"
fi

# 检查工具目录
ls -la {OH_ROOT}/prebuilts/command-line-tools/
```

### 4.5 注意事项

- **版本校验优先**：每次编译静态测试套前，优先执行版本校验
- **按需替换**：仅在版本不匹配或工具不存在时才执行替换
- **首次编译必需**：首次编译静态测试套前，如果工具不存在必须执行替换
- **后续编译**：如果版本匹配，后续编译无需重复替换
- **执行位置**：必须在 `{OH_ROOT}` 目录下执行命令
- **网络要求**：需要替换时，能够访问 `gitee.com` 仓库
- **权限要求**：需要有删除和写入 `prebuilts` 目录的权限
- **性能优化**：版本校验可避免不必要的下载和替换，提高编译效率

### 4.6 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|--------|
| 下载失败 | 网络问题或仓库地址错误 | 检查网络连接和仓库地址是否正确 |
| 权限不足 | 没有写入 `prebuilts` 目录的权限 | 使用 `sudo` 或修改目录权限 |
| 工具目录不存在 | 步骤执行顺序错误 | 确保按步骤1、2、3的顺序执行 |

---

## 五、重要注意事项

### 5.1 首次编译静态测试套的必需步骤

#### 5.1.1 清理 prebuilts 目录

**为什么需要清理**：
- 编译静态测试套时会同步编译静态 SDK
- 如果 prebuilts 目录存在旧的 SDK，可能导致编译错误或不一致
- 确保使用最新的静态 SDK 进行编译

**清理命令**：
```bash
cd {OH_ROOT}
rm -rf prebuilts/ohos-sdk/linux
echo "✅ 清理完成"
```

**验证清理**：
```bash
ls -la {OH_ROOT}/prebuilts/ohos-sdk/ | grep -E "^d.*linux"
# 如果没有输出，说明清理成功
```

#### 5.1.2 添加 hap_static 参数

**为什么需要指定**：
- 默认编译类型为动态测试套（hap_dynamic）
- 静态测试套使用不同的编译模板和工具链
- 不指定参数会导致编译失败或生成错误的 HAP 包

**正确示例**：
```bash
# ✅ 正确：编译静态测试套
./test/xts/acts/build.sh product_name=rk3568 system_size=standard xts_suitetype=hap_static suite=ActsUiStaticTest

# ❌ 错误：缺少 hap_static 参数
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiStaticTest
```

### 5.2 静态 SDK 同步编译

**编译机制说明**：

编译静态测试套时，构建系统会：
1. 检测到 `xts_suitetype=hap_static` 参数
2. 设置 `sdk_build_arkts=true` 标志
3. 首先编译静态 SDK 到 `prebuilts/ohos-sdk/linux`
4. 使用编译出的静态 SDK 编译测试套
5. 生成静态 HAP 包

**编译日志示例**：
```
[OHOS INFO]  Building static ohos-sdk...
[OHOS INFO]  Executing SDK build: ... sdk_build_arkts=true ...
[OHOS INFO]  SDK build completed successfully
[OHOS INFO]  Building test suite with static SDK...
```

**SDK 编译时间**：
- 首次编译：约 10-20 分钟（取决于系统性能）
- 后续编译：约 5-10 分钟（使用缓存）
- 总编译时间：SDK 编译 + 测试套编译

---

## 六、编译输出管理

### 5.1 编译产物验证

#### 5.1.1 检查编译状态

```bash
# 查看编译日志
tail -f out/rk3568/suites/acts/acts/build.log

# 检查编译错误
grep -i "error" out/rk3568/suites/acts/acts/build.log

# 检查 SDK 编译状态
grep -i "sdk" out/rk3568/suites/acts/acts/build.log | tail -20
```

#### 5.1.2 验证输出文件

```bash
# 检查 HAP 包是否存在
test -f out/rk3568/suites/acts/acts/testcases/ActsUiStaticTest/ActsUiStaticTest.hap && echo "✅ HAP 存在" || echo "❌ HAP 不存在"

# 查看 HAP 包大小
du -sh out/rk3568/suites/acts/acts/testcases/

# 验证静态 SDK 是否编译成功
test -d prebuilts/ohos-sdk/linux && echo "✅ SDK 存在" || echo "❌ SDK 不存在"
```

### 5.2 验证静态 HAP 包

**检查 HAP 包类型**：
```bash
# 解压 HAP 包检查内部结构
unzip -l out/rk3568/suites/acts/acts/testcases/ActsUiStaticTest/ActsUiStaticTest.hap

# 静态 HAP 包特征：
# - 使用静态编译的 SDK
# - 包含静态链接的库
# - 文件结构可能不同
```

---

## 七、参考示例

### 7.1 完整编译示例

```bash
# 步骤1：准备编译环境（首次必需）
# 参考：linux_compile_env_setup.md

# 步骤2：版本校验（每次编译静态套前必需）
cd {OH_ROOT}
if [ -f ./prebuilts/command-line-tools/hvigor/hvigor/package.json ]; then
    TOOL_VERSION=$(cat ./prebuilts/command-line-tools/hvigor/hvigor/package.json | grep '"version"' | cut -d'"' -f4)
    echo "当前 hvigor 版本: $TOOL_VERSION"
    if [ "$TOOL_VERSION" = "6.0.0-arkts1.2-ohosTest-25072102" ]; then
        echo "✅ 版本匹配，无需替换"
        NEED_REPLACE=false
    else
        echo "⚠️  版本不匹配，需要替换"
        NEED_REPLACE=true
    fi
else
    echo "❌ 工具不存在，需要下载"
    NEED_REPLACE=true
fi

# 步骤2.5：根据校验结果执行操作（仅在需要时）
if [ "$NEED_REPLACE" = true ]; then
    echo "开始替换 hvigor 工具..."
    # 清理 SDK 缓存
    rm -rf prebuilts/ohos-sdk/linux
    echo "✅ SDK 缓存清理完成"

    # 清理旧工具
    rm -rf ./prebuilts/command-line-tools

    # 下载新工具
    git clone https://gitee.com/laoji-fuli/hvigor0702.git -b debug2 command-line-tools

    # 移动到预置目录
    mv -f command-line-tools ./prebuilts/
    echo "✅ hvigor 工具替换完成"
else
    echo "跳过替换，直接编译"
fi

# 步骤3：配置 BUILD.gn（首次必需）
# 参考：build_gn_config.md
# 确保使用 ohos_js_app_static_suite() 而非 ohos_js_app_suite()

# 步骤4：预编译清理（每次编译前强制执行）
# 参考：linux_prebuild_cleanup.md
# ⚠️ 重要：确保清理所有缓存，以便编译结果包含所有最新代码
cd {OH_ROOT}
./test/xts/acts/cleanup_group.sh {OH_ROOT} testfwk

# 步骤5：执行编译（必须添加 hap_static 参数）
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard xts_suitetype=hap_static suite=ActsUiStaticTest

# 步骤6：验证编译产物
test -f out/rk3568/suites/acts/acts/testcases/ActsUiStaticTest/ActsUiStaticTest.hap && echo "✅ 编译成功" || echo "❌ 编译失败"

# 步骤7：验证静态 SDK
test -d prebuilts/ohos-sdk/linux && echo "✅ SDK 编译成功" || echo "❌ SDK 编译失败"
```

### 7.2 参考路径

| 类型 | 路径 |
|------|------|
| 编译脚本 | `./test/xts/acts/build.sh` |
| 模板文件 | `./test/xts/tools/build/suite.gni` |
| 测试框架 | `./test/xts/acts/` |
| 静态 SDK 输出 | `prebuilts/ohos-sdk/linux` |
| hvigor 工具 | `prebuilts/command-line-tools/` |
| 编译输出 | `out/{product_name}/suites/acts/acts/testcases/` |

### 7.3 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|--------|
| 编译失败：找不到 SDK | 首次编译未清理 prebuilts | 清理 `prebuilts/ohos-sdk/linux` 后重新编译 |
| 编译失败：hap_static 参数无效 | BUILD.gn 配置错误 | 检查是否使用 `ohos_js_app_static_suite()` |
| 编译失败：编译工具错误 | 未替换 hvigor 工具 | 执行版本校验，如版本不匹配则替换 |
| 编译失败：版本校验失败 | 无法读取 package.json | 检查工具目录是否存在，如不存在则下载 |
| 编译超时 | SDK 编译时间过长 | 检查系统资源，或使用缓存加速 |
| HAP 包不正确 | 使用了动态编译方式 | 检查命令是否包含 `xts_suitetype=hap_static` |

---

## 八、版本历史

- **v1.4.0** (2026-02-11): **强化预编译清理的强制执行**
   - **核心更新**：
     * 更新重要提示：将"按需替换"改为"强制清理"
     * 明确预编译清理步骤必须每次编译前执行
     * 强调清理的目的是确保编译结果包含所有最新代码
   - **工作流程更新**：
     * 更新工作流程图，步骤4明确标注"清理测试套缓存"、"清理 out 目录"、"确保包含最新代码"
     * 更新快速参考表格，将"每次编译前必需"改为"每次编译前强制执行"，并添加说明
     * 更新完整编译示例，在预编译清理步骤添加"⚠️ 重要"提示
   - **章节调整**：
     * 不改动其他章节的序号
   - **优化效果**：
     * 确保无论是动态还是静态测试套，编译前都执行清理
     * 避免缓存导致编译结果不包含最新代码的问题
     * 提高编译结果的可靠性
   - 版本号升级至 v1.4.0

- **v1.3.0** (2026-02-11): **添加 hvigor 工具版本校验机制**
   - **核心更新**：
     * 更新第四章标题："hvigor 工具版本校验和替换流程"
     * 新增 4.1 节：版本校验逻辑
     * 新增版本校验步骤和决策流程
     * 更新 4.2 节：仅在需要时执行替换
     * 更新 4.3 节：完整的准备流程（带版本校验）
     * 更新 4.4 节：验证工具版本
     * 更新 4.5 节：注意事项（强调按需替换）
   - **工作流程更新**：
     * 更新工作流程图，新增步骤2版本校验
     * 步骤2.5改为"仅在需要时执行"
     * 更新快速参考表格，添加版本校验步骤
   - **优化效果**：
     * 避免不必要的工具替换操作
     * 提高编译流程效率
     * 减少网络请求和磁盘操作
   - 版本号升级至 v1.3.0

- **v1.2.0** (2026-02-11): **添加 hvigor 工具替换流程**
  - **核心更新**：
    * 新增第四章"hvigor 工具替换流程"
    * 说明为何需要替换 hvigor 工具
    * 提供完整的替换步骤（清理、下载、移动）
    * 提供完整的命令序列
    * 添加验证工具替换的方法
    * 添加注意事项和常见问题
  - **工作流程更新**：
    * 更新工作流程图，新增步骤2.5
    * 更新重要提示（三点改为四点）
    * 更新应用场景说明
    * 更新快速参考表格
    * 更新完整编译示例，添加步骤2.5
    * 更新参考路径，添加 hvigor 工具路径
    * 更新常见问题排查，添加编译工具错误
  - **章节调整**：
    * 原第五章改为第六章（编译输出管理）
    * 原第六章改为第七章（参考示例）
    * 原第七章改为第八章（版本历史）
  - 版本号升级至 v1.2.0

- **v1.1.0** (2026-02-11): **添加 subagent 执行和错误处理机制**
  - **核心更新**：
    * 新增 subagent 执行编译任务说明
    * 新增编译进程监听机制
    * 新增自动错误处理流程
    * 新增 SDK 错误处理说明
  - **工作流程图更新**：
    * 添加 subagent 执行步骤
    * 添加监听编译进程步骤
    * 添加编译结果处理步骤
    * 添加自动错误处理步骤（包含 SDK 错误处理）
  - **核心功能更新**：
    * 添加 subagent 执行功能
    * 添加监听机制功能
    * 添加错误处理功能
  - 版本号升级至 v1.1.0

- **v1.0.0** (2026-02-10): 从 build_workflow_linux.md 拆分出的静态测试套编译流程文档
  - 专注于静态测试套编译流程
  - 强调首次编译前清理 SDK 缓存
  - 明确 hap_static 参数的必要性
  - 说明静态 SDK 的编译机制
  - 提供完整的编译示例和注意事项
