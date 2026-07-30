---
name: ohos-issue-xts-log-analysis
description: "分析XTS测试日志并定界问题归属。当用户提供XTS测试日志目录（含summary_report.xml/module_run.log/hilog.*.gz）、提到测试失败/App died/Blocked/SIGSEGV/cppcrash/jscrash、或需要hilog时间窗切片与domain定界时使用。支持4种输入形态自动识别、Shell执行链判定、源码→领域证据链追溯、崩溃栈解析。"
metadata:
  author: openharmony
  scope: domain
  stage: troubleshooting
  domain: xts
  capability: log-analysis
  version: 0.1.0
  status: stable
  tags:
    - xts
    - log-analysis
    - troubleshooting
    - domain-tracing
  related-skills:
    - ohos-issue-crash-log-analysis
    - ohos-test-xts-generation
---

# ohos-issue-xts-log-analysis

> **XTS测试问题日志定界分析** — 基于执行日志的 XTS 测试问题分析技能，采用分层过滤模型，支持4种输入形态自动识别、源码→领域证据链追溯、崩溃栈解析。

## 核心功能与适用场景
- 多形态自动识别（全量报告/log根/单testsuite/hilog目录）
- 分层过滤（时间窗→domain分组→渐进式扩展）
- 源码→领域证据链（API→子系统→domain→日志行）
- 标准报告生成（2章节，符合XTS规范）
- 适用：XTS失败定界 / App died / Blocked排查 / SO崩溃栈解析

## 前置配置
- **OH_ROOT**（可选，有源码时启用）：配置 `./.xts-analysis-config.json`，详见 [config.md](./docs/config.md)
- **数据库验证（强制）**：`data/xts_rules.db` 必须存在；表结构见 [database-schema.md](./docs/database-schema.md)
  - module_domain(529条 JS/TS→domain) / api_path_mapping(2172条 sdk-js+sdk_c→子系统) / subsystem_domain_mapping(555) / subsystem_domain_inference(18 子系统→domain)

## 输入形态识别（强制）
`ls -la <日志目录>` 判定形态，按形态选流程：

| 形态 | 识别特征 | 流程 |
|------|----------|------|
| ① 全量报告 | 含 `summary_report.xml` | A |
| ② log 根 | 下全是 `Acts*/` 子目录 | A |
| ③ 单 testsuite | 含 `module_run.log` | A |
| ④ hilog 目录 | 含 `hilog.*.gz`，无 `module_run.log` | B |

- 流程A → [modules/L0_PreAnalysis/FormAndDecrypt.md](./modules/L0_PreAnalysis/FormAndDecrypt.md)（**不要加载** 形态④路由）
- 流程B → [modules/L0_PreAnalysis/Form4_Limited.md](./modules/L0_PreAnalysis/Form4_Limited.md)（**不要加载** 流程A形态识别步骤）
- 崩溃/冻屏深度分析 → 由 Step 2.7 检测后触发：[崩溃分析](./modules/L0_PreAnalysis/CrashAnalysis.md) ｜ [冻屏分析](./modules/L0_PreAnalysis/FreezeAnalysis.md)（**不要加载**，除非 Step 2.7 检测到对应日志）

### 流程覆盖图（Flow Coverage Map）

> 流程B真正跳过的只有 **Step 2**（锁定失败用例，改用户提供）和 **Step 3**（执行状态分析，无module_run.log）。Step 2.5/2.5.6/2.7 与流程A完全相同。

| Step | 层 | 流程A（形态①②③） | 流程B（形态④） | 加载文件 |
|------|----|------------------|---------------|---------|
| 1 形态识别 | L0 | ✅ 执行 | ✅ 变体 | A:FormAndDecrypt / B:Form4_Limited |
| 1.5 解密 | L0 | ✅ 执行 | ✅ 共享 | FormAndDecrypt |
| 2 锁定失败用例 | L0 | ✅ 执行 | ⏭️ 跳过（用户提供） | FailureAndSource(仅A) |
| 2.5 源码定位 | L0 | ✅ 执行 | ✅ 共享 | FailureAndSource |
| 2.5.6 import提取 | L0 | ✅ 执行 | ✅ 共享（必须） | FailureAndSource |
| 2.7 崩溃/冻结检测 | L0 | ✅ 执行 | ✅ 共享 | CrashFreezeDetect→CrashAnalysis/FreezeAnalysis |
| 3 执行状态分析 | L0 | ✅ 执行 | ⏭️ 跳过（无module_run.log） | ExecutionAndTimeWindow(仅A) |
| 4 提取时间窗 | L0 | ✅ 执行 | ✅ 变体（仅hilog [Hypium]） | ExecutionAndTimeWindow（含形态④变体） |
| 5 分层过滤 | L1 | ✅ 执行 | ✅ 共享 | LayeredFilter |
| 6 生成报告 | L2 | ✅ 执行 | ✅ 共享+标注 | ReportGeneration+ReportStructure |

## 加密日志解密 + 硬门禁（P0，最高优先级）
> 工具详解：[hilogtool-guide.md](./references/hilogtool-guide.md)

检测到 `hilog.*.gz` → **必须用 hilogtool 解密**（禁 gunzip/strings）。dict 必需（`hilog_dict.*.zip`/`dict.zip`，与hilog同目录，时间戳无需匹配）。

> ⚠️ **dict.zip 是 hilogtool 的输入参数（`-d`），不要手动 `unzip` 解压 dict**。hilogtool 内部自动处理 dict。手动 unzip dict 只会产生无用的密钥文件，不能解密 hilog。

### 平台决策树（wine 不可用时禁止降级，必须按平台尝试）

```
检测到 hilog.*.gz → 必须解密（禁止"wine不可用就跳过解密降级为module_run.log"）：
  ├─ Windows：直接运行 hilogtool.exe（原生，无需 wine）
  │    1. mkdir <hilog目录>_parsed                          # 先创建输出目录（hilogtool 不自动创建）
  │    2. <skill路径>/tools/hilogtool.exe parse -i <hilog目录> -o <hilog目录>_parsed -d <dict.zip>
  │    或用 .cmd 启动器（自动探测 Python，无 Python 时直跑 hilogtool.exe）：
  │       cmd /c scripts\check_dict.cmd <hilog目录>        # cmd / PowerShell
  │       cmd /c scripts\parallel_decrypt.cmd <hilog目录>  # 并行解密+自动创建目录+缓存
  │    ⚠️ Git Bash 下路径用正斜杠避免转义：cmd //c "C:/Users/.../scripts/check_dict.cmd" "D:/..."
  │
  ├─ Linux：先检测 wine64，未安装则安装
  │    1. wine64 --version || sudo apt-get install -y wine64
  │    2. python3 scripts/parallel_decrypt.py <hilog目录>   # 自动调 wine64+自动创建目录+缓存
  │    或手动（须用完整路径）：
  │       wine64 <skill路径>/tools/hilogtool.exe parse -i <hilog目录> -o <hilog目录>_parsed -d <dict.zip>
  │    ⚠️ 不要用相对路径 hilogtool.exe，wine64 找不到；不要 cd 到工具目录
  │
  └─ macOS：同 Linux（需 wine64）
```

### 跨平台脚本（推荐，有 Python 时优先用）

```bash
python3 scripts/check_dict.py <hilog目录>         # 解密前检查 dict
python3 scripts/parallel_decrypt.py <hilog目录>    # 并行解密（自动缓存+自动创建输出目录，输出 <目录>_parsed/）
python3 scripts/verify_dict_location.py <日志目录> # 解密后验证 dict 位置
python3 scripts/preflight_gate.py <日志目录>       # 生成报告前硬门禁（未解密→非0退出→只许输出解密失败桩报告）
```

> ⚠️ **Windows 桩程序陷阱（2026-07-15）**：若 `python3` 指向 `C:\Users\<u>\AppData\Local\Microsoft\WindowsApps\python3.exe`（Microsoft Store 应用执行别名桩程序），在非交互终端会**静默退出、零输出**，`.py` 脚本看似“无反应”实为**根本未执行**（脚本内自检无法捕获）。判定：`python3 -c "import sys;sys.stdout.write('PYOK')"` 无输出即桩程序。对策：用上方 `.cmd` 启动器（自动绕过），或直跑 `hilogtool.exe`，或装真 Python（python.org，勾选 Add to PATH）后用 `py` 调用。

> ⚠️ **解密硬门禁**：日志目录含 `hilog.*.gz` 且未成功解密 → **禁止**生成含"行号/domain分层/崩溃栈/定界结论"的完整报告，只输出「解密失败桩报告」（含失败原因 + 上述解决命令 + "解密后重新生成"），不含任何定界结论。
>
> **为什么（理解而非死记）**：定界要回答的是**为什么失败**（崩溃？断言？环境？），而**为什么**只存在于 hilog 里——崩溃栈、domain 域日志、行号全在解密后的 hilog。`module_run.log` 只能告诉你**什么**失败了（pass/fail/blocked 计数 + 错误码），给不出崩溃根因/域日志/行号。所以没有解密 hilog 就定界 = 猜测 = 必错——实测把 media_service SIGSEGV 崩溃误判成"分辨率参数校验"，结论全错。
>
> **预先驳掉三个常见借口**：
> - ❌ "解密要几分钟，先跳过"：解密几分钟是正确报告的必要成本；错误定界更费时（流转错团队、错误修复、返工）。
> - ❌ "用 module_run.log 也能定界"：module_run.log 只有**结果**（failed/blocked/error msg），没有**根因**（崩溃栈/domain/行号）。它能说"什么挂了"，说不出"为什么挂"——而定界就是问"为什么"。
> - ❌ "wine 不可用，降级用 module_run.log"：Windows **不需要 wine**（直接运行 hilogtool.exe 原生）；Linux **先装 wine64**（`sudo apt-get install wine64`）再解密。见上方平台决策树。
>
> 仅当目录内**完全没有** `hilog.*.gz`（纯 module_run.log，无加密日志）时，才可用 module_run.log 做有限分析（无行号/domain，仅执行链+用例结果）。

## 核心工作流程

**前置分析**：形态识别 → 锁定失败用例 → 源码定位+import提取 → **崩溃/冻结检测（Step 2.7，强制）** → Shell执行链分析（bm install→aa test→Collected count→[Listener]，详见 [shell-chain.md](./references/shell-chain.md)）
**日志分析**：提取时间窗（hilog [Hypium] 优先，filter_hilog.py 全平台必用，详见 [time-window.md](./references/time-window.md)）→ 分层过滤
**报告生成**：`preflight_gate.py` 生成前硬门禁（未解密必拦）→ 生成2章节标准报告 → `validate_report.py` 校验至 0 错误（硬门禁，取数真实性+崩溃时间线+计数全检）

### 文件导航图（按步骤加载，避免过度加载）

```
Step 1 形态识别        → modules/L0_PreAnalysis/FormAndDecrypt.md（流程A）/ Form4_Limited.md（流程B）
Step 1.5 解密          → modules/L0_PreAnalysis/FormAndDecrypt.md（A+B共享）
Step 2 锁定失败用例    → modules/L0_PreAnalysis/FailureAndSource.md（仅流程A；流程B跳过，用户提供用例名）
Step 2.5 源码定位      → modules/L0_PreAnalysis/FailureAndSource.md + references/source-location.md（A+B共享）
Step 2.5.6 import提取  → references/constraints.md（六、证据链生成流程）（A+B共享，必须）
Step 2.7 崩溃/冻结检测 → modules/L0_PreAnalysis/CrashFreezeDetect.md（检测命令）→ 按结果加载：
                          modules/L0_PreAnalysis/CrashAnalysis.md（崩溃）/ FreezeAnalysis.md（冻屏）（A+B共享）
Step 3 执行状态分析    → references/shell-chain.md（仅流程A；流程B跳过，无module_run.log）
Step 4 提取时间窗      → modules/L0_PreAnalysis/ExecutionAndTimeWindow.md（含形态④变体）+ references/time-window.md
Step 5 分层过滤        → modules/L1_Filter/LayeredFilter.md（A+B共享）
Step 6 生成报告        → modules/L2_Report/ReportGeneration.md（A+B共享）+ ReportStructure.md（格式）
  生成前自检           → references/constraints.md 三b节（P1-P8清单）
```

> 每步只加载对应文件，不要一次性加载全部引用。

### ⚠️ 强制流程（证据链追溯）— 禁止跳过
> 完整约束：[references/constraints.md](./references/constraints.md)（证据链+通用禁止+报告数据真实性+自检清单，单一权威定义）
> 
> **加载时机**：Step 2.5.6（import提取）时加载 constraints.md 六节（证据链）；Step 6（报告生成）时加载 constraints.md 二~三b节（数据真实性+自检清单）。**不要在 Step 1 形态识别阶段加载约束文件**。

**核心禁止**（违规→报告无效）：禁止猜测import/模块名/domain；禁止猜测日志内容/XXX占位符；禁止省略分层标记[主]/[P1]/[P2]/[P3]；禁止混淆测试框架与被测API；禁止跳过内部模块探索（≤3层）。

1. **提取import**（必须）：`python3 scripts/extract_imports.py <测试源码>` （JS/TS/C，自动分类，支持NAPI sdk_c/*.h）
2. **探索引用链**（内部模块时）：`python3 scripts/explore_import_chain.py <源码> --max-depth 3`
3. **查询domain**（必须）：`python3 scripts/map_domain.py "@ohos.xxx"` 或 `"@kit.ArkTS"` 或 NAPI头 `"native_api.h"`；NAPI .so 用 `python3 scripts/trace_napi_chain.py <测试文件> --xts-root <XTS根> --format chain`
4. **生成证据链**：用查询结果填 `源码→@ohos模块→子系统→domain→日志过滤` 追溯图，禁止瞎编。

> ⚠️ **系统服务domain发现（2026-07-15新增）**：`map_domain.py` 返回的是**SDK domain**（测试侧调用的API domain，如 `C002B`），但被测**系统服务进程**在hilog中可能使用**不同的domain**（如 media_service 用 `C02B2B`/`C02B22`/`C02B24`）。当 filter_hilog.py 用SDK domain过滤返回0条主分析集时：
> 1. 在hilog中grep系统服务进程名（如 `grep "media_service" hilog`）发现实际domain标签
> 2. 用实际domain标签重新执行 filter_hilog.py（如 `-d 02B2B 02B22 02B24`）
> 3. 证据链中同时标注SDK domain和系统服务domain
> 
> > 同根因用例：可用「同根因模板」（基本信息+时间窗+根因继承+定界），但基本信息与时间窗提取表格必须完整（详见 [modules/L2_Report/ReportGeneration.md](./modules/L2_Report/ReportGeneration.md) 同根因用例特殊处理）。
>
> ⚠️ **多根因场景（2026-07-15新增）**：一次XTS执行可能同时存在两个独立根因（如系统崩溃→FAILED + 测试代码缺陷→appfreeze→BLOCKED）。需分别分析、分别定界、分别流转。详见 [ReportStructure.md - 多根因报告结构](./modules/L2_Report/ReportStructure.md)。

## 强制脚本
| 脚本 | 用途 |
|------|------|
| extract_imports.py | 提取import/#include并分类（api/kit/c_api/internal/test_framework） |
| explore_import_chain.py | 内部模块引用链探索（≤3层） |
| map_domain.py | @ohos/@kit/xxx.h → domain+子系统（JS/TS/NAPI） |
| trace_napi_chain.py | NAPI .so 6层追溯（.so→封装→C++→SDK接口→subsystem→domain） |
| query_api_path.py | 2172条接口路径→子系统查询 |
| parallel_decrypt.py / check_dict.py / verify_dict_location.py | 解密/检查/验证（跨平台） |
| parallel_decrypt.cmd / check_dict.cmd | Windows 启动器（探测 Python 桩程序，无 Python 时直跑 hilogtool.exe 原生解密） |
| **run.cmd** | **Windows 通用启动器**：纯 Python 分析/门禁脚本（preflight_gate/filter_hilog/validate_report/verify_dict_location/map_domain 等）专用；探测桩程序，无真 Python 时**失败退出(非0)而非静默通过**——否则 preflight_gate 会静默"通过"硬门禁、filter_hilog 无分层标记、validate_report 无校验，断安全链 |
| **preflight_gate.py** | **报告生成前硬门禁**（含 hilog.\*.gz 未解密→非0退出→只许输出解密失败桩报告） |
| filter_hilog.py | 全平台分层过滤+Hypium时间窗提取（Linux/Windows必用，统一[主]/[P1]/[P2]/[P3]标记） |
| validate_report.py | 报告结构校验（2章节/6段落/BLOCKED计数/appfreeze/分层统计/取数真实性/崩溃时间线，生成后必跑，硬门禁） |
| query_db.py | 定界规则/责任人/SO库归属查询 |
| analyze_crash_stack.py | SO 崩溃栈快速分析（可选，调 query_db.so_mapping） |

> AI主导判断，脚本辅助。

## 输出规范（报告生成前必读）
> 完整格式：[modules/L2_Report/ReportGeneration.md](./modules/L2_Report/ReportGeneration.md)（含标准段落结构 + 同根因用例格式 + 报告生成流程 + 禁止行为）
>
> ⚠️ **生成报告前必须加载以下文件（缺一不可，未加载则章节结构必错）**：
> 1. [modules/L2_Report/ReportGeneration.md](./modules/L2_Report/ReportGeneration.md) — 完整格式规范 + 报告生成流程 + 标准段落结构
> 2. [references/constraints.md](./references/constraints.md) 三b节 — P1-P8 自检清单
>
> **加载时机**：Step 6（报告生成）时加载。**不要在 Step 1-5 分析阶段加载 ReportGeneration.md**（分析阶段只需 SKILL.md + 对应流程模块）。

- **命名**：`XTS_Analysis_Report_YYYYMMDD.md`，存日志目录
- **2章节（全表格）**：
  - 一、hilog日志用例详情（每个失败用例6段落：基本信息/时间窗提取/源码→领域证据链/关键日志片段/源码定位与分析/问题定界）
  - 二、总结（测试侧/系统侧分类 + 定界结论表格 + 建议流转）
- **必须含**：所在日志(hilog)、起始行号、结束行号；分层统计 主:N行|P1:X|P2:Y|P3:Z + [主]/[P1]/[P2]/[P3] 标记
- **禁止简化**：第2-14个用例也需完整表格（基本信息+时间窗提取必填）；禁止用文字替代表格
- **BLOCKED分类**：类型A异常触发用例（完整6段，与FAILED同）；类型B级联阻塞（汇总，不逐条）；崩溃为根因时1.1节放崩溃分析（真实调用栈+时间线，禁XXX占位符，BLOCKED须含套件内missed完整统计）
- **数据真实性6规则**（详见 [references/constraints.md](./references/constraints.md)）：①时间窗起<止 ②消耗时间grep真实值 ③禁XXX占位符 ④崩溃真实调用栈 ⑤BLOCKED完整统计 ⑥解密硬门禁

## 全平台取数（强制，2026-07-14改进）
Linux/Windows 均必须用 Python 脚本取数（统一 [主]/[P1]/[P2]/[P3] 标记格式，grep 无法生成标记），禁止退化为"推测/约N行"：
```bash
# 行号/时间窗（替代 grep -n）
python3 scripts/filter_hilog.py -i <hilog> --extract-hypium --testcase <用例名> --json
# 分层计数+[主]/[P1]/[P2]/[P3]标记（替代 grep -c / grep -n -E / sed -n）
python3 scripts/filter_hilog.py -i <hilog> -d <domain> --time-start <t> --time-end <t> --json   # 或 --stats-only
# 报告结构校验（生成后必跑）
python3 scripts/validate_report.py <报告.md> <module_run.log> <crash_log目录>
```
> 取不到精确值如实写"未提取到"，禁止"XXX（推测）"/"约N行"。详细约束见 [references/constraints.md](./references/constraints.md)。
>
> ⚠️ **Windows 桩程序环境取数（2026-07-15）**：上述 `python3 scripts/xxx.py` 在 Windows 上若 `python3` 是 Microsoft Store 桩程序会**静默退出零输出**（filter_hilog 无行号、preflight_gate 静默"通过"、validate_report 无校验 → 断安全链）。此时改用通用启动器：`cmd /c scripts\run.cmd filter_hilog -i <hilog> ...` / `run.cmd validate_report <报告> <mrl> <crash>` / `run.cmd preflight_gate <日志目录>`（探测桩程序，无真 Python 时**失败退出**而非静默成功）。Linux/macOS 无此问题，直接 `python3 scripts/xxx.py`。

## 跨平台一致性要求（2026-07-15新增）

> 同一日志在 Linux 和 Windows 下分析，结论必须一致。若不一致，必有一方出错。

**跨平台高频偏差（实测发现）**：
| 偏差 | 原因 | 对策 |
|------|------|------|
| BLOCKED漏算missed | Windows下未grep "missed" | 强制：`grep -n "missed" module_run.log` |
| appfreeze根因误判 | 未提取主线程栈，用"可能原因"猜测 | 强制：从appfreeze-*.log提取`#00 pc`栈帧 |
| 崩溃分析节位置错 | 放在1.3而非1.1 | 强制：崩溃分析必须在### 1.1 |
| 行号用~约数 | filter_hilog.py未执行或Python桩程序 | 强制：用.cmd启动器或filter_hilog.py |
| 多根因未识别 | appfreeze误归因为崩溃导致 | 强制：cppcrash+appfreeze→分别提取栈→独立定界 |

> 生成报告前对照 [constraints.md 三b节](./references/constraints.md) 自检清单逐项确认；生成后必跑 `validate_report.py`（校验10-13自动检查上述偏差）。

## 故障排除
- **Windows 下 `.py` 脚本零输出/无 `_parsed/`**（`python3` 是 Microsoft Store 桩程序）→ 用 `scripts\check_dict.cmd` / `scripts\parallel_decrypt.cmd` 启动器（自动绕过），见 [hilogtool-guide.md](./references/hilogtool-guide.md) "Windows Python 桩程序"小节
- 解密问题（dict缺失/路径/hilogtool）→ [hilogtool-guide.md](./references/hilogtool-guide.md)
- **wine 不可用** → `sudo apt-get install wine64`；应急可用 `strings hilog.000.gz | grep -E "Error|FAILED|Hypium"`（不完整，仅应急）
- **hilogtool 报错 std::out_of_range** → 原因：使用了 gunzip 解压后的文件。hilog.gz 包含两层（gzip+GLS_BINARY加密），**禁用 gunzip**，必须用 hilogtool 处理原始 .gz 文件
- 源码/OH_ROOT → [config.md](./docs/config.md)
- 数据库缺失 → 确认 skill 安装完整；关键字/SO库未匹配 → `python3 scripts/query_db.py rules --keyword "<关键字>"` / `so "<库名>"`
- 报告格式不符 → `python3 scripts/validate_report.py <报告.md> <module_run.log> <crash_log目录>` 校验，或查 [modules/L2_Report/ReportGeneration.md](./modules/L2_Report/ReportGeneration.md)
- 文件缺失降级（无源码/无 dict/无 hilog 等场景）→ [degradation-matrix.md](./docs/degradation-matrix.md)（质量分级 L0-L4 + 降级路径）

---

## 评估用例
> 端到端评估用例见 [evals/evals.json](./evals/evals.json)（含 3 个场景：标准 FAILED 定界 / 崩溃+级联阻塞 / 多根因场景）。测试输入文件在 [evals/test_cases/](./evals/test_cases/)，每条用例含 `prompt`、`files`、`expected_output` 和 `assertions`（`contains`/`llm_judge` 两种断言类型）。

---

**更新**：2026-07-30（重构：modules/ 分层目录化 L0_PreAnalysis/L1_Filter/L2_Report；L0_Standard 拆为7文件；L3_CrashFreeze 并入 L0 拆为 CrashAnalysis+FreezeAnalysis+CrashFreezeDetect；L2_Report 拆为 ReportGeneration+ReportStructure；docs/ 扁平化入 references/；Form4Limited→Form4_Limited 瘦身为流程B薄路由+步骤路由表；修复P7：流程B补2.5/2.5.6/2.7共享标注；新增Flow Coverage Map；ExecutionAndTimeWindow补形态④变体节）
**设计理念**：文档驱动AI操作，AI主导判断，脚本辅助查询；SKILL.md 仅含触发+流程+关键命令+指针，细节在各 reference
