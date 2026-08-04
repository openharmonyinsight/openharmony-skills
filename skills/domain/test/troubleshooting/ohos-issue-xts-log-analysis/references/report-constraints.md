# 报告数据约束

> ⚠️ 本文件是报告数据真实性 / 自检 / 校验 / 多根因规则的**单一权威定义**（原 constraints.md 一~五节）。
> 证据链生成约束（import/domain真实性、源码路径规则、引用链探索）见 [evidence-chain-constraints.md](./evidence-chain-constraints.md)。
> 「跨平台取数/桩程序陷阱」由 [SKILL.md「全平台取数」](../SKILL.md) 权威定义；本文件遇到此主题只给指针。

---

## 目录

- 一、全平台取数强制
- 二、数据真实性7规则（最高优先级）
  - 规则1：时间窗必须 start running 起、specDone 止，且 起始行号 < 结束行号
  - 规则1b：appfreeze时间窗提取（2026-07-15新增）
  - 规则2：消耗时间必须从 hilog 真实提取
  - 规则3：禁止 XXX 占位符
  - 规则4：崩溃根因节必须有真实调用栈
  - 规则5：BLOCKED 必须完整统计（含套件内未执行）
  - 规则6：解密硬门禁——未解密禁止生成完整报告
  - 规则7：空结果处置铁律——脚本取数为0时禁止伪造（2026-07-15新增）
- 三、分层过滤标记强制（Step 5）
- 三b、报告生成前自检清单P1-P8（2026-07-15新增）
- 四、报告生成后校验（Step 6，强制）
- 五、多根因场景处理（2026-07-15新增）

---

## 一、全平台取数强制

> 取数命令、`run.cmd` 启动器、Windows 桩程序陷阱详见 [SKILL.md「全平台取数」](../SKILL.md)（单一事实源）。本节只保留约束：

- Linux/Windows 均必须用 `filter_hilog.py` 取数，**禁止退化为"推测/约N行"**
- 取不到精确值 → 用 `filter_hilog.py` 重取；仍取不到则写「未提取到」
- **禁止**：行号写"XXX（推测）"/"约N行"

---

## 二、数据真实性7规则（最高优先级）

### 规则1：时间窗必须 start running 起、specDone 止，且 起始行号 < 结束行号

- ✅ 起始 = `[Hypium]start running case '<用例名>'`
- ✅ 结束 = `[Hypium]<用例名> specDone end print success`（优先级①），其次下一 start 前（②），其次 fail（③），suite end `OHOS_REPORT_RESULT`（④），文件末尾（⑤）
- ✅ **起始行号必须 < 结束行号**
- ❌ 禁止把 `[fail]` 行同时当起始和结束

#### 规则1b：appfreeze时间窗提取（2026-07-15新增）

> why：appfreeze发生时主线程冻结，[Hypium] start/specDone 标记可能未写入hilog（测试未正常结束），导致 `filter_hilog.py --extract-hypium` 返回0条。此时不能放弃时间窗提取，需从其他来源推断。

**appfreeze时间窗提取回退顺序**：
1. **优先**：从 appfreeze 日志提取（`appfreeze-*.log` 中的 `Fault time` + `TIMESTAMP` 字段）
2. **次选**：从 module_run.log 提取（前一条用例 PASSED 时间 → 套件 End 时间）
3. **末选**：从 hilog 提取 appfreeze 事件行（`grep "THREAD_BLOCK" hilog`）

**时间窗标注**：
- 起始时间：前一条用例结束时间（如 `[120/173] testOhAvPlayerSetPlaybackRateError001 PASSED` 的时间戳）
- 结束时间：套件结束标记时间（如 `End test suite [AVPlayerTest]` 的时间戳）
- 行号：标注「未提取到（主线程冻结，[Hypium]标记未写入）」
- 时间来源：标注「module_run.log [Listener] + appfreeze日志（PC时间+设备时间混合）」

**禁止**：
- ❌ 禁止因 [Hypium] 标记缺失而跳过 appfreeze 用例分析
- ❌ 禁止伪造 [Hypium] 行号
- ✅ 如实标注行号缺失原因，但时间窗和关键日志片段必须提取

### 规则2：消耗时间必须从 hilog 真实提取

```bash
grep "[Hypium]\[fail]<用例名> ; consuming" <hilog>
# → 填 consuming 后的真实值（如 1454ms）
```
- ❌ 禁止把 A 用例的 consuming 填到 B 用例

### 规则3：禁止 XXX 占位符

- ❌ 禁止时间线/字段写 `00:34:15.XXX`、`行号XXX`、`PID XXX`
- ✅ 取不到写「未提取到」

### 规则4：崩溃根因节必须有真实调用栈

- ✅ 1.1节含 cppcrash 真实栈帧：`#00 pc <addr> /system/lib64/xxx.so (FuncName+<offset>)` 至少 3-4 帧
- ❌ 禁止只写示意图而无 pc/函数偏移

### 规则5：BLOCKED 必须完整统计（含套件内未执行）

```bash
grep -n "missed" module_run.log
# [52 tests in AVPlayerTest had missed] + [2 suites have missed]
# → BLOCKED = 52(套件内) + 20 + 100 = 172，不得只算 20+100=120
```
- ❌ 禁止漏算「套件内未执行」的 BLOCKED

### 规则6：解密硬门禁——未解密禁止生成完整报告

- ✅ 含 `hilog.*.gz` 且未解密 → 只输出「解密失败桩报告」
- ❌ 禁止用 module_run.log 兜底生成"看似完整"的报告
- ✅ 生成报告前必跑程序门禁：`python3 scripts/preflight_gate.py <日志目录>`（非0退出=禁止生成完整报告）

### 规则7：空结果处置铁律——脚本取数为0时禁止伪造（2026-07-15新增）

> why：跨平台实测发现，`filter_hilog.py` 因正则不匹配日志格式而返回 0 条时，AI 在 Windows 端直接「编造 hilog 行」生成报告，结论全错。空结果≠许可伪造。

**铁律**：
- ✅ `filter_hilog.py` / `extract_imports.py` 等返回 **0 条**结果时，必须 **debug**（核对正则与日志实际格式，如 `[Hypium]start running case 'X'` vs `[Hypium] start test: X`；domain 行的 `C/A` 类型前缀）或如实写「未提取到」
- ✅ 报告引用的每一条 hilog 行必须真实存在于解密后 hilog（`validate_report.py` 校验8 会 grep 核对，编造必被拦截）
- ❌ 禁止把空结果改为文字描述/示意图顶替
- ❌ 禁止编造带真实时间戳+PID的日志行（即便时间戳是真的，消息体是编的也算伪造）

**反例（真实事故）**：Windows 报告引用 `06-30 00:34:15.847 5602 5653 E C02B22/.../HiTransCoder: (OnEvent(), -): transcoder event error`，时间戳/PID 取自真实崩溃，但消息体 `transcoder event error` 在所有 hilog 中不存在；真实行是 `case testOhAvTransCoderNdkPrepareError0007 ret 2`。该报告被校验8 判定「5 条 hilog 行不存在(疑似伪造)」直接判废。

---

## 三、分层过滤标记强制（Step 5）

**4层标记定义**：

| 标记 | 含义 | 来源 |
|------|------|------|
| `[主]` | 主分析集 | domain 匹配 |
| `[P1]` | P1扩展 | 同(PID,TID) |
| `[P2]` | P2扩展 | 同PID不同TID |
| `[P3]` | P3扩展 | 位置窗口±20行 |

**强制要求**：
- ✅ 所有日志摘录必须带分层来源标记
- ✅ 必须报告分层统计表格（主:N行\|P1:X\|P2:Y\|P3:Z）
- ✅ 主分析集为0 → 明确报告"时间窗内未找到domain日志" + 强制触发P1/P2/P3扩展
- ❌ 禁止省略分层标记
- ❌ 禁止省略分层统计表格
- ❌ 禁止主分析集为空时不执行扩展

---

## 三b、报告生成前自检清单P1-P8（2026-07-15新增）

> why：跨平台实测发现，Windows环境下的报告与Linux环境对同一日志的分析结论存在系统性偏差（BLOCKED漏算52条、appfreeze根因误判为系统侧、崩溃分析节位置错误、行号用~约数）。原因是部分脚本在Windows下未正确执行（Python桩程序陷阱）或AI跳过了强制步骤。此清单在报告生成前**逐项自检**，不通过则禁止生成报告。

**生成前自检（逐项确认，不通过补执行）**：

| # | 检查项 | 通过条件 | 不通过时的处理 |
|---|--------|---------|--------------|
| P1 | preflight_gate.py | 已运行且退出码=0 | 补运行；未解密→只输出解密失败桩报告 |
| P2 | filter_hilog.py 分层取数 | 每个FAILED用例有 主:N\|P1:X\|P2:Y\|P3:Z | 补运行 `--stats-only`；取不到写「未提取到」 |
| P3 | [主]/[P1]/[P2]/[P3] 标记 | 关键日志片段每条带分层标记 | 补运行 `--json` 取带标记输出 |
| P4 | BLOCKED计数含missed | 报告BLOCKED = 显式BLOCKED + missed_tests | `grep -n "missed" module_run.log` 核对 |
| P5 | 崩溃分析在1.1节 | cppcrash存在时，崩溃分析为### 1.1 | 移动到1.1节，后续用例引用 |
| P6 | appfreeze主线程栈 | appfreeze节含 `#00 pc 0x...` 真实栈帧 | 从appfreeze-*.log提取主线程调用栈 |
| P7 | 行号精确 | 无~前缀/约N行 | 用 `filter_hilog.py --extract-hypium` 重取 |
| P8 | 多根因识别 | cppcrash+appfreeze同时存在时，分别分析+分别定界 | 提取appfreeze栈，独立判断归属 |

> 自检通过后生成报告，生成后再跑 `validate_report.py` 校验（校验10-13会自动检查上述P5-P8项）。

---

## 四、报告生成后校验（Step 6，强制）

```bash
# 报告生成后必须运行校验脚本
python3 scripts/validate_report.py <报告.md> <module_run.log> <crash_log目录>
# Windows 桩程序环境改用 run.cmd 启动器（无 Python 时失败退出而非静默通过）
cmd /c scripts\run.cmd validate_report <报告.md> <module_run.log> <crash_log目录>
```

**校验项**（validate_report.py 自动检查）：
1. 2章节结构（一、hilog日志用例详情 + 二、总结）
2. FAILED用例6段落完整性（同根因用例4段落）
3. 崩溃/冻结检测：有cppcrash→有崩溃分析节；有appfreeze→有BLOCKED类型A节
4. BLOCKED计数交叉校验（FAILED+BLOCKED+PASSED = Collected）
5. 分层统计完整性（每个FAILED含 主/P1/P2/P3）
6. 禁止XXX占位符
7. 时间窗起始行号 < 结束行号
8. 取数真实性（C1）：报告引用的 hilog 行必须在解密后 hilog 中真实存在，编造即判废
9. 崩溃时间线完整性（C2）：cppcrash 文件数 = 崩溃时间线条目数（逐条列出）

**退出码**：0=通过，1=有错误（必须修正，禁止交付），2=有警告（建议修正）

---

## 五、多根因场景处理（2026-07-15新增）

> why：实测发现，一次XTS执行可能同时存在两个独立根因（如：系统服务崩溃导致部分FAILED + 测试代码缺陷导致appfreeze导致BLOCKED），需要分别分析、分别定界、分别流转。

**多根因识别依据**：
- 两个根因的崩溃栈/调用栈**不同**（如：SIGSEGV in media_service vs sleep() in libavplayerndk.so）
- 两个根因的问题归属**不同**（如：系统侧 vs 测试侧）
- 两个根因的因果链**独立**（如：崩溃发生在套件A，appfreeze发生在套件B，无直接因果）

**多根因报告要求**：
- ✅ 每个根因独立成节（1.1 崩溃分析 + 1.N+1 appfreeze分析），各自包含完整证据链
- ✅ FAILED用例引用根因1（"同根因"），BLOCKED用例引用根因2
- ✅ "二、总结"中定界结论表格**分别标注**每个用例的问题归属
- ✅ 建议流转**分两条**（系统侧→系统团队，测试侧→测试团队）
- ❌ 禁止将两个独立根因混为一节
- ❌ 禁止将测试侧问题错误归因为系统侧（如把NAPI sleep()循环归因为media_service问题）

详见 [ReportStructure.md - 多根因报告结构](../modules/L2_Report/ReportStructure.md)

---

**约束版本**: 2026-07-15（新增规则1b appfreeze时间窗 + 多根因场景处理）
**强制执行**: 所有报告必须遵守上述约束
**违规后果**: 报告无效，需重新生成
