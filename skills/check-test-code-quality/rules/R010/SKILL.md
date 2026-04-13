# R010: BUILD.gn配置错误

## 规则信息

| 属性 | 值 |
|------|-----|
| 规则编号 | R010 |
| 问题类型 | BUILD.gn配置错误 |
| 严重级别 | Critical |
| 规则复杂度 | complex |
| 扫描范围 | BUILD.gn files only |
| testcase字段 | `-`（BUILD.gn为非测试文件，无对应it()块） |

## 问题描述

`part_name`/`subsystem_name`不匹配。BUILD.gn中声明的`part_name`必须在对应`subsystem_name`的components列表中存在。

## 修复建议

使用完整的子系统-组件映射表，确保`part_name`在对应`subsystem`的components中。

## 映射表数据源

映射表从以下三个配置文件构建：

1. `vendor/hihope/rk3568/config.json`
2. `productdefine/common/inherit/rich.json`
3. `productdefine/common/inherit/chipset_common.json`

## 扫描逻辑

### Step 1: 收集文件

扫描目标目录下所有名为`BUILD.gn`的文件。

```python
import os

def find_build_gn_files(scan_root):
    build_gn_files = []
    for dirpath, dirnames, filenames in os.walk(scan_root):
        if 'BUILD.gn' in filenames:
            build_gn_files.append(os.path.join(dirpath, 'BUILD.gn'))
    return build_gn_files
```

### Step 2: 解析BUILD.gn提取part_name和subsystem_name

对每个BUILD.gn文件，使用正则表达式提取`part_name`和`subsystem_name`字段。

```python
import re

def extract_build_gn_fields(content):
    part_name = None
    subsystem_name = None

    part_match = re.search(r'part_name\s*=\s*["\']([^"\']+)["\']', content)
    if part_match:
        part_name = part_match.group(1)

    subsystem_match = re.search(r'subsystem_name\s*=\s*["\']([^"\']+)["\']', content)
    if subsystem_match:
        subsystem_name = subsystem_match.group(1)

    return part_name, subsystem_name
```

### Step 3: 构建子系统-组件映射表

从三个配置文件中读取并合并映射关系。每个配置文件的结构包含子系统定义，每个子系统下有components列表。

```python
import json

def load_subsystem_mapping(config_roots):
    subsystem_map = {}

    config_files = [
        'vendor/hihope/rk3568/config.json',
        'productdefine/common/inherit/rich.json',
        'productdefine/common/inherit/chipset_common.json',
    ]

    for config_file in config_files:
        for root in config_roots:
            full_path = os.path.join(root, config_file)
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                _parse_config(data, subsystem_map)
                break

    return subsystem_map

def _parse_config(data, subsystem_map):
    subsystems = data.get('subsystems', [])
    for subsys in subsystems:
        name = subsys.get('subsystem', '')
        components = subsys.get('components', [])
        if name not in subsystem_map:
            subsystem_map[name] = set()
        subsystem_map[name].update(components)
```

### Step 4: 验证匹配关系

对每个BUILD.gn，检查提取出的`part_name`是否在`subsystem_name`对应的components集合中。

```python
def validate_part_subsystem(part_name, subsystem_name, subsystem_map):
    if not part_name or not subsystem_name:
        return True

    if subsystem_name not in subsystem_map:
        return True

    return part_name in subsystem_map[subsystem_name]
```

### Step 5: 生成问题报告

```python
def scan_r010(scan_root, config_roots, base_dir):
    issues = []
    subsystem_map = load_subsystem_mapping(config_roots)
    build_gn_files = find_build_gn_files(scan_root)

    for file_path in build_gn_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        part_name, subsystem_name = extract_build_gn_fields(content)

        if not part_name or not subsystem_name:
            continue

        if not validate_part_subsystem(part_name, subsystem_name, subsystem_map):
            rel_path = os.path.relpath(file_path, base_dir)

            part_line = 0
            for i, line in enumerate(content.splitlines(), 1):
                if re.search(r'part_name\s*=\s*["\']' + re.escape(part_name) + '["\']', line):
                    part_line = i
                    break

            available_parts = sorted(subsystem_map.get(subsystem_name, set()))

            issues.append({
                'rule': 'R010',
                'type': 'BUILD.gn配置错误',
                'severity': 'Critical',
                'file': rel_path,
                'line': part_line,
                'testcase': '-',
                'snippet': f'part_name = "{part_name}", subsystem_name = "{subsystem_name}"',
                'suggestion': (
                    f'part_name "{part_name}" 不在 subsystem_name "{subsystem_name}" 的components中。'
                    f'可选的part_name: {available_parts}'
                ),
            })

    return issues
```

## 错误示例

```python
# BUILD.gn - 错误：invalid_part不在arkui的components中
ohos_js_app_suite("ActsTest") {
  testonly = true
  part_name = "invalid_part"       # ✗ 错误
  subsystem_name = "arkui"
  hap_name = "ActsTest"
}
```

## 正确示例

```python
# BUILD.gn - 正确：ace_engine在arkui的components中
ohos_js_app_suite("test") {
  testonly = true
  part_name = "ace_engine"         # ✓ 正确
  subsystem_name = "arkui"
  hap_name = "ActsTest"
}
```

## 注意事项

1. 如果`subsystem_name`本身不在映射表中，跳过验证（可能是新增子系统）
2. 映射表需从三个配置文件合并，任何一个文件中出现的映射关系都有效
3. BUILD.gn文件中可能存在多个target，每个target都需要检查
4. 不检查group类型的BUILD.gn（group类型通常不包含part_name/subsystem_name）
5. 如果BUILD.gn文件中缺少part_name或subsystem_name字段，跳过该文件

## 输出格式

每条issue的字段：

| 字段 | 值 |
|------|-----|
| rule | `R010` |
| type | `BUILD.gn配置错误` |
| severity | `Critical` |
| file | 相对路径（如`ability/xxx/BUILD.gn`） |
| line | part_name所在行号 |
| testcase | `-` |
| snippet | `part_name = "xxx", subsystem_name = "yyy"` |
| suggestion | 问题描述 + 可选的part_name列表 |

## 技术挑战与解决方案

### 维护完整的子系统-组件映射表

**挑战**: 维护完整的子系统-组件映射表

**解决方案**:
```python
SUBSYSTEM_PARTS_MAP = {
    "account": ["os_account"],
    "arkui": ["ace_engine", "napi", "ui_appearance", "ui_lite"],
    "bundle": ["bundle_framework"],
    "communication": ["bluetooth", "wifi", "netstack", "dsoftbus"],
    # ... 共50+个子系统
}
```
