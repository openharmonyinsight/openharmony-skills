# XTS测试代码质量检查 - 编码规范合规规则详情

本文档包含23条编码规范合规规则（R001-R023）的核心信息，包括问题描述、检测模式、正反例、关键陷阱。

**规则分类**：检测代码写没写对、符不符合编码规范

---

## R001 - 禁止使用getSync系统接口

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
多设备XTS适配禁止使用任何形式的`getSync()`系统接口。`getSync()`是同步阻塞调用，在多设备测试场景中会导致死锁或超时问题。

**注意**: 本规则只针对**系统参数模块**的`getSync()`调用（如`@ohos.systemparameter`），不针对应用API的`getSync()`（如`mPreference.getSync()`）。

### 检测模式
```python
# 先检测import
import_patterns = [
    r'import\s+.*\s+from\s+[\'"]@ohos\.systemparameter[\'"]',
    r'import\s+.*\s+from\s+[\'"]@ohos\.systemParameterEnhance[\'"]',
    r'import\s+.*\{.*systemParameter.*\}\s+from\s+[\'"]@kit\.BasicServicesKit[\'"]',
]

# 再检测getSync调用
getsync_pattern = r'(\w+)\.getSync\s*\('
```

### 反例
```typescript
import parameter from '@ohos.systemparameter';
let value = parameter.getSync('key');  // ✗ 使用了getSync系统接口
```

### 正例
```typescript
import { BusinessError } from '@kit.BasicServicesKit';
let value = await parameter.get('key');  // ✓ 使用异步API替代

// 或使用canIUs
if (canIUse("SystemCapability.xxx")) {
    // 基于能力的判断
}
```

### 关键陷阱
1. **必须扫描所有源代码文件**，不仅是测试文件（会导致约81个问题漏报）
2. **模块名大小写不匹配**：需同时覆盖`@ohos.systemparameter`（小写p）和`@ohos.systemParameterEnhance`（大写P），否则漏检约70条
3. **必须同时处理named import和default import**：只处理named import会漏检约41条

---

## R002 - 错误码断言必须是number类型

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
`error.code`的类型为`number`，但测试代码中经常使用**string字面量**对其进行断言或比较。这属于类型不匹配的低级错误。

### 检测模式
```python
# 模式1: assertEqual中的string字面量
r'expect\s*\(\s*\w+\.code\s*\)\s*\.\s*assertEqual\s*\(\s*[\'"](\d+)[\'"]'

# 模式2: expect中的string参数
r'expect\s*\(\s*\w+\.code\s*,\s*[\'"]'

# 模式3: assertTrue中的string比较
r'expect\s*\(\s*\w+\.code\s*===?\s*[\'"]'

# 模式4: if条件中的string比较
r'if\s*\(\s*\w+\.code\s*===?\s*[\'"]'
```

### 反例
```typescript
expect(error.code).assertEqual("401");  // ✗ string类型
expect(error.code === '14000011').assertTrue();  // ✗ string比较
if (error.code == "801") { ... }  // ✗ string比较
```

### 正例
```typescript
expect(error.code).assertEqual(401);  // ✓ number类型
expect(error.code === 14000011).assertTrue();  // ✓ number比较
if (error.code == 801) { ... }  // ✓ number比较
```

### 关键陷阱
1. **不要误报console.log中的用法**：日志输出不是断言
2. **不要误报非纯数字的string字面量**：如`"PARAM_ERROR"`不是错误码
3. **catch变量别名追踪**：`catch(err)`中的`err.code`应检测，但其他位置的`err.code`不应报告

### ArkTS-Sta 适用性

> **本规则不适用于 ArkTS-Sta（静态语法）项目**。Sta 编译器严格类型检查会拒绝 `error.code === "401"`（number vs string）和 `expect(error.code).assertEqual("401")` 为编译错误，代码无法编译通过。如果 Sta 项目代码能编译通过，则不存在本规则描述的问题。

---

## R003 - 禁止恒真断言

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
测试用例中使用`expect(true).assertTrue()`等恒真断言，断言只会产生成功结果，用例恒通过。此类断言未对接口实际返回值进行断言校验，相当于没有任何有效断言。

### 检测模式（必须覆盖全部3种）
```python
r003_patterns = [
    # 模式1: expect(true).assertTrue()（最常见，~96.7%）
    r'expect\s*\(\s*true\s*\)\s*\.\s*assertTrue\s*\(',
    
    # 模式2: expect(true).assertEqual(true)（易遗漏，~3.3%，约128个）
    r'expect\s*\(\s*true\s*\)\s*\.\s*assertEqual\s*\(\s*true\s*\)',
    
    # 模式3: expect(false).assertFalse()（罕见，~0.0%）
    r'expect\s*\(\s*false\s*\)\s*\.\s*assertFalse\s*\(',
]
```

### 反例
```typescript
expect(true).assertTrue();  // ✗ 恒真断言
expect(true).assertEqual(true);  // ✗ 恒真断言（易遗漏）
expect(false).assertFalse();  // ✗ 恒真断言
```

### 正例
```typescript
let actualValue = someFunction();
expect(actualValue).assertTrue();  // ✓ 断言实际值
expect(actualValue).assertEqual('expected');  // ✓ 断言具体期望值
expect(count).assertLargerOrEqual(800);  // ✓ 断言count >= 800
```

### 关键陷阱
**必须覆盖模式2**：`expect(true).assertEqual(true)`占3.3%（128个），遗漏会导致约2014个文件的问题被完全忽略。

---

## R004 - 测试用例缺少断言

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

> **说明**: R004需要追踪跨文件的断言封装函数，因此必须扫描所有源文件，而非仅测试文件。

### 问题描述
测试用例（`it()`）中完全没有断言。断言是测试用例的核心，用于验证被测功能是否符合预期。没有断言的测试用例无法验证任何功能，等同于无效测试。

### Hypium框架支持的断言方法
```
assertClose, assertContain, assertEqual, assertFail, assertFalse, assertTrue,
assertInstanceOf, assertLarger, assertLess, assertLargerOrEqual, assertLessOrEqual,
assertNull, assertThrowError, assertUndefined, assertNaN, assertNegUnlimited,
assertPosUnlimited, assertDeepEquals, expect(...).assert*
```

### 反例
```typescript
it('test001', Level.LEVEL0, () => {
    let result = someFunction();
    console.log(result);  // ✗ 无断言
});
```

### 正例
```typescript
it('test001', Level.LEVEL0, () => {
    let result = someFunction();
    expect(result).assertEqual('expected');  // ✓ 有断言
});
```

### 关键陷阱
1. **间接断言检测**：需递归追踪wrapper函数，最大深度5层
2. **try-catch断言检测**：两个分支都必须有断言
3. **字符串感知的大括号匹配**：模板字符串中的`{}`不应被计入

---

## R005 - 组件尺寸使用固定值

**严重级别**: Warning  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
UI组件的width/height属性使用了固定像素值，导致多设备上页面适用性差，引起XTS适配问题。应使用百分比方式实现自适应布局。

### 检测模式
```python
# 数值参数形式: .width(100), .height(50)
numeric_pattern = r'\.(width|height)\s*\(\s*\d+\s*\)'

# 字符串参数形式: .width('100px'), .height("200vp")
string_pattern = r'\.(width|height)\s*\(\s*['"]\s*\d+\s*(?:px|vp|fp|lpx)?\s*['"]\s*\)'
```

### 反例
```typescript
.width(100)  // ✗ 固定像素值
.height('50px')  // ✗ 固定像素值
```

### 正例
```typescript
.width('50%')  // ✓ 百分比
.height('100%')  // ✓ 百分比
.width(widthValue)  // ✓ 变量引用
```

### 关键陷阱
**必须扫描所有源代码文件**，不是测试文件！仅扫描`.test.ets`会漏报47226个问题。

---

## R006 - 禁止基于设备类型差异化

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

> **说明**: R006检测所有源文件中的deviceInfo.deviceType使用，避免设备类型差异化判断。

### 问题描述
在条件判断中使用`deviceInfo.deviceType`或从其赋值的变量进行设备类型判断，导致XTS测试无法在所有设备上正确执行。应使用`SystemCapability`和`canIUse`进行能力判断。

### 检测模式
```python
# 直接使用
r'\bdeviceInfo\.deviceType\b'

# 条件上下文
r'(if\s*\(|else\s*if\s*\(|switch\s*\(|case\s+|\?\s*|&&|\|\||==|!=|\breturn\b)'
```

### 反例
```typescript
if (deviceInfo.deviceType === 'phone') {  // ✗ 基于设备类型差异化
    // ...
}
```

### 正例
```typescript
if (canIUse("SystemCapability.xxx")) {  // ✓ 基于能力判断
    // ...
}
```

### 关键陷阱
**必须扫描所有源代码文件**，不是测试文件。

---

## R007 - Test.json禁止配置项

**严重级别**: Critical  
**扫描范围**: Test.json文件

### 问题描述
Test.json配置文件中存在禁止的配置项：
- `setenforce 0` — 会关闭SELinux，引入安全问题
- `rerun: true` — 会导致测试报告出现异常
- `appfreeze.filter_bundle_name` — 会屏蔽appfreeze异常

### 检测模式
```python
# setenforce 0
'setenforce 0' in line

# rerun配置
r'"rerun"\s*:\s*(true|1|"true"|"ture")'

# appfreeze.filter_bundle_name
'appfreeze.filter_bundle_name' in line
```

### 反例
```json
{
    "setenforce": "0",  // ✗ 禁止配置
    "rerun": true,  // ✗ 禁止配置
    "appfreeze.filter_bundle_name": "xxx"  // ✗ 禁止配置
}
```

### 正例
```json
{
    // 不包含上述禁止配置项
}
```

---

## R008 - 用例声明格式不规范

**严重级别**: Warning  
**扫描范围**: 测试文件（.test.ets, .test.ts, .test.js）

### 问题描述
测试用例的文档注释格式不符合规范要求，包括缺少注释标记、分隔符错误、空行等问题。

### 规范要求
1. 文档注释以`/**`开头，以`*/`结尾，每行以`*`开始
2. 参数名以`@`修饰，参数名和参数值以**空格**分隔，禁止使用其他分隔符（如冒号）
3. 文档注释结束行的下一行应紧接要修饰的测试用例，禁止出现空行

### 反例
```typescript
/**
 * @tc.number:SUB_XXX_0100  // ✗ 使用冒号分隔
 * @tc.name:testFunc
 */
// 空行  // ✗ 注释和it()之间有空行
it('testFunc', ...)
```

### 正例
```typescript
/**
 * @tc.number SUB_XXX_0100  // ✓ 使用空格分隔
 * @tc.name testFunc
 */
it('testFunc', ...)  // ✓ 紧接it()，无空行
```

---

## R009 - @tc.number命名不规范

**严重级别**: Warning  
**扫描范围**: 测试文件（.test.ets, .test.ts, .test.js）

### 问题描述
`@tc.number`的命名不符合`SUB_{子系统}_{部件}_XXXX`格式要求。

### 命名规范
```
SUB_{子系统}_{部件}_[XX?]_XXXX
```
- `SUB_` — 固定前缀
- `{子系统}` — 子系统名称，使用大写字母（如`APPEXECFWK`、`ARKUI`）
- `{部件}` — 部件名称，使用大写字母
- `[XX?]` — 可选的中间标识段（如`SDK`、`HAG`）
- `XXXX` — 4位阿拉伯数字，递增以100为单位

### 反例
```typescript
@tc.number SUB_ArkUI_Button_001  // ✗ 子系统不是大写
@tc.number SUB_ARKUI_BUTTON_001  // ✗ 数字不以100为单位
```

### 正例
```typescript
@tc.number SUB_APPEXECFWK_BUNDLEMGR_SDK_HAG_0100  // ✓ 符合规范
@tc.number SUB_ARKUI_BUTTON_0100  // ✓ 符合规范
```

---

## R010 - part_name/subsystem_name不匹配

**严重级别**: Critical  
**扫描范围**: BUILD.gn文件

### 问题描述
BUILD.gn中声明的`part_name`必须在对应`subsystem_name`的components列表中存在。

### 检测模式
```python
# 提取part_name和subsystem_name
r'part_name\s*=\s*["\']([^"\']+)["\']'
r'subsystem_name\s*=\s*["\']([^"\']+)["\']'

# 验证映射关系
part_name in subsystem_map[subsystem_name]
```

### 反例
```python
part_name = "button"  # ✗ 该部件不属于subsystem_name
subsystem_name = "graphic"
```

### 正例
```python
part_name = "button"  # ✓ button属于arkui子系统
subsystem_name = "arkui"
```

### 关键陷阱
**需从远程仓库获取映射表**：三个配置文件URL必须同时覆盖。如果URL不可达，需明确告警，不可静默返回0个问题。

---

## R011 - testsuite重复

**严重级别**: Critical  
**扫描范围**: 同一独立XTS工程内的所有测试文件

### 问题描述
一个独立XTS工程下不允许describe命名重复。即同一个独立XTS工程中，所有测试文件里的`describe()`函数的第一个参数不能重复。

### 检测模式
```python
# 提取describe名称
r"describe\s*\(\s*['\"]([^'\"]+)['\"]"

# 工程内去重
工程内describe名称唯一
```

### 反例
```typescript
// 文件A
describe('ButtonTest', ...)  // ✗ testsuite重复

// 文件B（同一工程）
describe('ButtonTest', ...)  // ✗ 与文件A重复
```

### 正例
```typescript
// 文件A
describe('ButtonTest', ...)

// 文件B（同一工程）
describe('ButtonTestAdapt001', ...)  // ✓ 唯一命名
```

### 关键陷阱
**必须识别独立XTS工程边界**：group类型的BUILD.gn只是聚合入口，不阻止其子目录成为独立工程。

---

## R012 - 签名证书APL等级和app-feature配置错误

**严重级别**: Critical  
**扫描范围**: .p7b签名文件

### 问题描述
签名证书APL等级和app-feature配置错误。

### 检测模式
解析DER二进制格式的.p7b文件，提取APL等级和app-feature信息。

### 关键陷阱
DER二进制解析复杂，需使用专门的解析库。

---

## R013 - 注释的废弃代码

**严重级别**: Warning  
**扫描范围**: 测试文件（.test.ets, .test.ts, .test.js）

### 问题描述
用例代码被注释掉后留在文件中，形成废弃代码。检测连续注释块（≥3行）中包含代码特征的内容。

### 检测逻辑
1. **注释块识别**：连续3行及以上的注释（`//`或`/* */`块）
2. **代码特征检测**：注释文本包含至少2个代码关键字（如function、let、const、return、if、for、expect、it等）
3. **完整函数/模板检测**：包含完整函数定义、测试用例声明或特殊模板注释

### 代码关键字列表
```python
CODE_PATTERNS = [
    'function', 'var', 'let', 'const', 'return', 'if', 'for', 'while',
    'switch', 'case', 'break', 'class', 'import', 'export', 'async',
    'await', 'try', 'catch', 'throw', 'new', 'this', 'expect',
    'it()', 'describe()', '{', '}', ';', '=>'
]
```

### 完整函数模式
```python
COMPLETE_FUNC_PATTERNS = [
    'function xxx(...) {',
    'xxx = (...) => {',
    'it("xxx", ...)',
    'describe("xxx", ...)',
    'class xxx',
    'new xxx',
    'expect(...)',
    'try {',
    'if (...)',
    'for (...)',
    'while (...)',
    'switch (...)',
]
```

### 排除场景
- **License头**：包含Copyright、Apache License等版权信息
- **Javadoc格式**：包含≥2个@标记（@tc.name、@tc.number、@param等）
- **模板注释**：特定模板注释（如"Presets an action"）

### 反例
```typescript
// 连续3行注释包含代码特征
// let sleep = (ms: number): Promise<void> => {  // ✗ 注释的废弃代码
//     return new Promise(resolve => setTimeout(resolve, ms));
// };
```

### 正例
```typescript
// 删除废弃代码，不保留注释
```

### 关键陷阱
1. **必须≥3行连续注释**：单行注释不检测
2. **必须≥2个代码关键字**：避免误报普通说明注释
3. **排除Javadoc和License**：避免误报文档注释

---

## R014 - 测试HAP命名不规范

**严重级别**: Critical  
**扫描范围**: BUILD.gn文件

### 问题描述
测试HAP的`hap_name`属性命名不符合规范。检测三种模板类型的命名：
- `ohos_js_app_suite`: hap_name必须以`Acts`开头，以`Test`结尾
- `ohos_js_app_static_suite`: hap_name必须以`Acts`开头，以`StaticTest`结尾  
- `ohos_moduletest_suite`: target_name必须以`Acts`开头，以`Test`结尾

### 命名规范
**hap_name采用大驼峰方式（PascalCase）**

| 模板类型 | 命名规范 | 正确示例 |
|---------|---------|---------|
| `ohos_js_app_suite` | 以`Acts`开头，以`Test`结尾 | `ActsAbilityTest` |
| `ohos_js_app_static_suite` | 以`Acts`开头，以`StaticTest`结尾 | `ActsAbilityStaticTest` |
| `ohos_moduletest_suite` | target_name以`Acts`开头，以`Test`结尾 | `ActsModuleTest` |

### 检测对象
检测`hap_name`属性值，而非target名称：
```python
ohos_js_app_suite("target_name") {  # target_name保持不变
  hap_name = "ActsHapTest"          # ← 检测此属性值
}
```

### 反例
```python
ohos_js_app_suite("ActsArkUIButtonTest") {
  hap_name = "ActsArkUIButtonTest"  # ✗ 符合规范，无问题
}

ohos_js_app_suite("module_normalized_test") {
  hap_name = "module_normalized_test"  # ✗ 不以Acts开头，不符合规范
}
```

### 正例
```python
ohos_js_app_suite("ActsArkUIButtonTest") {
  hap_name = "ActsArkUIButtonTest"  # ✓ 符合规范
}

ohos_js_app_suite("ActsHapTest") {
  hap_name = "ActsHapTest"  # ✓ 符合规范
}
```

### 特殊情况
- 名称中包含`validator`时跳过检测（验证器模块）
- 空hap_name跳过检测

---

## R015 - Level参数缺省

**严重级别**: Warning  
**扫描范围**: 测试文件（.test.ets, .test.ts, .test.js）

### 问题描述
`it()`调用缺少Level参数。

### 检测模式
```python
# 检测it()签名中缺少Level
r"it\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*(?!Level)"
```

### 反例
```typescript
it('test001', () => {  // ✗ 缺少Level参数
    expect(1).assertEqual(1);
});
```

### 正例
```typescript
it('test001', Level.LEVEL0, () => {  // ✓ 包含Level参数
    expect(1).assertEqual(1);
});
```

---

## R016 - testcase命名规范

**严重级别**: Warning  
**扫描范围**: 测试文件（.test.ets, .test.ts, .test.js）

### 问题描述
`it()`的第一个参数（testcase名称）不符合命名规范。

### 命名规范
- 无特殊字符（如`$`、`#`、`@`）
- 不使用纯数字
- 不与`@tc.name`不一致

### 反例
```typescript
it('test@001', ...)  // ✗ 包含特殊字符
it('123', ...)  // ✗ 纯数字
```

### 正例
```typescript
it('test001', ...)  // ✓ 符合规范
it('SUB_ARKUI_BUTTON_0100', ...)  // ✓ 符合规范
```

---

## R017 - syscap.json配置多个能力

**严重级别**: Critical  
**扫描范围**: syscap.json文件

### 问题描述
syscap.json配置多个能力。

### 检测模式
```python
# 解析syscap.json，检查能力数量
len(syscap_list) > 1
```

### 反例
```json
{
    "system_capabilities": [
        "SystemCapability.xxx",
        "SystemCapability.yyy"  // ✗ 配置多个能力
    ]
}
```

### 正例
```json
{
    "system_capabilities": [
        "SystemCapability.xxx"  // ✓ 仅配置一个能力
    ]
}
```

---

## R018 - testcase重复

**严重级别**: Critical  
**扫描范围**: 同一文件同一describe块内的测试用例

### 问题描述
同一个describe块内，`it()`函数的第一个参数（testcase名称）不能重复。

> **注意**: 本规则只在**同一文件同一describe块内**检测重复，不检测跨文件或跨describe块的重复。

### 检测模式
```python
# 提取it()名称
r"it\s*\(\s*['\"]([^'\"]+)['\"]"

# describe块内去重
同一describe块内it()名称唯一
```

### 反例
```typescript
describe('ButtonTest', () => {
    it('test001', ...)  // ✗ testcase重复（同一describe内）
    it('test001', ...)  // ✗ 与上一行重复（同一describe内）
});
```

### 正例
```typescript
describe('ButtonTest', () => {
    it('test001', ...)  // ✓ 唯一命名
    it('test002', ...)  // ✓ 唯一命名
});

// 跨describe块不检测重复
describe('ButtonTest1', () => {
    it('test001', ...)  // ✓ 不同describe块
});

describe('ButtonTest2', () => {
    it('test001', ...)  // ✓ 不同describe块，不报告
});

// 跨文件不检测重复
// 文件A: describe('Test', () => { it('commonTest', ...) })
// 文件B: describe('Test', () => { it('commonTest', ...) })  // ✓ 不同文件，不报告
```

### 关键陷阱
**只检测同一describe块内**：不同describe块或不同文件中同名testcase不报告，避免误报合理命名的测试用例。

---

## R019 - .key重复

**严重级别**: Critical  
**扫描范围**: 同一独立XTS工程内的pages目录下的文件

> **注意**: 本规则检查pages目录下的.key()重复，而非测试文件。代码实现见`unified_engine.py:427: if '/pages/' in fp`。

### 问题描述
同一个独立XTS工程中，所有`.key()`调用中传入的key值不能重复。

### 检测模式
```python
# 提取.key()值
r'\.key\s*\(\s*['\"]([^'\"]+)['\"]'

# 工程内去重
工程内.key()值唯一
```

### 反例
```typescript
// 文件A
Component().key('buttonKey')  // ✗ key重复

// 文件B（同一工程）
Component().key('buttonKey')  // ✗ 与文件A重复
```

### 正例
```typescript
// 文件A
Component().key('buttonKeyA')

// 文件B（同一工程）
Component().key('buttonKeyB')  // ✓ 唯一key
```

---

## R020 - .id重复

**严重级别**: Critical  
**扫描范围**: 同一独立XTS工程内的pages目录下的文件

> **注意**: 本规则检查pages目录下的.id()重复，而非测试文件。代码实现见`unified_engine.py:427: if '/pages/' in fp`。

### 问题描述
同一个独立XTS工程中，所有`.id()`调用中传入的id值不能重复。

### 检测模式
```python
# 提取.id()值
r'\.id\s*\(\s*['\"]([^'\"]+)['\"]'

# 工程内去重
工程内.id()值唯一
```

### 反例
```typescript
// 文件A
Component().id('buttonId')  // ✗ id重复

// 文件B（同一工程）
Component().id('buttonId')  // ✗ 与文件A重复
```

### 正例
```typescript
// 文件A
Component().id('buttonIdA')

// 文件B（同一工程）
Component().id('buttonIdB')  // ✓ 唯一id
```

---

## R021 - hypium版本号>=1.0.26

**严重级别**: Critical  
**扫描范围**: oh-package.json5文件

### 问题描述
Hypium测试框架版本号必须>=1.0.26。

### 检测模式
```python
# 解析oh-package.json5，提取hypium版本
version >= "1.0.26"
```

### 反例
```json
{
    "dependencies": {
        "@ohos/hypium": "1.0.0"  // ✗ 版本过低
    }
}
```

### 正例
```json
{
    "dependencies": {
        "@ohos/hypium": "1.0.26"  // ✓ 版本符合要求
    }
}
```

---

## R022 - errcode值断言使用宽松比较

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
errcode值断言应使用严格比较（`===`/`!==`），而非宽松比较（`==`/`!=`）。

### 检测模式
```python
# 检测宽松比较
r'error\.code\s*==[^=]'
r'error\.code\s*!=[^=]'
```

### 反例
```typescript
if (error.code == 401) { ... }  // ✗ 使用宽松比较
expect(error.code != 801).assertTrue();  // ✗ 使用宽松比较
```

### 正例
```typescript
if (error.code === 401) { ... }  // ✓ 使用严格比较
expect(error.code !== 801).assertTrue();  // ✓ 使用严格比较
```

### ArkTS-Sta 适用性

> **本规则不适用于 ArkTS-Sta（静态语法）项目**。Sta 编译器严格类型检查会拒绝 `error.code == 401`（`==` 跨类型比较）为编译错误。对同类型（number vs number），`==` 和 `===` 行为完全一致。如果 Sta 项目代码能编译通过，则不存在本规则描述的宽松比较问题。

---

## R023 - 禁止errcode值类型强转后断言

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
禁止对errcode值进行类型强转后断言。

### 检测模式
```python
# 检测类型强转
r'error\.code\s*\.\s*toString\s*\('
r'String\s*\(\s*error\.code'
r'Number\s*\(\s*error\.code'
```

### 反例
```typescript
expect(error.code.toString()).assertEqual("401");  // ✗ 类型强转
expect(String(error.code)).assertEqual("401");  // ✗ 类型强转
```

### 正例
```typescript
expect(error.code).assertEqual(401);  // ✓ 直接断言number类型
```

### ArkTS-Sta 适用性

> **本规则适用于 ArkTS-Sta 项目**。虽然 Sta 禁止 `any` 类型，但 `.toString()` 和 `String()` 方法仍可在 Sta 代码中使用。对 `error.code`（number 类型）调用 `.toString()` 或 `String()` 进行类型强转后断言，属于低级错误，Sta 编译器不会拦截此类逻辑错误。

---
## 规则统计

| 类别 | 规则数 | 规则编号 |
|------|--------|---------|
| **Critical** | 17 | R001-R004,R006-R007,R010-R012,R014,R017-R023 |
| **Warning** | 6 | R005,R008-R009,R013,R015-R016 |

---

## 参考文档

- [references/TRAPS.md](TRAPS.md) - 已知扫描陷阱（44个）
- [references/RULES_TECHNICAL.md](RULES_TECHNICAL.md) - 测试技术问题规则详情（R201-R206）
- [guides/FIX_GUIDE.md](../guides/FIX_GUIDE.md) - 问题修复指南