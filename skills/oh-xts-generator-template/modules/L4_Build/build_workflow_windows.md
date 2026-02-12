# Windows 编译与测试工作流

> **模块信息**
> - 层级：L4_Build
> - 优先级：按需加载
> - 适用范围：Windows 环境下的 HarmonyOS XTS 测试工程编译、安装和测试
> - 平台：Windows
> - 依赖：L1_Framework
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

### 2.4 项目结构确认

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

## 三、HAP 编译流程（DevEco Studio）

### 3.1 编译方式选择

Windows 环境下提供两种编译方式：**DevEco Studio IDE**（推荐新手）和**命令行编译**（推荐自动化）。

| 编译方式 | 优点 | 缺点 | 推荐度 |
|---------|------|------|--------|
| **DevEco Studio IDE** | 简单可靠、自动签名、可视化 | 需要 GUI 操作 | ⭐⭐⭐⭐⭐ |
| **命令行编译** | 可自动化、无需 GUI、适合 CI/CD | 需要配置路径 | ⭐⭐⭐⭐ |
| PowerShell 脚本 | 可自动化 | 配置复杂、易出错 | ⭐⭐ |

### 3.2 编译主应用 HAP（可选）

如果需要先编译主应用：

1. **打开项目**：
   - 启动 DevEco Studio
   - File → Open → 选择项目目录

2. **编译主 HAP**：
   - 菜单：Build → Build Hap(s) / APP(s) → Build Hap(s)
   - 或右键 `entry` 模块 → Build → Rebuild 'entry'

3. **输出位置**：
   ```
   entry/build/default/outputs/default/entry-default-signed.hap
   ```

### 3.3 编译测试 HAP（必须）

这是测试执行的关键步骤，提供两种编译方式：

#### 方式 1：使用 DevEco Studio IDE（推荐新手）

1. **在 DevEco Studio 中**：
   - 菜单：**Build → Build Hap(s) / APP(s) → Build OhosTest Hap(s)**
   - 或快捷键：`Ctrl + F9`

2. **编译验证**：
   - 查看 Build 窗口输出
   - 成功标志：`BUILD SUCCESSFUL`
   - 失败标志：红色错误信息

3. **Test HAP 输出位置**：
   ```
   entry/build/default/outputs/ohosTest/entry-ohosTest-signed.hap
   ```

#### 方式 2：使用命令行编译（推荐自动化）

使用 DevEco Studio 的 `hvigorw` 命令行工具进行编译，适合自动化和脚本化。

##### 3.3.2.1 查找 DevEco Studio 安装路径

```powershell
# 查找 hvigorw 工具
where hvigorw

# 预期输出示例：
# D:\DevEco Studio\tools\hvigor\bin\hvigorw
# D:\DevEco Studio\tools\hvigor\bin\hvigorw.bat
```

##### 3.3.2.2 编译命令格式

```powershell
# 完整命令格式
hvigorw.bat assembleHap --mode module -p module=entry@ohosTest -p product=default

# 参数说明
# assembleHap         : 执行 HAP 编译任务
# --mode module       : 模块模式编译
# -p module=entry@ohosTest : 编译 entry 模块的 ohosTest 目标
# -p product=default  : 使用 default 产品配置
```

##### 3.3.2.3 实际编译示例

```powershell
# 进入项目目录
cd C:\Users\x00886684\DevEcoStudioProjects\MyApplication3

# 执行编译（使用完整路径）
"D:\DevEco Studio\tools\hvigor\bin\hvigorw.bat" assembleHap --mode module -p module=entry@ohosTest -p product=default

# 或使用相对路径（如果 hvigorw 在 PATH 中）
hvigorw.bat assembleHap --mode module -p module=entry@ohosTest -p product=default
```

##### 3.3.2.4 编译输出示例

```
> hvigor UP-TO-DATE :entry:ohosTest@PreBuild...
> hvigor Finished :entry:ohosTest@CompileResource... after 378 ms
> hvigor Finished :entry:ohosTest@OhosTestCompileArkTS... after 11 s 6 ms
> hvigor Finished :entry:ohosTest@SignHap... after 209 ms
> hvigor BUILD SUCCESSFUL in 14 s 251 ms
```

**关键输出解读**：
- `BUILD SUCCESSFUL` - 编译成功
- 总耗时：约 14 秒（取决于项目大小）
- Test HAP 输出位置：`entry/build/default/outputs/ohosTest/entry-ohosTest-signed.hap`

##### 3.3.2.5 编译失败处理

如果编译失败，查看错误信息：

```powershell
# 查看详细错误日志
# 编译输出会显示具体的错误信息，包括：
# - 红色错误文本
# - 错误文件位置
# - 错误行号
# - 错误原因
```

常见编译错误：
- **签名配置错误**：检查 `File → Project Structure → Signing Configs`
- **SDK 版本不匹配**：更新 HarmonyOS SDK
- **依赖包缺失**：运行 `ohpm install`

##### 3.3.2.6 验证编译产物

```powershell
# 检查 Test HAP 是否生成
$TestHapPath = "entry\build\default\outputs\ohosTest\entry-ohosTest-signed.hap"
if (Test-Path $TestHapPath) {
    $FileSize = (Get-Item $TestHapPath).Length / 1MB
    Write-Host "✓ Test HAP found: $TestHapPath ($FileSize MB)" -ForegroundColor Green
} else {
    Write-Host "✗ Test HAP not found!" -ForegroundColor Red
    exit 1
}

# 列出所有 HAP 文件
Get-ChildItem "entry\build\default\outputs" -Recurse -Filter "*.hap" | Format-Table Name, @{Name="Size(MB)";Expression={$_.Length/1MB}}
```

##### 3.3.2.7 命令行编译优势

相比 IDE 编译，命令行编译的优势：

| 优势 | 说明 |
|------|------|
| **可自动化** | 易于集成到脚本和 CI/CD 流程 |
| **无需 GUI** | 可在无图形界面环境下执行 |
| **可重复** | 命令可以精确复现 |
| **高效** | 无需启动 IDE，节省资源 |
| **日志完整** | 所有输出都可以重定向到文件 |

### 3.4 验证编译产物

使用 PowerShell 验证 HAP 文件：

```powershell
# 进入项目目录
cd C:\Users\x00886684\DevEcoStudioProjects\MyApplication3

# 检查 Test HAP 是否生成
$TestHapPath = "entry\build\default\outputs\ohosTest\entry-ohosTest-signed.hap"
if (Test-Path $TestHapPath) {
    $FileSize = (Get-Item $TestHapPath).Length / 1KB
    Write-Host "✓ Test HAP found: $TestHapPath ($FileSize KB)" -ForegroundColor Green
} else {
    Write-Host "✗ Test HAP not found!" -ForegroundColor Red
    exit 1
}

# 列出所有 HAP 文件
Get-ChildItem "entry\build\default\outputs" -Recurse -Filter "*.hap" | Format-Table Name, Length
```

---

## 四、测试执行流程

### 4.1 获取测试套信息

在执行测试前，需要知道测试套的名称。

#### 方法1：查看 List.test.ets

```powershell
# 查看测试套注册文件
Get-Content "entry\src\ohosTest\ets\test\List.test.ets"
```

示例输出：
```typescript
import abilityTest from './Ability.test';
import BufferTest from './buffer/Buffer1.test';
import bufferTest from './buffer/Buffer2.test';
import bufferNewTest from './buffer/Buffer2New.test.ets';

export default function testsuite() {
  abilityTest();
  BufferTest();
  bufferTest();
  bufferNewTest();
}
```

#### 方法2：查找 describe 名称

```powershell
# 搜索所有测试套名称
Select-String -Path "entry\src\ohosTest\ets\test\**\*.test.ets" -Pattern "describe\(" -Context 0,0
```

### 4.2 单个测试套执行

使用 `hdc shell aa test` 命令执行测试。

#### 4.2.1 基本命令格式

```powershell
# 完整命令格式
hdc shell aa test -b <BundleName> -m <ModuleName> -s unittest <TestRunner> -s class <TestSuite> -s timeout <Timeout>

# 参数说明
# -b <BundleName>   : 应用包名（从 AppScope/app.json5 获取）
# -m <ModuleName>   : 模块名（测试模块通常是 entry_test）
# -s unittest <TestRunner> : 测试运行器（通常是 OpenHarmonyTestRunner）
# -s class <TestSuite>     : 测试套名称（describe 的第一个参数）
# -s timeout <Timeout>     : 超时时间（毫秒）
```

#### 4.2.2 实际执行示例

```powershell
# 执行 ActsBufferNewTest 测试套
hdc shell aa test -b com.example.myapplication -m entry_test -s unittest OpenHarmonyTestRunner -s class ActsBufferNewTest -s timeout 15000

# 执行 ActsAbilityTest 测试套
hdc shell aa test -b com.example.myapplication -m entry_test -s unittest OpenHarmonyTestRunner -s class ActsAbilityTest -s timeout 15000
```

#### 4.2.3 获取 BundleName

从 `AppScope/app.json5` 中获取：

```json
{
  "app": {
    "bundleName": "com.example.myapplication"  // 这是 BundleName
  }
}
```

### 4.3 执行所有测试套

为了执行所有测试套，需要逐个执行每个测试套并汇总结果。

#### 4.3.1 获取所有测试套名称

```powershell
# 查找所有测试套
$TestFiles = Get-ChildItem "entry\src\ohosTest\ets\test" -Recurse -Filter "*.test.ets" | Where-Object { $_.Name -ne "List.test.ets" }

foreach ($file in $TestFiles) {
    Write-Host "`n=== $($file.Name) ===" -ForegroundColor Cyan
    Select-String -Path $file.FullName -Pattern "describe\(" | ForEach-Object {
        if ($_ -match 'describe\(["\']([^"\']+)["\']') {
            Write-Host "  - $($matches[1])" -ForegroundColor Gray
        }
    }
}
```

#### 4.3.2 批量执行所有测试套

```powershell
# 配置参数
$BundleName = "com.example.myapplication"
$ModuleName = "entry_test"
$TestRunner = "OpenHarmonyTestRunner"
$Timeout = 15000

# 测试套列表（从 List.test.ets 中获取）
$TestSuites = @(
    "ActsAbilityTest",
    "bufferTest",
    "ActsBufferTest",
    "ActsBufferNewTest"
)

# 执行所有测试套
$Results = @()

foreach ($suite in $TestSuites) {
    Write-Host "`n=== Executing: $suite ===" -ForegroundColor Cyan

    $Command = "hdc shell aa test -b $BundleName -m $ModuleName -s unittest $TestRunner -s class $suite -s timeout $Timeout"
    $Output = Invoke-Expression $Command

    # 解析结果
    if ($Output -match 'Tests run: (\d+), Failure: (\d+), Error: (\d+), Pass: (\d+)') {
        $Result = [PSCustomObject]@{
            Suite     = $suite
            Total     = [int]$matches[1]
            Failed    = [int]$matches[2]
            Errors    = [int]$matches[3]
            Passed    = [int]$matches[4]
            PassRate  = [math]::Round(([int]$matches[4] / [int]$matches[1]) * 100, 2)
        }
        $Results += $Result

        Write-Host "  Total: $($Result.Total)" -ForegroundColor White
        Write-Host "  Passed: $($Result.Passed)" -ForegroundColor Green
        Write-Host "  Failed: $($Result.Failed)" -ForegroundColor Red
        Write-Host "  Pass Rate: $($Result.PassRate)%" -ForegroundColor Cyan
    }
}

# 汇总统计
Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "OVERALL TEST RESULTS" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan

$TotalTests = ($Results | Measure-Object -Property Total -Sum).Sum
$TotalPassed = ($Results | Measure-Object -Property Passed -Sum).Sum
$TotalFailed = ($Results | Measure-Object -Property Failed -Sum).Sum
$TotalErrors = ($Results | Measure-Object -Property Errors -Sum).Sum
$OverallPassRate = [math]::Round(($TotalPassed / $TotalTests) * 100, 2)

Write-Host "`nTotal Test Suites: $($Results.Count)" -ForegroundColor White
Write-Host "Total Test Cases: $TotalTests" -ForegroundColor White
Write-Host "Passed: $TotalPassed ($OverallPassRate%)" -ForegroundColor Green
Write-Host "Failed: $TotalFailed" -ForegroundColor Red
Write-Host "Errors: $TotalErrors" -ForegroundColor Yellow

# 详细结果表格
Write-Host "`nDetailed Results:" -ForegroundColor Cyan
$Results | Format-Table -AutoSize
```

---

## 五、测试结果解析

### 5.1 Hypium 输出格式

Hypium 测试框架输出标准格式：

```
OHOS_REPORT_SUM: 13                          # 总用例数
OHOS_REPORT_STATUS: class=ActsBufferNewTest  # 测试套名

OHOS_REPORT_STATUS: current=1                # 当前用例序号
OHOS_REPORT_STATUS: numtests=13              # 总用例数
OHOS_REPORT_STATUS: test=testBufferFrom20009 # 用例名
OHOS_REPORT_STATUS_CODE: 0                   # 0=通过, -2=失败

OHOS_REPORT_RESULT: stream=Tests run: 13, Failure: 5, Error: 0, Pass: 8, Ignore: 0
OHOS_REPORT_CODE: -1                         # -1=有失败, 0=全通过
```

### 5.2 解析测试结果

#### 5.2.1 提取汇总信息

```powershell
# 执行测试并捕获输出
$TestOutput = hdc shell aa test -b com.example.myapplication -m entry_test -s unittest OpenHarmonyTestRunner -s class ActsBufferNewTest -s timeout 15000

# 提取结果行
$ResultLine = $TestOutput | Select-String "OHOS_REPORT_RESULT: stream=" | Select-Object -Last 1

if ($ResultLine -match 'Tests run: (\d+), Failure: (\d+), Error: (\d+), Pass: (\d+), Ignore: (\d+)') {
    [int]$Total = $matches[1]
    [int]$Failed = $matches[2]
    [int]$Errors = $matches[3]
    [int]$Passed = $matches[4]
    [int]$Ignored = $matches[5]
    [double]$PassRate = [math]::Round(($Passed / $Total) * 100, 2)

    Write-Host "`n=== Test Results ===" -ForegroundColor Cyan
    Write-Host "Total:    $Total" -ForegroundColor White
    Write-Host "Passed:   $Passed ($PassRate%)" -ForegroundColor Green
    Write-Host "Failed:   $Failed" -ForegroundColor Red
    Write-Host "Errors:   $Errors" -ForegroundColor Yellow
    Write-Host "Ignored:  $Ignored" -ForegroundColor Gray
}
```

#### 5.2.2 提取失败用例详情

```powershell
# 提取失败的用例
$FailedTests = $TestOutput | Select-String "OHOS_REPORT_STATUS_CODE: -2" -Context 5,0

foreach ($failed in $FailedTests) {
    $context = $failed.Context.PreContext | Select-String "test=" | Select-Object -First 1
    if ($context -match 'test=([^\s]+)') {
        $testName = $matches[1]

        # 提取错误信息
        $errorLine = $failed.Context.PostContext | Select-String "stream=" | Select-Object -First 1
        $errorMsg = if ($errorLine -match 'stream=(.+)') { $matches[1] } else { "Unknown error" }

        Write-Host "✗ $testName" -ForegroundColor Red
        Write-Host "  Error: $errorMsg" -ForegroundColor Gray
    }
}
```

### 5.3 生成测试报告

```powershell
# 生成 JSON 格式报告
$Report = @{
    timestamp   = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    bundleName  = $BundleName
    moduleName  = $ModuleName
    suites      = @(
        foreach ($result in $Results) {
            @{
                name      = $result.Suite
                total     = $result.Total
                passed    = $result.Passed
                failed    = $result.Failed
                errors    = $result.Errors
                passRate  = $result.PassRate
            }
        }
    )
    summary     = @{
        totalSuites  = $Results.Count
        totalTests   = $TotalTests
        totalPassed  = $TotalPassed
        totalFailed  = $TotalFailed
        totalErrors  = $TotalErrors
        passRate     = $OverallPassRate
    }
}

$ReportJson = $Report | ConvertTo-Json -Depth 4
$ReportJson | Out-File "test_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').json" -Encoding UTF8

Write-Host "`n✓ Report saved to: test_report_*.json" -ForegroundColor Green
```

---

## 六、完整自动化脚本

### 6.1 一键执行所有测试

将以下脚本保存为 `run_all_tests.ps1`：

```powershell
<#
.SYNOPSIS
    HarmonyOS XTS 测试自动化脚本
.DESCRIPTION
    在 Windows 环境下自动执行所有测试套并统计结果
.PARAMETER ProjectPath
    项目根目录（默认当前目录）
.PARAMETER BundleName
    应用包名
.EXAMPLE
    .\run_all_tests.ps1 -ProjectPath "C:\Projects\MyApp" -BundleName "com.example.myapplication"
#>

param(
    [string]$ProjectPath = (Get-Location).Path,
    [string]$BundleName = "com.example.myapplication"
)

# 配置参数
$ModuleName = "entry_test"
$TestRunner = "OpenHarmonyTestRunner"
$Timeout = 15000

# 检查项目路径
if (-not (Test-Path $ProjectPath)) {
    Write-Host "✗ Project path not found: $ProjectPath" -ForegroundColor Red
    exit 1
}

# 切换到项目目录
Set-Location $ProjectPath

# 检查 Test HAP 是否存在
$TestHapPath = "entry\build\default\outputs\ohosTest\entry-ohosTest-signed.hap"
if (-not (Test-Path $TestHapPath)) {
    Write-Host "⚠ Test HAP not found: $TestHapPath" -ForegroundColor Yellow
    Write-Host "Please build Test HAP first:" -ForegroundColor Yellow
    Write-Host "  DevEco Studio → Build → Build Hap(s) / APP(s) → Build OhosTest Hap(s)" -ForegroundColor Cyan
    exit 1
}

Write-Host "`n" + "="*70 -ForegroundColor Cyan
Write-Host "HarmonyOS XTS Test Automation" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "Project:   $ProjectPath" -ForegroundColor Gray
Write-Host "Bundle:    $BundleName" -ForegroundColor Gray
Write-Host "Test HAP:  $TestHapPath" -ForegroundColor Gray
Write-Host "="*70 -ForegroundColor Cyan

# 获取所有测试套
Write-Host "`n[1/4] Discovering test suites..." -ForegroundColor Yellow

$ListTestPath = "entry\src\ohosTest\ets\test\List.test.ets"
if (-not (Test-Path $ListTestPath)) {
    Write-Host "✗ List.test.ets not found" -ForegroundColor Red
    exit 1
}

# 解析 List.test.ets 获取测试套
$ListContent = Get-Content $ListTestPath -Raw
$Imports = $ListContent | Select-String "import\s+\w+\s+from\s+['\"](.+)['\"]" | ForEach-Object { $_.Matches[0].Groups[1].Value }

$TestSuites = @()
foreach ($import in $Imports) {
    # 跳过 List.test.ets
    if ($import -match "List\.test") { continue }

    # 查找对应的测试文件
    $testFile = Get-ChildItem "entry\src\ohosTest\ets\test" -Recurse -Filter "*$($import.Split('/')[-1])*" | Where-Object { $_.Name -ne "List.test.ets" } | Select-Object -First 1

    if ($testFile) {
        # 查找 describe 名称
        $describeMatch = Select-String -Path $testFile.FullName -Pattern "describe\(['\"]([^'\"]+)['\"]" | Select-Object -First 1
        if ($describeMatch) {
            $suiteName = $describeMatch.Matches[0].Groups[1].Value
            $TestSuites += @{
                Name = $suiteName
                File = $testFile.Name
            }
            Write-Host "  ✓ Found: $($suiteName)" -ForegroundColor Green
        }
    }
}

if ($TestSuites.Count -eq 0) {
    Write-Host "✗ No test suites found" -ForegroundColor Red
    exit 1
}

# 执行所有测试套
Write-Host "`n[2/4] Running test suites..." -ForegroundColor Yellow

$Results = @()
$TotalStartTime = Get-Date

foreach ($suite in $TestSuites) {
    $suiteName = $suite.Name
    Write-Host "`n--- Executing: $suiteName ---" -ForegroundColor Cyan

    $SuiteStartTime = Get-Date

    # 执行测试
    $Command = "hdc shell aa test -b $BundleName -m $ModuleName -s unittest $TestRunner -s class $suiteName -s timeout $Timeout"
    $Output = Invoke-Expression $Command
    $SuiteEndTime = Get-Date
    $SuiteDuration = ($SuiteEndTime - $SuiteStartTime).TotalMilliseconds

    # 解析结果
    if ($Output -match 'Tests run: (\d+), Failure: (\d+), Error: (\d+), Pass: (\d+), Ignore: (\d+)') {
        $Result = [PSCustomObject]@{
            Suite      = $suiteName
            Total      = [int]$matches[1]
            Failed     = [int]$matches[2]
            Errors     = [int]$matches[3]
            Passed     = [int]$matches[4]
            Ignored    = [int]$matches[5]
            PassRate   = [math]::Round(([int]$matches[4] / [int]$matches[1]) * 100, 2)
            Duration   = [math]::Round($SuiteDuration, 0)
        }
        $Results += $Result

        # 显示结果
        $Color = if ($Result.Failed -eq 0 -and $Result.Errors -eq 0) { "Green" } else { "Yellow" }
        Write-Host "  Total:     $($Result.Total)" -ForegroundColor White
        Write-Host "  Passed:    $($Result.Passed) ($($Result.PassRate)%)" -ForegroundColor Green
        Write-Host "  Failed:    $($Result.Failed)" -ForegroundColor Red
        Write-Host "  Errors:    $($Result.Errors)" -ForegroundColor Yellow
        Write-Host "  Duration:  $($Result.Duration) ms" -ForegroundColor Gray

        # 如果有失败，显示详细错误
        if ($Result.Failed -gt 0) {
            Write-Host "`n  Failed tests:" -ForegroundColor Red
            $FailedTests = $Output | Select-String "OHOS_REPORT_STATUS_CODE: -2" -Context 5,2
            foreach ($failed in $FailedTests) {
                $context = $failed.Context.PreContext | Select-String "test=" | Select-Object -First 1
                if ($context -match 'test=([^\s]+)') {
                    Write-Host "    ✗ $($matches[1])" -ForegroundColor Red
                }
            }
        }
    } else {
        Write-Host "  ✗ Failed to parse test output" -ForegroundColor Red
    }
}

$TotalEndTime = Get-Date
$TotalDuration = ($TotalEndTime - $TotalStartTime).TotalSeconds

# 汇总统计
Write-Host "`n[3/4] Generating summary..." -ForegroundColor Yellow

$TotalTests = ($Results | Measure-Object -Property Total -Sum).Sum
$TotalPassed = ($Results | Measure-Object -Property Passed -Sum).Sum
$TotalFailed = ($Results | Measure-Object -Property Failed -Sum).Sum
$TotalErrors = ($Results | Measure-Object -Property Errors -Sum).Sum
$TotalIgnored = ($Results | Measure-Object -Property Ignored -Sum).Sum
$OverallPassRate = [math]::Round(($TotalPassed / $TotalTests) * 100, 2)

Write-Host "`n" + "="*70 -ForegroundColor Cyan
Write-Host "OVERALL TEST RESULTS" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "`nTotal Test Suites:    $($Results.Count)" -ForegroundColor White
Write-Host "Total Test Cases:     $TotalTests" -ForegroundColor White
Write-Host "Passed:               $TotalPassed ($OverallPassRate%)" -ForegroundColor Green
Write-Host "Failed:               $TotalFailed" -ForegroundColor Red
Write-Host "Errors:               $TotalErrors" -ForegroundColor Yellow
Write-Host "Ignored:              $TotalIgnored" -ForegroundColor Gray
Write-Host "Total Duration:       $([math]::Round($TotalDuration, 2)) s" -ForegroundColor Gray

# 详细结果表格
Write-Host "`nDetailed Results:" -ForegroundColor Cyan
$Results | Format-Table -AutoSize

# 保存报告
Write-Host "`n[4/4] Saving report..." -ForegroundColor Yellow

$Report = @{
    timestamp   = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    projectPath = $ProjectPath
    bundleName  = $BundleName
    duration    = [math]::Round($TotalDuration, 2)
    suites      = @(
        foreach ($result in $Results) {
            @{
                name      = $result.Suite
                total     = $result.Total
                passed    = $result.Passed
                failed    = $result.Failed
                errors    = $result.Errors
                ignored   = $result.Ignored
                passRate  = $result.PassRate
                duration  = $result.Duration
            }
        }
    )
    summary     = @{
        totalSuites  = $Results.Count
        totalTests   = $TotalTests
        totalPassed  = $TotalPassed
        totalFailed  = $TotalFailed
        totalErrors  = $TotalErrors
        totalIgnored = $TotalIgnored
        passRate     = $OverallPassRate
        duration     = [math]::Round($TotalDuration, 2)
    }
}

$ReportFile = "test_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
$Report | ConvertTo-Json -Depth 4 | Out-File $ReportFile -Encoding UTF8

Write-Host "  ✓ Report saved: $ReportFile" -ForegroundColor Green

Write-Host "`n" + "="*70 -ForegroundColor Cyan
if ($TotalFailed -eq 0 -and $TotalErrors -eq 0) {
    Write-Host "✓ ALL TESTS PASSED!" -ForegroundColor Green
} else {
    Write-Host "⚠ SOME TESTS FAILED" -ForegroundColor Yellow
}
Write-Host "="*70 -ForegroundColor Cyan
```

### 6.2 使用方法

```powershell
# 方法1：使用默认参数（当前目录）
.\run_all_tests.ps1

# 方法2：指定项目路径和包名
.\run_all_tests.ps1 -ProjectPath "C:\Projects\MyApp" -BundleName "com.example.myapplication"
```

### 6.3 预期输出示例

```
======================================================================
HarmonyOS XTS Test Automation
======================================================================
Project:   C:\Projects\MyApp
Bundle:    com.example.myapplication
Test HAP:  entry\build\default\outputs\ohosTest\entry-ohosTest-signed.hap
======================================================================

[1/4] Discovering test suites...
  ✓ Found: ActsAbilityTest
  ✓ Found: bufferTest
  ✓ Found: ActsBufferTest
  ✓ Found: ActsBufferNewTest

[2/4] Running test suites...

--- Executing: ActsAbilityTest ---
  Total:     1
  Passed:    1 (100%)
  Failed:    0
  Errors:    0
  Duration:  17 ms

--- Executing: bufferTest ---
  Total:     440
  Passed:    440 (100%)
  Failed:    0
  Errors:    0
  Duration:  0 ms

--- Executing: ActsBufferTest ---
  Total:     653
  Passed:    653 (100%)
  Failed:    0
  Errors:    0
  Duration:  0 ms

--- Executing: ActsBufferNewTest ---
  Total:     13
  Passed:    8 (61.54%)
  Failed:    5
  Errors:    0
  Duration:  189 ms

  Failed tests:
    ✗ testBufferFrom20010
    ✗ testBufferFrom20012
    ✗ testBufferFrom30011
    ✗ testBufferFrom30012
    ✗ testBufferFrom30017

[3/4] Generating summary...

======================================================================
OVERALL TEST RESULTS
======================================================================

Total Test Suites:    4
Total Test Cases:     1107
Passed:               1102 (99.55%)
Failed:               5
Errors:               0
Ignored:              0
Total Duration:       0.21 s

Detailed Results:

Suite              Total Passed Failed Errors PassRate Duration
-----              ----- ------ ------ ------ -------- --------
ActsAbilityTest        1      1      0      0    100.00       17
bufferTest           440    440      0      0    100.00        0
ActsBufferTest       653    653      0      0    100.00        0
ActsBufferNewTest     13      8      5      0     61.54      189

[4/4] Saving report...
  ✓ Report saved: test_report_20250201_153045.json

======================================================================
⚠ SOME TESTS FAILED
======================================================================
```

---

## 七、故障排除

### 7.1 编译问题

#### 问题：Test HAP 未生成

**症状**：
```
⚠ Test HAP not found: entry\build\default\outputs\ohosTest\entry-ohosTest-signed.hap
```

**解决方案**：
1. 在 DevEco Studio 中打开项目
2. 菜单：**Build → Build Hap(s) / APP(s) → Build OhosTest Hap(s)**
3. 等待编译完成，查看 Build 窗口输出
4. 确认显示 `BUILD SUCCESSFUL`

#### 问题：编译失败

**常见错误**：
- 签名配置错误
- SDK 版本不匹配
- 依赖包缺失

**解决方案**：
1. 查看 Build 窗口的红色错误信息
2. 检查签名配置（File → Project Structure → Signing Configs）
3. 更新 SDK：Tools → SDK Manager
4. 清理并重新编译：Build → Clean Project → Build OhosTest Hap(s)

### 7.2 设备连接问题

#### 问题：设备未连接

**症状**：
```
hdc shell aa test ...
error: device not found
```

**解决方案**：
```powershell
# 1. 检查设备列表
hdc list targets

# 2. 如果为空，重启 hdc
hdc kill
hdc start

# 3. 添加设备（USB 网络）
hdc tconn 192.168.1.100:5555

# 4. 再次检查
hdc list targets
```

#### 问题：测试超时

**症状**：
```
start ability successfully.
[长时间无输出]
```

**解决方案**：
```powershell
# 增加超时时间到 60 秒
hdc shell aa test -b com.example.myapplication -m entry_test -s unittest OpenHarmonyTestRunner -s class ActsBufferNewTest -s timeout 60000
```

### 7.3 测试执行问题

#### 问题：测试套名称错误

**症状**：
```
error: test class ActsXXXTest not found
```

**解决方案**：
1. 检查测试套名称是否正确（区分大小写）
2. 查看 `List.test.ets` 确认测试套注册
3. 使用 Grep 查找实际的 `describe()` 名称

```powershell
# 查找所有测试套名称
Select-String -Path "entry\src\ohosTest\ets\test\**\*.test.ets" -Pattern "describe\("
```

#### 问题：BundleName 错误

**症状**：
```
error: bundle does not exist
```

**解决方案**：
1. 查看 `AppScope/app.json5` 中的 `bundleName`
2. 确保使用正确的包名（区分大小写）

```powershell
# 查看包名
Get-Content "AppScope\app.json5" | Select-String "bundleName"
```

### 7.4 结果解析问题

#### 问题：无法解析测试结果

**症状**：
```
✗ Failed to parse test output
```

**解决方案**：
1. 检查测试是否真的执行了（查看完整输出）
2. 查看是否有设备错误或应用崩溃
3. 保存完整输出以便调试

```powershell
# 保存完整输出
$Output = hdc shell aa test -b com.example.myapplication -m entry_test -s unittest OpenHarmonyTestRunner -s class ActsBufferNewTest -s timeout 15000
$Output | Out-File "test_debug_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt" -Encoding UTF8
```

---

## 八、最佳实践

### 8.1 开发工作流

推荐的开发和测试流程：

```
1. 编写/修改测试代码
   ↓
2. 在 DevEco Studio 中编译 Test HAP
   Build → Build OhosTest Hap(s)
   ↓
3. 执行测试
   .\run_all_tests.ps1
   ↓
4. 查看报告
   test_report_*.json
   ↓
5. 修复失败的测试（如有）
   ↓
6. 重复步骤 1-5
```

### 8.2 持续集成

可以将此流程集成到 CI/CD：

```powershell
# CI 脚本示例
.\run_all_tests.ps1 -ProjectPath $env:PROJECT_PATH -BundleName $env:BUNDLE_NAME

# 检查退出码
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tests failed!" -ForegroundColor Red
    exit 1
}
```

### 8.3 性能优化

- **并行执行**：对于独立的测试套，可以考虑并行执行
- **超时设置**：根据测试用例的执行时间调整超时值
- **设备选择**：使用性能更好的设备可以加快测试速度

---

## 九、实际案例总结

### 9.1 成功执行案例

以下是基于实际项目的测试执行总结：

**项目信息**：
- 项目名称：MyApplication3
- BundleName：com.example.myapplication
- 测试套数量：4 个
- 总测试用例：1,107 个

**执行结果**：
```
总测试用例数:    1,107
通过用例数:      1,102 (99.55%)
失败用例数:          5 (0.45%)
错误用例数:          0 (0.00%)
```

**测试套详情**：

| 测试套 | 总用例 | 通过 | 失败 | 通过率 |
|--------|--------|------|------|--------|
| ActsAbilityTest | 1 | 1 | 0 | 100% |
| bufferTest | 440 | 440 | 0 | 100% |
| ActsBufferTest | 653 | 653 | 0 | 100% |
| ActsBufferNewTest | 13 | 8 | 5 | 61.54% |

**关键步骤**：
1. ✅ 在 DevEco Studio 中编译 Test HAP
2. ✅ 使用 `hdc shell aa test` 命令执行测试
3. ✅ 解析 Hypium 输出格式
4. ✅ 汇总所有测试套结果

### 9.2 经验总结

**成功要点**：
1. **DevEco Studio 编译**：使用 IDE 编译是最可靠的方式
2. **自动安装**：`hdc shell aa test` 命令会自动安装 HAP
3. **逐个执行**：需要逐个执行测试套并汇总结果
4. **结果解析**：Hypium 输出格式固定，可以使用正则表达式解析

**注意事项**：
1. 确保设备连接正常（`hdc list targets`）
2. Test HAP 必须先编译（`Build → Build OhosTest Hap(s)`）
3. BundleName 必须与 `app.json5` 一致
4. 测试套名称必须与 `describe()` 第一个参数一致

---

## 十、ArkTS 静态 XTS 编译流程（arkts-sta）

> **本章适用场景**：当用户明确提到"arkts-sta"、"arkts静态"、"ArkTS静态"、"静态xts"等关键词，或者工程配置了 `arkTSVersion: "1.2"` 时使用本章流程。

### 10.1 静态编译模式概述

ArkTS 静态 XTS 编译模式是针对 ArkTS 静态强类型语法的编译流程，具有以下特点：

- **严格类型检查**：所有变量和函数必须有明确的类型注解
- **静态规范约束**：遵守 ArkTS 静态语言规范（禁止 any、禁止对象解构等）
- **Java 环境依赖**：需要配置 JAVA_HOME 环境变量
- **特殊编译参数**：使用静态模式特定的编译参数

### 10.2 环境准备

#### 10.2.1 检查工程类型

首先确认工程是否为静态模式：

```powershell
# 检查 build-profile.json5 中的 arkTSVersion 配置
Get-Content "build-profile.json5" | Select-String "arkTSVersion"
```

**静态工程特征**：
- `build-profile.json5` 中包含 `"arkTSVersion": "1.2"` 或更高版本
- 工程使用 ArkTS 静态语法规范
- 编译时会进行严格的静态类型检查

#### 10.2.2 Java 环境配置（必需）

静态编译必须配置 Java 环境：

```powershell
# 方法1：临时设置（当前 PowerShell 会话）
$env:JAVA_HOME = "D:\DevEco Studio\jbr"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH

# 验证 Java 安装
java -version

# 预期输出示例：
# openjdk version "11.0.15" 2022-04-19
# OpenJDK Runtime Environment (build 11.0.15+10)
```

**⚠️ 重要**：静态编译过程中，hvigorw 需要调用 Java 编译器，如果 JAVA_HOME 未配置会导致 `spawn java ENOENT` 错误。

#### 10.2.3 Node.js 环境配置

```powershell
# 检查 Node.js 版本
node --version

# 预期输出：v14.x 或更高
```

### 10.3 静态编译流程

#### 10.3.1 方法1：使用 PowerShell 脚本（推荐）

创建 `build_arkts_static.ps1`：

```powershell
# ============================================
# ArkTS 静态 XTS 编译脚本
# ============================================

# 1. 设置 Java 环境
Write-Host "[1/4] 配置 Java 环境..." -ForegroundColor Yellow
$env:JAVA_HOME = "D:\DevEco Studio\jbr"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH

# 2. 设置 Node.js 路径
Write-Host "[2/4] 配置 Node.js 环境..." -ForegroundColor Yellow
$env:PATH = "D:\DevEco Studio\tools\node;" + $env:PATH

# 3. 执行静态编译
Write-Host "[3/4] 开始 ArkTS 静态编译..." -ForegroundColor Yellow
& "D:\DevEco Studio\tools\node\node.exe" "D:\DevEco Studio\tools\hvigor\bin\hvigorw.js" `
  --mode module `
  -p product=default `
  assembleHap `
  --analyze=normal `
  --parallel `
  --incremental `
  --no-daemon

# 4. 检查编译结果
Write-Host "[4/4] 检查编译产物..." -ForegroundColor Yellow
$TestHapPath = "entry\build\default\outputs\ohosTest\entry-ohosTest-signed.hap"
if (Test-Path $TestHapPath) {
    $FileSize = (Get-Item $TestHapPath).Length / 1KB
    Write-Host "✓ 静态编译成功: $TestHapPath ($FileSize KB)" -ForegroundColor Green
} else {
    Write-Host "✗ 编译失败，未找到 Test HAP" -ForegroundColor Red
    exit 1
}
```

**使用方法**：

```powershell
# 在项目目录下执行
powershell -ExecutionPolicy Bypass -File build_arkts_static.ps1
```

#### 10.3.2 方法2：直接使用 hvigorw 命令

```powershell
# 进入项目目录
cd C:\Users\x00886684\Desktop\xts_demo_1

# 设置 Java 环境（必需）
$env:JAVA_HOME = "D:\DevEco Studio\jbr"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH

# 执行静态编译
"D:\DevEco Studio\tools\hvigor\bin\hvigorw.bat" assembleHap --mode module -p module=entry@ohosTest -p product=default
```

### 10.4 编译输出示例

**成功输出**：

```
> hvigor UP-TO-DATE :entry:ohosTest@PreBuild...
> hvigor Finished :entry:ohosTest@CompileResource... after 378 ms
> hvigor Finished :entry:ohosTest@OhosTestCompileArkTS... after 15 s 234 ms
> hvigor Finished :entry:ohosTest@SignHap... after 209 ms
> hvigor BUILD SUCCESSFUL in 18 s 451 ms
```

**关键差异**：
- 静态编译通常比动态编译慢（需要额外的类型检查）
- `OhosTestCompileArkTS` 阶段耗时更长（静态类型检查）

### 10.5 静态类型检查

静态编译会自动执行以下类型检查：

#### 10.5.1 类型注解完整性检查

```typescript
// ✓ 正确 - 显式类型注解
function add(a: number, b: number): number {
  return a + b;
}

// ✗ 错误 - 缺少类型注解（静态模式下会报错）
function add(a, b) {
  return a + b;
}
```

#### 10.5.2 禁止 any 类型检查

```typescript
// ✗ 错误 - 静态模式禁止使用 any
let data: any = getSomeData();

// ✓ 正确 - 使用具体类型或 unknown
let data: unknown = getSomeData();
```

#### 10.5.3 字段初始化检查

```typescript
// ✓ 正确 - 所有字段都初始化
class Person {
  name: string = "";
  age: number = 0;
}

// ✗ 错误 - 字段未初始化
class Person {
  name: string;
  age: number;
}
```

### 10.6 常见编译错误及解决方案

#### 错误1：spawn java ENOENT

**症状**：
```
Error: spawn java ENOENT
```

**原因**：Java 不在 PATH 环境变量中

**解决方案**：
```powershell
# 设置 JAVA_HOME
$env:JAVA_HOME = "D:\DevEco Studio\jbr"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH

# 或使用 PowerShell 脚本（推荐）
powershell -ExecutionPolicy Bypass -File build_arkts_static.ps1
```

#### 错误2：类型检查错误

**症状**：
```
Type 'any' is not allowed in ArkTS static mode
Type 'string' is not assignable to type 'number'
```

**原因**：违反 ArkTS 静态类型规范

**解决方案**：
1. 检查是否使用了 `any` 类型
2. 确保所有函数参数和返回值都有类型注解
3. 验证类型兼容性
4. 参考：`references/arkts-static-spec/` 目录下的规范文档

#### 错误3：字段未初始化

**症状**：
```
Property 'xxx' has no initializer and is not definitely assigned
```

**解决方案**：
```typescript
// 添加默认值或使用构造函数初始化
class MyClass {
  // 方法1：添加默认值
  field: string = "";

  // 方法2：构造函数初始化
  constructor() {
    this.field = "";
  }
}
```

### 10.7 测试执行流程

静态编译成功后，测试执行流程与动态模式相同：

#### 10.7.1 安装 HAP

```powershell
# 使用 hdc 安装
hdc install entry\build\default\outputs\ohosTest\entry-ohosTest-signed.hap

# 或使用自动安装（推荐）
hdc shell aa test -b <BundleName> -m entry_test -s unittest OpenHarmonyTestRunner -s class <TestSuite>
```

#### 10.7.2 执行测试

```powershell
# 执行单个测试套
hdc shell aa test -b com.example.myapplication -m entry_test -s unittest OpenHarmonyTestRunner -s class ActsBufferTest -s timeout 15000

# 执行所有测试套（使用自动化脚本）
.\run_all_tests.ps1
```

### 10.8 完整自动化脚本

创建 `build_and_test_static.ps1`：

```powershell
<#
.SYNOPSIS
    ArkTS 静态 XTS 测试完整自动化脚本
.DESCRIPTION
    包含静态编译、HAP 安装、测试执行的完整流程
#>

param(
    [string]$ProjectPath = (Get-Location).Path,
    [string]$BundleName = "com.example.myapplication"
)

# 1. 配置环境
Write-Host "`n[环境准备] 配置 Java 和 Node.js 环境..." -ForegroundColor Yellow
$env:JAVA_HOME = "D:\DevEco Studio\jbr"
$env:PATH = "$env:JAVA_HOME\bin;D:\DevEco Studio\tools\node;" + $env:PATH

# 2. 静态编译
Write-Host "`n[1/3] 执行 ArkTS 静态编译..." -ForegroundColor Yellow
Set-Location $ProjectPath

& "D:\DevEco Studio\tools\node\node.exe" "D:\DevEco Studio\tools\hvigor\bin\hvigorw.js" `
  --mode module `
  -p product=default `
  assembleHap `
  --analyze=normal `
  --parallel `
  --incremental `
  --no-daemon

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 编译失败" -ForegroundColor Red
    exit 1
}

# 3. 检查设备
Write-Host "`n[2/3] 检查设备连接..." -ForegroundColor Yellow
$Devices = hdc list targets
if ($Devices -eq "") {
    Write-Host "✗ 未检测到设备" -ForegroundColor Red
    exit 1
}
Write-Host "✓ 设备已连接: $Devices" -ForegroundColor Green

# 4. 执行测试
Write-Host "`n[3/3] 执行测试..." -ForegroundColor Yellow
# 这里可以调用 run_all_tests.ps1 或直接执行测试命令
.\run_all_tests.ps1 -ProjectPath $ProjectPath -BundleName $BundleName

Write-Host "`n✓ ArkTS 静态 XTS 测试流程完成" -ForegroundColor Green
```

### 10.9 静态与动态编译对比

| 特性 | 动态模式 | 静态模式 |
|------|---------|---------|
| **类型检查** | 运行时检查 | 编译时严格检查 |
| **any 类型** | 允许 | **禁止** |
| **类型注解** | 可选 | **必需** |
| **字段初始化** | 可延迟 | **必须初始化** |
| **编译速度** | 较快 | 稍慢（额外类型检查） |
| **代码安全性** | 中等 | **高** |
| **Java 环境** | 可选 | **必需** |
| **适用场景** | 快速开发、原型 | 生产代码、严格规范 |

### 10.10 最佳实践

#### 10.10.1 开发流程

```
1. 编写测试代码
   ↓
2. 本地类型检查（IDE 实时提示）
   ↓
3. 静态编译验证
   ↓
4. 修复类型错误（如有）
   ↓
5. 执行测试
   ↓
6. 查看测试报告
```

#### 10.10.2 代码规范

1. **始终使用显式类型注解**
2. **避免使用 any**，使用具体类型或 unknown
3. **初始化所有字段**
4. **使用类型守卫**进行类型收窄
5. **遵循 ArkTS 静态规范**

#### 10.10.3 性能优化

- **增量编译**：使用 `--incremental` 参数加速重复编译
- **并行编译**：使用 `--parallel` 参数利用多核
- **缓存优化**：避免频繁清理构建产物

---

## 十一、版本历史

- **v2.2.0** (2026-02-10): 添加 ArkTS 静态 XTS 编译流程
  - **新增**：第十章 - ArkTS 静态 XTS 编译流程完整指南
  - **新增**：静态编译模式概述和触发条件
  - **新增**：静态编译 PowerShell 脚本模板
  - **新增**：静态类型检查规则和常见错误
  - **新增**：静态与动态编译对比表
  - **改进**：更新模块概述，区分动态和静态模式
  - **改进**：更新工作流概览，展示静态编译流程
  - **改进**：添加编译模式选择指南
  - **验证**：基于 OH_XTS_GENERATOR_ARKTS_STATIC 技能文档

- **v2.1.0** (2025-02-02): 添加命令行编译方式
  - **新增**：3.3.2 节 - 命令行编译方式详细说明
  - **新增**：`hvigorw.bat` 命令行编译完整流程
  - **新增**：编译输出示例和错误处理
  - **新增**：命令行编译优势对比
  - **改进**：更新编译方式选择表格，添加命令行选项
  - **验证**：基于实际项目成功编译（14.3秒，BUILD SUCCESSFUL）
  - **优化**：完整支持从编译到测试的自动化流程

- **v2.0.0** (2025-02-02): 重大更新
  - 重构为完整的编译、测试、结果统计工作流
  - 添加 DevEco Studio IDE 编译方式（推荐）
  - 添加详细的测试执行流程和命令格式
  - 添加完整的测试结果解析方法
  - 添加一键执行所有测试的自动化脚本
  - 添加多个测试套的批量执行和汇总
  - 添加故障排除和最佳实践
  - 基于实际测试经验完善文档

- **v1.0.0** (2025-01-31): 初始版本，Windows 编译工作流
