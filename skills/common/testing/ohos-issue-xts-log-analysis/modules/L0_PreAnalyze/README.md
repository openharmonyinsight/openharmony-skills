# L0_PreAnalyze - 前置分析流程详细说明

> **核心模块**：必须在任何日志切片前完成的前置分析
> 
> **更新时间**：2026-07-09
> **重要更新**：新增源码定位流程（步骤一～步骤四）

## 模块概述

前置分析是 XTS 问题分析的核心阶段，负责：
- 识别输入目录形态
- **定位源码工程（新增）**
- 锁定失败用例
- 确认测试执行状态
- 提取时间窗

**⚠️ 强制要求**：前置分析必须在分层过滤前完成。若测试未执行（install/aa test 失败），则**不做 hilog 切片**——直接定界为环境问题。

---

## Step -1：源码工程定位（新增，优先执行）

> **改进方案**：2026-07-09，基于用户反馈优化源码定位流程

### 背景

**问题发现**：
- AI优先搜索testsuite名称或目录名，导致定位错误
- 目录命名规则与testsuite名不匹配（驼峰 vs 下划线）
- 未利用最精确的信息（testcase名称）

**改进流程**：
```
步骤一：搜索 testcase 名称（最高优先级）
  ↓ 如果唯一 → 100%确定源码文件
  
步骤二：搜索 testsuite 名称
  ↓ 如果唯一 → 100%确定源码文件
  
步骤三：路径交集检查
  ↓ 步骤一 + 步骤二的路径交集 → 如果唯一 → 确定
  
步骤四：搜索 BUILD.gn 中的 hap_name（兜底方案）
  ↓ 最终兜底方案
```

### 定位工具

**脚本路径**：`scripts/locate_xts_source.py`

**调用方式**：
```bash
python3 scripts/locate_xts_source.py \
  --testcase "testWebView_getPercentComplete1006" \
  --testsuite "getPercentComplete" \
  --hap "ActsAceWebPageDownloadCloudServiceControllerGroupTwelveTest.hap" \
  --root "/home/xianf/master/test/xts" \
  --output json
```

### AI操作步骤

**步骤一：搜索 testcase 名称（推荐）**

```bash
# 从日志提取 testcase 名称
# 日志格式: it('testWebView_getPercentComplete1006', ...)

# 搜索命令
grep -r "it('testcase_name'" OH_ROOT/acts --include="*.test.ets" --include="*.test.ts"

# 结果判定
匹配数 = 1 → ✅ 成功，返回源码路径
匹配数 > 1 → 进入步骤二
匹配数 = 0 → 进入步骤二
```

**步骤二：搜索 testsuite 名称**

```bash
# 从日志提取 testsuite 名称
# 日志格式: describe('getPercentComplete', ...)

# 搜索命令（忽略大小写）
grep -ri "describe.*testsuite_name" OH_ROOT/acts --include="*.test.ets"

# 结果判定
匹配数 = 1 → ✅ 成功，返回源码路径
匹配数 > 1 → 进入步骤三
匹配数 = 0 → 进入步骤四
```

**步骤三：路径交集检查**

```bash
# 判断逻辑
如果步骤一和步骤二的路径有交集 → ✅ 返回交集路径
如果无交集 → 进入步骤四
```

**步骤四：搜索 BUILD.gn 中的 hap_name**

```bash
# 从日志提取 HAP 文件名
# 日志格式: bm install ... ActsAceWeb...Test.hap

# 搜索命令（通过BUILD.gn中的hap_name字段）
find OH_ROOT/acts -name "BUILD.gn" -exec grep -l "hap_name.*HAP_NAME" {} \;

# 结果判定
匹配数 = 1 → ✅ 成功，返回项目目录
匹配数 > 1 → 返回候选列表，需人工确认
匹配数 = 0 → ❌ 失败，未找到源码
```

### 实际案例验证

**案例：ActsAceWebPageDownloadCloudServiceControllerGroupTwelveTest**

```bash
# 输入参数
testcase: testWebView_getPercentComplete1006
testsuite: getPercentComplete
hap: ActsAceWebPageDownloadCloudServiceControllerGroupTwelveTest.hap

# 执行结果（步骤一）
[步骤一] 搜索 testcase: testWebView_getPercentComplete1006
  ✓ 唯一匹配: .../ace_web_page_download_cloudservice_controller_group_twelve/.../GetPercentComplete.test.ets

定位结果
============================================================
成功: True
定位步骤: step1
定位方法: testcase_unique
源码文件: .../GetPercentComplete.test.ets
```

**验证结论**：
- ✅ 步骤一唯一匹配，直接定位成功
- ✅ 准确率：100%
- ✅ 效率：一步定位

### 关键改进点

| 改进项 | AI旧方法 | 改进方案 |
|--------|----------|----------|
| **搜索优先级** | Testsuite → 目录名 → HAP名 | **Testcase → Testsuite → 交集 → HAP名** |
| **HAP定位方式** | 目录名转换（易错） | **BUILD.gn搜索（准确）** |
| **唯一性判断** | 无明确判断 | **明确判定匹配数** |
| **准确率** | 低（找到错误文件） | **高（100%正确）** |

### 注意事项

1. **优先搜索 testcase**：testcase是最精确的标识符，唯一性最高
2. **BUILD.gn 搜索**：HAP名不要转换为目录名，直接搜索BUILD.gn中的hap_name字段
3. **编码处理**：读取测试文件时添加 `encoding='utf-8', errors='ignore'`
4. **兜底方案**：步骤四找到项目目录后，会自动搜索测试文件匹配testcase/testsuite

---

## Step 0：识别输入目录形态（4种）

用户输入可能是以下 4 种形态之一。AI**不向上回溯补全**，而是按当前目录的可达文件判定哪些步骤可执行。

### 形态识别方法

**AI操作**：
```bash
ls -la <日志目录>
```

### 形态判定依据

| 形态 | 示例路径 | 识别特征 | 当前目录可达文件 |
|------|----------|----------|-----------------|
| **① 全量报告** | `.../2026-06-26-15-53-21/` | 含 `summary_report.xml` 或 `summary.ini` | summary_report.xml + 所有 log/<mod>/module_run.log + hilog + dict |
| **② log 根** | `.../2026-06-26-15-53-21/log/` | 下全是 `Acts*/` 子目录，无 xml | 所有 module_run.log + hilog + dict（无汇总 xml） |
| **③ 单 testsuite** | `.../log/ActsAACommandImplicitStartTest/` | 含 `module_run.log` | module_run.log + hilog + dict（无汇总 xml） |
| **④ hilog 目录** | `.../Acts.../hilog_FMR0123417000740/` | 含 `hilog.*.gz`，无 `module_run.log` | 仅 hilog*.gz + dict（无 module_run.log、无 xml） |

### 各形态可执行步骤 + 用户需补充信息

| 形态 | 可执行步骤 | 跳过步骤 | 用户须额外提供（缺则降级/中止） |
|------|-----------|---------|--------------------------------|
| ① 全量报告 | Step 0-5 全部 | 无 | 源码路径（建议，非必须） |
| ② log 根 | Step 1(改用 module_run.log FAILED) + 2-5 | Step 1 xml 路径 | 无（自动扫描 FAILED 行）；可指定 testsuite 名缩小范围 |
| ③ 单 testsuite | Step 1(改用 module_run.log FAILED) + 2-5 | Step 1 xml 路径 | 无（单模块）；源码路径（建议） |
| ④ hilog 目录 | Step 5(改用 hilog `[Hypium]` 标记取设备时间窗) | Step 1-4 全跳过 | **必须**：失败用例名 + 源码路径（否则无法定位目标/无法解析 domain） |

**形态④特殊要求**：
- 无 module_run.log → 无法判定执行状态（Step 3）
- 无 PC 时间窗（Step 4）
- 只能用 hilog 内 `[Hypium]start/[Hypium][fail]` 标记取设备时间窗
- **必须由用户提供**失败用例名

---

## Step 0.5：加密文件检测与解密（强制）

> 📖 **详细工具使用**: [docs/tools/hilogtool-guide.md](../../docs/tools/hilogtool-guide.md)

### 加密文件识别

**检测方法**：
```bash
# 检查是否存在加密文件
ls <日志目录>/hilog.*.gz

# 或检查文件类型
file <日志目录>/hilog.*.gz
# 输出: gzip compressed data
```

**加密文件特征**：
- 文件名：`hilog.*.gz` 或 `hilog.*.zst`
- 直接 zcat 显示乱码或二进制内容

### 解密操作（必须执行）

**⚠️ 重要提示**：
- **检测到加密文件 → 必须使用 hilogtool 解密**
- **不要使用 gunzip**（会破坏 GLS_BINARY 结构，导致 std::out_of_range 错误）
- **不要降级处理**（strings 提取不完整）

**hilogtool 工具路径**（skill 已内置）：
```bash
# Linux 环境
~/.opencode/skills/xts-issue-analysis/docs/tools/hilogtool/hilogtool.exe

# Windows 环境
docs/tools/hilogtool/hilogtool.exe
```

**解密命令**：
```bash
# Linux 环境（使用 wine64）
DISPLAY= wine64 ~/.opencode/skills/xts-issue-analysis/docs/tools/hilogtool/hilogtool.exe parse \
    -i <日志目录> \
    -o <日志目录>/parsed \
    -d <日志目录>/hilog_dict.*.zip

# Windows 环境
hilogtool.exe parse -i <日志目录> -o <日志目录>/parsed -d <日志目录>/hilog_dict.*.zip
```

**解密验证**：
```bash
# 检查输出目录
ls <日志目录>/parsed/*.txt

# 统计行数（应该有大量日志）
wc -l <日志目录>/parsed/*.txt
```

**常见问题**：
| 问题 | 解决方案 |
|------|---------|
| `Permission denied` | `chmod +x hilogtool.exe` |
| wine 未安装 | `sudo apt-get install wine64` |
| 首次运行超时 | 先执行 `wine64 --version` 初始化 |
| MIT-SHM 错误 | 设置 `DISPLAY=` 环境变量 |
| 字典文件找不到 | 检查是否存在 `hilog_dict.*.zip` |

---

## Step 1：锁定失败用例（失败信号源）

### 失败信号源优先级

**AI操作**（优先级顺序）：

**方法1（优先）**：从 summary_report.xml 提取
```bash
grep "result=\"false\"" summary_report.xml
```

**解析XML提取**：
- testsuite name
- testcase name
- message（错误信息）

**方法2（回退）**：从 module_run.log 提取
```bash
grep "FAILED" module_run.log
```

**解析日志提取**：
- [Listener] 行中的 testsuite#caseID
- 时间戳

### 判定分支

| 失败信号源状态 | 判定 | 后续操作 |
|---------------|------|---------|
| ①或② 任一可达 | 得失败用例清单 | 继续 Step 2 |
| 两者均不可达 | 无失败信号源 | **必须用户提供用例名，否则中止** |
| 用户指定 testsuite 名称 | 仅分析该 testsuite 内的失败项 | 继续 Step 2 |

### 输出

```
Step 1：锁定失败用例
失败用例数：X个
hap_name（源码定位用）: ActsAceCArkUI16Test  ← 新增：用于 Step 2.5 源码路径定位
失败用例清单：
  1. ActsAACommandImplicitStartTest#SUB_Ability_..._3100
  2. ...
信号源：summary_report.xml（或 module_run.log）
```

**hap_name 提取方法**：
- 形态①②③：从日志目录名提取 `basename <日志目录>`
- 形态④：需用户手动提供（否则无法定位源码）

---

## Step 2：定位 module_run.log + 设备 SN

**AI操作**：

对每个失败 testsuite：
```bash
ls -la log/<modulename>/module_run.log
```

**提取信息**：
- 设备 SN（如 FMR0123417000740，来自 [Hdc] 行）
- bundle name（来自 aa test 命令 -b 参数）

**module_run.log 不可达** → 跳过，标注"无执行链信息"

### 输出

```
Step 2：定位 module_run.log + 设备 SN
testsuite: ActsAACommandImplicitStartTest
module_run.log: log/ActsAACommandImplicitStartTest/module_run.log ✅
设备 SN: FMR0123417000740
bundle name: com.example.actsaac...
```

---

## Step 3：分析 shell 命令执行链（关键定界点）

> 📖 **详细分析说明**: [../docs/workflows/shell-chain-analysis.md](../../docs/workflows/shell-chain-analysis.md)

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

### 输出

```
Step 3：分析 shell 命令执行链
判定结果：测试正常执行（或 install失败 / aa test失败 / 未运行）
证据：
  - bm install：成功（或 失败：xxx）
  - aa test：成功（或 失败：xxx）
  - Collected count：100个用例（或 0个）
  - [Listener]：有逐用例输出（或 无输出）
```

---

## Step 4：提取失败用例时间窗

> 📖 **详细对齐说明**: [../docs/workflows/time-window-alignment.md](../../docs/workflows/time-window-alignment.md)
> 
> **⚠️ 2026-07-10改进**：新增精确结束标记逻辑，避免时间窗越界。

**AI操作**（优先级顺序）：

### 方法1（优先）：从 hilog [Hypium] 标记提取（设备时间，精确时间窗）

**⚠️ 时间窗提取必须包含完整生命周期**（2026-07-10强制改进）：

```bash
# 步骤1：查找起始标记（固定）
grep -n "Hypium.*start running case 'testcase_X'" hilog.txt

# 步骤2：查找结束标记（优先级顺序）
# 优先级①（最精确）：specDone标记
grep -n "Hypium.*testcase_X specDone end print success" hilog.txt

# 优先级②（边界）：下一个用例start标记
grep -n "Hypium.*start running case 'testcase_Y'" hilog.txt
# 结束行号 = 下一个start行号 - 1

# 优先级③（失败）：fail标记（不完全精确）
grep -n "Hypium.*\[fail\]testcase_X" hilog.txt

# 步骤3：边界验证（强制）
# 验证：结束行号 < 下一个用例start行号
```

**结束标记优先级**（强制要求）：
1. **优先级①（最精确）**：`[Hypium]XXX specDone end print success` - 包含完整生命周期
2. **优先级②（边界）**：下一个 `[Hypium]start running case 'YYY'` 前一行
3. **优先级③（失败）**：`[Hypium][fail]XXX` - 包含部分后续日志
4. **优先级④（suite end）**：`OHOS_REPORT_RESULT` - 测试套件结束标记（最后一条用例）
5. **优先级⑤（文件末尾）**：文件总行数 - 最后回退（suite end未找到时）

**提取内容**：
- [Hypium]start running case → 起始时间 + 行号
- [Hypium]XXX specDone end → 结束时间 + 行号（精确）
- 设备时间（无需对齐）
- **边界验证**：下一个用例start标记（确保不越界）
- **最后一条用例判断**：无下一个start时优先使用suite end标记
- **suite end回退**：suite end未找到时使用文件末尾

**⚠️ 禁止事项**：
- ❌ 禁止仅用fail标记作为结束（遗漏specDone日志）
- ❌ 禁止结束行号超过下一个用例start标记
- ❌ 禁止最后一条用例未特殊处理
- ❌ 禁止最后一条用例直接使用文件末尾而未先尝试suite end标记

**最后一条用例的特殊处理**：
- 如果无下一个start标记 → 判断为最后一条用例
- 优先级①（specDone）：仍然可用，优先使用
- 优先级④（suite end）：`OHOS_REPORT_RESULT` 标记（测试套件精确结束）
- 优先级⑤（文件末尾）：suite end未找到时的最后回退
- 报告中标注边界情况和使用的优先级

### 方法2（回退）：从 module_run.log 提取（PC 时间）

```bash
grep "FAILED.*testcase_X" module_run.log
```

**提取内容**：
- 找 [Listener] [... testcase_X FAILED] 行 → 得终止时间 T_end(PC)
- 找上一用例 PASSED/FAILED 行或 aa test 开始行 → 得起始时间 T_start(PC)
- 时间窗 = [T_start, T_end]，均为 PC 端时间

### module_run.log 不可达时的处理

时间窗只能从 hilog 内 [Hypium]start/[specDone end] 提取（设备时间）

### 输出

```
Step 4：提取失败用例时间窗（精确时间窗）
时间窗来源：hilog [Hypium] 标记
起始时间：06-26 15:53:48.123，行号：1234
结束时间：06-26 15:53:52.456，行号：1567（specDone标记）
结束标记类型：specDone标记（优先级①）
边界验证：下一个用例start在1568，未越界 ✅
时间类型：设备时间（或 PC时间，需对齐）
```

---

## Step 5：PC↔设备时间对齐

> 📖 **详细对齐策略**: [../docs/workflows/time-window-alignment.md](../../docs/workflows/time-window-alignment.md)

⚠️ module_run.log 为 PC 时间，hilog 为设备时间，存在毫秒级差。

### 对齐策略（三选一，按优先级）

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

### module_run.log 不可达时的处理

直接用 hilog 内 [Hypium] 标记的时间窗（设备时间），跳过 PC 对齐

### 输出

```
Step 5：PC↔设备时间对齐
对齐策略：主时钟同步标记（或 hilog文件名时间戳 / ±2s容差）
时钟同步：已同步（或 未同步，需容差匹配）
时间窗（设备时间）：06-26 15:53:48.123 - 06-26 15:53:52.456
```

---

## 🔴 无法分析的硬条件（强制检查）

| 必要条件 | 说明 | 缺失后果 |
|---------|------|---------|
| **失败信号源** | `summary_report.xml`、`module_run.log`（含 FAILED 行）、或用户口头指定失败用例名，**三者至少有一** | 无任何失败信号 → **无法定位分析目标，必须中止**并提示用户提供用例名或更完整目录 |
| **至少一份证据** | `module_run.log`、`hilog*.gz`、`result/*.xml`，**三者至少有一** | 三者全无 → **没有任何可分析内容，必须中止** |

> 只要满足上述两项硬条件，即使其他文件缺失，也能产出**至少基于 XML message 或 shell 命令链的定界结论**（精度降级，但可用）。

---

## 输入产物

- 日志目录（任一形态①②③④）
- 源码路径（可选，配置 OH_ROOT）
- 失败用例名（形态④必须用户提供）

## 输出产物

供后续 L2_Filter、L3_Report 使用：
- `failed_cases`：失败用例清单（testsuite/modulename/testcase/message）
- `exec_status`：每个 testsuite 的执行阶段判定（正常执行 / install失败 / aa test失败 / 未运行）
- `time_windows`：每个失败用例的时间窗 [T_start, T_end]（已对齐设备时间）
- `device_sn`：设备 SN（用于定位 hilog 子目录）
- `clock_synced`：PC↔设备时钟是否已同步（布尔）

---

## 关键改进说明

| 对比项 | 原设计 | 新设计 | 改进效果 |
|--------|--------|--------|---------|
| 流程前置 | hilog 切片前不检查执行状态 | 强制前置分析，判定执行状态 | 避免无用切片（环境问题不做切片） |
| 形态识别 | 单一输入形态 | 4种形态自动识别 + 用户补充信息 | 提高适配性 |
| 时间窗对齐 | 不对齐或简单匹配 | 3种策略优先级选择 | 提高时间窗准确性 |

---

**更新时间**：2026-07-06  
**文档来源**：IMPROVEMENT_PLAN.md A-0 章节（第107-235行）  
**设计理念**：前置分析强制执行，测试未执行不做切片  
**改进要点**：
- 2026-07-06：Step 1 输出增加 hap_name 提取，用于 Step 2.5 源码路径定位
- 2026-07-03：前置分析强制执行，测试未执行不做切片