# 工程级检测共享逻辑

本文件定义R011、R019、R020等工程级规则共用的检测基类。R019（.key重复）和R020（.id重复）的扫描逻辑完全一致，仅正则模式和规则标识不同，其余步骤均复用以下共享函数。

## 共享函数

### is_group_build_gn(build_gn_path)

判断BUILD.gn是否为group类型（聚合构建）。

```python
import os
import re

def is_group_build_gn(build_gn_path):
    try:
        with open(build_gn_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return bool(re.search(r'\bgroup\s*\(', content))
    except Exception:
        return False
```

### find_independent_projects(scan_root)

识别所有独立XTS工程目录。group类型的BUILD.gn只是聚合入口，不阻止其子目录成为独立工程。

```python
def find_independent_projects(scan_root):
    all_build_gn_dirs = set()
    for dirpath, dirnames, filenames in os.walk(scan_root):
        if 'BUILD.gn' in filenames:
            all_build_gn_dirs.add(os.path.abspath(dirpath))

    non_group_dirs = {
        d for d in all_build_gn_dirs
        if not is_group_build_gn(os.path.join(d, 'BUILD.gn'))
    }

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

    projects = []
    for dirpath in all_build_gn_dirs:
        if dirpath in parent_dirs:
            continue
        if is_group_build_gn(os.path.join(dirpath, 'BUILD.gn')):
            continue
        has_source_files = any(
            fn.endswith(('.ets', '.ts', '.js'))
            for fn in os.listdir(dirpath)
        )
        if has_source_files:
            projects.append(dirpath)
    return projects
```

### get_project_source_files(project_dir)

递归收集工程目录下所有源代码文件（包括子目录）。

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

### collect_attr_values(project_dir, source_files, base_dir, pattern)

按正则提取文件中的属性值。pattern需有两个捕获组：(quote, value)。空字符串自动跳过。

```python
def collect_attr_values(project_dir, source_files, base_dir, pattern):
    items = []
    for file_path in source_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue
        for match in pattern.finditer(content):
            attr_value = match.group(2)
            if not attr_value:
                continue
            line_num = content[:match.start()].count('\n') + 1
            rel_path = os.path.relpath(file_path, base_dir)
            items.append({
                'value': attr_value,
                'file': rel_path,
                'line': line_num,
            })
    return items
```

### find_duplicate_groups(items)

检测重复值，每个重复组只保留第一次出现。

```python
from collections import defaultdict

def find_duplicate_groups(items):
    value_to_occurrences = defaultdict(list)
    for item in items:
        value_to_occurrences[item['value']].append(item)

    duplicates = []
    for value, occurrences in value_to_occurrences.items():
        if len(occurrences) > 1:
            first = occurrences[0]
            other_locs = [
                f"{occ['file']}:{occ['line']}"
                for occ in occurrences[1:]
            ]
            duplicates.append({
                'value': value,
                'count': len(occurrences),
                'first_file': first['file'],
                'first_line': first['line'],
                'other_locations': other_locs,
            })
    return duplicates
```

## 使用规则

| 规则 | 检测目标 | 正则 | 收集文件范围 |
|------|---------|------|------------|
| R019 | `.key('xxx')` | `\.key\s*\(\s*(["\'])([^"\']+)\1\s*\)` | 递归所有源代码 |
| R020 | `.id('xxx')` | `\.id\s*\(\s*(["\'])([^"\']+)\1\s*\)` | 递归所有源代码 |
| R011 | `describe('xxx')` | `describe\s*\(\s*([\'"])([^\'"]+)\1` | 仅根目录测试文件 |

## 关键陷阱

### group类型父BUILD.gn的子工程被错误过滤

- **严重性**: 极严重，导致arkui子系统49→997个工程漏检
- **问题**: 过滤`parent_dirs`时未区分group和非group父BUILD.gn
- **修复**: 只将"父目录是非group BUILD.gn"的子目录标记为应排除
- **影响**: R011, R019, R020
