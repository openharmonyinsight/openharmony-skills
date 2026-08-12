## Phase 9: Test Execution & Failure Analysis

---

### 🔧 工具依赖

本 Phase 需要确认以下工具可用：

```
{skill_root}/scripts/run_xts_test.py
hdc（OpenHarmony Device Connector）
{LOG_ANALYSIS}/scripts/filter_hilog.py          — ohos-issue-xts-log-analysis 日志分析
{LOG_ANALYSIS}/scripts/parallel_decrypt.py       — hilog 加密日志解密
{LOG_ANALYSIS}/scripts/preflight_gate.py         — 报告生成前硬门禁
{LOG_ANALYSIS}/scripts/validate_report.py        — 报告结构校验
{LOG_ANALYSIS}/scripts/extract_imports.py         — 源码 import 提取
{LOG_ANALYSIS}/scripts/map_domain.py             — domain 定界查询
```

> **日志分析 skill 路径**：`{LOG_ANALYSIS} = {skill_root}/../ohos-issue-xts-log-analysis`
>
> 该 skill 提供 hilog 解密、分层过滤、domain 定界、崩溃栈解析、证据链追溯、标准报告生成+校验等能力，用于替代手动 grep/zcat 分析。详见 `{LOG_ANALYSIS}/SKILL.md`。

#### hdc 环境自动检测与配置（步骤 0，必须执行）

**在检查任何前置条件之前，必须先检测并配置 hdc**：

```bash
# 步骤 0a: 检查 hdc 是否已在 PATH 中
if command -v hdc &> /dev/null; then
    echo "✅ hdc is in PATH"
    hdc version
else
    echo "⚠️ hdc not in PATH, trying to add from prebuilts"
    HDC_DIR="{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains"
    if [ -f "$HDC_DIR/hdc" ]; then
        export PATH="$HDC_DIR:$PATH"
        echo "✅ Added $HDC_DIR to PATH"
        hdc version
    else
        echo "❌ hdc not found in prebuilts, searching other paths"
        HDC_FOUND=$(find {OH_ROOT}/prebuilts -name "hdc" -type f 2>/dev/null | head -1)
        if [ -n "$HDC_FOUND" ]; then
            HDC_FOUND_DIR=$(dirname "$HDC_FOUND")
            export PATH="$HDC_FOUND_DIR:$PATH"
            echo "✅ Added $HDC_FOUND_DIR to PATH"
            hdc version
        else
            echo "❌ hdc not found in environment, will skip Phase 9"
        fi
    fi
fi
```

> **关键约束**：
> - hdc 路径通常为 `{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains/hdc`
> - `export PATH` 必须在当前 shell 会话中执行（非子 shell），否则 xdevice 无法继承
> - 如果 hdc 在任何路径都找不到，Phase 9 标记为"跳过 — hdc 不可用"并记录到 session_issues

---

### ⚙️ 按需加载

| 条件 | 加载文件 | 说明 |
|------|---------|------|
| 测试执行命令参考 | `{skill_root}/modules/L3_Validation/executor/test_execution_guide.md` | HAP 安装、xdevice/aa test 命令格式、输出解析（OHOS_REPORT_RESULT）、批量执行、报告生成 |
| Windows + aa test 自动化 | `{skill_root}/modules/L3_Validation/executor/test_workflow_windows_automation.md` | PowerShell 一键执行脚本、故障排除、最佳实践 |
| 失败用例日志分析 | `{skill_root}/../ohos-issue-xts-log-analysis/SKILL.md` | hilog 解密、分层过滤、domain 定界、崩溃栈解析、定界报告 |

---

---

### Phase 执行策略

Phase 9 耗时较长（数百用例约需 15-30 分钟），支持以下执行策略：

| 策略 | 触发条件 | 说明 |
|------|---------|------|
| **执行** | 用户要求真机验证，或自动检测到设备可用 | 完整执行测试并分析失败用例 |
| **后台执行** | 用户希望在等待测试的同时继续其他工作 | 启动后台进程，不阻塞主流程 |
| **跳过** | 用户明确要求跳过，或无设备可用 | 记录跳过原因，直接进入下一阶段 |

> **与 Phase 10 并行**：Phase 9（测试执行）和 Phase 10（覆盖率扫描）均耗时较长且相互独立，可以并行执行。详见下方 9.8 节。

---

### 前置条件

#### 方案 A：WSL 原生执行（推荐，优先检测）

| 条件 | 检查方式 |
|------|---------|
| Phase 8 编译成功 | `{TestName}.hap` 存在于 testcases/ |
| hdc 在 PATH 中或 prebuilts 可用 | `{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains/hdc list targets` 能返回设备 SN |
| WSL Python3 + xdevice 已安装 | `python3 -m pip list \| grep xdevice` |

#### 方案 B：Windows PowerShell 降级方案

| 条件 | 检查方式 |
|------|---------|
| Phase 8 编译成功 | `{TestName}.hap` 存在于 testcases/ |
| 设备通过 USB 连接 Windows | `powershell.exe -Command "& 'D:\\hdc.exe' list targets"` |
| Windows Python + xdevice 已安装 | `powershell.exe -Command "python -m pip list \| Select-String 'xdevice'"` |

**前置检测流程**：先检测方案 A，若 hdc 可用且能发现设备则使用方案 A；否则回退检测方案 B。两者均不满足则跳过本 Phase。

---

### 执行方式

本 Phase 支持三种执行方式，按优先级排序：

| 优先级 | 方式 | 适用场景 | 说明 |
|--------|------|---------|------|
| 1（推荐） | **WSL 原生执行** | WSL + prebuilts hdc 可用 | 直接在 WSL 中运行 xdevice，无需跨系统 |
| 2（降级） | **Windows PowerShell** | WSL hdc 不可用但 Windows 可用 | 通过 PowerShell 调用 Windows 端 xdevice |
| 3（手动） | **手动模式** | 脚本不可用时的兜底 | 手动同步 + 执行 + 解析 |

---

### 9.1 方案 A：WSL 原生执行（推荐）

**适用条件**：`{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains/hdc list targets` 能返回设备 SN。

#### 步骤 0：环境检测

```bash
# 检查 prebuilts hdc 是否可用
HDC_PATH="{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains/hdc"
if $HDC_PATH list targets 2>/dev/null | grep -qv "Empty"; then
    echo "WSL 原生方案可用"
else
    echo "WSL 原生方案不可用，回退到方案 B"
    # 跳转到 9.2
fi
```

#### 步骤 1：设置 hdc 环境并验证设备

```bash
export PATH="{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains:$PATH"

# 验证设备连接
hdc list targets
# 预期输出：设备 SN（如 2f011130375330303010b120b32b2c00）
```

> **注意**：hdc 必须加入 PATH，否则 xdevice 会报 `Can not find hdc or hdc_std environment variable`。

#### 步骤 2：确认 xdevice 已安装

```bash
python3 -m pip list | grep xdevice
# 预期输出：
#   xdevice             0.0.0
#   xdevice-devicetest  0.0.0
#   xdevice-ohos        0.0.0

# 若未安装，先安装：
# cd {OH_ROOT}/out/rk3568/suites/acts/acts && bash run.sh --help
```

#### 步骤 3：确认 user_config.xml 设备 SN 正确

```bash
cat {OH_ROOT}/out/rk3568/suites/acts/acts/user_config.xml
# 确认 <info> 的 sn 属性与 hdc list targets 返回值一致
```

若 SN 不一致，需要更新 user_config.xml 中的 sn 值（但不允许使用 sed 修改，应提醒用户手动修改或通过脚本处理）。

#### 步骤 4：执行测试

**方式 4a：直接执行（用例少时，< 200 个）**

```bash
export PATH="{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains:$PATH"
cd {OH_ROOT}/out/rk3568/suites/acts/acts
python3 -m xdevice run -l {TestName} -t ACTS
```

**方式 4b：后台执行（用例多时，≥ 200 个，避免超时）**

```bash
export PATH="{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains:$PATH"
cd {OH_ROOT}/out/rk3568/suites/acts/acts
nohup python3 -m xdevice run -l {TestName} -t ACTS > /tmp/xts_run.log 2>&1 &
echo "PID: $!"
```

后台执行时，通过以下命令监控进度：

```bash
# 查看已通过/失败数
grep -c "PASSED" /tmp/xts_run.log
grep -c "FAILED" /tmp/xts_run.log

# 查看最新输出
tail -20 /tmp/xts_run.log

# 检查进程是否还在运行
ps aux | grep "python3 -m xdevice" | grep -v grep
```

> **耗时参考**：735 个用例约需 20 分钟（每个用例平均 ~1.6 秒）。设置合理超时等待。

#### 步骤 5：收集结果

```bash
# 报告目录
REPORT_DIR=$(ls -td {OH_ROOT}/out/rk3568/suites/acts/acts/reports/*/ | head -1)

# 读取摘要 XML
cat ${REPORT_DIR}result/summary_report.xml

# 或从 xdevice latest 链接读取
cat ~/.xdevice/latest/summary_report.xml
cat ~/.xdevice/latest/summary.ini
```

#### 步骤 6：解析失败用例

```bash
# 提取所有失败用例
grep 'result="false"' ~/.xdevice/latest/summary_report.xml

# 按测试套分组统计失败数
grep 'result="false"' ~/.xdevice/latest/summary_report.xml | \
    sed 's/.*classname="\([^"]*\)".*/\1/' | sort | uniq -c | sort -rn
```

#### WSL 原生方案优势

| 对比项 | WSL 原生（方案 A） | Windows PowerShell（方案 B） |
|--------|---------------------|-------------------------------|
| hdc 来源 | Linux prebuilts `hdc` | Windows `D:\hdc.exe` |
| xdevice | WSL Python3 原生 | Windows Python |
| 执行命令 | `python3 -m xdevice` | `powershell.exe -Command "..."` |
| 路径处理 | 无需转换 | 需要 WSL↔Windows 路径映射 |
| 同步步骤 | 无需（直接读 acts 目录） | 需要 cp 到 Windows 盘 |
| 复杂度 | **低** | 高 |

---

### 9.2 方案 B：Windows PowerShell 降级方案

**适用条件**：WSL 中 hdc 不可用，但 Windows 端 hdc.exe 和 xdevice 可用。

#### 步骤 1：同步 acts 套件到 Windows 盘

```bash
SUITE_DIR=/mnt/d/acts_suite/acts
mkdir -p "$SUITE_DIR"
rsync -a --delete-before {OH_ROOT}/out/rk3568/suites/acts/acts/ "$SUITE_DIR"
```

#### 步骤 2：通过 PowerShell 执行测试

```bash
powershell.exe -Command "cd D:\acts_suite\acts; python -m xdevice run -l {TestName} -t ACTS"
```

#### 步骤 3：收集并解析结果

```bash
# 找到最新报告目录
ls /mnt/d/acts_suite/acts/reports/ | tail -1

# 解析结果
python {skill_root}/scripts/run_xts_test.py parse \
    --report-dir /mnt/d/acts_suite/acts/reports/{latest_dir} \
    --output .coverage_data/test_execution
```

---

### 9.3 自动模式（run_xts_test.py 脚本）

如果 `run_xts_test.py` 脚本已适配 WSL 原生方案，可使用自动模式：

```bash
python {skill_root}/scripts/run_xts_test.py run \
    --test-name {TestName} \
    --acts-source {OH_ROOT}/out/rk3568/suites/acts/acts \
    --output .coverage_data
```

脚本自动完成：
1. 检测环境（优先 WSL 原生，降级 Windows PowerShell）
2. 执行测试（xdevice 模式）
3. 收集报告文件到 `.coverage_data/test_execution/`（含 `summary_report.xml` + `{module}_module_run.log` + `hilog.*.gz`）
4. 解析 `summary_report.xml`，提取通过/失败/禁用统计
5. 生成 `test_summary.json` 摘要

> **与 §9.4 对接**：脚本收集的 `.coverage_data/test_execution/` 目录可直接作为 ohos-issue-xts-log-analysis 的输入（形态①全量报告）。脚本内置的 hilog 分析使用 `gzip.open`（仅解压非解密），**不要使用其结果**——hilog 加密日志必须由 ohos-issue-xts-log-analysis 的 `parallel_decrypt.py` 解密后再分析。

---

### 9.4 失败用例分析（委托 ohos-issue-xts-log-analysis）

#### Step A：委托日志分析

委托 ohos-issue-xts-log-analysis 执行完整分析流程，skill 会自动识别日志形态并锁定失败用例：

> **日志目录确定**（按执行模式）：
>
> | 执行模式 | 日志目录 | skill 形态 |
> |---------|---------|-----------|
> | §9.1 方案 A/B（xdevice 直接执行） | `{OH_ROOT}/out/rk3568/suites/acts/acts/reports/{timestamp}/log/{TestName}/` | ① 全量报告（含 summary_report.xml） |
> | §9.3 自动模式（run_xts_test.py） | `.coverage_data/test_execution/`（脚本已收集 summary_report.xml + module_run.log + hilog.*.gz） | ① 全量报告 |
> | aa test 模式（hdc shell 直接执行） | hilog 需从设备拉取：`hdc file pull /data/log/ {local_dir}/`；测试结果在 terminal stdout 中 | ④ hilog 目录（无 summary_report.xml） |
>
> **aa test 模式补充**：无 `summary_report.xml`，需先从 terminal stdout 提取失败用例名，再将拉取的 hilog 目录交给 skill：
> ```bash
> # aa test 执行，输出重定向到文件
> hdc shell aa test -b {bundleName} -m entry_test \
>     -s unittest OpenHarmonyTestRunner \
>     -s class {TestSuite} -s timeout {timeout} \
>     > /tmp/aa_test_output.log 2>&1
> # 从 terminal 输出提取汇总和失败用例（格式：OHOS_REPORT_RESULT: stream=Tests run: N, Failure: N, ...）
> grep -E "OHOS_REPORT_RESULT|OHOS_REPORT_STATUS_CODE: -2" /tmp/aa_test_output.log
> # 拉取设备 hilog
> hdc file pull /data/log/ ${LOG_DIR}/
> ```
> 然后将 `${LOG_DIR}` 交给 skill（形态④ hilog 目录）。

```bash
# 日志分析 skill 路径
LOG_ANALYSIS="{skill_root}/../ohos-issue-xts-log-analysis"

# 日志目录（按实际执行模式选择其一）：
#   xdevice 直接执行（§9.1）：  {OH_ROOT}/out/rk3568/suites/acts/acts/reports/{timestamp}/log/{TestName}/
#   自动模式（§9.3 run_xts_test.py）：.coverage_data/test_execution/（含 summary_report.xml + hilog.*.gz）
#   aa test 模式：从设备拉取的 hilog 目录（如 /tmp/aa_test_logs/）
LOG_DIR="{OH_ROOT}/out/rk3568/suites/acts/acts/reports/$(ls {OH_ROOT}/out/rk3568/suites/acts/acts/reports/ | tail -1)/log/{TestName}/"

# 1. hilog 解密（硬门禁，禁 gunzip/strings）
python3 ${LOG_ANALYSIS}/scripts/check_dict.py ${LOG_DIR}
python3 ${LOG_ANALYSIS}/scripts/parallel_decrypt.py ${LOG_DIR}

# 2. 硬门禁检查（未解密则只输出桩报告，禁止生成定界结论）
python3 ${LOG_ANALYSIS}/scripts/preflight_gate.py ${LOG_DIR}

# 3. 分层过滤 + Hypium 时间窗提取（每个失败用例）
python3 ${LOG_ANALYSIS}/scripts/filter_hilog.py \
    -i ${LOG_DIR}_parsed/ --extract-hypium --testcase "{TestCaseName}" --json

# 4. 源码 → domain 证据链追溯
python3 ${LOG_ANALYSIS}/scripts/extract_imports.py {测试源码路径}
python3 ${LOG_ANALYSIS}/scripts/map_domain.py "@ohos.xxx"
# NAPI .so 追溯：
python3 ${LOG_ANALYSIS}/scripts/trace_napi_chain.py {测试文件} --xts-root {XTS根} --format chain

# 5. domain 分层过滤（用证据链查到的 domain）
python3 ${LOG_ANALYSIS}/scripts/filter_hilog.py \
    -i ${LOG_DIR}_parsed/ -d {domain} \
    --time-start {t_start} --time-end {t_end} --json

# 6. 生成定界报告（AI 根据脚本输出填写 2 章节标准报告）
#    报告路径：${LOG_DIR}/XTS_Analysis_Report_YYYYMMDD.md

# 7. 报告校验（硬门禁，生成后必跑）
python3 ${LOG_ANALYSIS}/scripts/validate_report.py \
    "${LOG_DIR}/XTS_Analysis_Report_YYYYMMDD.md" \
    "${LOG_DIR}/module_run.log" \
    "${LOG_DIR}_parsed/"
```

**skill 产出**：`{LOG_DIR}/XTS_Analysis_Report_YYYYMMDD.md`

报告结构（2 章节标准格式）：
- **一、hilog 日志用例详情**（每个失败用例 6 段落）：
  1. 基本信息（用例名/结果/耗时/message）
  2. 时间窗提取（hilog 起止行号/消耗时间）
  3. 源码→领域证据链（import→@ohos 模块→子系统→domain→日志行）
  4. 关键日志片段（分层标记 [主]/[P1]/[P2]/[P3]）
  5. 源码定位与分析（行号/调用栈）
  6. 问题定界（测试侧 vs 系统侧）
- **二、总结**：测试侧/系统侧分类 + 定界结论表格 + 建议流转

> **Windows 环境**：若 `python3` 是 Microsoft Store 桩程序（静默退出零输出），改用启动器：
> `cmd /c ${LOG_ANALYSIS}/scripts/run.cmd filter_hilog -i ...` / `run.cmd preflight_gate ...` / `run.cmd validate_report ...`

#### Step B：基于定界报告自动修复

读取 skill 产出的定界结论，按定界类别分类处理：

| 定界类别 | 说明 | 修复策略 | 修复 Phase |
|---------|------|---------|-----------|
| **测试侧-基础设施** | 路由未注册/done()未调用/控件 ID 不匹配/超时 | **自动修复** | Phase 6/5 |
| **测试侧-逻辑错误** | 参数传错/预期值写错/异步处理错误 | **自动修复** | Phase 5 |
| **系统侧-接口缺陷** | 断言失败，实际值与 .d.ts 声明不符 | **不修改**，标注 `[疑似接口缺陷]` | — |
| **系统侧-崩溃** | SIGSEGV/cppcrash/jscrash | **不修改**，记录崩溃栈 | — |
| **系统侧-能力不支持** | 801 能力不支持 | 检查 801 防护是否到位 | — |

**自动修复回退路径**（测试侧问题）：

| 失败模式 | 修复 Phase | 修复方式 |
|---------|-----------|---------|
| 页面路由未注册 | Phase 6 | 补注册 main_pages.json → Phase 8 重编 |
| done() 未调用 | Phase 5 | 修复异步回调 done() → Phase 7 → Phase 8 |
| 控件 ID 不匹配 | Phase 5A + 5B | 统一 Demo 与 UiTest 控件 ID → Phase 7 → Phase 8 |
| 参数传错 | Phase 5 | 修正参数值（对照 .d.ts 签名） → Phase 7 → Phase 8 |
| 预期值写错 | Phase 5 | 修正预期值（对照 .d.ts 声明） → Phase 7 → Phase 8 |
| 异步处理错误 | Phase 5 | 修复 Promise/await 逻辑 → Phase 7 → Phase 8 |
| beforeAll/beforeEach 初始化异常 | Phase 5 | 修复前置钩子初始化逻辑 → Phase 7 → Phase 8 |
| 超时 | Phase 5 | 调整 sleep/等待逻辑 → Phase 7 → Phase 8 |
| Demo 页面 bug | Phase 5A | 修改 Demo 页面代码 → Phase 7 → Phase 8 |

> **自动修复流程**：修复 → Phase 7 验证 → Phase 8 重编 → 再次 Phase 9 执行
>
> **系统侧问题处理**：记录实际值 vs 预期值差异，标注 `[疑似接口缺陷]`，汇报用户确认后才可修改。禁止修改测试代码来迎合错误行为。
>
> **旧用例失败**（非本次生成）：记录但不修复，标注"已有缺陷"
>
> **关键原则**：断言失败说明实际行为与预期不符。预期值来源于 .d.ts 接口声明和官方文档，具有权威性。通过 ohos-issue-xts-log-analysis 的 domain 定界 + 崩溃栈解析 + 证据链追溯，可精准区分测试侧与系统侧，避免误修复。

---

### 9.5 输出

| 文件 | 路径 | 内容 |
|------|------|------|
| 测试摘要 | `.coverage_data/test_execution/test_summary.json` | 通过/失败/禁用统计 + 失败列表 |
| **定界报告** | `{LOG_DIR}/XTS_Analysis_Report_YYYYMMDD.md` | ohos-issue-xts-log-analysis 产出的 2 章节标准报告（含测试侧/系统侧定界结论） |
| 失败分析 | `.coverage_data/test_execution/failure_analysis.md` | 基于定界报告的修复决策记录 + 自动修复执行情况 |
| 原始 XML | `~/.xdevice/latest/summary_report.xml` | xdevice 原始 XML 报告 |
| 执行摘要 | `~/.xdevice/latest/summary.ini` | 平台/设备/耗时等元信息 |
| 报告 HTML | `~/.xdevice/latest/summary_report.html` | 可视化测试报告 |
| 模块日志 | `{reports_dir}/log/{TestName}/module_run.log` | 测试执行器日志 |
| 解密 hilog | `{LOG_DIR}_parsed/hilog.*.txt` | parallel_decrypt.py 解密后的明文 hilog |
| 完整日志 | `/tmp/xts_run.log`（后台执行时） | xdevice 完整控制台输出 |

---

### 9.6 结果判定

| 结果 | 操作 |
|------|------|
| **全部通过** | ✅ Phase 9 完成，进入下一阶段 |
| **有失败，但全部是旧用例** | ✅ Phase 9 完成（标注旧用例缺陷），进入下一阶段 |
| **新生成的用例失败（测试侧问题）** | ⚠️ 按 §9.4 Step B 自动修复 → Phase 7 验证 → Phase 8 重编 → 再次 Phase 9 |
| **新生成的用例失败（系统侧问题）** | 📋 标注 `[疑似接口缺陷]`，记录实际值 vs 预期值，汇报用户确认，不自动修改 |
| **混合失败（测试侧+系统侧）** | ⚠️ 测试侧自动修复 + 系统侧记录 → 重测后仅系统侧失败留存 → 汇报用户 |
| **无法连接设备** | ⏭️ 跳过 Phase 9，记录原因，进入下一阶段 |

> **测试侧 vs 系统侧判定依据**：由 ohos-issue-xts-log-analysis 的定界报告决定。测试侧 = 测试代码缺陷（路由/done()/控件ID/参数/异步/超时）；系统侧 = 接口缺陷（断言失败/崩溃/能力不支持）。

---

### 9.7 环境支持矩阵

| 环境 | 能否执行 | 推荐方案 |
|------|---------|---------|
| WSL + prebuilts hdc 可用 | ✅ | **方案 A：WSL 原生执行**（直接 `python3 -m xdevice`） |
| WSL + Windows USB 设备（hdc 不可用） | ✅ | 方案 B：Windows PowerShell 降级 |
| Linux 原生 + USB 设备 | ✅ | 方案 A：直接 `python -m xdevice` |
| Windows 原生 | ✅ | 直接 `run.bat` 或 `python -m xdevice` |
| Linux 远程服务器（无设备） | ❌ | 跳过，仅编译验证 |

---

### 9.8 与 Phase 10 并行执行

Phase 9（设备测试执行）和 Phase 10（覆盖率扫描）**互相独立、无依赖**，可以并行执行以节省总耗时。

#### 并行条件

| 条件 | Phase 9 | Phase 10 |
|------|---------|---------|
| 依赖 | 编译产物（HAP）+ 设备 | 编译产物（源码）+ APICoverageDetector |
| 耗时 | 15-30 分钟（取决于用例数） | 5-15 分钟（取决于扫描范围） |
| 资源 | 设备 + hdc | CPU + 扫描工具 |

#### 并行执行方式

```bash
# 终端 1：启动 Phase 9 后台测试执行
export PATH="{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains:$PATH"
cd {OH_ROOT}/out/rk3568/suites/acts/acts
nohup python3 -m xdevice run -l {TestName} -t ACTS > /tmp/xts_run.log 2>&1 &

# 终端 2（或同一终端）：启动 Phase 10 覆盖率扫描
python {skill_root}/scripts/async_coverage_scan.py start
```

在 Agent 流程中，并行执行意味着：
1. 先启动 Phase 9 后台进程
2. 立即进入 Phase 10 执行覆盖率扫描
3. Phase 10 完成后，回来检查 Phase 9 结果
4. 汇总两阶段结果

> **用户可控**：如果用户不需要真机验证或覆盖率扫描，可跳过任一阶段。跳过时记录原因即可。

### 统计集成（Phase 完成后执行）

```bash
# 记录设备测试情况
python {skill_root}/scripts/adoption_stats.py --action record_phase9 \
  --test-report {测试报告路径} \
  --output-dir {output_dir}
```
