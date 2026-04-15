# R005: 组件尺寸使用固定值

## 规则信息

| 属性 | 值 |
|------|------|
| 规则编号 | R005 |
| 问题类型 | 组件尺寸使用固定值 |
| 严重级别 | Warning |
| 规则复杂度 | complex |

## 问题描述

UI组件的width/height属性使用了固定像素值，导致多设备上页面适用性差，引起XTS适配问题。应使用百分比方式实现自适应布局。

**规范来源**: 用例低级问题.md 第5条 — "页面设计涉及组件尺寸大小，禁止使用固定值，考虑百分比方式"

## 扫描范围

**⚠️ 关键陷阱**: R005必须扫描**所有源代码文件**，不是测试文件！仅扫描`.test.ets`会漏报47226个问题（检出率0%）。

> 详见 [references/TRAPS.md](../../references/TRAPS.md) 陷阱2/7。

## 检测逻辑

### 步骤1: 收集文件

```python
def get_r005_scan_files(directory: str) -> list[str]:
    source_files = get_all_source_files(directory)  # .ets, .ts, .js
    return source_files
```

### 步骤2: 逐行检测

对每个文件逐行扫描，检测以下模式：

**模式A — 数值参数形式**:
```python
import re

# .width(100), .width( 200 ), .height(50)
numeric_pattern = re.compile(r'\.(width|height)\s*\(\s*\d+\s*\)')
```

**模式B — 字符串参数形式**:
```python
# .width('100px'), .width("100vp"), .height('200fp'), .height("50lpx")
string_pattern = re.compile(
    r"""\.(width|height)\s*\(\s*['"]\s*\d+\s*(?:px|vp|fp|lpx)?\s*['"]\s*\)""",
    re.IGNORECASE
)
```

**排除模式**（不应报告）:
```python
# 百分比 — 正确用法
# .width('50%'), .width("100%")
percent_pattern = re.compile(r'\.(width|height)\s*\(\s*['"]?\s*\d+\.?\d*\s*%')

# 变量引用 — 正确用法
# .width(widthValue), .height(this.height)
variable_pattern = re.compile(r'\.(width|height)\s*\(\s*[a-zA-Z_$]')
```

### 步骤3: 定位所属用例

对于源代码文件（非测试文件），`testcase` 字段固定为 `-`。

对于测试文件（`.test.ets`/`.test.ts`/`.test.js`），需要解析该行所在的 `it()` 块，取 `it('` 后的第一个字符串参数作为 testcase 名称。

```python
def find_testcase_for_line(lines: list[str], target_line: int) -> str:
    if not is_test_file(filepath):
        return '-'
    # 向上搜索最近的 it('...') 声明
    for i in range(target_line - 1, -1, -1):
        match = re.search(r"\bit\s*\(\s*['\"]([^'\"]+)['\"]", lines[i])
        if match:
            return match.group(1)
    return '-'
```

### 步骤4: 输出问题

每检测到一个问题，生成以下格式的数据：

```python
{
    'rule': 'R005',
    'type': '组件尺寸使用固定值',
    'severity': 'Warning',
    'file': relative_file_path,
    'line': line_number,
    'testcase': testcase_name,
    'snippet': matched_line.strip(),
    'suggestion': f'路径: {relative_file_path}, 行号: {line_number}, 问题描述: {prop}使用了固定像素值，建议使用百分比方式实现自适应布局'
}
```

## 输出格式

| 列名 | 说明 |
|------|------|
| 问题ID | R005 |
| 问题类型 | 组件尺寸使用固定值 |
| 严重级别 | Warning |
| 文件路径 | 相对路径 |
| 行号 | 问题所在行号 |
| 所属用例 | `it('` 后的参数，非测试文件为 `-` |
| 代码片段 | 匹配到的代码行 |
| 修复建议 | 路径+行号+问题描述 |

## 错误示例

```typescript
// 错误1: width和height都使用固定数值
@Component
struct MyComponent {
  build() {
    Text('Hello')
      .width(100)    // ✗ 错误：使用固定像素值
      .height(50);   // ✗ 错误：使用固定像素值
  }
}
```

```typescript
// 错误2: height使用固定数值
@Component
struct MyComponent {
  build() {
    Text('Hello')
      .width('50%')
      .height(200);  // ✗ 错误：使用固定像素值
  }
}
```

```typescript
// 错误3: 使用字符串形式的固定值
@Component
struct MyComponent {
  build() {
    Image($r('app.media.icon'))
      .width('100px')    // ✗ 错误：使用固定像素值
      .height("100vp");  // ✗ 错误：使用固定像素值
  }
}
```

```typescript
// 错误4: 带空格的数值参数
Column() {
  Row()
    .width( 300 )  // ✗ 错误：使用固定像素值
    .height( 200 ) // ✗ 错误：使用固定像素值
}
```

## 正确示例

```typescript
// 正确1: 使用百分比
@Component
struct MyComponent {
  build() {
    Text('Hello')
      .width('50%')   // ✓ 正确：使用百分比
      .height('30%'); // ✓ 正确：使用百分比
  }
}
```

```typescript
// 正确2: 使用自适应布局
@Component
struct MyComponent {
  build() {
    Text('Hello')
      .width('100%')     // ✓ 正确：自适应宽度
      .layoutWeight(1);  // ✓ 正确：自适应高度
  }
}
```

```typescript
// 正确3: 使用变量（从配置或计算获取）
@Component
struct MyComponent {
  @State componentWidth: number = 0
  @State componentHeight: string = '50%'

  aboutToAppear() {
    this.componentWidth = 200
  }

  build() {
    Text('Hello')
      .width(this.componentWidth)  // ✓ 正确：使用变量
      .height(this.componentHeight) // ✓ 正确：使用变量
  }
}
```

## 扫描命令参考

```bash
# 使用grep快速扫描（仅数值形式）
grep -rn '\.width\s*(\s*[0-9]' --include='*.ets' --include='*.ts' --include='*.js' /path/to/code

# 使用grep快速扫描（字符串形式）
grep -rn "\.width\s*(\s*['\"]" --include='*.ets' --include='*.ts' --include='*.js' /path/to/code
```

## 注意事项

1. **⚠️ 必须扫描所有源代码文件**（`.ets`, `.ts`, `.js`），不能只扫描测试文件
2. 百分比值（`'50%'`、`"100%"`）不算违规
3. 变量引用（`.width(someVar)`）不算违规
4. R005属于Warning级别，默认不扫描，需使用 `--level warning` 或 `--level all`
5. 预期问题数量约47226个，扫描时间约30分钟

## 技术挑战与解决方案

**挑战**: 准确识别固定值，排除百分比和变量

**解决方案**:
```python
patterns = [
    r'\.width\s*\(\s*(\d+)\s*\)',           # .width(100)
    r'\.height\s*\(\s*(\d+)\s*\)',          # .height(100)
    r'\.width\s*\(\s*["\'](\d+)px["\']\s*\)',  # .width('100px')
]

# 排除百分比
exclude_patterns = [
    r'\.width\s*\(\s*["\']\d+%["\']',  # .width('50%')
]

---

## 最新评估结果与实现状态（2026-04-14）

### 实现状态

**当前状态**: ❌ **未实现**（使用占位符扫描器）

**技术原因**:
- R005属于"模型生成规则"，需要根据本文档的检测逻辑动态生成扫描代码
- 在 `scripts/main.py` 的 `load_rule_scanners()` 函数中，R005被替换为noop扫描器（空操作）
- 当前实现返回空列表，无法检测任何问题

### 改进方案

**方案1：实现为预置脚本（推荐）**

在 `scripts/simple_rules.py` 中添加R005的扫描实现：

```python
# ======================== R005: 组件尺寸使用固定值 ========================
# Source: rules/R005/SKILL.md

_R005_NUMERIC_RE = re.compile(r'\.(width|height)\s*\(\s*(\d+)\s*\)')
_R005_STRING_RE = re.compile(
    r"""\.(width|height)\s*\(\s*['"]\s*(\d+)\s*(?:px|vp|fp|lpx)?\s*['"]\s*\)""",
    re.IGNORECASE
)
_R005_PERCENT_RE = re.compile(r'\.(width|height)\s*\(\s*['"]?\s*\d+\.?\d*\s*%')
_R005_VARIABLE_RE = re.compile(r'\.(width|height)\s*\(\s*[a-zA-Z_$]')


def scan_r005(files, base_dir):
    issues = []
    for fp in files:
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # 排除百分比和变量引用
            if _R005_PERCENT_RE.search(line) or _R005_VARIABLE_RE.search(line):
                continue

            # 检测数值形式
            m_num = _R005_NUMERIC_RE.search(line)
            if m_num:
                prop = m_num.group(1)
                tc = _find_testcase(content, i)
                issues.append(_make_issue(
                    'R005', '组件尺寸使用固定值', 'Warning',
                    fp, base_dir, i, line,
                    f'路径: {os.path.relpath(fp, base_dir)}, 行号: {i}, 问题描述: {prop}使用了固定像素值，建议使用百分比方式实现自适应布局',
                    testcase=tc))
                continue

            # 检测字符串形式
            m_str = _R005_STRING_RE.search(line)
            if m_str:
                prop = m_str.group(1)
                tc = _find_testcase(content, i)
                issues.append(_make_issue(
                    'R005', '组件尺寸使用固定值', 'Warning',
                    fp, base_dir, i, line,
                    f'路径: {os.path.relpath(fp, base_dir)}, 行号: {i}, 问题描述: {prop}使用了固定像素值，建议使用百分比方式实现自适应布局',
                    testcase=tc))

    return issues
```

**方案2：动态生成检测代码**

修改 `scripts/main.py`，在扫描时根据本文档的检测逻辑动态生成并执行R005检测代码。

**方案3：独立扫描脚本**

创建独立的 `scripts/scan_r005.py` 文件，实现R005的完整检测逻辑。

### 参考文档

- [SKILL.md](../../SKILL.md) - 主技能文档（规则总览和评估结果）
- [scripts/simple_rules.py](../../scripts/simple_rules.py) - 预置扫描脚本（需添加R005实现）
- [scripts/main.py](../../scripts/main.py) - 扫描入口（需修改noop扫描器逻辑）
```
