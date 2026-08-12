## Phase 8: Test Execution & Failure Analysis

---

### 🔧 工具依赖

本 Phase 需要确认以下工具可用：

```
hdc（设备连接工具）
xdevice（测试执行框架）
```

> **注意**：`run_xts_test.py` 已复制到 CAPI 技能目录，配置路径已适配为 `.oh-capi-xts-config.json`。

---

### ⚙️ 按需加载

无。

---

### 🚫 Do NOT Load

```
所有 modules/L2_Generation 模块
```

---

### Phase 执行策略

Phase 8 耗时较长（数百用例约需 15-30 分钟），支持以下执行策略：

| 策略 | 触发条件 | 说明 |
|------|---------|------|
| **执行** | 用户要求真机验证，或自动检测到设备可用 | 完整执行测试并分析失败用例 |
| **后台执行** | 用户希望在等待测试的同时继续其他工作 | 启动后台进程，不阻塞主流程 |
| **跳过** | 用户明确要求跳过，或无设备可用 | 记录跳过原因，直接进入下一阶段 |

---

### 前置条件

#### 方案 A：WSL 原生执行（推荐，优先检测）

| 条件 | 检查方式 |
|------|---------|
| Phase 7 编译成功 | `{TestName}.hap` 存在于 testcases/ |
| hdc 在 PATH 中或 prebuilts 可用 | `{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains/hdc list targets` 能返回设备 SN |
| WSL Python3 + xdevice 已安装 | `python3 -m pip list \| grep xdevice` |

#### 方案 B：Windows PowerShell 降级方案

| 条件 | 检查方式 |
|------|---------|
| Phase 7 编译成功 | `{TestName}.hap` 存在于 testcases/ |
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

### 8.1 方案 A：WSL 原生执行（推荐）

**适用条件**：`{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains/hdc list targets` 能返回设备 SN。

#### 步骤 0：环境检测

```bash
HDC_PATH="{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains/hdc"
if $HDC_PATH list targets 2>/dev/null | grep -qv "Empty"; then
    echo "WSL 原生方案可用"
else
    echo "WSL 原生方案不可用，回退到方案 B"
fi
```

#### 步骤 1：设置 hdc 环境并验证设备

```bash
export PATH="{OH_ROOT}/prebuilts/ohos-sdk/linux/26/toolchains:$PATH"
hdc list targets
```

#### 步骤 2：确认 xdevice 已安装

```bash
python3 -m pip list | grep xdevice
# 若未安装：cd {OH_ROOT}/out/rk3568/suites/acts/acts && bash run.sh --help
```

#### 步骤 3：确认 user_config.xml 设备 SN 正确

```bash
cat {OH_ROOT}/out/rk3568/suites/acts/acts/user_config.xml
# 确认 <info> 的 sn 属性与 hdc list targets 返回值一致
```

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

后台执行时监控进度：

```bash
grep -c "PASSED" /tmp/xts_run.log
grep -c "FAILED" /tmp/xts_run.log
tail -20 /tmp/xts_run.log
ps aux | grep "python3 -m xdevice" | grep -v grep
```

#### 步骤 5：收集结果

```bash
REPORT_DIR=$(ls -td {OH_ROOT}/out/rk3568/suites/acts/acts/reports/*/ | head -1)
cat ${REPORT_DIR}result/summary_report.xml
cat ~/.xdevice/latest/summary_report.xml
cat ~/.xdevice/latest/summary.ini
```

#### 步骤 6：解析失败用例

```bash
grep 'result="false"' ~/.xdevice/latest/summary_report.xml
grep 'result="false"' ~/.xdevice/latest/summary_report.xml | \
    sed 's/.*classname="\([^"]*\)".*/\1/' | sort | uniq -c | sort -rn
```

---

### 8.2 方案 B：Windows PowerShell 降级方案

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
ls /mnt/d/acts_suite/acts/reports/ | tail -1

# 使用脚本解析结果
python {skill_root}/scripts/run_xts_test.py parse \
    --report-dir /mnt/d/acts_suite/acts/reports/{latest_dir} \
    --output .coverage_data/test_execution
```

---

### 8.3 失败用例分析

#### 分析流程

对每个失败用例（`status="run"` 且 `result="false"`，排除 `status="disable"`），按以下流程分析：

**Step A：检查 XML 报告** — 从 `summary_report.xml` 提取 time 值和 message 值

**Step B：检查 hilog**

```bash
HILOG_DIR=$(ls -td {OH_ROOT}/out/rk3568/suites/acts/acts/reports/*/ | head -1)log/{TestName}/hilog_*/
zcat ${HILOG_DIR}hilog.*.gz | grep "{TestCaseName}"
```

关注关键行：
- `[Hypium]start running case` — 用例开始
- `REPORT_STATUS_CODE: 0` — 用例通过（PASS）
- `REPORT_STATUS_CODE: 2` — 用例失败（FAIL）
- `can't find this page` — 路由注册遗漏

**Step C：判定失败模式**

| 模式 | 特征 | 根因 | 修复建议 |
|------|------|------|---------|
| **undefined reference** | 编译阶段已报错，设备上 crash | N-API 封装调用了 .h 中不存在的函数 | 回到 Phase 5 修正 NapiTest.cpp |
| **is not a function** | ETS 侧调用报错 | `napi_property_descriptor` 中缺少函数注册 | 运行 `auto_fix_napi_triple.sh` |
| **type mismatch** | 参数传递错误 | C++ / d.ts / ETS 类型不一致 | 回到 Phase 6 三重校验 |
| **null pointer crash** | SIGSEGV | N-API 封装未处理 napi_null 输入 | 回到 Phase 5 添加 null 检查 |
| **memory leak** | 内存持续增长 | `napi_finalize` 未注册或未释放 C 资源 | 回到 Phase 5 检查 finalize 回调 |
| **done() 未调用** | time=0, 无 message | 异步回调中 done() 未执行 | 检查 async 函数是否有 try-catch 吞掉异常 |
| **超时** | 用例执行超过 180s | 异步操作未完成 | 检查 sleep 时间或回调等待逻辑 |

**Step D：区分"旧用例失败"和"新生成用例失败"**

- 旧用例失败（非本次生成）：记录但不修复，标注"已有缺陷"
- 新生成用例失败：需要定位并修复，回到对应 Phase 修正

**Step E：失败修复回退路径**

| 失败模式 | 修复 Phase | 说明 |
|---------|-----------|------|
| N-API 函数注册错误 | Phase 6 | 运行 auto_fix → 重新编译 |
| N-API 封装代码 bug | Phase 5 | 修改 NapiTest.cpp → Phase 6 → Phase 7 |
| ETS 测试代码 bug | Phase 5 | 修改 .test.ets → Phase 6 → Phase 7 |
| 设计文档错误 | Phase 4 | 调整设计 → Phase 5 → Phase 6 → Phase 7 |

---

### 8.4 输出

| 文件 | 路径 | 内容 |
|------|------|------|
| 测试摘要 | `.coverage_data/test_execution/test_summary.json` | 通过/失败/禁用统计 + 失败列表 |
| 失败分析 | `.coverage_data/test_execution/failure_analysis.md` | 每个失败用例的详细分析 + 根因推断 |
| 原始 XML | `~/.xdevice/latest/summary_report.xml` | xdevice 原始 XML 报告 |
| 执行摘要 | `~/.xdevice/latest/summary.ini` | 平台/设备/耗时等元信息 |

---

### 8.5 结果判定

| 结果 | 操作 |
|------|------|
| **全部通过** | Phase 8 完成，进入 Phase 9 |
| **有失败，但全部是旧用例** | Phase 8 完成（标注旧用例缺陷），进入 Phase 9 |
| **新生成的用例失败** | 分析失败原因 → 按回退路径修复 → 重新编译 → 再次执行 |
| **无法连接设备** | 跳过 Phase 8，记录原因，进入 Phase 9 |

---

### 8.6 环境支持矩阵

| 环境 | 能否执行 | 推荐方案 |
|------|---------|---------|
| WSL + prebuilts hdc 可用 | ✅ | **方案 A：WSL 原生执行** |
| WSL + Windows USB 设备（hdc 不可用） | ✅ | 方案 B：Windows PowerShell 降级 |
| Linux 原生 + USB 设备 | ✅ | 方案 A：直接 `python -m xdevice` |
| Windows 原生 | ✅ | 直接 `run.bat` 或 `python -m xdevice` |
| Linux 远程服务器（无设备） | ❌ | 跳过，仅编译验证 |
