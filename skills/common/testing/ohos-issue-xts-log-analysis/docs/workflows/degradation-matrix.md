# 降级矩阵详细说明

> **核心设计**：质量分级 + 降级路径 + 报告标注

## 概述

降级矩阵定义了 XTS 问题分析在不同文件缺失组合下的分析能力质量分级，以及对应的降级路径和报告标注方式。

---

## 质量分级（L0-L4）

| 质量等级 | 名称 | 分析能力 | 证据链完整性 |
|---------|------|---------|-------------|
| **L0** | 完整域驱动切片 | 时间窗 + domain 精准切片 + 源码验证 | 完整（API→子系统→domain→日志行） |
| **L1** | 域切片无源码 | 时间窗 + domain 精准切片（无源码） | 部分（domain 推断自 testsuite 名） |
| **L2** | shell 命令链定界 | 仅 shell 命令执行链分析 | 基础（执行状态判定） |
| **L3** | 仅 XML message | 仅 summary_report.xml message 文本 | 有限（仅错误文本） |
| **L4** | 盲扫 hilog | 无时间窗，全量日志盲扫 | 低（关键字匹配） |
| **❌** | 无法分析 | 无失败信号源或无证据 | 无（必须中止） |

---

## 输入形态默认质量（文件齐全时）

| 形态 | 可达文件（齐全时） | 默认质量 | 关键限制 |
|------|-------------------|---------|---------|
| **① 全量报告** | summary_report.xml + module_run.log + hilog + dict | **L0** | 无 |
| **② log 根** | 所有 module_run.log + hilog + dict（无汇总 xml） | **L0** | 失败用例靠 module_run.log FAILED 行定位（需逐目录扫描） |
| **③ 单 testsuite** | module_run.log + hilog + dict（无汇总 xml） | **L0** | 仅分析该 testsuite；hilog 域需源码（用户另提供） |
| **④ hilog 目录** | 仅 hilog + dict（无 module_run.log、无 xml） | **L4** 盲扫 | 无法确认执行状态、无 PC 时间窗；**用户须提供失败用例名 + 源码路径**，否则中止 |

---

## 文件缺失组合的降级路径

### 降级矩阵表

| 缺失组合 | 可用分析路径 | 降级质量 | 降级处理 |
|---------|-------------|---------|---------|
| **仅缺 .ets 源码**（用户未提供） | 域切片仍可（API→domain 需源码，缺则用 module 名推断子系统） | **L1** | 报告"源码定位/分析"段标注"未提供源码"；domain 用 testsuite→subsystem_mapping 推断 |
| **仅缺 hilog_dict.zip** | hilog 解密不可用 | **L1\*** | `strings` 提取 + grep 降级解密；报告标注"未解密，精度受限" |
| **缺 summary_report.xml**（②③④形态） | module_run.log FAILED 行定位失败用例 | **L0** | 失败用例靠 `[Listener] FAILED` 行；报告标注"无汇总报告" |
| **缺 module_run.log**（形态④） | 无法做 shell 链定界 + 无 PC 时间窗 | **L4** | ① 时间窗改从 hilog `[Hypium]` 标记提取（设备时间） ② 无法判定执行状态，标注"未确认执行状态" ③ 扩大 domain 备用集范围 ④ **须用户提供失败用例名 + 源码路径** |
| **缺 hilog*.gz**（全缺） | 无设备日志 | **L2/L3** | 仅基于 module_run.log shell 命令链 + XML message 定界；报告标注"无 hilog" |
| **缺 summary_report.xml + module_run.log**（仅 hilog 在，形态④） | 无失败信号源 | **L4** 或 ❌ | **须用户提供失败用例名**，否则无法定位 → 中止；已提供则盲扫 hilog 找 crash/断言（L4） |
| **缺 module_run.log + hilog**（仅 xml 在） | 无可切片日志 | **L3** | 仅基于 XML message 文本定界；报告标注"仅执行结果，无日志" |
| **三者全缺**（xml+module_run.log+hilog） | 无 | ❌ | **中止**，提示用户提供更完整目录 |
| **[Listener] 行缺失**（module_run.log 在但无逐用例结果） | 无法定位具体失败用例 | **L2** | 定界为"测试未正常执行"（指向 shell 链阶段②/③）；不做 hilog 切片 |
| **date 同步行缺失** | PC↔设备时间无法精确对齐 | **L1\*** | 时间窗扩大 ±2s 容差，依赖 hilog `[Hypium]` 标记锚定 |

---

## 形态④专项处理（最受限形态）

### 形态④降级逻辑

```
用户给 hilog_SN/ 目录 → 跳过 Step 1-4，仅 Step 5 改用 hilog [Hypium] 标记取设备时间窗
   ↓ 检查用户是否提供失败用例名 + 源码路径
   ├─ 已提供 → L4 盲扫：按用户指定用例名，从 hilog [Hypium]start/[Hypium][fail] 锚定时间窗 + domain 切片
   │           （无法判定执行状态、无 PC 时间窗，报告标注"未确认执行状态/无 PC 对齐"）
   └─ 未提供 → ❌ 中止，提示用户："该目录仅含 hilog，请补充：失败用例名 + 源码路径"
```

### 形态④报告标注模板

```markdown
## 一、测试执行概况

**分析说明**：形态④（hilog目录），缺少 module_run.log，无法确认执行状态。

**报告质量**：L4（盲扫 hilog）

**降级依据**：
- ❌ 无 summary_report.xml → 无法自动提取失败用例
- ❌ 无 module_run.log → 无法判定执行状态 + 无 PC 时间窗
- ✅ 用户已提供失败用例名 + 源码路径 → 可继续分析
```

---

## 无法分析的硬条件（必须满足其一，否则中止）

| 必要条件 | 说明 | 缺失后果 |
|---------|------|---------|
| **失败信号源** | `summary_report.xml`、`module_run.log`（含 FAILED 行）、或用户口头指定失败用例名，**三者至少有一** | 无任何失败信号 → **无法定位分析目标，必须中止**并提示用户提供用例名或更完整目录 |
| **至少一份证据** | `module_run.log`、`hilog*.gz`、`result/*.xml`，**三者至少有一** | 三者全无 → **没有任何可分析内容，必须中止** |

---

## 报告降级标注模板

### L1 降级标注（无源码）

```markdown
## 三、hilog日志用例详情

**源码定位**：未配置OH_ROOT，无法定位具体源码

**源码分析**：未提供源码，domain 推断自 testsuite 名

**降级说明**：L1（域切片无源码），domain 推断自 testsuite 名 → subsystem_mapping
```

### L2 降级标注（仅 shell 命令链）

```markdown
## 一、测试执行概况

**分析说明**：仅基于 module_run.log shell 命令链分析

**报告质量**：L2（shell 命令链定界）

**降级依据**：
- ❌ 无 hilog 日志 → 无法做日志切片分析
- ✅ module_run.log 存在 → 可做执行状态判定
```

### L3 降级标注（仅 XML message）

```markdown
## 一、测试执行概况

**分析说明**：仅基于 summary_report.xml message 文本分析

**报告质量**：L3（仅 XML message）

**降级依据**：
- ❌ 无 module_run.log → 无法做执行状态判定
- ❌ 无 hilog 日志 → 无法做日志切片分析
- ✅ XML message 存在 → 可提取错误文本

**失败原因**：Error in ..., expect false, error: failed to start ability.
```

### L4 降级标注（盲扫 hilog）

```markdown
## 一、测试执行概况

**分析说明**：形态④（hilog目录），缺少 module_run.log，无法确认执行状态

**报告质量**：L4（盲扫 hilog）

**降级依据**：
- ❌ 无 summary_report.xml → 无法自动提取失败用例
- ❌ 无 module_run.log → 无法判定执行状态 + 无 PC 时间窗
- ✅ 用户已提供失败用例名 → 可继续分析

**时间窗提取**：从 hilog [Hypium] 标记提取（设备时间）
```

### ❌ 中止标注

```markdown
## 无法分析

**中止原因**：
- ❌ 无失败信号源（无 summary_report.xml + 无 module_run.log FAILED 行 + 用户未提供用例名）
- ❌ 无可分析内容（三者全缺：xml + module_run.log + hilog）

**建议用户提供**：
1. 更完整的日志目录（含 summary_report.xml 或 module_run.log）
2. 失败用例名（如 SUB_Ability_..._3100）
3. 源码路径（如 /home/xianf/master/test/xts/acts/ability）
```

---

## AI执行检查清单

| 检查项 | 操作 | 输出 |
|--------|------|------|
| ✅ 检查输入形态 | ls -la <日志目录> | 形态①②③④ |
| ✅ 检查文件可达性 | 检测 summary_report.xml / module_run.log / hilog | 可达文件清单 |
| ✅ 检查失败信号源 | 检测 xml FAILED / module_run.log FAILED / 用户提供 | 失败用例清单或中止 |
| ✅ 检查证据存在性 | 检测 module_run.log / hilog / xml | 至少一份或中止 |
| ✅ 判定质量等级 | 根据降级矩阵判定 | L0-L4 或 ❌ |
| ✅ 输出降级标注 | 生成报告降级说明 | 报告内容 |

---

## 设计理念

**不猜测、不回溯**：
- 缺什么就跳过对应步骤
- 跳过的步骤若影响目标定位（如形态④无法自得失败用例名），则**强制要求用户输入**
- 保证每次分析的输入精确可追溯

---

## 关键改进说明

| 对比项 | 原设计 | 新设计 | 改进效果 |
|--------|--------|--------|---------|
| 质量分级 | 无分级 | L0-L4 + ❌ 分级 | 明确分析能力边界 |
| 降级路径 | 不明确降级处理 | 明确降级矩阵 + 处理方式 | 提高分析鲁棒性 |
| 报告标注 | 无降级标注 | 强制标注降级状态 | 提高报告可信度 |
| 硬条件检查 | 不检查 | 强制检查失败信号源 + 证据 | 避免无用分析 |

---

**更新时间**：2026-07-03  
**文档来源**：IMPROVEMENT_PLAN.md 第246-270行  
**设计理念**：质量分级明确，降级路径清晰，硬条件强制检查