# R007: Test.json禁止配置项

## 规则信息

| 属性 | 值 |
|------|------|
| 规则编号 | R007 |
| 问题类型 | Test.json禁止配置项 |
| 严重级别 | Critical |
| 规则复杂度 | simple |

## 问题描述

Test.json配置文件中存在禁止的配置项：
- `setenforce 0` — 会关闭SELinux，引入安全问题
- `rerun: true` — 会导致测试报告出现异常
- `appfreeze.filter_bundle_name` — 会屏蔽appfreeze异常

**规范来源**:
- 用例低级问题.md 第9条 — "禁止配置setenforce 0，会关闭selinux引入问题"
- 用例低级问题.md 第10条 — "禁止配置rerun:true，会导致报告出现异常"
- 用例低级问题.md 第11条 — "禁止配置appfreeze.filter_bundle_name，会屏蔽appfreeze异常"

## 扫描范围

| 应扫描 | 文件名 |
|--------|--------|
| **Test.json文件** | 所有名为 `Test.json` 的文件（不区分大小写） |

R007只扫描Test.json配置文件，不扫描源代码文件。

## 检测逻辑

### 步骤1: 定位Test.json文件

```python
import os
import re

def get_r007_scan_files(directory: str) -> list[str]:
    test_json_files = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower() == 'test.json':
                test_json_files.append(os.path.join(root, f))
    return test_json_files
```

### 步骤2: 逐行检测禁止配置项

```python
def check_r007(file_path: str) -> list[dict]:
    issues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # 检测1: setenforce 0（不检测 setenforce 1）
        if 'setenforce 0' in stripped:
            issues.append({
                'rule': 'R007',
                'type': 'Test.json禁止配置项',
                'severity': 'Critical',
                'file': file_path,
                'line': i,
                'testcase': '-',
                'snippet': stripped,
                'suggestion': (
                    f'路径: {file_path}, 行号: {i}, '
                    f'问题描述: 禁止配置setenforce 0，会关闭SELinux引入安全问题。请移除该配置。'
                ),
                'detail': 'setenforce 0'
            })
            continue

        # 检测2: rerun 配置
        # 匹配 "rerun": true, "rerun":"true", "rerun":"ture", "rerun": 1 等
        if re.search(r'"rerun"\s*:\s*(true|1|"true"|"ture")', stripped, re.IGNORECASE):
            issues.append({
                'rule': 'R007',
                'type': 'Test.json禁止配置项',
                'severity': 'Critical',
                'file': file_path,
                'line': i,
                'testcase': '-',
                'snippet': stripped,
                'suggestion': (
                    f'路径: {file_path}, 行号: {i}, '
                    f'问题描述: 禁止配置rerun:true，会导致测试报告出现异常。请移除该配置。'
                ),
                'detail': 'rerun'
            })
            continue

        # 检测3: appfreeze.filter_bundle_name
        if 'appfreeze.filter_bundle_name' in stripped:
            issues.append({
                'rule': 'R007',
                'type': 'Test.json禁止配置项',
                'severity': 'Critical',
                'file': file_path,
                'line': i,
                'testcase': '-',
                'snippet': stripped,
                'suggestion': (
                    f'路径: {file_path}, 行号: {i}, '
                    f'问题描述: 禁止配置appfreeze.filter_bundle_name，会屏蔽appfreeze异常。请移除该配置。'
                ),
                'detail': 'appfreeze.filter_bundle_name'
            })

    return issues
```

### 检测要点

1. **setenforce 0**: 只检测 `setenforce 0`，不检测 `setenforce 1`（setenforce 1是允许的）
2. **rerun**: 检测 `"rerun": true`、`"rerun": 1`、`"rerun": "true"`、`"rerun": "ture"`（注意常见拼写错误）
3. **appfreeze.filter_bundle_name**: 检测完整字段名，无论值是什么
4. **行号**: 必须准确报告问题所在行号
5. **testcase字段**: 固定为 `-`（配置文件，无对应用例）

## 输出格式

| 列名 | 说明 |
|------|------|
| 问题ID | R007 |
| 问题类型 | Test.json禁止配置项 |
| 严重级别 | Critical |
| 文件路径 | 相对路径 |
| 行号 | 问题所在行号 |
| 所属用例 | `-`（配置文件） |
| 代码片段 | 匹配到的代码行 |
| 修复建议 | 路径+行号+问题描述 |

## 错误示例

```json
// 错误1: 配置setenforce 0
{
  "kits": [
    {
      "type": "ShellKit",
      "run-command": [
        "setenforce 0",
        "hilog -Q pidoff"
      ]
    }
  ]
}
```

```json
// 错误2: 配置rerun
{
  "driver": {
    "type": "OHJSUnitTest",
    "rerun": true
  }
}
```

```json
// 错误3: 配置appfreeze.filter_bundle_name
{
  "kits": [
    {
      "type": "ShellKit",
      "run-command": [
        "param set hiviewdfx.appfreeze.filter_bundle_name com.example.myapplication"
      ]
    }
  ]
}
```

## 正确示例

```json
// 正确: 不配置setenforce 0、rerun、appfreeze.filter_bundle_name
{
  "kits": [
    {
      "type": "ShellKit",
      "run-command": [
        "setenforce 1",
        "hilog -Q pidoff"
      ]
    }
  ],
  "driver": {
    "type": "OHJSUnitTest"
  }
}
```

## 扫描命令参考

```bash
# 扫描setenforce 0
grep -rn 'setenforce 0' --include='Test.json' /path/to/code

# 扫描rerun
grep -rn '"rerun"' --include='Test.json' /path/to/code

# 扫描appfreeze
grep -rn 'appfreeze.filter_bundle_name' --include='Test.json' /path/to/code
```

## 注意事项

1. 文件名匹配不区分大小写（`Test.json`、`test.json`、`TEST.JSON` 均匹配）
2. 同一行中可能存在多个违规配置，每个违规配置分别报告
3. `setenforce 1` 是允许的，不应报告
4. `rerun: false` 或 `rerun: 0` 不视为违规
5. testcase字段始终为 `-`，因为Test.json是配置文件
