# 证据链生成约束

> ⚠️ 本文件是证据链生成规则的**单一权威定义**（原 constraints.md 六节 + 七节违规后果）。
> [FailureAndSource.md](../modules/L0_PreAnalysis/FailureAndSource.md) 定义流程步骤，本文件定义规则。二者不重叠：FailureAndSource.md 引用规则编号，不复制规则定义。
> 报告数据真实性 / 自检 / 校验 / 多根因等约束见 [report-constraints.md](./report-constraints.md)。

---

## 目录

- 证据链生成流程
  - 禁止事项清单（import/模块名/domain真实性、源码路径规则、引用链探索）
  - 强制流程清单
  - 自动检查机制
- 违规后果

---

## 证据链生成流程

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

> 时间窗提取的完整规则（结束标记优先级①~⑤、最后一条用例特殊处理、边界验证、报告标注格式）的**权威定义**见 [ExecutionAndTimeWindow.md Step 4 提取时间窗](../modules/L0_PreAnalysis/ExecutionAndTimeWindow.md) 与 [report-constraints.md 二、规则1](./report-constraints.md)。本节仅保留约束要点，不重复示例，避免两处定义漂移（此前此处曾误将"文件末尾"标为优先级④，实为⑤）。

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

## 违规后果

- **报告无效**：需要重新生成
- **定界错误**：可能流转到错误的团队
- **浪费时间**：需要重新分析和验证

---

**约束版本**: 2026-07-15
**强制执行**: 所有报告必须遵守上述约束
**违规后果**: 报告无效，需重新生成
