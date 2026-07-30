# 时间窗对齐策略详细说明

## 目录

- 概述
- 时间来源对比
- 对齐策略（三选一，按优先级）
  - 策略①：主时钟同步标记对齐（优先）
  - 策略②：hilog 文件名时间戳对齐
  - 策略③：同步标记缺失时的容差匹配
- module_run.log 不可达时的处理
- 时间窗提取优先级（强制要求）
- 容差参数表
- 报告输出格式
  - 时间窗提取表格
  - 对齐策略说明
- 常见问题
  - Q1: 同步标记缺失怎么办？
  - Q2: hilog 文件名无时间戳怎么办？
  - Q3: [Hypium] 标记缺失怎么办？
- AI执行检查清单
- 关键改进说明

---

> **关键问题**：module_run.log 为 PC 时间，hilog 为设备时间，存在毫秒级时钟差

## 概述

时间窗对齐是前置分析的关键步骤，用于解决 PC 时间（module_run.log）与设备时间（hilog）之间的时钟差问题。准确的时间窗对齐是分层过滤的基础。

---

## 时间来源对比

| 时间来源 | 类型 | 格式 | 精度 | 特点 |
|---------|------|------|------|------|
| **module_run.log** | PC 时间 | `[YYYY-MM-DD HH:MM:SS,mmm]` | 毫秒级 | PC端记录，可能有时钟差 |
| **hilog [Hypium] 标记** | 设备时间 | `MM-DD HH:MM:SS.mmm` | 毫秒级 | 设备端记录，精确但无年份 |
| **hilog 文件名** | 设备时间 | `hilog.XXX.20260626-HHMMSS.gz` | 秒级 | 文件名含设备时间戳 |

---

## 对齐策略（三选一，按优先级）

### 策略①：主时钟同步标记对齐（优先）

**适用条件**：module_run.log 首行含 `hdc shell date` 同步标记

**原理**：
- module_run.log 首行 `hdc shell date '2026-06-26 15:53:44'` 为 PC 下发的时间
- 该时刻起设备时钟被强制同步为 PC 时间
- 此后 PC↔设备时钟差≈0（仅漂移毫秒级）

**AI操作**：
```bash
grep "hdc shell date" module_run.log
```

**判定**：
- 若含 date 同步行 → **直接用 PC 时间窗匹配 hilog**
- 时钟差 ≈ 0（仅毫秒级漂移）

**示例**：
```text
# module_run.log（PC时间）
[2026-06-26 15:53:44,232] [Hdc] hdc shell date '2026-06-26 15:53:44'  ← 同步标记
[2026-06-26 15:53:52,973] [Listener] [... SUB_..._3100 FAILED]        ← 失败用例时间

# hilog（设备时间）
hilog.027.20260626-155352.gz  ← 文件名含设备时间 15:53:52（与PC时间一致）
```

**对齐结果**：
- PC 时间窗 = 设备时间窗（一致）
- 容差 = ±500ms（漂移补偿）

---

### 策略②：hilog 文件名时间戳对齐

**适用条件**：无同步标记，但 hilog 文件名含时间戳

**原理**：
- hilog 文件名含设备时间（`hilog.027.20260626-155352.gz` → 15:53:52）
- 据此选择覆盖时间窗的 hilog 文件
- 对内部日志做 ±500ms 容差匹配

**AI操作**：
```bash
ls -la hilog.*.gz
# 提取文件名时间戳
```

**示例**：
```text
# module_run.log（PC时间）
[2026-06-26 15:53:52,973] [Listener] [... SUB_..._3100 FAILED]  ← PC时间：15:53:52

# hilog 文件名（设备时间）
hilog.026.20260626-155340.gz  ← 设备时间：15:53:40
hilog.027.20260626-155352.gz  ← 设备时间：15:53:52（匹配！）
```

**对齐操作**：
- 选择 `hilog.027.20260626-155352.gz`（覆盖失败时间）
- 容差 = ±500ms

---

### 策略③：同步标记缺失时的容差匹配

**适用条件**：无同步标记，无 hilog 文件名时间戳，或时间戳不完整

**原理**：
- 扩大时间窗 ±2s 容差
- 依赖 hilog 内 `[Hypium]start running case` 标记锚定

**AI操作**：
```bash
# 扩大时间窗
# PC 时间窗：15:53:52
# 设备时间窗：15:53:50 - 15:53:54（±2s 容差）

# 锚定标记
grep -n "Hypium.*start.*SUB_..._3100" hilog.txt
```

**示例**：
```text
# PC 时间窗（module_run.log）
起始：15:53:48
结束：15:53:52

# 设备时间窗（扩大容差）
起始：15:53:46（-2s）
结束：15:53:54（+2s）

# 锚定标记（hilog）
行1234: 06-26 15:53:48.123 ... [Hypium]start running case 'SUB_..._3100'
行1567: 06-26 15:53:52.456 ... [Hypium][fail]SUB_..._3100
```

**对齐结果**：
- 用 [Hypium] 标记精确锚定
- 容差 = ±2s（保守匹配）

---

## module_run.log 不可达时的处理

**适用场景**：形态④（hilog 目录），无 module_run.log

**处理方式**：
- **直接用 hilog [Hypium] 标记的时间窗**（设备时间）
- **跳过 PC 对齐**
- 报告标注："形态④（hilog目录），无PC时间窗，使用设备时间"

**AI操作**（2026-07-10改进：精确时间窗提取）：
```bash
# 步骤1：提取起始标记
grep -n "Hypium.*start running case 'SUB_..._3100'" hilog.txt

# 步骤2：提取结束标记（优先级顺序）
# 优先级①：specDone标记（最精确）
grep -n "Hypium.*SUB_..._3100 specDone end print success" hilog.txt

# 优先级②：下一个用例的start标记（边界）
grep -n "Hypium.*start running case 'SUB_..._3200'" hilog.txt

# 优先级③：fail标记（失败标记）
grep -n "Hypium.*\[fail\]SUB_..._3100" hilog.txt

# 优先级④：suite end标记（测试套件结束，新增）
grep -n "OHOS_REPORT_RESULT" hilog.txt

# 优先级⑤：文件末尾（最后一条用例的最后回退）
# 如果suite end未找到，使用文件末尾
if [ -z "$(grep 'Hypium.*start running case' hilog.txt | tail -1 | grep 'SUB_..._3100')" ]; then
    # 优先级④：suite end标记
    suite_end=$(grep -n "OHOS_REPORT_RESULT" hilog.txt)
    
    # 优先级⑤：文件末尾（如果suite end未找到）
    if [ -z "$suite_end" ]; then
        wc -l hilog.txt
        # 结束行号 = 文件总行数
    fi
fi
```

**⚠️ 强制要求**：
- 结束标记必须按优先级①②③④⑤顺序查找
- 禁止仅用fail标记作为结束（会遗漏specDone日志）
- 必须验证边界（不超过下一个用例start标记）
- 必须判断是否为最后一条用例（特殊处理）

**最后一条用例的特殊处理**：
- 如果无下一个start标记 → 判断为最后一条用例
- 优先级①（specDone）：仍然可用，优先使用
- 优先级④（suite end）：`OHOS_REPORT_RESULT` 标记（测试套件精确结束）
- 优先级⑤（文件末尾）：suite end未找到时的最后回退

---

## 时间窗提取优先级（强制要求）

| 优先级 | 时间窗来源 | 适用形态 | 精度 | 对齐需求 |
|--------|-----------|---------|------|---------|
| **1（最高）** | hilog [Hypium] 标记 | 所有形态 | 高（设备时间+行号） | 无需对齐 |
| **2（回退）** | module_run.log [Listener] | 形态①②③ | 中（PC时间） | 需对齐 |

**强制要求**：优先使用 hilog [Hypium] 标记，缺失时回退 module_run.log

---

## 容差参数表

| 策略 | 容差范围 | 适用条件 |
|------|---------|---------|
| 策略① | ±500ms | 有同步标记，时钟差≈0 |
| 策略② | ±500ms | 有 hilog 文件名时间戳 |
| 策略③ | ±2s | 无同步标记，需保守匹配 |

---

## 报告输出格式

### 时间窗提取表格

在报告"一、hilog日志用例详情"章节中，输出以下信息：

```markdown
#### 时间窗提取（设备时间）
- **起始时间**: 06-27 09:24:03.900（行13886）
- **结束时间**: 06-27 09:24:06.917（行14016）
- **时间来源**: hilog `[Hypium]start/[fail]`标记
- **PID/TID**: 38894/38894
```

### 对齐策略说明

若有对齐操作，输出：

```markdown
#### PC↔设备时间对齐
- **对齐策略**: 主时钟同步标记（或 hilog文件名时间戳 / ±2s容差）
- **时钟同步**: 已同步（或 未同步，需容差匹配）
- **时间窗（设备时间）**: 06-26 15:53:48.123 - 06-26 15:53:52.456
```

---

## 常见问题

### Q1: 同步标记缺失怎么办？

**解决**：使用策略②（hilog 文件名时间戳）或策略③（±2s 容差）

### Q2: hilog 文件名无时间戳怎么办？

**解决**：使用策略③（±2s 容差），依赖 [Hypium] 标记锚定

### Q3: [Hypium] 标记缺失怎么办？

**解决**：
- 回退 module_run.log [Listener] 时间
- 使用策略③（±2s 容差）
- 报告标注降级状态

---

## AI执行检查清单

| 检查项 | 操作 | 输出 |
|--------|------|------|
| ✅ 检查同步标记 | grep "hdc shell date" module_run.log | 有/无同步标记 |
| ✅ 检查 hilog 文件名 | ls -la hilog.*.gz + 提取时间戳 | 文件名时间戳 |
| ✅ 提取 [Hypium] 标记 | grep -n "Hypium.*start/fail" hilog.txt | 设备时间+行号 |
| ✅ 选择对齐策略 | 根据条件选择策略①②③ | 对齐策略类型 |
| ✅ 计算时间窗 | 根据策略计算时间窗 | 设备时间窗 |
| ✅ 输出时间窗信息 | 生成时间窗表格 | 报告内容 |

---

## 关键改进说明

| 对比项 | 原设计 | 新设计 | 改进效果 |
|--------|--------|--------|---------|
| 时间窗来源 | module_run.log 优先 | hilog [Hypium] 标记优先 | 更准确（设备时间+行号） |
| 对齐策略 | 无对齐 | 3种策略优先级选择 | 提高时间窗准确性 |
| 容差参数 | 无容差 | ±500ms / ±2s 分级容差 | 兼顾精度与覆盖 |
| **结束标记逻辑（20260710新增）** | 仅用fail标记 | 优先级①②③④四级结束标记 | 精确时间窗，避免越界 |

**2026-07-10改进：精确结束标记逻辑**

**问题背景**：
- 原逻辑仅用 `[Hypium][fail]XXX` 作为结束标记
- 但fail标记后还有specDone等后续日志
- 导致结束行号错误（如testXmlCase001：3102→应到3124）

**改进方案**：
- 新增四级结束标记优先级（specDone > next_start > fail > file_end）
- 强制边界验证（不超过下一个用例start）
- 新增最后一条用例的特殊处理（优先级④）
- 报告中标注结束标记类型和边界验证结果

**示例对比**：
```text
❌ 原逻辑（仅用fail标记）：
起始：3082 [Hypium]start running case 'testXmlCase001'
结束：3102 [Hypium][fail]testXmlCase001 ← 遗漏后续日志
下一个用例：3125 [Hypium]start running case 'testXmlCase002'

✅ 新逻辑（使用specDone标记）：
起始：3082 [Hypium]start running case 'testXmlCase001'
结束：3124 [Hypium]testXmlCase001 specDone end ← 包含完整生命周期
边界验证：下一个用例在3125，未越界 ← 正确

✅ 最后一条用例（使用suite end标记）：
起始：60753 [Hypium]start running case 'testLastCase'
结束：43181 OHOS_REPORT_RESULT: stream=Tests run: ... ← suite end标记（优先级④）
边界情况：最后一条用例，使用suite end精确结束
时间窗：60753-43181

✅ 最后一条用例（suite end未找到，回退文件末尾）：
起始：60753 [Hypium]start running case 'testLastCase'
结束：51877（文件末尾）← 优先级⑤，suite end未找到
边界情况：最后一条用例，suite end未找到，回退文件末尾
时间窗：60753-51877
```

**四级结束标记优先级**：
1. **优先级①（最精确）**：`[Hypium]XXX specDone end print success`
   - 包含完整生命周期
   - 最精确的结束位置
   
2. **优先级②（边界）**：下一个 `[Hypium]start running case 'YYY'` 前一行
   - 用例边界，避免包含下一个用例日志
   
3. **优先级③（失败）**：`[Hypium][fail]XXX`
   - 包含部分后续日志（不完全精确）
   - 仅在优先级①②未找到时使用
   
4. **优先级④（suite end，新增）**：`OHOS_REPORT_RESULT` 标记
   - 测试套件结束标记
   - 最后一条用例的精确结束
   - 格式：`OHOS_REPORT_RESULT: stream=Tests run: XXX, Failure: YYY, ...`
   
5. **优先级⑤（文件末尾，降级）**：文件总行数
   - 最后的回退方案
   - 仅在suite end未找到时使用

---

**更新时间**：2026-07-10  
**文档来源**：IMPROVEMENT_PLAN.md 第221-232行 + 2026-07-10时间窗精确提取改进 + 最后一条用例边界情况补充（suite end标记）  
**设计理念**：优先设备时间，分级对齐策略，保守容差匹配，精确结束标记，边界情况处理（suite end优先，文件末尾回退）
