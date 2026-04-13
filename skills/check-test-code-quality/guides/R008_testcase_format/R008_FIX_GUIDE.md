# R008 用例声明格式不规范 - 修复指南

## 问题描述

测试用例的文档注释（`/** ... */`）中，`@tc.xxx` 参数声明格式不规范。规范要求参数名与值之间使用空格分隔，且文档注释格式应遵循统一规范。

### 问题分类

| 问题类型 | 示例 | 修复方式 |
|---------|------|---------|
| @tc.xxx使用冒号分隔符 | `* @tc.level:    Level 1` | 冒号替换为空格 |
| 文档注释结束行与测试用例间有空行 | `*/` 后跟空行再跟 `it()` | 删除多余空行 |
| 注释行未以*开始 | `/***有问题***/` | 需人工修复 |

### 规范格式

```typescript
/**
 * @tc.number    ConvertPointTest_0010
 * @tc.name      convertPointTest
 * @tc.desc      api axisPinch
 * @tc.level     Level 1
 * @tc.type      Function
 * @tc.size      MediumTest
 */
it('convertPointTest', Level.LEVEL1, async (done: Function) => {
```

**要点**：
- `@tc.xxx` 与值之间用**空格**分隔，不用冒号
- `*/` 与 `it()` 之间不留空行
- 注释行以 ` * ` 开始

## 自动修复

### 可自动修复的类型

1. **@tc.xxx 冒号分隔符 → 空格**（1014个，占83.5%）
2. **文档注释后多余空行删除**（16个，占1.3%）

### 无法自动修复的类型

- `/***有问题***/` — 注释内容需根据语义修改
- `levelUniqueId: Normal value"` — 代码逻辑相关
- 其他非@tc.xxx格式问题

### 自动修复脚本

```python
import csv
import re
import os


def fix_r008_from_csv(csv_path, code_root):
    fix_stats = {
        'tc.level_colon': 0,
        'tc.type_colon': 0,
        'tc.size_colon': 0,
        'tc.number_colon': 0,
        'tc.name_colon': 0,
        'tc.desc_colon': 0,
        'blank_line': 0,
        'skipped': 0,
    }

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        rid_idx = header.index('问题ID')
        file_idx = header.index('文件路径')
        line_idx = header.index('行号')
        sug_idx = header.index('修复建议')
        issues = [row for row in reader if row[rid_idx] == 'R008']

    file_issues = {}
    for row in issues:
        filepath = os.path.join(code_root, row[file_idx])
        if not os.path.isfile(filepath):
            fix_stats['skipped'] += 1
            continue
        file_issues.setdefault(filepath, []).append({
            'line': int(row[line_idx]),
            'suggestion': row[sug_idx],
        })

    tc_params = ['level', 'type', 'size', 'number', 'name', 'desc']
    colon_patterns = {
        p: re.compile(rf'(\*\s*@tc\.{p}\s*):\s+')
        for p in tc_params
    }

    for filepath, issues_list in file_issues.items():
        issues_list.sort(key=lambda x: x['line'], reverse=True)
        for issue in issues_list:
            line_num = issue['line']
            suggestion = issue['suggestion']

            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if line_num < 1 or line_num > len(lines):
                fix_stats['skipped'] += 1
                continue

            fixed = False
            if '冒号' in suggestion:
                for param, pattern in colon_patterns.items():
                    if f'tc.{param}' in suggestion:
                        old_line = lines[line_num - 1]
                        new_line = pattern.sub(r'\1 ', old_line)
                        if new_line != old_line:
                            lines[line_num - 1] = new_line
                            fix_stats[f'tc.{param}_colon'] += 1
                            fixed = True
                        break
            elif '空行' in suggestion:
                if line_num < len(lines) and lines[line_num].strip() == '':
                    del lines[line_num]
                    fix_stats['blank_line'] += 1
                    fixed = True

            if not fixed:
                fix_stats['skipped'] += 1
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)

    return fix_stats


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python fix_r008.py <csv_path> <code_root>")
        sys.exit(1)
    stats = fix_r008_from_csv(sys.argv[1], sys.argv[2])
    total = sum(v for k, v in stats.items() if k != 'skipped' and v > 0)
    print(f"修复完成: 合计 {total}, 跳过 {stats['skipped']}")
    for k, v in stats.items():
        if v > 0:
            print(f"  {k}: {v}")
```

### 使用方法

```bash
# 从CSV报告修复R008问题
python3 fix_r008.py /path/to/report.csv /path/to/code_root
```

## 修复统计（arkui子系统实测）

| 修复类型 | 修复数量 |
|---------|---------|
| @tc.level 冒号→空格 | 683 |
| @tc.type 冒号→空格 | 136 |
| @tc.size 冒号→空格 | 134 |
| @tc.number 冒号→空格 | 22 |
| @tc.name 冒号→空格 | 16 |
| @tc.desc 冒号→空格 | 23 |
| 文档注释后空行删除 | 16 |
| **合计修复** | **1030** |
| 跳过（需人工处理） | 185 |

**修复率**: 1030/1215 = 84.8%

## 技术要点

### 要点1: CSV路径拼接陷阱

CSV中文件路径是相对于扫描根目录的（如 `arkui/xxx/test.ets`），拼接时需注意扫描根目录的选择：

```python
# 错误：CSV路径以"arkui/"开头，SCAN_ROOT已经包含"arkui"，会导致双拼
SCAN_ROOT = '/home/xxx/acts/arkui'
# os.path.join(SCAN_ROOT, 'arkui/xxx/test.ets') = '/home/xxx/acts/arkui/arkui/xxx/test.ets' ← 双arkui

# 正确：SCAN_ROOT指向acts目录，CSV的arkui/前缀正好匹配
SCAN_ROOT = '/home/xxx/acts'
# os.path.join(SCAN_ROOT, 'arkui/xxx/test.ets') = '/home/xxx/acts/arkui/xxx/test.ets' ← 正确
```

### 要点2: 逆序修复避免行号偏移

删除空行会导致后续行号整体上移。修复时**必须按行号从大到小排序**处理同一文件的问题：

```python
issues_list.sort(key=lambda x: x['line'], reverse=True)
```

这样先处理文件末尾的问题，删除空行不影响前面问题的行号。

### 要点3: 冒号分隔符正则匹配

`@tc.level:` 的冒号前可能有多个空格，冒号后也可能有多个空格：

```python
# 修复前:     * @tc.level:    Level 1
# 修复后:     * @tc.level Level 1

pattern = re.compile(r'(\*\s*@tc\.level\s*):\s+')
new_line = pattern.sub(r'\1 ', line)
```

正则说明：
- `(\*\s*@tc\.level\s*)` — 捕获组：`*` + 空格 + `@tc.level` + 可选空格
- `:` — 匹配冒号
- `\s+` — 匹配冒号后的一个或多个空格
- 替换为 `\1 ` — 捕获组内容 + 一个空格

### 要点4: CSV中逗号干扰字段解析

代码片段和修复建议字段可能包含逗号，导致CSV字段错位。应使用`csv.reader`而非手动分割：

```python
# 正确：csv.reader自动处理引号内的逗号
reader = csv.reader(f)
header = next(reader)
file_idx = header.index('文件路径')

# 错误：手动split会被逗号干扰
row = line.split(',')  # snippet中的逗号会导致字段偏移
```

### 要点5: 同一文件多个问题的处理策略

一个文件可能有多处R008问题。优化策略：

1. **按文件分组**：减少文件IO次数
2. **同一文件内逆序处理**：避免行号偏移
3. **每次修复后立即写回**：确保后续读取最新内容

```python
for filepath, issues_list in file_issues.items():
    issues_list.sort(key=lambda x: x['line'], reverse=True)
    for issue in issues_list:
        # 读取 -> 修复 -> 写回（每次都读写完整文件）
        with open(filepath, 'r') as f:
            lines = f.readlines()
        # ... fix ...
        with open(filepath, 'w') as f:
            f.writelines(lines)
```

**注意**: 每次都重新读取文件是因为同一文件可能有多种修复类型（冒号+空行），需要确保行号准确。
