# AI Behavior Constraints

> **强制规则**: AI必须遵守以下约束，违反将导致报告无效

---

## 一、禁止事项清单

### 1. ❌ 禁止猜测import语句

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

### 2. ❌ 禁止猜测模块名

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

### 3. ❌ 禁止瞎编domain值

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

### 4. ❌ 禁止混淆测试框架和被测API

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

### 5. ❌ 禁止跳过内部模块探索

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

### 6. ❌ 禁止错误的时间窗提取（2026-07-10新增）

**问题描述**:
- 仅用 `[Hypium][fail]XXX` 作为结束标记
- 遗漏fail标记后的specDone等后续日志
- 结束行号超过下一个用例start标记（包含其他用例日志）

**强制要求**:
- ✅ **必须**：按优先级①②③顺序查找结束标记
- ✅ **必须**：使用specDone标记作为精确结束（优先级①）
- ✅ **必须**：验证边界（结束行号 < 下一个用例start行号）
- ❌ **禁止**：仅用fail标记作为结束
- ❌ **禁止**：结束行号超过下一个用例start标记

**结束标记优先级**:
```
优先级①（最精确）：[Hypium]XXX specDone end print success
优先级②（边界）：下一个 [Hypium]start running case 'YYY' 前一行
优先级③（失败）：[Hypium][fail]XXX（不完全精确，含部分后续日志）
优先级④（suite end）：OHOS_REPORT_RESULT（测试套件结束标记）
优先级⑤（文件末尾）：文件总行数（最后回退）
```

**正确示例**（testXmlCase001）:
```bash
# 步骤1：查找起始标记
grep -n "Hypium.*start running case 'testXmlCase001'" hilog.427.txt
# 结果：3082 [Hypium]start running case 'testXmlCase001'

# 步骤2：查找结束标记（优先级①）
grep -n "Hypium.*testXmlCase001 specDone end print success" hilog.427.txt
# 结果：3124 [Hypium]testXmlCase001 specDone end print success ← 正确！

# 步骤3：边界验证
grep -n "Hypium.*start running case 'testXmlCase002'" hilog.427.txt
# 结果：3125 [Hypium]start running case 'testXmlCase002'
# 验证：结束行号3124 < 下一个start 3125 ✅ 未越界

# 时间窗：3082-3124（包含完整生命周期）
```

**正确示例**（最后一条用例testLastCase，使用suite end）:
```bash
# 步骤1：查找起始标记
grep -n "Hypium.*start running case 'testLastCase'" hilog.txt
# 结果：60753 [Hypium]start running case 'testLastCase'

# 步骤2：查找结束标记（优先级①）
grep -n "Hypium.*testLastCase specDone end print success" hilog.txt
# 结果：未找到

# 步骤3：查找下一个start标记（优先级②）
grep -n "Hypium.*start running case" hilog.txt | tail -1
# 结果：60753 [Hypium]start running case 'testLastCase' ← 这是最后一个

# 步骤4：判断为最后一条用例，查找suite end（优先级④）
grep -n "OHOS_REPORT_RESULT" hilog.txt
# 结果：43181 OHOS_REPORT_RESULT: stream=Tests run: ... ← suite end标记

# 时间窗：60753-43181（使用suite end标记）
```

**正确示例**（最后一条用例，suite end未找到，回退文件末尾）:
```bash
# 步骤1-3：同上，判断为最后一条用例

# 步骤4：查找suite end（优先级④）
grep -n "OHOS_REPORT_RESULT" hilog.txt
# 结果：未找到

# 步骤5：回退文件末尾（优先级⑤）
wc -l hilog.txt
# 结果：51877
# 结束行号：51877（文件末尾）

# 时间窗：60753-51877（suite end未找到，回退文件末尾）
```

**错误示例**（testXmlCase001）:
```bash
❌ 错误1：仅用fail标记
结束行号：3102 [Hypium][fail]testXmlCase001 ← 错误！
遗漏：3102-3124的specDone等后续日志
结果：时间窗不完整，缺少关键日志

❌ 错误2：超过下一个用例start
结束行号：3130 ← 错误！超过下一个start（3125）
包含：testXmlCase002的日志（行3125-3130）
结果：时间窗越界，包含其他用例日志
```

**错误示例**（最后一条用例）:
```bash
❌ 错误3：最后一条用例未特殊处理
判断：无下一个start标记
错误做法：仅用fail标记作为结束
正确做法：使用文件末尾作为结束（优先级④）
```

**报告标注要求**:
```markdown
#### 时间窗提取

| 项目 | 内容 |
|------|------|
| 起始行号 | 3082 |
| 结束行号 | 3124 |
| 结束标记类型 | specDone标记（优先级①） |
| 边界验证 | 下一个用例start在3125，未越界 ✅ |
``

---

## 二、强制流程清单

### 1. ✅ 证据链生成流程

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

**自动化工具**:
```bash
# 一键生成证据链（自动完成上述步骤）
$ python3 scripts/generate_evidence_chain.py <测试文件>
```

---

### 2. ✅ 报告生成流程

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

## 三、自动检查机制

### 检查点1：import语句来源

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

### 检查点2：domain值来源

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

### 检查点3：模块名准确性

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

## 四、违规处理

### 违规示例识别

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

---

### 违规后果

- **报告无效**：需要重新生成
- **定界错误**：可能流转到错误的团队
- **浪费时间**：需要重新分析和验证

---

## 五、最佳实践

### 1. 使用自动化工具

```bash
# 推荐：一键生成证据链
$ python3 scripts/generate_evidence_chain.py <测试文件>

# 自动完成：
# ✅ 提取import
# ✅ 探索引用链
# ✅ 查询domain
# ✅ 生成Markdown
```

---

### 2. 验证每个步骤

```bash
# 步骤1：验证import提取
$ python3 scripts/extract_imports.py <测试文件>

# 步骤2：验证引用链探索
$ python3 scripts/explore_import_chain.py <测试文件>

# 步骤3：验证domain查询
$ python3 scripts/map_domain.py "<模块名>"
```

---

### 3. 检查报告格式

**必须包含**:
- ✅ import语句（从源码提取）
- ✅ 模块名（从脚本提取）
- ✅ domain值（从脚本提取）
- ✅ 子系统归属（从脚本提取）
- ✅ 查询工具说明

---

**更新时间**: 2026-07-09
**强制执行**: 所有报告必须遵守上述约束
**违规后果**: 报告无效，需重新生成