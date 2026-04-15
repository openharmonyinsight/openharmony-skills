# R015: Level参数缺省

- **规则编号**: R015
- **严重级别**: Warning
- **规则复杂度**: complex（需要代码分析）
- **问题类型**: it()函数缺少Level参数
- **修复方式**: 添加`Level.LEVEL*`参数
- **预期问题数量**: 1100+

## 扫描范围

仅扫描测试文件：
- `.test.ets` - ArkTS测试文件
- `.test.ts` - TypeScript测试文件
- `.test.js` - JavaScript测试文件

## 问题描述

`it()`函数声明时缺少`Level.LEVEL*`参数，不符合编码规范要求。每个测试用例必须指定测试级别。

## 检测逻辑

### 核心算法

```python
import re

def scan_r015(file_path: str, content: str) -> list:
    """
    扫描文件中缺少Level参数的it()函数调用。

    Args:
        file_path: 文件相对路径
        content: 文件完整内容

    Returns:
        问题列表，每条包含 rule, type, severity, file, line, testcase, snippet, suggestion
    """
    issues = []
    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # 匹配it()函数调用的起始行
        if re.search(r'\bit\s*\(\s*["\']', line):
            # 检查当前行是否已包含Level.LEVEL
            if 'Level.LEVEL' in line:
                i += 1
                continue

            # 如果行末以逗号结尾，Level参数可能在下一行，不报告
            if line.rstrip().endswith(','):
                i += 1
                continue

            # 提取it()声明块（可能跨多行）以获取完整参数列表
            it_block, end_idx = extract_it_declaration(lines, i)
            if it_block and 'Level.LEVEL' in it_block:
                i = end_idx + 1
                continue

            # 确认缺少Level参数，提取testcase名称
            tc_match = re.search(r'\bit\s*\(\s*([\'"])([^\'"]+)\1', line)
            tc_name = tc_match.group(2) if tc_match else '-'

            snippet = line.strip()
            if len(snippet) > 120:
                snippet = snippet[:120] + '...'

            issues.append({
                'rule': 'R015',
                'type': 'Level参数缺省',
                'severity': 'Warning',
                'file': file_path,
                'line': i + 1,
                'testcase': tc_name,
                'snippet': snippet,
                'suggestion': (
                    f"路径: {file_path}, 行号: {i + 1}, "
                    f"问题描述: it()函数缺少Level参数。"
                    f"请在it()的第二个参数位置添加Level.LEVEL0、Level.LEVEL1、"
                    f"Level.LEVEL2、Level.LEVEL3或Level.LEVEL4。"
                ),
            })

        i += 1

    return issues
```

### 提取it()声明块（处理多行it()声明）

```python
def extract_it_declaration(lines: list, start_idx: int) -> tuple:
    """
    从起始行开始，提取完整的it()参数声明部分（直到遇到第一个 { ）。
    使用状态机跳过字符串字面量中的括号和逗号。

    Args:
        lines: 文件所有行
        start_idx: it()起始行索引

    Returns:
        (it_declaration_text, end_line_index) 或 (None, start_idx)
    """
    in_single = False
    in_double = False
    paren_depth = 0
    found_open_paren = False
    declaration_lines = []

    for idx in range(start_idx, min(start_idx + 20, len(lines))):
        line = lines[idx]
        declaration_lines.append(line)

        j = 0
        while j < len(line):
            c = line[j]

            # 处理转义字符
            if c == '\\' and (in_single or in_double):
                j += 2
                continue

            # 处理字符串字面量
            if c == "'" and not in_double:
                in_single = not in_single
            elif c == '"' and not in_single:
                in_double = not in_double
            elif not in_single and not in_double:
                if c == '(':
                    paren_depth += 1
                    found_open_paren = True
                elif c == ')':
                    paren_depth -= 1
                elif c == '{':
                    # 遇到函数体开始的{，停止提取
                    if found_open_paren and paren_depth <= 0:
                        return '\n'.join(declaration_lines), idx
                elif c == ',':
                    # 逗号在字符串外且括号平衡，可能Level在后续行
                    pass
            j += 1

        # 如果括号已经平衡且找到过开括号，停止
        if found_open_paren and paren_depth <= 0:
            return '\n'.join(declaration_lines), idx

    return None, start_idx
```

### 陷阱：字符串字面量中的大括号

在提取`it()`块时，字符串字面量中的`{`和`}`会干扰大括号计数，必须使用状态机跳过字符串内容。

**错误做法**（朴素大括号计数）：
```python
# 错误：字符串中的{和}被计入
brace_count += line.count('{') - line.count('}')
```

**正确做法**（状态机解析）：
```python
def count_braces_outside_strings(line: str) -> tuple:
    """只计算字符串外的{和}数量"""
    in_single = False
    in_double = False
    open_count = 0
    close_count = 0
    i = 0
    while i < len(line):
        c = line[i]
        if c == '\\' and (in_single or in_double):
            i += 2
            continue
        if c == "'" and not in_double:
            in_single = not in_single
        elif c == '"' and not in_single:
            in_double = not in_double
        elif not in_single and not in_double:
            if c == '{':
                open_count += 1
            elif c == '}':
                close_count += 1
        i += 1
    return open_count, close_count
```

### 陷阱：行末逗号表示参数在下一行

如果`it()`声明行以逗号结尾，Level参数可能在下一行，此时不应报告。

```python
# 错误：行末有逗号，Level在下一行
it('test001',
  Level.LEVEL0,    # ← Level在下一行，不应报告
  async (done: Function) => {
```

```python
if line.rstrip().endswith(','):
    # Level参数可能在下一行，跳过不报告
    continue
```

## 错误示例

```javascript
// 错误1：缺少Level参数
it('test001', () => {
  console.info('test001');
  // ✗ 错误：缺少Level参数
});
```

```javascript
// 错误2：缺少Level参数
it('testUrl[Symbol.iterator]()002', () => {
  console.info('test002');
  // ✗ 错误：缺少Level参数
});
```

```javascript
// 错误3：缺少Level参数（使用function关键字）
it('test003', async function (done) {
  console.info('test003');
  done();
  // ✗ 错误：缺少Level参数
});
```

```javascript
// 错误4：缺少Level参数（使用TypeScript类型注解）
it('test004', async (done: Function) => {
  console.info('test004');
  done();
  // ✗ 错误：缺少Level参数
});
```

## 正确示例

```javascript
// 正确1：包含Level.LEVEL0参数
it('test001', Level.LEVEL0, () => {
  console.info('test001');
  // ✓ 正确：包含Level参数
});
```

```javascript
// 正确2：测试用例名称中包含括号也能正确识别Level参数
it('testUrl[Symbol.iterator]()002', Level.LEVEL0, () => {
  console.info('test002');
  // ✓ 正确：包含Level参数
});
```

```javascript
// 正确3：Level在下一行（行末有逗号）
it('test003',
  Level.LEVEL0,    // ✓ 正确：Level在下一行
  async (done: Function) => {
  console.info('test003');
  done();
});
```

```javascript
// 正确4：使用Level.LEVEL1
it('test004', Level.LEVEL1, async (done: Function) => {
  console.info('test004');
  done();
  // ✓ 正确：包含Level参数
});
```

```javascript
// 正确5：使用Level.LEVEL2
it('test005', Level.LEVEL2, 0, () => {
  expect(true).assertTrue();
  // ✓ 正确：包含Level参数
});
```

## 输出格式

### 问题数据结构

```python
{
    'rule': 'R015',
    'type': 'Level参数缺省',
    'severity': 'Warning',
    'file': 'rel/path.test.ets',
    'line': 25,
    'testcase': 'test001',
    'snippet': "it('test001', () => {",
    'suggestion': '路径: rel/path.test.ets, 行号: 25, 问题描述: it()函数缺少Level参数。请在it()的第二个参数位置添加Level.LEVEL0、Level.LEVEL1、Level.LEVEL2、Level.LEVEL3或Level.LEVEL4。'
}
```

### Excel报告列

| 列序 | 列名 | 示例 |
|------|------|------|
| 1 | 问题ID | R015 |
| 2 | 问题类型 | Level参数缺省 |
| 3 | 严重级别 | Warning |
| 4 | 文件路径 | web/DFX/log/entry/src/ohosTest/ets/test/Test.test.ets |
| 5 | 行号 | 25 |
| 6 | 所属用例 | test001 |
| 7 | 代码片段 | `it('test001', () => {` |
| 8 | 修复建议 | 路径: ..., 行号: 25, 问题描述: it()函数缺少Level参数。请在it()的第二个参数位置添加Level.LEVEL0... |

## 修复建议

在`it()`函数的testcase名称之后、回调函数之前，添加`Level.LEVEL*`参数：

```javascript
// 修复前
it('test001', () => {
  // ...
});

// 修复后
it('test001', Level.LEVEL0, () => {
  // ...
});
```

可选的Level级别：
- `Level.LEVEL0` - 最基础级别
- `Level.LEVEL1`
- `Level.LEVEL2`
- `Level.LEVEL3`
- `Level.LEVEL4` - 最高级别

## 错误/正确示例

> 来源: EXAMPLES.md

以下为补充示例（与上方已有示例互补）：

**错误示例**：
```javascript
// 错误：缺少Level参数
it('test001', () => {
  console.info('test001');
  // ✗ 错误：缺少Level参数
});
```

```javascript
// 错误：测试用例名称中包含括号但仍缺少Level参数
it('testUrl[Symbol.iterator]()002', () => {
  console.info('test002');
  // ✗ 错误：缺少Level参数
});
```

**正确示例**：
```javascript
// 正确：包含Level参数
it('test001', Level.LEVEL0, () => {
  console.info('test001');
  // ✓ 正确：包含Level参数
});
```

```javascript
// 正确：测试用例名称中包含括号也能正确识别Level参数
it('testUrl[Symbol.iterator]()002', Level.LEVEL0, () => {
  console.info('test002');
  // ✓ 正确：包含Level参数
});
```

## 实现细节

> 来源: IMPLEMENTATION_DETAILS.md

**检测方法**: 检查it()函数是否包含`Level.LEVEL`参数

**注意**: 如果行末是逗号，说明参数可能在下一行，不报错。

```python
if re.search(r'\bit\s*\(\s*["\']', line):
    if 'Level.LEVEL' not in line:
        if not line.rstrip().endswith(','):
            # 报告Level参数缺省
```

## 技术挑战与解决方案

> 来源: V3_UPGRADE_GUIDE.md

- **预期问题数量**: 1171个
- **实现方式**: it()函数解析 + Level参数检测
- **支持格式**: Level.LEVEL0~3, Level*
