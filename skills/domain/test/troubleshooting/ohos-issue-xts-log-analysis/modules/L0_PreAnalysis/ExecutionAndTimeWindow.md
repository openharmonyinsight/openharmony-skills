# L0_PreAnalysis - 执行状态分析与时间窗（Step 3-4）

> Shell执行链详见 [shell-chain.md](../../references/shell-chain.md)；时间窗对齐详见 [time-window.md](../../references/time-window.md)。
---

## Step 3：分析执行状态

> 📖 **详细分析说明**: [shell-chain.md](../../references/shell-chain.md)

**AI操作**：顺序检查 module_run.log 中的执行阶段

### 执行阶段检查

**阶段①：bm install** → hap 是否安装成功？
```bash
grep "bm install" module_run.log
grep -A 5 "bm install" module_run.log  # 查 install 后是否有报错
```

**判定**：
- install 后无报错 / 出现 [Listener] → 成功
- install 后有报错 / 无后续 aa test → 失败

**阶段②：aa test** → aa test 命令是否正常下发？
```bash
grep "aa test" module_run.log
grep "OHJSUnitDriver" module_run.log  # 查是否出现 run test
```

**判定**：
- 出现 [OHJSUnitDriver] run test → 成功
- aa test 报错 / 无后续 OHJSUnitDriver → 失败

**阶段③：Collected count** → 用例是否被收集到？
```bash
grep "Collected suite count" module_run.log
```

**判定**：
- suite count > 0 / test count > 0 → 成功
- suite count = 0 / test count = 0 → 失败

**阶段④：[Listener]** → 是否有逐用例结果输出？
```bash
grep "[Listener]" module_run.log
grep "PASSED" module_run.log
grep "FAILED" module_run.log
```

**判定**：
- 有 PASSED/FAILED 行 → 成功
- 无 [Listener] 行 → 失败（用例未真正运行）

### 执行状态判定分支

| 执行阶段状态 | 判定 | 后续操作 |
|-------------|------|---------|
| ①②③④ 全通过 | 测试正常执行，失败为用例逻辑问题 | 继续 Step 4，进入 hilog 切片 |
| ① 失败（install 报错 / 无后续 aa test） | hap 安装失败（环境/包问题） | **不做 hilog 切片**，直接定界环境问题 |
| ②③ 失败（aa test 报错 / 用例数=0） | aa test 执行失败 | **不做 hilog 切片**，直接定界环境问题 |
| ④ 无 [Listener] 行（用例未真正运行） | 测试框架/启动问题 | **不做 hilog 切片**，直接定界环境问题 |

**⚠️ 强制要求**：前置分析必须在分层过滤前完成。若测试未执行（install/aa test 失败），则**不做 hilog 切片**——直接定界为环境问题。

### 输出

```
Step 3：分析执行状态
判定结果：测试正常执行（或 install失败 / aa test失败 / 未运行）
证据：
  - bm install：成功（或 失败：xxx）
  - aa test：成功（或 失败：xxx）
  - Collected count：100个用例（或 0个）
  - [Listener]：有逐用例输出（或 无输出）
```

> ⚠️ 执行状态判定结果用于**内部分析流程控制**（决定是否进行hilog切片），**不在分析报告中体现**。

---

## Step 4：提取时间窗

> 📖 **详细对齐说明**: [time-window.md](../../references/time-window.md)
>
> **⚠️ 改进**：新增精确结束标记逻辑，避免时间窗越界。

> 跨平台取数规则、Windows 桩程序陷阱与 `run.cmd` 启动器用法，详见 [SKILL.md「全平台取数」](../../SKILL.md)。Linux/Windows 均必须用 `filter_hilog.py` 取数，grep/Select-String 无法生成 `[主]/[P1]/[P2]/[P3]` 标记。

**说明**：时间窗提取信息在"一、hilog日志用例详情"每个用例的「时间窗提取」段落（1.X.2）中展示。

```bash
# ✅ 跨平台推荐（Linux/Windows 通用，精确行号，无需 grep）
# 提取某用例的 [Hypium] 时间窗（起始/结束行号 + 时间），输出 JSON
python3 scripts/filter_hilog.py -i <hilog文件> --extract-hypium --testcase <用例名> --json

# 列出 hilog 中所有 [Hypium] 用例及其时间窗
python3 scripts/filter_hilog.py -i <hilog文件> --extract-hypium

# 仅取统计（不取明细）
python3 scripts/filter_hilog.py -i <hilog文件> --extract-hypium --stats-only
```

### 方法1（优先）：从 hilog [Hypium] 标记提取（设备时间，精确时间窗）

**⚠️ 时间窗提取必须包含完整生命周期**

> 下方 `grep -n` 为 Linux **概念示意**（说明优先级查找逻辑）；实际取数用本节顶部的 `filter_hilog.py --extract-hypium`（全平台必用，grep/Select-String 无法在 Windows 原生 shell 运行且不生成标记）。

```bash
# 步骤1：提取起始标记（概念示意）
grep -n "Hypium.*start running case 'testcase_X'" hilog.txt

# 步骤2：提取结束标记（优先级顺序）
# 优先级①：specDone标记（最精确）
grep -n "Hypium.*testcase_X specDone end print success" hilog.txt

# 优先级②：下一个用例的start标记（边界）
grep -n "Hypium.*start running case 'testcase_Y'" hilog.txt

# 优先级③：fail标记（失败标记，包含部分后续日志）
grep -n "Hypium.*\[fail\]testcase_X" hilog.txt
```

**结束标记优先级**（强制要求）：
1. **优先级①（最精确）**：`[Hypium]XXX specDone end print success` - 用例真正结束，包含完整生命周期
2. **优先级②（边界）**：下一个 `[Hypium]start running case 'YYY'` 的前一行 - 用例边界，避免包含下一个用例日志
3. **优先级③（失败标记）**：`[Hypium][fail]XXX` - 失败标记，包含部分后续日志（不完全精确）
4. **优先级④（suite end）**：`OHOS_REPORT_RESULT` - 测试套件结束标记（最后一条用例的精确结束）
5. **优先级⑤（文件末尾）**：文件总行数 - 最后的回退方案（suite end未找到时使用）

**⚠️ 边界情况处理**：

**最后一条用例的特殊处理**：
- 如果是测试套件的最后一个用例（无下一个start标记）→ 使用优先级①、④或⑤
- 优先级①（specDone）：仍然可用，优先使用
- 优先级②（边界）：不可用（无下一个start）
- 优先级④（suite end）：`OHOS_REPORT_RESULT` 标记（测试套件结束）
- 优先级⑤（文件末尾）：suite end未找到时的最后回退

```bash
# 判断是否为最后一条用例
if [ -z "$(grep 'Hypium.*start running case' hilog.txt | tail -1 | grep 'testcase_X')" ]; then
    echo "✅ 这是最后一条用例"

    # 优先级①：specDone标记（仍然可用）
    grep -n "Hypium.*testcase_X specDone end print success" hilog.txt

    # 优先级④：suite end标记（测试套件结束）
    grep -n "OHOS_REPORT_RESULT" hilog.txt

    # 优先级⑤：文件末尾（最后回退）
    wc -l hilog.txt
fi
```

**⚠️ 禁止事项**：
- ❌ 禁止仅用 `[fail]` 标记作为结束（会遗漏后续的 specDone 日志）
- ❌ 禁止超过下一个用例的 start 标记（会包含下一个用例的日志）
- ❌ 禁止最后一条用例直接使用文件末尾而未先尝试 suite end 标记
- ✅ 必须按优先级①②③④⑤顺序查找结束标记
- ✅ 必须判断是否为最后一条用例（特殊处理）

**示例对比（testXmlCase001）**：

**❌ 错误示例（仅用fail标记）**：
```
起始：3082 [Hypium]start running case 'testXmlCase001'
结束：3102 [Hypium][fail]testXmlCase001 ← 错误！遗漏了specDone日志
结果：时间窗3082-3102，缺少后续关键日志（specDone标记）
```

**✅ 正确示例（使用specDone标记）**：
```
起始：3082 [Hypium]start running case 'testXmlCase001'
结束：3124 [Hypium]testXmlCase001 specDone end print success ← 正确！
结果：时间窗3082-3124，包含完整生命周期

下一个用例：3125 [Hypium]start running case 'testXmlCase002' ← 边界验证
```

**✅ 最后一条用例示例（testLastCase）**：
```
起始：60753 [Hypium]start running case 'testLastCase'
结束标记查找：
  - 优先级①：未找到specDone标记
  - 优先级②：无下一个start标记（这是最后一条用例）
  - 优先级④：找到suite end标记 OHOS_REPORT_RESULT（行43181）← 精确！

时间窗：60753-43181（suite end标记）
边界情况：最后一条用例，无下一个start，使用suite end标记
```

**✅ 文件末尾回退示例（suite end未找到）**：
```
起始：60753 [Hypium]start running case 'testLastCase'
结束标记查找：
  - 优先级①：未找到specDone标记
  - 优先级②：无下一个start标记（这是最后一条用例）
  - 优先级④：未找到suite end标记（OHOS_REPORT_RESULT）
  - 优先级⑤：文件末尾（行51877）← 最后回退

时间窗：60753-51877（文件末尾）
边界情况：最后一条用例，suite end未找到，使用文件末尾
```

**提取内容**：
- [Hypium]start running case → 起始时间 + 行号
- [Hypium]XXX specDone end → 结束时间 + 行号（精确）
- 设备时间（无需对齐）
- **所在日志文件** - hilog文件名（如 hilog.050.20260630-020003.txt）
- **边界验证** - 下一个用例start标记（确保不越界）
- **最后一条用例判断**：无下一个start时优先使用suite end标记
- **suite end回退**：suite end未找到时使用文件末尾
- 报告中标注边界情况和使用的优先级

### 方法2（回退）：从 module_run.log 提取（PC 时间）

```bash
grep "FAILED.*testcase_X" module_run.log
```

**提取内容**：
- 找 [Listener] [... testcase_X FAILED] 行 → 得终止时间 T_end(PC)
- 找上一用例 PASSED/FAILED 行或 aa test 开始行 → 得起始时间 T_start(PC)
- 时间窗 = [T_start, T_end]，均为 PC 端时间

**module_run.log 不可达时的处理**：
时间窗只能从 hilog 内 [Hypium]start/[specDone end] 提取（设备时间）

### PC↔设备时间对齐

⚠️ module_run.log 为 PC 时间，hilog 为设备时间，存在毫秒级差。

**对齐策略（三选一，按优先级）**：

**策略①：主时钟同步标记对齐（优先）**

module_run.log 首行 `hdc shell date '2026-06-26 15:53:44'` 为 PC 下发的时间，该时刻起设备时钟被强制同步为 PC 时间。此后 PC↔设备时钟差≈0（仅漂移毫秒级）。

**操作**：
```bash
grep "hdc shell date" module_run.log
```

**判定**：
- 若 module_run.log 含 date 同步行 → 直接用 PC 时间窗匹配 hilog 文件名时间戳

**策略②：hilog 文件名时间戳对齐**

hilog 文件名含设备时间（hilog.027.20260626-155352.gz → 15:53:52 设备时间），据此选择覆盖时间窗的 hilog 文件，并对内部日志做 ±500ms 容差匹配。

**策略③：同步标记缺失时**

扩大时间窗 ±2s 容差，并依赖 [Hypium]start running case 标记锚定。

**module_run.log 不可达时的处理**：
直接用 hilog 内 [Hypium] 标记的时间窗（设备时间），跳过 PC 对齐

### 输出

```
Step 4：提取时间窗（用于"一、hilog日志用例详情"）
时间窗来源：hilog [Hypium] 标记（精确时间窗）
所在日志文件：hilog.427.20260630-020003.txt
起始时间：06-30 02:00:04.019，行号：3082
结束时间：06-30 02:00:04.020，行号：3124（specDone标记）
结束标记类型：优先级①（specDone标记）
边界验证：下一个用例start在行3125，未越界

对齐策略：主时钟同步标记（或 hilog文件名时间戳 / ±2s容差）
时钟同步：已同步（或 未同步，需容差匹配）
时间窗（设备时间）：06-26 15:53:48.123 - 06-26 15:53:52.456

⚠️ 注意：时间窗提取信息在"一、hilog日志用例详情"每个用例的「时间窗提取」段落中展示。
```

---

## Step 4 变体：形态④（流程B）时间窗

> 形态④无 module_run.log，时间窗仅从 hilog [Hypium] 标记提取（设备时间），跳过PC对齐。
> 流程B入口见 [Form4_Limited.md](./Form4_Limited.md)。

**与流程A的差异**：
- 起始/结束标记：同 Step 4 方法1（[Hypium]start / specDone end），设备时间
- PC↔设备对齐：**跳过**（无 module_run.log 的 `hdc shell date` 同步行，无 PC 时间）
- Step 3 执行状态分析：**跳过**（无 module_run.log，无法判定 bm install/aa test 链）

**提取方法**（全平台必用 `filter_hilog.py`）：
```bash
# 提取指定用例 [Hypium] 时间窗（起始/结束行号+时间，输出 JSON）
python3 scripts/filter_hilog.py -i <解密hilog> --extract-hypium --testcase <用例名> --json
# 列出所有 [Hypium] 用例时间窗
python3 scripts/filter_hilog.py -i <解密hilog> --extract-hypium
```

**提取内容**：
- `[Hypium]start running case '<用例>'` → 起始时间 + 行号
- `[Hypium]<用例> specDone end print success` → 结束时间 + 行号（优先级①，最精确）
- 设备时间（无需对齐）
- **结束标记优先级①~⑤查找逻辑与流程A完全相同**（specDone优先，禁止仅用 `[fail]`）

**报告标注**："形态④（hilog目录），无PC时间窗，使用设备时间"

> 详细回退顺序见 [time-window.md「module_run.log 不可达时的处理」](../../references/time-window.md)

---

