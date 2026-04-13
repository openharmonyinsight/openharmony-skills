# R013: 注释的废弃代码

## 规则信息

| 属性 | 值 |
|------|-----|
| 规则编号 | R013 |
| 问题类型 | 注释的废弃代码 |
| 严重级别 | Warning |
| 规则复杂度 | complex |
| 扫描范围 | 测试文件（`.test.ets`, `.test.ts`, `.test.js`） |
| testcase字段 | 所属的it()名称，不在it()块内时为`-` |

## 问题描述

存在大量注释的废弃代码。测试文件中包含连续多行的注释代码块，这些代码已经不再使用但仍然保留在文件中，影响代码可读性。

## 修复建议

直接删除注释的废弃代码。使用版本控制系统（如Git）保留历史记录，不需要在代码中注释保留。

## 扫描逻辑

### Step 1: 筛选测试文件

```python
import os

TEST_EXTENSIONS = ('.test.ets', '.test.ts', '.test.js')

def find_test_files(scan_root):
    test_files = []
    for dirpath, dirnames, filenames in os.walk(scan_root):
        for fn in filenames:
            if fn.endswith(TEST_EXTENSIONS):
                test_files.append(os.path.join(dirpath, fn))
    return test_files
```

### Step 2: 识别连续注释块

检测连续3行及以上的注释行组成的代码块。

```python
import re

def find_comment_blocks(content):
    lines = content.split('\n')
    blocks = []
    current_block = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        is_comment = (
            stripped.startswith('//') or
            stripped.startswith('*') or
            stripped.startswith('/*') or
            (current_block and stripped.startswith('*/'))
        )

        if is_comment:
            current_block.append((i, line))
        else:
            if len(current_block) >= 3:
                blocks.append(list(current_block))
            current_block = []

    if len(current_block) >= 3:
        blocks.append(list(current_block))

    return blocks
```

### Step 3: 检测代码特征

判断注释块内容是否包含代码特征（而非普通文档注释）。

```python
CODE_PATTERNS = [
    r'\bfunction\b',
    r'\bvar\b',
    r'\blet\b',
    r'\bconst\b',
    r'\breturn\b',
    r'\bif\s*\(',
    r'\bfor\s*\(',
    r'\bwhile\s*\(',
    r'\bswitch\s*\(',
    r'\bcase\b',
    r'\bbreak\b',
    r'\bclass\b',
    r'\bimport\b',
    r'\bexport\b',
    r'\basync\b',
    r'\bawait\b',
    r'\btry\b',
    r'\bcatch\b',
    r'\bthrow\b',
    r'\bnew\b',
    r'\bthis\b',
    r'\bexpect\b',
    r'\bit\s*\(',
    r'\bdescribe\s*\(',
    r'\{',
    r'\}',
    r';',
    r'\=\>',
    r'\.\w+\s*\(',
]

def extract_comment_text(block):
    texts = []
    for _, line in block:
        stripped = line.strip()
        if stripped.startswith('//'):
            texts.append(stripped[2:].strip())
        elif stripped.startswith('*') and not stripped.startswith('*/'):
            texts.append(stripped[1:].strip())
        elif stripped.startswith('/*'):
            texts.append(stripped[2:].strip())
        elif stripped.startswith('*/'):
            texts.append(stripped[2:].strip())
        else:
            texts.append(stripped)
    return '\n'.join(texts)

def has_code_characteristics(comment_text):
    pattern_count = 0
    for pattern in CODE_PATTERNS:
        if re.search(pattern, comment_text):
            pattern_count += 1
    return pattern_count >= 2
```

### Step 4: 检测完整函数定义或测试用例

检查注释块中是否包含完整的函数定义或测试用例声明。

```python
def has_complete_function(comment_text):
    patterns = [
        r'function\s+\w+\s*\([^)]*\)\s*\{',
        r'(?:async\s+)?\w+\s*=\s*(?:async\s+)?\([^)]*\)\s*(?:=>|\{)',
        r'it\s*\(\s*["\'][^"\']+["\']',
        r'describe\s*\(\s*["\'][^"\']+["\']',
        r'\bclass\s+\w+',
    ]
    match_count = sum(1 for p in patterns if re.search(p, comment_text))
    return match_count >= 1

def is_javadoc_like(comment_text):
    javadoc_markers = [
        r'@tc\.name',
        r'@tc\.number',
        r'@tc\.desc',
        r'@tc\.size',
        r'@tc\.type',
        r'@tc\.level',
        r'@param',
        r'@return',
        r'@throws',
        r'@since',
        r'@deprecated',
    ]
    match_count = sum(1 for m in javadoc_markers if re.search(m, comment_text))
    return match_count >= 2
```

### Step 5: 判断所属testcase

解析文件中所有`it()`块的范围，判断注释块的起始行落在哪个`it()`块内。

```python
def find_it_blocks(content):
    it_pattern = re.compile(
        r"it\s*\(\s*['\"]([^'\"]+)['\"]",
        re.MULTILINE
    )
    it_blocks = []
    for match in it_pattern.finditer(content):
        name = match.group(1)
        start_line = content[:match.start()].count('\n') + 1
        it_blocks.append((start_line, name))
    return sorted(it_blocks, key=lambda x: x[0])

def get_testcase_for_line(line_num, it_blocks):
    testcase = '-'
    for i, (start, name) in enumerate(it_blocks):
        if i + 1 < len(it_blocks):
            next_start = it_blocks[i + 1][0]
            if start < line_num < next_start:
                testcase = name
                break
        else:
            if line_num > start:
                testcase = name
                break
    return testcase
```

### Step 6: 生成问题报告

```python
def scan_r013(scan_root, base_dir):
    issues = []
    test_files = find_test_files(scan_root)

    for file_path in test_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        it_blocks = find_it_blocks(content)
        comment_blocks = find_comment_blocks(content)

        for block in comment_blocks:
            start_line = block[0][0]
            end_line = block[-1][0]
            comment_text = extract_comment_text(block)

            if is_javadoc_like(comment_text):
                continue

            if not has_code_characteristics(comment_text):
                continue

            is_function = has_complete_function(comment_text)
            if not is_function and len(block) < 5:
                continue

            rel_path = os.path.relpath(file_path, base_dir)
            testcase = get_testcase_for_line(start_line, it_blocks)

            block_preview = '\n'.join(line for _, line in block[:5])
            if len(block) > 5:
                block_preview += '\n  ... (省略' + str(len(block) - 5) + '行)'

            issues.append({
                'rule': 'R013',
                'type': '注释的废弃代码',
                'severity': 'Warning',
                'file': rel_path,
                'line': start_line,
                'testcase': testcase,
                'snippet': block_preview,
                'suggestion': (
                    f'第{start_line}-{end_line}行存在注释的废弃代码（共{len(block)}行）。'
                    f'建议直接删除，使用版本控制系统保留历史记录。'
                ),
            })

    return issues
```

## 错误示例

```javascript
// 错误1：大量注释的废弃代码
// 废弃的旧方法 - 不要删除，保留参考
// function oldMethod() {
//   let value = testFunction();
//   expect(value).assertEqual('expected');
//   return value;
// }

function newMethod() {
  let newValue = newTestFunction();
  expect(newValue).assertEqual('newExpected');
}
```

```javascript
// 错误2：注释掉的完整测试用例
it('test001', () => {
  // 废弃的测试逻辑
  // let value = testFunction();
  // expect(value).assertEqual('expected');
  // done();

  let newValue = newTestFunction();
  expect(newValue).assertEqual('newExpected');
});
```

```javascript
// 错误3：注释掉的函数定义（3行以上）
// function oldTestMethod(done: Function) {
//   console.info('old test start');
//   let result = doSomething();
//   expect(result).assertTrue();
//   done();
// }
```

## 正确示例

```javascript
// 正确：直接删除废弃代码，保持代码简洁
it('test001', () => {
  let newValue = newTestFunction();
  expect(newValue).assertEqual('newExpected');
});
```

```javascript
// 正确：如果需要保留旧逻辑作为参考，使用Git历史记录
function newMethod() {
  let currentValue = currentFunction();
  expect(currentValue).assertEqual('expected');
}
```

## 排除规则

以下注释块不应被报告：

1. **JSDoc文档注释**：包含`@tc.name`、`@tc.number`、`@param`、`@return`等标记的注释
2. **少于3行的注释**：不视为"大量"注释
3. **无代码特征的注释**：纯文字说明、TODO、FIXME等
4. **单行代码片段**：如仅`// let x = 1;`一行，不构成"废弃代码块"

## 输出格式

每条issue的字段：

| 字段 | 值 |
|------|-----|
| rule | `R013` |
| type | `注释的废弃代码` |
| severity | `Warning` |
| file | 相对路径（如`xxx/test.test.ets`） |
| line | 注释块起始行号 |
| testcase | 所属的it()名称，不在it()块内时为`-` |
| snippet | 注释块前5行预览 |
| suggestion | 第X-Y行存在注释的废弃代码（共N行）。建议直接删除，使用版本控制系统保留历史记录。 |
