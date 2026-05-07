# Windows 编译与测试工作流

> **模块信息**
> - 层级：L3_Validation
> - 优先级：按需加载
> - 适用范围：Windows 环境下的 HarmonyOS XTS 测试工程编译、安装和测试
> - 平台：Windows
> - 依赖：conventions
> - 相关：`build_workflow_linux.md`（Linux 编译方案）
> - 版本：v2.2.0
> - 更新日期：2026-02-10

---

## 一、模块概述

Windows 编译与测试工作流模块提供在 Windows 环境下 OpenHarmony XTS 测试工程的完整编译、安装和测试指导，包括环境准备、DevEco Studio IDE 编译、HAP 包安装、测试执行、结果解析和问题排查。

### 1.1 编译模式说明

本工作流支持两种 ArkTS XTS 编译模式：

#### 1.1.1 ArkTS 动态 XTS 编译模式（默认）

- **适用场景**：标准的 ArkTS 动态语法 XTS 测试工程
- **工程特征**：`build-profile.json5` 中无 `arkTSVersion` 配置或 `arkTSVersion` 未设置为静态版本
- **编译方式**：使用 DevEco Studio IDE 或 `hvigorw.bat` 命令行工具
- **编译目标**：`Build → Build OhosTest Hap(s)`
- **详细流程**：见第三章

#### 1.1.2 ArkTS 静态 XTS 编译模式（arkts-sta）

- **适用场景**：基于 ArkTS 静态强类型语法的 XTS 测试工程
- **工程特征**：`build-profile.json5` 中配置 `arkTSVersion: "1.2"` 或更高版本
- **触发关键词**：当用户提到"arkts-sta"、"arkts静态"、"ArkTS静态"、"静态xts"等关键词时启用
- **编译方式**：使用 PowerShell 脚本或 `hvigorw.bat` 命令行工具
- **编译特点**：
  - 严格的静态类型检查
  - 需要配置 Java 环境
  - 编译参数包含静态模式标识
- **详细流程**：见第四章

> **⚠️ 重要提示**：在使用本工作流前，请确认你的 XTS 工程是动态还是静态模式。
> - 动态模式：参考第三章流程
> - 静态模式：参考第四章流程（需明确指定"arkts-sta"或"arkts静态"）

### 1.2 核心功能

- **环境准备** - Windows 开发环境配置和工具链设置
- **HAP 编译** - 使用 DevEco Studio IDE 或命令行编译测试 HAP 包
- **HAP 安装** - 使用 hdc 工具安装 HAP 到 RK 板
- **测试执行** - 使用 hdc shell aa test 命令执行测试
- **结果解析** - 解析 Hypium 测试框架输出并统计结果
- **多套测试** - 执行工程下所有测试套并汇总结果
- **问题排查** - Windows 编译和测试常见错误和解决方案
- **静态类型检查** - ArkTS 静态语法规范校验（静态模式专用）

### 1.2 工作流概览

```
┌─────────────────┐
│ 1. DevEco 编译  │ ← 使用 DevEco Studio IDE 编译 HAP
└────────┬────────┘
         ↓
┌─────────────────┐
│ 2. HAP 自动安装 │ ← hdc shell aa test 自动安装
└────────┬────────┘
         ↓
┌─────────────────┐
│ 3. 执行测试     │ ← 运行测试用例
└────────┬────────┘
         ↓
┌─────────────────┐
│ 4. 结果统计     │ ← 解析并汇总测试结果
└─────────────────┘
```

### 1.3 工作流概览

#### 1.3.1 ArkTS 动态 XTS 编译工作流

```
┌─────────────────┐
│ 1. DevEco 编译  │ ← 使用 DevEco Studio IDE 编译 HAP
└────────┬────────┘
         ↓
┌─────────────────┐
│ 2. HAP 自动安装 │ ← hdc shell aa test 自动安装
└────────┬────────┘
         ↓
┌─────────────────┐
│ 3. 执行测试     │ ← 运行测试用例
└────────┬────────┘
         ↓
┌─────────────────┐
│ 4. 结果统计     │ ← 解析并汇总测试结果
└─────────────────┘
```

#### 1.3.2 ArkTS 静态 XTS 编译工作流（arkts-sta）

```
┌─────────────────────┐
│ 1. 检测工程类型     │ ← 识别 arkTSVersion 配置
└────────┬────────────┘
         ↓
┌─────────────────────┐
│ 2. 配置 Java 环境   │ ← 设置 JAVA_HOME 环境变量
└────────┬────────────┘
         ↓
┌─────────────────────┐
│ 3. 执行静态编译     │ ← 使用 hvigorw.bat + 静态参数
└────────┬────────────┘
         ↓
┌─────────────────────┐
│ 4. 静态类型检查     │ ← 验证 ArkTS 静态规范
└────────┬────────────┘
         ↓
┌─────────────────────┐
│ 5. HAP 安装         │ ← hdc 工具安装
└────────┬────────────┘
         ↓
┌─────────────────────┐
│ 6. 执行测试         │ ← hdc shell aa test
└────────┬────────────┘
         ↓
┌─────────────────────┐
│ 7. 结果统计         │ ← 解析并汇总测试结果
└─────────────────────┘
```

### 1.4 与 Linux 方案的差异

| 特性 | Linux 方案 | Windows 动态方案 | Windows 静态方案 |
|------|-----------|----------------|----------------|
| **编译环境** | Linux Shell + 命令行 | DevEco Studio IDE（推荐） | PowerShell + hvigorw.bat |
| **编译方式** | `./test/xts/acts/build.sh` | DevEco Studio → Build Haps(s) | hvigorw.bat + 静态参数 |
| **Test HAP 编译** | Build → Build OhosTest Hap(s) | Build → Build OhosTest Hap(s) | hvigorw assembleHap (静态模式) |
| **HAP 输出** | out/{product}/suites/acts/testcases/ | entry/build/default/outputs/ohosTest/ | entry/build/default/outputs/ohosTest/ |
| **设备工具** | hdc (Linux 版) | hdc.exe (Windows 版) | hdc.exe (Windows 版) |
| **测试执行** | hdc shell aa test | hdc shell aa test | hdc shell aa test |
| **路径分隔符** | `/` | `\` | `\` |
| **Java 环境** | 可选 | 可选 | **必需** |
| **类型检查** | 标准检查 | 标准检查 | **严格静态类型检查** |

### 1.5 编译模式选择指南

| 判断条件 | 推荐模式 | 参考章节 |
|---------|---------|---------|
| 用户提到"arkts-sta"、"arkts静态"、"静态xts" | **ArkTS 静态模式** | 第四章 |
| build-profile.json5 中有 `arkTSVersion: "1.2"` | **ArkTS 静态模式** | 第四章 |
| 标准动态 XTS 工程 | **ArkTS 动态模式** | 第三章 |
| 不确定工程类型 | **ArkTS 动态模式**（默认） | 第三章 |

---

## 二、Windows 环境准备

### 2.1 环境要求

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Operating System | Windows 10/11 | 推荐 Windows 11 |
| DevEco Studio | 4.0+ | 必须安装，用于编译 HAP |
| Node.js | 14.x+ | 随 DevEco Studio 安装 |
| PowerShell | 5.1+ | 推荐 PowerShell 7+ |
| hdc 工具 | 随 DevEco 安装 | 用于设备连接和测试 |
| RK 开发板 | HarmonyOS 系统 | 测试目标设备 |

### 2.2 DevEco Studio 安装与配置

#### 2.2.1 下载与安装 DevEco Studio

1. 访问 [DevEco Studio 下载页面](https://developer.harmonyos.com/cn/develop/deveco-studio)
2. 下载 Windows 版本（推荐 4.0+）
3. 运行安装程序并按提示完成安装
4. 安装完成后首次启动 DevEco Studio

#### 2.2.2 配置签名信息

DevEco Studio 需要配置签名信息才能编译 HAP：

1. 打开 DevEco Studio
2. File → Project Structure → Signing Configs
3. 确认签名配置：
   - **Certpath**: `C:\Users\{用户名}\.ohos\config\default_*.cer`
   - **Profile**: `C:\Users\{用户名}\.ohos\config\default_*.p7b`
   - **StoreFile**: `C:\Users\{用户名}\.ohos\config\default_*.p12`

#### 2.2.3 验证工具安装

打开 PowerShell 或命令提示符：

```powershell
# 检查 hdc 工具（用于设备连接和测试）
hdc --version

# 检查 Node.js
node --version

# 预期输出示例：
# HDC 1.1.0a
# v16.18.0
```

### 2.3 设备连接准备

#### 2.3.1 RK 板连接

1. **USB 网络配置**（推荐）：
   - 使用 USB 网络将 RK 板连接到开发机
   - 确保 RK 板 IP 地址可访问（如 `192.168.1.100`）

2. **检查设备连接**：

```powershell
# 检查 hdc 设备列表
hdc list targets

# 预期输出示例：
# 192.168.1.100:5555
```

3. **如果设备未显示**：

```powershell
# 重启 hdc 服务
hdc kill
hdc start

# 添加设备（USB 网络）
hdc tconn 192.168.1.100:5555

# 再次检查
hdc list targets
```

### 2.4 SDK 路径配置

Windows 编译依赖 DevEco Studio 的 SDK 路径配置。`local.properties` 中必须正确指向 SDK 目录。

#### 2.4.1 SDK 目录结构

DevEco Studio SDK 默认路径：
```
C:\Users\{用户名}\AppData\Local\OpenHarmony\Sdk\
├── {API_VERSION}/          # 如 26.0.0
│   ├── ets/                # ArkTS 编译器
│   ├── js/                 # JS 运行时
│   ├── native/             # Native 工具链
│   ├── previewer/          # 预览器
│   └── toolchains/         # 构建工具（restool 等）
```

#### 2.4.2 local.properties 配置

IDE 同步后会自动生成 `local.properties`：
```properties
sdk.dir=C:/Users/{用户名}/AppData/Local/OpenHarmony/Sdk
```

> **⚠️ 重要**：`sdk.dir` 应指向 `Sdk` 父目录（不含版本号），hvigor 会自动根据 `compileSdkVersion` 定位组件。
> 如果 SDK 目录名不是 `openharmony`（如 `26.0.0`），需创建 junction 链接：
> ```cmd
> mklink /J "C:\Users\{用户名}\AppData\Local\OpenHarmony\Sdk\openharmony" "C:\Users\{用户名}\AppData\Local\OpenHarmony\Sdk\26.0.0"
> ```

#### 2.4.3 环境变量（可选备选方案）

如果 `local.properties` 未生效，可设置环境变量：
```powershell
$env:OHOS_BASE_SDK_HOME = "C:\Users\{username}\AppData\Local\OpenHarmony\Sdk\{sdk_version}"
```

### 2.5 项目结构确认

打开 DevEco Studio 项目后，确认以下结构：

```
MyApplication3/
├── AppScope/
│   └── app.json5              # App 级配置（bundleName、版本、签名）
├── entry/
│   ├── src/
│   │   ├── main/              # 主应用代码
│   │   │   ├── ets/
│   │   │   │   ├── entryability/
│   │   │   │   ├── pages/
│   │   │   │   └── entrybackupability/
│   │   │   ├── resources/     # 资源文件
│   │   │   └── module.json5   # 主模块配置
│   │   └── ohosTest/          # 测试代码
│   │       ├── ets/
│   │       │   ├── TestRunner.ets          # 测试运行器入口
│   │       │   └── test/
│   │       │       ├── List.test.ets       # 测试套聚合器
│   │       │       ├── Ability.test.ets    # Ability 测试
│   │       │       └── buffer/             # Buffer API 测试
│   │       │           ├── Buffer1.test.ets
│   │       │           ├── Buffer2.test.ets
│   │       │           └── Buffer2New.test.ets
│   │       └── module.json5   # 测试模块配置
│   ├── build-profile.json5    # 模块编译配置
│   └── oh-package.json5       # 模块依赖
├── build-profile.json5        # 根编译配置
└── oh-package.json5           # 根依赖
```

---

## 三、Windows 命令行编译流程

> **前提**：DevEco Studio 已安装且 SDK 已下载（通过 IDE 的 SDK Manager）。

### 3.0 选择正确的 hvigor 版本

**重要**：ArkTS-Dyn（动态语法）和 ArkTS-Sta（静态语法）使用不同版本的 hvigor 工具，编译前必须根据项目的 ETS 版本选择对应的 hvigor 路径。

从 `.oh-xts-config.json` 读取对应的 hvigor 路径：

| ETS 版本 | 配置字段 | 用途 |
|----------|---------|------|
| ArkTS-Dyn（动态） | `for_windows.hvigor_path_1.1` | 动态语法项目编译 |
| ArkTS-Sta（静态） | `for_windows.hvigor_path_1.2` | 静态语法项目编译 |

**选择逻辑**：
1. 检查目标项目的 `build-profile.json5` 中的 `arkTSVersion` 字段
2. 如果 `arkTSVersion` 为 `"1.2"` 或更高 → 使用 `hvigor_path_1.2`
3. 其他情况（无该字段或值为空）→ 使用 `hvigor_path_1.1`

**下文中所有 `{hvigor_path}` 表示根据上述规则选择的 hvigor 路径**：
- ArkTS-Dyn 项目：`{hvigor_path}` = `.oh-xts-config.json` 中的 `hvigor_path_1.1` 值
- ArkTS-Sta 项目：`{hvigor_path}` = `.oh-xts-config.json` 中的 `hvigor_path_1.2` 值

### 3.1 IDE 同步（首次或 SDK 变更后必须执行）

在执行命令行编译前，**必须先在 DevEco Studio IDE 中触发同步**，以确保：
- `local.properties` 正确生成
- `oh_modules` 依赖安装完成
- hvigor workspace 缓存正确初始化

**IDE 同步命令**（在 IDE 终端或命令行执行）：
```cmd
"{deveco_studio_path}\tools\node\node.exe" "{hvigor_path}\hvigorw.js" --sync -p product=default --analyze=normal --parallel --incremental --daemon
```

> **⚠️ 注意**：
> - `{hvigor_path}` 需替换为 `.oh-xts-config.json` 中对应 ETS 版本的 hvigor 路径（参见 3.0 节）
> - 路径中的 `{deveco_studio_path}` 需替换为实际的 DevEco Studio 安装路径
> - `--sync` 参数触发项目同步（等同于 IDE 中的 File → Sync）
> - 同步会自动安装 hvigor 依赖到 `~/.hvigor/project_caches/` 的 workspace 中
> - 首次同步耗时较长，后续增量同步较快

### 3.2 项目清理

```cmd
"{deveco_studio_path}\tools\node\node.exe" "{hvigor_path}\hvigorw.js" -p product=default clean --analyze=normal --parallel --incremental --daemon
```

### 3.3 命令行编译（动态测试套）

#### 3.3.1 编译命令

```cmd
cd /d {xts_acts_path}\testfwk\uitest
"{hvigor_path}\hvigorw.bat" assembleHap --mode module -p module=entry@ohosTest
```

#### 3.3.2 编译产物

编译成功后，HAP 包位于：
```
{项目目录}/entry/build/default/outputs/default/{模块名}-ohosTest.hap
```

#### 3.3.3 停止 hvigor daemon

如果遇到编译问题，可重启 daemon：
```cmd
"{hvigor_path}\hvigorw.bat" --stop-daemon
```

### 3.4 关键路径参考

| 路径 | 说明 |
|------|------|
| `{hvigor_path}/hvigorw.bat` | hvigor 编译包装脚本（根据 ETS 版本选择路径） |
| `{hvigor_path}/hvigorw.js` | hvigor 编译 JS 入口 |
| `{DevEco_Studio}/tools/node/node.exe` | Node.js 运行时 |
| `{hvigor_path}/../hvigor/` | hvigor 引擎模块 |
| `{hvigor_path}/../hvigor-ohos-plugin/` | hvigor OpenHarmony 插件 |
| `~/.hvigor/project_caches/{hash}/workspace/` | hvigor 工作空间缓存 |
| `{项目}/.hvigor/outputs/build-logs/build.log` | 编译日志 |
| `{项目}/local.properties` | SDK 路径配置 |

### 3.5 常见编译错误排查

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Unable to find sdk.dir in local.properties` | SDK 路径未配置 | 在 IDE 中执行同步，或手动设置 `local.properties` |
| `Unable to find components: toolchains:XX` | SDK 组件未安装或路径不匹配 | 通过 IDE SDK Manager 下载组件；检查 SDK 目录结构 |
| `Component has been placed in the wrong place` | SDK 版本目录结构不匹配 | 创建 `openharmony` junction 链接到实际 SDK 版本目录 |
| `ENOENT: no such file ... hvigor.js` | hvigor workspace 缓存损坏 | 删除 `~/.hvigor/project_caches/{hash}/workspace` 并重新同步 |
| `Cannot find module '@ohos/cangjie-build-support'` | 缺少仓颉构建支持（可忽略） | 非仓颉项目可忽略此警告 |

### 3.6 完整编译流程示例

```powershell
# 0. 根据 ETS 版本从 .oh-xts-config.json 读取 hvigor 路径
# ArkTS-Dyn: $hvigorPath = (读取 for_windows.hvigor_path_1.1)
# ArkTS-Sta: $hvigorPath = (读取 for_windows.hvigor_path_1.2)

# 1. 停止可能残留的 daemon
& "$hvigorPath\hvigorw.bat" --stop-daemon

# 2. 进入项目目录
Set-Location "{xts_acts_path}\testfwk\uitest"

# 3. 项目清理（可选）
& "{deveco_studio_path}\tools\node\node.exe" "$hvigorPath\hvigorw.js" -p product=default clean --analyze=normal --parallel --incremental --daemon

# 4. IDE 同步（首次或 SDK 变更后）
& "{deveco_studio_path}\tools\node\node.exe" "$hvigorPath\hvigorw.js" --sync -p product=default --analyze=normal --parallel --incremental --daemon

# 5. 编译 ohosTest HAP
& "$hvigorPath\hvigorw.bat" assembleHap --mode module -p module=entry@ohosTest

# 6. 验证编译产物
Test-Path "{xts_acts_path}\testfwk\uitest\entry\build\default\outputs\*\*.hap"
```

---
