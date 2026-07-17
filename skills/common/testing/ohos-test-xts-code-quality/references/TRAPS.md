# 已知扫描陷阱（跨规则通用）

本文档记录了37个已知扫描陷阱，按严重性和影响范围分类。**建议先阅读汇总表格，遇到具体问题时跳转到对应章节。**

## 陷阱汇总表

| 类别 | 陷阱编号 | 严重性 | 影响规则 | 一句话描述 |
|------|---------|--------|---------|-----------|
| **解析陷阱** | 陷阱1 | 极严重 | R004,R015,R016,R018 | 字符串中大括号干扰it()块提取 |
| | 陷阱1b | 严重 | R004,R018 | 反引号模板字符串中撇号干扰 |
| | 陷阱1c | 极严重 | R012 | p7b文件DER二进制格式解析失败 |
| | 陷阱31 | 极严重 | R201,R202 | it()跨行声明导致async/done识别失败 |
| | 陷阱35 | 严重 | R015 | 箭头函数`{`被跳过导致Level误判 |
| **范围陷阱** | 陷阱2 | 严重 | R001,R005,R006 | 仅扫描测试文件遗漏非测试源码 |
| | 陷阱7 | 极严重 | R005 | 47226个问题完全漏报 |
| **检测陷阱** | 陷阱3 | 严重 | R001 | 模块名大小写不匹配漏检70条 |
| | 陷阱4 | 严重 | R001 | default import未识别漏检41条 |
| | 陷阱5 | 中等 | R002 | 检测过于宽泛导致3.9倍过度报告 |
| | 陷阱6 | 中等 | R003 | 遗漏assertEqual变体漏检2014条 |
| | 陷阱8 | 极严重 | R016 | 用格式检测代替特殊字符检测 |
| | 陷阱9 | 极严重 | R016 | 用@tc.name值作为检测源 |
| | 陷阱15 | 严重 | R013,R017,R202,R206 | snippet使用描述文本而非代码 |
| **工程陷阱** | 陷阱10 | 极严重 | R011,R019,R020 | group类型BUILD.gn子工程被过滤 |
| | 陷阱37 | 高 | R018 | 跨文件工程级检测是超范围误检 |
| **数据依赖** | 陷阱11 | 严重 | R010 | 远程映射表不可用时静默返回0 |
| | 陷阱16 | 中等 | 所有规则 | subsystem映射表路径不匹配 |
| **异步陷阱** | 陷阱12 | 高 | R201 | done()未在catch分支调用 |
| | 陷阱13 | 高 | R201 | async函数无done参数是合法模式 |
| | 陷阱39 | 高 | R201 | async+done混用模式下.then()不误报 |
| | 陷阱26 | 高 | R201 | done()在try-catch外部调用合法 |
| | 陷阱27 | 高 | R201 | .then().catch()两边均有done合法 |
| | 陷阱32 | 极严重 | R201 | all_paths_have_done提前return跳过检查 |
| | 陷阱33 | 高 | R201 | 外层catch处理同步异常时无需done |
| | 陷阱14 | 中 | R202 | .then()链中间有.catch() |
| | 陷阱15 | 中 | R202 | await sleep()不需要try-catch |
| | 陷阱22 | 中 | R202 | 系统API await不一定在try-catch中 |
| | 陷阱23 | 极严重 | R202 | is_inside_try_block遇到嵌套回调提前返回 |
| | 陷阱24 | 中 | R202 | SYSTEM_API_PATTERNS不匹配复合方法名 |
| | 陷阱25 | 高 | R202 | .then()链.catch()检测遇回调内分号 |
| | 陷阱34 | 极严重 | R202 | 花括号深度追踪受对象字面量干扰 |
| | 陷阱16 | 高 | R202 | Promise.all是安全的并发 |
| | 陷阱28 | 高 | R201,R202,R004 | it()解析器误匹配export function |
| **资源陷阱** | 陷阱19 | 低 | R204 | .once()注册的监听器自动移除 |
| | 陷阱17 | 高 | R205 | beforeEach不是beforeAll的配对 |
| | 陷阱18 | 高 | R204,R205,R206 | 嵌套describe的钩子独立性 |
| **设计陷阱** | 陷阱20 | 高 | R206 | 只读共享变量不算隐式依赖 |
| | 陷阱36 | 极严重 | R206 | describe级共享变量100%漏检 |
| **输出陷阱** | 陷阱29 | 极严重 | 所有规则 | snippet填写描述性文本而非代码 |
| | 陷阱30 | 严重 | 所有规则 | Excel问题ID列用序号而非规则编号 |
| **格式陷阱** | 陷阱38 | 高 | R008 | 空格分隔也被误判为冒号分隔 |

---

## 详细说明

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

---

## 测试技术问题规则陷阱（R201-R206）

## 陷阱12: done()未在catch分支调用
- **严重性**: 高
- **问题**: 用例有try-catch结构，done()只在try分支调用。当被测接口抛出异常时，用例会超时。
- **修复**: 检测try-catch时，验证每个catch分支都包含 `done()` 调用。
- **影响**: R201

## 陷阱13: async函数无done参数是合法模式
- **严重性**: 高（误报风险）
- **问题**: `it('name', level, async () => { ... })` 无done参数，只要体内所有异步操作均await就是合法的。误判为"缺少done"会导致大量误报。
- **修复**: 先检查是否为 `async` 函数。async且体内异步操作均await → 合法，不报告。
- **影响**: R201

## 陷阱14: .then()链中间有.catch()
- **严重性**: 中（误报风险）
- **问题**: `a.then().then().catch()` 中间有多个.then()，最终有.catch()。不能仅检查第一个.then()后。
- **修复**: 从第一个.then()向后搜索到链结束（遇到`;`或非`.`开头的行），检查整个链是否有.catch()。
- **影响**: R202

## 陷阱15: await sleep()不需要try-catch
- **严重性**: 中（误报风险）
- **问题**: `await sleep(500)` 是工具函数，不会抛异常。
- **修复**: 排除 `await sleep(` 调用。
- **影响**: R202

## 陷阱16: Promise.all是安全的并发
- **严重性**: 中（误报风险）
- **问题**: `Promise.all([a(), b()])` 中a和b是并发的，但这是有意为之的设计。
- **修复**: 检测到 `Promise.all` 时跳过该用例的并发检测。
- **影响**: R203

## 陷阱17: beforeEach/afterEach不是beforeAll/afterAll的配对
- **严重性**: 高（误报风险）
- **问题**: Hypium的四个钩子是独立配对的：`beforeAll↔afterAll`，`beforeEach↔afterEach`。有beforeEach不代表有afterAll的需求。
- **修复**: 分别检测两对配对关系，不交叉。
- **影响**: R205

## 陷阱18: 嵌套describe的钩子独立性
- **严重性**: 高（误报风险）
- **问题**: 内层describe的beforeAll不需要外层describe的afterAll配对。每个层级独立检测。
- **修复**: 在每个describe块内独立检测，不跨层级配对。
- **影响**: R204, R205, R206

## 陷阱19: .once()注册的监听器自动移除
- **严重性**: 低
- **问题**: `.once()` 注册的监听器在触发后自动移除，不需要手动 `.off()`。
- **修复**: 排除 `.once()` 注册的监听器。
- **影响**: R204

## 陷阱20: 只读共享变量不算隐式依赖
- **严重性**: 高（误报风险）
- **问题**: 多个用例只读取共享变量但不修改，不存在隐式依赖。
- **修复**: 仅当多个用例**修改**同一共享变量且无beforeEach重置时才报告。
- **影响**: R206

## 陷阱21: expect链式调用中硬编码位置不固定（已移除）
- **严重性**: 高（误报风险）
- **问题**: `expect(result).assertEqual('xxx')` 中硬编码值在第二个参数，但 `expect('xxx').assertEqual(result)` 中在第一个参数。
- **修复**: 跳过所有 `expect(` 开头的行。
- **影响**: R208（已移除）

## 陷阱22: 系统API await不一定在try-catch中
- **严重性**: 中（误报风险）
- **问题**: 某些系统API调用在测试中不需要try-catch（如预期成功的正常流程）。强制要求所有await都包裹try-catch会导致大量误报。
- **修复**: R202采用保守策略——仅报告明显的系统API调用（如delegator、数据库操作等）未包裹try-catch。
- **影响**: R202

## 陷阱23: is_inside_try_block遇到嵌套回调提前返回False
- **严重性**: 极严重（误报风险），实测导致camera模块24个误报
- **问题**: `is_inside_try_block()` 向上回溯时，遇到嵌套回调的 `})` 误判为块退出。例如：
  ```typescript
  try {
    xxx.open().then(() => {   // ← 回调的})
      await xxx.close();   // 向上回溯先遇到 })，误判为不在try中
    });
  } catch (err) { }
  ```
- **修复**: 改用花括号深度追踪。向上逐字符扫描，`})` 使depth先+1后-1不归零，只有独立的 `}` 才使depth归零并检查块退出。
- **修复代码**:
  ```python
  def is_inside_try_block(lines, line_idx):
      depth = 0
      for i in range(line_idx - 1, -1, -1):
          for c in reversed(lines[i]):
              if c == '}': depth += 1
              elif c == '{': depth -= 1
              if depth == 0:
                  s = lines[i].strip()
                  if re.match(r'try\s*\{', s): return True
                  if re.match(r'\}\s*catch', s): return False
                  if re.match(r'\}\s*[;\s]*$', s): return False
      return False
  ```
- **影响**: R202

## 陷阱24: SYSTEM_API_PATTERNS不匹配复合方法名
- **严重性**: 中（漏报风险）
- **问题**: `\.get\s*\(` 不匹配 `.getFileDescriptor(`、`.getAudioEffectMode(`、`.getAVMetadata(` 等复合方法名。实际代码中系统API方法名多为 `动词+名词` 复合形式。
- **修复**: 扩展 `SYSTEM_API_PATTERNS`，使用通用动词模式匹配所有 `await obj.verb()` 调用：
  ```python
  r'\bawait\s+\w+\.(?:get|set|put|delete|query|execute|create|open|close|start|stop|release|read|write|register|unregister|connect|disconnect|send|receive|enable|disable|subscribe|unsubscribe|on|off)\w*\s*\(',
  ```
- **影响**: R202

## 陷阱25: .then()链.catch()检测遇回调内分号提前终止
- **严重性**: 高（误报风险）
- **问题**: 检测 `.then()` 链是否有 `.catch()` 时，如果用逐行检查，遇到 `.then()` 回调内的 `;`（如 `done();`）会误判链已结束。例如：
  ```typescript
  someApi.getData().then(() => {
    done();              // ← 这里的;导致链检测提前终止
  }).catch((err) => {    // ← 实际有.catch()，但被漏检
    console.log(err);
  });
  ```
- **修复**: `.then()` 链的 `.catch()` 检测必须使用**字符级扫描**（非逐行），正确追踪括号深度。从 `.then(` 位置开始向后扫描，遇到 `;` 时仅在括号深度归零时才视为链结束。
- **影响**: R202

## 陷阱26: done()在try-catch外部调用是合法的
- **严重性**: 高（误报风险）
- **问题**: done()在try-catch块之后调用（同层作用域），覆盖所有执行路径，这是合法的done回调模式。
- **修复**: R201的 `check_done_coverage` 必须检查try-catch之后的 `done()`，不能仅检查catch内部。
- **修复代码**:
  ```python
  def check_done_coverage_v2(body):
      # 找到try块的结束位置
      # 检查try_end_line + 1 到 body末尾是否有 done()
      after_try_catch = '\n'.join(lines[try_end_line+1:])
      if re.search(r'\bdone\s*\(\s*\)', after_try_catch):
          return True  # done()在try-catch之后，覆盖所有路径
  ```
- **影响**: R201

## 陷阱27: .then().catch()两边均有done()是合法模式
- **严重性**: 高（误报风险）
- **问题**: `async (done) => { xxx.then(done).catch(done); }` 中，`.then()` 和 `.catch()` 都调用了 `done()`，这是合法的done回调模式，不应被R201报告为"未await的异步操作"。
- **修复**: R201检测到 `async + done` 参数时，`.then()` 链不需要await（因为done回调模式不关心await）。仅当 `async + 无done` 时才检查 `.then()` 是否被await。
- **影响**: R201

## 陷阱28: it()解析器误匹配export function内部代码
- **严重性**: 高（误报风险）
- **问题**: `parse_it_blocks()` 可能将 `export function` 内部的异步代码误识别为 `it()` 块。例如 `export async function getAsset()` 内的 `new Promise(...)` 被误判为it()块内的问题。
- **修复**: `parse_it_blocks()` 必须验证 `it(` 前面没有 `function` 关键字。此外，issue报告时应验证异步操作确实在 `it()` 块的行号范围内。
- **影响**: R201, R202, R004

## 陷阱29: snippet字段填写描述性文本而非真实代码
- **严重性**: 极严重（数据质量问题）
- **问题**: 模型动态生成扫描脚本时，snippet字段被填入了描述性文本而非源文件的真实代码行。例如：
  - `"snippet": "case body contains async operations directly"` — 这是问题类型的描述，不是代码
  - `"snippet": "declares done parameter but never calls done()"` — 这是问题描述，不是代码
  - `"snippet": "try-catch without done() in catch branch"` — 这是判断结论，不是代码
  正确的snippet应该类似于 `"snippet": "it('testFunc', Level.LEVEL0, () => {"` 或 `"snippet": "await pixelMap.release();"`。
- **根因**: 模型在编写issue字典时，将问题描述或判断逻辑直接赋值给了snippet字段，而非回溯到源文件读取对应行的真实代码。
- **修复**: 生成issue时，snippet必须通过以下方式从源文件提取：
  ```python
  # 正确做法：从源文件读取对应行的真实代码
  source_lines = content.split('\n')
  real_line = source_lines[line_number - 1].strip()  # line_number是1-based
  snippet = real_line[:120]  # 截取前120字符
  ```
  如果`line`字段指向it()声明行，snippet就是it()声明的完整代码。如果问题涉及多行，取触发问题的那一行。如果行号对应的是抽象判断（如"该用例整体缺少done"），取it()声明行作为snippet。
- **影响**: 所有29条规则

## 陷阱30: Excel报告问题ID列使用了序号而非规则编号
- **严重性**: 严重（数据质量问题）
- **问题**: 生成Excel报告时，"问题ID"列使用了递增序号（1, 2, 3...）而非规则编号（R001, R201等），导致用户无法从报告中识别问题属于哪条规则。
- **根因**: 报告生成代码使用了 `enumerate(all_issues, 1)` 作为问题ID。
- **修复**: 报告生成时，"问题ID"列直接使用 `issue['rule']` 字段的值：
  ```python
  # 正确做法
  ws1.append([iss.get('rule','-'), iss.get('category','-'), ...])
  
  # 错误做法
  for idx, iss in enumerate(all_issues, 1):
      ws1.append([idx, ...])  # ← 错误：用了序号
  ```
- **影响**: 所有29条规则

## 陷阱31: it()声明跨行时decl_lines范围不足导致async/done参数识别失败
- **严重性**: 极严重（大量误报）
- **问题**: 当it()声明跨多行时（如 `it('name', Level,` 在第一行，`async (done:Function)=> {` 在第二行），解析器设 `start` 为it()匹配行的下一行，但 `decl_lines = lines[start-3:start]` 可能遗漏包含 `async` 和 `done:` 的行，导致 `is_async=False, has_done_param=False`，将合法用例误报为"缺少done回调且未使用async/await"。
- **典型误报场景**:
  ```
  80: it('testFunc', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0,
  81:   async (done:Function)=> {    // ← async和done都在这行
  ```
  解析器匹配第80行，设 `start=81`，`decl_lines = lines[78:81]` 取到第79、80行，**遗漏第81行**的 `async (done:Function)`。
- **根因**: `decl_lines` 向前取3行，但 `async`/`done` 可能在 `start` 行本身（即it()匹配行的下一行），不在取值范围内。
- **修复**: `decl_lines` 必须包含 `start` 行本身：
  ```python
  # 正确做法：包含 start 行（it()匹配行的下一行）
  decl_lines = content.split('\n')[max(0, start - 1):start + 1]
  
  # 错误做法：遗漏 start 行
  decl_lines = content.split('\n')[max(0, start - 3):start]
  ```
- **影响**: R201, R202（所有需要判断is_async/has_done_param的规则）

## 陷阱32: all_paths_have_done在catch块无done时立即return，跳过后续检查
- **严重性**: 极严重（大量误报）
- **问题**: `all_paths_have_done()` 函数在遍历catch块时，发现某个catch块没有 `done()` 就立即 `return False`，导致后续的 `has_done_after_catch` 检查（检查最后一个catch块之后是否有 `done()`）永远不会执行。
- **典型误报场景**: try-catch内部有 `.then(done).catch(done)` 覆盖异步路径，外层 catch 只处理同步异常。函数在第一个无 `done()` 的 catch 处就 return False，但 `done()` 实际上已在 `.then()/.catch()` 链中调用，且所有异步路径都已被覆盖。
- **根因**: 循环内的 `return False` 短路了后续的"catch之后是否有done"检查逻辑。
- **修复**: 循环中用标记变量记录是否有catch缺少done，循环结束后再综合判断：
  ```python
  # 正确做法：循环中标记，循环后综合判断
  catch_missing_done = False
  for cm in catch_matches:
      ...
      if not re.search(r'\bdone\s*\(\s*\)', block_content):
          catch_missing_done = True
          break
  if not catch_missing_done:
      return True
  # 然后检查最后一个catch块之后是否有done()
  last_cm = catch_matches[-1]
  ...
  if re.search(r'\bdone\s*\(\s*\)', after_all_catches):
      return True
  return False
  
  # 错误做法：循环内直接return False
  for cb in catch_blocks:
      ...
      if not re.search(r'\bdone\s*\(\s*\)', block_content):
          return False  # ← 错误：短路了后续检查
  ```
- **影响**: R201

## 陷阱33: 外层catch处理同步异常时无需done（.then/.catch链已覆盖异步路径）
- **严重性**: 高（误报风险）
- **问题**: 当 try 块内包含 `.then(done).catch(done)` 链时，`.then()/.catch()` 已覆盖所有异步路径的done调用。外层 `try-catch` 仅捕获同步异常（如Promise构造前的代码），其 catch 块不需要 `done()`。`all_paths_have_done()` 会报告外层 catch 缺少 done()，但这是合法模式。
- **典型场景**:
  ```typescript
  try {
    await pixelMap5.crop(region).then(() => { done(); }).catch(() => { done(); });
  } catch (err) {        // ← 仅处理crop()同步抛出的异常
    expect().assertFail(); // ← 不需要done()，异步路径已被.then/.catch覆盖
  }
  ```
- **修复**: 在 `all_paths_have_done()` 判定catch块缺少done后，额外检查 try 块内部（catch之前）是否已有 `.then().catch()` 链且两边都有 `done()`。如果是，则外层 catch 无需 done()，不报告：
  ```python
  # 检查try块内部是否已有.then().catch()链且都有done
  has_done_inside_try = bool(re.search(r'\bdone\s*\(\s*\)', body[:last_cm.start()]))
  if has_done_inside_try:
      for tm in re.finditer(r'\.\s*catch\s*\(', body[:last_cm.start()]):
          before = body[max(0, tm.start()-200):tm.start()]
          if re.search(r'\.\s*then\s*\(', before):
               return True  # .then().catch()链已覆盖异步路径
  ```
- **影响**: R201

## 陷阱34: is_inside_try_block使用花括号深度追踪，对象字面量和回调闭包干扰
- **严重性**: 极严重（大量误报，R202历史最高400+误报）
- **问题**: `is_inside_try_block()` 使用花括号深度追踪判断某行是否在try块内，但对象字面量（如 `const opts = { ... };`）的闭合 `};` 会使depth归零，后续的 `{` 使depth变负，导致 `try {` 在depth≠0时被跳过。此外，`.then(() => { ... })` 的回调闭包 `})` 也会干扰深度计数。
- **典型误报场景**:
  ```typescript
  try {
    const dstOpts = { size: { width: 4, height: 6 }, editable: true };  // }; 使depth归零
    await image.createPremultipliedPixelMap(...);  // ✗ 被误报（实际在try内）
  } catch (err) { }
  ```
- **根因**: 花括号深度追踪无法区分代码块 `{}` 和对象字面量 `{}`，因为两者使用相同的字符。
- **修复**: 彻底废弃花括号深度追踪方案，改为基于行号位置匹配：
  ```python
  def is_inside_try_block(lines, line_idx):
      try_starts = []
      try_ends = []
      for i, line in enumerate(lines):
          s = line.strip()
          if re.match(r'try\s*\{', s):
              try_starts.append(i)
          elif re.match(r'\}\s*catch', s):
              try_ends.append(i)
          elif re.match(r'\s*finally\s*\{', s):
              try_ends.append(i)
      for ts in reversed(try_starts):
          if ts >= line_idx:
              continue
          matching_te = None
          for te in try_ends:
              if te > ts:
                  matching_te = te
                  break
          if matching_te is not None and matching_te >= line_idx:
              return True
      return False
  ```
- **影响**: R202（所有使用is_inside_try_block的规则）

---

## 陷阱35: R015 extract_it_declaration 箭头函数 `{` 被跳过

- **问题**: `it("name", Level.LEVEL0, async (done: () => void): Promise<void> => {` 这种跨行 it() 声明中，箭头函数体 `{` 出现时 `paren_depth=1`（`it(` 未闭合），导致 `extract_it_declaration` 的 `paren_depth <= 0` 条件不满足，返回 `None`，Level 参数被误判为缺省
- **根因**: 箭头函数 `=> {` 的 `{` 不是 `it()` 调用的闭合大括号，而是箭头函数体开始。旧逻辑仅用 `paren_depth` 判断声明结束，无法区分这两种 `{`
- **修复**: 在 `extract_it_declaration` 中新增 `saw_arrow` 标志，追踪 `=>` token（等号+大于号连续出现），遇到 `{` 时若 `saw_arrow=True` 也视为声明结束
- **代码**:
  ```python
  saw_arrow = False
  # ... in the char loop:
  elif c == '=' and j + 1 < len(line) and line[j + 1] == '>':
      saw_arrow = True
      j += 2
      continue
  elif c == '{':
      if found_open_paren and (paren_depth <= 0 or saw_arrow):
          return '\n'.join(declaration_lines), idx
      saw_arrow = False
  else:
      if c not in (' ', '\t'):
          saw_arrow = False
  ```
- **验证**: security 子系统 R015 从 751→0（全部为箭头函数 Level 误报），ability 从 181→55（消除 126 项误报）
- **影响**: R015

## 陷阱36: R206 `_find_shared_variables` 初始大括号深度未扣除（极严重，100%漏检describe级共享变量）

- **严重性**: 极严重，导致R206 Dyn模式describe级共享变量100%漏检
- **问题**: `_find_shared_variables(desc_body)` 通过 `in_block` 花括号深度追踪判断是否在it()/function等块内，仅当 `in_block <= 0` 时才识别 `let`/`var` 声明为共享变量。但 `desc_body` 的第一行是 `describe('name', () => {`，其 `{` 使 `in_block` 从0变为1，导致后续所有行的 `in_block` 始终 > 0，**永远无法达到 `in_block <= 0`**。结果：describe块内声明的所有共享变量（如 `let result = 0;`）都无法被识别。
- **根因**: `in_block` 从0开始计数，但describe块的opening brace在desc_body第一行，立即将in_block推到1。变量检测条件 `in_block <= 0` 在describe块内部永远不满足。
- **影响范围**: 2026-04-23 arkui扫描中R206从0420_new的968→19（仅剩文件级共享变量，describe级全部漏检）。0420_new的968个问题大部分是将it()内部的局部变量（如 `let result = xxx()` 在it()体内声明）误判为共享变量的假阳性，但确实存在describe级共享变量被漏检的情况。
- **修复**: 在首次检测到 `in_block > 0` 时将其重置为0（扣除describe块的opening brace）：
  ```python
  def _find_shared_variables(desc_body):
      shared_vars = set()
      lines = desc_body.split('\n')
      if not lines:
          return shared_vars
      in_block = 0
      block_keywords = re.compile(r'\b(?:it|beforeAll|beforeEach|afterAll|afterEach|describe|function)\s*\(')
      initial_depth_set = False
      for line in lines:
          stripped = line.strip()
          brace_delta = _count_braces_outside_strings(stripped)
          if block_keywords.search(stripped):
              in_block += brace_delta
          else:
              in_block += brace_delta
          if not initial_depth_set and in_block > 0:
              in_block = 0
              initial_depth_set = True
          if in_block <= 0:
              in_block = 0
              m = re.match(r'(?:let|var)\s+(\w+)', stripped)
              if m:
                  shared_vars.add(m.group(1))
      return shared_vars
  ```
- **验证**: describe内 `let result = 0;` 现在正确识别为共享变量。嵌套describe内变量不会被误识别为外层共享变量。
- **影响**: R206

## 陷阱37: R018 0420_new的跨文件工程级检测是超范围误检

- **严重性**: 高（误检风险）
- **问题**: R018规则定义为"同一describe下不允许testcase重复"，检测范围是**同一文件内同一describe块**。0420_new版本的扫描器额外实现了跨文件工程级检测（如 `setKeyProcessingMode001` 在两个不同文件中各出现一次），报告了2583个问题。但根据规则定义，跨文件重复不属于R018的检测范围。
- **根因**: 0420_new版本的R018扫描器将"工程内唯一"误解为R018的检测范围。实际上R018仅检查同一文件同一describe块内的重复，跨文件重复由测试框架的执行器自行处理。
- **正确行为**: 0423报告R018=0是正确的——所有跨文件重复都不在R018检测范围内。
- **影响**: R018

- **严重性**: 极严重（误报风险），0420_new报告R008有313951个问题，0423修正后仅1230个
- **问题**: 0420_new版本的R008扫描器将所有包含`@tc.xxx`注解行的JSDoc注释都标记为问题，即使参数和值之间使用的是正确的空格分隔（如 `@tc.name   ArkUiDialogDismissBackPress`）。扫描器误将"冒号或其他分隔符"作为检测条件，实际上正确使用空格分隔的注解也被标记。
- **根因**: 0420_new版本的R008检测逻辑过于宽泛，未精确区分冒号分隔和空格分隔。
- **修复**: 0423版本已修正。R008的 `_COLON_SEP_RE` 精确匹配 `@(tc\.\w+)\s*:\s` 模式（冒号后跟空格），仅当注解确实使用了冒号分隔符时才报告。
- **验证**: 0423 arkui报告R008=1230（1026个冒号分隔 + 187个星号开头 + 16个空行 + 1个注释结尾），无空格分隔误报。
- **影响**: R008

## 陷阱15: snippet字段使用描述性文本而非真实代码行
- **严重性**: 严重，违反报告格式规范
- **问题**: 当issue无法精确定位到某一行代码时（如R206全局状态共享、R017 syscap.json能力统计、R013连续注释块），扫描器可能将问题描述（如"变量TAG在13个用例中被修改"）填入snippet字段。snippet字段规范要求必须填写**源文件中的真实代码行**。
- **根因**: 工程级检测规则（R019/R020/R206）和统计类规则（R017）在无法精确定位单行代码时，倾向于用描述文本填充snippet。wrapper追踪规则（R202）会在snippet前添加"封装函数xxx（同文件）内部:"前缀。
- **修复原则**:
  1. snippet必须始终填写真实代码行：`content.split('\n')[line_number - 1][:120]`
  2. 如果无法定位到具体行号，使用该issue关联的**第一条证据代码行**
  3. 描述性信息（变量名、用例数量、封装函数名等）应放入suggestion字段
  4. wrapper追踪的snippet不应包含"封装函数xxx内部:"前缀
- **已知修复**: R013/R017/R202/R206已修复
- **影响**: R013, R017, R202, R206

## 陷阱16: subsystem映射表路径不匹配
- **严重性**: 中等，导致Excel"所属子系统"列为空
- **问题**: `get_subsystem()`使用前缀匹配，但映射表的key是相对于`xts_acts/`的完整路径（如`ability/ability_runtime`）。当扫描根目录是子系统目录（如`xts_acts/ability`）时，文件相对路径是`ability_runtime/xxx`，首级目录`ability_runtime`无法匹配映射表key `ability/ability_runtime`。
- **修复**: `get_subsystem()`增加首级目录尾部匹配：提取路径首级目录名，在映射表key中查找以该目录名结尾的key。如果匹配到唯一结果，返回对应子系统。
```python
_DIR_SUFFIX_MAP = {}
for _d, _s in SUBSYSTEM_MAPPING.items():
    _suffix = _d.split('/')[-1] if '/' in _d else None
    if _suffix:
        _DIR_SUFFIX_MAP.setdefault(_suffix, []).append((_d, _s))

def get_subsystem(file_path):
    fp = file_path.replace("\\", "/")
    for d in SORTED_DIRS:
        if fp.startswith(d + "/"):
            return SUBSYSTEM_MAPPING[d]
    first_dir = fp.split('/')[0] if '/' in fp else None
    if first_dir and first_dir in _DIR_SUFFIX_MAP:
        entries = _DIR_SUFFIX_MAP[first_dir]
        if len(entries) == 1:
            return entries[0][1]
    return "-"
```
- **注意**: 首级目录名在映射表中不唯一时不匹配（如`wifi_p10p`可能属于多个映射），仅唯一匹配时才生效。
- **影响**: 所有规则的subsystem字段

## 陷阱39: async+done混用模式下.then()不误报
- **严重性**: 高（误报风险）
- **问题**: `it('name', level, async (done: Function) => { someApi().then(data => { done(); }) })` 模式中，虽然存在`.then()`链式调用，但done参数在回调中正确调用时，测试是安全的。如果检测此类问题会导致大量误报（特别是JavaScript文件）。
- **触发条件**: 
  1. 用例声明为 `async (done: Function)` 或 `async function (done)`
  2. 用例体内存在 `.then()` 调用
  3. done在回调中被调用
- **典型代码**:
```typescript
// 合法的混用模式
it('testAsync', Level.LEVEL0, async (done: Function) => {
    someApi().then(data => {
        expect(data).assertEqual('expected');
        done();  // done在回调中正确调用
    });
});
```
- **修复**: 当检测到 `is_async and has_done_param` 时，直接跳过检测（`pass`），不报告`.then()`链式调用问题。原因：
  1. done参数声明表明测试框架已识别此用例为异步
  2. 框架会等待done()调用
  3. `.then()`回调内的done()调用是合法的测试完成信号
- **JavaScript特殊处理**: JavaScript文件的done参数声明模式为 `async function (done)`，检测正则 `\bdone\s*(?:\(\s*\)|:|\b)` 可兼容TS类型注解和JS无类型注解。
- **影响**: R201
