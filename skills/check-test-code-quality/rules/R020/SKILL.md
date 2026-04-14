# R020: .id重复

## 规则信息

| 属性 | 值 |
|------|-----|
| 规则编号 | R020 |
| 问题类型 | .id重复 |
| 严重级别 | Critical |
| 规则复杂度 | complex |
| 扫描范围 | 同一独立XTS工程内的所有源代码文件（`.ets`, `.ts`, `.js`） |
| testcase字段 | `-`（.id()不在it()块内） |

## 问题描述

一个独立XTS工程下的页面设计中，`.id()` 的字符串参数值不允许重复。即同一个独立XTS工程中，所有源代码文件里 `.id('xxx')` 的字符串参数值不能重复。

## 与R019的关系

R020与R019的扫描逻辑完全一致，唯一差异是检测目标属性。两者共享相同的工程级检测基类（见 [references/project_level_scan.md](../../references/project_level_scan.md)），包括：

- `find_independent_projects()` — 工程边界识别
- `get_project_source_files()` — 递归源文件收集
- `collect_attr_values()` — 属性值提取
- `find_duplicate_groups()` — 重复检测

## 差异对照

| 属性 | R019 | R020 |
|------|------|------|
| 检测目标 | `.key('xxx')` | `.id('xxx')` |
| 正则 | `\.key\s*\(\s*(["\'])([^"\']+)\1\s*\)` | `\.id\s*\(\s*(["\'])([^"\']+)\1\s*\)` |
| 问题描述 | .key重复 | .id重复 |

## 检测模式

```python
import re
ID_PATTERN = re.compile(
    r'\.id\s*\(\s*(["\'])([^"\']+)\1\s*\)',
    re.MULTILINE
)
```

## 扫描逻辑

1. **识别独立XTS工程**: 复用 `find_independent_projects()`，见 [references/project_level_scan.md](../../references/project_level_scan.md)
2. **收集工程内所有源代码文件**: 递归收集（`os.walk`），见 `get_project_source_files()`
3. **提取.id()值**: 复用 `collect_attr_values(project_dir, source_files, base_dir, ID_PATTERN)`
4. **检测重复**: 复用 `find_duplicate_groups(items)`
5. **生成报告**: 每个重复组只报告第一次出现

## 扫描代码

```python
def scan_r020(scan_root, base_dir):
    issues = []
    projects = find_independent_projects(scan_root)

    for project_dir in projects:
        source_files = get_project_source_files(project_dir)
        if not source_files:
            continue

        ids = collect_attr_values(project_dir, source_files, base_dir, ID_PATTERN)
        duplicates = find_duplicate_groups(ids)

        for dup in duplicates:
            rel_project = os.path.relpath(project_dir, base_dir)
            other_info = '; '.join(dup['other_locations'])

            issues.append({
                'rule': 'R020',
                'type': '.id重复',
                'severity': 'Critical',
                'file': dup['first_file'],
                'line': dup['first_line'],
                'testcase': '-',
                'snippet': f".id('{dup['value']}')",
                'suggestion': (
                    f"路径: {dup['first_file']}, 行号: {dup['first_line']}, "
                    f"问题描述: 在独立XTS工程 '{rel_project}' 中，.id值 "
                    f"'{dup['value']}' 重复 {dup['count']} 次。"
                    f"重复位置: {other_info}。"
                ),
            })

    return issues
```

## 修复建议

确保.id()的值在工程内唯一。修改重复的id值为有意义的唯一标识。

## 修复建议格式

```
路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名称}' 中，.id值 '{id值}' 重复 {重复次数} 次。重复位置: {位置1}, {位置2}, ...
```

## 错误示例

```typescript
// File1: TestAddCustomProperty.ets（同一独立工程内）
Button('Add')
  .id('buttonCustomProperty')    // 第一次出现

Text('Custom')
  .id('customPropertyValue')     // 第一次出现
```

```typescript
// File2: TestRemoveCustomProperty.ets（同一独立工程内）
Button('Remove')
  .id('buttonCustomProperty')    // 错误：与File1重复

Text('RemoveCustom')
  .id('customPropertyValue')     // 错误：与File1重复
```

## 正确示例

```typescript
// File1: TestAddCustomProperty.ets（同一独立工程内）
Button('Add')
  .id('addButtonCustomProperty')     // id值唯一

Text('Custom')
  .id('addCustomPropertyValue')      // id值唯一
```

```typescript
// File2: TestRemoveCustomProperty.ets（同一独立工程内）
Button('Remove')
  .id('removeButtonCustomProperty')  // id值唯一

Text('RemoveCustom')
  .id('removeCustomPropertyValue')   // id值唯一
```

## 陷阱

与R019完全一致，详见 [rules/R019/SKILL.md](../R019/SKILL.md) 的陷阱章节。

## 输出格式

| 字段 | 值 |
|------|-----|
| rule | `R020` |
| type | `.id重复` |
| severity | `Critical` |
| file | 相对路径 |
| line | .id()所在行号 |
| testcase | `-` |
| snippet | `.id('customPropertyValue')` |
| suggestion | 路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名}' 中，.id值 '{id值}' 重复 {次数} 次。重复位置: {文件:行号}; ... |
