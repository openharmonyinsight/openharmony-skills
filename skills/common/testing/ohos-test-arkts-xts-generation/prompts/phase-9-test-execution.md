## Phase 9: Test Execution & Failure Analysis

---

### 🔧 工具依赖

本 Phase 需要确认以下工具可用：

```
{skill_root}/scripts/run_xts_test.py
```

---

### ⚙️ 按需加载

无。

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有 L2_Generation 模块
```

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
rm -rf /mnt/d/acts_suite/acts/
cp -r {OH_ROOT}/out/rk3568/suites/acts/acts/ /mnt/d/acts_suite/acts/
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
2. 执行测试
3. 收集报告文件到 `.coverage_data/test_execution/`
4. 解析 `summary_report.xml`，提取通过/失败/禁用统计
5. 分析失败用例，生成 `failure_analysis.md`

---

### 9.4 失败用例分析

#### 分析流程

对每个失败用例（`status="run"` 且 `result="false"`，排除 `status="disable"`），按以下流程分析：

**Step A：检查 XML 报告**

从 `summary_report.xml` 提取：
- `time` 值（0.0 表示 done() 未调用）
- `message` 值（错误消息）

**Step B：检查 hilog**

从报告目录中的 `.gz` hilog 文件搜索失败用例：

```bash
HILOG_DIR=$(ls -td {OH_ROOT}/out/rk3568/suites/acts/acts/reports/*/ | head -1)log/{TestName}/hilog_*/
zcat ${HILOG_DIR}hilog.*.gz | grep "{TestCaseName}"
```

关注以下关键行：
- `[Hypium]start running case` — 用例开始
- `[Hypium]{name} specStart start print success` — spec 开始
- `REPORT_STATUS_CODE: 0` — 用例通过（PASS）
- `REPORT_STATUS_CODE: 2` — 用例失败（FAIL）
- `[Hypium][pass]{name}` — 明确通过
- `[Hypium][fail]{name}` — 明确失败
- `{name} specDone end print success` — spec 正常结束
- `can't find this page` — **路由注册遗漏**（Phase 6 未注册 Demo 页面）
- `push page error` / `replaceUrl` 错误 — 页面跳转失败

**Step C：判定失败模式**

| 模式 | 特征 | 根因 | 修复建议 |
|------|------|------|---------|
| **页面路由未注册** | hilog: `can't find this page {path}`, `error in beforeEach` | Phase 6 遗漏：Demo 页面未加入 main_pages.json | **回到 Phase 6** 补注册路由 → 重新编译 |
| **Empty Text / Empty JSON** | message: `Unexpected Text in JSON: Empty Text` | Demo 页面渲染为空（通常也因路由未注册） | 检查 Demo 页面是否存在且已注册 |
| **beforeEach 错误** | message: `error in beforeEach function`, time≈0 | beforeEach 中路由跳转失败 | 同"页面路由未注册" |
| **done() 未调用** | time=0, 无 message, 有 specStart 无 specDone | 异步回调中 done() 未执行，或 JS 异常被吞掉 | 检查 async 函数是否有 try-catch 吞掉异常 |
| **断言失败** | REPORT_STATUS_CODE: 2, hilog 有 assertEqual 相关日志 | 预期值与实际值不匹配 | 检查 Inspector 返回值格式是否变化 |
| **控件 ID 未找到** | hilog 有 "getInspectorByKey" 但返回空 | Demo 页面未正确设置 .key() | 检查 Demo 页面控件 ID 与测试代码一致 |
| **超时** | 用例执行超过 180s | 异步操作未完成 | 检查 sleep 时间或回调等待逻辑 |
| **已知 blocked** | message="error_msg: mark blocked" | 已知缺陷，被主动禁用 | 无需修复，记录即可 |

> **最高频失败模式**：根据实践经验，"页面路由未注册"是最常见的失败原因。hilog 中的 `can't find this page {PageName}` 是明确诊断信号。修复方式：在 `main_pages.json` 中添加缺失的路由。

**Step D：区分"旧用例失败"和"新生成用例失败"**

- 旧用例失败（非本次生成）：记录但不修复，标注"已有缺陷"
- 新生成用例失败：需要定位并修复，回到对应 Phase 修正

**Step E：失败修复回退路径**

| 失败模式 | 修复 Phase | 说明 |
|---------|-----------|------|
| 页面路由未注册 | Phase 6 | 补注册 main_pages.json → Phase 8 重编 |
| Demo 页面 bug | Phase 5A | 修改 Demo 页面代码 → Phase 7 → Phase 8 |
| 测试代码 bug | Phase 5 | 修改测试代码 → Phase 7 → Phase 8 |
| Inspector 值变化 | Phase 4 | 调整预期值 → Phase 5 → Phase 7 → Phase 8 |

---

### 9.5 输出

| 文件 | 路径 | 内容 |
|------|------|------|
| 测试摘要 | `.coverage_data/test_execution/test_summary.json` | 通过/失败/禁用统计 + 失败列表 |
| 失败分析 | `.coverage_data/test_execution/failure_analysis.md` | 每个失败用例的详细分析 + 根因推断 |
| 原始 XML | `~/.xdevice/latest/summary_report.xml` | xdevice 原始 XML 报告 |
| 执行摘要 | `~/.xdevice/latest/summary.ini` | 平台/设备/耗时等元信息 |
| 报告 HTML | `~/.xdevice/latest/summary_report.html` | 可视化测试报告 |
| 模块日志 | `{reports_dir}/log/{TestName}/module_run.log` | 测试执行器日志 |
| 完整日志 | `/tmp/xts_run.log`（后台执行时） | xdevice 完整控制台输出 |

---

### 9.6 结果判定

| 结果 | 操作 |
|------|------|
| **全部通过** | ✅ Phase 9 完成，进入下一阶段 |
| **有失败，但全部是旧用例** | ✅ Phase 9 完成（标注旧用例缺陷），进入下一阶段 |
| **新生成的用例失败** | ⚠️ 分析失败原因 → 按回退路径修复 → 重新编译 → 再次 Phase 9 |
| **无法连接设备** | ⏭️ 跳过 Phase 9，记录原因，进入下一阶段 |

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
