# AI行为约束（单一权威定义）

> ⚠️ 本文件是所有AI约束的**单一权威定义**。
> [FailureAndSource.md](../modules/L0_PreAnalysis/FailureAndSource.md) 定义流程步骤，本文件定义规则。二者不重叠：FailureAndSource.md 引用规则编号，不复制规则定义。
> 「跨平台取数/桩程序陷阱」由 [SKILL.md「全平台取数」](../SKILL.md) 权威定义；本文件遇到此主题只给指针。

> **强制规则**: AI必须遵守以下约束，违反将导致报告无效

## 目录

- 一、全平台取数强制
- 二、数据真实性6规则（最高优先级）
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
- 六、证据链生成流程
  - 禁止事项清单（import/模块名/domain真实性、源码路径规则、引用链探索）
  - 强制流程清单
  - 自动检查机制
- 七、通用禁止事项
  - 违规处理
  - 最佳实践

---

## 一、全平台取数强制

> 取数命令、`run.cmd` 启动器、Windows 桩程序陷阱详见 [SKILL.md「全平台取数」](../SKILL.md)（单一事实源）。本节只保留约束：

- Linux/Windows 均必须用 `filter_hilog.py` 取数，**禁止退化为"推测/约N行"**
- 取不到精确值 → 用 `filter_hilog.py` 重取；仍取不到则写「未提取到」
- **禁止**：行号写"XXX（推测）"/"约N行"

---

## 二、数据真实性6规则（最高优先级）

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

## 六、证据链生成流程

### 禁止事项清单

#### 1. ❌ 禁止猜测import语句

**问题描述**:
- AI猜测import方式，如：`import stream from '@ohos.stream'`（不存在）
- 实际应为：`import { stream } from '@kit.ArkTS'`

**强制要求**:
- ✅ **必须**：使用`extract_imports.py`脚本提取实际import语句
- ✅ **必须**：从源码文件实际读取import
- ❌ **禁止**：凭空猜测import方式
- ❌ **禁止**：假设API模块名

**正确示例**:
```bash
# 正确：使用脚本提取
$ python3 scripts/extract_imports.py StreamTest08.test.ets

# 输出：
import { stream } from '@kit.ArkTS';  ← 实际import
```

**错误示例**:
```typescript
// ❌ 错误：AI猜测的import（不存在）
import stream from '@ohos.stream';

// ✅ 正确：实际的import
import { stream } from '@kit.ArkTS';
```

---

#### 2. ❌ 禁止猜测模块名

**问题描述**:
- AI猜测模块名：`@ohos.stream`（不存在）
- 实际模块名：`@ohos.util.stream`

**强制要求**:
- ✅ **必须**：从脚本返回结果中提取模块名
- ✅ **必须**：验证模块名是否存在于数据库
- ❌ **禁止**：猜测API模块名
- ❌ **禁止**：使用不存在的模块名查询

**正确示例**:
```bash
# 正确：查询kit展开，从结果中提取模块名
$ python3 scripts/map_domain.py "@kit.ArkTS"

# 返回：
{
  "status": "expanded",
  "modules": ["@ohos.util.stream", ...]  ← 从结果中提取
}
```

**错误示例**:
```bash
# ❌ 错误：猜测模块名
$ python3 scripts/map_domain.py "@ohos.stream"  # 不存在

# 返回：
{
  "status": "unmapped",
  "reason": "'@ohos.stream' NOT FOUND..."
}
```

---

#### 3. ❌ 禁止瞎编domain值

**问题描述**:
- AI在报告中瞎编domain值
- 使用测试运行时domain代替业务API domain

**强制要求**:
- ✅ **必须**：使用`map_domain.py`查询domain
- ✅ **必须**：从查询结果中提取domain值
- ❌ **禁止**：手动编写domain值
- ❌ **禁止**：混淆测试运行时domain和被测方domain

**正确示例**:
```markdown
| API | 子系统 | domain | 日志行 | 时间 |
|-----|--------|--------|--------|------|
| @ohos.util.stream | 公共基础类库 | C003F00 | 241 | 01:55:56 |

**Domain归属说明**:
- `@ohos.util.stream` → `0xD003F00` → **公共基础类库**
- 查询工具：`python3 map_domain.py "@ohos.util.stream"`
```

**错误示例**:
```markdown
| API | 子系统 | domain | 日志行 | 时间 |
|-----|--------|--------|--------|------|
| @ohos.stream | commonlibrary | A03D00 | 241 | 01:55:56 |

❌ 错误：
1. 模块名不存在（@ohos.stream）
2. domain错误（A03D00是测试运行时，不是业务API）
3. 没有使用脚本查询结果
```

---

#### 4. ❌ 禁止混淆测试框架和被测API

**问题描述**:
- 将测试框架API（如`@ohos.hypium`）当作被测API
- 查询测试框架的domain

**强制要求**:
- ✅ **必须**：识别并过滤测试框架API
- ✅ **必须**：区分`test_framework`和`api_module`
- ❌ **禁止**：将测试框架API当作被测方

**正确示例**:
```python
# 正确：分类import时自动过滤测试框架
{
  "imports": [
    {"module": "@ohos/hypium", "type": "test_framework", "skip": true},  ← 跳过
    {"module": "@kit.ArkTS", "type": "kit_module", "skip": false}  ← 保留
  ]
}
```

**错误示例**:
```bash
# ❌ 错误：查询测试框架的domain
$ python3 scripts/map_domain.py "@ohos.hypium"

# 测试框架不应查询domain！
```

---

#### 5. ❌ 禁止跳过内部模块探索

**问题描述**:
- 遗漏内部模块（如Utils.ets）中引用的API
- 导致证据链不完整

**强制要求**:
- ✅ **必须**：探索内部模块的引用链（最多3层）
- ✅ **必须**：使用`explore_import_chain.py`脚本
- ❌ **禁止**：直接跳过内部模块

**正确示例**:
```bash
# 正确：探索内部模块
$ python3 scripts/explore_import_chain.py ScrollBackToTopTest.test.ets --max-depth 3

# 输出：
被测API列表:
  @ohos.arkui.inspector → ArkUI (0xD003900) [第2层]  ← 从Utils.ets发现
  @ohos.file.fs → 文件管理 (0xD004300) [第2层]  ← 从Utils.ets发现
```

**错误示例**:
```markdown
❌ 错误：
import Utils from '../common/Utils';  ← 内部模块

直接跳过，不探索Utils.ets内部引用的API

结果：遗漏了inspector、fs等实际被测API
```

---

#### 6. ❌ 禁止错误的时间窗提取

> 时间窗提取的完整规则（结束标记优先级①~⑤、最后一条用例特殊处理、边界验证、报告标注格式）的**权威定义**见 [ExecutionAndTimeWindow.md Step 4 提取时间窗](../modules/L0_PreAnalysis/ExecutionAndTimeWindow.md) 与本文件「二、规则1」。本节仅保留约束要点，不重复示例，避免两处定义漂移（此前此处曾误将"文件末尾"标为优先级④，实为⑤）。

**约束要点**：
- ✅ 结束标记按优先级①~⑤顺序查找：①specDone → ②下一start前 → ③fail → ④suite end(OHOS_REPORT_RESULT) → ⑤文件末尾
- ✅ 必须验证边界：结束行号 < 下一个用例 start 行号
- ✅ 最后一条用例（无下一 start）必须用 ④suite end 或 ⑤文件末尾，不可仅用 ③fail
- ❌ 禁止仅用 `[Hypium][fail]XXX` 作为结束（遗漏 specDone 等后续日志）
- ❌ 禁止结束行号超过下一个用例 start 标记（包含其他用例日志）

---

#### 7. ❌ 禁止在"源码定位与分析"中使用相对路径（2026-07-13新增）

**问题描述**:
- 在报告"3.2.5 源码定位与分析"（或1.X.5）的"源码位置"字段中使用相对路径或仅文件名
- 相对路径无法唯一定位源码文件，不便于跨环境追溯和流转到责任人团队

**强制要求**:
- ✅ **必须**：源码位置使用绝对路径，格式 `绝对路径:起始行号-结束行号`
- ✅ **必须**：从源码文件实际读取的完整绝对路径
- ❌ **禁止**：使用相对路径（如 `../test/file.ets:82`）
- ❌ **禁止**：仅使用文件名（如 `file.ets:82`）

**正确示例**:
```markdown
**源码位置**: `/home/user/code/arkui/test/TextAreaLetterSpacing.test.ets:82-105`
```

**错误示例**:
```markdown
❌ 错误1（仅文件名）：
**源码位置**: `TextAreaLetterSpacing.test.ets:82`

❌ 错误2（相对路径）：
**源码位置**: `../test/TextAreaLetterSpacing.test.ets:82`

✅ 正确（绝对路径）：
**源码位置**: `/home/user/code/arkui/test/TextAreaLetterSpacing.test.ets:82-105`
```

**适用范围**:
- `complete_testcase_template.md` 中的 1.X.5 源码定位与分析
- `blocked_testcase_template.md` 中的 1.X.5 源码定位与分析
- 报告中所有"源码位置"字段

---

#### 8. ❌ 禁止忽略用户输入的源码路径（2026-07-13新增）

**问题描述**:
- 用户在分析请求中已提供源码路径（如"源码路径是 /home/.../acts/ability"），但 AI 仍只用配置文件的 OH_ROOT
- 不同用户的 OH_ROOT 不同，静态配置可能不匹配当前用户环境

**强制要求**:
- ✅ **必须**：定位源码前，先检查用户输入是否含源码路径
- ✅ **必须**：用户提供的源码路径优先于配置文件 OH_ROOT
- ✅ **必须**：用户输入有源码路径时，使用 `--source-path` 传给 `locate_xts_source.py`
- ❌ **禁止**：忽略用户输入，直接用配置文件 OH_ROOT
- ❌ **禁止**：因配置文件 OH_ROOT 不匹配而放弃源码定位

**源码根路径解析优先级**（从高到低）：
1. 用户本次输入提供的源码路径（最高）
2. 脚本命令行参数（`--root` / `--oh-root`）
3. 脚本 `--source-path` 推断
4. 配置文件 OH_ROOT
5. AI 主动提示用户提供（最低）

**正确示例**:
```bash
# 用户输入："源码路径是 /home/myuser/code/oh/test/xts/acts/ability"
# ✅ 正确：使用 --source-path 让脚本自动推断根路径
$ python3 scripts/locate_xts_source.py \
    --testcase "xxx" --testsuite "yyy" --hap "zzz" \
    --source-path "/home/myuser/code/oh/test/xts/acts/ability"
```

**错误示例**:
```bash
# ❌ 错误1：忽略用户输入，只用配置文件（可能路径不匹配）
$ python3 scripts/locate_xts_source.py --testcase "xxx" --testsuite "yyy" --hap "zzz"
# 即使配置文件有 OH_ROOT，但如果用户提供了路径，应优先用用户的

# ❌ 错误2：配置文件不匹配时不尝试用户输入
# OH_ROOT=/home/xianf/master（配置文件），但当前用户是 /home/myuser/code/oh
# AI 直接报"路径不存在"而不尝试用户输入 → 错误
```

**适用范围**:
- FailureAndSource.md Step -1：源码工程定位
- FailureAndSource.md Step 2.5：源码路径定位
- 报告 1.X.5 源码定位与分析

---

### 强制流程清单

#### 1. ✅ 证据链生成流程

**必须执行以下步骤（按顺序）**:

```
步骤1：提取import
$ python3 scripts/extract_imports.py <测试文件>

步骤2：探索引用链（如有内部模块）
$ python3 scripts/explore_import_chain.py <测试文件> --max-depth 3

步骤3：查询domain
$ python3 scripts/map_domain.py "<模块名>"

步骤4：生成证据链（使用查询结果）
从脚本返回结果中提取数据，禁止瞎编
```

> 证据链生成由 AI 主导：依次调用 extract_imports.py → explore_import_chain.py（可选）→ map_domain.py，用结果填证据链追溯图。

---

#### 2. ✅ 报告生成流程

**必须遵守格式规范**:

```markdown
#### 3.X.3 源码→领域证据链

| API | 子系统 | domain | 日志行 | 时间 |
|-----|--------|--------|--------|------|
| <从脚本提取> | <从脚本提取> | <从脚本提取> | 待补充 | 待补充 |

**证据链追溯**:
```
失败用例源码(<文件名>)
    │ import { <名称> } from '<模块>';  ← 从脚本提取
    ▼
<模块> → domain
    │ <模块> → <domain> → <子系统>  ← 从脚本提取
    ▼
精准日志过滤
    │ 过滤域：<domain正则>  ← 从脚本提取
    ▼
日志切片 → 行xxx-xxx
```

**Domain归属说明**:
- `<模块>` → `<domain>` → **<子系统>**（从脚本提取）
- 查询工具：`python3 map_domain.py "<模块>"`
```

---

### 自动检查机制

#### 检查点1：import语句来源

**检查方式**:
- 报告中的import语句是否与源码文件一致？
- 是否使用了`extract_imports.py`脚本？

**验证方法**:
```bash
# 提取源码import
$ python3 scripts/extract_imports.py <测试文件> --format text

# 对比报告中的import语句
```

---

#### 检查点2：domain值来源

**检查方式**:
- 报告中的domain值是否来自脚本查询结果？
- 是否使用了`map_domain.py`脚本？

**验证方法**:
```bash
# 查询domain
$ python3 scripts/map_domain.py "<模块名>"

# 对比报告中的domain值
```

---

#### 检查点3：模块名准确性

**检查方式**:
- 模块名是否存在于数据库？
- 是否使用了正确的模块名？

**验证方法**:
```bash
# 验证模块名
$ python3 scripts/map_domain.py "<模块名>"

# 如果返回status=unmapped，说明模块名错误
```

---

## 七、通用禁止事项

### 违规处理

#### 违规示例识别

**示例1：猜测import**
```markdown
❌ 违规：
import stream from '@ohos.stream';  ← 猜测的import

✅ 正确：
import { stream } from '@kit.ArkTS';  ← 实际import
```

**示例2：瞎编domain**
```markdown
❌ 违规：
domain: A03D00  ← 瞎编的domain

✅ 正确：
domain: C003F00  ← 从脚本查询结果提取
```

**示例3：混淆测试框架**
```markdown
❌ 违规：
被测API: @ohos.hypium  ← 测试框架

✅ 正确：
跳过测试框架API
被测API: @kit.ArkTS  ← 实际被测API
```

**示例4：源码位置使用相对路径**
```markdown
❌ 违规：
**源码位置**: `TextAreaLetterSpacing.test.ets:82`  ← 仅文件名，无法定位

✅ 正确：
**源码位置**: `/home/user/code/arkui/test/TextAreaLetterSpacing.test.ets:82-105`  ← 绝对路径
```

---

#### 违规后果

- **报告无效**：需要重新生成
- **定界错误**：可能流转到错误的团队
- **浪费时间**：需要重新分析和验证

---

### 最佳实践

#### 1. 证据链原子脚本组合

```bash
# Step 1 提取 import
$ python3 scripts/extract_imports.py <测试文件>
# Step 2 探索内部模块引用链（可选）
$ python3 scripts/explore_import_chain.py <测试文件> --max-depth 3
# Step 3 查询 domain
$ python3 scripts/map_domain.py @ohos.xxx
# AI 用三步结果填证据链追溯图，禁止瞎编
```

---

#### 2. 验证每个步骤

```bash
# 步骤1：验证import提取
$ python3 scripts/extract_imports.py <测试文件>

# 步骤2：验证引用链探索
$ python3 scripts/explore_import_chain.py <测试文件>

# 步骤3：验证domain查询
$ python3 scripts/map_domain.py "<模块名>"
```

---

#### 3. 检查报告格式

**必须包含**:
- ✅ import语句（从源码提取）
- ✅ 模块名（从脚本提取）
- ✅ domain值（从脚本提取）
- ✅ 子系统归属（从脚本提取）
- ✅ 查询工具说明

---

**约束版本**: 2026-07-15（新增规则1b appfreeze时间窗 + 多根因场景处理）
**强制执行**: 所有报告必须遵守上述约束
**违规后果**: 报告无效，需重新生成
