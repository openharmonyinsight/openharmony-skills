# XTS测试代码质量检查 - 测试技术问题规则详情

本文档包含6条测试技术问题规则（R201-R206）的核心信息，包括问题描述、检测模式、正反例、关键陷阱。

**规则分类**：检测异步安全、资源管理、测试设计等运行时风险

---

## R201 - 异步用例缺少done回调或未await

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
在Hypium测试框架中，当`it()`回调函数体内包含异步操作（如`setTimeout`、回调函数、Promise `.then()`、未await的Promise调用）时，必须通过done回调或async/await确保框架能正确等待异步操作完成。

### 检测模式
```python
# 异步操作模式
async_patterns = [
    r'\bsetTimeout\s*\(',
    r'\bsetInterval\s*\(',
    r'\.\s*then\s*\(',
    r'\bnew\s+Promise\s*[<(]',
    r'(?:callback|cb|onComplete|onSuccess|onError|onResult)\s*[,\)]',
]

# done回调检测
r'\bdone\s*\(\s*\)'
r'async\s*\(\s*done\s*:'
```

### 检测逻辑说明
检测以下问题场景：
1. **非async用例包含异步操作**：缺少done参数
2. **async用例缺少done参数**：存在未await的.then()链式调用
3. **done参数声明但未调用**：将导致用例超时
4. **done未在所有执行路径上调用**：如catch分支缺失done()

**不检测的场景**（合法混用模式）：
- `async (done: Function)` 用例：即使存在.then()调用，只要done在回调中正确调用，测试是安全的
- done作为参数传递给其他函数（如`someFunc(done)`）

### 反例
```typescript
// 缺少done回调（非async用例）
it('testAsync', Level.LEVEL0, () => {
    setTimeout(() => {
        expect(result).assertEqual('expected');  // ✗ 缺少done回调
    }, 1000);
});

// catch中未调用done()
it('testAsync', Level.LEVEL0, async (done: Function) => {
    try {
        let result = await someApi();
        done();
    } catch (err) {
        console.error(err);  // ✗ catch中未调用done()
    }
});

// async用例缺少done参数且有未await的.then()
it('testAsync', Level.LEVEL0, async () => {
    someApi().then(data => {  // ✗ async用例中未await
        expect(data).assertEqual('expected');
    });
});
```

### 正例
```typescript
// done回调模式
it('testAsync', Level.LEVEL0, async (done: Function) => {
    setTimeout(() => {
        expect(result).assertEqual('expected');
        done();  // ✓ 调用done
    }, 1000);
});

// async/await模式
it('testAsync', Level.LEVEL0, async () => {
    await someApi();  // ✓ 使用await
    expect(result).assertEqual('expected');
});

// async+done混用模式（合法）
it('testAsync', Level.LEVEL0, async (done: Function) => {
    someApi().then(data => {  // ✓ 虽然有.then()，但done在回调中调用
        expect(data).assertEqual('expected');
        done();
    });
});

// done覆盖所有路径
it('testAsync', Level.LEVEL0, async (done: Function) => {
    try {
        let result = await someApi();
        done();
    } catch (err) {
        console.error(err);
        done();  // ✓ catch中也调用done()
    }
});
```

### JavaScript文件特殊处理
对于`.js`文件，done参数检测模式为：
```javascript
// JavaScript中常见的done声明方式
it('testName', Level.LEVEL0, async function (done) {  // ✓ 测测此模式
    // ...
});
```

检测正则：`\bdone\s*(?:\(\s*\)|:|\b)`，兼容TypeScript类型注解和JavaScript无类型注解两种风格。

### 关键陷阱
1. **封装函数检测**：需追踪wrapper函数内部的异步操作，最大深度3层（同文件）
2. **跨文件封装函数**：需解析import并追踪到源文件，最大深度2层
3. **done()必须覆盖所有执行路径**：包括catch分支

### ArkTS-Sta 特化检测

> **Sta 工程额外检测**: Promise executor 声明为 async（`new Promise(async () => {})`），这在 Sta 中是运行时风险模式。已由 `complex_rules.py` 的 `_check_sta_async_executor()` 实现。
> 
> **Sta 编译器已拦截**: `done: Function` 类型声明在 Sta 中编译报错（10605008），但 `done: () => void` 是合法的，仍需扫描检测是否正确调用。

---

## R202 - 异步回调/Promise未正确处理错误

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
异步回调函数或Promise链中未正确处理错误（未使用catch、未在回调参数中处理err）。

### 检测模式
```python
# .then()无catch
r'\.\s*then\s*\([^)]*\)\s*(?!\.\s*catch)'

# 回调函数缺少err参数
r'(?:callback|onSuccess|onComplete)\s*=\s*\([^)]*\)\s*=>'
```

### 反例
```typescript
someApi().then(result => {  // ✗ 无catch处理
    expect(result).assertEqual('expected');
});

someApi((result) => {  // ✗ 回调缺少err参数
    expect(result).assertEqual('expected');
});
```

### 正例
```typescript
// Promise链添加catch
someApi()
    .then(result => {
        expect(result).assertEqual('expected');
    })
    .catch(err => {  // ✓ 有catch处理
        expect(err.code).assertEqual(401);
    });

// 回调函数包含err参数
someApi((err, result) => {  // ✓ 包含err参数
    if (err) {
        expect(err.code).assertEqual(401);
    } else {
        expect(result).assertEqual('expected');
    }
});
```

### ArkTS-Sta 特化检测

> **Sta 工程额外检测**: `reject` 传入非 Error 类型对象（如 `reject("string")`），这在 Sta 严格类型系统下仍可能发生。已由 `complex_rules.py` 的 Sta 分支实现。

---

## R203 - 多异步接口并发调用无隔离导致时序异常

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
多个异步接口并发调用时缺乏隔离机制，导致时序异常（如状态竞争、回调交叉）。

### 检测模式
检测同一用例内多个异步接口并发调用，且缺乏await或串行化机制。

### 反例
```typescript
it('testConcurrent', Level.LEVEL0, async () => {
    someApi1();  // ✗ 未await，并发调用
    someApi2();  // ✗ 未await，并发调用
    // 缺乏隔离机制
});
```

### 正例
```typescript
it('testConcurrent', Level.LEVEL0, async () => {
    await someApi1();  // ✓ 串行化
    await someApi2();  // ✓ 串行化
});
```

---

## R204 - 资源创建后未释放

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
资源（监听器、连接、对象等）创建后未在适当位置释放。

### 检测模式
```python
# 监听器注册
r'\.(on|subscribe|addListener|addEventListener)\s*\('

# 检查是否有对应的off/unsubscribe/removeListener
```

### 反例
```typescript
emitter.on('event', callback);  // ✗ 注册监听器但未释放
// 用例结束未调用emitter.off()
```

### 正例
```typescript
emitter.on('event', callback);
// 用例结束时
emitter.off('event');  // ✓ 释放监听器
```

---

## R205 - beforeAll/beforeEach存在但缺少配对的afterAll/afterEach

**严重级别**: Critical  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
`beforeAll`/`beforeEach`存在但缺少配对的`afterAll`/`afterEach`，导致资源未释放。

### 检测模式
```python
# 检测before钩子
r'beforeAll\s*\('
r'beforeEach\s*\('

# 检查是否有对应的after钩子
```

### 反例
```typescript
beforeAll(() => {  // ✗ 有beforeAll但无afterAll
    resource = createResource();
});
```

### 正例
```typescript
beforeAll(() => {
    resource = createResource();
});
afterAll(() => {  // ✓ 配对的afterAll
    releaseResource(resource);
});
```

---

## R206 - 用例间存在隐式依赖

**严重级别**: Warning  
**扫描范围**: 所有源代码文件（.ets, .ts, .js）

### 问题描述
用例间存在隐式依赖，导致用例执行顺序敏感。

**Sta工程**：检测EAWorker共享对象
**Dyn工程**：检测全局状态共享（`globalThis`）

### 检测模式
```python
# Sta工程: EAWorker共享对象
r'EAWorker'

# Dyn工程: globalThis状态共享
r'globalThis\s*\.\s*\w+'
```

### 反例
```typescript
// 用例A修改全局状态
globalThis.sharedState = 'value';  // ✗ 全局状态共享

// 用例B依赖用例A的状态
expect(globalThis.sharedState).assertEqual('value');  // ✗ 隐式依赖
```

### 正例
```typescript
// 每个用例独立，不依赖全局状态
it('testA', Level.LEVEL0, () => {
    let localState = 'value';  // ✓ 局部变量
    expect(localState).assertEqual('value');
});
```

### ArkTS-Sta 特化检测

> **Sta 工程**: 检测 EAWorker 共享对象（SharedArrayBuffer、Atomics、SharedMap、SharedSet）在多用例间的隐式依赖。`globalThis` 在 Sta 中编译报错，不检测。
> 
> **Dyn 工程**: 检测 `globalThis` 全局状态共享和 describe 块级共享变量被多用例修改。

---

## 规则统计

| 类别 | 规则数 | 规则编号 |
|------|--------|---------|
| **Critical** | 5 | R201-R205 |
| **Warning** | 1 | R206 |
| **异步/时序安全** | 3 | R201-R203 |
| **资源管理** | 2 | R204-R205 |
| **测试设计** | 1 | R206 |

---

## 参考文档

- [references/TRAPS.md](TRAPS.md) - 已知扫描陷阱（44个）
- [references/RULES_COMPLIANCE.md](RULES_COMPLIANCE.md) - 编码规范合规规则详情（R001-R023）
- [guides/FIX_GUIDE.md](../guides/FIX_GUIDE.md) - 问题修复指南