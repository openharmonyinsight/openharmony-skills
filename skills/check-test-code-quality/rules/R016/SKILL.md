# R016: testcase命名规范

- **规则编号**: R016
- **严重级别**: Warning
- **规则复杂度**: complex（需要代码分析）
- **问题类型**: testcase名称包含特殊字符（仅允许英文字母、数字、下划线、连字符）
- **修复方式**: 移除特殊字符，追加`Adapt`+三位数字后缀，同步修改`@tc.name`
- **预期问题数量**: 400+

## 扫描范围

仅扫描测试文件：
- `.test.ets` - ArkTS测试文件
- `.test.ts` - TypeScript测试文件
- `.test.js` - JavaScript测试文件

## 问题描述

testcase名称（`it()`的第一个参数）中包含特殊字符。仅允许使用英文字母（`a-zA-Z`）、数字（`0-9`）、下划线（`_`）和连字符（`-`）。

**检测对象**: 以`it()`的第一个参数为准，不检测`@tc.name`的值。`@tc.name`仅在修复阶段同步修改。

## 检测逻辑

### 核心算法

```python
import re

TC_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
IT_PATTERN = re.compile(r'\bit\s*\(\s*([\'"])([^\'"]+)\1')
TC_NAME_ANNOTATION = re.compile(r'@tc\.name\s+(.+)')

def scan_r016(file_path: str, content: str) -> list:
    issues = []
    lines = content.split('\n')

    it_entries = extract_all_it_entries(lines)

    for entry in it_entries:
        tc_name = entry['it_tc_name']
        it_line_idx = entry['line_idx']

        if TC_NAME_PATTERN.match(tc_name):
            continue

        # testcase名称包含特殊字符
        snippet = lines[it_line_idx].strip()
        if len(snippet) > 120:
            snippet = snippet[:120] + '...'

        # 生成修复建议
        suggestion = build_r016_suggestion(file_path, it_line_idx + 1, tc_name, lines, entry)

        issues.append({
            'rule': 'R016',
            'type': 'testcase命名规范',
            'severity': 'Warning',
            'file': file_path,
            'line': it_line_idx + 1,
            'testcase': tc_name,
            'snippet': snippet,
            'suggestion': suggestion,
        })

    return issues
```

### 提取所有it()条目

```python
def extract_all_it_entries(lines: list) -> list:
    """
    提取文件中所有it()函数调用及其对应的@tc.name注解。

    Returns:
        [{'line_idx': int, 'tc_name': str, 'tc_name_line_idx': int|None, 'has_tc_annotation': bool}]
    """
    entries = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # 匹配it()函数调用
        match = IT_PATTERN.search(line)
        if match:
            it_tc_name = match.group(2)
            tc_name_line_idx = None
            has_tc_annotation = False
            final_tc_name = it_tc_name

            # 向上查找最近的 @tc.name 注解
            for back in range(i - 1, max(i - 20, -1), -1):
                back_line = lines[back].strip()
                if not back_line:
                    continue
                if back_line.startswith('* @tc.name') or back_line.startswith('@tc.name'):
                    tc_match = re.search(r'@tc\.name\s+(.+)', back_line)
                    if tc_match:
                        annotated_name = tc_match.group(1).strip()
                        final_tc_name = annotated_name
                        tc_name_line_idx = back
                        has_tc_annotation = True
                    break
                # 遇到注释块开始或非注释行，停止向上搜索
                if back_line.startswith('/**') or back_line.startswith('/*'):
                    break
                if not back_line.startswith('*') and not back_line.startswith('//'):
                    break

            entries.append({
                'line_idx': i,
                'tc_name': final_tc_name,
                'it_tc_name': it_tc_name,
                'tc_name_line_idx': tc_name_line_idx,
                'has_tc_annotation': has_tc_annotation,
            })

        i += 1

    return entries
```

### 修复建议生成

```python
def build_r016_suggestion(file_path: str, line_num: int, tc_name: str,
                          lines: list, entry: dict) -> str:
    """
    生成R016修复建议，包含具体的修复方案。

    修复规则：
    1. 移除testcase名称中所有非[a-zA-Z0-9_-]的字符
    2. 移除后追加Adapt+三位数字后缀（从001开始）
    3. 如果追加后命名存在重复，数字递增
    4. 同步修改@tc.name值（如果有）
    5. 仅修改it()和@tc.name，不修改@tc.number、@tc.desc等
    """
    # 步骤1：移除特殊字符
    cleaned = re.sub(r'[^a-zA-Z0-9_-]', '', tc_name)

    # 步骤2：收集文件中已有的testcase名称，确保不重复
    existing_names = set()
    for e in extract_all_it_entries(lines):
        existing_names.add(e['tc_name'])

    # 步骤3：追加Adapt+三位数字后缀，确保唯一
    new_name = None
    for suffix_num in range(1, 1000):
        candidate = f"{cleaned}Adapt{suffix_num:03d}"
        if candidate not in existing_names:
            new_name = candidate
            break

    if new_name is None:
        new_name = f"{cleaned}Adapt999"

    suggestion_parts = [
        f"路径: {file_path}, 行号: {line_num}, ",
        f"问题描述: testcase名称 '{tc_name}' 包含特殊字符。",
        f"仅允许英文字母、数字、下划线、连字符。",
    ]

    if entry['has_tc_annotation']:
        suggestion_parts.append(
            f"修复: 将it()参数和@tc.name修改为 '{new_name}'。"
        )
    else:
        suggestion_parts.append(
            f"修复: 将it()参数修改为 '{new_name}'。"
        )

    return ''.join(suggestion_parts)
```

## 修复规则

### 修复步骤

1. **移除特殊字符**：从testcase名称中移除所有非`[a-zA-Z0-9_-]`的字符
2. **追加后缀**：在清理后的名称后追加`Adapt`+三位数字后缀（从`001`开始）
3. **去重检查**：如果追加后命名在文件内已存在，数字递增（`001` -> `002` -> `003`...）
4. **同步@tc.name**：`it()`参数变动时，必须同步修改对应的`@tc.name`值，保持一致
5. **仅修改必要字段**：只修改`it()`和`@tc.name`，不修改`@tc.number`、`@tc.desc`等其他字段

### 修复示例

```javascript
// 修复前
/**
 * @tc.name   test.name@001
 * @tc.number SUB_TEST_0100
 * @tc.desc   测试用例描述
 */
it('test.name@001', Level.LEVEL0, () => {
  // ✗ 错误：包含@和.字符
});

// 修复后
/**
 * @tc.name   testname001Adapt001
 * @tc.number SUB_TEST_0100     ← 不修改
 * @tc.desc   测试用例描述      ← 不修改
 */
it('testname001Adapt001', Level.LEVEL0, () => {
  // ✓ 正确：移除了特殊字符并追加Adapt后缀
});
```

## 错误示例

```javascript
// 错误1：包含@和.字符
it('test.name@001', Level.LEVEL0, () => {
  // ✗ 错误：包含@和.字符
});
```

```javascript
// 错误2：包含空格
it('test name 001', Level.LEVEL0, () => {
  // ✗ 错误：包含空格
});
```

```javascript
// 错误3：包含#字符
it('test#name001', Level.LEVEL0, () => {
  // ✗ 错误：包含#字符
});
```

```javascript
// 错误4：包含中文
it('测试用例001', Level.LEVEL0, () => {
  // ✗ 错误：包含中文字符
});
```

```javascript
// 错误5：包含括号
it('test(001)', Level.LEVEL0, () => {
  // ✗ 错误：包含括号
});
```

```javascript
// 错误6：包含冒号和斜杠
it('test:api/v1', Level.LEVEL0, () => {
  // ✗ 错误：包含冒号和斜杠
});
```

## 正确示例

```javascript
// 正确1：仅使用英文字母和数字
it('testName001', Level.LEVEL0, () => {
  // ✓ 正确：符合命名规范
});
```

```javascript
// 正确2：使用下划线分隔
it('test_name_001', Level.LEVEL0, () => {
  // ✓ 正确：符合命名规范
});
```

```javascript
// 正确3：使用连字符分隔
it('test-name-001', Level.LEVEL0, () => {
  // ✓ 正确：符合命名规范
});
```

```javascript
// 正确4：混合使用字母、数字、下划线和连字符
it('testFunc_API_v2-001', Level.LEVEL0, () => {
  // ✓ 正确：符合命名规范
});
```

## 输出格式

### 问题数据结构

```python
{
    'rule': 'R016',
    'type': 'testcase命名规范',
    'severity': 'Warning',
    'file': 'rel/path.test.ets',
    'line': 25,
    'testcase': 'test.name@001',
    'snippet': "it('test.name@001', Level.LEVEL0, () => {",
    'suggestion': '路径: rel/path.test.ets, 行号: 25, 问题描述: testcase名称 \'test.name@001\' 包含特殊字符。仅允许英文字母、数字、下划线、连字符。修复: 将it()参数和@tc.name修改为 \'testname001Adapt001\'。'
}
```

### Excel报告列

| 列序 | 列名 | 示例 |
|------|------|------|
| 1 | 问题ID | R016 |
| 2 | 问题类型 | testcase命名规范 |
| 3 | 严重级别 | Warning |
| 4 | 文件路径 | web/DFX/log/entry/src/ohosTest/ets/test/Test.test.ets |
| 5 | 行号 | 25 |
| 6 | 所属用例 | test.name@001 |
| 7 | 代码片段 | `it('test.name@001', Level.LEVEL0, () => {` |
| 8 | 修复建议 | 路径: ..., 行号: 25, 问题描述: testcase名称 'test.name@001' 包含特殊字符... |

## 陷阱与注意事项

### 1. @tc.name与it()参数不一致

有些文件中`@tc.name`的值与`it()`第一个参数不一致，此时应以`@tc.name`为准进行检测。

### 2. 仅修改it()和@tc.name

修复时只修改`it()`的第一个参数和对应的`@tc.name`注解值，**不得修改**：
- `@tc.number` - 用例编号
- `@tc.desc` - 用例描述
- `@tc.size` - 用例规模
- `@tc.type` - 用例类型
- `@tc.level` - 用例级别

### 3. Adapt后缀去重

追加`Adapt`后缀后，需要在当前文件范围内检查是否与已有testcase名称冲突。如果冲突，数字递增。

### 4. 清理后名称为空

如果移除所有特殊字符后名称为空（如`@#$%`），则使用`unnamedTest`作为基础名称，再追加`Adapt`后缀。

### 5. 严禁使用命名格式检测代替特殊字符检测（极严重）

- **严重性**: 极严重，曾导致print子系统313条R016全部误报（0%准确率）
- **问题**: 将R016错误实现为"检查testcase名称是否符合`testXxx`或`IT_xxx`格式"，用正则 `^(test|IT|it)[A-Z]\w*$` 做格式匹配。
- **正确实现**: 必须使用 `^[a-zA-Z0-9_-]+$` 做正向字符集匹配。

> 详见 [references/TRAPS.md](../../references/TRAPS.md) 陷阱8。

### 6. 不得用@tc.name的值作为检测源（极严重）

R016的检测对象是`it()`的第一个参数，不是`@tc.name`注解的值。`@tc.name`仅在修复阶段同步修改。

> 详见 [references/TRAPS.md](../../references/TRAPS.md) 陷阱9。

## 错误/正确示例

> 来源: EXAMPLES.md

以下为补充示例（与上方已有示例互补）：

**错误示例**：
```javascript
// 错误：包含特殊字符
it('test.name@001', () => {  // ✗ 错误：包含@字符
  console.info('test001');
});
```

```javascript
// 错误：包含空格
it('test name 001', () => {  // ✗ 错误：包含空格
  console.info('test001');
});
```

```javascript
// 错误：包含其他特殊字符
it('test#name001', () => {  // ✗ 错误：包含#字符
  console.info('test001');
});
```

**正确示例**：
```javascript
// 正确：仅使用英文字母、数字、下划线和连字符
it('test_name_001', () => {  // ✓ 正确：符合命名规范
  console.info('test001');
});

it('testName001', () => {  // ✓ 正确：符合命名规范
  console.info('test001');
});

it('test-name-001', () => {  // ✓ 正确：符合命名规范
  console.info('test001');
});
```

## 实现细节

> 来源: IMPLEMENTATION_DETAILS.md

**命名规范**: testcase名称只能包含英文字母、数字、下划线、连字符

```python
def check_testcase_naming(tc_name: str):
    # 只允许英文字母、数字、下划线、连字符
    if not re.match(r'^[a-zA-Z0-9_-]+$', tc_name):
        report_issue("testcase名称包含特殊字符")
```

## 技术挑战与解决方案

> 来源: V3_UPGRADE_GUIDE.md

- **预期问题数量**: 414个
- **实现方式**: 名称提取 + 特殊字符检测
- **允许字符**: a-zA-Z0-9_-
