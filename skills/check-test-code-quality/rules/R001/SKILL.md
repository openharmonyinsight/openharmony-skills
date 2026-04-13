# R001: 禁止使用getSync系统接口

## 规则元数据

| 字段 | 值 |
|------|-----|
| 规则ID | R001 |
| 规则名称 | 禁止使用getSync系统接口 |
| 严重级别 | Critical |
| 规则类别 | simple（简单规则，可用grep直接检测） |
| 问题类型 | 源代码规范 |
| 修复建议 | 使用`canIUse`接口替代或`差异化API`接口替代 |

## 问题描述

多设备XTS适配禁止使用任何形式的`getSync()`系统接口。`getSync()`是同步阻塞调用，在多设备测试场景中会导致死锁或超时问题。

**注意**: 本规则只针对**系统参数模块**的`getSync()`调用（如`@ohos.systemparameter`），不针对应用API的`getSync()`（如`mPreference.getSync()`）。

## 扫描范围

### 文件类型（关键）

R001必须扫描**所有源代码文件**，不仅仅是测试文件：

| 文件类型 | 扩展名 | 是否扫描 |
|---------|--------|---------|
| ArkTS源代码 | `.ets` | **是** |
| TypeScript源代码 | `.ts` | **是** |
| JavaScript源代码 | `.js` | **是** |
| 配置文件 | `BUILD.gn`, `Test.json`等 | 否 |

### 文件扫描函数

```python
def get_all_source_files(directory: str) -> List[str]:
    """
    获取所有源代码文件（包括测试文件和非测试文件）

    扫描文件类型: .ets, .ts, .js

    Args:
        directory: 扫描目录

    Returns:
        源代码文件路径列表
    """
    source_files = []
    source_extensions = ['.ets', '.ts', '.js']

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in source_extensions):
                source_files.append(os.path.join(root, file))

    return source_files
```

## 检测逻辑

### 第一步：检测系统参数模块的import语句

必须确认文件中存在以下任一import模式，才继续检测getSync调用：

```python
import_patterns = [
    r'import\s+.*\s+from\s+[\'"]@ohos\.systemparameter[\'"]',
    r'import\s+.*\s+from\s+[\'"]@ohos\.systemParameterEnhance[\'"]',
    r'import\s+.*\{.*systemParameter.*\}\s+from\s+[\'"]@kit\.BasicServicesKit[\'"]',
    r'import\s+.*\{.*systemParameterEnhance.*\}\s+from\s+[\'"]@kit\.BasicServicesKit[\'"]'
]
```

**关键**: 必须先确认import存在，再检测getSync调用。这样可以避免误报应用API的getSync。

**注意**: `@ohos.systemparameter`（小写p）和 `@ohos.systemParameterEnhance`（大写P）是两个不同的模块名，必须分别匹配，不能仅用大小写不敏感的正则。同时必须覆盖 default import（`import xxx from`）和 named import（`import { xxx } from`）两种形式。

### 第二步：检测getSync调用

```python
getsync_pattern = r'(\w+)\.getSync\s*\('
```

### 第三步：确认getSync调用对象是系统参数模块的变量

从import语句中提取变量名，然后确认getSync调用使用的变量名与之匹配。

例如：
- `import parameter from '@ohos.systemparameter'` → 变量名`parameter` → 检测`parameter.getSync(`
- `import systemParameterEnhance from '@ohos.systemParameterEnhance'` → 变量名`systemParameterEnhance` → 检测`systemParameterEnhance.getSync(`
- `import { systemParameter } from '@kit.BasicServicesKit'` → 变量名`systemParameter` → 检测`systemParameter.getSync(`

### 完整检测代码

```python
import re
import os

def check_r001(file_path: str, base_dir: str = '') -> list:
    """
    检测R001问题：禁止使用getSync系统接口

    Args:
        file_path: 文件绝对路径
        base_dir: 基准目录（用于计算相对路径）

    Returns:
        问题列表，每条问题包含: rule, type, severity, file, line, testcase, snippet, suggestion
    """
    issues = []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    full_content = content

    # 第一步：检测系统参数模块的import
    # 必须同时覆盖 named import 和 default import
    # 必须同时覆盖 @ohos.systemparameter 和 @ohos.systemParameterEnhance（大小写不同）
    import_patterns = [
        # Named import: import { systemParameterEnhance } from '@ohos.systemParameterEnhance'
        r'import\s+\{([^}]+)\}\s+from\s+[\'"]@ohos\.systemparameter[\'"]',
        r'import\s+\{([^}]+)\}\s+from\s+[\'"]@ohos\.systemParameterEnhance[\'"]',
        # Default import: import parameter from '@ohos.systemparameter'
        r'import\s+(\w+)\s+from\s+[\'"]@ohos\.systemparameter[\'"]',
        r'import\s+(\w+)\s+from\s+[\'"]@ohos\.systemParameterEnhance[\'"]',
        # @kit.BasicServicesKit (仅 named import)
        r'import\s+\{([^}]*\b(?:systemParameter|systemParameterEnhance)\b[^}]*)\}\s+from\s+[\'"]@kit\.BasicServicesKit[\'"]',
    ]

    has_system_param_import = False
    system_param_vars = set()

    for pattern in import_patterns:
        for match in re.finditer(pattern, full_content):
            has_system_param_import = True
            if match.lastindex and match.group(1):
                system_param_vars.add(match.group(1))
            else:
                named_match = re.search(
                    r'\b(systemParameter|systemParameterEnhance)\b',
                    match.group(0)
                )
                if named_match:
                    system_param_vars.add(named_match.group(1))

    if not has_system_param_import:
        return issues

    # 第二步：检测getSync调用
    getsync_pattern = r'(\w+)\.getSync\s*\('

    for i, line in enumerate(lines, 1):
        for match in re.finditer(getsync_pattern, line):
            var_name = match.group(1)

            # 第三步：确认是系统参数模块的变量
            if var_name in system_param_vars:
                rel_path = os.path.relpath(file_path, base_dir) if base_dir else file_path
                testcase = find_testcase(lines, i)

                issues.append({
                    'rule': 'R001',
                    'type': '禁止使用getSync系统接口',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': i,
                    'testcase': testcase,
                    'snippet': line.strip(),
                    'suggestion': (
                        f"多设备XTS适配禁止使用getSync()系统接口。"
                        f"请使用canIUse接口替代或差异化API接口替代。"
                    )
                })

    return issues


def find_testcase(lines: list, target_line: int) -> str:
    """
    查找目标行所在的it()块，提取testcase名称

    Args:
        lines: 文件所有行（0-indexed list）
        target_line: 目标行号（1-indexed）

    Returns:
        testcase名称，或 '-'
    """
    it_pattern = re.compile(r"\bit\s*\(\s*['\"]([^'\"]+)['\"]")

    best_it_name = '-'
    best_it_start = -1

    for i, line in enumerate(lines):
        match = it_pattern.search(line)
        if match and (i + 1) <= target_line:
            if (i + 1) > best_it_start:
                best_it_name = match.group(1)
                best_it_start = i + 1

    if best_it_start > 0 and best_it_start <= target_line:
        return best_it_name

    return '-'


def scan_directory(directory: str) -> list:
    """
    扫描目录中所有源代码文件的R001问题

    Args:
        directory: 扫描目录

    Returns:
        所有问题列表
    """
    all_issues = []

    source_extensions = ['.ets', '.ts', '.js']

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in source_extensions):
                file_path = os.path.join(root, file)
                issues = check_r001(file_path, directory)
                all_issues.extend(issues)

    return all_issues
```

## 检测要点

| 检测项 | 要求 |
|--------|------|
| 检测所有形式的getSync()调用 | 必须 |
| 支持多个import语句 | 必须 |
| 支持变量引用（如`parameter.getSync()`） | 必须 |
| 不检测应用API的getSync（如`mPreference.getSync()`） | 必须 |
| 确认系统参数import存在后才报告 | 必须 |
| **同时覆盖 `@ohos.systemparameter` 和 `@ohos.systemParameterEnhance` 两种大小写** | **必须** |
| **同时处理 named import（`{ }`）和 default import（无 `{ }`）** | **必须** |
| **处理多行 import 语句** | 建议 |

## 输出格式

每条issue必须包含以下字段：

```python
{
    'rule': 'R001',                      # 问题规则编号
    'type': '禁止使用getSync系统接口',     # 问题类型描述
    'severity': 'Critical',              # 严重级别
    'file': 'rel/path.test.ets',         # 相对文件路径
    'line': 25,                          # 问题行号
    'testcase': 'testGetSync',           # 所属用例名称（it()的第一个参数），无对应用例时为 '-'
    'snippet': 'parameter.getSync(...)', # 问题代码片段
    'suggestion': '...'                  # 修复建议
}
```

### testcase字段说明

- **非测试文件**（如BUILD.gn、Ability文件、Page文件等）中检测到的问题：testcase字段为 `-`
- **测试文件**中不在任何`it()`块内的问题（如import语句、describe级别的代码）：testcase字段为 `-`
- **测试文件**中在`it()`块内的问题：取`it('`后面的第一个字符串参数

## 代码示例

### 错误示例

#### 错误1：使用parameter.getSync()

```javascript
import parameter from '@ohos.systemparameter';
export default function test() {
  describe('test', () => {
    it('test001', () => {
      let value = parameter.getSync('key');  // ✗ 错误：使用了getSync系统接口
      expect(value).assertEqual('expected');
    });
  });
}
```

#### 错误2：使用systemParameterEnhance.getSync()

```javascript
import systemParameterEnhance from '@ohos.systemParameterEnhance';
export default function test() {
  describe('test', () => {
    it('test001', () => {
      let value = systemParameterEnhance.getSync('key');  // ✗ 错误：使用了getSync系统接口
      expect(value).assertEqual('expected');
    });
  });
}
```

#### 错误3：从@kit.BasicServicesKit导入并使用getSync

```javascript
import { systemParameter } from '@kit.BasicServicesKit';
export default function test() {
  describe('test', () => {
    it('test001', () => {
      let value = systemParameter.getSync('key');  // ✗ 错误：使用了getSync系统接口
      expect(value).assertEqual('expected');
    });
  });
}
```

### 正确示例

#### 正确1：使用canIUse进行能力判断

```javascript
import { BusinessError } from '@kit.BasicServicesKit';
export default function test() {
  describe('test', () => {
    it('test001', () => {
      if (canIUse("SystemCapability.xxx")) {
        // 基于能力的判断
      }
    });
  });
}
```

#### 正确2：使用差异化API（异步get替代getSync）

```javascript
import { BusinessError } from '@kit.BasicServicesKit';
export default function test() {
  describe('test', () => {
    it('test001', async (done: Function) => {
      try {
        // 使用异步API替代getSync
        let value = await parameter.get('key');
        expect(value).assertEqual('expected');
        done();
      } catch (error) {
        expect(error.code).assertEqual(17100001);
        done();
      }
    });
  });
}
```

#### 正确3：使用mPreference等应用API（不是系统接口）

```javascript
import preferences from '@ohos.data.preferences';
export default function test() {
  describe('test', () => {
    it('test001', () => {
      let value = mPreference.getSync('key');  // ✓ 正确：这是应用API，不是系统接口
      expect(value).assertEqual('expected');
    });
  });
}
```

## 陷阱与警告

### 陷阱：扫描文件类型错误（导致约81个问题漏报）

**严重性**: 极高

**问题描述**: R001不仅存在于测试文件（`.test.ets`）中，也存在于**非测试源代码文件**（如`.ets`页面文件、`.ts`模块文件、Ability文件等）。

**错误做法**:
```python
# 错误: 只扫描测试文件
test_files = get_test_files(directory)  # 只返回 .test.ets/.test.ts/.test.js
for fp in test_files:
    check_r001(fp, ...)  # 漏掉 Ability/Page 等文件中的 getSync
```

**正确做法**:
```python
# 正确: R001 应扫描所有源代码文件
source_files = get_all_source_files(directory)  # 返回所有 .ets/.ts/.js
for fp in source_files:
    check_r001(fp, ...)
```

**影响**: 使用`get_test_files()`而非`get_all_source_files()`会导致约81个R001问题漏报。

**规则分类参考**:

| 规则类别 | 扫描范围 | 相关规则 | 文件扫描函数 |
|---------|---------|---------|------------|
| **源代码规范** | 所有源代码文件 | **R001**, R005, R006 | `get_all_source_files()` |
| 测试代码规范 | 仅测试文件 | R002, R003, R004, R015, R016, R018 | `get_test_files()` |
| 配置文件 | 配置文件 | R007, R010, R012, R014, R017 | 特殊处理 |

### 陷阱：误报应用API的getSync

**问题描述**: 不是所有`getSync()`调用都违反R001。只有系统参数模块（`@ohos.systemparameter`等）的`getSync()`才是禁止的。应用API（如`@ohos.data.preferences`的`mPreference.getSync()`）是允许的。

**检测策略**: 必须先确认文件中存在系统参数模块的import语句，然后再检测getSync调用，且调用变量必须与import的变量名匹配。

### 陷阱：模块名大小写不匹配（导致约70个问题漏报）

**严重性**: 严重

**问题描述**: 系统参数模块存在两种大小写形式的模块名，正则表达式必须同时覆盖，否则会漏检大量问题。

| 模块名形式 | 示例 | 出现频率 |
|-----------|------|---------|
| 小写 | `@ohos.systemparameter` | 较少 |
| **大写P** | `@ohos.systemParameterEnhance` | **主要形式（约70条）** |

**错误做法**（仅匹配小写）:
```python
import_patterns = [
    r'import\s+\{([^}]+)\}\s+from\s+["\']@ohos\.systemparameter(?:Enhance)?["\']',
    # ↑ systemparameter 小写 p，无法匹配 @ohos.systemParameterEnhance（大写 P）
]
```

**正确做法**（同时覆盖两种大小写）:
```python
import_patterns = [
    r'import\s+\{([^}]+)\}\s+from\s+["\']@ohos\.systemparameter["\']',
    r'import\s+\{([^}]+)\}\s+from\s+["\']@ohos\.systemParameterEnhance["\']',
    r'import\s+\{([^}]+)\}\s+from\s+["\']@kit\.BasicServicesKit["\']',
]
# 或者使用 re.IGNORECASE 标志：
# r'import\s+\{([^}]+)\}\s+from\s+["\']@ohos\.systemparameter(?:Enhance)?["\']'
# 需注意 IGNORECASE 也会匹配 @ohos.SystemParameter 等不存在的大小写组合
```

**影响**: 实际扫描中（xts_acts目录，85277个源代码文件），仅因此大小写问题就漏检70条，占R001问题总数的32%（70/220）。

**验证方法**: 扫描完成后，检查结果中是否存在来自 `@ohos.systemParameterEnhance` 导入的文件。如果大量 ability_runtime 目录下的文件缺失，很可能是此问题。

### 陷阱：默认导入（default import）未识别（导致约41个问题漏报）

**严重性**: 严重

**问题描述**: 系统参数模块的导入有两种语法形式。如果只处理 named import（大括号形式），会漏检 default import 形式。

| 导入形式 | 语法 | 变量提取方式 | 出现频率 |
|---------|------|------------|---------|
| Named import | `import { systemParameterEnhance } from '@ohos.systemParameterEnhance'` | 从 `{ }` 内提取 | 较多 |
| **Default import** | `import parameter from '@ohos.systemparameter'` | 从 `import` 后提取变量名 | **约41条** |

**典型代码**（default import，常见于 usb、bluetooth 等子系统）:
```javascript
import parameter from '@ohos.systemparameter';

// 后续使用:
testParam.sendData = parameter.getSync('test_usb', 'default');
```

**错误做法**（只处理 named import）:
```python
# 仅匹配 import { xxx } from '...' 形式
named_import_re = re.compile(
    r'import\s+\{([^}]+)\}\s+from\s+["\'](@ohos\.systemparameter(?:Enhance)?|@kit\.BasicServicesKit)["\']'
)
# ↑ 无法匹配 import parameter from '@ohos.systemparameter'
```

**正确做法**（同时处理两种导入形式）:
```python
# Named import: import { systemParameterEnhance } from '...'
named_import_re = re.compile(
    r'import\s+\{([^}]+)\}\s+from\s+["\'](@ohos\.systemparameter(?:Enhance)?|@kit\.BasicServicesKit)["\']'
)

# Default import: import parameter from '...'
default_import_re = re.compile(
    r'import\s+(\w+)\s+from\s+["\'](@ohos\.systemparameter(?:Enhance)?|@kit\.BasicServicesKit)["\']'
)

# 使用 re.finditer（而非 re.search）以支持同一文件中的多个导入
for m in named_import_re.finditer(content):
    names = [n.strip() for n in m.group(1).split(',')]
    var_names.update(names)

for m in default_import_re.finditer(content):
    var_names.add(m.group(1))  # m.group(1) 是 default import 的变量名
```

**影响**: 实际扫描中漏检41条，主要集中在 `usb/usb_standard`、`communication/bluetooth_ble` 等子系统的测试文件中。

### 陷阱：多行导入语句未处理

**严重性**: 低

**问题描述**: 部分文件的 import 语句跨多行书写，单行正则无法匹配。

```javascript
// 多行 import 示例
import {
  systemParameterEnhance,
  otherModule
} from '@ohos.systemParameterEnhance';
```

**修复**: 扫描前将多行 import 合并为单行，或使用 `re.DOTALL` / `re.MULTILINE` 标志。

```python
# 将多行合并为单行后再匹配
normalized_content = re.sub(r'\n\s*', ' ', content)
matches = import_re.finditer(normalized_content)
```

## 参考文档

- [SKILL.md](../../SKILL.md) - 主技能文档（规则总览）
- [rules/R001/SKILL.md](SKILL.md) - R001规则完整说明（含示例、实现细节、陷阱说明）
- [references/兼容性测试代码设计和编码规范2.0.md](../../references/兼容性测试代码设计和编码规范2.0.md) - 编码规范参考
- [references/用例低级问题.md](../../references/用例低级问题.md) - 用例低级问题参考
