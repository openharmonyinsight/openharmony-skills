# R018: testcase重复

- **规则编号**: R018
- **严重级别**: Critical
- **规则复杂度**: complex（需要文件级分析）
- **问题类型**: 一个describe下不允许testcase（@tc.name）重复
- **修复方式**: 保留首个testcase不变，后续重复的追加`Adapt{三位数字}`后缀，并同步更新`@tc.name`
- **预期问题数量**: 500+

## 修复历史

| 版本 | 日期 | 修复内容 |
|------|------|---------|
| v1.1.0 | 2026-03-11 | 文件类型修复：添加`.test.js`文件类型扫描（storage目录51%的测试文件为.js格式，此前全部遗漏） |
| v3.4.0 | 2026-03-12 | 正则表达式修复：添加`\b`单词边界，消除`split()`、`submit()`、`visit()`等误报（减少730个误报，85.9%） |
| v3.4.0 | 2026-03-12 | 合并报告：同一组重复只报告第一个出现位置，修复建议中列出所有重复行号 |

## 扫描范围

仅扫描测试文件：
- `.test.ets` - ArkTS测试文件
- `.test.ts` - TypeScript测试文件
- `.test.js` - JavaScript测试文件

**检测范围**：仅在同一个文件内的同一个describe块中检查@tc.name重复，**不跨文件检查**。

## 与R011的区别

| 规则 | 检测对象 | 检测范围 | 修复后缀 |
|------|----------|----------|---------|
| R011 | testsuite（`describe`的第一个参数） | 同一独立工程内（跨文件检测） | `Adapt{N}` |
| R018 | testcase（`it`的第一个参数 / `@tc.name`） | 仅当前文件内同一describe块（不跨文件检测） | `Adapt{N}` |

## 问题描述

在同一个describe块内，多个`it()`函数使用了相同的testcase名称（`@tc.name`或`it()`的第一个参数）。这会导致测试执行时无法区分不同的测试用例。

## 检测逻辑

### 核心算法

```python
import re

IT_NAME_PATTERN = re.compile(r'\bit\s*\(\s*([\'"])([^\'"]+)\1')
DESCRIBE_PATTERN = re.compile(r'\bdescribe\s*\(\s*([\'"])([^\'"]+)\1')

def scan_r018(file_path: str, content: str) -> list:
    """
    扫描文件中同一describe块内重复的testcase名称。

    检测逻辑：
    1. 识别文件中所有describe块的边界
    2. 在每个describe块内，提取所有it()的第一个参数
    3. 检查是否有重复的testcase名称
    4. 只为每组重复的第一个出现位置创建问题报告
    5. 修复建议中列出所有重复位置的行号

    Args:
        file_path: 文件相对路径
        content: 文件完整内容

    Returns:
        问题列表
    """
    issues = []
    lines = content.split('\n')

    # 步骤1：识别describe块边界
    describe_blocks = identify_describe_blocks(lines)

    # 步骤2：在每个describe块内检查testcase重复
    for desc_block in describe_blocks:
        block_issues = check_duplicates_in_block(file_path, lines, desc_block)
        issues.extend(block_issues)

    return issues
```

### 识别describe块边界

```python
def identify_describe_blocks(lines: list) -> list:
    """
    识别文件中所有describe块的行范围。

    使用状态机正确处理嵌套describe和大括号计数，
    跳过字符串字面量中的大括号。

    Returns:
        [{'start': int, 'end': int, 'name': str}]
        start和end为行索引（0-based，包含边界行）
    """
    blocks = []
    stack = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 匹配describe函数调用
        desc_match = re.search(r'\bdescribe\s*\(\s*([\'"])([^\'"]+)\1', stripped)
        if desc_match:
            desc_name = desc_match.group(2)
            stack.append({
                'start': i,
                'name': desc_name,
                'brace_depth': 0,
                'found_first_brace': False,
            })
            continue

        # 处理栈顶describe块的大括号
        if stack:
            in_single = False
            in_double = False
            j = 0
            while j < len(line):
                c = line[j]
                if c == '\\' and (in_single or in_double):
                    j += 2
                    continue
                if c == "'" and not in_double:
                    in_single = not in_single
                elif c == '"' and not in_single:
                    in_double = not in_double
                elif not in_single and not in_double:
                    if c == '{':
                        stack[-1]['brace_depth'] += 1
                        stack[-1]['found_first_brace'] = True
                    elif c == '}':
                        stack[-1]['brace_depth'] -= 1
                j += 1

            # 检查describe块是否结束
            if (stack[-1]['found_first_brace'] and
                    stack[-1]['brace_depth'] <= 0):
                block = stack.pop()
                blocks.append({
                    'start': block['start'],
                    'end': i,
                    'name': block['name'],
                })

    return blocks
```

### 在describe块内检查重复

```python
def check_duplicates_in_block(file_path: str, lines: list,
                               desc_block: dict) -> list:
    """
    在一个describe块内检查testcase名称重复。

    只为每组重复的第一个出现位置创建报告，
    修复建议中列出所有重复位置的行号。

    Args:
        file_path: 文件相对路径
        lines: 文件所有行
        desc_block: describe块信息 {'start', 'end', 'name'}

    Returns:
        问题列表
    """
    issues = []
    seen = {}  # tc_name -> first_line_idx
    all_occurrences = {}  # tc_name -> [line_idx, ...]

    for i in range(desc_block['start'], desc_block['end'] + 1):
        line = lines[i]
        match = IT_NAME_PATTERN.search(line)
        if match:
            tc_name = match.group(2)
            if tc_name not in seen:
                seen[tc_name] = i
                all_occurrences[tc_name] = [i]
            else:
                all_occurrences[tc_name].append(i)

    # 只为有重复的testcase创建报告
    for tc_name, occurrence_lines in all_occurrences.items():
        if len(occurrence_lines) < 2:
            continue

        first_line = occurrence_lines[0]
        duplicate_lines = occurrence_lines[1:]
        duplicate_line_nums = [l + 1 for l in duplicate_lines]

        snippet = lines[first_line].strip()
        if len(snippet) > 120:
            snippet = snippet[:120] + '...'

        # 构建修复建议，列出所有重复行号
        dup_str = ', '.join(str(n) for n in duplicate_line_nums)
        suggestion = (
            f"路径: {file_path}, 行号: {first_line + 1}, "
            f"问题描述: testcase '{tc_name}' 在describe '{desc_block['name']}' 内重复 "
            f"{len(occurrence_lines)} 次。"
            f"与当前文件第{dup_str}行重复，修改testcase名称，确保describe内唯一。"
        )

        issues.append({
            'rule': 'R018',
            'type': 'testcase重复',
            'severity': 'Critical',
            'file': file_path,
            'line': first_line + 1,
            'testcase': tc_name,
            'snippet': snippet,
            'suggestion': suggestion,
        })

    return issues
```

## 正则表达式陷阱

### 必须使用\b单词边界

**问题**：如果不使用`\b`单词边界，正则表达式会错误匹配`split(`、`submit(`、`visit()`等非`it()`调用。

**错误正则**（无`\b`）：
```python
pattern = r'it\s*\(\s*([\'"])([^\'"]+)\1'
# 会匹配:
#   it('test001', ...)   ← 正确
#   split(':')           ← 错误！"it"匹配了split中的子串
#   submit()             ← 错误！
#   visit()              ← 错误！
```

**正确正则**（有`\b`）：
```python
pattern = r'\bit\s*\(\s*([\'"])([^\'"]+)\1'
# 只匹配:
#   it('test001', ...)   ← 正确
#   split(':')           ← 不匹配 ✓
#   submit()             ← 不匹配 ✓
#   visit()              ← 不匹配 ✓
```

**修复效果**：
| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| 问题数 | 850 | 120 |
| 减少误报 | - | 730个（85.9%） |

## 错误示例

```javascript
// 错误：同一describe下testcase重复
describe("TestSuite", function () {
  /**
   * @tc.name   test001
   * @tc.number SUB_TEST_0100
   */
  it('test001', Level.LEVEL0, async function (done) {
    console.info('test001');
    done();
  });

  /**
   * @tc.name   test001  // ✗ 错误：与当前文件第10行testcase命名重复
   * @tc.number SUB_TEST_0200
   */
  it('test001', Level.LEVEL0, async function (done) {  // ✗ 错误
    console.info('test001 again');
    done();
  });
});
```

```javascript
// 错误：同一describe下3次重复
describe("MyTest", () => {
  it('testCase', Level.LEVEL0, () => { /* ... */ });  // 第一次
  it('testCase', Level.LEVEL0, () => { /* ... */ });  // ✗ 第二次重复
  it('testCase', Level.LEVEL0, () => { /* ... */ });  // ✗ 第三次重复
});
```

## 正确示例

```javascript
// 正确1：同一describe内testcase命名唯一
describe("TestSuite", function () {
  /**
   * @tc.name   test001
   * @tc.number SUB_TEST_0100
   */
  it('test001', Level.LEVEL0, async function (done) {  // ✓ 正确
    console.info('test001');
    done();
  });

  /**
   * @tc.name   test002
   * @tc.number SUB_TEST_0200
   */
  it('test002', Level.LEVEL0, async function (done) {  // ✓ 正确
    console.info('test002');
    done();
  });
});
```

```javascript
// 正确2：不同describe块内允许同名testcase
describe("SuiteA", function () {
  it('test001', Level.LEVEL0, () => { /* SuiteA的test001 */ });  // ✓ 正确
});

describe("SuiteB", function () {
  it('test001', Level.LEVEL0, () => { /* SuiteB的test001 */ });  // ✓ 正确：不同describe块
});
```

```javascript
// 正确3：跨文件的testcase同名不检测（允许）
// File1.test.ets
describe("TestSuite", function () {
  it('test001', Level.LEVEL0, () => { /* ... */ });  // ✓ 跨文件不检测
});

// File2.test.ets
describe("TestSuite", function () {
  it('test001', Level.LEVEL0, () => { /* ... */ });  // ✓ 跨文件不检测
});
```

## 输出格式

### 问题数据结构

```python
{
    'rule': 'R018',
    'type': 'testcase重复',
    'severity': 'Critical',
    'file': 'rel/path.test.ets',
    'line': 10,
    'testcase': 'test001',
    'snippet': "it('test001', Level.LEVEL0, async function (done) {",
    'suggestion': '路径: rel/path.test.ets, 行号: 10, 问题描述: testcase \'test001\' 在describe \'TestSuite\' 内重复 2 次。与当前文件第25, 40行重复，修改testcase名称，确保describe内唯一。'
}
```

### Excel报告列

| 列序 | 列名 | 示例 |
|------|------|------|
| 1 | 问题ID | R018 |
| 2 | 问题类型 | testcase重复 |
| 3 | 严重级别 | Critical |
| 4 | 文件路径 | storage/entry/src/ohosTest/ets/test/Test.test.ets |
| 5 | 行号 | 10 |
| 6 | 所属用例 | test001 |
| 7 | 代码片段 | `it('test001', Level.LEVEL0, async function (done) {` |
| 8 | 修复建议 | 路径: ..., 行号: 10, 问题描述: testcase 'test001' 在describe 'TestSuite' 内重复 2 次。与当前文件第25, 40行重复，修改testcase名称，确保describe内唯一。 |

## 修复建议格式

**建议格式**：`与当前文件第{line_num}行重复，修改testcase名称，确保describe内唯一`

当有多个重复位置时，用逗号分隔所有行号：
`与当前文件第25, 40行重复，修改testcase名称，确保describe内唯一`

## 陷阱与注意事项

### 1. \b单词边界（已修复）

正则表达式必须使用`\bit\s*\(`模式，避免匹配`split(`、`submit(`、`visit()`等。

### 2. 文件类型完整性（已修复）

必须扫描`.test.ets`、`.test.ts`和`.test.js`三种文件类型。早期版本仅扫描`.test.ets`和`.test.ts`，导致storage目录中51%的`.test.js`文件被遗漏。

### 3. 不同describe块内允许同名

R018仅在同一个describe块内检查重复。不同describe块内允许使用相同的testcase名称。嵌套describe块各自独立检查。

### 4. 只报告第一个出现位置

同一组重复的testcase只报告第一次出现的行号，后续重复行号在修复建议中列出。避免同一组重复被多次报告。

### 5. 字符串字面量中的大括号

在识别describe块边界时，必须使用状态机跳过字符串字面量中的`{`和`}`，否则会导致块边界判断错误。

### 6. 嵌套describe块

文件中可能存在嵌套的describe块（describe内包含describe）。每个describe块独立检查，内层describe的testcase不与外层describe的testcase比较。

## 错误/正确示例

> 来源: EXAMPLES.md

以下为补充示例（与上方已有示例互补）：

**检测范围说明**:

> **重要**: R018规则**仅检查当前文件内是否存在重复的testcase**，不检查跨文件的情况（即使两个文件属于同一个testsuite也不检查）。

**错误示例**：
```javascript
// 错误：同一文件内同一describe下testcase重复
// File.test.ets
describe("TestSuite", function () {
  /**
   * @tc.name   test001
   * @tc.number SUB_TEST_0100
   */
  it('test001', Level.LEVEL0, async function (done) {
    console.info('test001');
    done();
  });

  /**
   * @tc.name   test001  // ✗ 错误：与当前文件第10行testcase命名重复
   * @tc.number SUB_TEST_0200
   */
  it('test001', Level.LEVEL0, async function (done) {  // ✗ 错误：testcase命名重复
    console.info('test001 again');
    done();
  });
});
```

**正确示例**：
```javascript
// 正确1：同一文件内testcase命名唯一
// File.test.ets
describe("TestSuite", function () {
  /**
   * @tc.name   test001
   * @tc.number SUB_TEST_0100
   */
  it('test001', Level.LEVEL0, async function (done) {  // ✓ 正确：testcase命名唯一
    console.info('test001');
    done();
  });

  /**
   * @tc.name   test002
   * @tc.number SUB_TEST_0200
   */
  it('test002', Level.LEVEL0, async function (done) {  // ✓ 正确：testcase命名唯一
    console.info('test002');
    done();
  });
});
```

```javascript
// 正确2：跨文件的testcase同名不检测（允许）
// File1.test.ets
describe("TestSuite", function () {
  it('test001', Level.LEVEL0, async function (done) {  // ✓ 正确：跨文件不检测
    console.info('file1 test001');
    done();
  });
});

// File2.test.ets（即使属于同一个testsuite，也不检测跨文件重复）
describe("TestSuite", function () {
  it('test001', Level.LEVEL0, async function (done) {  // ✓ 正确：跨文件不检测
    console.info('file2 test001');
    done();
  });
});
```

## 实现细节

> 来源: IMPLEMENTATION_DETAILS.md

**检测范围**: **仅检查当前文件内是否存在重复的testcase，不检查跨文件的情况**（即使两个文件属于同一个testsuite也不检测）

**检测方法**: 对每个describe块单独检查，同一describe块内的it()名称不允许重复

```python
def _check_r018(self, rel_path, content, lines):
    # 对每个describe块单独检查（只检查当前文件）
    for describe_block in describe_blocks:
        seen = {}
        for it_match in it_pattern.finditer(describe_block):
            tc_name = it_match.group(1)
            if tc_name in seen:
                # 报告重复：与当前文件第X行重复
                line_num = seen[tc_name]
                fix_suggestion = f"与当前文件第{line_num}行重复，修改testcase名称，确保describe内唯一"
            else:
                seen[tc_name] = line_num
```

### 正则表达式修复

**2026-03-12修复**: 添加单词边界`\b`，避免匹配`split(':')`等非`it()`调用

**修复前（错误）**:
```python
pattern = r'it\s*\(\s*([\'"])([^\'"]+)\1'
# 会匹配: "it(", "split(", "submit(", "visit("
```

**修复后（正确）**:
```python
pattern = r'\bit\s*\(\s*([\'"])([^\'"]+)\1'
#         ↑ 添加单词边界 \b
# 只匹配: "it("
# 不匹配: "split(", "submit(", "visit("
```

**修复效果**:
| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| 问题数 | 850 | 120 |
| 涉及文件数 | 102 | 约60个 |
| 减少误报 | - | 730个（85.9%） |

### 合并报告

**需求背景**: 同一组重复的testcase不应该多次报告，避免冗余。

**技术要求**:
1. **只报告第一次出现的位置**: 每组重复的testcase只报告第一次出现的行号
2. **显示所有重复位置**: 在修复建议中列出所有重复的行号
3. **统计重复次数**: 明确显示该testcase重复了多少次

### 与R011的区别

| 规则 | 检测对象 | 检测范围 |
|------|----------|----------|
| R011 | testsuite（describe） | 同一独立工程内（跨文件检测） |
| R018 | testcase（it的第一个参数） | 仅当前文件内（不跨文件检测） |

## 技术规范

> 来源: TECHNICAL_SPECIFICATION.md

### 规则定义
- **规则ID**: R018
- **规则名称**: testcase重复
- **严重级别**: Critical
- **问题描述**: 一个describe下不允许testcase（@tc.name)重复

### 检测范围
- **范围**: 在同一个describe块内检查@tc.name重复
- **不检查**:
  - 跨文件的describe块
  - 不同describe块间的@tc.name
  - 没有@tc.name的testcase

### 常见错误

#### 错误一: @tc.name匹配不准确
- **问题**: 正则表达式匹配不够精确
- **后果**: 可能误匹配代码中的其他位置
- **解决**: 精确匹配JSDoc注释（详见IMPLEMENTATION_DETAILS.md）

#### 错误二: 跨文件检查重复
- **问题**: 跨文件合并testcase检查
- **后果**: 跨文件误报
- **解决**: 按文件分组检查

### 最佳实践
1. **@tc.name格式**: 必须是JSDoc注释格式
2. **检测范围**: 只在同一个describe块内检查
3. **重复问题去重**: 同一个重复问题只报告一次

### 修复建议格式

```
路径: {文件路径}, 行号: {行号}, 问题描述: 在describe '{describe名称}' 内，testcase名称 '{testcase名称}' 重复 {重复次数} 次。重复行号: {行号1}, {行号2}, ...
```

## 技术挑战与解决方案

> 来源: V3_UPGRADE_GUIDE.md

- **预期问题数量**: 566个
- **实现方式**: describe块边界识别 + @tc.name收集
- **范围限制**: 仅在同一describe块内检查
