# Windows 编译与测试执行

> 本文件从 `build_workflow_windows.md` 第三至五章拆分而来，包含动态模式的编译、测试执行和结果解析。
> **环境准备**: `build_workflow_windows.md` 第二章
> **自动化脚本**: `build_workflow_windows_automation.md`
> **静态编译**: `build_workflow_windows_static.md`

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
cd C:\Users\{username}\DevEcoStudioProjects\MyApplication3

# 执行编译（使用完整路径）
"D:\path\to\hvigor\bin\hvigorw.bat" assembleHap --mode module -p module=entry@ohosTest -p product=default

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
cd C:\Users\{username}\DevEcoStudioProjects\MyApplication3

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

