# R019: .key重复

## 规则信息

| 属性 | 值 |
|------|-----|
| 规则编号 | R019 |
| 问题类型 | .key重复 |
| 严重级别 | Critical |
| 规则复杂度 | complex |
| 扫描范围 | 同一独立XTS工程内的所有源代码文件（`.ets`, `.ts`, `.js`） |
| testcase字段 | `-`（.key()不在it()块内） |

## 问题描述

一个独立XTS工程下的页面设计中，`.key()` 的字符串参数值不允许重复。即同一个独立XTS工程中，所有源代码文件里 `.key('xxx')` 的字符串参数值不能重复。

## 修复建议

确保.key()的值在工程内唯一。修改重复的key值为有意义的唯一标识。

## 修复建议格式

```
路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名称}' 中，.key值 '{key值}' 重复 {重复次数} 次。重复位置: {位置1}, {位置2}, ...
```

## 扫描逻辑

### Step 1: 识别独立XTS工程

复用R011的独立XTS工程识别逻辑：

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

            has_source_files = any(
                fn.endswith(('.ets', '.ts', '.js'))
                for fn in filenames
            )
            if has_source_files:
                projects.append(os.path.abspath(dirpath))
    return projects
```

### Step 2: 收集工程内所有源代码文件

**关键**: 需要递归收集工程目录下的所有源代码文件（包括子目录），与R011不同（R011只收集根目录下的测试文件）。因为`.key()`可能出现在工程的任意子目录的`.ets`文件中。

```python
def get_project_source_files(project_dir):
    source_extensions = ('.ets', '.ts', '.js')
    source_files = []
    for root, dirs, files in os.walk(project_dir):
        for fn in files:
            if fn.endswith(source_extensions):
                source_files.append(os.path.join(root, fn))
    return source_files
```

### Step 3: 提取.key()值

在工程内的源代码文件中，提取所有 `.key('xxx')` 或 `.key("xxx")` 的字符串参数。

```python
KEY_PATTERN = re.compile(
    r'\.key\s*\(\s*(["\'])([^"\']+)\1\s*\)',
    re.MULTILINE
)

def collect_key_info(project_dir, source_files, base_dir):
    keys = []

    for file_path in source_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for match in KEY_PATTERN.finditer(content):
            key_value = match.group(2)
            line_num = content[:match.start()].count('\n') + 1
            rel_path = os.path.relpath(file_path, base_dir)

            keys.append({
                'value': key_value,
                'file': rel_path,
                'line': line_num,
                'abs_path': os.path.abspath(file_path),
            })

    return keys
```

### Step 4: 检测重复（每个重复组只报告一次）

```python
from collections import defaultdict

def find_duplicate_keys(keys):
    value_to_occurrences = defaultdict(list)
    for key_info in keys:
        value_to_occurrences[key_info['value']].append(key_info)

    duplicates = []
    for value, occurrences in value_to_occurrences.items():
        if len(occurrences) > 1:
            first = occurrences[0]
            other_locs = []
            for occ in occurrences[1:]:
                other_locs.append(f"{occ['file']}:{occ['line']}")
            duplicates.append({
                'value': value,
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
def scan_r019(scan_root, base_dir):
    issues = []
    projects = find_independent_projects(scan_root)

    for project_dir in projects:
        source_files = get_project_source_files(project_dir)
        if not source_files:
            continue

        keys = collect_key_info(project_dir, source_files, base_dir)
        duplicates = find_duplicate_keys(keys)

        for dup in duplicates:
            rel_project = os.path.relpath(project_dir, base_dir)
            other_info = '; '.join(dup['other_locations'])

            issues.append({
                'rule': 'R019',
                'type': '.key重复',
                'severity': 'Critical',
                'file': dup['first_file'],
                'line': dup['first_line'],
                'testcase': '-',
                'snippet': f".key('{dup['value']}')",
                'suggestion': (
                    f"路径: {dup['first_file']}, 行号: {dup['first_line']}, "
                    f"问题描述: 在独立XTS工程 '{rel_project}' 中，.key值 "
                    f"'{dup['value']}' 重复 {dup['count']} 次。"
                    f"重复位置: {other_info}。"
                ),
            })

    return issues
```

## 错误示例

```typescript
// File1: TestAddCustomProperty.ets（同一独立工程内）
Button('Add')
  .key('buttonCustomProperty')    // 第一次出现

Text('Custom')
  .key('customPropertyValue')     // 第一次出现
```

```typescript
// File2: TestRemoveCustomProperty.ets（同一独立工程内）
Button('Remove')
  .key('buttonCustomProperty')    // ✗ 错误：与File1重复

Text('RemoveCustom')
  .key('customPropertyValue')     // ✗ 错误：与File1重复
```

## 正确示例

```typescript
// File1: TestAddCustomProperty.ets（同一独立工程内）
Button('Add')
  .key('addButtonCustomProperty')     // ✓ key值唯一

Text('Custom')
  .key('addCustomPropertyValue')      // ✓ key值唯一
```

```typescript
// File2: TestRemoveCustomProperty.ets（同一独立工程内）
Button('Remove')
  .key('removeButtonCustomProperty')  // ✓ key值唯一

Text('RemoveCustom')
  .key('removeCustomPropertyValue')   // ✓ key值唯一
```

## 陷阱与注意事项

### 陷阱1: 与R011的工程文件收集方式不同

R011只收集工程根目录下的测试文件（`os.listdir(project_dir)`），而R019需要递归收集工程下所有子目录的源代码文件（`os.walk(project_dir)`），因为`.key()`可能出现在`entry/src/ohosTest/ets/MainAbility/pages/`等深层子目录的`.ets`文件中。

### 陷阱2: .key()参数可能是变量

如果`.key()`的参数不是字符串字面量而是变量（如`.key(myKeyVar)`），则不进行重复检查。正则`.key\s*\(\s*(["\'])([^"\']+)\1\s*\)`已经自然排除了这种情况。

### 陷阱3: 跨工程的同名.key不视为重复

与R011/testsuite重复规则一致，不同独立XTS工程之间的同名.key值不视为重复。

### 陷阱4: 同一重复组只报告一次

同一组重复的.key值只报告第一次出现的行号，后续重复行号在修复建议中列出。避免同一组重复被多次报告。

### 陷阱5: 空字符串key值

`.key('')` 或 `.key("")` 空字符串key值不进行重复检查。如果需要检测，可以在收集阶段过滤掉空字符串：

```python
if not key_value:
    continue
```

### 陷阱6: group类型父BUILD.gn的子工程被错误过滤

- **严重性**: 极严重，导致arkui子系统ace_ets_component_seven等多层嵌套工程全部漏检（49→997个工程，80→1567个问题）
- **问题**: 独立XTS工程识别时，"过滤包含子BUILD.gn的父目录"这一步将所有有父BUILD.gn的子目录标记为`parent_dirs`并排除。但如果父BUILD.gn是`group()`类型（聚合构建，不产生HAP），其子目录仍然是独立XTS工程，不应被排除。
- **典型结构**:
```
ace_ets_component_seven/           ← BUILD.gn (group类型，聚合构建)
  ├── ace_ets_component_seven_special/     ← BUILD.gn (独立工程，应扫描)
  │     ├── entry/src/main/ets/.../geometryTransition.ets  .key('button') 31行
  │     ├── entry/src/main/ets/.../button.ets              .key('button') 56行
  │     ├── entry/src/main/ets/.../motionPath.ets          .key('button') 38行
  │     └── entry/src/main/ets/.../transition.ets          .key('button') 40行
  ├── ace_ets_component_common_seven_attrs_align/  ← BUILD.gn (独立工程，应扫描)
  └── ... (120+个子工程)
```
- **错误实现**: 先收集所有有子BUILD.gn的目录为`parent_dirs`，再过滤group。由于group父目录本身不会被标记为`parent_dirs`（它是顶层），但其子目录会被标记为`parent_dirs`（因为父目录有BUILD.gn），导致所有子工程被排除。
- **正确实现**: 过滤`parent_dirs`时，只将"父目录是非group的BUILD.gn目录"的子目录标记为`parent_dirs`。group类型的父BUILD.gn不阻止其子目录成为独立工程。
```python
def find_independent_projects(scan_root):
    all_build_gn_dirs = set()
    for dirpath, dirnames, filenames in os.walk(scan_root):
        if 'BUILD.gn' in filenames:
            all_build_gn_dirs.add(os.path.abspath(dirpath))

    # 只收集非group的BUILD.gn目录
    non_group_dirs = set()
    for d in all_build_gn_dirs:
        if not is_group_build_gn(os.path.join(d, 'BUILD.gn')):
            non_group_dirs.add(d)

    # 只将"父目录是非group BUILD.gn"的子目录标记为应排除
    parent_dirs = set()
    for d in all_build_gn_dirs:
        if d in parent_dirs:
            continue
        parent = os.path.dirname(d)
        while parent != os.path.abspath(scan_root) and parent != '/':
            if parent in non_group_dirs:
                parent_dirs.add(d)
                break
            parent = os.path.dirname(parent)

    for dirpath in all_build_gn_dirs:
        if dirpath in parent_dirs:
            continue
        if is_group_build_gn(os.path.join(dirpath, 'BUILD.gn')):
            continue
        projects.append(dirpath)
    return projects
```
- **影响**: R011, R019（所有工程级检测规则）

## 输出格式

每条issue的字段：

| 字段 | 值 |
|------|-----|
| rule | `R019` |
| type | `.key重复` |
| severity | `Critical` |
| file | 相对路径（如`arkui/ace_c_arkui_test_api13/entry/src/ohosTest/ets/.../TestAddCustomProperty.ets`） |
| line | .key()所在行号 |
| testcase | `-` |
| snippet | `.key('customPropertyValue')` |
| suggestion | 路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名}' 中，.key值 '{key值}' 重复 {次数} 次。重复位置: {文件:行号}; ... |

## 排除规则

- 跨工程的同名.key不视为重复
- .key()参数为变量（非字符串字面量）的不进行检查
- .key()参数为空字符串的不进行检查（可选）

## 技术规范

### 检测范围补充说明

**检查**:
- 同一独立XTS工程内所有源代码文件（`.ets`, `.ts`, `.js`）中的`.key()`字符串参数值
- 递归扫描工程目录下所有子目录

**不检查**:
- 跨工程的.key值
- .key()参数为变量的情况
- 非独立XTS工程的文件

### 实际案例

```
工程: arkui/ace_c_arkui_test_api13
重复值：customPropertyValue
1、arkui/ace_c_arkui_test_api13/entry/src/ohosTest/ets/MainAbility/pages/customproperty/TestRemoveCustomProperty.ets 45行 .key('customPropertyValue')
2、arkui/ace_c_arkui_test_api13/entry/src/ohosTest/ets/MainAbility/pages/customproperty/TestAddCustomProperty.ets 37行 .key('customPropertyValue')

重复值：buttonCustomProperty
1、arkui/ace_c_arkui_test_api13/entry/src/ohosTest/ets/MainAbility/pages/customproperty/TestRemoveCustomProperty.ets 33行 .key('buttonCustomProperty')
2、arkui/ace_c_arkui_test_api13/entry/src/ohosTest/ets/MainAbility/pages/customproperty/TestAddCustomProperty.ets 38行 .key('buttonCustomProperty')
```
