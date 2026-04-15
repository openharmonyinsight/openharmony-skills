# R008: 用例声明格式不规范

## 规则信息

| 属性 | 值 |
|------|------|
| 规则编号 | R008 |
| 问题类型 | 用例声明格式不规范 |
| 严重级别 | Warning |
| 规则复杂度 | complex |

## 问题描述

测试用例的文档注释格式不符合规范要求，包括缺少注释标记、分隔符错误、空行等问题。

**规范来源**: 用例低级问题.md 第15条 — "XTS上库用例声明需符合要求"

### 规范要求

1. 文档注释以 `/**` 开头，以 `*/` 结尾，每行以 `*` 开始
2. 参数名以 `@` 修饰，参数名和参数值以（一或若干个）空格分隔，禁止使用其他分隔符
3. 文档注释结束行的下一行应紧接要修饰的测试用例，禁止出现空行

## 扫描范围

| 应扫描 | 文件扩展名 |
|--------|-----------|
| **测试文件** | `.test.ets`, `.test.ts`, `.test.js` |

## 检测逻辑

### 步骤1: 收集测试文件

```python
def get_r008_scan_files(directory: str) -> list[str]:
    test_files = get_test_files(directory)  # .test.ets, .test.ts, .test.js
    return test_files
```

### 步骤2: 提取文档注释块

在测试文件中，找到所有位于 `it(` 调用之前的文档注释块：

```python
import re

def extract_doc_blocks(content: str) -> list[dict]:
    lines = content.split('\n')
    doc_blocks = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 查找 /** 开头的文档注释
        if stripped.startswith('/**'):
            block_start = i + 1  # 1-indexed
            block_lines = [line]
            j = i + 1

            # 收集注释块内容直到 */
            while j < len(lines):
                block_lines.append(lines[j])
                if '*/' in lines[j]:
                    break
                j += 1

            block_end = j + 1  # 1-indexed
            block_text = '\n'.join(block_lines)

            # 检查注释块后是否紧跟 it() 调用
            next_code_line_idx = j + 1
            testcase_name = None
            has_empty_line = False

            # 跳过空行
            while next_code_line_idx < len(lines) and lines[next_code_line_idx].strip() == '':
                has_empty_line = True
                next_code_line_idx += 1

            if next_code_line_idx < len(lines):
                next_line = lines[next_code_line_idx].strip()
                tc_match = re.search(r"\bit\s*\(\s*['\"]([^'\"]+)['\"]", next_line)
                if tc_match:
                    testcase_name = tc_match.group(1)

            doc_blocks.append({
                'start_line': block_start,
                'end_line': block_end,
                'lines': block_lines,
                'text': block_text,
                'testcase': testcase_name or '-',
                'has_empty_line_before_it': has_empty_line,
                'next_code_line': next_code_line_idx + 1 if next_code_line_idx < len(lines) else None
            })

            i = j + 1
        else:
            i += 1

    return doc_blocks
```

### 步骤3: 检测注释格式问题

对每个文档注释块，检测以下5种问题：

```python
def check_doc_block(block: dict) -> list[dict]:
    issues = []
    lines = block['lines']
    testcase = block['testcase']

    # 问题1: 缺少 /** 开头或 */ 结尾
    first_line = lines[0].strip()
    last_line = lines[-1].strip()
    if not first_line.startswith('/**'):
        issues.append({
            'line': block['start_line'],
            'type': 'missing_opening',
            'snippet': first_line,
            'detail': '文档注释未以/**开头'
        })
    if '*/' not in last_line and (len(lines) == 1 or '*/' not in lines[-1]):
        issues.append({
            'line': block['end_line'],
            'type': 'missing_closing',
            'snippet': last_line,
            'detail': '文档注释未以*/结尾'
        })

    # 问题2: 每行未以 * 开始（跳过首行和末行）
    for idx, line in enumerate(lines[1:-1], start=block['start_line'] + 1):
        stripped = line.strip()
        if stripped and not stripped.startswith('*'):
            issues.append({
                'line': idx,
                'type': 'missing_asterisk',
                'snippet': stripped,
                'detail': '注释行未以*开始'
            })

    # 问题3: 参数名缺少 @ 修饰符
    for idx, line in enumerate(lines, start=block['start_line']):
        stripped = line.strip().lstrip('*').strip()
        # 匹配 tc.name, tc.number 等无 @ 前缀的参数
        no_at_match = re.match(r'^(tc\.\w+)\s+\S', stripped)
        if no_at_match:
            issues.append({
                'line': idx,
                'type': 'missing_at_modifier',
                'snippet': line.strip(),
                'detail': f'参数 {no_at_match.group(1)} 缺少@修饰符'
            })

    # 问题4: 使用冒号分隔符（应使用空格）
    for idx, line in enumerate(lines, start=block['start_line']):
        # 匹配 @tc.name : value 或 @tc.name: value 模式
        colon_match = re.search(r'@(tc\.\w+)\s*:\s', line)
        if colon_match:
            issues.append({
                'line': idx,
                'type': 'colon_separator',
                'snippet': line.strip(),
                'detail': f'参数 {colon_match.group(1)} 使用了冒号分隔符，应使用空格'
            })

    # 问题5: 注释结束行与测试用例之间存在空行
    if block['has_empty_line_before_it'] and block['testcase'] != '-':
        issues.append({
            'line': block['end_line'],
            'type': 'empty_line_before_it',
            'snippet': '*/ 后存在空行',
            'detail': '文档注释结束行与测试用例之间不应有空行'
        })

    return issues
```

### 步骤4: 输出问题

```python
def check_r008(file_path: str, content: str) -> list[dict]:
    doc_blocks = extract_doc_blocks(content)
    all_issues = []

    for block in doc_blocks:
        issues = check_doc_block(block)
        for issue in issues:
            all_issues.append({
                'rule': 'R008',
                'type': '用例声明格式不规范',
                'severity': 'Warning',
                'file': file_path,
                'line': issue['line'],
                'testcase': block['testcase'],
                'snippet': issue['snippet'],
                'suggestion': (
                    f'路径: {file_path}, 行号: {issue["line"]}, '
                    f'问题描述: {issue["detail"]}'
                )
            })

    return all_issues
```

## 输出格式

| 列名 | 说明 |
|------|------|
| 问题ID | R008 |
| 问题类型 | 用例声明格式不规范 |
| 严重级别 | Warning |
| 文件路径 | 相对路径 |
| 行号 | 问题所在行号 |
| 所属用例 | 关联的 `it('` 参数名 |
| 代码片段 | 匹配到的代码行 |
| 修复建议 | 路径+行号+问题描述 |

## 错误示例

```typescript
// 错误1: 缺少@修饰符
/**
 * tc.name        testName        // ✗ 错误：缺少@
 * tc.number      SUB_XXX_XXXX_XXXX  // ✗ 错误：缺少@
 */
it('testName', () => {
  console.info('test001');
});
```

```typescript
// 错误2: 使用/* 开头（应为/**）
/*                                           // ✗ 错误：应使用 /**
 * @tc.name        testName
 */
it('testName', () => {
  console.info('test001');
});
```

```typescript
// 错误3: 使用冒号分隔
/**
 * @tc.name       : testName              // ✗ 错误：不应使用冒号
 * @tc.number    : SUB_XXX_XXXX_XXXX     // ✗ 错误：不应使用冒号
 */
it('testName', () => {
  console.info('test001');
});
```

```typescript
// 错误4: 注释结束行与用例间有空行
/**
 * @tc.name        testName
 */
                                                     // ✗ 错误：不应有空行
it('testName', () => {
  console.info('test001');
});
```

```typescript
// 错误5: 注释行未以*开始
/**
   tc.name        testName       // ✗ 错误：未以*开始
 * @tc.number      SUB_XXX_XXXX
 */
it('testName', () => {
  console.info('test001');
});
```

## 正确示例

```typescript
// 正确: 使用标准格式
/**
 * @tc.name        testName
 * @tc.number      SUB_XXX_XXXX_XXXX
 * @tc.desc        测试用例描述
 * @tc.size        MEDIUMTEST
 * @tc.type        Function
 * @tc.level       Level2
 */
it('testName', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, async (done) => {
  console.info('test001');
  done();
});
```

## 检测问题类型汇总

| 类型编号 | 问题 | 检测方法 |
|---------|------|---------|
| 1 | 缺少 `/**` 开头 | 首行不以 `/**` 开始 |
| 2 | 缺少 `*/` 结尾 | 末行不包含 `*/` |
| 3 | 每行未以 `*` 开始 | 中间行不以 `*` 开始 |
| 4 | 参数名缺少 `@` 修饰符 | 行内容匹配 `tc.\w+` 但无 `@` 前缀 |
| 5 | 使用冒号分隔符 | 行内容匹配 `@tc.\w+\s*:` |
| 6 | 注释与用例间有空行 | `*/` 与 `it(` 之间存在空行 |

## 注意事项

1. R008属于Warning级别，默认不扫描，需使用 `--level warning` 或 `--level all`
2. 预期问题数量约321676个，扫描时间约60分钟
3. 只扫描测试文件（`.test.ets`/`.test.ts`/`.test.js`），不扫描非测试源代码文件
4. 同一个注释块可能存在多个问题，每个问题分别报告
5. testcase字段取注释块后紧跟的 `it('` 参数名

## 技术挑战与解决方案

**挑战**: 解析JSDoc注释并检查完整性

**解决方案**:
```python
required_tags = [
    '@tc.number', '@tc.name', '@tc.desc', '@tc.type',
    '@tc.level', '@tc.size', '@tc.size', '@tc.since'
]

---

## 最新评估结果与实现状态（2026-04-14）

### 实现状态

**当前状态**: ❌ **未实现**（使用占位符扫描器）

**技术原因**:
- R008属于"模型生成规则"，需要根据本文档的检测逻辑动态生成扫描代码
- 在 `scripts/main.py` 的 `load_rule_scanners()` 函数中，R008被替换为noop扫描器（空操作）
- 当前实现返回空列表，无法检测任何问题

### 改进方案

**方案1：实现为预置脚本（推荐）**

在 `scripts/simple_rules.py` 中添加R008的扫描实现：

```python
# ======================== R008: 用例声明格式不规范 ========================
# Source: rules/R008/SKILL.md

_R008_NO_AT_RE = re.compile(r'^\s*\*\s*(tc\.\w+)\s+\S')


def scan_r008(files, base_dir):
    issues = []
    for fp in files:
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue
        lines = content.split('\n')
        in_doc_comment = False
        doc_start_line = 0
        testcase_name = None

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # 检测 /** 开始
            if stripped.startswith('/**'):
                in_doc_comment = True
                doc_start_line = i
                continue

            # 检测 */ 结束
            if in_doc_comment and '*/' in stripped:
                in_doc_comment = False
                # 查找下一个 it() 调用
                for j in range(i, min(i + 5, len(lines))):
                    m = re.search(r"\bit\s*\(\s*['\"]([^'\"]+)['\"]", lines[j])
                    if m:
                        testcase_name = m.group(1)
                        break
                continue

            # 在注释块内检测问题
            if in_doc_comment:
                # 检测缺少 @ 修饰符
                m = _R008_NO_AT_RE.search(stripped)
                if m:
                    issues.append(_make_issue(
                        'R008', '用例声明格式不规范', 'Warning',
                        fp, base_dir, i, line,
                        f'路径: {os.path.relpath(fp, base_dir)}, 行号: {i}, 问题描述: 参数 {m.group(1)} 缺少@修饰符',
                        testcase=testcase_name or '-'))

    return issues
```

**方案2：动态生成检测代码**

修改 `scripts/main.py`，在扫描时根据本文档的检测逻辑动态生成并执行R008检测代码。

**方案3：独立扫描脚本**

创建独立的 `scripts/scan_r008.py` 文件，实现R008的完整检测逻辑。

### 自动修复支持

根据 `guides/R008_testcase_format/R008_FIX_GUIDE.md`，R008支持自动修复：

**修复内容**:
1. 将 `tc.name` 改为 `@tc.name`
2. 将 `tc.number` 改为 `@tc.number`
3. 删除多余空行

**修复命令**:
```bash
python3 scripts/main.py /path/to/code --rules R008 --fix
```

### 参考文档

- [SKILL.md](../../SKILL.md) - 主技能文档（规则总览和评估结果）
- [scripts/simple_rules.py](../../scripts/simple_rules.py) - 预置扫描脚本（需添加R008实现）
- [scripts/main.py](../../scripts/main.py) - 扫描入口（需修改noop扫描器逻辑）
- [guides/R008_testcase_format/R008_FIX_GUIDE.md](../../guides/R008_testcase_format/R008_FIX_GUIDE.md) - 修复指南

详细评估报告见：`/home/xianf/master/test/xts/evaluation_report.md`
```
