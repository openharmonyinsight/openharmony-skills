# 测试执行与结果解析指南

> **编译流程**: ../builder/build_workflow_windows_compile.md
> **静态编译**: ../builder/build_workflow_windows_static.md
> **自动化脚本**: test_workflow_windows_automation.md（同目录）

---

## 一、执行方式选择

| 方式 | 适用场景 | 命令 | 输出格式 |
|------|---------|------|---------|
| **xdevice（WSL 原生）** | 批量执行多套、需标准化 XML 报告、CI/CD 集成、需自动收集 hilog.gz | `python3 -m xdevice run` | summary_report.xml |
| **aa test（hdc shell 通用）** | 无 xdevice 环境、快速验证单套/单用例、HAP 自动安装、无 acts 目录、调试定位 | `hdc shell aa test` | terminal stdout（OHOS_REPORT_RESULT） |

> 命令语法跨平台一致（hdc shell 在 WSL/Linux/Windows 下相同），但 hdc 版本、输出捕获方式、路径格式需按平台适配。

---

## 二、HAP 安装

### 2.1 hdc install（手动安装）

```bash
# WSL/Linux
hdc install {项目路径}/entry/build/default/outputs/ohosTest/entry-ohosTest-signed.hap

# Windows PowerShell
hdc install entry\build\default\outputs\ohosTest\entry-ohosTest-signed.hap

# 静态测试套
hdc install entry\build\default\outputs\default\entry-default-signed.hap
```

### 2.2 aa test 自动安装（推荐）

`hdc shell aa test` 命令会自动安装 HAP，无需预先 `hdc install`：

```bash
hdc shell aa test -b {BundleName} -m entry_test \
    -s unittest OpenHarmonyTestRunner -s class {TestSuite} -s timeout {Timeout}
```

> aa test 自动安装是推荐方式——一步完成安装+执行，避免版本不一致问题。

---

## 三、WSL xdevice 执行

> 完整执行步骤编排见 Phase 9 §9.1（环境检测→执行→收集→解析）。本节为命令格式参考。

### 3.1 环境准备

```bash
# hdc 路径
export PATH="{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains:$PATH"
# 必须在当前 shell 会话执行（非子 shell），否则 xdevice 无法继承

# 验证设备
hdc list targets
# 预期输出：设备 SN（如 2f011130375330303010b120b32b2c00）

# 确认 xdevice 已安装
python3 -m pip list | grep xdevice
# 预期：xdevice / xdevice-devicetest / xdevice-ohos

# 确认 user_config.xml 设备 SN 正确
cat {OH_ROOT}/out/rk3568/suites/acts/acts/user_config.xml
# <info> 的 sn 属性需与 hdc list targets 一致
```

### 3.2 执行命令

```bash
# 直接执行（用例少时，< 200 个）
cd {OH_ROOT}/out/rk3568/suites/acts/acts
python3 -m xdevice run -l {TestName} -t ACTS

# 后台执行（用例多时，≥ 200 个）
nohup python3 -m xdevice run -l {TestName} -t ACTS > /tmp/xts_run.log 2>&1 &
echo "PID: $!"
```

后台执行监控：
```bash
grep -c "PASSED" /tmp/xts_run.log    # 已通过数
grep -c "FAILED" /tmp/xts_run.log    # 已失败数
tail -20 /tmp/xts_run.log            # 最新输出
```

### 3.3 输出

| 产物 | 路径 | 内容 |
|------|------|------|
| 报告目录 | `{acts}/reports/{timestamp}/` | 完整报告 |
| 摘要 XML | `~/.xdevice/latest/summary_report.xml` | testsuite/testcase 节点，result="true/false" |
| 模块日志 | `log/{TestName}/module_run.log` | 测试执行器日志 |
| hilog | `log/{TestName}/hilog_*/hilog.*.gz` | 加密 hilog（需 parallel_decrypt.py 解密） |

---

## 四、aa test 执行

### 4.0 适用场景

| 场景 | 说明 |
|------|------|
| **无 xdevice 环境** | 设备已连接但 WSL/Windows 未安装 xdevice，aa test 只需 hdc 可用 |
| **HAP 自动安装** | aa test 命令自动安装 HAP，无需预先 `hdc install` |
| **快速验证单个测试套** | 不需完整 XML 报告，只需 terminal 输出的 pass/fail 统计 |
| **调试单个用例** | `-s class` 精确到单个用例（如 `ActsBufferTest#testCase1`），快速定位问题 |
| **无 acts 套件目录** | xdevice 需要 acts 目录结构，aa test 直接在设备端执行 |
| **ExtensionAbility 测试** | 某些 ExtensionAbility 测试需 aa test 方式拉起 |
| **幂等性验证** | 重复执行单个用例验证稳定性，无需每次重新安装 |

### 4.1 获取测试套信息

#### 方法1：查看 List.test.ets

```bash
# WSL/Linux
cat entry/src/ohosTest/ets/test/List.test.ets

# Windows PowerShell
Get-Content "entry\src\ohosTest\ets\test\List.test.ets"
```

示例输出：
```typescript
import abilityTest from './Ability.test';
import BufferTest from './buffer/Buffer1.test';

export default function testsuite() {
  abilityTest();
  BufferTest();
}
```

#### 方法2：查找 describe 名称

```bash
# WSL/Linux
grep -rn 'describe(' entry/src/ohosTest/ets/test/**/*.test.ets

# Windows PowerShell
Select-String -Path "entry\src\ohosTest\ets\test\**\*.test.ets" -Pattern "describe\(" -Context 0,0
```

### 4.2 命令格式

```bash
# 完整命令格式
hdc shell aa test -b <BundleName> -m <ModuleName> \
    -s unittest <TestRunner> \
    -s class <TestSuite> \
    -s timeout <Timeout>

# 参数说明
# -b <BundleName>           : 应用包名（从 AppScope/app.json5 获取）
# -m <ModuleName>           : 模块名（测试模块通常是 entry_test）
# -s unittest <TestRunner>  : 测试运行器（通常是 OpenHarmonyTestRunner）
# -s class <TestSuite>      : 测试套名称（describe 的第一个参数）
# -s timeout <Timeout>      : 超时时间（毫秒）
```

实际执行示例：
```bash
hdc shell aa test -b com.example.myapplication -m entry_test \
    -s unittest OpenHarmonyTestRunner \
    -s class ActsBufferNewTest -s timeout 15000
```

获取 BundleName：从 `AppScope/app.json5` 的 `app.bundleName` 字段获取。

### 4.3 WSL 下的执行

```bash
# WSL 直接执行（hdc 来自 prebuilts，已在 §3.1 设置 PATH）
hdc shell aa test -b {bundleName} -m entry_test \
    -s unittest OpenHarmonyTestRunner \
    -s class {TestSuite} -s timeout {timeout} \
    > /tmp/aa_test_output.log 2>&1
```

与 Windows PowerShell 的差异：

| 差异点 | WSL/Linux | Windows PowerShell |
|--------|-----------|-------------------|
| hdc 可执行文件 | `hdc`（prebuilts/linux） | `hdc.exe`（prebuilts/windows） |
| 输出捕获 | `> /tmp/xxx.log 2>&1` | `$Output = Invoke-Expression $Command` |
| 路径格式 | `/tmp/` | `C:\` |
| 命令语法 | 相同（hdc shell 跨平台） | 相同 |

### 4.4 批量执行

```bash
# WSL/Linux：批量执行所有测试套
BUNDLE_NAME="com.example.myapplication"
MODULE_NAME="entry_test"
TEST_RUNNER="OpenHarmonyTestRunner"
TIMEOUT=15000

# 测试套列表（从 List.test.ets 获取）
TEST_SUITES=("ActsAbilityTest" "bufferTest" "ActsBufferTest" "ActsBufferNewTest")

for suite in "${TEST_SUITES[@]}"; do
    echo "=== Executing: $suite ==="
    hdc shell aa test -b $BUNDLE_NAME -m $MODULE_NAME \
        -s unittest $TEST_RUNNER -s class $suite -s timeout $TIMEOUT \
        2>&1 | tee -a /tmp/aa_test_all.log
done
```

```powershell
# Windows PowerShell：批量执行（详见 test_workflow_windows_automation.md 一键脚本）
$TestSuites = @("ActsAbilityTest", "bufferTest", "ActsBufferTest", "ActsBufferNewTest")
foreach ($suite in $TestSuites) {
    $Output = Invoke-Expression "hdc shell aa test -b $BundleName -m $ModuleName -s unittest $TestRunner -s class $suite -s timeout $Timeout"
    # 解析结果...
}
```

---

## 五、结果解析

### 5.1 xdevice 输出（summary_report.xml）

XML 结构：
```xml
<testsuite name="ActsBufferNewTest" tests="13" failures="5" disabled="0" time="12.5">
  <testcase name="testBufferFrom20009" classname="ActsBufferNewTest" status="run" result="true" time="1.2" message=""/>
  <testcase name="testBufferFrom20010" classname="ActsBufferNewTest" status="run" result="false" time="0.0" message="assertEqual failed"/>
</testsuite>
```

提取失败用例：
```bash
# 提取所有失败用例
grep 'result="false"' ~/.xdevice/latest/summary_report.xml

# 按测试套分组统计失败数
grep 'result="false"' ~/.xdevice/latest/summary_report.xml | \
    sed 's/.*classname="\([^"]*\)".*/\1/' | sort | uniq -c | sort -rn
```

### 5.2 aa test 输出（OHOS_REPORT_RESULT）

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

提取汇总信息：
```bash
# WSL/Linux：从输出文件提取
grep -E "OHOS_REPORT_RESULT|OHOS_REPORT_CODE" /tmp/aa_test_output.log
# 输出：OHOS_REPORT_RESULT: stream=Tests run: 13, Failure: 5, ...

# 正则提取数值
grep "OHOS_REPORT_RESULT" /tmp/aa_test_output.log | \
    sed 's/.*Tests run: \([0-9]*\), Failure: \([0-9]*\), Error: \([0-9]*\), Pass: \([0-9]*\), Ignore: \([0-9]*\).*/Total:\1 Failed:\2 Errors:\3 Passed:\4 Ignored:\5/'
```

```powershell
# Windows PowerShell
$ResultLine = $TestOutput | Select-String "OHOS_REPORT_RESULT: stream=" | Select-Object -Last 1
if ($ResultLine -match 'Tests run: (\d+), Failure: (\d+), Error: (\d+), Pass: (\d+), Ignore: (\d+)') {
    $Total = [int]$matches[1]
    $Failed = [int]$matches[2]
    $Passed = [int]$matches[4]
}
```

提取失败用例详情：
```bash
# WSL/Linux：提取失败用例名（OHOS_REPORT_STATUS_CODE: -2 的上下文中有 test=用例名）
grep -B5 "OHOS_REPORT_STATUS_CODE: -2" /tmp/aa_test_output.log | grep "test="
```

```powershell
# Windows PowerShell
$FailedTests = $TestOutput | Select-String "OHOS_REPORT_STATUS_CODE: -2" -Context 5,0
foreach ($failed in $FailedTests) {
    $context = $failed.Context.PreContext | Select-String "test=" | Select-Object -First 1
    if ($context -match 'test=([^\s]+)') {
        Write-Host "✗ $($matches[1])"
    }
}
```

### 5.3 生成报告

```bash
# WSL/Linux：生成 JSON 格式报告
python3 -c "
import json, re, sys

output = open('/tmp/aa_test_output.log').read()
match = re.search(r'Tests run: (\d+), Failure: (\d+), Error: (\d+), Pass: (\d+), Ignore: (\d+)', output)
if match:
    report = {
        'total': int(match.group(1)),
        'failed': int(match.group(2)),
        'errors': int(match.group(3)),
        'passed': int(match.group(4)),
        'ignored': int(match.group(5)),
    }
    print(json.dumps(report, indent=2))
"
```

```powershell
# Windows PowerShell：生成 JSON 格式报告
$Report = @{
    timestamp  = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    bundleName = $BundleName
    summary    = @{ totalTests = $TotalTests; totalPassed = $TotalPassed; totalFailed = $TotalFailed }
}
$Report | ConvertTo-Json -Depth 4 | Out-File "test_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').json" -Encoding UTF8
```
