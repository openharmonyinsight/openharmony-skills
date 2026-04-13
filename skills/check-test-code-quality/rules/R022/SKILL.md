# R022: errcode值(.code)值断言使用"==="非"=="

## 规则信息

| 属性 | 值 |
|------|-----|
| 规则编号 | R022 |
| 问题类型 | errcode值断言使用==而非=== |
| 严重级别 | Critical |
| 规则复杂度 | simple |
| 扫描范围 | 所有源代码文件（`.ets`, `.ts`, `.js`） |
| testcase字段 | 需解析`it()`块范围 |

## 问题描述

测试用例中对`.code`（errcode）进行值断言时，必须使用严格相等运算符`===`，不允许使用宽松相等运算符`==`。

## 修复建议

将`==`替换为`===`。例如：`expect(err.code == 401)` 改为 `expect(err.code === 401)`。

## 修复建议格式

```
路径: {文件路径}, 行号: {行号}, 问题描述: errcode值断言使用了宽松相等运算符'=='，应使用严格相等运算符'==='。
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

使用状态机解析，追踪字符串字面量内的大括号（含反引号追踪），提取每个`it()`块的行号范围。用于将问题行号关联到所属testcase。

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

### Step 3: 检测.code ==模式

在源代码文件中，查找`.code`后跟`==`（非`===`）的模式。

```python
import re

CODE_EQ_PATTERN = re.compile(r'\.code\s*==(?!=)')

def scan_r022(file_path, base_dir):
    issues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')

    it_blocks = extract_it_blocks(content)

    for line_idx, line in enumerate(lines):
        if not CODE_EQ_PATTERN.search(line):
            continue

        # 跳过注释行
        stripped = line.strip()
        if stripped.startswith('//'):
            continue
        code_part = stripped
        if '//' in stripped:
            code_part = stripped[:stripped.index('//')].strip()
        if not CODE_EQ_PATTERN.search(code_part):
            continue

        line_num = line_idx + 1
        testcase = '-'
        for block in it_blocks:
            if block['start'] <= line_num <= block['end']:
                testcase = block['name']
                break

        rel_path = os.path.relpath(file_path, base_dir)
        issues.append({
            'rule': 'R022',
            'type': 'errcode值断言使用==而非===',
            'severity': 'Critical',
            'file': rel_path,
            'line': line_num,
            'testcase': testcase,
            'snippet': stripped.strip(),
            'suggestion': (
                f"路径: {rel_path}, 行号: {line_num}, "
                f"问题描述: errcode值断言使用了宽松相等运算符'=='，应使用严格相等运算符'==='。"
            ),
        })

    return issues
```

## 错误示例

```typescript
expect(err.code == 0).assertTrue();           // ✗ 错误：使用 ==
expect(err.code == 29360216).assertTrue();     // ✗ 错误：使用 ==
expect((error as BusinessError)?.code == 401).assertTrue();  // ✗ 错误：使用 ==
if (e.code == 801) {                          // ✗ 错误：使用 ==
```

## 正确示例

```typescript
expect(err.code === 0).assertTrue();           // ✓ 正确：使用 ===
expect(err.code === 29360216).assertTrue();     // ✓ 正确：使用 ===
expect((error as BusinessError)?.code === 401).assertTrue();  // ✓ 正确：使用 ===
if (e.code === 801) {                          // ✓ 正确：使用 ===
```

## 陷阱与注意事项

### 陷阱1: 必须区分==和===

正则`\.code\s*==(?!=)`使用负向前瞻`(?!=)`确保只匹配`==`而非`===`。

- `\.code == 401` → 匹配（问题）
- `\.code === 401` → 不匹配（合规）

### 陷阱2: 跳过注释行

`//` 注释中的 `.code ==` 不应被检测。需要先去除注释部分再进行匹配。

```typescript
// expect(err.code == 401).assertTrue();  // ← 被注释掉，不检查
```

### 陷阱3: 多个.code ==在同一行

一行代码中可能包含多个`.code ==`（如`||`组合断言），每个都应报告：

```typescript
expect((err.code == 13900012 || err.code == 13900006)).assertTrue();
// ↑ 两个.code ==都应报告
```

### 陷阱4: 非断言场景中的.code ==

`.code ==`不仅出现在`expect()`断言中，也可能出现在`if`条件判断等场景中。R022对所有`.code ==`统一报告，不区分是否在断言内。因为无论是断言还是条件判断，对errcode都应使用`===`严格比较。

## 输出格式

每条issue的字段：

| 字段 | 值 |
|------|-----|
| rule | `R022` |
| type | `errcode值断言使用==而非===` |
| severity | `Critical` |
| file | 相对路径 |
| line | `.code ==`所在行号 |
| testcase | 所属it()块名称或`-` |
| snippet | 当前行内容 |
| suggestion | 路径: {文件路径}, 行号: {行号}, 问题描述: errcode值断言使用了宽松相等运算符'=='，应使用严格相等运算符'==='。 |

## 排除规则

- `//` 注释行中的 `.code ==` 不检查
- `.code ===`（严格相等）不报告

## 技术规范

### 检测范围补充说明

**检查**:
- 源代码文件（`.ets`, `.ts`, `.js`）中所有 `.code ==`（非`.code ===`）
- 包括 `expect()` 断言、`if` 条件判断等所有场景

**不检查**:
- 注释中的 `.code ==`
- `.code ===`（已使用严格相等）

### 实际案例

```
全仓扫描结果（预估）:
- 问题数: ~8800+ 行包含 .code ==（非===）
- 涉及子系统: 全部子系统
- 典型场景:
  - expect(err.code == 0).assertTrue();
  - expect((error as BusinessError)?.code == 401).assertTrue();
  - if (e.code == 801) { ... }
  - expect((err.code == 13900012 || err.code == 13900006)).assertTrue();
```

### 与R002的关系

- R002: 检查errcode断言中错误码是否为number类型（`"401"` string vs `401` number）
- R022: 检查errcode断言中是否使用严格相等`===`（`==` vs `===`）
- 两个规则互补，可同时触发：`expect(err.code == "401")` 会同时触发R002和R022
