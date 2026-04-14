# R017: syscap.json配置多个能力

- **规则编号**: R017
- **严重级别**: Critical
- **规则复杂度**: complex（需要JSON解析）
- **问题类型**: 一个XTS工程的syscap.json文件中配置了多个syscap能力
- **修复方式**: 仅配置一个syscap能力
- **预期问题数量**: 3000+

## 扫描范围

仅扫描`syscap.json`文件。

**文件定位规则**：在每个XTS工程目录下查找`syscap.json`文件（通常位于工程根目录或`src`目录下）。

## 问题描述

一个XTS工程的`syscap.json`文件中配置了多个syscap能力。根据规范，每个XTS工程应仅配置一个syscap能力，即被测API对应的能力。

## 检测逻辑

### 核心算法

```python
import json
import os
import re

def find_syscap_files(directory: str) -> list:
    """
    在目录下递归查找所有syscap.json文件。

    Args:
        directory: 扫描根目录

    Returns:
        syscap.json文件绝对路径列表
    """
    syscap_files = []
    for root, dirs, files in os.walk(directory):
        if 'syscap.json' in files:
            syscap_files.append(os.path.join(root, 'syscap.json'))
    return syscap_files


def scan_r017(file_path: str) -> list:
    """
    检查syscap.json文件是否配置了多个syscap能力。

    Args:
        file_path: syscap.json文件路径

    Returns:
        问题列表
    """
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return [{
            'rule': 'R017',
            'type': 'syscap.json配置多个能力',
            'severity': 'Critical',
            'file': file_path,
            'line': 1,
            'testcase': '-',
            'snippet': f'syscap.json解析失败: {e}',
            'suggestion': f'路径: {file_path}, 行号: 1, 问题描述: syscap.json文件格式错误，无法解析。',
        }]

    # 检查devices.custom[].xts数组
    devices = data.get('devices', {})
    custom_devices = devices.get('custom', [])

    for device_idx, device in enumerate(custom_devices):
        xts_list = device.get('xts', [])

        if len(xts_list) > 1:
            # 在文件中定位xts数组所在行
            line_num = find_xts_array_line(file_path, data)

            snippet = ', '.join(xts_list[:3])
            if len(xts_list) > 3:
                snippet += f', ... (共{len(xts_list)}个)'

            issues.append({
                'rule': 'R017',
                'type': 'syscap.json配置多个能力',
                'severity': 'Critical',
                'file': file_path,
                'line': line_num,
                'testcase': '-',
                'snippet': snippet,
                'suggestion': (
                    f"路径: {file_path}, 行号: {line_num}, "
                    f"问题描述: 配置了{len(xts_list)}个syscap能力，应仅配置1个。"
                    f"请保留被测API对应的能力，移除其余能力。"
                ),
            })

    return issues


def find_xts_array_line(file_path: str, data: dict) -> int:
    """
    在syscap.json文件中定位xts数组所在的行号。

    Args:
        file_path: 文件路径
        data: 已解析的JSON数据

    Returns:
        xts数组第一个元素所在行号，找不到返回1
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        xts_list = data.get('devices', {}).get('custom', [{}])[0].get('xts', [])
        if xts_list:
            first_cap = xts_list[0]
            for i, line in enumerate(lines, 1):
                if first_cap in line:
                    return i
    except Exception:
        pass

    return 1
```

### 批量扫描入口

```python
def batch_scan_r017(directory: str) -> list:
    """
    扫描目录下所有syscap.json文件。

    Args:
        directory: 扫描根目录

    Returns:
        所有问题列表
    """
    all_issues = []
    syscap_files = find_syscap_files(directory)

    for file_path in syscap_files:
        rel_path = os.path.relpath(file_path, directory)
        issues = scan_r017(rel_path)
        all_issues.extend(issues)

    return all_issues
```

## syscap.json文件结构

### 标准格式

```json
{
  "devices": {
    "general": [],
    "custom": [
      {
        "xts": [
          "SystemCapability.Ability.AbilityRuntime.Core"
        ]
      }
    ]
  }
}
```

### 关键路径（含类型约束）

**必须严格按层级类型取值，不可跳层或混淆层级类型。**

| JSON路径 | 类型 | 说明 |
|---------|------|------|
| `data.devices` | **dict** `{str: ...}` | 设备配置根节点，包含 `"general"` 和 `"custom"` 两个key |
| `data.devices.custom` | **list** `[dict, ...]` | 自定义设备配置数组，每个元素是一个dict |
| `data.devices.custom[].xts` | **list** `[str, ...]` | XTS syscap能力字符串数组（**检测目标**） |

**正确取值方式**（两步，不可合并为一步）：
```python
# 第1步：从dict中取出custom列表
devices = data.get('devices', {})       # → dict {"general": [], "custom": [...]}
custom_devices = devices.get('custom', [])  # → list [dict, ...]

# 第2步：遍历列表中的每个dict
for device in custom_devices:           # device → dict {"xts": [...]}
    xts_list = device.get('xts', [])    # → list [str, ...]
```

**常见错误**（会导致100%漏检）：
```python
# ✗ 错误：把devices dict直接当列表遍历，遍历的是key字符串
for dev in data.get('devices', []):     # dev是"general"或"custom"字符串
    dev.get('custom')                   # → AttributeError: 'str' has no 'get'

# ✗ 错误：合并取值后类型丢失
custom = data.get('devices', {}).get('custom', [])  # 正确
for dev in custom:
    xts = dev.get('xts', [])            # dev必须是dict，如果custom被错误赋值为list of list则会报错
```

## 错误示例

```json
// 错误：配置了多个能力
{
  "devices": {
    "general": [],
    "custom": [
      {
        "xts": [
          "SystemCapability.Ability.AbilityRuntime.Core",
          "SystemCapability.Ability.AbilityRuntime.FAModel",
          "SystemCapability.Ability.AbilityRuntime.AbilityCore"
        ]
      }
    ]
  }
}
// ✗ 错误：配置了3个syscap能力，应仅配置1个
```

```json
// 错误：配置了2个能力
{
  "devices": {
    "general": [],
    "custom": [
      {
        "xts": [
          "SystemCapability.Account.OsAccount",
          "SystemCapability.Account.AppAccount"
        ]
      }
    ]
  }
}
// ✗ 错误：配置了2个syscap能力，应仅配置1个
```

## 正确示例

```json
// 正确：仅配置一个能力
{
  "devices": {
    "general": [],
    "custom": [
      {
        "xts": [
          "SystemCapability.Ability.AbilityRuntime.Core"
        ]
      }
    ]
  }
}
// ✓ 正确：仅配置了1个syscap能力
```

```json
// 正确：仅配置一个能力
{
  "devices": {
    "general": [],
    "custom": [
      {
        "xts": [
          "SystemCapability.Web.Webview"
        ]
      }
    ]
  }
}
// ✓ 正确：仅配置了1个syscap能力
```

## 输出格式

### 问题数据结构

```python
{
    'rule': 'R017',
    'type': 'syscap.json配置多个能力',
    'severity': 'Critical',
    'file': 'ability/AccessManager/entry/syscap.json',
    'line': 5,
    'testcase': '-',
    'snippet': 'SystemCapability.Ability.AbilityRuntime.Core, SystemCapability.Ability.AbilityRuntime.FAModel, SystemCapability.Ability.AbilityRuntime.AbilityCore',
    'suggestion': '路径: ability/AccessManager/entry/syscap.json, 行号: 5, 问题描述: 配置了3个syscap能力，应仅配置1个。请保留被测API对应的能力，移除其余能力。'
}
```

### Excel报告列

| 列序 | 列名 | 示例 |
|------|------|------|
| 1 | 问题ID | R017 |
| 2 | 问题类型 | syscap.json配置多个能力 |
| 3 | 严重级别 | Critical |
| 4 | 文件路径 | ability/AccessManager/entry/syscap.json |
| 5 | 行号 | 5 |
| 6 | 所属用例 | `-` |
| 7 | 代码片段 | `SystemCapability.Ability.AbilityRuntime.Core, ...` |
| 8 | 修复建议 | 路径: ..., 行号: 5, 问题描述: 配置了3个syscap能力，应仅配置1个... |

**注意**：`所属用例`字段始终为`-`，因为syscap.json不是测试文件，不存在testcase概念。

## 修复建议

1. 确认被测API对应的syscap能力
2. 在`xts`数组中仅保留该能力
3. 移除其余所有能力配置

```json
// 修复前
{
  "devices": {
    "custom": [
      {
        "xts": [
          "SystemCapability.Ability.AbilityRuntime.Core",
          "SystemCapability.Ability.AbilityRuntime.FAModel",
          "SystemCapability.Ability.AbilityRuntime.AbilityCore"
        ]
      }
    ]
  }
}

// 修复后（假设被测API属于Core能力）
{
  "devices": {
    "custom": [
      {
        "xts": [
          "SystemCapability.Ability.AbilityRuntime.Core"
        ]
      }
    ]
  }
}
```

## 边界情况

### 1. xts数组为空

`xts`数组为空（`[]`）时不报告，因为0个能力不违反"应仅配置1个"的规则。但实际使用中这种情况极少。

### 2. custom数组为空

`custom`数组为空时不报告。

### 3. 缺少devices节点

如果`syscap.json`文件缺少`devices`节点，JSON解析不会报错但不会产生问题报告。可根据实际需要决定是否将缺少`devices`节点作为额外问题报告。

### 4. JSON解析失败

如果`syscap.json`文件格式错误（非有效JSON），解析会抛出异常，此时报告为解析错误，便于用户定位和修复。

### 5. devices层级类型混淆（已知陷阱）

`data['devices']` 是 **dict**（包含 `"general"` 和 `"custom"` 两个key），不是设备列表。必须通过 `.get('custom', [])` 再取一层才能得到设备列表。如果直接遍历 `data['devices']`，遍历的是dict的key字符串（`"general"`、`"custom"`），对字符串调用 `.get()` 会导致 `AttributeError`，异常被静默捕获后所有文件全部跳过，造成100%漏检。

**验证方法**：实现完成后，用以下命令快速验证是否漏检：
```bash
grep -r '"SystemCapability' --include='syscap.json' -l | xargs grep -c '"SystemCapability' | grep -v ':1$' | wc -l
```
如果该命令输出的数量远大于扫描结果数量，说明存在漏检。

## 错误/正确示例

> 来源: EXAMPLES.md

以下为补充示例（与上方已有示例互补）：

**错误示例**：
```json
// 错误：配置多个能力
{
  "devices": {
    "general": [],
    "custom": [
      {
        "xts": [
          "SystemCapability.Ability.AbilityRuntime.Core",
          "SystemCapability.Ability.AbilityRuntime.FAModel",
          "SystemCapability.Ability.AbilityRuntime.AbilityCore"
        ]
      }
    ]
  }
}
```

**正确示例**：
```json
// 正确：仅配置一个能力
{
  "devices": {
    "general": [],
    "custom": [
      {
        "xts": [
          "SystemCapability.Ability.AbilityRuntime.Core"
        ]
      }
    ]
  }
}
```

## 实现细节

> 来源: IMPLEMENTATION_DETAILS.md

**检测范围**: syscap.json文件

**检测方法**: 检查 `devices.custom[].xts` 数组，如果长度大于1则报错

```python
def check_syscap_json(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for device in data['devices']['custom']:
        xts_list = device.get('xts', [])
        if len(xts_list) > 1:
            report_issue(f"配置了{len(xts_list)}个syscap能力，应仅配置1个")
```

## 技术挑战与解决方案

> 来源: V3_UPGRADE_GUIDE.md

- **预期问题数量**: 3025个
- **实现方式**: JSON解析 + 能力数量统计
- **检查字段**: os_account, system_capability
