# Windows 自动化脚本与故障排除

> 本文件从 `build_workflow_windows.md` 第六至九章拆分而来，包含自动化脚本、故障排除和最佳实践。
> **编译流程**: `build_workflow_windows_compile.md`
> **静态编译**: `build_workflow_windows_static.md`

---

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

