# R009: @tc.number命名不规范

## 规则信息

| 属性 | 值 |
|------|------|
| 规则编号 | R009 |
| 问题类型 | @tc.number命名不规范 |
| 严重级别 | Warning |
| 规则复杂度 | simple |

## 问题描述

`@tc.number` 的命名不符合 `SUB_{子系统}_{部件}_XXXX` 格式要求。用例编号命名规则为 `SUB_{子系统}_{部件}_[XX?]_增加4位阿拉伯数字标识`，用例编号的递增要求以100为单位。

**规范来源**: 用例低级问题.md 第16条 — "@tc.number命名不符合要求"

## 扫描范围

| 应扫描 | 文件扩展名 |
|--------|-----------|
| **测试文件** | `.test.ets`, `.test.ts`, `.test.js` |

**⚠️ 默认不扫描**: R009属于Warning级别，默认情况下不会被扫描。需要使用 `--level warning` 或 `--level all` 参数。

## 命名规范

### 正确格式

```
SUB_{子系统}_{部件}_[XX?]_XXXX
```

- `SUB_` — 固定前缀
- `{子系统}` — 子系统名称，使用大写字母（如 `APPEXECFWK`、`ARKUI`）
- `{部件}` — 部件名称，使用大写字母（如 `BUNDLEMGR`、`BUTTON`）
- `[XX?]` — 可选的中间标识段（如 `SDK`、`HAG`、`API9`）
- `XXXX` — 4位阿拉伯数字，递增以100为单位（如 `0100`、`0200`）

### 正确示例

```
SUB_APPEXECFWK_BUNDLEMGR_SDK_HAG_0100
SUB_ARKUI_BUTTON_0100
SUB_DISTRIBUTEDDATAMGR_KVSTORE_0200
SUB_SECURITY_HUKS_AGREE_DH_0300
```

## 检测逻辑

### 步骤1: 提取@tc.number值

```python
import re

def extract_tc_numbers(content: str) -> list[dict]:
    lines = content.split('\n')
    results = []

    for i, line in enumerate(lines, 1):
        # 匹配 @tc.number 后面的值
        match = re.search(r'@tc\.number\s+([^\s*]+)', line)
        if match:
            tc_number = match.group(1).strip()
            results.append({
                'line': i,
                'value': tc_number,
                'snippet': line.strip()
            })

    return results
```

### 步骤2: 验证命名格式

```python
def validate_tc_number(tc_number: str) -> list[str]:
    errors = []

    # 规则1: 必须以 SUB_ 开头
    if not tc_number.startswith('SUB_'):
        errors.append(f'不以SUB_开头: {tc_number}')
        return errors  # 不以SUB_开头则后续检查无意义

    # 规则2: 提取SUB_后面的部分
    remainder = tc_number[4:]  # 去掉 "SUB_"

    if not remainder:
        errors.append(f'SUB_后缺少内容: {tc_number}')
        return errors

    # 规则3: 分割各段
    segments = remainder.split('_')
    if len(segments) < 3:
        errors.append(f'段数不足（至少需要3段: 子系统_部件_数字）: {tc_number}')
        return errors

    # 规则4: 子系统名称必须全大写
    subsystem = segments[0]
    if subsystem != subsystem.upper() or not subsystem.isalpha():
        errors.append(f'子系统名称"{subsystem}"应使用全大写字母')

    # 规则5: 部件名称必须全大写
    component = segments[1]
    if component != component.upper() or not component.isalpha():
        errors.append(f'部件名称"{component}"应使用全大写字母')

    # 规则6: 最后一段必须是4位数字
    last_segment = segments[-1]
    if not last_segment.isdigit():
        errors.append(f'数字部分"{last_segment}"应为纯数字')
    elif len(last_segment) != 4:
        errors.append(f'数字部分"{last_segment}"应为4位（当前{len(last_segment)}位）')

    return errors
```

### 步骤3: 完整检测流程

```python
def check_r009(file_path: str, content: str) -> list[dict]:
    tc_numbers = extract_tc_numbers(content)
    issues = []

    for tc in tc_numbers:
        errors = validate_tc_number(tc['value'])
        if errors:
            # 定位所属用例（向下搜索最近的 it('...')）
            testcase = find_nearest_testcase(content.split('\n'), tc['line'])

            issues.append({
                'rule': 'R009',
                'type': '@tc.number命名不规范',
                'severity': 'Warning',
                'file': file_path,
                'line': tc['line'],
                'testcase': testcase,
                'snippet': tc['snippet'],
                'suggestion': (
                    f'路径: {file_path}, 行号: {tc["line"]}, '
                    f'问题描述: @tc.number命名不规范: {"; ".join(errors)}。'
                    f'正确格式: SUB_{{子系统}}_{{部件}}_XXXX'
                )
            })

    return issues


def find_nearest_testcase(lines: list[str], start_line: int) -> str:
    for i in range(start_line - 1, min(start_line + 10, len(lines))):
        match = re.search(r"\bit\s*\(\s*['\"]([^'\"]+)['\"]", lines[i])
        if match:
            return match.group(1)
    return '-'
```

### 步骤4: 检测所有错误类型汇总

| 错误类型 | 检测条件 | 示例 |
|---------|---------|------|
| 不以SUB_开头 | 不匹配 `^SUB_` | `ArcButtonPosition_001` |
| 段数不足 | 分割后少于3段 | `SUB_APPEXECFWK_0100` |
| 子系统名小写 | 含小写字母 | `SUB_appexecfwk_BUNDLEMGR_0100` |
| 部件名小写 | 含小写字母 | `SUB_APPEXECFWK_bundlemgr_0100` |
| 数字不足4位 | 数字部分长度<4 | `SUB_APPEXECFWK_BUNDLEMGR_100` |
| 数字含非数字 | 最后一段含字母 | `SUB_APPEXECFWK_BUNDLEMGR_01AB` |

## 输出格式

| 列名 | 说明 |
|------|------|
| 问题ID | R009 |
| 问题类型 | @tc.number命名不规范 |
| 严重级别 | Warning |
| 文件路径 | 相对路径 |
| 行号 | 问题所在行号 |
| 所属用例 | 关联的 `it('` 参数名 |
| 代码片段 | 匹配到的代码行 |
| 修复建议 | 路径+行号+问题描述 |

```python
{
    'rule': 'R009',
    'type': '@tc.number命名不规范',
    'severity': 'Warning',
    'file': relative_file_path,
    'line': line_number,
    'testcase': testcase_name,
    'snippet': ' * @tc.number SUB_appexecfwk_bundlemgr_0100',
    'suggestion': '路径: xxx.test.ets, 行号: 10, 问题描述: @tc.number命名不规范: 子系统名称"appexecfwk"应使用全大写字母; 部件名称"bundlemgr"应使用全大写字母。正确格式: SUB_{子系统}_{部件}_XXXX'
}
```

## 错误示例

```typescript
// 错误1: 缺少部件名称
/**
 * @tc.number      SUB_APPEXECFWK_0100
 * @tc.name        testBundleName
 */
it('testBundleName', Level.LEVEL0, () => {
  // ✗ 错误：缺少部件名称，应为 SUB_APPEXECFWK_BUNDLEMGR_0100
});
```

```typescript
// 错误2: 使用小写字母
/**
 * @tc.number      SUB_appexecfwk_bundlemgr_0100
 * @tc.name        testBundleName
 */
it('testBundleName', Level.LEVEL0, () => {
  // ✗ 错误：子系统名称应使用大写字母，应为 SUB_APPEXECFWK_BUNDLEMGR_0100
});
```

```typescript
// 错误3: 数字位数不足
/**
 * @tc.number      SUB_APPEXECFWK_BUNDLEMGR_100
 * @tc.name        testBundleName
 */
it('testBundleName', Level.LEVEL0, () => {
  // ✗ 错误：数字部分应为4位，应为 SUB_APPEXECFWK_BUNDLEMGR_0100
});
```

```typescript
// 错误4: 不以SUB_开头
/**
 * @tc.name   ArcButtonPosition_001
 * @tc.number ArcButtonPosition_001
 */
it('ArcButtonPosition_001', Level.LEVEL0, () => {
  // ✗ 错误：不以SUB_开头
});
```

```typescript
// 错误5: 子系统名大小写混合
/**
 * @tc.number    Sub_Device_Attest_Test_0200
 * @tc.name      testDeviceAttest
 */
it('testDeviceAttest', Level.LEVEL0, () => {
  // ✗ 错误：子系统名称应全大写，应为 SUB_DEVICE_ATTEST_TEST_0200
});
```

## 正确示例

```typescript
// 正确1: 符合命名规范
/**
 * @tc.number      SUB_APPEXECFWK_BUNDLEMGR_SDK_HAG_0100
 * @tc.name        testBundleName
 * @tc.desc        Test bundle name
 */
it('testBundleName', Level.LEVEL0, () => {
  // ✓ 正确：符合 SUB_{子系统}_{部件}_XXXX 格式
});
```

```typescript
// 正确2: 带可选中间段
/**
 * @tc.number      SUB_SECURITY_HUKS_AGREE_DH_0200
 * @tc.name        testHuksAgreeDh
 * @tc.desc        Test HUKS agree DH
 */
it('testHuksAgreeDh', Level.LEVEL0, () => {
  // ✓ 正确：SUB_SECURITY(子系统)_HUKS(部件)_AGREE_DH(可选段)_0200(4位数字)
});
```

## 扫描命令参考

```bash
# 快速扫描不以SUB_开头的@tc.number
grep -rn '@tc.number' --include='*.test.ets' --include='*.test.ts' --include='*.test.js' /path/to/code | grep -v 'SUB_'

# 快速扫描所有@tc.number（人工检查）
grep -rn '@tc.number' --include='*.test.ets' --include='*.test.ts' --include='*.test.js' /path/to/code
```

## 注意事项

1. R009属于Warning级别，默认不扫描，需使用 `--level warning` 或 `--level all`
2. 用例编号递增要求以100为单位（0100, 0200, 0300...），但当前检测暂不强制检查递增步长
3. 子系统名称和部件名称必须全大写
4. 数字部分必须恰好4位
5. 中间段（如 `SDK`、`HAG`、`API9`）是可选的
6. testcase字段取 `@tc.number` 下方最近的 `it('` 参数名
