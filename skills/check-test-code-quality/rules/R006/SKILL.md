# R006: 禁止基于设备类型差异化

## 规则信息

| 属性 | 值 |
|------|------|
| 规则编号 | R006 |
| 问题类型 | 禁止基于设备类型差异化 |
| 严重级别 | Critical |
| 规则复杂度 | simple |

## 问题描述

在条件判断中使用 `deviceInfo.deviceType` 或从其赋值的变量进行设备类型判断，导致XTS测试无法在所有设备上正确执行。应使用 `SystemCapability` 和 `canIUse` 进行能力判断。

**规范来源**: 用例低级问题.md 第8条 — "禁止基于deviceInfo.deviceType差异化"

## 扫描范围

**⚠️ 关键陷阱（陷阱2）**: R006必须扫描**所有源代码文件**，不是测试文件！

| 应扫描 | 文件扩展名 |
|--------|-----------|
| **所有源代码文件** | `.ets`, `.ts`, `.js` |

**错误做法**: 只扫描 `.test.ets` 文件 → 漏报部分问题

**正确做法**: 使用 `get_all_source_files()` 获取所有 `.ets`/`.ts`/`.js` 文件

## 检测逻辑

### 步骤1: 检测deviceInfo模块导入

首先扫描文件中是否导入了deviceInfo相关模块：

```python
import re

def has_deviceinfo_import(content: str) -> bool:
    patterns = [
        r"import\s+.*deviceInfo\s+.*from\s+['\"]@ohos\.deviceInfo['\"]",
        r"import\s+\{[^}]*deviceInfo[^}]*\}\s+from\s+['\"]@kit\.BasicServicesKit['\"]",
        r"import\s+.*deviceInfo\s+.*from\s+['\"]@kit\.BasicServicesKit['\"]",
        r"from\s+['\"]@ohos\.deviceInfo['\"]",
    ]
    for p in patterns:
        if re.search(p, content):
            return True
    return False
```

### 步骤2: 检测直接使用deviceInfo.deviceType

在条件判断中直接使用 `deviceInfo.deviceType`：

```python
def check_direct_device_type(lines: list[str], has_import: bool) -> list[dict]:
    issues = []
    if not has_import:
        return issues

    for i, line in enumerate(lines, 1):
        # 排除: console.log/info/debug/error/warn
        if re.search(r'console\.\s*(log|info|debug|error|warn)', line):
            continue

        # 排除: 纯赋值语句（不包含条件判断关键字）
        stripped = line.strip()
        if re.match(r'^(let|const|var|this\.)', stripped) and not re.search(r'\b(if|else|switch|case|return|&&|\|\||\?)\b', stripped):
            continue

        # 检测: deviceInfo.deviceType 出现在条件上下文中
        if re.search(r'\bdeviceInfo\.deviceType\b', line):
            # 检查是否在条件表达式中
            if re.search(r'(if\s*\(|else\s*if\s*\(|switch\s*\(|case\s+|\?\s*|&&|\|\||==|!=|\breturn\b)', line):
                issues.append({
                    'line': i,
                    'snippet': line.strip(),
                    'type': 'direct'
                })

    return issues
```

### 步骤3: 检测变量间接使用

检测从 `deviceInfo.deviceType` 赋值的变量是否在条件判断中使用：

```python
def check_variable_device_type(lines: list[str], has_import: bool) -> list[dict]:
    issues = []
    if not has_import:
        return issues

    # 收集从deviceInfo.deviceType赋值的变量名
    assigned_vars = set()
    var_pattern = re.compile(
        r'(?:let|const|var)\s+(\w+)\s*(?::\s*string)?\s*=\s*deviceInfo\.deviceType'
    )
    for line in lines:
        m = var_pattern.search(line)
        if m:
            assigned_vars.add(m.group(1))

    if not assigned_vars:
        return issues

    # 检测这些变量是否在条件判断中使用
    for i, line in enumerate(lines, 1):
        # 排除: console.log/info/debug/error/warn
        if re.search(r'console\.\s*(log|info|debug|error|warn)', line):
            continue

        for var_name in assigned_vars:
            # 排除: 纯属性访问（如 deviceTypeInfo.length）
            if re.search(rf'\b{re.escape(var_name)}\.\w+\s*$', line.strip()):
                continue

            # 排除: 纯赋值右侧
            if re.match(rf'^\s*(?:let|const|var)\s+{re.escape(var_name)}\s*=', line):
                continue

            # 检测: 变量出现在条件上下文中
            if re.search(rf'\b{re.escape(var_name)}\b', line):
                if re.search(r'(if\s*\(|else\s*if\s*\(|switch\s*\(|case\s+|\?\s*|&&|\|\||==|!=)', line):
                    issues.append({
                        'line': i,
                        'snippet': line.strip(),
                        'type': 'variable',
                        'var_name': var_name
                    })

    return issues
```

### 步骤4: 合并结果并去重

```python
def check_r006(file_path: str, content: str) -> list[dict]:
    lines = content.split('\n')
    has_import = has_deviceinfo_import(content)

    direct_issues = check_direct_device_type(lines, has_import)
    variable_issues = check_variable_device_type(lines, has_import)

    all_issues = direct_issues + variable_issues
    # 去重（同一行不重复报告）
    seen_lines = set()
    unique_issues = []
    for issue in all_issues:
        if issue['line'] not in seen_lines:
            seen_lines.add(issue['line'])
            unique_issues.append(issue)

    return unique_issues
```

### 步骤5: 定位所属用例

```python
def find_testcase_for_line(lines: list[str], target_line: int, filepath: str) -> str:
    if not is_test_file(filepath):
        return '-'
    for i in range(target_line - 1, -1, -1):
        match = re.search(r"\bit\s*\(\s*['\"]([^'\"]+)['\"]", lines[i])
        if match:
            return match.group(1)
    return '-'
```

## 输出格式

| 列名 | 说明 |
|------|------|
| 问题ID | R006 |
| 问题类型 | 禁止基于设备类型差异化 |
| 严重级别 | Critical |
| 文件路径 | 相对路径 |
| 行号 | 问题所在行号 |
| 所属用例 | `it('` 后的参数，非测试文件为 `-` |
| 代码片段 | 匹配到的代码行 |
| 修复建议 | 路径+行号+问题描述 |

```python
{
    'rule': 'R006',
    'type': '禁止基于设备类型差异化',
    'severity': 'Critical',
    'file': relative_file_path,
    'line': line_number,
    'testcase': testcase_name,
    'snippet': matched_line.strip(),
    'suggestion': f'路径: {relative_file_path}, 行号: {line_number}, 问题描述: 在条件判断中使用了deviceInfo.deviceType，应使用SystemCapability和canIUse进行能力判断'
}
```

## 错误示例

```typescript
// 错误1: 直接使用deviceInfo.deviceType
import deviceInfo from '@ohos.deviceInfo';
export default function test() {
  describe('test', () => {
    it('test001', () => {
      if (deviceInfo.deviceType == 'default') {  // ✗ 错误：基于设备类型判断
        // default 设备的测试逻辑
      } else {
        // 其他设备的测试逻辑
      }
    });
  });
}
```

```typescript
// 错误2: 使用deviceTypeInfo变量
import deviceInfo from '@ohos.deviceInfo';
export default function test() {
  describe('test', () => {
    it('test001', () => {
      let deviceTypeInfo: string = deviceInfo.deviceType;
      if (deviceTypeInfo == 'default') {  // ✗ 错误：基于设备类型判断
        // default 设备的测试逻辑
      }
    });
  });
}
```

```typescript
// 错误3: 从@kit.BasicServicesKit导入
import { deviceInfo } from '@kit.BasicServicesKit';
it('MenuStyleOptionsTest_0101', 0, async (done: Function) => {
  let deviceTypeInfo: string = deviceInfo.deviceType
  if (deviceTypeInfo == 'default') {  // ✗ 错误：基于设备类型判断
    let text = JSON.stringify(...);
    expect(text).assertEqual('1');
  }
  done();
});
```

## 正确示例

```typescript
// 正确1: 仅打印日志，不影响测试逻辑
import deviceInfo from '@ohos.deviceInfo';
export default function test() {
  describe('test', () => {
    it('test001', () => {
      console.info('Device type = ' + deviceInfo.deviceType);  // ✓ 正确：仅打印日志
    });
  });
}
```

```typescript
// 正确2: 使用SystemCapability进行能力判断
export default function test() {
  describe('test', () => {
    it('test001', () => {
      if (canIUse("SystemCapability.xxx")) {  // ✓ 正确：基于能力判断
        // 基于能力的测试逻辑
      }
    });
  });
}
```

## 排除情况

以下场景**不报告**问题：

1. **console日志**: `console.info('Device type = ' + deviceInfo.deviceType)` — 仅打印，不影响逻辑
2. **纯赋值语句**: `let deviceTypeInfo: string = deviceInfo.deviceType` — 赋值本身不构成条件判断
3. **属性访问**: `deviceTypeInfo.length` — 对变量属性的访问不构成条件判断
4. **未导入deviceInfo模块**: 如果文件中没有导入deviceInfo相关模块，则不检测

## 扫描命令参考

```bash
# 快速扫描直接使用
grep -rn 'deviceInfo\.deviceType' --include='*.ets' --include='*.ts' --include='*.js' /path/to/code

# 快速扫描变量形式
grep -rn 'deviceType' --include='*.ets' --include='*.ts' --include='*.js' /path/to/code
```

## 已知扫描陷阱

### 陷阱: 属性访问和日志打印被误报为条件判断

**严重性**: 严重，曾导致大量误报（window目录R006问题数从46膨胀到数百）

**问题**: 使用 `deviceType ==` 或 `deviceInfo.deviceType` 等宽泛正则时，会将单纯的属性访问和日志打印误报为条件判断。

**误报案例**:

```typescript
// 误报1: 纯赋值语句 — 不构成条件判断
let deviceType: string = deviceInfo.deviceType;  // ✗ 误报！这只是赋值

// 误报2: console日志打印 — 不影响测试逻辑
console.info(`====>${caseName} end fail====` + deviceInfo.deviceType);  // ✗ 误报！只是打印
```

**正确应报案例**:

```typescript
// 正确报告: 条件判断中使用设备类型
if (deviceType === '2in1' || (deviceType === 'tablet' && isFreeWindowMode === true) ||
    (deviceType === 'phone' && isFreeWindowMode === true)) {  // ✓ 应报告

if (deviceInfo.deviceType === '2in1') {          // ✓ 应报告
} else if (deviceInfo.deviceType === 'tablet') {  // ✓ 应报告
} else if (deviceInfo.deviceType === 'phone') {   // ✓ 应报告
```

**修复**: 必须同时满足两个条件才报告：
1. 行中包含 `deviceType` 或 `deviceInfo.deviceType`
2. 行中包含条件判断关键字（`if`、`else if`、`switch`）或三元运算符（`?`）

并且必须排除以下场景：
- `console.info/log/warn/error/debug(...)` 日志打印行
- `let/const/var deviceType = deviceInfo.deviceType` 纯赋值行
- 不含条件关键字的纯属性访问行

```python
# 错误做法（导致大量误报）
if re.search(r'\bdeviceType\s*==', line):   # 匹配所有 == 比较，包括非条件上下文
    report_issue()

# 正确做法（先排除非条件行，再检测条件判断）
if re.search(r'console\.\s*(log|info|debug|error|warn)', line):
    continue  # 跳过日志打印
if re.match(r'^\s*(let|const|var)\s+.*deviceType\s*=\s*deviceInfo\.deviceType', line):
    continue  # 跳过纯赋值
if not re.search(r'\b(?:if|else\s+if|while|switch)\b', line) and '?' not in line:
    continue  # 跳过非条件行
# 然后才检测 deviceType 条件判断
if re.search(r'\bdeviceType\s*[!=]==\s*[\'"](?:tablet|phone|2in1|pad|pc|tv|wearable|car|default)[\'"]', line):
    report_issue()
```

**影响**: R006规则，所有子系统的扫描结果
