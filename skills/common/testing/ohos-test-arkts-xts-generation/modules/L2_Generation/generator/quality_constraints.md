# 代码质量约束

> **模块信息**
> - 层级：L2_Generation
> - 子模块：generator/
> - 用途：定义测试代码生成时必须遵循的质量约束
> - 来源：整合自 check-test-code-quality 技能的适用规则 (R002/R003/R004/R008/R009/R013/R015/R016/R018/R022/R023)

---

这些约束是**生成时的硬性要求**，不是可选建议。遵循它们可以确保生成的代码天然通过 check-test-code-quality 的 23 条规则扫描，无需返工修复。每条规则后括号内说明了违反后的具体后果，帮助理解约束的必要性。

---

## 1. 错误码断言使用 number 字面量 (R002)

`error.code` 的类型是 `number`，所有断言和比较必须使用数字字面量。（使用字符串字面量时，`assertEqual` 会因类型不匹配而始终判定不相等，错误码断言永远失败）

```typescript
expect(error.code).assertEqual(5400102);
if (error.code === 801) { ... }
```

```typescript
expect(error.code).assertEqual("5400102");
if (error.code == "801") { ... }
```

---

## 2. 禁止恒真断言 (R003)

以下三种模式没有任何验证价值，永远为真：（恒真断言不验证任何运行时行为，测试永远显示"通过"但实际什么都没测，是无效测试）

- `expect(true).assertTrue()`
- `expect(true).assertEqual(true)`
- `expect(false).assertFalse()`

所有断言必须测试运行时实际值。如果 try 块执行成功且无异常，使用 `expect(result).assertEqual(expected)` 或省略成功断言（catch 块已有断言即可）。

---

## 3. 每个 it() 块必须有断言 (R004)

每个 `it()` 块内必须包含至少一个 `expect()` 调用。如果使用了 try-catch，try 分支和 catch 分支必须各自包含断言。（缺少 expect() 的 it() 块会静默通过，产生"一切正常"的假象，无法发现 API 行为异常）

```typescript
it('test001', ..., async (done) => {
  let result = await someFunction();
  expect(result).assertEqual('expected');
  done();
});
```

```typescript
it('test001', ..., async (done) => {
  let result = await someFunction();
  done();
});
```

---

## 4. @tc 注释块格式完整 (R008)

每个 `it()` 前必须有完整的 JSDoc 注释块：
- 以 `/**` 开头，`*/` 结尾，内部每行以 `*` 开头
- 参数使用 `@` 前缀（如 `@tc.name`），值与参数名之间用空格分隔（不用冒号）
- `*/` 与 `it()` 之间不能有空行
- 必须包含：`@tc.number`、`@tc.name`、`@tc.desc`、`@tc.size`、`@tc.type`、`@tc.level`

```typescript
/**
 * @tc.number SUB_MULTIMEDIA_MEDIA_AVPLAYER_GETLOADEDTIMERANGES_RETURN_001
 * @tc.name getLoadedTimeRangesReturnTest001
 * @tc.desc AVPlayer getLoadedTimeRanges return loaded time ranges test.
 * @tc.size MediumTest
 * @tc.type Function
 * @tc.level Level 3
 * @tc.require
 */
it('getLoadedTimeRangesReturnTest001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, ...
```

---

## 5. @tc.number 命名格式 (R009)

格式：`SUB_{子系统大写}_{模块大写}_{API大写}_{类型}_{4位序号}`

```
SUB_MULTIMEDIA_MEDIA_AVPLAYER_GETLOADEDTIMERANGES_RETURN_0001
SUB_APPEXECFWK_BUNDLEMGR_SDK_HAG_0100
```

```
ArcButtonPosition_001
SUB_appexecfwk_bundlemgr_0100
```

---

## 6. 不生成注释掉的废弃代码 (R013)

不要生成被注释掉的函数、测试用例或代码块。如果某段代码不需要，直接删除，不要注释保留。版本历史由 Git 管理。（注释掉的代码增加文件体积、干扰代码审查、混淆读者对活跃代码的判断，且版本追溯应交给 Git 而非注释）

---

## 7. it() 第二参数必须包含 Level 枚举 (R015)

`it()` 的第二个参数必须包含 `Level.LEVEL*`，不能省略。（Hypium 测试运行器依赖 Level 值进行测试分级筛选，省略后该用例无法被正确归类和调度执行）

```typescript
it('testName', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (done) => { ... });
```

```typescript
it('testName', async (done) => { ... });
```

---

## 8. it() 名称仅使用合规字符 (R016)

`it()` 的第一个参数（测试名称）只能包含：`a-z`、`A-Z`、`0-9`、`_`、`-`。

禁止使用：空格、点号、`@`、`#`、中文、括号、冒号、斜杠等。（Hypium 测试发现机制对特殊字符敏感，不合规字符会导致用例注册失败或报告系统解析异常）

```typescript
it('getLoadedTimeRangesReturnTest001', ...)
it('testFunc_API_v2-001', ...)
```

```typescript
it('test.name@001', ...)
it('测试用例001', ...)
```

---

## 9. 同一 describe 内 it() 名称不重复 (R018)

同一个 `describe` 块内，所有 `it()` 的第一个参数必须唯一。不同 describe 块可以重名。（重复名称会导致测试运行器只执行其中一个而静默跳过另一个，掩盖缺失的测试覆盖）

```typescript
describe('Suite', () => {
  it('test001', ...)   // OK
  it('test002', ...)   // OK, unique
});
```

```typescript
describe('Suite', () => {
  it('test001', ...)
  it('test001', ...)   // 重复，禁止
});
```

---

## 10. 错误码比较使用严格相等 (R022)

`.code` 的比较必须使用 `===` 或 `assertEqual`，禁止使用 `==`。（`==` 会进行隐式类型转换，`401 == "401"` 为 true，掩盖了 API 实际返回类型不符的问题）

```typescript
expect(error.code).assertEqual(5400102);
if (err.code === 801) { ... }
```

```typescript
expect(err.code == 0).assertTrue();
if (error.code == 801) { ... }
```

注意：使用 `expect(error.code).assertEqual(401)` 是推荐方式，因为 `assertEqual` 本身就是严格相等。

---

## 11. 禁止 errcode 类型强转 (R023)

禁止对 `.code` 使用 `Number()` 等类型强转。`.code` 本身就是 `number` 类型，如果 API 返回了非 number 类型，应提 bug 而非在测试中强转。（强转掩盖了 API 返回类型与声明不一致的缺陷，使 bug 无法被发现和修复）

```typescript
expect(error.code).assertEqual(401);
```

```typescript
expect(Number(err.code)).assertEqual(401);
expect(Number(error.code) === 401).assertTrue();
```

---

## 12. catch 块必须有断言 (R024)

try-catch 结构中，**catch 块必须包含至少一个 `expect()` 调用**。空 catch 块或只有 `console.log` 的 catch 块会吞掉异常，导致测试无效。（空 catch 块使异常被静默吞掉，无论 API 抛出什么错误测试都显示"通过"，形成无效测试）

```typescript
try {
  api.method(invalidParam);
  expect().assertFail();
} catch (error) {
  expect(error.code).assertEqual(401);
}
```

```typescript
// ❌ 空 catch 块
try {
  api.method(invalidParam);
  expect().assertFail();
} catch (error) {
  // 吞掉异常
}

// ❌ catch 块只有 console.log
try {
  api.method(invalidParam);
  expect().assertFail();
} catch (error) {
  console.log('error: ' + error);  // 不是断言
}
```

---

## 13. 禁止裸 expect() 无断言方法 (R025)

调用 `expect(value)` 后必须链式调用 `.assertXxx()` 断言方法。裸 `expect()` 不执行任何验证。（裸 expect() 调用不会触发任何断言逻辑，测试看起来有验证但实际上什么都没检查）

```typescript
expect(result).assertEqual(expected);
expect(error.code).assertEqual(401);
```

```typescript
// ❌ expect 后没有链式断言
expect(result);  // 什么都没验证
```

---

## 14. 禁止 console.log 代替断言 (R026)

`console.log` 不能代替 `expect()` 断言。日志仅用于辅助调试，不构成测试验证。（日志输出不会被测试框架判定为通过/失败，只打印日志的测试无法验证 API 行为的正确性）

```typescript
let result = api.method();
expect(result).assertEqual(expected);
console.info(TAG + ' method returned: ' + result);  // 辅助日志，OK
```

```typescript
let result = api.method();
console.log('result is: ' + result);  // ❌ 用日志代替断言
```

---

## 15. 禁止未使用的导入 (R027)

导入但未使用的符号应删除。`format_validator.md` 3.3 节会检查此项。（未使用的导入增加编译时间和产物体积，且在代码审查时造成困惑）

```typescript
import { describe, it, expect, Level } from '@ohos/hypium';
```

```typescript
// ❌ 导入了未使用的符号
import { describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level } from '@ohos/hypium';
// beforeAll、afterEach、TestType、Size 未使用
```

---

## 16. describe 嵌套不超过 2 层 (R028)

`describe` 嵌套层级不超过 2 层（`export default function` 内的 `describe` 算第 1 层，其内的 `describe` 算第 2 层）。过度嵌套导致文件过长、测试报告难以阅读。

```typescript
export default function APITest() {
  describe('APIParameterTest', () => {
    it('test001', Level.LEVEL1, () => { ... });
  });
  describe('APIErrorCodeTest', () => {
    it('testError001', Level.LEVEL2, () => { ... });
  });
}
```

```typescript
// ❌ 4 层嵌套
export default function APITest() {
  describe('APIParameterTest', () => {
    describe('StringParamTest', () => {
      describe('NormalValueTest', () => {
        describe('ShortStringTest', () => {
          it('test001', Level.LEVEL1, () => { ... });
        });
      });
    });
  });
}
```

---

## 17. @tc.level 与 it() Level 必须一致 (R029)

`@tc` 注释块中的 `@tc.level` 必须与 `it()` 第二参数中的 `Level.*` 枚举值一致。（不一致会导致测试报告中的等级信息与实际执行等级矛盾，影响测试结果归档和分级统计的准确性）

```typescript
/**
 * @tc.level LEVEL3
 */
it('test001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => { ... });
```

```typescript
// ❌ @tc.level 和 it() Level 不匹配
/**
 * @tc.level LEVEL3
 */
it('test001', Level.LEVEL2, () => { ... });
```
