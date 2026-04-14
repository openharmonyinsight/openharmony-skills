# R019: .key重复

> R019是工程级属性重复检测的基类规则。R020（.id重复）与此规则共享完全相同的扫描逻辑，仅检测目标不同。共享函数定义见 [references/project_level_scan.md](../../references/project_level_scan.md)。

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

## 检测模式

```python
import re
KEY_PATTERN = re.compile(
    r'\.key\s*\(\s*(["\'])([^"\']+)\1\s*\)',
    re.MULTILINE
)
```

## 扫描逻辑

### Step 1: 识别独立XTS工程

复用 [references/project_level_scan.md](../../references/project_level_scan.md) 中的 `find_independent_projects()` 函数。必须使用修正后的版本，正确处理group类型父BUILD.gn（见陷阱6）。

### Step 2: 收集工程内所有源代码文件

**关键**: 需要递归收集工程目录下的所有源代码文件（包括子目录），与R011不同（R011只收集根目录下的测试文件）。因为`.key()`可能出现在工程的任意子目录的`.ets`文件中。

复用 `get_project_source_files(project_dir)`。

### Step 3: 提取.key()值

在工程内的源代码文件中，提取所有 `.key('xxx')` 或 `.key("xxx")` 的字符串参数。

复用 `collect_attr_values(project_dir, source_files, base_dir, KEY_PATTERN)`。

### Step 4: 检测重复（每个重复组只报告一次）

复用 `find_duplicate_groups(items)`。

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

        keys = collect_attr_values(project_dir, source_files, base_dir, KEY_PATTERN)
        duplicates = find_duplicate_groups(keys)

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

## 修复建议

确保.key()的值在工程内唯一。修改重复的key值为有意义的唯一标识。

## 修复建议格式

```
路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名称}' 中，.key值 '{key值}' 重复 {重复次数} 次。重复位置: {位置1}, {位置2}, ...
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

`.key('')` 或 `.key("")` 空字符串key值不进行重复检查。`collect_attr_values`已通过 `if not attr_value: continue` 过滤。

### 陷阱6: group类型父BUILD.gn的子工程被错误过滤

**严重性**: 极严重，导致arkui子系统多层嵌套工程全部漏检（49→997个工程，80→1567个问题）

> 详见 [references/TRAPS.md](../../references/TRAPS.md) 陷阱10，以及 [references/project_level_scan.md](../../references/project_level_scan.md) 中的 `find_independent_projects()` 实现。

## 输出格式

| 字段 | 值 |
|------|-----|
| rule | `R019` |
| type | `.key重复` |
| severity | `Critical` |
| file | 相对路径 |
| line | .key()所在行号 |
| testcase | `-` |
| snippet | `.key('customPropertyValue')` |
| suggestion | 路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名}' 中，.key值 '{key值}' 重复 {次数} 次。重复位置: {文件:行号}; ... |

## 排除规则

- 跨工程的同名.key不视为重复
- .key()参数为变量（非字符串字面量）的不进行检查
- .key()参数为空字符串的不进行检查

## 实际案例

```
工程: arkui/ace_c_arkui_test_api13
重复值：customPropertyValue
1、arkui/ace_c_arkui_test_api13/entry/src/ohosTest/ets/MainAbility/pages/customproperty/TestRemoveCustomProperty.ets 45行 .key('customPropertyValue')
2、arkui/ace_c_arkui_test_api13/entry/src/ohosTest/ets/MainAbility/pages/customproperty/TestAddCustomProperty.ets 37行 .key('customPropertyValue')

重复值：buttonCustomProperty
1、arkui/ace_c_arkui_test_api13/entry/src/ohosTest/ets/MainAbility/pages/customproperty/TestRemoveCustomProperty.ets 33行 .key('buttonCustomProperty')
2、arkui/ace_c_arkui_test_api13/entry/src/ohosTest/ets/MainAbility/pages/customproperty/TestAddCustomProperty.ets 38行 .key('buttonCustomProperty')
```
