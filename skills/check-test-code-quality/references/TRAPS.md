# 已知扫描陷阱（跨规则通用）

## 陷阱1: it()块提取时字符串字面量中的大括号干扰
- **严重性**: 极严重，曾导致53951个R004误报
- **问题**: 朴素大括号计数会将字符串中的`{}`错误计入
- **修复**: 使用状态机解析，追踪当前是否在字符串字面量内
```python
def count_braces_outside_strings(line):
    in_single = in_double = in_backtick = False
    open_count = close_count = 0
    i = 0
    while i < len(line):
        c = line[i]
        if c == '\\\\' and (in_single or in_double or in_backtick):
            i += 2; continue
        if c == '`' and not in_single and not in_double:
            in_backtick = not in_backtick
        elif c == "'" and not in_double and not in_backtick:
            in_single = not in_single
        elif c == '"' and not in_single and not in_backtick:
            in_double = not in_double
        elif not in_single and not in_double and not in_backtick:
            if c == '{': open_count += 1
            elif c == '}': close_count += 1
        i += 1
    return open_count, close_count
```
- **影响**: R004, R015, R016, R018

## 陷阱1b: 反引号模板字符串中的撇号/引号干扰
- **严重性**: 严重，导致R004误报（有断言的用例被误判为缺少断言）
- **问题**: TypeScript/JavaScript的反引号模板字符串（`` `...` ``）中可能包含撇号（如 `user's`）或引号。如果状态机不追踪反引号状态，会将模板字符串内的`'`误识别为单引号字符串定界符的开启，导致后续代码中的`}`被跳过，大括号匹配错误，it()函数体范围计算错误。
- **触发条件**: it()块内使用反引号模板字符串，且字符串中包含`'`或`"`
- **典型代码**:
```typescript
// 反引号模板字符串中包含撇号 user's
console.info(`getCertificateStorePath Success to get user's path: ${userCACurrentPath}`);
// 上面这行中的 user's 会被没有 backtick 追踪的状态机误判：
//   's path: ${userCACurrentPath}' 被当成一个完整的单引号字符串
//   导致后续的 } catch (err) { ... } 中的 } 被跳过
//   it()函数体范围延伸到下一个it()块，断言检测失效
```
- **修复**: 状态机增加`in_backtick`状态，反引号字符串内的`'`和`"`不作为字符串定界符：
```python
if c == '`' and not in_single and not in_double:
    in_backtick = not in_backtick
elif c == "'" and not in_double and not in_backtick:  # 注意加 in_backtick 条件
    in_single = not in_single
elif c == '"' and not in_single and not in_backtick:   # 注意加 in_backtick 条件
    in_double = not in_double
```
- **影响**: R004, R018（任何依赖大括号匹配提取it()/describe()块范围的规则）

## 陷阱1c: p7b文件是DER二进制格式，json.loads()必失败
- **严重性**: 极严重，导致R012规则100%漏检
- **问题**: p7b签名文件是DER（ASN.1）二进制格式（文件头`0x30 0x82`），不是纯JSON文本。`json.loads()`或`raw.decode('utf-8')`必定失败，如果异常被静默捕获则所有p7b文件全部跳过。
- **修复**: 用`raw.decode('utf-8', errors='replace')`容错解码后，用正则提取`"apl"`、`"app-feature"`等字段，不依赖`json.loads()`。
- **影响**: R012

## 陷阱2: 扫描文件类型错误
- **严重性**: 严重
- **问题**: R001/R005/R006只扫描测试文件，遗漏非测试源代码文件
- **修复**: R001/R005/R006必须使用`get_all_source_files()`
- **影响**: R001 (~81个), R005 (47226个完全漏报), R006

## 陷阱3: R001模块名大小写不匹配
- **严重性**: 严重
- **问题**: `@ohos.systemParameterEnhance`（大写P）与正则 `@ohos.systemparameter`（小写p）不匹配，导致约70个问题漏报
- **修复**: import正则必须同时覆盖 `@ohos.systemparameter` 和 `@ohos.systemParameterEnhance` 两种大小写形式
- **影响**: R001 (~70个, 占总数32%)

## 陷阱4: R001默认导入（default import）未识别
- **严重性**: 严重
- **问题**: `import parameter from '@ohos.systemparameter'`（无大括号）是default import，仅处理named import会漏检约41个问题
- **修复**: 同时处理 `import { xxx } from`（named）和 `import xxx from`（default）两种导入形式
- **影响**: R001 (~41个, 主要集中在usb/bluetooth子系统)

## 陷阱5: R002检测过于宽泛
- **严重性**: 中等，导致3.9倍过度报告
- **修复**: 仅检测`error.code`的string字面量断言，不检测`err.code`（除非确认为别名）

## 陷阱6: R003遗漏assertEqual变体
- **严重性**: 中等，导致~2014个漏报
- **修复**: 必须检测`expect(true).assertEqual(true)`变体

## 陷阱7: R005检测需使用所有源代码文件
- **严重性**: 极严重，导致47226个问题完全漏报（0%检出率）
- **问题**: UI组件的width/height固定值存在于`.ets`页面文件中，不是`.test.ets`文件

## 陷阱8: R016用命名格式检测代替特殊字符检测
- **严重性**: 极严重，导致print子系统313条R016全部误报（0%准确率）
- **问题**: R016规则定义为"testcase名称仅允许`[a-zA-Z0-9_-]`字符"，但`scan_print.py`将其错误实现为"检查名称是否符合`testXxx`或`IT_xxx`格式"，使用正则`^(test|IT|it)[A-Z]\w*$`。例如`printExtension_function_0100`只含合规字符但被误报。
- **根因**: 实现者混淆了"命名格式建议"与"字符集硬性约束"。R016只约束字符集，不约束格式。
- **修复**: 必须使用`^[a-zA-Z0-9_-]+$`做正向字符集匹配，而非格式匹配。
- **验证**: `printExtension_function_0100`、`scan_function_0100`、`testFunc_API_v2-001`均为合规名称，不应触发R016。

## 陷阱9: R016用@tc.name值作为检测源
- **严重性**: 极严重，导致customization子系统R016大量误报
- **问题**: R016的检测对象是`it()`的第一个参数，不是`@tc.name`注解的值。`@tc.name`注解格式多样（`@tc.name: xxx`、`@tc.name    : xxx`等），用正则`@tc\.name\s+(.+)`提取会捕获冒号和空格，导致合规名称被误判。
- **典型误报**: `it("test_set_disallowed_policy_for_account_0700", ...)` 参数合规，但`@tc.name    : test_...`被提取为`: test_...`，冒号触发R016。
- **修复**: R016只检测`it()`的第一个参数。`@tc.name`仅在修复阶段同步修改。

## 陷阱10: 独立XTS工程识别时group类型父BUILD.gn的子工程被错误过滤
- **严重性**: 极严重，导致arkui子系统多层嵌套工程全部漏检（49→997个工程，80→1567个R019问题）
- **问题**: "过滤包含子BUILD.gn的父目录"这一步将所有有父BUILD.gn的子目录排除。但如果父BUILD.gn是`group()`类型（聚合构建），其子目录仍然是独立XTS工程，不应被排除。
- **典型结构**:
```
ace_ets_component_seven/           ← BUILD.gn (group类型)
  ├── ace_ets_component_seven_special/     ← BUILD.gn (独立工程，应扫描) ✗ 被错误排除
  ├── ace_ets_component_common_seven_attrs_align/  ← BUILD.gn (独立工程) ✗ 被错误排除
  └── ... (120+个子工程全部漏检)
```
- **根因**: 过滤`parent_dirs`时未区分group和非group父BUILD.gn。group父目录的BUILD.gn是聚合构建文件，不产生HAP，其子目录中的BUILD.gn才是真正的独立工程。
- **修复**: 只将"父目录是**非group** BUILD.gn"的子目录标记为应排除。group类型的父BUILD.gn不阻止其子目录成为独立工程。
```python
non_group_dirs = {d for d in all_build_gn_dirs if not is_group_build_gn(os.path.join(d, 'BUILD.gn'))}
parent_dirs = set()
for d in all_build_gn_dirs:
    parent = os.path.dirname(d)
    while parent != os.path.abspath(scan_root) and parent != '/':
        if parent in non_group_dirs:  # 只检查非group父目录
            parent_dirs.add(d)
            break
        parent = os.path.dirname(parent)
```
- **影响**: R011, R019, R020（所有工程级检测规则，需识别独立XTS工程边界）

## 陷阱11: R010扫描依赖远程数据源，缺少映射表时静默返回0
- **严重性**: 严重，导致R010规则100%漏检（0个问题，实际应有15个）
- **问题**: R010需要子系统-部件映射表来验证BUILD.gn中`part_name`是否属于对应`subsystem_name`的components。映射表需从3个远程配置文件构建，但预置脚本未内置映射表，也未实现远程获取逻辑。`main.py`将R010作为complex规则使用noop占位，直接返回空列表，不报任何错误。
- **根因链**:
  1. **架构层**: R010被归类为complex规则，`main.py`中为noop占位函数，执行时直接返回`[]`
  2. **数据依赖层**: 映射表需从远程仓库获取3个JSON文件（vendor_hihope/config.json、productdefine_common/rich.json、productdefine_common/chipset_common.json），本地扫描路径中通常不包含这些文件
  3. **URL可达性层**: `rules/R010/SKILL.md`中给出的URL是`gitcode.com`，该域名需要认证才能访问raw文件；实际可用的URL是`gitee.com`
  4. **数据格式层**: SKILL.md示例代码中`subsystem_map[name].update(components)`假设components是字符串列表，但实际数据中components是对象数组`[{"component": "xxx", "features": []}]`，直接update会抛`unhashable type: 'dict'`异常
- **修复**:
  1. 将R010纳入预置扫描脚本，内置远程数据获取和本地缓存逻辑
  2. 使用`gitee.com`作为主URL，`gitcode.com`作为备用URL
  3. components解析时区分字符串和对象两种格式：
  ```python
  for c in components:
      if isinstance(c, str):
          mapping[name].add(c)
      elif isinstance(c, dict):
          mapping[name].add(c.get('component', ''))
  ```
  4. 将映射表缓存到本地文件（如`/tmp/r010_mapping.json`），避免每次扫描都请求远程
  5. 如果远程不可达，在终端输出明确警告而非静默返回0
- **影响**: R010

## 历史教训

**R018文件类型遗漏 (2026-03-11)**: 只扫描`.test.ets`和`.test.ts`，遗漏`.test.js`文件导致4个R018问题全部漏检。修复: 在文件过滤中添加`.test.js`。

**R004反引号模板字符串撇号干扰 (2026-04-07)**: 反引号模板字符串中的撇号（如`user's`）被误识别为单引号定界符，导致大括号匹配错误，有断言的用例被误判为缺少断言。修复: 状态机增加`in_backtick`状态追踪，反引号字符串内的`'`和`"`不作为字符串定界符。

**R012 p7b文件DER二进制格式解析失败 (2026-04-07)**: p7b文件是DER（ASN.1）二进制格式，`json.loads()`和`raw.decode('utf-8')`均失败，异常被静默捕获导致R012规则100%漏检（security目录71个p7b文件全部跳过，漏检1个`apl=system_core`问题）。修复: 使用`raw.decode('utf-8', errors='replace')`容错解码后，用正则直接提取`"apl"`、`"app-feature"`等字段，不依赖`json.loads()`。

**R010外部数据依赖导致静默漏检 (2026-04-14)**: R010需要子系统-部件映射表（54个子系统、332个部件），数据来源于3个远程配置文件。`main.py`将R010作为complex规则使用noop占位函数，执行时静默返回空列表（0个问题），终端输出`(complex规则，需模型生成扫描代码)`但不视为错误。实际扫描发现15个part_name/subsystem_name不匹配问题。根因: ①R010未纳入预置脚本；②远程URL(gitcode.com)需要认证不可达；③SKILL.md示例代码中`set().update(components)`会因components是对象数组而抛异常。修复: 将R010纳入预置脚本，使用gitee.com URL获取数据，正确处理对象格式的components，并添加远程不可达时的明确告警。

**R017 JSON层级类型混淆导致100%漏检 (2026-04-14)**: syscap.json中`data['devices']`是dict（`{"general": [], "custom": [...]}`），不是设备列表。模型实现时直接遍历`data['devices']`，遍历的是dict的key字符串（`"general"`、`"custom"`），对字符串调用`.get('xts')`触发`AttributeError`，异常被静默捕获后所有1568个syscap.json全部跳过（结果0个，实际应1547个）。根因: SKILL.md的"关键路径"未标注每层节点的类型（dict vs list），模型容易混淆`devices`（dict）和`custom`（list）。修复: 在SKILL.md中增加类型约束表，明确`devices`是dict、`custom`是list，并添加验证命令供快速检查漏检。
