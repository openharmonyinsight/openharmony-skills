# 代码质量约束

> **模块信息**
> - 层级：L2_Generation
> - 子模块：generator/
> - 用途：定义测试代码生成时必须遵循的质量约束
> - 来源：整合自 ohos-test-xts-code-quality 技能的适用规则 (R002-R023 合规 + R201-R205 技术)

---

这些约束是**生成时的硬性要求**，不是可选建议。遵循它们可以确保生成的代码天然通过 ohos-test-xts-code-quality 的 29 条规则扫描，无需返工修复。每条规则后括号内说明了违反后的具体后果。代码块中 `// ✅️` 标记正确写法，`// ❌` 标记违规写法，反例仅标记当前规则的违规点，其他字段仍保持正确。

---

## 1. 错误码断言使用 number 字面量 (R002)

`error.code` 的类型是 `number`，所有断言和比较必须使用数字字面量。（使用字符串字面量时，`assertEqual` 会因类型不匹配而始终判定不相等，错误码断言永远失败）

```typescript
// ✅️ number 类型断言
expect(error.code).assertEqual(5400102);
if (error.code === 801) { ... }
```

```typescript
// ❌ string 类型断言
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
// ✅️ it() 内有断言
it('test001', ..., async (done: () => void) => {
  let result = await someFunction();
  expect(result).assertEqual('expected');
  done();
});
```

```typescript
// ❌ it() 内无断言
it('test001', ..., async (done: () => void) => {
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
 * @tc.number SUB_MULTIMEDIA_MEDIA_AVPLAYER_GETLOADEDTIMERANGES_RETURN_0100
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

**注意**：序号必须从 `0100` 开始递增（`0100`, `0200`, `0300` ...），中间的编号（如 `0101`）预留给未来补充用例使用。

```
// ✅️ 符合命名格式
SUB_MULTIMEDIA_MEDIA_AVPLAYER_GETLOADEDTIMERANGES_RETURN_0100
SUB_APPEXECFWK_BUNDLEMGR_SDK_HAG_0100
```

```
// ❌ 不符合命名格式
ArcButtonPosition_0100
SUB_appexecfwk_bundlemgr_0100
SUB_APPEXECFWK_BUNDLEMGR_SDK_HAG_100
SUB_MULTIMEDIA_MEDIA_AVPLAYER_GETLOADEDTIMERANGES_RETURN_0100
```

---

## 6. 不生成注释掉的废弃代码 (R013)

不要生成被注释掉的函数、测试用例或代码块。如果某段代码不需要，直接删除，不要注释保留。版本历史由 Git 管理。（注释掉的代码增加文件体积、干扰代码审查、混淆读者对活跃代码的判断，且版本追溯应交给 Git 而非注释）

---

## 7. it() 第二参数必须包含 Level 枚举 (R015)

`it()` 的第二个参数必须包含 `Level.LEVEL*`，不能省略。（Hypium 测试运行器依赖 Level 值进行测试分级筛选，省略后该用例无法被正确归类和调度执行）

```typescript
// ✅️ 包含完整 Level 标志
it('testName', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (done: () => void) => { ... });
```

```typescript
// ❌ 缺少 Level 标志
it('testName', async (done: () => void) => { ... });
```

---

## 8. it() 名称仅使用合规字符 (R016)

`it()` 的第一个参数（测试名称）只能包含：`a-z`、`A-Z`、`0-9`、`_`、`-`。

禁止使用：空格、点号、`@`、`#`、中文、括号、冒号、斜杠等。（Hypium 测试发现机制对特殊字符敏感，不合规字符会导致用例注册失败或报告系统解析异常）

```typescript
// ✅️ 仅使用合规字符（a-z A-Z 0-9 _ -）
it('getLoadedTimeRangesReturnTest001', ...)
it('testFunc_API_v2-001', ...)
```

```typescript
// ❌ 包含特殊字符
it('test.name@001', ...)
it('测试用例001', ...)
```

---

## 9. 同一 describe 内 it() 名称不重复 (R018)

同一个 `describe` 块内，所有 `it()` 的第一个参数必须唯一。不同 describe 块可以重名。（重复名称会导致测试运行器只执行其中一个而静默跳过另一个，掩盖缺失的测试覆盖）

```typescript
// ✅️ describe 内名称唯一
describe('Suite', () => {
  it('test001', ...)
  it('test002', ...)
});
```

```typescript
// ❌ describe 内名称重复
describe('Suite', () => {
  it('test001', ...)
  it('test001', ...)   // 重复
});
```

---

## 10. 错误码断言禁止使用比较运算符 (R022)

`.code` 的断言和比较必须使用 `===`/`!==` 或 `assertEqual`，禁止使用所有比较运算符（`==`、`!=`、`>`、`<`、`>=`、`<=`）构造断言。

**说明**：`==`/`!=` 是松散等值比较，会隐式类型转换（`401 == "401"` 为 true）。`>`/`<`/`>=`/`<=` 是关系比较，不属于精确值断言——errcode 断言应精确匹配具体错误码值，而非比较大小范围。如需判断"是否有错误"，使用 `expect(error.code).assertEqual(expectedCode)` 或 `if (error.code === expectedCode)`。

```typescript
// ✅️ 严格相等或 assertEqual
expect(error.code).assertEqual(5400102);
if (error.code === 801) { ... }
```

```typescript
// ❌ 松散等值比较（== 会隐式类型转换，number == string 恒为 true）
if (error.code == "801") { ... }
expect(error.code == 401).assertTrue();  // 即使两侧同为 number，也应使用 ===
```

---

## 11. 禁止 errcode 类型强转 (R023)

禁止对 `.code` 使用 `Number()` 等类型强转。`.code` 本身就是 `number` 类型，如果 API 返回了非 number 类型，应提 bug 而非在测试中强转。（强转掩盖了 API 返回类型与声明不一致的缺陷，使 bug 无法被发现和修复）

```typescript
// ✅️ 直接断言 number
expect(error.code).assertEqual(401);
```

```typescript
// ❌ 类型强转
expect(Number(err.code)).assertEqual(401);
expect(Number(error.code) === 401).assertTrue();
```

---

## 12. catch 块必须有断言 (R024)

try-catch 结构中，**catch 块必须包含至少一个 `expect()` 调用**。空 catch 块或只有 `console.log` 的 catch 块会吞掉异常，导致测试无效。（空 catch 块使异常被静默吞掉，无论 API 抛出什么错误测试都显示"通过"，形成无效测试）

```typescript
// ✅️ catch 块有断言
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
// ✅️ expect 后链式调用断言方法
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
// ✅️ expect 断言 + console.info 辅助日志
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
// ✅️ 仅导入使用的符号
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
// ✅️ 2 层嵌套
export default function APITest() {
  describe('APIParameterTest', () => {
    it('test001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => { ... });
  });
  describe('APIErrorCodeTest', () => {
    it('testError001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, () => { ... });
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
          it('test001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => { ... });
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
// ✅️ @tc.level 与 it() Level 一致
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
it('test001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, () => { ... });
```

---

## 18. 异步用例必须正确处理 done/await (R201)

异步 `it()` 回调如果接收 `done` 参数，必须在所有异步操作完成后调用 `done()`；如果使用 `async/await`，则不能声明 `done` 参数。禁止既声明 `done` 又使用 `async` 却不调用 `done()`。（未调用 `done()` 会导致测试超时失败；ArkTS-Sta 工程额外检测 Promise executor 是否声明为 async）

```typescript
// ✅️ done() 在所有异步路径上调用
it('test001', ..., async (done: () => void): Promise<void> => {
  let result = await someFunction();
  expect(result).assertEqual(expected);
  done();
});
```

```typescript
// ❌ 缺少 done() 调用，测试会超时
it('test001', ..., async (done: () => void): Promise<void> => {
  let result = await someFunction();
  expect(result).assertEqual(expected);
});
```

---

## 19. 异步回调/Promise 必须处理错误 (R202)

异步操作中的错误必须通过 try-catch 捕获并在 catch 中断言错误码，或通过 `.catch()` 处理。禁止在异步回调中忽略错误。（未处理的 Promise rejection 会导致测试进程崩溃；ArkTS-Sta 工程额外检测 reject 是否传入非 Error 类型）

```typescript
// ✅️ try-catch 处理错误
try {
  let result = await api.asyncMethod();
  expect(result).assertEqual(expected);
} catch (error) {
  expect(error.code).assertEqual(401);
}
```

```typescript
// ❌ Promise 链缺少 .catch()
api.asyncMethod().then((result) => {
  expect(result).assertEqual(expected);
});
```

---

## 20. 多异步接口并发调用必须隔离 (R203)

同一个 `it()` 内并发调用多个异步接口时，每个接口的返回/错误必须独立断言，不能让一个接口的错误影响另一个接口的结果判断。（时序交叉会导致断言对象混淆，一个接口的超时被误判为另一个接口的错误）

```typescript
// ✅️ 串行 await，每个独立断言
let result1 = await api.method1();
expect(result1).assertEqual(expected1);
let result2 = await api.method2();
expect(result2).assertEqual(expected2);
```

```typescript
// ❌ 并发调用未隔离
let [r1, r2] = await Promise.all([api.method1(), api.method2()]);
// 如果 method1 抛出，method2 的结果无法断言
```

---

## 21. 资源创建后必须释放 (R204)

通过 `on()`/`subscribe()` 注册的监听器、打开的连接、创建的对象，必须在 `afterEach` 或 `finally` 中对应 `off()`/`unsubscribe()`/`close()`/`release()`。（未释放的资源会累积导致内存泄漏，影响后续测试执行和设备稳定性）

```typescript
// ✅️ it() 注册监听 + afterEach 释放
it('test001', ..., () => {
  emitter.on('event', callback);
  expect(result).assertEqual(expected);
});
afterEach(() => {
  if (observer) {
    observer.off('event', callback);
  }
});
```

```typescript
// ❌ it() 注册监听但未在 afterEach 中释放
it('test001', ..., () => {
  emitter.on('event', callback);
  // afterEach 中没有对应的 emitter.off()
});
```

---

## 22. beforeAll/beforeEach 必须有配对的 afterAll/afterEach (R205)

如果存在 `beforeAll` 或 `beforeEach`，必须存在对应的 `afterAll` 或 `afterEach`，即使 after 钩子为空也必须声明。（缺少配对的 after 钩子意味着资源分配后没有回收路径，环境状态会泄漏到后续测试）

```typescript
// ✅️ before/after 钩子配对
beforeAll(() => { /* setup */ });
afterAll(() => { /* teardown */ });
beforeEach(() => { /* setup */ });
afterEach(() => { /* teardown */ });
```

```typescript
// ❌ 缺少 after 钩子
beforeAll(() => { /* setup */ });
beforeEach(() => { /* setup */ });
```

---

## 23. 801 设备能力防护完整性 (R030)

当 API 的 `@throws` 声明了 801 错误码时，该 API 的所有用例（PARAM/RETURN/BOUNDARY/EVENT 等）都必须包裹 801 防护逻辑：try 块执行正常场景，catch 块判断 `error.code === 801`→正常通过，其他→`expect().assertFail()`。（不包裹 801 防护的用例在不支持该能力的设备上会因 801 异常而失败，这些失败与被测 API 的逻辑正确性无关，属于设备差异导致的误报）

```typescript
// ✅️ API @throws 含 801 时，正常用例包裹 801 防护
it('testMethod0100', ..., () => {
  let errCodeCapabilityNotSupported = 801;
  try {
    let result = api.method(param);
    expect(result).assertEqual(expected);
  } catch (error) {
    expect(error.code).assertEqual(errCodeCapabilityNotSupported);
  }
});
```

```typescript
// ❌ API @throws 含 801，但正常用例未包裹防护
it('testMethod0100', ..., () => {
  let result = api.method(param);  // 不支持设备上抛 801，测试失败
  expect(result).assertEqual(expected);
});
```
