# R002: 错误码断言必须是number类型

## 规则元信息

| 字段 | 值 |
|------|------|
| 规则编号 | R002 |
| 规则名称 | 错误码断言必须是number类型 |
| 严重级别 | Critical |
| 规则分类 | simple rule（简单规则，可用grep/正则直接检测） |
| 扫描范围 | 所有源代码文件（`.ets`, `.ts`, `.js`） |

## 问题描述

`error.code` 的类型为 `number`，但测试代码中经常使用 **string字面量** 对其进行断言或比较。这属于类型不匹配的低级错误。

**核心原因**: 错误码是数字类型（如 `401`、`14000011`），使用字符串（如 `"401"`、`'14000011'`）进行断言/比较是类型错误。

## 修复方法

将所有 `error.code` 相关的 string 断言/比较改为 number 类型。

## 检测模式

### Pattern 1: `assertEqual` 中的 string 字面量（最常见）

```javascript
// 错误
expect(error.code).assertEqual("401");
expect(error.code).assertEqual('14000011');

// 正确
expect(error.code).assertEqual(401);
expect(error.code).assertEqual(14000011);
```

### Pattern 2: `expect` 中的 string 参数

```javascript
// 错误
expect(error.code, "401");

// 正确
expect(error.code, 401);
```

### Pattern 3: `assertTrue` 中的 string 比较

```javascript
// 错误
expect(error.code === '14000011').assertTrue();

// 正确
expect(error.code === 14000011).assertTrue();
```

### Pattern 4: `if` 条件中的 string 比较（== 和 ===）

```javascript
// 错误
if (error.code == "801") { ... }    // 宽松相等
if (error.code === "401") { ... }   // 严格相等

// 正确
if (error.code == 801) { ... }
if (error.code === 401) { ... }
```

### Pattern 6: string 变量间接断言（变量追踪）

```javascript
// 错误 - 变量定义为string类型
let codeNum = "401";
expect(error.code).assertEqual(codeNum);

// 正确 - 变量定义为number类型
let codeNum = 401;
expect(error.code).assertEqual(codeNum);
```

### Pattern 7: 函数参数类型标注为 string（参数追踪）

```javascript
// 错误 - 函数参数类型标注为string
const requestVideoDestUriError = async (testNum: string, done: Function, destUri: string, errCode: string) => {
  try {
    // ...
  } catch (error) {
    expect(error.code).assertEqual(errCode);  // errCode是string类型
    done();
  }
};

// 正确 - 函数参数类型标注为number
const requestVideoDestUriError = async (testNum: string, done: Function, destUri: string, errCode: number) => {
  try {
    // ...
  } catch (error) {
    expect(error.code).assertEqual(errCode);  // errCode是number类型
    done();
  }
};
```

### Pattern 8: `const` 定义的 string 常量

```javascript
// 错误
const ERROR_PArameter = '23800151';
expect(error.code).assertEqual(ERROR_PArameter);

// 正确
const ERROR_PArameter = 23800151;
expect(error.code).assertEqual(ERROR_PArameter);
```

## 推荐检测正则

### 核心正则（必须实现）

```python
import re

# 精确模式1: expect(xxx.code).assertEqual('string') - string字面量
r002_assertEqual_pattern = re.compile(
    r'expect\s*\(\s*\w+\.code\s*\)\s*\.\s*assertEqual\s*\(\s*[\'"]'
)

# 精确模式2: expect(xxx.code, "string") - expect中的string参数
r002_expect_pattern = re.compile(
    r'expect\s*\(\s*\w+\.code\s*,\s*[\'"]'
)

# 精确模式3: expect(xxx.code === 'string').assertTrue() - string比较在assertTrue中
r002_assertTrue_pattern = re.compile(
    r'expect\s*\(\s*\w+\.code\s*===?\s*[\'"]'
)

# 精确模式4: if (xxx.code == 'string') 或 if (xxx.code === 'string') - if条件中的string比较
# 使用 ===? 匹配 == 和 ===，避免同一行被两个正则重复报告
r002_if_pattern = re.compile(
    r'if\s*\(\s*\w+\.code\s*===?\s*[\'"]'
)
```

### 变量追踪（增强检测）

```python
# 追踪string类型变量定义
r002_var_def_pattern = re.compile(
    r'(?:let|const|var)\s+(\w+)\s*=\s*[\'"]\d+[\'"]'
)

# 追踪string类型函数参数
r002_param_pattern = re.compile(
    r'(\w+)\s*:\s*string'
)

# 追踪string类型常量（文件顶部const定义）
r002_const_pattern = re.compile(
    r'const\s+(\w+)\s*=\s*[\'"]\d+[\'"]'
)
```

## 陷阱与注意事项

### 陷阱1: 不要过度匹配 `err.code`

`err.code` 只有在 `err` 是 `error` 的别名时才应报告。需要通过上下文判断：

```javascript
// 情况A: err是error的别名（应报告）
} catch (err) {
  expect(err.code).assertEqual("401");  // 报告
}

// 情况B: err是其他变量（不应报告）
let err = getSomeObject();
expect(err.code).assertEqual("401");  // err.code 不是 error.code，不报告
```

**处理策略**: 如果 catch 块的参数名为 `err`，则 `err` 是 `error` 的别名，应报告。

### 陷阱2: 不要匹配 `console.log` 中的用法

```javascript
// 不应报告
console.log(`error.code: ${error.code}`);  // 日志输出，不是断言
console.log("error.code is " + error.code);
```

### 陷阱3: 不要匹配赋值语句

```javascript
// 不应报告
let code = error.code;  // 赋值，不是断言
const myCode = error.code.toString();  // 转换，不是断言
```

### 陷阱4: string字面量中包含非数字内容

如果 string 字面量不是纯数字，则不是错误码断言，不应报告：

```javascript
// 不应报告 - "PARAM_ERROR" 不是错误码数字
expect(error.code).assertEqual("PARAM_ERROR");
expect(error.code).assertEqual("business_error");
```

**处理策略**: 只匹配 `assertEqual` 后面的引号内容为纯数字的情况。可以用正则进一步验证：

```python
r002_assertEqual_with_number = re.compile(
    r'expect\s*\(\s*\w+\.code\s*\)\s*\.\s*assertEqual\s*\(\s*[\'"](\d+)[\'"]'
)
```

## 扫描实现

### 文件过滤

```python
import os

def is_test_file(filepath):
    """检查是否为测试文件"""
    test_extensions = ('.test.ets', '.test.ts', '.test.js')
    return any(filepath.endswith(ext) for ext in test_extensions)
```

### 行级检测函数

```python
def scan_r002_line(line, line_num, string_vars=None):
    """
    扫描单行代码中的R002问题。

    Args:
        line: 当前行内容
        line_num: 行号
        string_vars: 已知的string类型变量集合（来自变量追踪）

    Returns:
        list[dict]: 发现的问题列表
    """
    issues = []

    # 跳过注释行
    stripped = line.strip()
    if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('/*'):
        return issues

    # 跳过console.log
    if 'console.log' in line or 'console.info' in line or 'console.warn' in line or 'console.error' in line:
        return issues

    # 跳过赋值语句（左侧有 = 且不是 ==）
    if re.match(r'\s*(?:let|const|var)\s+', line):
        return issues

    # Pattern 1: expect(xxx.code).assertEqual('...')
    m = r002_assertEqual_with_number.search(line)
    if m:
        issues.append({
            'rule': 'R002',
            'type': '错误码断言必须是number类型',
            'severity': 'Critical',
            'line': line_num,
            'snippet': stripped,
            'suggestion': f'error.code 是 number 类型，断言值 "{m.group(1)}" 应改为数字: {m.group(1)}'
        })
        return issues

    # Pattern 2: expect(xxx.code, '...')
    m = r002_expect_pattern.search(line)
    if m:
        issues.append({
            'rule': 'R002',
            'type': '错误码断言必须是number类型',
            'severity': 'Critical',
            'line': line_num,
            'snippet': stripped,
            'suggestion': 'error.code 是 number 类型，expect() 中的比较值应使用数字类型'
        })
        return issues

    # Pattern 3: expect(xxx.code === '...').assertTrue()
    m = r002_assertTrue_pattern.search(line)
    if m:
        issues.append({
            'rule': 'R002',
            'type': '错误码断言必须是number类型',
            'severity': 'Critical',
            'line': line_num,
            'snippet': stripped,
            'suggestion': 'error.code 是 number 类型，比较值应使用数字类型'
        })
        return issues

    # Pattern 4: if (xxx.code == '...') 或 if (xxx.code === '...')
    m = r002_if_pattern.search(line)
    if m:
        issues.append({
            'rule': 'R002',
            'type': '错误码断言必须是number类型',
            'severity': 'Critical',
            'line': line_num,
            'snippet': stripped,
            'suggestion': 'error.code 是 number 类型，if 条件中的比较值应使用数字类型'
        })
        return issues

    return issues
```

### 文件级检测（含变量追踪）

```python
def scan_r002_file(filepath, content):
    """
    扫描整个文件中的R002问题，包含变量追踪。

    Args:
        filepath: 文件路径
        content: 文件内容

    Returns:
        list[dict]: 发现的问题列表
    """
    issues = []
    lines = content.split('\n')

    # 第一遍：收集string类型变量和常量定义
    string_vars = set()
    for line in lines:
        # let/const/var xxx = "401"
        m = re.search(r'(?:let|const|var)\s+(\w+)\s*=\s*[\'"](\d+)[\'"]', line)
        if m:
            string_vars.add(m.group(1))

    # 第二遍：收集string类型函数参数
    for line in lines:
        params = re.findall(r'(\w+)\s*:\s*string', line)
        string_vars.update(params)

    # 第三遍：逐行检测
    for i, line in enumerate(lines, 1):
        line_issues = scan_r002_line(line, i, string_vars)
        issues.extend(line_issues)

        # 额外检测：变量追踪模式
        # expect(error.code).assertEqual(codeNum) 其中 codeNum 是 string 类型
        if string_vars:
            m = re.search(r'expect\s*\(\s*(\w+)\.code\s*\)\s*\.\s*assertEqual\s*\(\s*(\w+)\s*\)', line)
            if m and m.group(2) in string_vars:
                issues.append({
                    'rule': 'R002',
                    'type': '错误码断言必须是number类型',
                    'severity': 'Critical',
                    'line': i,
                    'snippet': line.strip(),
                    'suggestion': f'变量 "{m.group(2)}" 是 string 类型，应改为 number 类型'
                })

            # if (error.code == codeNum) 其中 codeNum 是 string 类型
            m = re.search(r'if\s*\(\s*(\w+)\.code\s*==\s*(\w+)\s*\)', line)
            if m and m.group(2) in string_vars:
                issues.append({
                    'rule': 'R002',
                    'type': '错误码断言必须是number类型',
                    'severity': 'Critical',
                    'line': i,
                    'snippet': line.strip(),
                    'suggestion': f'变量 "{m.group(2)}" 是 string 类型，应改为 number 类型'
                })

    return issues
```

## 输出格式

每条问题必须包含以下字段：

```python
{
    'rule': 'R002',
    'type': '错误码断言必须是number类型',
    'severity': 'Critical',
    'file': 'path/to/file.test.ets',
    'line': 25,
    'testcase': 'testFuncName',  # 所属用例名称（it()的第一个参数），无对应用例时为 '-'
    'snippet': 'expect(error.code).assertEqual("401")',
    'suggestion': 'error.code 是 number 类型，断言值 "401" 应改为数字: 401'
}
```

### testcase 字段说明

- 从问题所在行向上查找包含该行的 `it()` 块，取 `it('` 后面的第一个字符串参数
- 非测试文件中的问题：`testcase` 为 `-`
- 测试文件中不在任何 `it()` 块内的问题：`testcase` 为 `-`

## 完整错误/正确示例

### 错误示例

```javascript
// 错误1: assertEqual中使用string字面量
it('test001', Level.LEVEL0, () => {
  try {
    // ...
  } catch (error) {
    expect(error.code).assertEqual("401");  // R002
  }
});

// 错误2: assertTrue中的string比较
it('test002', Level.LEVEL0, () => {
  expect(error.code === '14000011').assertTrue();  // R002
});

// 错误3: if条件中的宽松string比较
it('test003', Level.LEVEL0, () => {
  if (error.code == "801") {  // R002
    // ...
  }
});

// 错误4: if条件中的严格string比较
it('test004', Level.LEVEL0, () => {
  if (error.code === "401") {  // R002
    // ...
  }
});

// 错误5: string变量间接断言
it('test005', Level.LEVEL0, () => {
  let codeNum = "401";
  if (error.code == codeNum) {  // R002
    expect(error.code).assertEqual(codeNum);  // R002
  }
});

// 错误6: string类型函数参数
const requestVideoDestUriError = async (testNum: string, done: Function, destUri: string, errCode: string) => {
  try {
    // ...
  } catch (error) {
    expect(error.code).assertEqual(errCode);  // R002 - errCode是string类型
    done();
  }
};

// 错误7: const定义的string常量
const ERROR_PArameter = '23800151';
it('test007', Level.LEVEL0, () => {
  expect(error.code).assertEqual(ERROR_PArameter);  // R002
});

// 错误8: err是error的别名
it('test008', Level.LEVEL0, () => {
  try {
    // ...
  } catch (err) {
    expect(err.code).assertEqual("401");  // R002 - err是error的别名
  }
});
```

### 正确示例

```javascript
// 正确1: 使用number字面量
it('test001', Level.LEVEL0, () => {
  try {
    // ...
  } catch (error) {
    expect(error.code).assertEqual(401);  // number类型
  }
});

// 正确2: number比较
it('test002', Level.LEVEL0, () => {
  expect(error.code === 14000011).assertTrue();  // number比较
});

// 正确3: number条件判断
it('test003', Level.LEVEL0, () => {
  if (error.code == 801) {  // number比较
    // ...
  }
});

// 正确4: number变量
it('test004', Level.LEVEL0, () => {
  let codeNum = 401;
  if (error.code == codeNum) {
    expect(error.code).assertEqual(codeNum);
  }
});

// 正确5: number类型函数参数
const requestVideoDestUriError = async (testNum: string, done: Function, destUri: string, errCode: number) => {
  try {
    // ...
  } catch (error) {
    expect(error.code).assertEqual(errCode);  // errCode是number类型
    done();
  }
};

// 正确6: number常量
const ERROR_PArameter = 23800151;
it('test006', Level.LEVEL0, () => {
  expect(error.code).assertEqual(ERROR_PArameter);  // number类型
});
```

## 不应报告的场景

```javascript
// 场景1: console.log - 日志输出不是断言
console.log(`error.code: ${error.code}`);
console.log("error code is " + error.code);

// 场景2: 赋值语句
let code = error.code;
const myCode = error.code.toString();

// 场景3: err不是error的别名
let err = getSomeObject();
expect(err.code).assertEqual("some-code");  // err.code 不是 error.code

// 场景4: 非纯数字的string字面量
expect(error.code).assertEqual("PARAM_ERROR");  // 不是数字错误码

// 场景5: 注释行
// expect(error.code).assertEqual("401");  // 注释中的代码
```
