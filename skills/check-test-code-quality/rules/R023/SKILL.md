# R023: 禁止errcode值(.code)类型强转后断言

## 规则信息

| 属性 | 值 |
|------|-----|
| 规则编号 | R023 |
| 问题类型 | 禁止errcode值类型强转后断言 |
| 严重级别 | Critical |
| 规则复杂度 | simple |
| 扫描范围 | 所有源代码文件（`.ets`, `.ts`, `.js`） |
| testcase字段 | 需解析`it()`块范围 |

## 问题描述

errcode值（`.code`）本身一定是number类型，不允许使用`Number()`等类型强转后再进行断言。类型强转是对errcode类型问题的规避行为，正确做法是给开发提单修复API的errcode类型。

## 修复建议

1. 新增API接口出现的errcode类型问题：给开发提单修复
2. 已转测的API，给开发提单后，测试侧先按错误的（string类型）上库，**不使用`Number()`强转规避**

## 修复建议格式

```
路径: {文件路径}, 行号: {行号}, 问题描述: errcode值断言使用了类型强转'Number()'，应移除强转并给开发提单修复errcode类型问题。
```

## 扫描逻辑

### Step 1: 收集源代码文件

```python
def get_all_source_files(directory):
    source_extensions = ('.ets', '.ts', '.js')
    result = []
    for root, dirs, files in os.walk(directory):
        for fn in files:
            if fn.endswith(source_extensions):
                result.append(os.path.join(root, fn))
    return result
```

### Step 2: 提取it()块范围

使用状态机解析，追踪字符串字面量内的大括号（含反引号追踪），提取每个`it()`块的行号范围。

```python
def extract_it_blocks(content):
    blocks = []
    it_pattern = re.compile(r'\bit\s*\(\s*(["\'])(.+?)\1\s*,', re.MULTILINE)
    for match in it_pattern.finditer(content):
        start_line = content[:match.start()].count('\n') + 1
        name = match.group(2)
        brace_start = content.index('{', match.end())
        open_count, close_count = 0, 0
        i = brace_start
        in_single = in_double = in_backtick = False
        while i < len(content):
            c = content[i]
            if c == '\\' and (in_single or in_double or in_backtick):
                i += 2; continue
            if c == '`' and not in_single and not in_double:
                in_backtick = not in_backtick
            elif c == "'" and not in_double and not in_backtick:
                in_single = not in_single
            elif c == '"' and not in_single and not in_backtick:
                in_double = not in_double
            elif not in_single and not in_double and not in_backtick:
                if c == '{': open_count += 1
                elif c == '}':
                    close_count += 1
                    if open_count == close_count:
                        end_line = content[:i].count('\n') + 1
                        blocks.append({'name': name, 'start': start_line, 'end': end_line})
                        break
            i += 1
    return blocks
```

### Step 3: 检测Number(.code)模式

```python
import re

# 匹配 Number(...) 内包含 .code 的模式（支持嵌套括号）
def find_number_code_matches(line):
    """匹配 Number(...) 内包含 .code 的模式，使用括号计数处理嵌套。
    
    支持嵌套括号如: Number((error as BusinessError).code)
    """
    results = []
    pattern = re.compile(r'\bNumber\s*\(')
    for m in pattern.finditer(line):
        start = m.end()
        depth = 1
        i = start
        in_single = in_double = in_backtick = False
        while i < len(line) and depth > 0:
            c = line[i]
            if c == '\\' and (in_single or in_double or in_backtick):
                i += 2
                continue
            if c == '`' and not in_single and not in_double:
                in_backtick = not in_backtick
            elif c == "'" and not in_double and not in_backtick:
                in_single = not in_single
            elif c == '"' and not in_single and not in_backtick:
                in_double = not in_double
            elif not in_single and not in_double and not in_backtick:
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
            i += 1
        if depth == 0:
            inner = line[start:i - 1]
            if '.code' in inner:
                results.append(line[m.start():i])
    return results

def scan_r023(file_path, base_dir):
    issues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')

    it_blocks = extract_it_blocks(content)

    for line_idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//'):
            continue
        code_part = stripped
        if '//' in stripped:
            code_part = stripped[:stripped.index('//')].strip()
        matches = find_number_code_matches(code_part)
        if not matches:
            continue

        line_num = line_idx + 1
        testcase = '-'
        for block in it_blocks:
            if block['start'] <= line_num <= block['end']:
                testcase = block['name']
                break

        rel_path = os.path.relpath(file_path, base_dir)
        issues.append({
            'rule': 'R023',
            'type': '禁止errcode值类型强转后断言',
            'severity': 'Critical',
            'file': rel_path,
            'line': line_num,
            'testcase': testcase,
            'snippet': stripped,
            'suggestion': (
                f"路径: {rel_path}, 行号: {line_num}, "
                f"问题描述: errcode值断言使用了类型强转'Number()'，"
                f"应移除强转并给开发提单修复errcode类型问题。"
            ),
        })

    return issues
```

## 错误示例

```typescript
expect(Number(err.code) === 401).assertTrue();       // ✗ 错误：使用Number()强转
expect(Number(error.code)).assertEqual(201);          // ✗ 错误：使用Number()强转
if (Number(error.code) == 401) { ... }                 // ✗ 错误：使用Number()强转
this.progress = Number(error.code);                    // ✗ 错误：使用Number()强转
```

## 正确示例

```typescript
expect(err.code === 401).assertTrue();                 // ✓ 直接断言，errcode本身是number
expect(error.code === 201).assertTrue();                // ✓ 直接断言
```

## 陷阱与注意事项

### 陷阱1: 正则需匹配括号内含.code

`Number(...)`的括号内可能包含复杂的表达式，如`Number(err.code)`、`Number(error.code)`、`Number((error as BusinessError).code)`。正则`Number\s*\([^)]*\.code\s*\)`使用`[^)]*`匹配括号内任意字符直到`.code`。

### 陷阱2: 非断言场景也需要检测

`Number(.code)`不仅出现在`expect()`断言中，也可能出现在赋值（`this.progress = Number(error.code)`）或`if`条件判断中。R023对所有`Number(.code)`统一报告，因为类型强转本身就是对问题的规避。

### 陷阱3: 跳过注释行

`//` 注释中的 `Number(err.code)` 不应被检测。

### 陷阱4: 嵌套括号

部分代码可能存在嵌套括号，如`Number((error as BusinessError).code)`。正则`[^)]*\.code\s*\)`可以匹配这种情况，因为`[^)]*`会跳过内层括号的内容直到找到`.code)`。

## 输出格式

每条issue的字段：

| 字段 | 值 |
|------|-----|
| rule | `R023` |
| type | `禁止errcode值类型强转后断言` |
| severity | `Critical` |
| file | 相对路径 |
| line | `Number(.code)`所在行号 |
| testcase | 所属it()块名称或`-` |
| snippet | 当前行内容 |
| suggestion | 路径: {文件路径}, 行号: {行号}, 问题描述: errcode值断言使用了类型强转'Number()'，应移除强转并给开发提单修复errcode类型问题。 |

## 排除规则

- `//` 注释行中的 `Number(.code)` 不检查
- 非`.code`的`Number()`调用不检查（如`Number(strValue)`）

## 技术规范

### 检测范围补充说明

**检查**:
- 所有源代码文件（`.ets`, `.ts`, `.js`）中 `Number(...)` 内包含 `.code` 的调用
- 包括 `expect()` 断言、`if` 条件判断、赋值等所有场景

**不检查**:
- 注释中的 `Number(.code)`
- `Number()` 内不含 `.code` 的普通调用

### 实际案例

```
全仓扫描结果（预估）:
- 问题数: ~8500+ 行包含 Number(.code)
- 涉及子系统: 全部子系统
- 典型场景:
  - expect(Number(err.code) === 401).assertTrue();
  - expect(Number(error.code)).assertEqual(201);
  - if (Number(error.code) == 401) { ... }
  - this.progress = Number(error.code);
```

### 与R002的关系

- R002: 检查errcode断言中错误码是否为number类型（`"401"` string vs `401` number）
- R023: 检查是否使用`Number()`类型强转规避errcode类型问题
- 两个规则互补：`Number(err.code)`表明开发者知道errcode可能是string类型，但用强转规避而非提单修复
