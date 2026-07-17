# AI行为约束（L0_Standard流程）

> **适用模块**: L0_Standard Step 4-5（时间窗提取 + 分层过滤）  
> **强制执行**: 所有AI在执行Step 4-5时必须遵守  
> **违反后果**: 报告无效，需重新生成

---

## 0. 时间窗提取强制（Step 4，2026-07-10新增）

### ✅ 正确行为

**时间窗提取优先级**（强制要求）：
```bash
# 步骤1：查找起始标记（固定）
grep -n "Hypium.*start running case 'testcase_X'" hilog.txt
# 结果：起始行号

# 步骤2：查找结束标记（优先级顺序）
# 优先级①（最精确）：specDone标记
grep -n "Hypium.*testcase_X specDone end print success" hilog.txt

# 优先级②（边界）：下一个用例start标记
grep -n "Hypium.*start running case 'testcase_Y'" hilog.txt
# 结束行号 = 下一个start行号 - 1

# 优先级③（失败）：fail标记（不完全精确）
grep -n "Hypium.*\[fail\]testcase_X" hilog.txt

# 优先级④（suite end）：测试套件结束标记
# 判断是否为最后一条用例
if [ -z "$(grep 'Hypium.*start running case' hilog.txt | tail -1 | grep 'testcase_X')" ]; then
    echo "✅ 这是最后一条用例"
    grep -n "OHOS_REPORT_RESULT" hilog.txt
fi

# 优先级⑤（文件末尾）：最后的回退方案
# 如果suite end未找到
if [ -z "$(grep 'OHOS_REPORT_RESULT' hilog.txt)" ]; then
    wc -l hilog.txt
    # 结束行号 = 文件总行数
fi

# 步骤3：边界验证（强制）
if [ <结束行号> -ge <下一个start行号> ]; then
    echo "❌ 错误：结束行号超过下一个用例start，时间窗越界"
fi
```

**强制要求**：
- ✅ 按优先级①②③④⑤顺序查找结束标记
- ✅ 优先使用specDone标记（包含完整生命周期）
- ✅ 验证边界（结束行号 < 下一个用例start行号）
- ✅ 判断是否为最后一条用例（特殊处理）
- ✅ 最后一条用例优先使用suite end标记（OHOS_REPORT_RESULT）
- ✅ suite end未找到时回退文件末尾
- ✅ 报告中标注结束标记类型和边界验证结果

### ❌ 禁止行为

**禁止事项**：
1. ❌ 禁止仅用fail标记作为结束（遗漏specDone日志）
2. ❌ 禁止结束行号超过下一个用例start标记（包含其他用例日志）
3. ❌ 禁止跳过边界验证
4. ❌ 禁止最后一条用例未特殊处理（无下一个start时未使用suite end或文件末尾）
5. ❌ 禁止最后一条用例直接使用文件末尾而未先尝试suite end标记

**错误示例1**（仅用fail标记）：
```markdown
起始行号：3082 [Hypium]start running case 'testXmlCase001'
结束行号：3102 [Hypium][fail]testXmlCase001 ← ❌ 错误！

实际结束：3124 [Hypium]testXmlCase001 specDone end ← 正确位置
遗漏范围：3102-3124的22行日志（specDone等）
```

**错误示例2**（超过下一个start）：
```markdown
起始行号：3082 [Hypium]start running case 'testXmlCase001'
结束行号：3130 ← ❌ 错误！

下一个start：3125 [Hypium]start running case 'testXmlCase002'
越界范围：3125-3130的6行日志（testXmlCase002的日志）
```

**错误示例3**（最后一条用例未特殊处理）：
```markdown
最后一条用例：testLastCase
无下一个start标记 ← 未判断为最后一条用例

❌ 错误做法：仅用fail标记作为结束
✅ 正确做法：优先使用suite end标记（OHOS_REPORT_RESULT），未找到时回退文件末尾
```

**错误示例4**（最后一条用例直接使用文件末尾）：
```markdown
最后一条用例：testLastCase
suite end标记存在：43181 OHOS_REPORT_RESULT ← 未使用

❌ 错误做法：直接使用文件末尾（51877）
✅ 正确做法：优先使用suite end标记（43181），更精确
```

**正确示例**（使用specDone标记）：
```markdown
起始行号：3082 [Hypium]start running case 'testXmlCase001'
结束行号：3124 [Hypium]testXmlCase001 specDone end ← ✅ 正确！

边界验证：下一个start在3125，未越界 ✅
结束标记类型：specDone标记（优先级①）
时间窗：3082-3124（包含完整生命周期）
```

**正确示例**（最后一条用例，使用suite end）：
```markdown
起始行号：60753 [Hypium]start running case 'testLastCase'
结束行号：43181 OHOS_REPORT_RESULT: stream=Tests run: ... ← ✅ 正确！

边界情况：最后一条用例，无下一个start
结束标记类型：suite end标记（优先级④）
时间窗：60753-43181（使用suite end标记）
```

**正确示例**（最后一条用例，suite end未找到，回退文件末尾）：
```markdown
起始行号：60753 [Hypium]start running case 'testLastCase'
结束行号：51877（文件末尾）← ✅ 正确！

边界情况：最后一条用例，suite end未找到
结束标记类型：文件末尾（优先级⑤）
时间窗：60753-51877（suite end未找到，回退文件末尾）
```

**报告标注要求**：
```markdown
#### 时间窗提取

| 项目 | 内容 |
|------|------|
| 起始行号 | 3082 |
| 结束行号 | 3124 |
| 结束标记类型 | specDone标记（优先级①） |
| 边界验证 | 下一个用例start在3125，未越界 ✅ |
```

---

## 1. 分层过滤验证强制（Step 5）

### ✅ 正确行为

**验证流程**：
```bash
# 步骤1：执行domain过滤
grep -n -E '<domain正则>' time_window_slice.txt

# 步骤2：立即验证grep结果（强制）
primary_lines=$(grep -c -E '<domain正则>' time_window_slice.txt)

# 步骤3：如实报告
if [ "$primary_lines" -eq 0 ]; then
    # 明确报告：时间窗内未找到domain日志
    echo "⚠️ 主分析集为空：时间窗内未找到domain日志"
    echo "统计：主: 0行"
else
    # 提取日志，标记[主]
    echo "统计：主: $primary_lines行"
    grep -n -E '<domain正则>' time_window_slice.txt | \
    awk -F: '{print "[主] 行" $1 ": " $2}'
fi
```

**强制要求**：
- ✅ 执行grep后，立即验证结果行数
- ✅ 结果为空 → 明确报告"时间窗内未找到domain日志"
- ✅ 结果非空 → 提取日志，标记[主]，统计行数

### ❌ 禁止行为

**禁止事项**：
1. ❌ 禁止跳过验证步骤
2. ❌ 禁止在grep空结果时猜测应该有日志
3. ❌ 禁止使用XXX占位符表示"应该有但没找到"

**错误示例**：
```markdown
**关键证据**:
```
行241: [Hypium] specStart: testDuplexCork0003
行XXX: [C003F00] Stream API调用 ← ❌ AI猜测，用XXX占位符
行XXX: [Hypium][fail] expect undefined equals 401 ← ❌ AI猜测
行352: [Hypium] specDone: testDuplexCork0003
```
```

**正确示例**：
```markdown
**分层过滤结果**:
- 主分析集（domain匹配）：**0行**
- ⚠️ 时间窗内未找到domain C003F00日志

**关键证据**:
```
行241: [Hypium] specStart: testDuplexCork0003
行252: [P1] 12345 67890 其他子系统日志... ← ✅ 明确标记来源
行352: [Hypium] specDone: testDuplexCork0003
```

**说明**：
- ⚠️ **时间窗内未找到domain日志** ← ✅ 明确说明
```

---

## 2. 分层标记强制

### ✅ 正确行为

**分层标记格式**：
- `[主]` - 主分析集（domain匹配）
- `[P1]` - P1扩展（同PID/TID）
- `[P2]` - P2扩展（同PID不同TID）
- `[P3]` - P3扩展（位置窗口±20行）

**标记示例**：
```markdown
**关键证据**（带分层来源标记）:
```
[主] 行47: ... C00310/UiTestKit: findComponent failed ...
[P1] 行52: ... C00310/UiTestKit: component not found ...
[P2] 行61: ... C0013xx/Ams: ability launched ...
[P3] 行58: ... (上下文) ...
```
```

**强制要求**：
- ✅ 所有日志摘录必须带分层来源标记
- ✅ 必须报告分层统计表格
- ✅ 必须说明分层来源含义

### ❌ 禁止行为

**禁止事项**：
1. ❌ 禁止省略分层来源标记
2. ❌ 禁止省略分层统计报告
3. ❌ 禁止仅展示日志摘录不带标记

**错误示例**：
```markdown
**关键证据**:
```
行47: ... C00310/UiTestKit: findComponent failed ... ← ❌ 缺少分层标记
行52: ... C00310/UiTestKit: component not found ... ← ❌ 缺少分层标记
```
```

---

## 3. 如实报告强制

### ✅ 正确行为

**如实报告原则**：
- ✅ 如实报告实际情况（主分析集是否为空）
- ✅ 明确说明扩展触发原因
- ✅ 用户可追溯证据链来源

**正确示例**：
```markdown
**分层过滤统计**:

| 分层来源 | 行数 | 说明 |
|---------|------|------|
| 主分析集（domain匹配） | **0行** | ⚠️ 时间窗内未找到domain日志 |
| P1扩展（同PID/TID） | 23行 | 同线程因果链 |
| P2扩展（同PID不同TID） | 12行 | 同进程跨线程 |
| P3扩展（位置窗口±20行） | 40行 | 上下文兜底 |

> **说明**: 主分析集为0行，已执行P1/P2/P3扩展，所有摘录带分层来源标记
```

### ❌ 禁止行为

**禁止事项**：
1. ❌ 禁止猜测日志内容
2. ❌ 禁止隐瞒日志缺失情况
3. ❌ 禁止让用户无法判断日志是否存在

**错误示例**：
```markdown
**关键证据**:
```
行XXX: [C003F00] Stream API调用 ← ❌ 隐瞒日志缺失，猜测应该有日志
```

**说明**: 摘录关键失败日志 ← ❌ 未说明日志是否真的存在
```

---

## 4. 扩展触发强制

### ✅ 正确行为

**扩展触发条件**：
- 主分析集为0行 → **强制触发**P1/P2/P3扩展
- 主分析集非0但规则匹配失败 → 可选触发扩展

**扩展执行流程**：
```bash
# 触发扩展
if [ "$primary_lines" -eq 0 ]; then
    echo "⚠️ 主分析集为空，执行P1/P2/P3扩展..."
    
    # P1扩展：同(PID,TID)
    grep -n "<PID> <TID>" time_window_slice.txt | \
    awk -F: '{print "[P1] 行" $1 ": " $2}'
    
    # P2扩展：同PID不同TID
    grep -n "<PID>" time_window_slice.txt | grep -v "<TID>" | \
    awk -F: '{print "[P2] 行" $1 ": " $2}'
    
    # P3扩展：位置窗口±20行
    sed -n '<行号-20>,<行号+20>p' time_window_slice.txt | \
    awk '{print "[P3] 行" NR+<起始行号-1> ": " $0}'
fi
```

### ❌ 禁止行为

**禁止事项**：
1. ❌ 禁止主分析集为空时不执行扩展
2. ❌ 禁止扩展日志不带分层标记
3. ❌ 禁止不统计扩展行数

---

## 5. 验证清单

AI在执行Step 5后，必须自我检查：

### ✅ 必须项

- ✅ 是否执行了grep验证步骤？
- ✅ 是否如实报告主分析集行数（0或非0）？
- ✅ 是否明确说明"时间窗内未找到domain日志"（如为空）？
- ✅ 是否执行P1/P2/P3扩展（如主分析集为空）？
- ✅ 是否标记分层来源（[主]/[P1]/[P2]/[P3]）？
- ✅ 是否报告分层统计表格？

### ❌ 禁止项

- ❌ 是否使用了XXX占位符？（应该不出现）
- ❌ 是否猜测日志内容？（应该如实报告）
- ❌ 是否省略分层标记？（应该全部标记）
- ❌ 是否省略分层统计？（应该强制报告）

---

## 6. 常见错误对照

### 错误类型1：猜测日志（XXX占位符）

**触发场景**: grep空结果时，AI猜测应该有日志

**错误输出**:
```markdown
行XXX: [C003F00] Stream API调用 ← ❌ AI猜测
```

**正确输出**:
```markdown
⚠️ 时间窗内未找到domain C003F00的日志记录 ← ✅ 明确说明
[P1] 行252: 其他子系统日志 ← ✅ 执行扩展
```

---

### 错误类型2：省略分层标记

**触发场景**: 摘录日志时不标记来源

**错误输出**:
```markdown
行47: C00310/UiTestKit: findComponent failed ← ❌ 缺少标记
```

**正确输出**:
```markdown
[主] 行47: C00310/UiTestKit: findComponent failed ← ✅ 明确标记
```

---

### 错误类型3：隐瞒日志缺失

**触发场景**: 主分析集为空时不说明

**错误输出**:
```markdown
**关键证据**: ... ← ❌ 未说明日志是否存在
```

**正确输出**:
```markdown
**分层过滤结果**: 主分析集: **0行** ← ✅ 明确报告
⚠️ 时间窗内未找到domain日志 ← ✅ 明确说明
```

---

**约束文档生成时间**: 2026-07-10  
**强制执行**: 所有AI必须遵守  
**违反后果**: 报告无效，需重新生成