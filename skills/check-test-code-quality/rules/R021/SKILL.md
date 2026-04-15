# R021: hypium版本号>=1.0.26

## 规则信息

| 属性 | 值 |
|------|-----|
| 规则编号 | R021 |
| 问题类型 | hypium版本号不满足要求 |
| 严重级别 | Critical |
| 规则复杂度 | simple |
| 扫描范围 | 独立XTS工程根目录下的 `oh-package.json5` |
| testcase字段 | `-`（配置文件，不在it()块内） |

## 问题描述

一个独立XTS工程的 `oh-package.json5` 文件中，`devDependencies` 下的 `"@ohos/hypium"` 字段值必须 >= `1.0.26`。

## 修复建议

将 `"@ohos/hypium"` 的版本号升级到 `1.0.26` 或以上。

## 修复建议格式

```
路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名称}' 中，oh-package.json5的devDependencies.@ohos/hypium版本号为 '{当前版本}'，低于最低要求版本 1.0.26。
```

## 扫描逻辑

### Step 1: 识别独立XTS工程

复用R011的独立XTS工程识别逻辑（必须使用修正后的版本，正确处理group类型父BUILD.gn，见R019陷阱6）。

### Step 2: 定位oh-package.json5

在每个独立XTS工程的根目录下查找 `oh-package.json5` 文件。**注意**：
- 只检查工程根目录下的 `oh-package.json5`，不检查 `entry/oh-package.json5` 或 `cpp/*/oh-package.json5` 等子目录文件
- 如果根目录下没有 `oh-package.json5`，跳过该工程

### Step 3: 提取hypium版本号

在 `oh-package.json5` 文件中，提取 `devDependencies` 下 `"@ohos/hypium"` 的版本号字符串。

**关键**: 必须跳过注释行。`oh-package.json5` 支持 `//` 单行注释，注释掉的依赖不参与检查。

```python
import re
import os

HYPIMUM_PATTERN = re.compile(
    r'"@ohos/hypium"\s*:\s*"([^"]+)"'
)

def parse_version(version_str):
    parts = version_str.strip().split('.')
    result = []
    for p in parts:
        m = re.match(r'(\d+)', p)
        result.append(int(m.group(1)) if m else 0)
    while len(result) < 3:
        result.append(0)
    return tuple(result)

def scan_r021(scan_root, base_dir):
    MIN_VERSION = (1, 0, 26)
    issues = []
    projects = find_independent_projects(scan_root)

    for project_dir in projects:
        pkg_path = os.path.join(project_dir, 'oh-package.json5')
        if not os.path.isfile(pkg_path):
            continue

        with open(pkg_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_idx, line in enumerate(lines):
            stripped = line.strip()

            # 跳过注释行（// 开头或全行被注释）
            if stripped.startswith('//'):
                continue
            # 跳过 @ohos/hypium 被注释的情况
            # 例如: //    "@ohos/hypium": "1.0.21",
            code_part = stripped
            if '//' in stripped:
                # 取 // 之前的部分
                code_part = stripped[:stripped.index('//')].strip()

            match = HYPIMUM_PATTERN.search(code_part)
            if not match:
                continue

            version_str = match.group(1)
            version = parse_version(version_str)

            if version < MIN_VERSION:
                rel_path = os.path.relpath(pkg_path, base_dir)
                rel_project = os.path.relpath(project_dir, base_dir)
                line_num = line_idx + 1

                issues.append({
                    'rule': 'R021',
                    'type': 'hypium版本号不满足要求',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': line_num,
                    'testcase': '-',
                    'snippet': f'"@ohos/hypium": "{version_str}"',
                    'suggestion': (
                        f"路径: {rel_path}, 行号: {line_num}, "
                        f"问题描述: 在独立XTS工程 '{rel_project}' 中，"
                        f"oh-package.json5的devDependencies.@ohos/hypium版本号为 "
                        f"'{version_str}'，低于最低要求版本 1.0.26。"
                    ),
                })

    return issues
```

## 错误示例

```json5
{
  "modelVersion": "6.0.0",
  "description": "Please describe the basic information.",
  "dependencies": {
  },
  "devDependencies": {
    "@ohos/hypium": "1.0.25"   // ✗ 错误：版本低于 1.0.26
  }
}
```

```json5
{
  "devDependencies": {
    "@ohos/hypium": "1.0.6"    // ✗ 错误：版本低于 1.0.26
  }
}
```

## 正确示例

```json5
{
  "modelVersion": "6.0.0",
  "description": "Please describe the basic information.",
  "dependencies": {
  },
  "devDependencies": {
    "@ohos/hypium": "1.0.26"   // ✓ 版本号满足最低要求
  }
}
```

```json5
{
  "devDependencies": {
    "@ohos/hypium": "1.0.27"   // ✓ 版本号满足最低要求
  }
}
```

## 陷阱与注意事项

### 陷阱1: 必须跳过注释行

`oh-package.json5` 支持 `//` 单行注释。被注释掉的 `@ohos/hypium` 条目不参与检查。

```json5
"devDependencies": {
//    "@ohos/hypium": "1.0.21",   // ← 被注释掉，不检查
}
```

如果不过滤注释行，会将注释中的旧版本号误报为问题。

**判断方法**: 行去除首尾空白后以 `//` 开头，或行内 `//` 之前的部分不含 `@ohos/hypium`。

### 陷阱2: 只检查工程根目录的oh-package.json5

独立XTS工程下可能存在多个 `oh-package.json5` 文件：
- `{工程根目录}/oh-package.json5` ← **只检查这个**
- `{工程根目录}/entry/oh-package.json5` ← 不检查
- `{工程根目录}/entry/src/main/cpp/types/libxxx/oh-package.json5` ← 不检查

### 陷阱3: 版本号格式可能不标准

大部分工程的版本号为标准semver格式（如 `1.0.26`），但可能存在非标准格式。解析时只取数字部分进行比较：

```python
def parse_version(version_str):
    parts = version_str.strip().split('.')
    result = []
    for p in parts:
        m = re.match(r'(\d+)', p)
        result.append(int(m.group(1)) if m else 0)
    while len(result) < 3:
        result.append(0)
    return tuple(result)
```

### 陷阱4: devDependencies可能不存在

部分工程的 `oh-package.json5` 中可能没有 `devDependencies` 字段，或者 `devDependencies` 下没有 `"@ohos/hypium"` 条目。这种情况下不报错（规则只检查存在的hypium版本号是否满足要求）。

## 输出格式

每条issue的字段：

| 字段 | 值 |
|------|-----|
| rule | `R021` |
| type | `hypium版本号不满足要求` |
| severity | `Critical` |
| file | 相对路径（如`arkui/xxx/oh-package.json5`） |
| line | `"@ohos/hypium"` 所在行号 |
| testcase | `-` |
| snippet | `"@ohos/hypium": "1.0.25"` |
| suggestion | 路径: {文件路径}, 行号: {行号}, 问题描述: 在独立XTS工程 '{工程名}' 中，oh-package.json5的devDependencies.@ohos/hypium版本号为 '{版本}'，低于最低要求版本 1.0.26。 |

## 排除规则

- 被注释掉的 `@ohos/hypium` 条目不检查
- `entry/oh-package.json5` 等子目录文件不检查
- 工程根目录下无 `oh-package.json5` 的不检查
- `devDependencies` 中无 `@ohos/hypium` 条目的不检查

## 技术规范

### 检测范围补充说明

**检查**:
- 独立XTS工程根目录下的 `oh-package.json5` 中，`devDependencies.@ohos/hypium` 的版本号
- 版本号 < `1.0.26` 时报告问题

**不检查**:
- 被注释掉的依赖条目
- 子目录中的 `oh-package.json5`
- 无 `@ohos/hypium` 条目的文件

### 实际案例

```
全仓扫描结果（版本分布）:
- 1.0.26: 2954个工程（合规）
- 1.0.21: 33个工程（不合规，大部分已注释）
- 1.0.6:  18个工程（不合规，部分为活跃依赖如officeservice、web子系统）
- 1.0.24: 4个工程（不合规，如multimedia/av_codec）
- 1.0.25: 3个工程（不合规，如web子系统）
```

### 与其他规则的关系

R021与其他配置文件检查规则（R007/Test.json、R010/BUILD.gn、R012/p7b、R017/syscap.json）类似，都是检查工程配置文件中的特定字段值。区别在于：
- R021的扫描对象是 `oh-package.json5`（非标准JSON，支持注释和尾逗号）
- R021使用正则提取而非 `json.loads()` 解析，以兼容JSON5格式
