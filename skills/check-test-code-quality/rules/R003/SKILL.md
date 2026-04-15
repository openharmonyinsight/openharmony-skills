# R003: 禁止恒真断言

## 规则概述

| 属性 | 值 |
|------|-----|
| 规则编号 | R003 |
| 问题类型 | 禁止恒真断言 |
| 严重级别 | Critical |
| 规则分类 | 简单规则（正则匹配） |
| 扫描范围 | 所有源代码文件（`.ets`, `.ts`, `.js`） |

## 问题描述

测试用例中使用 `expect(true).assertTrue()` 等恒真断言，断言只会产生成功结果，用例恒通过。此类断言未对接口实际返回值进行断言校验，相当于没有任何有效断言。

## 检测模式（完整覆盖）

R003规则必须检测以下**全部3种**恒真断言模式：

```python
r003_patterns = [
    # 模式1: expect(true).assertTrue()
    # 最常见的恒真断言形式，true断言为true，恒成立
    re.compile(r'expect\s*\(\s*true\s*\)\s*\.\s*assertTrue\s*\('),

    # 模式2: expect(true).assertEqual(true)  ⚠️ 容易遗漏！
    # 128个问题，占R003总量的3.3%。true等于true，恒成立
    # 如果遗漏此模式，将导致约2014个问题被漏报
    re.compile(r'expect\s*\(\s*true\s*\)\s*\.\s*assertEqual\s*\(\s*true\s*\)'),

    # 模式3: expect(false).assertFalse()
    # false断言为false，恒成立
    re.compile(r'expect\s*\(\s*false\s*\)\s*\.\s*assertFalse\s*\('),
]
```

### 各模式占比

| 模式 | 代码形式 | 预估问题数 | 占比 | 遗漏影响 |
|------|---------|-----------|------|---------|
| 模式1 | `expect(true).assertTrue()` | ~3,800 | ~96.7% | 主要模式 |
| 模式2 | `expect(true).assertEqual(true)` | ~128 | ~3.3% | **易遗漏** |
| 模式3 | `expect(false).assertFalse()` | ~6 | ~0.0% | 罕见 |

## ⚠️ 已知陷阱

### 陷阱: 遗漏 assertEqual(true) 变体

**问题严重性**: ⭐⭐⭐⭐ 严重

`expect(true).assertEqual(true)` 是恒真断言的变体，容易被遗漏。该模式虽然占比仅3.3%（128个），但遗漏会导致约2014个相关文件的问题被完全忽略。必须将所有3种模式都加入检测列表。

> 详见 [references/TRAPS.md](../../references/TRAPS.md) 陷阱6。

## 错误示例

### 错误1: expect(true).assertTrue()（模式1，最常见）

```typescript
it('testCounter01', Level.LEVEL0, async (done: Function) => {
  console.info('[testCounter01] START');
  let strJson = getInspectorByKey('Counter');
  let obj: ESObject = JSON.parse(strJson);
  console.info("[testCounter01] obj is : " + JSON.stringify(obj.$attrs));
  expect(true).assertTrue();  // ✗ 恒真断言：true断言为true，恒成立
  console.info('[testCounter01] END');
  done();
});
```

来源: [用例低级问题.md](../../references/用例低级问题.md) 第⑤点

### 错误2: expect(true).assertEqual(true)（模式2，易遗漏）

```typescript
it('testIsLocationEnabled06', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
  try {
    let state = geolocationm.isLocationEnabled();
    console.info('[lbs_js] getLocationSwitchState06 result: ' + JSON.stringify(state));
    expect(true).assertEqual(state);  // ✗ 此处是对state的断言，但如果state恰好为true...
  } catch (error) {
    console.info("[lbs_js] getLocationSwitchState06 try err." + JSON.stringify(error));
    if (error.code == "801") {
      expect(error.code).assertEqual("801")
    } else {
      expect().assertFail();
    }
  }
});
```

来源: [用例低级问题.md](../../references/用例低级问题.md) 第②点

### 错误3: expect(true).assertEqual(true)（模式2变体）

```typescript
it('effectKitTest_static_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
  async (done: () => void): Promise<void> => {
  // ...
  try {
    let headFilter: effectKit.Filter = effectKit.createEffect(pixelMap);
    console.info('www data succeed')
    if (headFilter == undefined) {
      hilog.info(domain, tag, '%{public}s', 'effectKit createFilter failed.');
      return undefined;
    }
    let blurFilter: effectKit.Filter = headFilter.blur(10);
    expect(true).assertTrue();  // ✗ 恒真断言（模式1）
    hilog.info(domain, tag, '%{public}s', 'effectKit createFilter successfully.');
    const effectPixelMap = await blurFilter.getEffectPixelMap();
    if (effectPixelMap != undefined) {
      hilog.info(domain, tag, '%{public}s', 'effectKit getEffectPixelMap successfully.');
    } else {
      hilog.info(domain, tag, '%{public}s', 'effectKit getEffectPixelMap failed.');
    }
    hilog.info(domain, tag, '%{public}s', 'effectKit test END');
    expect(true).assertTrue();  // ✗ 恒真断言（模式1），出现两次
  } catch (err) {
    console.info('www data err ' + JSON.stringify(err))
  }
  done();
})
```

来源: [用例低级问题.md](../../references/用例低级问题.md) 第②点

### 错误4: expect(false).assertFalse()（模式3，罕见）

```typescript
it('testBoolCheck', Level.LEVEL0, () => {
  let result = someFunction();
  if (result === false) {
    expect(false).assertFalse();  // ✗ 恒真断言：false断言为false，恒成立
  }
});
```

## 正确示例

### 正确1: 使用实际变量值

```typescript
it('test001', Level.LEVEL0, () => {
  let actualValue = someFunction();
  expect(actualValue).assertTrue();  // ✓ 断言实际值，非恒真
});
```

### 正确2: 使用assertFalse验证实际false值

```typescript
it('test002', Level.LEVEL0, () => {
  let actualValue = someFunction();
  expect(actualValue).assertFalse();  // ✓ 断言实际值为false
});
```

### 正确3: 使用assertEqual验证具体值

```typescript
it('test003', Level.LEVEL0, () => {
  let actualValue = someFunction();
  expect(actualValue).assertEqual('expected');  // ✓ 断言具体期望值
});
```

### 正确4: 使用比较运算

```typescript
it('test004', Level.LEVEL0, () => {
  let count = 900;
  expect(count).assertLargerOrEqual(800);  // ✓ 断言count >= 800
});
```

### 正确5: try-catch中每个分支都有有效断言

```typescript
it('test005', Level.LEVEL0, async (done: Function) => {
  try {
    await someAsyncFunction();
    expect(true).assertTrue();  // ✗ 仍然是R003问题（恒真断言）
    done();
  } catch (error) {
    expect(error.code).assertEqual(401);  // ✓ catch块中有有效断言
    done();
  }
});
```

> **注意**: 即使try-catch结构中catch块有有效断言（如error.code），try块中的`expect(true).assertTrue()`仍然属于R003问题，因为该断言本身是恒真的。正确做法是移除try块中的恒真断言，或替换为对实际返回值的有效断言。

## 扫描实现

### 伪代码

```python
def check_r003(file_path: str, content: str, lines: list[str]) -> list[dict]:
    """
    扫描R003: 禁止恒真断言

    Args:
        file_path: 文件相对路径
        content: 文件完整内容
        lines: 文件按行分割的列表

    Returns:
        问题列表
    """
    issues = []

    r003_patterns = [
        re.compile(r'expect\s*\(\s*true\s*\)\s*\.\s*assertTrue\s*\('),
        re.compile(r'expect\s*\(\s*true\s*\)\s*\.\s*assertEqual\s*\(\s*true\s*\)'),
        re.compile(r'expect\s*\(\s*false\s*\)\s*\.\s*assertFalse\s*\('),
    ]

    # 解析it()块范围，用于填充testcase字段
    it_blocks = parse_it_blocks(content, lines)

    for i, line in enumerate(lines, 1):
        for pattern in r003_patterns:
            match = pattern.search(line)
            if match:
                # 提取匹配到的代码片段
                snippet = line.strip()

                # 确定所属用例
                testcase = find_testcase_for_line(it_blocks, i)

                # 判断恒真类型
                if 'assertEqual' in snippet:
                    suggestion = (
                        "禁止恒真断言。expect(true).assertEqual(true) 恒成立，"
                        "未对接口实际返回值进行断言校验。"
                        "请替换为对实际业务逻辑的有效断言，"
                        "如 expect(actualValue).assertEqual(expectedValue)。"
                    )
                elif 'assertFalse' in snippet:
                    suggestion = (
                        "禁止恒真断言。expect(false).assertFalse() 恒成立，"
                        "请替换为对实际变量值的断言，"
                        "如 expect(actualValue).assertFalse()。"
                    )
                else:
                    suggestion = (
                        "禁止恒真断言。expect(true).assertTrue() 恒成立，"
                        "未对接口实际返回值进行断言校验。"
                        "请替换为对实际业务逻辑的有效断言，"
                        "如 expect(actualValue).assertTrue() 或 expect(actualValue).assertEqual(expected)。"
                    )

                issues.append({
                    'rule': 'R003',
                    'type': '禁止恒真断言',
                    'severity': 'Critical',
                    'file': file_path,
                    'line': i,
                    'testcase': testcase,
                    'snippet': snippet,
                    'suggestion': suggestion,
                })
                break  # 同一行只报告一次（优先匹配第一个模式）

    return issues
```

### testcase字段解析

所有R003扫描结果必须包含 `testcase` 字段，用于标识问题所属的测试用例：

```python
def find_testcase_for_line(it_blocks: list[dict], line_num: int) -> str:
    """
    查找指定行号所属的it()块，返回testcase名称。

    Args:
        it_blocks: it()块列表，每个元素包含 {'name': str, 'start': int, 'end': int}
        line_num: 问题所在行号

    Returns:
        testcase名称，不在任何it()块内时返回 '-'
    """
    for block in it_blocks:
        if block['start'] <= line_num <= block['end']:
            return block['name']
    return '-'
```

## 输出格式

### Excel报告列

| 列序 | 列名 | 示例 |
|------|------|------|
| 1 | 问题ID | `R003` |
| 2 | 问题类型 | `禁止恒真断言` |
| 3 | 严重级别 | `Critical` |
| 4 | 文件路径 | `arkui/ace_ets_component_seven/.../Counter.test.ets` |
| 5 | 行号 | `213` |
| 6 | 所属用例 | `testCounter01` |
| 7 | 代码片段 | `expect(true).assertTrue();` |
| 8 | 修复建议 | `禁止恒真断言。expect(true).assertTrue() 恒成立，未对接口实际返回值进行断言校验。请替换为对实际业务逻辑的有效断言...` |

### 终端输出示例

```
[R003] arkui/ace_ets_component_seven/ace_ets_component_seven_special/entry/src/main/ets/test/Counter.test.ets:213
  用例: testCounter01
  代码: expect(true).assertTrue();
  建议: 禁止恒真断言。expect(true).assertTrue() 恒成立，未对接口实际返回值进行断言校验。
        请替换为对实际业务逻辑的有效断言，如 expect(actualValue).assertTrue() 或 expect(actualValue).assertEqual(expected)。
```

## 参考资料

- [用例低级问题.md](../../references/用例低级问题.md) - 第③点：禁止恒真断言
- [兼容性测试代码设计和编码规范2.0](../../references/兼容性测试代码设计和编码规范2.0.md) - 测试用例断言规范
- [官方文档](https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/application-test/unittest-guidelines.md)

## 额外正确示例

> 来源: 规则内置示例（原 docs/EXAMPLES.md，已迁移）

以下断言方法均可用于替代恒真断言：

### 正确6: 使用assertLessOrEqual - 检验小于等于

```typescript
it('test003', Level.LEVEL0, () => {
  let value = 50;
  expect(value).assertLessOrEqual(100);  // ✓ 正确：断言value <= 100
});
```

### 正确7: 使用assertLarger - 检验大于

```typescript
it('test004', Level.LEVEL0, () => {
  let result = 100;
  expect(result).assertLarger(50);  // ✓ 正确：断言result > 50
});
```

### 正确8: 使用assertLess - 检验小于

```typescript
it('test005', Level.LEVEL0, () => {
  let timeout = 5000;
  expect(timeout).assertLess(10000);  // ✓ 正确：断言timeout < 10000
});
```

---

### 参考文档

- [SKILL.md](../../SKILL.md) - 主技能文档（规则总览和评估结果）
- [scripts/simple_rules.py](../../scripts/simple_rules.py) - R003预置扫描脚本实现
