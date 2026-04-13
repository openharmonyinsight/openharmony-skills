# R011: testsuite重复

## 规则信息

| 属性 | 值 |
|------|-----|
| 规则编号 | R011 |
| 问题类型 | testsuite重复 |
| 严重级别 | Critical |
| 规则复杂度 | complex |
| 扫描范围 | 同一独立XTS工程内的所有测试文件 |
| testcase字段 | `-`（describe不在it()块内） |

## 问题描述

一个独立XTS工程下不允许describe命名重复。即同一个独立XTS工程中，所有测试文件里的`describe()`函数的第一个参数不能重复。

## 修复建议

确保testsuite命名唯一。重复的testsuite名称后追加`Adapt`+三位数字编号。

## 自动修复规则

- **命名格式**: `{原testsuite名称}Adapt{三位数字}`
- **保留首个**: 保留第一个出现的testsuite名称不变
- **递增编号**: 后续重复的依次编号为Adapt001, Adapt002, Adapt003...

## 修复建议格式

```
与{文件路径}:{行号}重复，修改testsuite名称，确保工程内唯一
```

## 扫描逻辑

### Step 1: 识别独立XTS工程

独立XTS工程的判断标准：
1. 目录下存在`BUILD.gn`文件
2. 目录下存在测试文件（`.test.ets`, `.test.ts`, `.test.js`）
3. **不是group类型的BUILD.gn**（group类型的BUILD.gn只是聚合其他工程的入口，不包含实际的测试代码）

```python
import os
import re

def is_group_build_gn(build_gn_path):
    with open(build_gn_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return bool(re.search(r'\bgroup\s*\(', content))

def find_independent_projects(scan_root):
    projects = []
    for dirpath, dirnames, filenames in os.walk(scan_root):
        if 'BUILD.gn' in filenames:
            build_gn_path = os.path.join(dirpath, 'BUILD.gn')
            if is_group_build_gn(build_gn_path):
                continue

            has_test_files = any(
                fn.endswith(('.test.ets', '.test.ts', '.test.js'))
                for fn in filenames
            )
            if has_test_files:
                projects.append(os.path.abspath(dirpath))
    return projects
```

### Step 2: 过滤子工程文件

**关键步骤**: 每个独立工程只扫描直接属于该工程的测试文件，必须排除子目录中的独立工程文件，否则会产生跨工程误报。

```python
def get_project_test_files(project_dir):
    test_extensions = ('.test.ets', '.test.ts', '.test.js')
    test_files = []
    for fn in os.listdir(project_dir):
        if fn.endswith(test_extensions):
            test_files.append(os.path.join(project_dir, fn))
    return test_files
```

### Step 3: 收集describe()名称

在工程内的测试文件中，提取所有`describe()`函数的第一个参数。

```python
DESCRIBE_PATTERN = re.compile(
    r'describe\s*\(\s*["\']([^"\']+)["\']',
    re.MULTILINE
)

def collect_describe_info(project_dir, test_files, base_dir):
    describes = []

    for file_path in test_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for match in DESCRIBE_PATTERN.finditer(content):
            name = match.group(1)
            line_num = content[:match.start()].count('\n') + 1
            rel_path = os.path.relpath(file_path, base_dir)

            describes.append({
                'name': name,
                'file': rel_path,
                'line': line_num,
                'abs_path': os.path.abspath(file_path),
            })

    return describes
```

### Step 4: 检测重复（每个重复组只报告一次）

```python
from collections import defaultdict

def find_duplicates(describes):
    name_to_occurrences = defaultdict(list)
    for desc in describes:
        name_to_occurrences[desc['name']].append(desc)

    duplicates = []
    for name, occurrences in name_to_occurrences.items():
        if len(occurrences) > 1:
            first = occurrences[0]
            other_locs = []
            for occ in occurrences[1:]:
                other_locs.append(f"{occ['file']}:{occ['line']}")
            duplicates.append({
                'name': name,
                'count': len(occurrences),
                'first_file': first['file'],
                'first_line': first['line'],
                'other_locations': other_locs,
            })
    return duplicates
```

### Step 5: 生成问题报告

**关键**: 只为每个重复组的第一次出现创建一条问题报告。

```python
def scan_r011(scan_root, base_dir):
    issues = []
    projects = find_independent_projects(scan_root)

    for project_dir in projects:
        test_files = get_project_test_files(project_dir)
        if not test_files:
            continue

        describes = collect_describe_info(project_dir, test_files, base_dir)
        duplicates = find_duplicates(describes)

        for dup in duplicates:
            rel_project = os.path.relpath(project_dir, base_dir)
            other_info = '; '.join(dup['other_locations'])

            issues.append({
                'rule': 'R011',
                'type': 'testsuite重复',
                'severity': 'Critical',
                'file': dup['first_file'],
                'line': dup['first_line'],
                'testcase': '-',
                'snippet': f'describe("{dup["name"]}", ...)',
                'suggestion': (
                    f'在独立XTS工程 \'{rel_project}\' 中，testsuite名称 '
                    f'\'{dup["name"]}\' 重复 {dup["count"]} 次。'
                    f'重复位置: {other_info}。'
                    f'修改testsuite名称，确保工程内唯一。'
                ),
            })

    return issues
```

## 常见错误及避免方法

### 错误1: 未过滤子工程文件（跨工程误报）

```
project/
├── BUILD.gn          # 独立工程A
├── test1.test.js
├── sub_project/
│   ├── BUILD.gn      # 独立工程B（子工程）
│   └── test2.test.js
```

如果不过滤子工程文件，工程A的扫描会把工程B的describe也收集进来，产生跨工程误报。

**避免方法**: 只收集工程根目录下的测试文件（`os.listdir(project_dir)`），不递归子目录。

### 错误2: 同一重复组报告多次

如果同一组重复的describe名称被报告多次（例如3个重复的describe报告了3条问题），会导致Excel报告中出现冗余。

**避免方法**: 每个重复的describe名称只报告一次，指向第一次出现的位置。

### 错误3: describe参数匹配不精确

使用`describe\s*\(\s*["\']([^"\']+)["\']`匹配describe的第一个参数，需要确保只匹配第一个参数。

**避免方法**: 使用非贪婪匹配`[^"\']+`精确提取第一个字符串参数。

### 错误4: 路径不一致导致relative_to失败

当扫描根目录和文件路径不一致时（例如一个使用绝对路径，另一个使用相对路径），`os.path.relpath()`会抛出异常。

**避免方法**: 所有路径在使用前必须通过`os.path.abspath()`或`pathlib.Path.resolve()`转换为绝对路径。

```python
from pathlib import Path

scan_root = Path(scan_root).resolve()
base_dir = Path(base_dir).resolve()
```

### 错误5: Group类型BUILD.gn误识别为独立工程

Group类型的BUILD.gn只是聚合入口，不包含实际的测试代码。如果将其识别为独立工程，会导致大量误报。

**避免方法**: 检查BUILD.gn内容是否包含`group(`关键字，如果包含则跳过。

## 错误示例

```javascript
// File1.test.js（同一独立工程内）
export default function TestSuite1() {
  describe("TransientTaskJsTest", function () {
    // 测试代码
  });
}

// File2.test.js（同一独立工程内）
export default function TestSuite2() {
  describe("TransientTaskJsTest", function () {  // ✗ 错误：与File1.test.js重复
    // 测试代码
  });
}
```

## 正确示例

```javascript
// File1.test.js（同一独立工程内）
export default function TestSuite1() {
  describe("TransientTaskJsTest", function () {  // ✓ 首次出现，保持不变
    // 测试代码
  });
}

// File2.test.js（同一独立工程内）
export default function TestSuite2() {
  describe("TransientTaskJsTestAdapt001", function () {  // ✓ 修复后命名唯一
    // 测试代码
  });
}
```

## 多个重复修复示例

```javascript
// 修复前
describe("ContinuousTaskJsTest", function () { }  // 首次出现
describe("ContinuousTaskJsTest", function () { }  // 第二次
describe("ContinuousTaskJsTest", function () { }  // 第三次

// 修复后
describe("ContinuousTaskJsTest", function () { }           // 保持不变
describe("ContinuousTaskJsTestAdapt001", function () { }   // Adapt001
describe("ContinuousTaskJsTestAdapt002", function () { }   // Adapt002
```

## 输出格式

每条issue的字段：

| 字段 | 值 |
|------|-----|
| rule | `R011` |
| type | `testsuite重复` |
| severity | `Critical` |
| file | 相对路径（如`xxx/File1.test.js`） |
| line | describe所在行号 |
| testcase | `-` |
| snippet | `describe("xxx", ...)` |
| suggestion | 在独立XTS工程 '{工程名}' 中，testsuite名称 '{名称}' 重复 {次数} 次。重复位置: {文件:行号}; ... |

## 排除规则

- 跨工程的同名describe不视为重复
- 包含变量拼接的describe名称不进行重复检查（如`describe("Test" + idx, ...)`）

## 技术规范

### 检测范围补充说明

**不检查**:
- 跨工程的describe块
- 不同独立工程间的describe块
- 子工程的describe块（由父工程检查时会过滤）

### 额外常见错误

##### 错误四: Python语法错误

**问题**: `for dep_entry in dep dep_entries:`
**后果**: 脚本无法运行
**解决**: 修复语法错误

##### 错误五: 正则表达式列表定义错误

**问题**: patterns列表混入字符串描述
**后果**: describe块无法正确识别
**解决**: 移除多余字符

## 技术挑战与解决方案

### 正确识别独立XTS工程边界

**挑战**: 正确识别独立XTS工程边界

**解决方案**:
```python
def is_independent_xts_project(dir_path):
    has_build_gn = os.path.exists(os.path.join(dir_path, "BUILD.gn"))
    has_test_files = any(glob.glob(...))
    return has_build_gn and has_test_files
```
